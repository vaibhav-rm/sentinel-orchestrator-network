Here is the precise **Git Repository Structure** for the **Sentinel Orchestrator Network (SON)**.

**Action:** One person (Member 1\) should create this folder structure immediately, run git init, and push it to GitHub. Everyone else clones it.

### **The SON Repository Tree**

Plaintext

sentinel-orchestrator-network/  
│  
├── .gitignore                   \# Crucial: Ignored files (see content below)  
├── README.md                    \# The "Face" of the repo (see content below)  
├── docker-compose.yml           \# Optional: Orchestrate entire stack  
│  
├── 📂 backend/                  \# \[MEMBER 1 DOMAIN\] \- The Orchestrator  
│   ├── main.py                  \# FastAPI Entry Point  
│   ├── requirements.txt         \# Python Dependencies  
│   ├── .env.example             \# Template for API Keys  
│   │  
│   ├── 📂 routers/              \# API Endpoints  
│   │   ├── \_\_init\_\_.py  
│   │   └── scan.py              \# POST /scan & WebSocket logic  
│   │  
│   ├── 📂 agents/               \# \[MEMBER 2 DOMAIN\] \- Detection Logic  
│   │   ├── \_\_init\_\_.py  
│   │   ├── sentinel.py          \# The Brain (Scam Detection)  
│   │   └── oracle.py            \# The Verifier (Liquidity Check)  
│   │  
│   ├── 📂 infrastructure/       \# \[MEMBER 3 & 4 DOMAIN\] \- The Pipes  
│   │   ├── \_\_init\_\_.py  
│   │   ├── hydra\_client.py      \# WebSocket connector to Hydra  
│   │   └── zk\_prover.py         \# Wrapper for Midnight Proofs  
│   │  
│   └── 📂 tests/                \# Test Vectors  
│       └── test\_vectors.json    \# Copy from Bible Part 4.2  
│  
├── 📂 frontend/                 \# \[MEMBER 5 DOMAIN\] \- Next.js Dashboard  
│   ├── package.json  
│   ├── tailwind.config.ts  
│   ├── tsconfig.json  
│   ├── .env.local.example  
│   │  
│   ├── 📂 public/               \# Images/Icons  
│   │  
│   ├── 📂 src/  
│   │   ├── 📂 app/  
│   │   │   ├── page.tsx         \# Main Dashboard Route  
│   │   │   └── layout.tsx  
│   │   │  
│   │   ├── 📂 components/  
│   │   │   ├── MatrixTerminal.tsx  \# The Log Window  
│   │   │   ├── StatusBadge.tsx     \# Red/Green Pill  
│   │   │   └── ScanInput.tsx       \# The Trigger Input  
│   │   │  
│   │   └── 📂 lib/  
│   │       └── websocket.ts        \# WS Connection Logic  
│  
├── 📂 hydra-node/               \# \[MEMBER 3 DOMAIN\] \- Docker Configs  
│   ├── docker-compose.yml       \# Standalone Hydra setup  
│   ├── config.json  
│   └── ledger/                  \# (Ignored) Local chain state  
│  
├── 📂 midnight-devnet/          \# \[MEMBER 4 DOMAIN\] \- ZK Configs  
│   ├── Dockerfile  
│   └── contract/  
│       └── threat\_check.compact \# The ZK Circuit Code  
│  
└── 📂 docs/                     \# \[SHARED\]  
    ├── SON\_BIBLE\_V5.md          \# Paste the text I gave you here  
    └── api\_schema.json          \# The Strict JSON Contracts

---

### **1\. The .gitignore Content (Copy-Paste)**

*Prevent "it works on my machine" errors by ignoring these files.*

Code snippet

\# Python  
\_\_pycache\_\_/  
\*.pyc  
venv/  
.env

\# Node/Next.js  
node\_modules/  
.next/  
out/  
.env.local

\# Docker/Infrastructure  
hydra-node/ledger/  
hydra-node/db/  
midnight-devnet/proofs/

\# IDEs  
.vscode/  
.idea/

\# OS  
.DS\_Store  
Thumbs.db

---

### **2\. The README.md Skeleton**

*Judges look at this first. Make it look professional instantly.*

Markdown

