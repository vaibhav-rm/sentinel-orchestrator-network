# **THE SON BIBLE: DEFINITIVE HACKATHON MANIFESTO**
## **Version 6.0 — 5-Agent Architecture**

**Project:** Sentinel Orchestrator Network (SON)  
**Hackathon:** Cardano Hackathon Asia (IBW 2025)  
**Team:** NexBlock (5 Members)  
**Philosophy:** Extreme Parallelization via Strict Contracts  
**Status:** FINAL & FROZEN (Version 6.0)

---

## **PART 1: THE EXECUTIVE VISION & STRATEGY**

### **1.1 The Narrative (The "Why")**

DeFi on Cardano is a "Dark Forest." Users blindly sign transactions, trusting frontend UIs that can be compromised.

- **The Gap:** L1 verification is too slow (20s blocks). Centralized APIs are untrustworthy.
- **The Innovation:** SON creates a **"Bodyguard Swarm"** of 5 specialized AI agents that live between the User and the Blockchain.

### **1.2 The Technology Stack**

| Component | Purpose |
|-----------|---------|
| **CrewAI** | Multi-agent orchestration and task sequencing |
| **Masumi** | Agent payments, discovery, and reputation |
| **Kodosumi Runtime** | Containerized agent execution environment |
| **Hydra** | Ultra-fast L2 consensus (< 1 second) |
| **Midnight** | ZK-proofs for privacy-preserving verification |
| **Cardano L1** | Immutable ThreatProof Capsule registry |

### **1.3 The User Journey (The "Movie Script")**

1. **Trigger:** User scans a Policy ID on the Dashboard.
2. **The Swarm:** 5 Agents activate sequentially via CrewAI.
3. **Detection:** Sentinel Agent finds a `mint_unlimited` vulnerability.
4. **Verification:** Oracle Agent confirms with DEX liquidity data.
5. **Compliance:** Compliance Agent checks wallet sanctions.
6. **Privacy:** ZK-Prover Agent generates a Midnight ZK-Proof.
7. **Consensus:** Consensus Agent aggregates votes, submits to Hydra.
8. **Result:** Dashboard flashes **RED**. ThreatProof Capsule minted on L1.

---

## **PART 2: THE 5-AGENT ARCHITECTURE**

### **Agent A — Sentinel Agent (Detection)**

| Attribute | Value |
|-----------|-------|
| **Role** | Primary detector & analyzer |
| **CrewAI Role** | `expert_detector` |
| **Masumi Pricing** | Per scan (fixed) |
| **Performance** | < 2 seconds |

**Functions:**
- Fetches contract CBOR/metadata via Blockfrost
- Runs regex-based threat pattern detection
- Computes risk score (0-100)
- Generates evidence hash (SHA-256)
- Casts vote: SAFE / WARNING / DANGER

**Threat Patterns Detected:**
- `mint_unlimited` — Unlimited token minting
- `rugpull_pattern` — Owner can drain funds
- `honeypot` — Transfer disabled for users
- `admin_backdoor` — Excessive admin control
- `hidden_fee` — Suspiciously high fees
- `proxy_risk` — Upgradeable contract logic

---

### **Agent B — Oracle Agent (Cross-Verification)**

| Attribute | Value |
|-----------|-------|
| **Role** | External data & liquidity verifier |
| **CrewAI Role** | `external_data_verifier` |
| **Masumi Pricing** | Per external lookup |
| **Performance** | < 3 seconds |

**Functions:**
- Queries DEX liquidity (WingRiders/Minswap)
- Fetches token holder distribution
- Analyzes trading volume patterns
- Cross-verifies Sentinel's findings
- Returns: CONFIRMED / DENIED / UNCERTAIN

**Data Sources:**
- WingRiders API
- Minswap API
- Blockfrost (holder data)

---

### **Agent C — Compliance Agent (Risk Policies)**

| Attribute | Value |
|-----------|-------|
| **Role** | Sanctions + wallet risk assessment |
| **CrewAI Role** | `compliance_checker` |
| **Masumi Pricing** | Usage-based |
| **Performance** | < 2 seconds |

**Functions:**
- Checks wallet against sanctions lists (OFAC mock)
- Analyzes wallet age and behavior
- Identifies risk indicators (new wallet, low activity)
- Calculates risk modifier (0.5 - 2.0)

