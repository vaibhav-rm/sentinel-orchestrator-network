# 🔄 Agentic Workflows

## Complete Agent Interaction Patterns

---

## WORKFLOW 1: SECURITY SCAN EXECUTION

### End-to-End Flow

```
[USER REQUEST]
    │
    ▼
┌────────────────────────────────────────────┐
│ API Gateway (FastAPI)                      │
│ POST /api/v1/scan/transaction              │
│ Body: {                                    │
│   "policy_id": "abc123...",                │
│   "user_tip": 10050                        │
│ }                                          │
└────────────┬───────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│ STEP 1: Sentinel Agent (Entry Point)      │
│                                            │
│ Actions:                                   │
│ 1. Generate unique scan_id (UUID)         │
│ 2. Validate request format                │
│ 3. Check protocol compliance               │
│    ├─ Parse CBOR                          │
│    ├─ Validate fields                     │
│    └─ Check metadata                      │
│ 4. Create Redis task tracking             │
│    redis.set(f"task:{scan_id}", {         │
│      "status": "initiated",               │
│      "progress": 0.1                      │
│    })                                      │
│                                            │
│ Decision:                                  │
│ IF compliance == INVALID:                 │
│   → Return DANGER verdict immediately     │
│ ELSE:                                      │
│   → Proceed to hire Oracle                │
└────────────┬───────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│ STEP 2: Hire Oracle via IACP              │
│                                            │
│ Sentinel creates HIRE_REQUEST:            │
│ {                                          │
│   "protocol": "IACP/2.0",                  │
│   "type": "HIRE_REQUEST",                  │
│   "from_did": "did:masumi:sentinel_01",   │
│   "to_did": "did:masumi:oracle_01",       │
│   "payload": {                             │
│     "task": "fork_check",                 │
│     "policy_id": "abc123...",             │
│     "user_tip": 10050,                    │
│     "scan_id": "uuid..."                  │
│   },                                       │
│   "escrow_id": "escrow_888",              │
│   "amount": 1.0,                          │
│   "timestamp": "2025-01-30T12:00:01Z",    │
│   "signature": "Ed25519_sig..."           │
│ }                                          │
│                                            │
│ Publish to: Redis channel "agent:oracle:inbox" │
│                                            │
│ Update task status:                        │
│ redis.set(f"task:{scan_id}", {            │
│   "status": "oracle_hired",               │
│   "progress": 0.2                         │
│ })                                         │
└────────────┬───────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│ STEP 3: Oracle Receives Request           │
│                                            │
│ Oracle subscribes to "agent:oracle:inbox" │
│ Receives HIRE_REQUEST message              │
│                                            │
│ Actions:                                   │
│ 1. Verify Sentinel's signature            │
│    ├─ Extract public key from DID registry│
│    ├─ Verify Ed25519 signature            │
│    └─ Check escrow balance (mocked)       │
│                                            │
│ 2. If verification fails → Reject request │
│ 3. If verified → Spawn 5 specialists      │
│                                            │
│ Update task status:                        │
│ redis.set(f"task:{scan_id}", {            │
│   "status": "specialists_spawning",       │
│   "progress": 0.3                         │
│ })                                         │
└────────────┬───────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│ STEP 4: Parallel Specialist Execution     │
│ (asyncio.gather with 10s timeout)         │
│                                            │
│ Spawn 5 agents simultaneously:             │
│                                            │
│ ┌──────────────────────────────────────┐  │
│ │ BlockScanner Agent                   │  │
│ │ Task: Query 5 RPC providers          │  │
│ │ Time: ~800ms                         │  │
│ │ Output: {risk: 0.95, findings: [...]}│  │
│ └──────────────────────────────────────┘  │
│                                            │
│ ┌──────────────────────────────────────┐  │
│ │ StakeAnalyzer Agent                  │  │
│ │ Task: Check pool saturation          │  │
│ │ Time: ~1200ms                        │  │
│ │ Output: {risk: 0.15, findings: [...]}│  │
│ └──────────────────────────────────────┘  │
│                                            │
│ ┌──────────────────────────────────────┐  │
│ │ VoteDoctor Agent                     │  │
│ │ Task: Check governance context       │  │
│ │ Time: ~900ms                         │  │
│ │ Output: {risk: 0.10, findings: [...]}│  │
│ └──────────────────────────────────────┘  │
│                                            │
│ ┌──────────────────────────────────────┐  │
│ │ MempoolSniffer Agent                 │  │
│ │ Task: Analyze UTxO patterns          │  │
│ │ Time: ~1100ms                        │  │
│ │ Output: {risk: 0.20, findings: [...]}│  │
│ └──────────────────────────────────────┘  │
│                                            │
│ ┌──────────────────────────────────────┐  │
│ │ ReplayDetector Agent                 │  │
│ │ Task: Check pattern hashes           │  │
│ │ Time: ~1400ms                        │  │
│ │ Output: {risk: 0.15, findings: [...]}│  │
│ └──────────────────────────────────────┘  │
│                                            │
│ Total execution time: max(800, 1200, 900, │
│                           1100, 1400)      │
│                       = 1400ms             │
│                                            │
│ Update task status:                        │
│ redis.set(f"task:{scan_id}", {            │
│   "status": "specialists_complete",       │
│   "progress": 0.7                         │
│ })                                         │
└────────────┬───────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│ STEP 5: Bayesian Fusion (Oracle)          │
│                                            │
│ Aggregate specialist results:              │
│                                            │
│ WEIGHTS = {                                │
│   BlockScanner: 0.30,                      │
│   StakeAnalyzer: 0.20,                     │
│   VoteDoctor: 0.15,                        │
│   MempoolSniffer: 0.20,                    │
│   ReplayDetector: 0.15                     │
│ }                                          │
│                                            │
│ weighted_risk = (0.95×0.30) + (0.15×0.20) │
│               + (0.10×0.15) + (0.20×0.20) │
│               + (0.15×0.15)               │
│             = 0.3925                       │
│                                            │
│ Apply severity override:                   │
│ IF BlockScanner.severity == CRITICAL:     │
│   weighted_risk = max(0.3925, 0.95)       │
│   → 0.95                                   │
│                                            │
│ Calculate confidence:                      │
│ confidence = successful_agents / 5         │
│            = 5 / 5 = 1.0                   │
│                                            │
│ Generate HIRE_RESPONSE:                    │
│ {                                          │
│   "protocol": "IACP/2.0",                  │
│   "type": "HIRE_RESPONSE",                 │
│   "from_did": "did:masumi:oracle_01",     │
│   "to_did": "did:masumi:sentinel_01",     │
│   "payload": {                             │
│     "status": "MINORITY_FORK_DETECTED",   │
│     "overall_risk": 0.95,                 │
│     "severity": "CRITICAL",               │
│     "findings": [...],                    │
│     "confidence": 1.0                     │
│   },                                       │
│   "signature": "Ed25519_sig..."           │
│ }                                          │
│                                            │
│ Publish to: "agent:sentinel:inbox"        │
│                                            │
│ Update task status:                        │
│ redis.set(f"task:{scan_id}", {            │
│   "status": "oracle_responded",           │
│   "progress": 0.9                         │
│ })                                         │
└────────────┬───────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│ STEP 6: Final Verdict (Sentinel)          │
│                                            │
│ Sentinel receives HIRE_RESPONSE            │
│                                            │
│ Actions:                                   │
│ 1. Verify Oracle's signature               │
│ 2. Determine final verdict                 │
│    IF status == "MINORITY_FORK_DETECTED": │
│      verdict = DANGER                      │
│      risk = 95                             │
│    ELSE IF status == "SAFE_CHAIN":        │
│      verdict = SAFE                        │
│      risk = 10                             │
│                                            │
│ 3. Generate ThreatProof Capsule            │
│    {                                       │
│      "scan_id": "uuid...",                │
│      "verdict": "DANGER",                 │
│      "risk_score": 95,                    │
│      "reason": "MINORITY_FORK_DETECTED",  │
│      "agent_signatures": {                │
│        "sentinel": "Ed25519_sig...",      │
│        "oracle": "Ed25519_sig...",        │
│        "block_scanner": "Ed25519_sig..."  │
│      },                                    │
│      "evidence_hash": "sha256:...",       │
│      "timestamp": "2025-01-30T12:00:05Z" │
│    }                                       │
│                                            │
│ 4. Store in PostgreSQL:                    │
│    INSERT INTO scans (                     │
│      scan_id, verdict, risk_score, ...    │
│    ) VALUES (...)                          │
│                                            │
│ 5. Cache in Redis (1 hour TTL):           │
│    redis.setex(f"scan:{scan_id}", 3600,   │
│               json.dumps(capsule))         │
│                                            │
│ 6. Broadcast to WebSocket:                │
│    ws.send(json.dumps({                   │
│      "type": "scan_complete",            │
│      "scan_id": "uuid...",               │
│      "verdict": "DANGER",                │
│      "data": capsule                      │
│    }))                                     │
│                                            │
│ Update task status:                        │
│ redis.set(f"task:{scan_id}", {            │
│   "status": "complete",                   │
│   "progress": 1.0                         │
│ })                                         │
└────────────┬───────────────────────────────┘
             │
             ▼
    [RETURN TO USER]
```

