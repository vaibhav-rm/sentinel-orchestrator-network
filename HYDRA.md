# Hydra Node Implementation in Sentinel Orchestrator Network

## 1. Why Hydra? (The Rationale)

The Sentinel Orchestrator Network (SON) is designed to be a high-performance security layer for the Cardano ecosystem. To achieve this, we integrated **Hydra**, Cardano's Layer 2 scalability solution.

### Key Drivers:
1.  **Ultra-Low Latency**: Mainnet block times are ~20 seconds. Hydra Head transactions confirm in **milliseconds**. This allows Sentinel to provide near real-time security scanning for high-frequency trading or rapid asset transfers.
2.  **High Throughput**: Hydra can handle thousands of transactions per second (TPS), far exceeding the Layer 1 limit. This ensures the Sentinel network doesn't become a bottleneck during network congestion.
3.  **Cost Efficiency**: Validation happens off-chain within the Hydra Head. We don't need to pay Layer 1 gas fees for every security check, only for opening/closing the head and settlement.
4.  **Isomorphic Design**: Hydra uses the *same* EUTxO model and Plutus scripts as Cardano Layer 1. This means our validation logic (`HydraNode` agent) works identically on both layers without rewriting code.

## 2. How It Works (The Architecture)

We implemented Hydra as a specialized **Agent** within the Sentinel network.

### Components:
*   **`HydraNode` Agent** (`backend/agents/hydra_node.py`): This is the high-level agent that acts as the interface. It receives scan requests from the Sentinel Orchestrator.
*   **`HydraClient`** (`backend/agents/hydra_client.py`): A dedicated WebSocket client that communicates directly with a running Hydra Node (default port `4001`).
*   **Sentinel Orchestrator** (`backend/agents/sentinel.py`): The brain that decides when to use Hydra.

### The Workflow:
1.  **Fast Path (Hydra)**: When a request comes in, Sentinel *first* asks the `HydraNode` to validate it.
    *   The `HydraNode` sends the transaction CBOR to the Hydra Head via WebSocket (`NewTx` message).
    *   If the Head validates it (returns `TxValid`), we get an instant **SAFE** verdict (Latency: <500ms).
2.  **Fallback (Oracle)**: If Hydra cannot validate it (e.g., the transaction is for an asset not in the Head, or CBOR is missing), it returns `verified: False`.
    *   Sentinel then escalates to the **Oracle Agent**.
    *   The Oracle performs a deep, slower on-chain check using **Koios** and **Blockfrost**.
3.  **Zero Trust Security**: We implemented a "Fail-Closed" mechanism. If Hydra fails or is offline, we *never* assume safety. We always fall back to the Oracle or flag a threat.

## 3. Technical Implementation Details

### WebSocket Communication
We use the `websockets` library to maintain a persistent connection to the Hydra Node API.
```python
# backend/agents/hydra_client.py
async def validate_tx(self, tx_cbor: str):
    message = {
        "tag": "NewTx",
        "transaction": {"type": "Hex", "cbor": tx_cbor}
    }
    # Sends to ws://localhost:4001 and awaits 'TxValid' or 'TxInvalid'
```

### Strict Validation Logic
In `backend/agents/hydra_node.py`, we ensure that missing data triggers a fallback, not a pass:
```python
if not tx_cbor:
    return {
        "verified": False, 
        "reason": "No TX CBOR - deferring to Oracle"
    }
```

### Integration with Sentinel
The Sentinel agent orchestrates the flow:
```python
# backend/agents/sentinel.py
# 1. Try Hydra
hydra_result = await self.hydra_node.validate_transaction(policy_id, tx_cbor)
if hydra_result["verified"]:
    return Vote.SAFE  # Instant return

# 2. If not verified, call Oracle
oracle_response = await self.oracle.process(...)
```

## 4. Summary
By integrating Hydra, we created a **Hybrid Security Model**:
*   **Layer 2 (Hydra)** provides speed and scalability for known/active channels.
*   **Layer 1 (Oracle)** provides global visibility and deep inspection for everything else.

This gives Sentinel the "best of both worlds"—the speed of a centralized API with the security and decentralization of Cardano.