\# 🛡️ Sentinel Orchestrator Network (SON)  
\> The Unified Trust Engine for Cardano (Masumi \+ Hydra \+ Midnight)

**\*\*Submission for Cardano Hackathon Asia (IBW 2025)\*\***

\#\# 🚀 The Vision  
SON is a decentralized "Bodyguard Swarm" that protects users from DeFi threats in real-time.  
1\. **\*\*Trigger:\*\*** User scans a Policy ID.  
2\. **\*\*Swarm:\*\*** 3 Agents activate via **\*\*Masumi\*\***.  
3\. **\*\*Privacy:\*\*** Threats verified via **\*\*Midnight ZK-Proofs\*\***.  
4\. **\*\*Speed:\*\*** Consensus reached via **\*\*Hydra L2\*\***.  
5\. **\*\*Result:\*\*** Immutable **\*\*ThreatProof Capsule\*\*** on L1.

\#\# 🏗️ Architecture  
\* **\*\*Frontend:\*\*** Next.js \+ Tailwind (Matrix UI)  
\* **\*\*Backend:\*\*** FastAPI (Python) Orchestrator  
\* **\*\*Agents:\*\*** Python (Blockfrost SDK \+ Regex Heuristics)  
\* **\*\*Infrastructure:\*\*** Single Static Hydra Head \+ Midnight Devnet

