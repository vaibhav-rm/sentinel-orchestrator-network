# 🏗️ System Architecture

## Complete Technical Architecture Documentation

---

## 1. OVERVIEW

### Architecture Principles

SON is built on four core architectural principles:

1. **Modularity**: Security and Governance modules operate independently
2. **Scalability**: Horizontal scaling via Kubernetes microservices
3. **Resilience**: Multi-source redundancy and graceful degradation
4. **Observability**: Comprehensive logging and real-time monitoring

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Dashboard   │  │    Wallet    │  │   Mobile     │ │
│  │  (Next.js)   │  │  Extension   │  │   (Future)   │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
└─────────┼──────────────────┼──────────────────┼─────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │ HTTP/WebSocket
┌─────────────────────────────┼────────────────────────────┐
│                    APPLICATION LAYER                      │
│              ┌───────────────────────────┐                │
│              │  API Gateway (FastAPI)    │                │
│              │  • Authentication         │                │
│              │  • Rate limiting          │                │
│              │  • Request routing        │                │
│              └───────────┬───────────────┘                │
└─────────────────────────┼────────────────────────────────┘
                          │
┌─────────────────────────┼────────────────────────────────┐
│                   ORCHESTRATION LAYER                     │
│     ┌────────────────────┴─────────────────────┐         │
│     │        Message Bus (Redis Pub/Sub)       │         │
│     │  • agent:sentinel:inbox                  │         │
│     │  • agent:oracle:inbox                    │         │
│     │  • agent:governance:inbox                │         │
│     │  • broadcast:all                         │         │
│     └──┬─────────────────────────────────┬─────┘         │
└────────┼─────────────────────────────────┼───────────────┘
         │                                 │
    ┌────┴────┐                       ┌────┴────┐
    │         │                       │         │
    ▼         ▼                       ▼         ▼
┌──────────────────────┐      ┌──────────────────────┐
│  SECURITY MODULE     │      │  GOVERNANCE MODULE   │
│                      │      │                      │
│  ┌────────────────┐  │      │  ┌────────────────┐ │
│  │ Sentinel Agent │  │      │  │   Governance   │ │
│  └───────┬────────┘  │      │  │  Orchestrator  │ │
│          │           │      │  └───────┬────────┘ │
│          ▼           │      │          │          │
│  ┌────────────────┐  │      │          ▼          │
│  │  Oracle Agent  │  │      │  ┌────────────────┐ │
│  └───────┬────────┘  │      │  │ ProposalFetcher│ │
│          │           │      │  │ PolicyAnalyzer │ │
│          ▼           │      │  │SentimentAnalyzer│ │
│  ┌────────────────┐  │      │  └────────────────┘ │
│  │ 5 Specialists: │  │      └──────────────────────┘
│  │ • BlockScanner │  │
│  │ • StakeAnalyzer│  │
│  │ • VoteDoctor   │  │
│  │ • MempoolSniff │  │
│  │ • ReplayDetect │  │
│  └────────────────┘  │
└──────────────────────┘
         │                                 │
         └────────────┬────────────────────┘
                      │
┌─────────────────────┼────────────────────────────────────┐
│                  DATA LAYER                               │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────┐ │
│  │  PostgreSQL    │  │  Redis Cache   │  │  IPFS      │ │
│  │  • Scan logs   │  │  • Active tasks│  │  • Metadata│ │
│  │  • ThreatProofs│  │  • TX patterns │  │            │ │
│  │  • Audit trail │  │  • Proposals   │  │            │ │
│  └────────────────┘  └────────────────┘  └────────────┘ │
└───────────────────────────────────────────────────────────┘
                      │