**Risk Modifier Logic:**
| Modifier | Meaning |
|----------|---------|
| 0.5 | Very low risk (established wallet, no flags) |
| 1.0 | Neutral (default) |
| 1.5 | Elevated risk (new wallet, some flags) |
| 2.0 | Critical risk (sanctions match, severe flags) |

---

### **Agent D — ZK-Prover Agent (Privacy + Integrity)**

| Attribute | Value |
|-----------|-------|
| **Role** | Privacy-preserving proof generation |
| **CrewAI Role** | `privacy_guardian` |
| **Masumi Pricing** | Per proof generation |
| **Performance** | < 2 seconds (mock) |

**Functions:**
- Takes threat results from Agents A/B/C
- Produces ZK proof of knowledge
- Ensures sensitive exploit details never exposed
- Returns proof hash and verification key

**Mock Mode:** Active by default until Midnight Devnet is stable.

---

### **Agent E — Consensus Agent (Final Arbiter)**

| Attribute | Value |
|-----------|-------|
| **Role** | Final decision + Hydra consensus + Capsule writer |
| **CrewAI Role** | `consensus_mediator` |
| **Masumi Pricing** | Per finalization |
| **Performance** | < 5 seconds |

**Functions:**
- Collects votes from all 4 previous agents
- Calculates weighted final score
- Submits to Hydra for L2 consensus
- Produces CIP-25 ThreatProof Capsule
- Writes capsule to Cardano L1

**Vote Weights:**
| Agent | Weight |
|-------|--------|
| Sentinel | 40% |
| Oracle | 25% |
| Compliance | 20% |
| ZK-Prover | 15% |

**Verdict Thresholds:**
| Score Range | Verdict |
|-------------|---------|
| 0-40 | SAFE |
| 41-70 | WARNING |
| 71-100 | DANGER |

---

## **PART 3: WORKFLOW ORCHESTRATION**

### **3.1 CrewAI Sequential Flow**

```
Sentinel Agent → Oracle Agent → Compliance Agent → ZK-Prover Agent → Consensus Agent
     (A)            (B)             (C)               (D)               (E)
```

Each agent:
1. Receives structured input from previous agent
2. Processes asynchronously
3. Produces structured output
4. Passes results via CrewAI task-handling

### **3.2 Complete Workflow (Step-by-Step)**

```
1.  User submits Policy ID via /api/v1/scan
2.  Backend Orchestrator (main.py) initiates CrewAI Crew
3.  Sentinel Agent analyzes contract → votes risk
4.  Oracle Agent verifies with DEX data → confirms/denies
5.  Compliance Agent checks sanctions → applies modifier
6.  ZK-Prover Agent generates proof → attaches hash
7.  Consensus Agent aggregates votes → calculates final score
8.  Consensus Agent submits to Hydra → gets confirmation
9.  Consensus Agent writes ThreatProof Capsule to L1
10. Masumi triggers payment distribution
11. Frontend Dashboard displays verdict with animation
```

### **3.3 Hydra Consensus Flow**

Only ZK-Prover and Consensus agents participate in Hydra directly:

```
Sentinel → votes risk (not Hydra)
Oracle → votes confirmation (not Hydra)
Compliance → votes sanctions weight (not Hydra)
ZK-Prover → attaches proof (Hydra participant)
Consensus → submits final vote to Hydra Head
Hydra Head → confirms (< 1 second)
Consensus → writes capsule to L1
```

---

## **PART 4: THE API CODEX (v2.0)**

*This is the Law. Breaking changes require 2 approvals in chat.*

### **A. External API (Frontend ↔ Backend)**

#### **1. Initiate Scan**

```http
POST /api/v1/scan
Authorization: Bearer son_hackathon_token_2025
Content-Type: application/json

{
  "schema_version": "2.0",
  "policy_id": "d5e6bf0500378d4f0da4e8dde6becec7621cd8cbf0abb9efb1c650668",
  "creator_wallet": "addr1...",
  "scan_depth": "standard",
  "mock_mode": false
}
```

**Success Response (202 Accepted):**
```json
{
  "task_id": "task_8821_xc",
  "status": "processing",
  "ws_url": "ws://localhost:8000/ws/logs/task_8821_xc",
  "estimated_time": 5
}
```

