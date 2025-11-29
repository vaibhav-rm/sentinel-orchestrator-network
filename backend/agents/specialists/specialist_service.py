"""
Specialist Service Wrapper for KODOSUMI Deployment
===================================================

This wrapper allows each specialist agent to run as an independent microservice
on KODOSUMI with FastAPI, health checks, and agent registration.

Usage:
    python specialist_service.py <specialist_name>
    
    Example:
        python specialist_service.py block_scanner
"""

import asyncio
import os
import sys
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

# Setup logging
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("SON.Specialist")

# Import specialist classes
try:
    from block_scanner import BlockScanner
    from stake_analyzer import StakeAnalyzer
    from vote_doctor import VoteDoctor
    from mempool_sniffer import MempoolSniffer
    from replay_detector import ReplayDetector
except ImportError:
    from .block_scanner import BlockScanner
    from .stake_analyzer import StakeAnalyzer
    from .vote_doctor import VoteDoctor
    from .mempool_sniffer import MempoolSniffer
    from .replay_detector import ReplayDetector


# Specialist mapping
SPECIALISTS = {
    "block_scanner": BlockScanner,
    "stake_analyzer": StakeAnalyzer,
    "vote_doctor": VoteDoctor,
    "mempool_sniffer": MempoolSniffer,
    "replay_detector": ReplayDetector,
}


class ScanRequest(BaseModel):
    """Request model for specialist scan"""
    address: str
    context: Optional[Dict[str, Any]] = None


class RegistrationPayload(BaseModel):
    """DID registration payload"""
    did: str
    public_key: str
    service_name: str
    service_url: str
    service_port: int


def create_specialist_app(specialist_instance) -> FastAPI:
    """Create FastAPI app for a specialist agent."""
    app = FastAPI(
        title=f"SON {specialist_instance.name}",
        description=f"Specialist agent for {specialist_instance.name}",
        version="1.0.0"
    )
    
    # =======================================================================
    # HEALTH CHECK ENDPOINT
    # =======================================================================
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint for Kubernetes/container orchestration."""
        return {
            "status": "healthy",
            "service": specialist_instance.name,
            "did": specialist_instance.did,
        }
    
    # =======================================================================
    # SCAN ENDPOINT
    # =======================================================================
    
    @app.post("/api/v1/scan")
    async def scan(request: ScanRequest):
        """Execute scan operation."""
        try:
            result = await specialist_instance.scan(
                request.address,
                request.context or {}
            )
            
            # Convert to dict
            result_dict = {
                "agent": specialist_instance.name,
                "did": specialist_instance.did,
                "risk_score": result.risk_score,
                "severity": result.severity.value,
                "findings": result.findings,
                "metadata": result.metadata,
                "success": result.success,
                "error": result.error,
            }
            
            # Sign the response if we have the method
            if hasattr(specialist_instance, '_sign_response'):
                signed_result = specialist_instance._sign_response(result_dict)
                return signed_result
            
            return result_dict
            
        except Exception as e:
            logger.error(f"Scan failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    # =======================================================================
    # AGENT INFO ENDPOINT
    # =======================================================================
    
    @app.get("/api/v1/agent/info")
    async def agent_info():
        """Get agent information."""
        return {
            "name": specialist_instance.name,
            "did": specialist_instance.did,
            "public_key": specialist_instance.get_public_key_b64()[:30] + "...",
            "version": "1.0.0",
            "protocol": "IACP/2.0",
        }
    
    # =======================================================================
    # REGISTRATION ENDPOINT (Called by KODOSUMI registry)
    # =======================================================================
    
    @app.post("/api/v1/register")
    async def register_with_registry(payload: RegistrationPayload):
        """Register this specialist with the KODOSUMI registry."""
        try:
            registry_url = os.getenv("KODOSUMI_REGISTRY_URL", "http://localhost:8080")
            
            registration = {
                "did": specialist_instance.did,
                "name": specialist_instance.name,
                "public_key": specialist_instance.get_public_key_b64(),
                "service_url": f"http://{os.getenv('HOSTNAME', 'localhost')}:8000",
                "protocol": "IACP/2.0",
                "capabilities": ["scan"],
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{registry_url}/api/v1/agents/register",
                    json=registration,
                    timeout=5.0,
                )
                
                if response.status_code == 200:
                    logger.info(f"✅ {specialist_instance.name} registered with KODOSUMI")
                    return {
                        "status": "registered",
                        "did": specialist_instance.did,
                        "registry": registry_url,
                    }
                else:
                    logger.warning(f"Registry returned {response.status_code}")
                    return {
                        "status": "registration_failed",
                        "error": response.text,
                    }
                    
        except Exception as e:
            logger.error(f"Registration failed: {e}")
            return {
                "status": "registration_error",
                "error": str(e),
            }
    
    return app


async def auto_register_with_registry(specialist_instance):
    """Automatically register specialist with KODOSUMI registry on startup."""
    await asyncio.sleep(2)  # Give registry time to start
    
    registry_url = os.getenv("KODOSUMI_REGISTRY_URL", "http://localhost:8080")
    
    for attempt in range(5):
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                registration = {
                    "did": specialist_instance.did,
                    "name": specialist_instance.name,
                    "public_key": specialist_instance.get_public_key_b64(),
                    "service_url": f"http://localhost:8000",
                    "protocol": "IACP/2.0",
                    "capabilities": ["scan"],
                }
                
                response = await client.post(
                    f"{registry_url}/api/v1/agents/register",
                    json=registration,
                )
                
                if response.status_code in [200, 201]:
                    logger.info(f"✅ {specialist_instance.name} auto-registered with KODOSUMI")
                    return
                    
        except Exception as e:
            logger.debug(f"Registration attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(2)


def run_specialist_service(specialist_name: str):
    """Run a specialist agent as a standalone service."""
    import uvicorn
    
    if specialist_name not in SPECIALISTS:
        print(f"Unknown specialist: {specialist_name}")
        print(f"Available specialists: {list(SPECIALISTS.keys())}")
        sys.exit(1)
    
    # Create specialist instance
    specialist_class = SPECIALISTS[specialist_name]
    specialist = specialist_class()
    
    logger.info(f"Starting {specialist.name} service...")
    logger.info(f"DID: {specialist.did}")
    logger.info(f"Public Key: {specialist.get_public_key_b64()[:30]}...")
    
    # Create FastAPI app
    app = create_specialist_app(specialist)
    
    # Add startup task for registry registration
    @app.on_event("startup")
    async def startup():
        asyncio.create_task(auto_register_with_registry(specialist))
    
    # Run server
    port = int(os.getenv("SERVICE_PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        specialist_name = os.getenv("SERVICE_NAME", "block_scanner").lower().replace("_", "_")
    else:
        specialist_name = sys.argv[1].lower()
    
    run_specialist_service(specialist_name)
