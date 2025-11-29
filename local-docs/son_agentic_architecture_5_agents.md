# **Sentinel Orchestrator Network (SON)**  
## **FINAL AGENTIC ARCHITECTURE (5-AGENT VERSION)**  
### *CrewAI + Masumi Node + Kodosumi Runtime + Hydra + Cardano L1*
---

# **0. Purpose of This Document**
This is a **clean, simplified, production-ready specification** of SON’s agentic architecture using **exactly 5 agents** — optimized for the hackathon implementation, aligned with your repo structure, and integrated tightly with:

- **CrewAI** (agent reasoning & workflows)
- **Masumi Node** (payment service + registry service)
- **Kodosumi Runtime** (agent execution environment)
- **Hydra** (ultra-fast consensus between agents)
- **Cardano L1** (ThreatProof Capsule output)

This is the **crystal-clear** agent model your entire team will reference.

---

# **1. The Five Agents**
To keep SON powerful but hackathon-practical, we converge everything into **5 universal agents**:

---
## **1.1 Agent A — Sentinel Agent (Detection)**
**Role:** Primary detector & analyzer. 

**Functions:**
- Scans mempool / policy IDs
- Extracts CBOR, metadata, bytecode
- Performs heuristic + regex-based threat detection
- Computes a risk score (0–100)
- Generates the evidence hash

**CrewAI Role Type:** `expert_detector`

**Masumi Pricing:** Per scan (fixed)

**Runs Inside:** Kodosumi Runtime → CrewAI task → Hydra input

---
## **1.2 Agent B — Oracle Agent (Cross-Verification)**
**Role:** External data & liquidity verification.

**Functions:**
- Queries DEX liquidity (WingRiders/Minswap APIs)
- Gathers real-world or chain metadata
- Confirms/denies Sentinel’s red flags

**CrewAI Role Type:** `external_data_verifier`

**Masumi Pricing:** Per external lookup

This merges the old “oracle cluster” into **one agent**.

---
## **1.3 Agent C — Compliance Agent (Risk Policies)**
**Role:** Sanctions + KYC + compliance-based reasoning.

**Functions:**
- Matches wallet against sanctions databases
- Checks suspicious wallet age / behavior
- Provides a compliance-weighted risk modifier

**CrewAI Role Type:** `compliance_checker`

**Masumi Pricing:** Usage-based

---
## **1.4 Agent D — ZK-Prover Agent (Privacy + Integrity)**
**Role:** Generate Midnight-compatible ZK proof OR mock.

**Functions:**
- Takes threat result from Agents A/B/C
- Produces **ZK proof of knowledge** (mock or real)
- Ensures sensitive exploit details are never exposed

**CrewAI Role Type:** `privacy_guardian`

**Masumi Pricing:** Per proof generation

**Runs as:** Midnight Compact wrapper via Python (`zk_prover.py`)

---
## **1.5 Agent E — Consensus Agent (Final Arbiter + Capsule Writer)**
**Role:** Final decision + Hydra consensus + CIP-25 Capsule generation.

**Functions:**
- Collects votes from A/B/C/D
- Runs consensus (Hydra or local-fallback)
- Finalizes verdict: SAFE or DANGER
- Produces a **ThreatProof Capsule**
- Writes capsule to Cardano L1

**CrewAI Role Type:** `consensus_mediator`

**Masumi Pricing:** Paid per finalization

---

# **2. How These 5 Agents Replace the Old 8-Agent System**
The old setup had: Detect, Verify, Compliance, Arbitrate, Fetch, Filter, Vote, Scribe.

The new mapping is:
```
Detect → Sentinel Agent
Verify → Oracle Agent
Compliance → Compliance Agent
Arbitrate → Consensus Agent
Fetch/Filter/Vote/Scribe → Oracle + Consensus Agents combined
ZK Layer → ZK-Prover Agent
```

This keeps full functionality with **far less complexity**.

---

# **3. How CrewAI Orchestrates the 5-Agent Workflow**
CrewAI becomes your internal multi-agent engine.

## **3.1 CrewAI Process Definition**
A single `Crew` contains all 5 agents.

Workflow:
```
Sentinel Agent → Oracle Agent → Compliance Agent → ZK-Prover Agent → Consensus Agent
```

Each agent:
- Receives structured input
- Produces structured output defined in `api_schema.json`
- Passes results to next agent via CrewAI task-handling

CrewAI **automatically handles**:
- task sequencing  
- result passing  
- output refinement  
- retries  
- error surfacing to Orchestrator  
- multi-agent reasoning