\#\# ⚡ Quick Start  
\#\#\# 1\. Backend (Orchestrator \+ Agents)  
\`\`\`bash  
cd backend  
python \-m venv venv  
source venv/bin/activate  
pip install \-r requirements.txt  
python main.py  
\# Runs on http://localhost:8000

### **2\. Frontend (Dashboard)**

Bash

cd frontend  
npm install  
npm run dev  
\# Runs on http://localhost:3000

### **3\. Infrastructure (Hydra)**

Bash

cd hydra-node  
docker-compose up \-d

## **👥 Team NexBlock**

* **Architect:** Member 1  
* **Brain:** Member 2  
* **Speed:** Member 3  
* **Ghost:** Member 4  
* **Face:** Member 5

\---

\#\#\# \*\*3. Immediate Action Plan\*\*  
1\.  \*\*Member 1:\*\* Create this folder structure locally.  
2\.  \*\*Member 1:\*\* Run \`git init\`.  
3\.  \*\*Member 1:\*\* Add the \`.gitignore\` and \`README.md\`.  
4\.  \*\*Member 1:\*\* Push to GitHub.  
5\.  \*\*Everyone:\*\* Clone the repo.  
6\.  \*\*Member 2, 3, 4:\*\* Go to your specific folders (\`backend/agents\`, \`hydra-node\`, \`midnight-devnet\`) and start working. Do not touch \`main.py\`.

\*\*GO.\*\*

---

# **THE SON BIBLE: THE DEFINITIVE HACKATHON MANIFESTO**

Project: Sentinel Orchestrator Network (SON)

Hackathon: Cardano Hackathon Asia (IBW 2025\)

Team: NexBlock (5 Members)

Philosophy: Extreme Parallelization via Strict Contracts.

Status: FINAL & FROZEN (Version 5.0)

---

## **PART 1: THE EXECUTIVE VISION & STRATEGY**

### **1.1 The Narrative (The "Why")**

DeFi on Cardano is a "Dark Forest." Users blindly sign transactions, trusting frontend UIs that can be compromised.

* **The Gap:** L1 verification is too slow (20s blocks). Centralized APIs are untrustworthy.  
* **The Innovation:** SON creates a **"Bodyguard Swarm"** that lives between the User and the Blockchain. It uses **Masumi** to hire agents, **Midnight** to prove threats privately (preserving agent IP), and **Hydra** to reach consensus in milliseconds.

### **1.2 The User Journey (The "Movie Script")**

1. **Trigger:** User scans a Policy ID on the Dashboard.  
2. **The Swarm:** 3 Agents (Sentinel, Oracle, Audit) activate instantly.  
3. **Privacy:** The Sentinel Agent finds a mint\_unlimited bug. Instead of publishing the exploit code (which hackers could use), it generates a **Midnight ZK Proof** that certifies: *"I know a vulnerability exists, but I won't show you how to exploit it."*  
4. **Speed:** The agents submit their votes \+ ZK Proofs to a private **Hydra Head** (L2).  
5. **Result:** The Head confirms the vote. The Dashboard flashes **RED**. A **ThreatProof Capsule** (NFT) is minted on L1 as permanent evidence.

---

## **PART 2: THE 5-PERSON SQUAD (DETAILED OPERATING PROCEDURES)**

### **MEMBER 1: THE ARCHITECT (Integration & Traffic Control)**

* **The Mission:** You are the **Server**. You own main.py. You do not write AI logic. You write plumbing.  
* **Technology:** Python (FastAPI), Uvicorn, AsyncIO.  
* **Detailed Workflow:**  
  1. **Setup:** Initialize FastAPI with CORS allowed for localhost:3000.  
  2. **Orchestration:** Create an async function run\_swarm(task\_id) that fires off sentinel.scan(), oracle.check(), and midnight.prove() in parallel using asyncio.gather().  
  3. **State Management:** Use a simple in-memory dictionary TASKS \= {} to store job status. Do not waste time setting up Redis/Postgres.  
  4. **Logging:** You are responsible for printing the **Observability Events** (Section 5\) to stdout so we can debug.  
* **Relationship:** You are the boss of Members 2, 3, 4\. You are the servant of Member 5\.

### **MEMBER 2: THE BRAIN (Detection Logic)**

* **The Mission:** You are the **Intelligence**. You write sentinel.py.  
* **Technology:** Python, blockfrost-python SDK, Regex.  
* **Detailed Workflow:**  
  1. **Fetch:** Use Blockfrost API to pull the script\_cbor or source code of the target Policy ID.  
  2. **Analyze:** Run a rigorous Regex check against a "Bad Word Dictionary":  
     * selfdestruct, mint\_unlimited, disable\_sell, blacklist, delegate\_call.  
  3. **Score:** Start at 0\. Add \+50 for every bad word found. Cap at 100\.  
  4. **Format:** Output the strict JSON defined in Part 3\.  
* **Constraint:** Your script must run in **\< 2 seconds**. Do not use OpenAI API calls in the critical path unless they are extremely fast.

### **MEMBER 3: THE SPEED DEMON (Hydra Infrastructure)**

* **The Mission:** You are the **Infrastructure**. You run the Hydra Node.  
* **Technology:** Docker, WebSocket Client (websockets lib).  
* **Detailed Workflow:**  
  1. **Boot:** Get the hydra-node and cardano-node running in Docker. Use the devnet mode provided by the hydra-poc repo.  
  2. **Init:** Run the hydra-tui or CLI to open a **Single Head** with 3 participants. **Leave this running.**  
  3. **Client:** Write hydra\_client.py. It accepts a vote\_payload. It wraps it in a CBOR transaction metadata field. It submits it to the Hydra WebSocket endpoint (ws://127.0.0.1:4001).  
* **Backup Plan:** If Docker fails, write a script that writes the vote to a local ledger.json file but *pretends* to be Hydra (sleep 0.5s).

### **MEMBER 4: THE GHOST (Midnight & Privacy)**

* **The Mission:** You are the **Narrative**. You build the ZK Proof.  
* **Technology:** Midnight Compact Language, Python Wrapper.  
* **Detailed Workflow:**  
  1. **Circuit:** Write a minimal Compact contract: contract ThreatVerifier { ledger risk\_found: Boolean; transition verify(witness: Boolean) { if (witness) risk\_found \= true; } }.  
  2. **Wrapper:** Write zk\_prover.py.  
  3. **The Switch:** Implement the logic:  
  4. Python

def get\_proof(finding):  
    if CONFIG.MOCK\_ZK:  
        time.sleep(1) \# Simulate computation  
        return "MOCK\_ZK\_SIG\_998877"  
    else:  
        return run\_midnight\_cli(finding)

5.   
   6.   
* **Constraint:** The Mock Mode must be active by default until the real Devnet is proven stable.

### **MEMBER 5: THE FACE (Frontend & UX)**

* **The Mission:** You are the **Salesman**. The judges judge what *you* build.  
* **Technology:** Next.js, Tailwind, Framer Motion, useWebSocket.  
* **Detailed Workflow:**  
  1. **Theme:** Dark Mode. Monospace fonts (Courier/Fira Code). Green/Red neons.  
  2. **State:** Use useState to track: status (IDLE, SCANNING, VOTING, FINALIZED).  
  3. **Animation:** When status \=== SCANNING, show a cascading matrix rain or a spinning radar.  
  4. **Integration:** Connect to ws://localhost:8000/ws/logs/{task\_id}. On every message, append it to a logs array and auto-scroll the terminal.

---

## **PART 3: THE GOD-LEVEL API CODEX (v5.0)**

*This is the Law. Breaking changes require 2 approvals in chat.*

### **A. Change Control Policy**

1. All JSON payloads must include "schema\_version": "1.0".  
2. If you change a key, update the version to 1.1 and notify the channel.

### **B. External API (Frontend ↔ Backend)**

**1\. Initiate Scan**

* **Endpoint:** POST /api/v1/scan  
* **Auth:** Bearer son\_hackathon\_token\_2025 (Add this TODO).  
* **Input Body:**  
* JSON

{  
  "schema\_version": "1.0",  
  "policy\_id": "1234567890abcdef...", // Required  
  "user\_wallet": "addr1...",          // Optional (for payment simulation)  
  "mock\_mode": false                  // Set true to bypass backend latency  
}

*   
*   
* **Success Response (202 Accepted):**  
* JSON

{  
  "task\_id": "task\_8821\_xc",  
  "status": "accepted",  
  "ws\_url": "ws://localhost:8000/ws/logs/task\_8821\_xc",  
  "estimated\_time": 5  
}

*   
*   
* **Error Response (400 Bad Request):**  
* JSON

{  
  "error\_code": "INVALID\_POLICY\_ID",  
  "message": "Policy ID must be a hex string."  
}

*   
* 

**2\. WebSocket Log Stream**

* **Endpoint:** /ws/logs/{task\_id}  
* **Streamed Messages:**  
* JSON

// Log Update  
{  
  "timestamp": "12:00:01",  
  "source": "SENTINEL",  
  "status": "SCANNING",  
  "message": "Analyzing Bytecode..."  
}

// Final Result (CRITICAL)  
{  
  "timestamp": "12:00:05",  
  "source": "ORCHESTRATOR",  
  "status": "FINALIZED",  
  "payload": {  
    "verdict": "DANGER", // or SAFE  
    "risk\_score": 95,  
    "capsule\_tx": "8821xc...",  
    "ipfs\_link": "ipfs://Qm..."  
  }  
}

*   
* 

### **C. Internal Interfaces (Python Function Outputs)**

**3\. Sentinel Agent (Member 2 ➔ Member 1\)**

JSON

{  
  "schema\_version": "1.0",  
  "agent\_did": "did:masumi:sentinel\_01",  
  "vote": "DANGER",  
  "risk\_score": 95,  
  "flags": \["mint\_unlimited", "hidden\_owner\_privilege"\],  
  "evidence\_hash": "a1b2c3..."  
}

**4\. Midnight Prover (Member 4 ➔ Member 1\)**

JSON

{  
  "schema\_version": "1.0",  
  "prover\_did": "did:masumi:midnight\_01",  
  "proof\_type": "compact\_zk",  
  "proof\_string": "MOCK\_ZK\_PROOF\_SIG\_XY78...",  
  "is\_mock": true  
}

**5\. Hydra Submitter (Member 3 ➔ Member 1\)**

JSON

{  
  "schema\_version": "1.0",  
  "head\_id": "hydra\_v1\_static",  
  "tx\_hash": "ab99...",  
  "status": "confirmed",  
  "signatures": \["sig\_1", "sig\_2", "sig\_3"\]  
}

### **D. Final Output (L1 Capsule)**

*Strict CIP-25 Compliance.*

JSON

{  
  "721": {  
    "\<POLICY\_ID\>": {  
      "ThreatProof\_001": {  
        "name": "SON Verdict: DANGER",  
        "image": "ipfs://QmRedShield...",  
        "attributes": {  
          "verdict": "MALICIOUS",  
          "risk\_score": "95",  
          "consensus\_weight": "100%",  
          "evidence\_root": "merkle\_root\_hash\_xyz",  
          "zk\_proof\_ref": "midnight\_tx\_777",  
          "timestamp": "2025-01-30T12:00:00Z"  
        }  
      }  
    }  
  }  
}

---

## **PART 4: TEST VECTORS & OBSERVABILITY**

### **4.1 Observability Events (Member 1 Implementation)**

*Print these to STDOUT so we can debug without reading 1000 lines of code.*

Plaintext

EVENT task\_started    task\_id=8821 policy\_id=abc...  
EVENT agent\_response  task\_id=8821 agent=sentinel status=success time=0.4s  
EVENT zk\_proof\_gen    task\_id=8821 status=mock\_mode time=1.0s  
EVENT hydra\_submit    task\_id=8821 tx=ab99...  
EVENT capsule\_minted  task\_id=8821 ipfs=Qm...

### **4.2 Test Vectors (For Frontend Dev)**

*Use these JSONs to verify your UI handles all states.*

**Vector A: The Rug Pull (DANGER)**

JSON

{  
  "verdict": "DANGER",  
  "risk\_score": 98,  
  "flags": \["mint\_unlimited", "selfdestruct"\],  
  "capsule\_tx": "fake\_tx\_danger"  
}

**Vector B: The Safe Token (SAFE)**

JSON

{  
  "verdict": "SAFE",  
  "risk\_score": 5,  
  "flags": \["liquidity\_locked", "verified\_source"\],  
  "capsule\_tx": "fake\_tx\_safe"  
}

**Vector C: The Error (TIMEOUT)**

JSON

{  
  "error\_code": "AGENT\_TIMEOUT",  
  "message": "Sentinel Agent failed to respond in 5000ms."  
}

---

## **PART 5: THE ORCHESTRATOR SEQUENCE (Visual Logic)**

Code snippet

sequenceDiagram  
    participant User as User (Frontend)  
    participant Orch as Orchestrator (M1)  
    participant Agents as Agents (M2/M3)  
    participant ZK as Midnight Prover (M4)  
    participant Hydra as Hydra Head (M3)  
    participant L1 as Cardano L1

    User-\>\>Orch: POST /scan (PolicyID)  
    Orch-\>\>Agents: Dispatch Tasks  
    par Parallel Execution  
        Agents-\>\>Agents: Python ML Analysis (Sentinel/Oracle)  
        Agents-\>\>ZK: Request Proof (Private Data)  
        ZK--\>\>Agents: Return ZK\_Proof\_String  
    end  
    Agents-\>\>Hydra: Submit Vote \+ Proof  
    Hydra-\>\>Hydra: Consensus Reached (3/3)  
    Hydra--\>\>Orch: Final Verdict Signed  
    Orch-\>\>L1: Mint ThreatProof Capsule (CIP-25)  
    Orch--\>\>User: WebSocket Alert: DANGER

---

## **PART 6: THE 30-HOUR TIMELINE**

* **Hour 0-4 (Setup & Mock):**  
  * **M1:** API returning Test Vector A.  
  * **M5:** UI consuming Test Vector A.  
  * **M3/M4:** Docker containers running (Empty).  
* **Hour 5-15 (The Build):**  
  * **M2:** Write regex logic.  
  * **M3:** Connect python to Hydra socket.  
  * **M4:** Write Midnight wrapper.  
* **Hour 16-24 (The Integration):**  
  * Replace Mocks with Real Calls one by one.  
  * Order: Sentinel \-\> Hydra \-\> Midnight.  
* **Hour 25-28 (The Safety Buffer):**  
  * **FAIL-SAFE CHECK:** If Hydra is flaky, switch to "File-Based Consensus". If Midnight is flaky, switch to "Mock ZK".  
* **Hour 29-30 (The Show):**  
  * Record the perfect run. Pitch practice.

---

## **PART 7: THE "DON'T FAIL" RULES**

1. **Hydra is Static:** Do NOT try to manage heads dynamically. Start one head. Keep it running.  
2. **Frontend is King:** If the backend works but the frontend is ugly, you lose. If the backend is mocked but the frontend is beautiful, you might still win. Prioritize the Visuals.  
3. **Video is Insurance:** Record a video of the system working perfectly (even if mocked) *before* the live demo. If the live demo crashes, play the video.  
4. **No Live Training:** Do not train AI models during the hackathon. Use pre-set rules.

**This is the way. Execute.**

