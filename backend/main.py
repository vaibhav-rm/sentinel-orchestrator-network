from fastapi import FastAPI, WebSocket, BackgroundTasks, HTTPException
from pydantic import BaseModel
from message_bus import MessageBus
from agents import SentinelAgent, OracleAgent
import uuid
import logging
import json
import base64
from datetime import datetime

# Initialize Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Sentinel Orchestrator Network (SON)",
    description="Blockchain security scanning with Sentinel & Oracle agents",
    version="1.0.0"
)

# Initialize MessageBus
message_bus = MessageBus()

# Initialize Agents
sentinel = SentinelAgent(enable_llm=True)
oracle = OracleAgent(enable_llm=True)

# Connect agents to each other
sentinel.set_oracle(oracle)

# Register agents with MessageBus
message_bus.register_agent("did:masumi:sentinel_01", sentinel.get_public_key_b64())
message_bus.register_agent("did:masumi:oracle_01", oracle.get_public_key_b64())

logger.info("✅ Sentinel and Oracle agents initialized and connected")


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class ScanRequest(BaseModel):
    """Request model for policy/transaction scan"""
    policy_id: str = None
    tx_cbor: str = None
    user_tip: int = 0  # User's node block height
    
    class Config:
        example = {
            "policy_id": "a" * 56,
            "user_tip": 1000
        }


class ScanResponse(BaseModel):
    """Response model for scan results"""
    task_id: str
    status: str
    policy_id: str = None
    verdict: str = None
    risk_score: int = None
    reason: str = None
    timestamp: str = None


# =============================================================================
# BACKGROUND TASK: SENTINEL AGENT SCAN
# =============================================================================

async def run_sentinel_scan(policy_id: str, user_tip: int, task_id: str):
    """
    Run the Sentinel agent scan in background.
    Publishes results to MessageBus for WebSocket clients.
    """
    try:
        logger.info(f"[{task_id}] Starting Sentinel scan for policy: {policy_id[:16]}...")
        
        # Run Sentinel agent
        result = await sentinel.process({
            "policy_id": policy_id,
            "user_tip": user_tip,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
        
        # Build response envelope for MessageBus
        response_envelope = {
            "sender_did": "did:masumi:sentinel_01",
            "payload": {
                "task_id": task_id,
                "policy_id": policy_id,
                "verdict": result.get("verdict"),
                "risk_score": result.get("risk_score"),
                "reason": result.get("reason"),
                "compliance": result.get("compliance"),
                "oracle_result": result.get("oracle_result"),
                "evidence_hash": result.get("evidence_hash"),
                "timestamp": result.get("timestamp"),
                "status": "completed"
            }
        }
        
        # Sign the envelope
        signed_envelope = sentinel._sign_envelope(response_envelope)
        
        # Publish to MessageBus
        await message_bus.publish(signed_envelope)
        
        logger.info(f"[{task_id}] Scan completed. Verdict: {result.get('verdict')}")
        
    except Exception as e:
        logger.error(f"[{task_id}] Scan failed: {str(e)}")
        
        # Publish error envelope
        error_envelope = {
            "sender_did": "did:masumi:sentinel_01",
            "payload": {
                "task_id": task_id,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
        signed_error = sentinel._sign_envelope(error_envelope)
        await message_bus.publish(signed_error)


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "operational",
        "service": "Sentinel Orchestrator Network (SON)",
        "agents": {
            "sentinel": "Agent A - Orchestrator & Compliance Checker",
            "oracle": "Agent B - Blockchain Verifier & Fork Detection"
        }
    }


@app.post("/api/v1/scan", response_model=ScanResponse)
async def scan(request: ScanRequest, background_tasks: BackgroundTasks):
    """
    Submit a policy/transaction for security scanning.
    
    Returns a task_id that can be used to listen for results via WebSocket.
    """
    # Validate input
    if not request.policy_id and not request.tx_cbor:
        raise HTTPException(
            status_code=400,
            detail="Either policy_id or tx_cbor must be provided"
        )
    
    task_id = str(uuid.uuid4())
    
    logger.info(f"[{task_id}] Received scan request - policy: {request.policy_id or 'N/A'}")
    
    # Trigger Sentinel agent in background
    background_tasks.add_task(
        run_sentinel_scan,
        request.policy_id or request.tx_cbor,
        request.user_tip,
        task_id
    )
    
    return ScanResponse(
        task_id=task_id,
        status="initiated",
        policy_id=request.policy_id,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )


@app.get("/api/v1/agents/info")
async def agents_info():
    """Get information about registered agents"""
    return {
        "sentinel": {
            "did": "did:masumi:sentinel_01",
            "role": "orchestrator",
            "public_key": sentinel.get_public_key_b64()[:20] + "...",
            "status": "active"
        },
        "oracle": {
            "did": "did:masumi:oracle_01",
            "role": "verifier",
            "public_key": oracle.get_public_key_b64()[:20] + "...",
            "status": "active",
            "specialists": list(oracle.specialists.keys())
        }
    }


# =============================================================================
# WEBSOCKET ENDPOINT FOR REAL-TIME RESULTS
# =============================================================================

@app.websocket("/ws/scan/{task_id}")
async def websocket_scan(websocket: WebSocket, task_id: str):
    """
    WebSocket endpoint to receive real-time scan results.
    
    Clients connect with: ws://localhost:8000/ws/scan/{task_id}
    Server publishes results when Sentinel completes the scan.
    """
    await message_bus.connect(websocket)
    logger.info(f"Client connected to scan results: {task_id}")
    
    try:
        while True:
            # Keep connection open and receive messages
            data = await websocket.receive_text()
            logger.debug(f"Received from client [{task_id}]: {data}")
            
    except Exception as e:
        logger.info(f"WebSocket closed for task {task_id}: {str(e)}")
    finally:
        message_bus.disconnect(websocket)


@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    """
    General WebSocket endpoint for agent activity logs.
    Broadcasts all agent events.
    """
    await message_bus.connect(websocket)
    logger.info("Client connected to activity logs")
    
    try:
        while True:
            await websocket.receive_text()
    except Exception as e:
        logger.info(f"WebSocket closed: {str(e)}")
    finally:
        message_bus.disconnect(websocket)