---

## WORKFLOW 2: GOVERNANCE ANALYSIS EXECUTION

### Sequential Pipeline Flow

```
[USER REQUEST]
    │
    ▼
┌────────────────────────────────────────────┐
│ API Gateway                                │
│ POST /api/v1/governance/analyze            │
│ Body: {                                    │
│   "gov_action_id": "847",                  │
│   "ipfs_hash": "QmXyz..."                  │
│ }                                          │
└────────────┬───────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│ Governance Orchestrator (Entry Point)      │
│                                            │
│ Initialize analysis pipeline               │
│ analysis_id = generate_uuid()             │
│                                            │
│ redis.set(f"analysis:{analysis_id}", {    │
│   "status": "initiated",                  │
│   "progress": 0.1,                        │
│   "current_agent": "ProposalFetcher"      │
│ })                                         │
└────────────┬───────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│ AGENT 1: ProposalFetcher                   │
│ Time: ~2.1 seconds                         │
│                                            │
│ Task: Retrieve metadata from IPFS          │
│                                            │
│ Try gateways sequentially:                 │
│ 1. ipfs.io (timeout 5s)                   │
│ 2. cloudflare-ipfs.com (timeout 5s)       │
│ 3. gateway.pinata.cloud (timeout 5s)       │
│ 4. dweb.link (timeout 5s)                 │
│                                            │
│ Parse CIP-100/108 format:                  │
│ {                                          │
│   "@context": "...",                       │
│   "body": {                                │
│     "title": "Marketing Campaign...",     │
│     "abstract": "...",                    │
│     "motivation": "...",                  │
│     "rationale": "...",                   │
│     "amount": 50000000000000,             │
│     "references": [...]                   │
│   }                                        │
│ }                                          │
│                                            │
│ Normalize and cache:                       │
│ redis.setex(                               │
│   f"proposal:{ipfs_hash}",                │
│   3600,  # 1 hour TTL                     │
│   json.dumps(metadata)                     │
│ )                                          │
│                                            │
│ Update status:                             │
│ redis.set(f"analysis:{analysis_id}", {    │
│   "status": "metadata_fetched",           │
│   "progress": 0.3                         │
│ })                                         │
│                                            │
│ Output: metadata (JSON)                    │
└────────────┬───────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│ AGENT 2: PolicyAnalyzer                    │
│ Time: ~1.9 seconds                         │
│                                            │
│ Input: metadata from ProposalFetcher       │
│                                            │
│ Phase 1: Hardcoded Rules (~50ms)           │
│ ─────────────────────────────────────────  │
│ rule_1: Check treasury cap                 │
│   if amount > 50M ADA:                     │
│     flags.append("TREASURY_CAP_VIOLATION") │
│                                            │
│ rule_2: Check marketing cap                │
│   if "marketing" in title.lower():        │
│     if amount > 5M ADA:                   │
│       flags.append("MARKETING_CAP")       │
│                                            │
│ rule_3: Check deliverables                 │
│   keywords = ["milestone", "kpi", ...]    │
│   if not any(k in text for k in keywords):│
│     flags.append("VAGUE_DELIVERABLES")    │
│                                            │
│ hardcoded_flags = ["TREASURY_CAP_VIOLATION",│
│                    "MARKETING_CAP_VIOLATION",│
│                    "VAGUE_DELIVERABLES"]    │
│                                            │
│ Phase 2: Gemini AI Analysis (~1800ms)      │
│ ─────────────────────────────────────────  │
│ prompt = construct_constitutional_prompt(  │
│   title, amount, motivation, rationale    │
│ )                                          │
│                                            │
│ gemini_response = await gemini.generate(   │
│   prompt,                                  │
│   config={"response_mime_type": "json"}   │
│ )                                          │
│                                            │
│ ai_analysis = {                            │
│   "summary": "...",                       │
│   "technical_summary": "...",             │
│   "flags": [                              │
│     "PROPOSER_VERIFICATION: No GitHub",   │
│     "DUPLICATE_RISK: Similar to #23"      │
│   ],                                       │
│   "recommendation": "NO",                 │
│   "reasoning": "...",                     │
│   "confidence": 0.92                      │
│ }                                          │
│                                            │
│ Merge flags:                               │
│ all_flags = hardcoded_flags + ai_analysis.flags│
│                                            │
│ Update status:                             │
│ redis.set(f"analysis:{analysis_id}", {    │
│   "status": "policy_analyzed",            │
│   "progress": 0.6,                        │
│   "current_agent": "SentimentAnalyzer"    │
│ })                                         │
│                                            │
│ Output: {flags, recommendation, confidence}│
└────────────┬───────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│ AGENT 3: SentimentAnalyzer                 │
│ Time: ~650ms                               │
│                                            │
│ Input: gov_action_id                       │
│                                            │
│ Task: Query on-chain votes                 │
│ votes = await blockfrost.get_proposal_votes(│
│   gov_action_id="847"                      │
│ )                                          │
│                                            │
│ Calculate stake-weighted support:          │
│ yes_power = sum(v.voting_power             │
│                 for v in votes             │
│                 if v.vote == "yes")        │
│ no_power = sum(v.voting_power              │
│                for v in votes              │
│                if v.vote == "no")          │
│ abstain_power = sum(v.voting_power         │
│                     for v in votes         │
│                     if v.vote == "abstain")│
│                                            │
│ total_power = yes_power + no_power +       │
│               abstain_power                │
│                                            │
│ support_pct = (yes_power / total_power) ×100│
│             = (60M / 614M) × 100           │
│             = 9.8%                         │
│                                            │
│ Categorize sentiment:                      │
│ if support_pct < 30%:                      │
│   sentiment = "STRONG_OPPOSITION"          │
│                                            │
│ Update status:                             │
│ redis.set(f"analysis:{analysis_id}", {    │
│   "status": "sentiment_analyzed",          │
│   "progress": 0.85                        │
│ })                                         │
│                                            │
│ Output: {                                  │
│   sentiment: "STRONG_OPPOSITION",         │
│   support_percentage: 9.8,                │
│   vote_breakdown: {yes: 12, no: 89, ...}  │
│ }                                          │
└────────────┬───────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│ Verdict Aggregation (Orchestrator)         │
│                                            │
│ Combine all agent outputs:                 │
│ - metadata (ProposalFetcher)               │
│ - policy_analysis (PolicyAnalyzer)         │
│ - sentiment (SentimentAnalyzer)            │
│                                            │
│ Apply decision rules:                      │
│                                            │
│ Rule 1: flags >= 2 → NO (auto)            │
│ IF len(policy_analysis.flags) >= 2:       │
│   verdict = {                              │
│     "recommendation": "NO",               │
│     "confidence": 0.9,                    │
│     "reason": "Multiple violations",      │
│     "auto_votable": True                  │
│   }                                        │
│   → TRIGGERED (5 flags) → STOP            │
│                                            │
│ (Skipped rules for brevity)               │
│                                            │
│ Generate complete report:                  │
│ {                                          │
│   "analysis_id": "uuid...",               │
│   "gov_action_id": "847",                 │
│   "metadata": {...},                      │
│   "policy_analysis": {...},               │
│   "sentiment": {...},                     │
│   "verdict": {...},                       │
│   "execution_time_ms": 4850,              │
│   "timestamp": "2025-01-30T12:00:05Z"    │
│ }                                          │
│                                            │
│ Store in PostgreSQL:                       │
│ INSERT INTO governance_analyses (...)      │
│                                            │
│ Cache in Redis (1 hour):                   │
│ redis.setex(f"analysis:{gov_action_id}",  │
│            3600, json.dumps(report))       │
│                                            │
│ Broadcast to WebSocket:                    │
│ ws.send(json.dumps({                      │
│   "type": "governance_complete",          │
│   "gov_action_id": "847",                 │
│   "recommendation": "NO",                 │
│   "data": report                          │
│ }))                                        │
│                                            │
│ Update status:                             │
│ redis.set(f"analysis:{analysis_id}", {    │
│   "status": "complete",                   │
│   "progress": 1.0                         │
│ })                                         │
└────────────┬───────────────────────────────┘
             │
             ▼
    [RETURN TO USER]
```