#### **2. WebSocket Log Stream**

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/logs/task_8821_xc');

// Agent Start Event
{
  "event_type": "agent_start",
  "agent_name": "sentinel",
  "data": { "policy_id": "abc..." },
  "timestamp": "2025-01-30T12:00:01Z"
}

// Agent Complete Event
{
  "event_type": "agent_complete",
  "agent_name": "sentinel",
  "data": {
    "vote": "DANGER",
    "risk_score": 85,
    "findings_count": 3
  },
  "timestamp": "2025-01-30T12:00:02Z"
}

// Workflow Complete Event
{
  "event_type": "workflow_complete",
  "agent_name": null,
  "data": {
    "final_verdict": "DANGER",
    "final_score": 78,
    "capsule_id": "CAPSULE_abc12345_20250130",
    "total_duration_ms": 3200
  },
  "timestamp": "2025-01-30T12:00:05Z"
}
```

### **B. Internal Agent Outputs**

See `docs/api_schema.json` for complete schema definitions.

### **C. ThreatProof Capsule (CIP-25)**

```json
{
  "721": {
    "<policy_id>": {
      "ThreatProof_A1B2C3D4": {
        "name": "ThreatProof Capsule #A1B2C3D4",
        "description": "SON threat analysis verdict: DANGER",
        "verdict": "DANGER",
        "risk_score": 78,
        "vote_weights": {
          "sentinel": 0.40,
          "oracle": 0.25,
          "compliance": 0.20,
          "zk_prover": 0.15
        },
        "vote_summary": {
          "sentinel": "DANGER",
          "oracle": "DANGER",
          "compliance": "WARNING",
          "zk_prover": "DANGER"
        },
        "evidence_merkle_root": "sha256_hash...",
        "hydra_tx_id": "hydra_tx_hash...",
        "zk_proof_hash": "proof_hash...",
        "version": "2.0",
        "timestamp": "2025-01-30T12:00:05Z"
      }
    }
  }
}
```

---

## **PART 5: THE 5-PERSON SQUAD**

### **Member 1: THE ARCHITECT (Integration & Traffic Control)**

- **Mission:** Own `main.py` and orchestration
- **Technology:** FastAPI, AsyncIO, CrewAI
- **Responsibilities:**
  - Initialize FastAPI with CORS
  - Create async `run_workflow(task_id)` using ThreatDetectionCrew
  - Manage WebSocket event streaming
  - Print observability events to stdout

### **Member 2: THE BRAIN (Detection Logic)**

- **Mission:** Own all 5 agent implementations
- **Technology:** Python, Blockfrost SDK, Regex
- **Responsibilities:**
  - Implement `SentinelAgent` (threat detection)
  - Implement `OracleAgent` (DEX verification)
  - Implement `ComplianceAgent` (sanctions)
  - Implement `ConsensusAgent` (vote aggregation)
  - Each agent must complete in < 2-5 seconds

### **Member 3: THE SPEED DEMON (Hydra Infrastructure)**

- **Mission:** Own Hydra node and consensus
- **Technology:** Docker, WebSocket, CBOR
- **Responsibilities:**
  - Get `hydra-node` and `cardano-node` running
  - Write `hydra_client.py` for WebSocket submission
  - Implement fallback: local `ledger.json` if Hydra fails

### **Member 4: THE GHOST (Midnight & Privacy)**

- **Mission:** Own ZK-Prover Agent
- **Technology:** Midnight Compact, Python
- **Responsibilities:**
  - Write minimal Compact circuit for threat verification
  - Implement `zk_prover.py` with mock/real switch
  - Mock mode active by default

### **Member 5: THE FACE (Frontend & UX)**

- **Mission:** Own the Dashboard
- **Technology:** Next.js, Tailwind, Framer Motion
- **Responsibilities:**
  - Dark mode Matrix theme
  - Real-time WebSocket log display
  - Agent status indicators (5 agents shown)
  - Final verdict animation

---

## **PART 6: TEST VECTORS & OBSERVABILITY**

### **6.1 Observability Events**

```
EVENT workflow_started  task_id=8821 policy_id=abc...
EVENT agent_start       task_id=8821 agent=sentinel
EVENT agent_complete    task_id=8821 agent=sentinel vote=DANGER score=85
EVENT agent_start       task_id=8821 agent=oracle
EVENT agent_complete    task_id=8821 agent=oracle vote=DANGER score=72
EVENT agent_start       task_id=8821 agent=compliance
EVENT agent_complete    task_id=8821 agent=compliance vote=WARNING modifier=1.5
EVENT agent_start       task_id=8821 agent=zk_prover
EVENT agent_complete    task_id=8821 agent=zk_prover proof=abc123...
EVENT agent_start       task_id=8821 agent=consensus
EVENT hydra_submit      task_id=8821 tx=hydra_abc...
EVENT capsule_minted    task_id=8821 capsule_id=CAPSULE_...
EVENT workflow_complete task_id=8821 verdict=DANGER score=78 duration=3200ms
```

### **6.2 Test Vectors**

**Vector A: Dangerous Token (DANGER)**
```json
{
  "policy_id": "deadbeef000000000000000000000000000000000000000000000000ab",
  "expected_verdict": "DANGER",
  "expected_score": "80-100"
}
```

**Vector B: Warning Token (WARNING)**
```json
{
  "policy_id": "warn0000000000000000000000000000000000000000000000000000ab",
  "expected_verdict": "WARNING",
  "expected_score": "41-70"
}
```

**Vector C: Safe Token (SAFE)**
```json
{
  "policy_id": "safe0000000000000000000000000000000000000000000000000000ab",
  "expected_verdict": "SAFE",
  "expected_score": "0-40"
}
```

---

## **PART 7: THE SEQUENCE DIAGRAM**

```
sequenceDiagram
    participant User as User (Frontend)
    participant Orch as Orchestrator (FastAPI)
    participant S as Sentinel Agent
    participant O as Oracle Agent
    participant C as Compliance Agent
    participant Z as ZK-Prover Agent
    participant Con as Consensus Agent
    participant H as Hydra Head
    participant L1 as Cardano L1

    User->>Orch: POST /scan (PolicyID)
    Orch->>S: process(input)
    S-->>Orch: {vote, risk_score, findings}
    Orch->>O: process(sentinel_output)
    O-->>Orch: {vote, verification_status}
    Orch->>C: process(sentinel, oracle)
    C-->>Orch: {vote, risk_modifier}
    Orch->>Z: process(all outputs)
    Z-->>Orch: {proof_hash, vote}
    Orch->>Con: process(all outputs)
    Con->>H: Submit final vote
    H-->>Con: Consensus confirmed
    Con->>L1: Mint ThreatProof Capsule
    L1-->>Con: tx_hash
    Con-->>Orch: Final result
    Orch-->>User: WebSocket: DANGER