---

# **4. How Masumi Enables “Economic Agents”**
Masumi converts each of the 5 agents into a **paid, discoverable microservice**.

## **4.1 Masumi Registry Service**
For each agent, registry contains:
- DID (agent identity) 
- Public keys
- Agent type
- Pricing model
- Reputation
- Version

Backend uses this to dynamically select and route tasks.

## **4.2 Masumi Payment Service**
Flow for each scan:
1. User triggers `/scan` → backend creates Payment Session
2. Payment is escrowed
3. Each agent receives micropayment after completing its task
4. Consensus Agent triggers payout via Masumi API

**This aligns incentives:** good agents get paid; slow or faulty ones lose jobs.

---

# **5. How Kodosumi Runtime Runs the Agents**
Kodosumi Runtime = execution sandbox where each agent’s Python CrewAI code lives.

It provides:
- containerized execution
- secure isolation
- local caching for faster scans
- fast communication bridges for Hydra & Masumi
- long-running service environment

Agents are treated as **modular containers**:
```
agents/
   sentinel.py
   oracle.py
   compliance.py
   zk_prover.py
   consensus.py
```

Each container communicates through:
- CrewAI internal bus
- Masumi APIs
- Hydra websocket
- Cardano RPC

---

# **6. Hydra’s Role: Multi-Agent Consensus for the 5-Agent Architecture**
Hydra is used ONLY at the final decision stage.

### **Why?**
Hydra gives:
- instant multi-party consensus
- extremely fast commit (< 1 sec)
- no on-chain fees until the end

### **Who participates?**
Agents A–E **do not all join** Hydra.
Only the final two:
- ZK-Prover Agent
- Consensus Agent

The Sentinel, Oracle, and Compliance Agents send **votes**, not Hydra messages.

This keeps Hydra lightweight.

### **Consensus Flow:**
```
(1) Sentinel → votes risk
(2) Oracle → votes confirmation
(3) Compliance → votes sanctions weight
(4) ZK-Prover → attaches proof
(5) Consensus Agent → submits final vote to Hydra
(6) Hydra Head → final agreement
(7) Consensus Agent → writes ThreatProof Capsule to L1
```

---

# **7. Cardano L1: Final Proof Storage**
The final output of the entire agentic pipeline is the **ThreatProof Capsule**.

CIP-25 Structure:
- verdict
- risk_score
- consensus weight
- Hydra signatures
- ZK-proof reference
- evidence Merkle root
- timestamp

Stored under `/docs/api_schema.json`.

---

# **8. Complete 5-Agent Workflow (Crystal-Clear)**
```
User → Backend Router → CrewAI → Agents → Hydra → L1 Capsule → Frontend
```

### **Step-by-step:**
1. **User** submits Policy ID.
2. **Backend Orchestrator** (main.py) initiates CrewAI process.
3. **Sentinel Agent** evaluates the token.
4. **Oracle Agent** cross-verifies liquidity + fundamentals.
5. **Compliance Agent** adds regulatory risk.
6. **ZK-Prover Agent** produces privacy-preserving proof.
7. **Consensus Agent** aggregates all results.
8. **Consensus Agent** sends final vote to **Hydra**.
9. **Hydra Head** confirms.
10. **Consensus Agent** writes the ThreatProof Capsule to **Cardano L1**.
11. **Masumi** triggers final payment.
12. **Frontend Dashboard** displays the verdict.

---

# **9. Why This Simplified 5-Agent Model Is Perfect for Hackathon Delivery**
✔ Minimal number of agents → easier coordination  
✔ Still maintains full “swarm intelligence” effect  
✔ Hydra usage remains meaningful  
✔ Masumi integrates cleanly into payment + registry flow  
✔ ZK-Agent is isolated for optional Midnight integration  
✔ CrewAI orchestrates everything with minimal boilerplate  
✔ Execution matches your repo structure 1:1  
✔ Works with mock, semi-real, and full-real infrastructure

---

# **10. Final Summary**
SON’s simplified 5-agent architecture provides:
- **strong intelligence** (Sentinel)
- **cross-validation** (Oracle)
- **regulation-aware scoring** (Compliance)
- **privacy guarantees** (ZK-Prover)
- **trust-minimized consensus + capsule writing** (Consensus)

This architecture is HIGH-IMPACT, HACKATHON-READY, and fully aligned with:
- CrewAI multi-agent workflows
- Masumi payments + registry
- Kodosumi agent runtime
- Hydra L2 consensus
- Cardano L1 final verification

This is the official agent architecture for SON.
