Based on research into blockchain security workflows and agentic AI collaboration patterns, here is your comprehensive user story and workflow documentation:

***

# **SON GOVERNANCE GUARD: USER STORY & WORKFLOW SPECIFICATION**

## **Document Overview**

This document defines the complete user journey for the Sentinel Orchestrator Network (SON), from entry point to final outcome. It covers three primary user personas, eight critical user stories, and the detailed technical workflow that powers the agentic security engine.

***

## **USER PERSONAS**

### **Persona 1: Sarah — The DeFi Trader**

**Background:**
- Age: 28, Product Manager at a tech company
- Crypto Experience: 2 years, primarily uses Nami wallet
- Technical Skill: Intermediate (can read basic transaction details)
- Primary Goal: Swap ADA for stablecoins without losing funds to governance issues
- Pain Point: "I don't understand block heights or forks. I just want to know if my transaction is safe."

**Key Behaviors:**
- Checks transactions 2-3 times before signing
- Reads security alerts but may not understand technical jargon
- Values speed but prioritizes safety
- Trusts visual feedback over text explanations

### **Persona 2: Marcus — The DAO Participant**

**Background:**
- Age: 35, Smart contract developer and SPO (Stake Pool Operator)
- Crypto Experience: 6 years, deep Cardano ecosystem knowledge
- Technical Skill: Advanced (reads CBOR, understands consensus)
- Primary Goal: Vote on governance proposals without chain-split risk
- Pain Point: "After the Chang Fork, I need to verify my node is on the canonical chain before every governance action."

**Key Behaviors:**
- Manually checks block explorers before critical transactions
- Runs his own node infrastructure
- Requires detailed technical logs and proofs
- Willing to pay premium for security guarantees

### **Persona 3: Lisa — The Casual NFT Collector**