```

---

## **PART 8: THE "DON'T FAIL" RULES**

1. **5 Agents Only:** Do not add more agents. The architecture is frozen.
2. **Sequential Workflow:** Agents run in order: A → B → C → D → E.
3. **Mock by Default:** ZK-Prover and external APIs use mocks until stable.
4. **Frontend is King:** Beautiful UI > perfect backend. Judges see the frontend.
5. **Video is Insurance:** Record a working demo before the live presentation.
6. **No Live Training:** Use pre-set patterns, not live ML training.
7. **Hydra is Static:** One head, keep it running. No dynamic head management.

---

## **PART 9: FILE STRUCTURE**

```
sentinel-orchestrator-network/
├── backend/
│   ├── agents/
│   │   ├── __init__.py      # Exports all agents
│   │   ├── base.py          # BaseAgent class
│   │   ├── sentinel.py      # Agent A
│   │   ├── oracle.py        # Agent B
│   │   ├── compliance.py    # Agent C
│   │   ├── consensus.py     # Agent E
│   │   └── crew.py          # ThreatDetectionCrew orchestrator
│   ├── infrastructure/
│   │   ├── zk_prover.py     # Agent D
│   │   └── hydra_client.py
│   ├── routers/
│   │   └── scan.py
│   └── main.py
├── docs/
│   ├── api_schema.json
│   └── SON_BIBLE_V6.md
├── frontend/
│   └── (Next.js app)
├── hydra-node/
│   └── docker-compose.yml
└── midnight-devnet/
    └── Dockerfile
```

---

**This is the 5-Agent Architecture. This is the way. Execute.**