┌─────────────────────┼────────────────────────────────────┐
│             BLOCKCHAIN INTEGRATION LAYER                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────┐ │
│  │  Blockfrost    │  │     Koios      │  │   Mesh     │ │
│  │  (Primary API) │  │   (Fallback)   │  │  (TX Sign) │ │
│  └────────────────┘  └────────────────┘  └────────────┘ │
│                                                           │
│  ┌────────────────┐  ┌────────────────┐                 │
│  │     Masumi     │  │     Gemini     │                 │
│  │  (Micropayment)│  │   (AI Engine)  │                 │
│  └────────────────┘  └────────────────┘                 │
└───────────────────────────────────────────────────────────┘
```

---

## 2. DETAILED COMPONENT ARCHITECTURE

### 2.1 API Gateway Layer

#### FastAPI Application

```python
# Main application structure
app = FastAPI(
    title="Sentinel Orchestrator Network",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware stack
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=60,
    burst_size=10
)

app.add_middleware(
    AuthenticationMiddleware,
    jwt_secret=os.getenv("JWT_SECRET"),
    excluded_paths=["/health", "/docs"]
)
```

#### Endpoint Structure

**Security Module Endpoints:**
```
POST   /api/v1/scan/transaction     # Scan transaction for threats
POST   /api/v1/scan/policy          # Scan policy ID
GET    /api/v1/scan/{task_id}       # Get scan results
WS     /ws/scan/{task_id}           # Real-time scan updates
```

**Governance Module Endpoints:**
```
POST   /api/v1/governance/analyze   # Analyze proposal
POST   /api/v1/governance/vote      # Submit vote transaction
GET    /api/v1/governance/proposals # List active proposals
GET    /api/v1/governance/{id}      # Get proposal details
```

**Agent Management Endpoints:**
```
GET    /api/v1/agents/info          # Get agent registry
GET    /api/v1/agents/{did}/status  # Agent health check
POST   /api/v1/agents/register      # Register new agent
WS     /ws/logs                     # Global agent activity stream
```

---

### 2.2 Message Bus Architecture

#### Redis Pub/Sub Channels

```python
CHANNELS = {
    # Agent-specific inboxes
    "agent:sentinel:inbox": "Commands for Sentinel",
    "agent:oracle:inbox": "Commands for Oracle",
    "agent:governance:inbox": "Commands for Governance Orchestrator",
    
    # Broadcast channels
    "broadcast:all": "System-wide announcements",
    "broadcast:alerts": "Critical alerts",
    
    # Result channels
    "results:scan:{task_id}": "Scan result streaming",
    "results:governance:{proposal_id}": "Governance analysis results",
    
    # Activity logging
    "logs:activity": "Agent activity logs",
    "logs:errors": "Error tracking"
}
```

#### Message Flow Example

```python
# Sentinel publishes HIRE_REQUEST
message = {
    "protocol": "IACP/2.0",
    "type": "HIRE_REQUEST",
    "from_did": "did:masumi:sentinel_01",
    "to_did": "did:masumi:oracle_01",
    "payload": {
        "task": "fork_check",
        "policy_id": "abc123...",
        "escrow_id": "escrow_888"
    },
    "timestamp": "2025-01-30T12:00:01Z",
    "signature": "Ed25519_sig..."
}

await redis.publish("agent:oracle:inbox", json.dumps(message))

# Oracle subscribes and processes
async def handle_oracle_inbox():
    pubsub = redis.pubsub()
    await pubsub.subscribe("agent:oracle:inbox")
    
    async for message in pubsub.listen():
        if message["type"] == "message":
            request = json.loads(message["data"])
            result = await process_hire_request(request)
            await redis.publish("agent:sentinel:inbox", json.dumps(result))
```

---

### 2.3 Security Module Architecture

#### Agent Hierarchy

```
Sentinel Agent (Coordinator)
    │
    ├─ Protocol Compliance Check (Local)
    │   ├─ CBOR Parsing
    │   ├─ Field Validation
    │   └─ Metadata Check
    │
    └─ Oracle Agent (Hired via IACP)
        │
        ├─ Specialist Spawning (Parallel)
        │   ├─ BlockScanner (800ms avg)
        │   ├─ StakeAnalyzer (1200ms avg)
        │   ├─ VoteDoctor (900ms avg)
        │   ├─ MempoolSniffer (1100ms avg)
        │   └─ ReplayDetector (1400ms avg)
        │
        ├─ Result Collection
        │   └─ asyncio.gather(*specialists, timeout=10)
        │
        └─ Bayesian Fusion
            ├─ Weighted Risk Aggregation
            ├─ Severity Override Logic
            └─ Confidence Calculation