---

## WORKFLOW 3: REAL-TIME WEBSOCKET STREAMING

### Live Agent Activity Broadcasting

```
[USER CONNECTS TO WEBSOCKET]
    │
    ▼
┌────────────────────────────────────────────┐
│ WebSocket Server                           │
│ ws://localhost:8000/ws/logs                │
│                                            │
│ Connection established                      │
│ client_id = generate_uuid()                │
│ active_connections.add(client_id)          │
│                                            │
│ Send welcome message:                      │
│ ws.send(json.dumps({                      │
│   "type": "connection",                   │
│   "status": "connected",                  │
│   "client_id": client_id                  │
│ }))                                        │
└────────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│ Subscribe to Redis Channels                │
│                                            │
│ pubsub = redis.pubsub()                    │
│ await pubsub.subscribe(                    │
│   "logs:activity",                         │
│   "broadcast:all",                         │
│   "results:scan:*",                        │
│   "results:governance:*"                   │
│ )                                          │
└────────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│ Agent Execution Triggers Events            │
│                                            │
│ When BlockScanner starts:                  │
│ redis.publish("logs:activity", {          │
│   "event_type": "agent_start",            │
│   "agent_name": "BlockScanner",           │
│   "scan_id": "uuid...",                   │
│   "timestamp": "2025-01-30T12:00:01Z"    │
│ })                                         │
│                                            │
│ When BlockScanner completes:               │
│ redis.publish("logs:activity", {          │
│   "event_type": "agent_complete",         │
│   "agent_name": "BlockScanner",           │
│   "scan_id": "uuid...",                   │
│   "data": {risk: 0.95, findings: [...]}, │
│   "duration_ms": 800,                     │
│   "timestamp": "2025-01-30T12:00:02Z"    │
│ })                                         │
└────────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│ WebSocket Forwards to All Clients          │
│                                            │
│ for client in active_connections:          │
│   await client.ws.send(json.dumps(event)) │
│                                            │
│ Client receives in real-time:              │
│ • Agent start notifications                │
│ • Agent completion with results            │
│ • Error notifications                      │
│ • Progress updates                         │
│ • Final verdicts                           │
└────────────────────────────────────────────┘
             │
             ▼
    [FRONTEND UPDATES UI]
```

---

## KEY WORKFLOW CHARACTERISTICS

### Parallelism
- **Security Module**: 5 specialists run simultaneously (asyncio.gather)
- **Governance Module**: Sequential (ProposalFetcher → PolicyAnalyzer → SentimentAnalyzer)

### Fault Tolerance
- **Agent Timeout**: 10 seconds per specialist
- **Graceful Degradation**: Oracle functions with 4/5 specialists
- **Retry Logic**: IPFS gateways tried sequentially until success

### State Management
- **Redis**: Active task tracking, progress updates
- **PostgreSQL**: Persistent audit logs
- **WebSocket**: Real-time UI updates

### Cryptographic Security
- **Ed25519 Signatures**: Every agent message signed
- **Verification**: Recipients verify sender signatures
- **ThreatProof Capsules**: Immutable evidence packages

### Performance
- **Security Scan**: <5 seconds total (parallel execution)
- **Governance Analysis**: <5 seconds total (sequential pipeline)
- **WebSocket Latency**: <100ms (local Redis pub/sub)