**Background:**
- Age: 22, University student with casual crypto interest
- Crypto Experience: 6 months, introduced via NFT drops
- Technical Skill: Beginner (doesn't know what CBOR means)
- Primary Goal: Mint NFTs during drops without worrying about scams
- Pain Point: "I heard about people losing money during forks but I don't know how to check if I'm safe."

**Key Behaviors:**
- Relies entirely on wallet UI guidance
- Easily overwhelmed by technical terminology
- Makes quick decisions during time-sensitive drops
- Needs "red light / green light" simplicity

***

## **USER STORIES**

### **Story 1: The Pre-Transaction Safety Check**

**As** Sarah (DeFi Trader),  
**I want to** paste my transaction details and get instant safety verification,  
**So that** I can confidently swap tokens without losing funds to a chain split.

**Acceptance Criteria:**
- Transaction analysis completes in < 5 seconds
- Verdict displays as clear visual indicator (red/green)
- Non-technical explanation provided ("You're on a ghost chain" not "Minority fork detected")
- Option to automatically switch to safe node if danger detected

**User Flow:**

```
1. Sarah opens Nami wallet, initiates 500 ADA → USDC swap
2. Wallet generates transaction CBOR: 84a3008182582...
3. Sarah copies CBOR, opens SON dashboard
4. Pastes CBOR into scan field
5. Clicks "INITIATE GOVERNANCE SCAN" button
6. Watches Matrix terminal for 3-4 seconds
7. Receives verdict: "GOVERNANCE SPLIT DETECTED"
8. Reads explanation: "Your wallet is connected to a ghost chain..."
9. Clicks "SWITCH TO SAFE NODE" button
10. SON provides new RPC endpoint
11. Sarah updates wallet settings, rescans
12. New verdict: "TRANSACTION VERIFIED ✓"
13. Returns to wallet, completes swap successfully
```

***

### **Story 2: The Governance Vote Verification**

**As** Marcus (DAO Participant),  
**I want to** verify my node's consensus state before voting on a constitutional proposal,  
**So that** my vote counts on the canonical chain and isn't replayed on a minority fork.

**Acceptance Criteria:**
- Detailed technical logs accessible via dropdown
- Agent collaboration costs displayed transparently
- ThreatProof NFT mintable as permanent record
- API endpoint available for CLI integration

**User Flow:**

```
1. Marcus drafts governance vote transaction via cardano-cli
2. Before signing, runs: `curl -X POST https://son-api.io/scan`
3. SON detects missing validity interval (TTL)
4. Sentinel agent flags replay attack vulnerability
5. Oracle agent hired automatically (1.0 ADA escrow)
6. Oracle scans 5 nodes, finds consensus divergence:
   - IOG Node: Block 10,050 (99.2% stake weight)
   - Marcus's Node: Block 10,020 (0.8% stake weight)
7. Midnight generates ZK-proof of verification without exposing vote content
8. Marcus receives JSON response with detailed technical breakdown
9. Clicks "VIEW FULL REPORT" in dashboard
10. Exports ThreatProof metadata
11. Mints NFT as immutable evidence
12. Reconfigures node to sync with IOG infrastructure
13. Re-scans transaction, receives "SAFE" verdict
14. Signs and submits vote on canonical chain
```

***

### **Story 3: The NFT Mint Safety Gate**

**As** Lisa (NFT Collector),  
**I want to** check if a minting contract is safe during a timed drop,  
**So that** I don't lose my ADA to a fake contract on a ghost chain.

**Acceptance Criteria:**
- Policy ID input accepted (not just CBOR)
- Verdict completes in < 3 seconds (drop urgency)
- Mobile-responsive interface (Lisa uses phone)
- Visual verdict dominates (minimal text)

**User Flow:**

```
1. Lisa sees Discord announcement: "Mint live! Policy: a3f7b..."
2. Opens SON mobile site on phone
3. Taps "Scan Policy ID" quick action
4. Pastes: a3f7b2c8d1e4f5...
5. Taps scan button (large, pink, center screen)
6. Watches simplified agent visualization (3 icons bouncing)
7. Receives verdict screen:
   - Green shield icon (full screen)
   - Text: "SAFE TO MINT ✓"
   - Subtext: "Contract verified on mainnet"
8. Taps "OPEN WALLET" button (deep link to Eternl)
9. Completes mint transaction
10. Returns to SON, sees auto-saved scan history
```

***

### **Story 4: The Historical Threat Audit**

**As** Marcus (Developer),  
**I want to** review all past threats detected by SON,  
**So that** I can analyze governance attack patterns and improve my infrastructure.

**Acceptance Criteria:**
- Dashboard displays threat timeline (last 30 days)
- Filterable by threat type (fork, replay, protocol violation)
- Exportable as CSV for analysis
- Aggregated statistics (total forks prevented, avg agent cost)

**User Flow:**

```
1. Marcus logs into SON dashboard
2. Navigates to "Threat Archive" tab
3. Views timeline visualization:
   - Jan 15: 3 fork detections (Chang v1.1 contentious vote)
   - Jan 22: 12 replay vulnerabilities (missing TTL)
   - Jan 28: 1 protocol violation (Plutus V1 deprecated usage)
4. Clicks "Jan 15" event cluster
5. Sees detailed breakdown:
   - 89 users protected
   - Total value at risk: 127,000 ADA
   - Average detection time: 2.3 seconds
6. Filters by "Replay Attack" threat type
7. Exports CSV with columns:
   [Timestamp, Threat Type, Policy ID, Agent Cost, Verdict]
8. Analyzes patterns in Jupyter Notebook
9. Shares findings with SPO community on forum
```

***

### **Story 5: The Agent Economy Monitoring**

**As** Sarah (Power User),  
**I want to** see how agents hire each other and track escrow costs,  
**So that** I understand the economics of my security checks.

**Acceptance Criteria:**
- Real-time agent collaboration graph displayed
- Payment flows animated as visual connections
- Cost breakdown per agent action
- Historical cost trends (daily average)

**User Flow:**

```
1. Sarah completes transaction scan (verdict: SAFE)
2. Clicks "View Agent Activity" button
3. Dashboard transitions to Agent Economy view
4. Sees triangular node graph:
   - SENTINEL (top vertex)
   - ORACLE (bottom-left vertex)
   - MIDNIGHT (bottom-right vertex)
5. Animated flow shows:
   - Sentinel → Oracle: 1.0 ADA (payment line pulses pink)
   - Oracle → Midnight: 0.5 ADA (verification subcontract)
6. Tooltip on hover:
   "SENTINEL hired ORACLE for fork check
    Escrow locked: 1.0 ADA
    Job completed: 2.1 seconds
    Payment released: 1.0 ADA"
7. Bottom panel shows cost breakdown:
   - Base scan: 0.5 ADA
   - Oracle hire: 1.0 ADA
   - Midnight ZK-proof: 0.5 ADA
   - Total: 2.0 ADA
8. Clicks "Last 7 Days" tab
9. Sees line chart: Average cost dropped from 2.5 → 2.0 ADA
   (Oracle optimized routing efficiency)
```

***

### **Story 6: The False Positive Challenge**

**As** Marcus (Advanced User),  
**I want to** manually override a "DANGER" verdict with supporting evidence,  
**So that** I can proceed with a transaction I've independently verified as safe.

**Acceptance Criteria:**
- "Challenge Verdict" button visible on DANGER screen
- Requires uploading counter-evidence (block explorer screenshot, node logs)
- Admin review process (48-hour SLA)
- Transparency report published if override approved

**User Flow:**

```
1. Marcus scans transaction, receives "MINORITY FORK" verdict
2. Manually checks Cardanoscan: His node IS on mainnet
3. Suspects SON oracle is using stale data
4. Clicks "Challenge Verdict" button
5. Modal appears: "Submit Counter-Evidence"
6. Uploads:
   - Screenshot of Cardanoscan block height
   - Output of `cardano-cli query tip --mainnet`
   - Signed statement with SPO credentials
7. Receives confirmation: "Challenge #4477 submitted"
8. 36 hours later, receives email:
   "Challenge approved. Oracle was querying deprecated node.
    SON has been updated. 2.0 ADA refunded."
9. Views SON blog post:
   "Incident Report: Oracle Node Rotation Delay"
10. Appreciates transparency, continues using SON
```

***

### **Story 7: The White-Label Integration**

**As** Wallet Developer (New Persona: "Alex"),  
**I want to** embed SON verification into my wallet's pre-signing flow,  
**So that** my users are protected automatically without visiting external sites.

**Acceptance Criteria:**
- REST API with < 500ms response time
- Webhook support for async scanning
- SDK available in JavaScript/TypeScript
- Rate limiting: 1000 requests/hour (free tier)

**User Flow:**

```
1. Alex is building "SafeWallet" (Cardano mobile wallet)
2. Reads SON API documentation at docs.son-network.io
3. Installs SDK: `npm install @son/sdk`
4. Integrates in transaction signing flow:

   import { SonClient } from '@son/sdk';
   
   async function signTransaction(cbor) {
     const son = new SonClient(API_KEY);
     const verdict = await son.scan({ tx_cbor: cbor });
     
     if (verdict.status === 'DANGER') {
       showModal('Transaction Blocked by Governance Guard');
       return;
     }
     
     wallet.sign(cbor);
   }

5. Tests with staging API
6. User "TestUser123" attempts fork transaction
7. SafeWallet UI shows SON-powered warning automatically
8. Alex monitors dashboard: 47 threats blocked in first week
9. Promotes SON integration in app store description
10. User retention increases 23% (trust signal)
```

***

### **Story 8: The Emergency Network Alert**

**As** SON System (Automated Actor),  
**I want to** broadcast network-wide alerts during critical governance events,  
**So that** all users are warned proactively before attempting dangerous transactions.

**Acceptance Criteria:**
- Alert triggers when >15% of scans detect same fork
- Multi-channel broadcast (dashboard banner, API webhook, Twitter bot)
- Threat level classification (Low/Medium/High/Critical)
- Auto-resolves when consensus normalizes

**User Flow:**

```
1. Chang Hard Fork v2.0 activates with contentious vote
2. Network begins splitting (40% reject, 60% accept)
3. SON detects pattern:
   - 10:15 AM: 8 fork detections in 5 minutes
   - 10:17 AM: 23 fork detections (threshold exceeded)
4. SON automatically:
   - Publishes alert to status page (status.son-network.io)
   - Sends webhook to 847 integrated wallets
   - Posts to Twitter: "@SONNetwork CRITICAL: Governance fork detected..."
   - Displays banner on dashboard:
     "⚠️ NETWORK ALERT: Chain split in progress. All scans may show DANGER."
5. Sarah opens SON, immediately sees banner
6. Decides to delay her swap until alert clears
7. 6 hours later: Consensus stabilizes (98% on new chain)
8. SON auto-resolves alert:
   - Banner changes to: "✓ RESOLVED: Network consensus restored."
9. Sarah proceeds with transaction safely
10. SON publishes post-mortem report
```

***

## **TECHNICAL WORKFLOW**

### **Phase 1: Transaction Ingestion**

**Trigger:** User submits CBOR or Policy ID via API/Dashboard

```
┌─────────────────────────────────────────────────┐
│ USER ACTION                                     │
│ • Paste CBOR/Policy ID                          │
│ • Click "Scan"                                  │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ FRONTEND (Next.js)                              │
│ • Validate input format                         │
│ • Show loading animation                        │
│ • Open WebSocket connection                     │
│ POST /api/v1/scan                               │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ API GATEWAY (FastAPI)                           │
│ • Authenticate request                          │
│ • Generate scan_id: "scan_8847"                 │
│ • Enqueue to MessageBus                         │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ MESSAGE BUS (Redis Pub/Sub)                     │
│ Topic: "scans.new"                              │
│ Payload: {scan_id, tx_cbor, user_session}       │
└─────────────────────────────────────────────────┘
```

**Data Flow:**
- Input validation ensures CBOR is hex-encoded, Policy ID matches regex `[a-f0-9]{56}`
- WebSocket connection allows real-time agent log streaming
- MessageBus decouples frontend from agent processing (async)

***

### **Phase 2: Sentinel Analysis**

**Agent:** SENTINEL-01 (Policy Compliance Checker)

```
┌─────────────────────────────────────────────────┐
│ SENTINEL AGENT INITIALIZATION                   │
│ • Subscribes to "scans.new"                     │
│ • Receives scan_8847                            │
│ • Loads transaction decoder                     │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ CBOR PARSING                                    │
│ 1. Decode transaction structure                 │
│ 2. Extract:                                     │
│    - Inputs/Outputs                             │
│    - Validity Interval (TTL)                    │
│    - Script References                          │
│    - Protocol Version                           │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ POLICY COMPLIANCE CHECKS                        │
│                                                 │
│ CHECK 1: Protocol Version                       │
│ IF script uses Plutus V1 AND current_era > V2  │
│   → FLAG: "DEPRECATED_PROTOCOL"                 │
│                                                 │
│ CHECK 2: Validity Interval                     │
│ IF validity_interval_start == NULL              │
│   → FLAG: "REPLAY_VULNERABLE"                   │
│   → TRIGGER: Oracle hiring sequence             │
│                                                 │
│ CHECK 3: Metadata Compliance                    │
│ IF CIP-25 structure invalid                     │
│   → FLAG: "MALFORMED_METADATA"                  │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
       ┌────────┴────────┐
       │  DECISION TREE  │
       │                 │
   SAFE│                 │UNSAFE
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│ PUBLISH:    │   │ HIRE ORACLE │
│ "VERDICT:   │   │ (Next Phase)│
│  SAFE"      │   └─────────────┘
└─────────────┘
```

**Key Logic (Python):**

```python
class SentinelAgent:
    def analyze_transaction(self, cbor):
        tx = CBORDecoder.parse(cbor)
        flags = []
        
        # Check 1: Protocol Version
        if tx.script_version == "PlutusV1" and self.current_era() > "Babbage":
            flags.append("DEPRECATED_PROTOCOL")
        
        # Check 2: Replay Protection
        if tx.validity_interval_start is None:
            flags.append("REPLAY_VULNERABLE")
            # Autonomous Decision: Hire Oracle
            self.hire_oracle(reason="NO_TTL_REPLAY_RISK")
        
        # Check 3: Metadata
        if not self.validate_cip25(tx.metadata):
            flags.append("MALFORMED_METADATA")
        
        return {"status": "NEEDS_ORACLE" if flags else "SAFE", "flags": flags}
```

***

### **Phase 3: Agentic Hiring (Oracle)**

**Trigger:** Sentinel flags replay vulnerability

```
┌─────────────────────────────────────────────────┐
│ SENTINEL DECISION ENGINE                        │
│ "I can't verify network state from here.        │
│  I need to hire the Oracle agent."              │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ ESCROW ENGINE (Smart Contract Lite)             │
│ 1. Lock 1.0 ADA from Sentinel's wallet          │
│ 2. Generate escrow_id: "esc_7742"               │
│ 3. Conditions:                                  │
│    - Release if Oracle completes job            │
│    - Refund if Oracle fails (timeout)           │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ HIRE_REQUEST MESSAGE (IACP Protocol)            │
│                                                 │
│ {                                               │
│   "protocol": "IACP/2.0",                       │
│   "type": "HIRE_REQUEST",                       │
│   "from_did": "did:masumi:sentinel_01",         │
│   "to_did": "did:masumi:oracle_01",             │
│   "payload": {                                  │
│     "task": "CHECK_FORK_STATUS",                │
│     "escrow_id": "esc_7742",                    │
│     "amount": 1.0,                              │
│     "context": {                                │
│       "scan_id": "scan_8847",                   │
│       "user_node_hint": "user_provided_rpc"     │
│     }                                           │
│   },                                            │
│   "timestamp": "2025-01-30T10:15:23Z",          │
│   "signature": "Ed25519:base64_sig..."          │
│ }                                               │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ MESSAGE BUS PUBLISH                             │
│ Topic: "agent.oracle.inbox"                     │
│ • Oracle agent listening 24/7                   │
│ • Receives hire request                         │
└─────────────────────────────────────────────────┘
```

**Frontend Visualization:**
- User sees in Matrix Terminal:
  ```
  [●] SENTINEL-01  Action: HIRE_REQUEST
      ↳ @ORACLE-01, Network Fork Check Needed
      ↳ Escrow: 1.0 ₳  [███████░░░] Locking...
  ```
- Animated coin (₳) flies from Sentinel avatar → Oracle avatar (1.2s duration)

***

### **Phase 4: Oracle Network Scanning**

**Agent:** ORACLE-01 (Consensus Validator)

```
┌─────────────────────────────────────────────────┐
│ ORACLE RECEIVES HIRE REQUEST                    │
│ • Validates Sentinel's signature                │
│ • Checks escrow_id exists                       │
│ • Accepts job (publishes OFFER_ACCEPTED)        │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ MULTI-NODE SCANNING                             │
│                                                 │
│ Target Nodes (Hardcoded List):                  │
│ 1. IOG Official Node (mainnet-1.iohk.io)        │
│ 2. Emurgo Node (cardano.emurgo.io)              │
│ 3. Cardano Foundation (node.cardano.org)        │
│ 4. User's Node (from context hint)              │
│ 5. Coinbase Node (cardano.coinbase.com)         │
│                                                 │
│ Query Each Node:                                │
│ GET /api/query/tip                              │
│ Response: {                                     │
│   "block_height": 10050,                        │
│   "block_hash": "7a3f...",                      │
│   "slot": 84726392,                             │
│   "epoch": 412                                  │
│ }                                               │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ CONSENSUS ANALYSIS                              │
│                                                 │
│ Results:                                        │
│ • IOG:       Block 10,050  (99.2% stake)        │
│ • Emurgo:    Block 10,050  (Matches)            │
│ • CF:        Block 10,051  (+1, within range)   │
│ • User:      Block 10,020  (-30, DIVERGED!)     │
│ • Coinbase:  Block 10,050  (Matches)            │
│                                                 │
│ VERDICT LOGIC:                                  │
│ IF user_block < (majority_block - 5):           │
│   status = "MINORITY_FORK"                      │
│   risk = "HIGH"                                 │
│   evidence = "30_block_divergence"              │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ JOB_COMPLETE MESSAGE                            │
│ {                                               │
│   "protocol": "IACP/2.0",                       │
│   "type": "JOB_COMPLETE",                       │
│   "from_did": "did:masumi:oracle_01",           │
│   "to_did": "did:masumi:sentinel_01",           │
│   "payload": {                                  │
│     "status": "MINORITY_FORK_DETECTED",         │
│     "mainnet_tip": 10050,                       │
│     "user_node_tip": 10020,                     │
│     "divergence_blocks": 30,                    │
│     "evidence": {                               │
│       "checked_nodes": 5,                       │
│       "consensus_nodes": 4,                     │
│       "stake_weight": 0.992                     │
│     }                                           │
│   },                                            │
│   "signature": "Ed25519:..."                    │
│ }                                               │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ ESCROW RELEASE                                  │
│ • Escrow Engine verifies Oracle signature       │
│ • Releases 1.0 ADA to Oracle wallet             │
│ • Publishes PAYMENT_COMPLETE event              │
└─────────────────────────────────────────────────┘
```

**Frontend Visualization:**
```
[◐] ORACLE-01       Status: SCANNING
    ↳ Checking 5 nodes...
    ↳ IOG:      Block 10,050 ✓
    ↳ Emurgo:   Block 10,050 ✓
    ↳ CF:       Block 10,051 ✓
    ↳ User:     Block 10,020 🔴 DIVERGED
    ↳ Coinbase: Block 10,050 ✓
    
[●] ORACLE-01       Verdict: MINORITY_FORK
    ↳ Evidence: 30-block divergence
    ↳ Payment: 1.0 ₳ RELEASED
```

***

### **Phase 5: Midnight ZK-Proof Generation**

**Agent:** MIDNIGHT-ZK (Privacy Notary)

```
┌─────────────────────────────────────────────────┐
│ SENTINEL REQUESTS PRIVACY PROOF                 │
│ "I need to prove this scan happened without     │
│  revealing the user's transaction details."     │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ MIDNIGHT AGENT (MOCK MODE FOR HACKATHON)        │
│                                                 │
│ IF mock_mode == True:                           │
│   proof = {                                     │
│     "zk_proof": "MOCK_0xA7F2B8C3D1E4...",       │
│     "verification_key": "vk_mock_...",          │
│     "public_inputs": {                          │
│       "scan_timestamp": 1738240523,             │
│       "verdict_hash": "sha256(DANGER)",         │
│       "agent_count": 3                          │
│     }                                           │
│   }                                             │
│   # In production: Call actual Midnight Compact │
│   # proof = midnight_cli.generate_proof(...)    │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ PROOF AGGREGATION                               │
│ Combine signatures from all agents:             │
│ • Sentinel signature                            │
│ • Oracle signature                              │
│ • Midnight proof                                │
│                                                 │
│ Generate Merkle Root:                           │
│ evidence_root = merkle_tree([                   │
│   hash(sentinel_sig),                           │
│   hash(oracle_report),                          │
│   hash(midnight_proof)                          │
│ ])                                              │
└─────────────────────────────────────────────────┘
```

***

### **Phase 6: Hydra Settlement**

**Trigger:** All agent verdicts collected

```
┌─────────────────────────────────────────────────┐
│ HYDRA HEAD (PRE-OPENED STATE CHANNEL)           │
│ • Running in Docker on dedicated server         │
│ • 3 participants: Sentinel, Oracle, Midnight    │
│ • Channel pre-funded with 100 ADA               │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ SUBMIT VERDICT TO HYDRA                         │
│                                                 │
│ hydra-client newTx --tx-file verdict.json       │
│                                                 │
│ verdict.json:                                   │
│ {                                               │
│   "scan_id": "scan_8847",                       │
│   "verdict": "UNSAFE_FORK",                     │
│   "evidence_root": "0xF7A2...",                 │
│   "agent_signatures": {                         │
│     "sentinel": "sig1...",                      │
│     "oracle": "sig2...",                        │
│     "midnight": "sig3..."                       │
│   },                                            │
│   "finality_timestamp": "2025-01-30T10:15:28Z"  │
│ }                                               │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ HYDRA INSTANT CONSENSUS                         │
│ • All 3 agents sign off (< 200ms)               │
│ • Verdict finalized in Hydra state              │
│ • NO L1 transaction yet (off-chain speed)       │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ OPTIONAL: L1 ANCHORING                          │
│ (Only if user clicks "Mint ThreatProof NFT")    │
│                                                 │
│ 1. Close Hydra head temporarily                 │
│ 2. Submit CIP-25 metadata to mainnet:           │
│    {                                            │
│      "721": {                                   │
│        "<POLICY>": {                            │
│          "ThreatProof_8847": {                  │
│            "verdict": "UNSAFE_FORK",            │
│            "evidence_root": "0xF7A2...",        │
│            "cost": "2.0 ADA"                    │
│          }                                      │
│        }                                        │
│      }                                          │
│    }                                            │
│ 3. Wait ~20 seconds (mainnet finality)          │
│ 4. Re-open Hydra head                           │
└─────────────────────────────────────────────────┘
```

**Why Hydra?**
- **Speed:** Sub-second finality for verdict delivery
- **Cost:** Off-chain transactions avoid L1 fees
- **Integrity:** Multi-signature prevents single-agent manipulation

***

### **Phase 7: Verdict Delivery**

```
┌─────────────────────────────────────────────────┐
│ BACKEND PUBLISHES FINAL VERDICT                 │
│ WebSocket Message:                              │
│ {                                               │
│   "event": "SCAN_COMPLETE",                     │
│   "scan_id": "scan_8847",                       │
│   "verdict": {                                  │
│     "status": "DANGER",                         │
│     "threat_type": "GOVERNANCE_FORK",           │
│     "severity": "HIGH",                         │
│     "explanation": "Your wallet is connected to │
│       a minority fork 30 blocks behind mainnet."│
│   },                                            │
│   "recommendations": [                          │
│     "Switch RPC to mainnet-1.iohk.io",          │
│     "Wait 2 hours for consensus",               │
│     "Do NOT sign this transaction"              │
│   ],                                            │
│   "agent_cost": "2.0 ADA",                      │
│   "proof_id": "threat_8847"                     │
│ }                                               │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ FRONTEND RENDERS VERDICT SCREEN                 │
│                                                 │
│ • Matrix terminal fades out (800ms)             │
│ • Red alarm animation triggers                  │
│ • Full-screen verdict card slides up            │
│ • "TRANSACTION BLOCKED" text pulses             │
│ • Action buttons appear:                        │
│   - [SWITCH TO SAFE NODE]                       │
│   - [VIEW THREAT PROOF]                         │
│   - [REPORT FALSE POSITIVE]                     │
└─────────────────────────────────────────────────┘
```

**User Experience:**
- **Sarah (DeFi Trader):** Sees "You're on a ghost chain. Switching nodes..." → Auto-fixed
- **Marcus (Developer):** Downloads full JSON report for post-mortem analysis
- **Lisa (NFT Collector):** Sees big red X, reads "Don't mint yet. Try again in 1 hour."

***

## **EDGE CASES & ERROR HANDLING**

### **Case 1: Oracle Timeout**

**Scenario:** Oracle agent doesn't respond within 10 seconds

```
Sentinel Logic:
IF time.now() - hire_timestamp > 10s:
    REFUND escrow to Sentinel
    FALLBACK to "UNKNOWN_NETWORK_STATE" verdict
    DISPLAY: "Network check unavailable. Proceed with caution."
```

### **Case 2: All Nodes Report Different Heights**

**Scenario:** No clear consensus (each of 5 nodes at different block)

```
Oracle Logic:
IF len(set(block_heights)) == 5:  # All unique
    status = "NETWORK_INSTABILITY"
    recommendation = "Wait 30 minutes for consensus"
```

### **Case 3: User Submits Invalid CBOR**

**Scenario:** Malformed hex string

```
API Gateway:
try:
    bytes.fromhex(cbor)
except ValueError:
    return 400, {"error": "INVALID_CBOR_FORMAT"}
```

### **Case 4: Hydra Head Offline**

**Scenario:** Docker container crashed

```
Settlement Layer:
IF hydra_ping() == False:
    FALLBACK to direct L1 submission
    WARNING: "Finality delayed (~20s due to mainnet settlement)"
```

***

## **SUCCESS METRICS**

### **User-Facing KPIs**

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Scan Completion Time** | < 5 seconds | Median time from scan click → verdict display |
| **False Positive Rate** | < 2% | Challenges approved / Total DANGER verdicts |
| **User Comprehension** | > 80% | Post-scan survey: "Did you understand the verdict?" |
| **Mobile Responsiveness** | 100% | All screens functional on 375px width |

### **Technical KPIs**

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Agent Uptime** | 99.5% | Percentage of time all 3 agents responsive |
| **WebSocket Latency** | < 100ms | Time from agent log → frontend display |
| **Hydra Settlement Speed** | < 500ms | Time from verdict → Hydra finalization |
| **API Throughput** | 100 req/s | Concurrent scans without degradation |

***

## **HACKATHON DEMO SCRIPT**

**Total Duration:** 3 minutes

### **Act 1: The Setup (0:00-0:30)**

> **Presenter:** "In the Voltaire Era, Cardano's governance can cause chain splits. Your wallet doesn't know which chain is real. Watch what happens when I try to spend 500 ADA on a ghost chain."

*[Screen: SON dashboard with clean hero shot]*

### **Act 2: The Scan (0:30-1:30)**

> **Action:** Paste malicious CBOR, click scan  
> **Visual:** Matrix terminal appears, agents communicate  
> **Narration:** "The Sentinel analyzes the code. It sees a replay vulnerability. It autonomously hires the Oracle—paying 1 ADA—to check the network."

*[Zoom on coin animation: Sentinel → Oracle]*

> **Narration:** "The Oracle scans 5 nodes. It discovers: I'm on a minority fork, 30 blocks behind."

### **Act 3: The Block (1:30-2:15)**

> **Visual:** Red alarm, "TRANSACTION BLOCKED"  
> **Narration:** "SON stops me. If I had signed this, attackers could replay it on the real chain and drain my wallet."

*[Click "View ThreatProof"]*

> **Visual:** 3D rotating shield NFT  
> **Narration:** "Every decision is cryptographically proven. I can mint this as permanent evidence."

### **Act 4: The Resolution (2:15-3:00)**

> **Action:** Click "Switch to Safe Node"  
> **Visual:** Dashboard provides new RPC endpoint  
> **Narration:** "SON fixes my wallet configuration. Let me scan again..."

*[Re-scan, green "SAFE" verdict]*

> **Closing:** "This is SON: The Constitutional Guard for Cardano's Voltaire Era. Built on Masumi agents, secured by Midnight privacy, settled via Hydra speed."

*[End card: SON logo + QR code to live demo]*

***

This document provides the complete narrative and technical foundation for judges to understand both the user impact and the engineering excellence behind SON.[1][2][3][4]

[1](https://community.trustcloud.ai/docs/grc-launchpad/grc-101/compliance/blockchain-and-compliance-ensuring-transparency-and-security-in-2024/)
[2](https://tde.fi/founder-resource/blogs/wallet/the-future-of-wallet-security-and-user-experience-in-2025/)
[3](https://raga.ai/resources/blogs/ai-agent-workflow-collaboration)
[4](https://www.cube.exchange/what-is/replay-attack)
[5](https://www.secuodsoft.com/blog/blockchain-development/a-comprehensive-overview-of-blockchain-development-your-complete-guide.php)
[6](https://www.sciencedirect.com/science/article/pii/S1319157824001204)
[7](https://www.trmlabs.com/resources/blog/what-is-the-best-blockchain-intelligence-tool-in-2025)
[8](https://procreator.design/blog/designing-for-blockchain-best-ux-practices/)
[9](https://hellotars.com/ai-agents/flow-visualizer-ai-agent)
[10](https://coconote.app/notes/b00daeda-9466-4820-8f5f-253393736823/transcript)