```

#### Data Flow Diagram

```
User Request
    │
    ▼
API Gateway
    │ validate_request()
    ▼
Sentinel Agent
    │ check_protocol_compliance()
    ├─ [VALID] → Continue
    └─ [INVALID] → Return DANGER verdict
    │
    ▼
Generate HIRE_REQUEST
    │ sign_with_ed25519()
    ▼
Redis: agent:oracle:inbox
    │
    ▼
Oracle Agent
    │ verify_signature()
    │ spawn_specialists()
    ▼
[Parallel Execution]
    ├─ BlockScanner → Query 5 RPC providers
    ├─ StakeAnalyzer → Query stake pools
    ├─ VoteDoctor → Query governance data
    ├─ MempoolSniffer → Query mempool
    └─ ReplayDetector → Query Redis bloom filter
    │
    ▼
Bayesian Fusion
    │ weighted_risk = Σ(risk_i × weight_i)
    │ confidence = successful_agents / 5
    ▼
Generate HIRE_RESPONSE
    │ sign_with_ed25519()
    ▼
Redis: agent:sentinel:inbox
    │
    ▼
Sentinel Agent
    │ verify_signature()
    │ aggregate_verdict()
    ▼
Generate ThreatProof Capsule
    │ store_in_postgres()
    │ cache_in_redis(ttl=3600)
    ▼
Return to User (WebSocket)
```

---

### 2.4 Governance Module Architecture

#### Pipeline Structure

```
User Request (Analyze Proposal)
    │
    ▼
Governance Orchestrator
    │
    ├─ Step 1: ProposalFetcher
    │   ├─ Try IPFS Gateway 1 (ipfs.io)
    │   ├─ Try IPFS Gateway 2 (cloudflare-ipfs.com)
    │   ├─ Try IPFS Gateway 3 (pinata)
    │   ├─ Try IPFS Gateway 4 (dweb.link)
    │   └─ Fallback: Redis Cache
    │   │
    │   ▼
    │   Parse CIP-100/108 Metadata
    │       ├─ title
    │       ├─ abstract
    │       ├─ motivation
    │       ├─ rationale
    │       ├─ amount
    │       └─ references
    │
    ├─ Step 2: PolicyAnalyzer
    │   │
    │   ├─ Layer 1: Hardcoded Rules (50ms)
    │   │   ├─ Treasury Cap Check (50M ADA)
    │   │   ├─ Marketing Cap Check (5M ADA)
    │   │   └─ Deliverables Check (keywords)
    │   │
    │   └─ Layer 2: Gemini AI Analysis (1800ms)
    │       ├─ Prompt Construction
    │       ├─ API Call (1M context window)
    │       ├─ JSON Parsing
    │       └─ Flag Merging
    │
    └─ Step 3: SentimentAnalyzer
        │
        ├─ Query Blockfrost (600ms)
        │   └─ GET /governance/proposals/{id}/votes
        │
        ├─ Calculate Stake-Weighted Support
        │   ├─ yes_power = Σ(voting_power where vote=yes)
        │   ├─ no_power = Σ(voting_power where vote=no)
        │   ├─ total = yes_power + no_power + abstain_power
        │   └─ support_pct = (yes_power / total) × 100
        │
        └─ Categorize Sentiment
            ├─ >70% = STRONG_SUPPORT
            ├─ >50% = MODERATE_SUPPORT
            ├─ >30% = DIVIDED
            └─ <30% = STRONG_OPPOSITION
    │
    ▼
Verdict Aggregation
    │
    ├─ Rule 1: flags >= 2 → NO (confidence: 0.9)
    ├─ Rule 2: support < 30% → NO (confidence: 0.85)
    ├─ Rule 3: amount > 25M ADA → ABSTAIN (confidence: 0.7)
    ├─ Rule 4: AI confidence > 0.7 → Follow AI
    └─ Default: ABSTAIN (confidence: 0.5)
    │
    ▼
Return Complete Analysis
    ├─ Store in PostgreSQL
    ├─ Cache in Redis (TTL: 1hr)
    └─ Stream to User (WebSocket)
```

---

### 2.5 Data Layer Architecture

#### PostgreSQL Schema

```sql
-- Scan history table
CREATE TABLE scans (
    scan_id UUID PRIMARY KEY,
    user_address VARCHAR(255),
    policy_id VARCHAR(56),
    tx_hash VARCHAR(64),
    verdict VARCHAR(20) NOT NULL, -- SAFE, WARNING, DANGER
    risk_score INTEGER NOT NULL, -- 0-100
    reason TEXT,
    sentinel_signature TEXT,
    oracle_signature TEXT,
    evidence_hash VARCHAR(64),
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_user_address (user_address),
    INDEX idx_created_at (created_at)
);

-- Specialist results table (for debugging)
CREATE TABLE specialist_results (
    result_id UUID PRIMARY KEY,
    scan_id UUID REFERENCES scans(scan_id),
    agent_name VARCHAR(50) NOT NULL,
    risk_score FLOAT NOT NULL,
    severity VARCHAR(20) NOT NULL,
    findings JSONB,
    metadata JSONB,
    success BOOLEAN,
    execution_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Governance analysis table
CREATE TABLE governance_analyses (
    analysis_id UUID PRIMARY KEY,
    gov_action_id VARCHAR(100) NOT NULL,
    ipfs_hash VARCHAR(100),
    title TEXT,
    amount_ada BIGINT,
    policy_flags JSONB,
    sentiment_category VARCHAR(50),
    support_percentage FLOAT,
    recommendation VARCHAR(20), -- YES, NO, ABSTAIN
    confidence FLOAT,
    auto_votable BOOLEAN,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(gov_action_id, ipfs_hash)
);

-- Agent registry table
CREATE TABLE agents (
    did VARCHAR(100) PRIMARY KEY,
    agent_name VARCHAR(50) NOT NULL,
    role VARCHAR(50),
    public_key TEXT NOT NULL,
    service_url VARCHAR(255),
    status VARCHAR(20) DEFAULT 'active',
    last_heartbeat TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ThreatProof capsules (immutable audit trail)
CREATE TABLE threat_proofs (
    proof_id UUID PRIMARY KEY,
    scan_id UUID REFERENCES scans(scan_id),
    capsule_json JSONB NOT NULL, -- Complete signed envelope
    ipfs_hash VARCHAR(100), -- For future NFT minting
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Redis Data Structures

```python
# Active task tracking
redis.setex(
    f"task:{task_id}",
    3600,  # 1 hour TTL
    json.dumps({
        "status": "processing",
        "progress": 0.6,
        "current_agent": "BlockScanner"
    })
)

# Transaction pattern bloom filter (replay detection)
redis.sadd(
    "tx_patterns",
    pattern_hash  # 16-char SHA-256 prefix
)
redis.expire("tx_patterns", 3600)  # 1 hour window

# Proposal metadata cache
redis.setex(
    f"proposal:{ipfs_hash}",
    3600,  # 1 hour TTL
    json.dumps(proposal_metadata)
)

# Agent health tracking
redis.hset(
    "agent_health",
    "did:masumi:oracle_01",
    json.dumps({
        "status": "healthy",
        "last_seen": "2025-01-30T12:00:01Z",
        "success_rate": 0.985
    })
)
```

---

### 2.6 Blockchain Integration Layer

#### Multi-Provider Strategy

```python
class BlockchainClient:
    """
    Redundant blockchain data access with automatic failover.
    """
    
    def __init__(self):
        self.providers = [
            BlockfrostProvider(api_key=os.getenv("BLOCKFROST_KEY")),
            KoiosProvider(),  # No API key needed
            DirectNodeProvider(rpc_url=os.getenv("CARDANO_NODE_RPC"))
        ]
    
    async def get_latest_block(self):
        """Try each provider until success."""
        for provider in self.providers:
            try:
                return await provider.get_latest_block()
            except Exception as e:
                logger.warning(f"{provider.name} failed: {e}")
                continue
        
        raise Exception("All blockchain providers failed")
    
    async def get_address_utxos(self, address):
        """Query with automatic failover."""
        for provider in self.providers:
            try:
                return await provider.get_address_utxos(address)
            except Exception:
                continue
        
        raise Exception("Could not fetch UTxOs")
```

#### Transaction Signing Flow

```python
# Using Mesh SDK for wallet integration
from meshsdk import Transaction, Wallet

async def submit_governance_vote(proposal_id, vote, wallet):
    """
    Build and sign governance vote transaction.
    """
    # Build transaction
    tx = Transaction(initiator=wallet)
    
    # Add governance vote certificate
    tx.voteGovernanceAction(
        govActionId=proposal_id,
        vote=vote,  # 'yes', 'no', or 'abstain'
        anchor={
            "url": f"https://son-network.io/votes/{proposal_id}",
            "dataHash": compute_anchor_hash(proposal_id, vote)
        }
    )
    
    # Wallet signs (user confirms in UI)
    signed_tx = await wallet.signTx(tx.build())
    
    # Submit to network
    tx_hash = await wallet.submitTx(signed_tx)
    
    return {
        "tx_hash": tx_hash,
        "status": "submitted",
        "explorer_url": f"https://cardanoscan.io/transaction/{tx_hash}"
    }
```

---

### 2.7 AI Integration Architecture

#### Gemini 2.0 Flash Configuration

```python
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    'gemini-2.0-flash-exp',
    generation_config={
        "response_mime_type": "application/json",  # Native JSON mode
        "temperature": 0.3,  # Low variance for consistency
        "max_output_tokens": 2048,
        "top_p": 0.95
    }
)

# Rate limiting (free tier)
rate_limiter = RateLimiter(
    requests_per_minute=15,
    burst_size=5
)

async def analyze_with_gemini(prompt):
    """
    Query Gemini with rate limiting and retry logic.
    """
    await rate_limiter.acquire()
    
    try:
        response = await asyncio.wait_for(
            model.generate_content_async(prompt),
            timeout=30.0
        )
        return json.loads(response.text)
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        # Fallback to hardcoded rules only
        return fallback_analysis(prompt)
```

---

### 2.8 Frontend Architecture

#### Next.js Application Structure

```
frontend/
├── app/
│   ├── layout.tsx              # Root layout (providers, fonts)
│   ├── page.tsx                # Homepage (landing)
│   ├── dashboard/
│   │   ├── page.tsx            # Main dashboard
│   │   ├── security/
│   │   │   └── page.tsx        # Security scan interface
│   │   └── governance/
│   │       └── page.tsx        # Governance analysis interface
│   └── api/
│       └── [...proxy]/route.ts # API proxy to backend
│
├── components/
│   ├── AgentRadar.tsx          # Real-time agent activity visualization
│   ├── ThreatCard.tsx          # Security verdict display
│   ├── ProposalCard.tsx        # Governance analysis display
│   ├── ScrambleText.tsx        # Matrix-style text animation
│   └── WebSocketProvider.tsx   # WebSocket connection manager
│
├── lib/
│   ├── websocket.ts            # WebSocket client
│   ├── api-client.ts           # Backend API wrapper
│   └── wallet-connector.ts     # Cardano wallet integration
│
└── styles/
    └── globals.css             # TailwindCSS + custom Matrix theme
```

#### WebSocket Integration

```typescript
// Real-time agent activity streaming
import { useWebSocket } from '@/lib/websocket';

export function DashboardPage() {
  const { lastMessage, sendMessage, readyState } = useWebSocket(
    'ws://localhost:8000/ws/logs'
  );
  
  useEffect(() => {
    if (lastMessage) {
      const event = JSON.parse(lastMessage.data);
      
      switch (event.event_type) {
        case 'agent_start':
          showAgentAnimation(event.agent_name, 'start');
          break;
        case 'agent_complete':
          showAgentAnimation(event.agent_name, 'complete');
          updateResults(event.data);
          break;
        case 'agent_error':
          showError(event.agent_name, event.error);
          break;
      }
    }
  }, [lastMessage]);
  
  return (
    <div className="dashboard">
      <AgentRadar />
      <ResultsPanel />
    </div>
  );
}
```

---

## 3. DEPLOYMENT ARCHITECTURE

### 3.1 Development Environment

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - BLOCKFROST_API_KEY=${BLOCKFROST_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - REDIS_URL=redis://redis:6379
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/son
    depends_on:
      - redis
      - postgres
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=son
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 3.2 Production Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: son-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: son-backend
  template:
    metadata:
      labels:
        app: son-backend
    spec:
      containers:
      - name: backend
        image: son/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: BLOCKFROST_API_KEY
          valueFrom:
            secretKeyRef:
              name: son-secrets
              key: blockfrost-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: son-backend-service
spec:
  selector:
    app: son-backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

---

## 4. SECURITY ARCHITECTURE

### 4.1 Authentication & Authorization

```python
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verify JWT token from Authorization header.
    """
    try:
        payload = jwt.decode(
            credentials.credentials,
            os.getenv("JWT_SECRET"),
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/v1/scan")
async def scan_transaction(
    request: ScanRequest,
    user = Depends(verify_jwt_token)
):
    """Protected endpoint requiring valid JWT."""
    return await perform_scan(request, user)
```

### 4.2 Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/v1/scan")
@limiter.limit("10/minute")  # 10 requests per minute
async def scan_transaction(request: Request, scan_request: ScanRequest):
    return await perform_scan(scan_request)
```

### 4.3 Cryptographic Signatures

```python
import nacl.signing
import base64

class CryptographicSigner:
    """Ed25519 signature management."""
    
    def __init__(self):
        self.private_key = nacl.signing.SigningKey.generate()
        self.public_key = self.private_key.verify_key
    
    def sign_message(self, message: dict) -> dict:
        """Sign a message envelope."""
        message_bytes = json.dumps(
            message,
            sort_keys=True,
            separators=(',', ':')
        ).encode()
        
        signed = self.private_key.sign(message_bytes)
        signature = base64.b64encode(signed.signature).decode()
        
        return {**message, "signature": signature}
    
    def verify_signature(self, envelope: dict, public_key_b64: str) -> bool:
        """Verify message signature."""
        signature_bytes = base64.b64decode(envelope["signature"])
        message = {k: v for k, v in envelope.items() if k != "signature"}
        message_bytes = json.dumps(
            message,
            sort_keys=True,
            separators=(',', ':')
        ).encode()
        
        public_key = nacl.signing.VerifyKey(base64.b64decode(public_key_b64))
        
        try:
            public_key.verify(message_bytes, signature_bytes)
            return True
        except:
            return False
```

---

## 5. MONITORING & OBSERVABILITY

### 5.1 Structured Logging

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """Output logs as structured JSON."""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("son.log")
    ]
)

for handler in logging.root.handlers:
    handler.setFormatter(JSONFormatter())
```

### 5.2 Performance Metrics

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
scan_requests = Counter('son_scan_requests_total', 'Total scan requests')
scan_duration = Histogram('son_scan_duration_seconds', 'Scan duration')
active_scans = Gauge('son_active_scans', 'Number of active scans')

@app.post("/api/v1/scan")
async def scan_transaction(request: ScanRequest):
    scan_requests.inc()
    active_scans.inc()
    
    start_time = time.time()
    try:
        result = await perform_scan(request)
        scan_duration.observe(time.time() - start_time)
        return result
    finally:
        active_scans.dec()
```

---

**Next Document**: [04-blockchain-features.md](./04-blockchain-features.md)
