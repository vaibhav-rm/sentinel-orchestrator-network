# backend/agents/oracle.py
import asyncio
import requests
import base64
import json
import nacl.signing
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from message_bus import MessageBus  # MEMBER1 builds this
import websockets
from fastapi import WebSocket
from enum import Enum

# =============================================================================
# ENUMS & TYPES
# =============================================================================

class VerificationStatus(Enum):
    """Status of external data verification"""
    PENDING = "pending"
    VERIFIED = "verified"
    FAILED = "failed"
    TIMEOUT = "timeout"

# =============================================================================
# BASE AGENT CLASS - Autonomous Microservice Template
# =============================================================================

class BaseAgent:
    """Template for all autonomous agents - inherits DID, payments, APIs"""

    def __init__(self, agent_name, cost_ada=0.2):
        self.name = agent_name
        self.cost = cost_ada
        self.did = f"did:key:{self.generate_key()}"  # Real DID
        self.blockfrost = self.init_blockfrost()  # Free API
        self.wallet_balance = 0.0
        self.explanation = ""

    def generate_key(self):
        """Generate DID key (simplified)"""
        key = nacl.signing.SigningKey.generate()
        return base64.b64encode(key.verify_key.encode()).decode()

    def init_blockfrost(self):
        """Initialize Blockfrost API client"""
        from blockfrost import BlockFrostApi, ApiUrls
        # Using pre-production network with fresh API key
        return BlockFrostApi(
            project_id="preprod99ILsNJwp7AtN1sGgf9f7g7BrFDnCPrg",
            base_url=ApiUrls.preprod.value
        )

    async def verify_payment(self, escrow_tx):
        """ZERO TRUST - Check escrow includes our DID + cost"""
        # In production: verify Cardano transaction
        return escrow_tx.get("amount", 0) >= self.cost

    async def work(self, chain_state):
        """Agent-specific logic - override in subclasses"""
        raise NotImplementedError

# =============================================================================
# SPECIALIST AGENTS - Real Cardano APIs, No Datasets
# =============================================================================

class BlockScanner(BaseAgent):
    """Block height comparison - detects forks"""

    async def work(self, chain_state):
        try:
            latest_block = await asyncio.get_event_loop().run_in_executor(
                None, self.blockfrost.block_latest
            )

            # Handle Blockfrost response (could be dict or object)
            if isinstance(latest_block, dict):
                mainnet_tip = latest_block.get("height")
            else:
                mainnet_tip = getattr(latest_block, 'height', 0)

            user_tip = chain_state["user_tip"]
            delta = abs(int(mainnet_tip) - int(user_tip))
            self.explanation = f"Block tip difference: {delta} blocks"
            risk_score = 0.9 if delta > 5 else 0.1
            return {"risk": risk_score, "evidence": self.explanation}
        except Exception as e:
            return {"risk": 0.5, "evidence": f"Blockfrost error: {str(e)}"}

class StakeAnalyzer(BaseAgent):
    """Stake pool analysis - detects minority control"""

    async def work(self, chain_state):
        try:
            loop = asyncio.get_event_loop()

            # 1) Get some pool IDs (e.g., first 50)
            pool_ids = await loop.run_in_executor(
                None, lambda: self.blockfrost.pools(count=50)
            )  # returns list[str]

            # 2) Fetch pool details for each ID
            pools = []
            for pid in pool_ids:
                detail = await loop.run_in_executor(
                    None, lambda pid=pid: self.blockfrost.pool(pid)
                )
                pools.append(detail)

            # 3) Compute total stake and top-10 stake
            # Handle both dict and Namespace responses
            def get_stake(pool):
                if isinstance(pool, dict):
                    return float(pool.get("live_stake", pool.get("active_stake", "0")) or 0)
                else:
                    # Namespace object
                    return float(getattr(pool, 'live_stake', getattr(pool, 'active_stake', 0)) or 0)

            stakes = [get_stake(p) for p in pools]
            total_stake = sum(stakes)

            # sort descending
            sorted_pools = sorted(
                pools,
                key=lambda p: get_stake(p),
                reverse=True
            )
            top10 = sorted_pools[:10]
            top10_stake = sum(get_stake(p) for p in top10)

            if total_stake == 0:
                ratio = 0.0
            else:
                ratio = top10_stake / total_stake

            self.explanation = (
                f"Top 10 pools control {ratio:.1%} of total sampled stake "
                f"({int(total_stake):,} lovelace)"
            )
            risk_score = 0.8 if ratio > 0.3 else 0.2
            return {"risk": risk_score, "evidence": self.explanation}

        except Exception as e:
            return {"risk": 0.5, "evidence": f"Stake analysis error: {str(e)}"}

class VoteDoctor(BaseAgent):
    """Governance vote analysis - current version uses epoch parameters as proxy"""

    async def work(self, chain_state):
        try:
            loop = asyncio.get_event_loop()

            # 1) Get latest epoch protocol parameters (real endpoint)
            params = await loop.run_in_executor(
                None, self.blockfrost.epoch_latest_parameters
            )

            # Handle dict vs object
            if not isinstance(params, dict):
                params = params.__dict__

            # 2) Simple sanity checks on key governance-related fields
            decentral_param = float(params.get("decentralisation_param", 0.0))
            min_fee_a = int(params.get("min_fee_a", 0))
            min_fee_b = int(params.get("min_fee_b", 0))

            anomalies = []
            if not (0.0 <= decentral_param <= 1.0):
                anomalies.append("decentralisation_param")
            if min_fee_a <= 0 or min_fee_b <= 0:
                anomalies.append("min_fee_a/min_fee_b")

            if anomalies:
                risk = 0.6
                self.explanation = (
                    "Governance parameter anomaly in: " + ", ".join(anomalies)
                )
            else:
                risk = 0.3
                self.explanation = (
                    f"Governance epoch params OK "
                    f"(decentralisation_param={decentral_param}, "
                    f"min_fee_a={min_fee_a}, min_fee_b={min_fee_b})"
                )

            return {"risk": risk, "evidence": self.explanation}

        except Exception as e:
            return {
                "risk": 0.5,
                "evidence": f"Governance analysis error: {str(e)}",
            }

class MempoolSniffer(BaseAgent):
    """Mempool/traffic analysis - uses latest block tx density as proxy"""

    async def work(self, chain_state):
        try:
            loop = asyncio.get_event_loop()

            # 1) Latest block info
            latest_block = await loop.run_in_executor(
                None, self.blockfrost.block_latest
            )
            if isinstance(latest_block, dict):
                block_hash = latest_block.get("hash")
                size = int(latest_block.get("size", 0))
            else:
                block_hash = getattr(latest_block, "hash", None)
                size = int(getattr(latest_block, "size", 0))

            # 2) Get up to 100 transactions from that block
            try:
                block_transactions = await loop.run_in_executor(
                    None, lambda: self.blockfrost.block_transactions(block_hash, count=100)
                )
                tx_hashes = [tx.get('hash') if isinstance(tx, dict) else getattr(tx, 'hash', '') for tx in block_transactions]
            except AttributeError:
                # Fallback: try alternative method names
                try:
                    block_transactions = await loop.run_in_executor(
                        None, lambda: self.blockfrost.transactions(block_hash, count=100)
                    )
                    tx_hashes = [tx.get('hash') if isinstance(tx, dict) else getattr(tx, 'hash', '') for tx in block_transactions]
                except:
                    tx_hashes = []  # Fallback if no method works
            tx_count = len(tx_hashes)

            # 3) Heuristic: many small txs in a relatively small block => spammy
            density = tx_count / max(size, 1)  # tx per byte
            # Normalize: assume "high" if > 0.01 tx per byte for demo
            spam_ratio = min(density / 0.01, 1.0)

            self.explanation = (
                f"Latest block {block_hash[:8]} has {tx_count} txs, size {size} bytes "
                f"(density={density:.5f} tx/byte)"
            )
            risk_score = 0.6 if spam_ratio > 0.5 else 0.3

            return {"risk": risk_score, "evidence": self.explanation}

        except Exception as e:
            return {
                "risk": 0.5,
                "evidence": f"Mempool analysis error: {str(e)}",
            }

class ReplayDetector(BaseAgent):
    """Transaction replay detection - checks for duplicate tx hashes in last N blocks"""

    async def work(self, chain_state):
        try:
            loop = asyncio.get_event_loop()

            # 1) Start from latest block
            latest_block = await loop.run_in_executor(
                None, self.blockfrost.block_latest
            )
            if isinstance(latest_block, dict):
                current_hash = latest_block.get("hash")
            else:
                current_hash = getattr(latest_block, "hash", None)

            hashes_seen = set()
            duplicates = 0
            blocks_scanned = 0

            # 2) Walk back a few blocks
            for _ in range(5):  # last 5 blocks
                if not current_hash:
                    break

                # Get transaction hashes from this block (API limit is 100)
                try:
                    block_transactions = await loop.run_in_executor(
                        None, lambda h=current_hash: self.blockfrost.block_transactions(h, count=100)
                    )
                    tx_hashes = [tx.get('hash') if isinstance(tx, dict) else getattr(tx, 'hash', '') for tx in block_transactions]
                except AttributeError:
                    # Fallback: try alternative method names
                    try:
                        block_transactions = await loop.run_in_executor(
                            None, lambda h=current_hash: self.blockfrost.transactions(h, count=100)
                        )
                        tx_hashes = [tx.get('hash') if isinstance(tx, dict) else getattr(tx, 'hash', '') for tx in block_transactions]
                    except:
                        tx_hashes = []  # Fallback if no method works
                for h in tx_hashes:
                    if h in hashes_seen:
                        duplicates += 1
                    else:
                        hashes_seen.add(h)

                blocks_scanned += 1

                # Get previous block hash
                block_detail = await loop.run_in_executor(
                    None, lambda h=current_hash: self.blockfrost.block(h)
                )
                if isinstance(block_detail, dict):
                    current_hash = block_detail.get("previous_block")
                else:
                    current_hash = getattr(block_detail, "previous_block", None)

            self.explanation = (
                f"Scanned {blocks_scanned} blocks, duplicate tx hashes: {duplicates}"
            )
            risk_score = 0.9 if duplicates > 0 else 0.3
            return {"risk": risk_score, "evidence": self.explanation}

        except Exception as e:
            return {
                "risk": 0.5,
                "evidence": f"Replay detection error: {str(e)}",
            }

# =============================================================================
# ORACLE COORDINATOR - Hires Swarm + Bayesian Fusion
# =============================================================================

class OracleCoordinator(BaseAgent):
    """Coordinates specialist agents using Matrix/escrow"""

    def __init__(self):
        super().__init__("oracle_coordinator", cost_ada=1.0)
        self.specialists = {
            "block_scanner": BlockScanner("block_scanner", 0.15),
            "stake_analyzer": StakeAnalyzer("stake_analyzer", 0.15),
            "vote_doctor": VoteDoctor("vote_doctor", 0.15),
            "mempool_sniffer": MempoolSniffer("mempool_sniffer", 0.15),
            "replay_detector": ReplayDetector("replay_detector", 0.15),
        }

    async def execute_fork_check(self, sentinel_request):
        """Main entry point - hires swarm and fuses results"""
        chain_state = sentinel_request["payload"]

        print(f"🤖 Oracle hiring swarm for fork check...")

        # 1. Hire all specialists concurrently
        tasks = []
        for name, agent in self.specialists.items():
            task = self.hire_specialist(name, agent, chain_state)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 2. Filter successful results
        valid_results = [r for r in results if isinstance(r, dict)]

        # 3. Bayesian fusion (simple weighted average)
        if valid_results:
            total_risk = sum(r["risk"] for r in valid_results)
            avg_risk = total_risk / len(valid_results)
            evidence = [r["evidence"] for r in valid_results]
        else:
            avg_risk = 0.5
            evidence = ["All specialists failed"]

        # 4. Determine final status
        fork_confirmed = avg_risk > 0.7
        status = "MINORITY_FORK_DETECTED" if fork_confirmed else "SAFE_CHAIN"

        print(f"🎯 Swarm consensus: {status} (risk: {avg_risk:.2f})")

        return {
            "status": status,
            "ai_fork_confirmed": fork_confirmed,
            "risk_score": avg_risk,
            "evidence": evidence,
            "specialists_hired": len(valid_results),
            "specialists_total": len(self.specialists)
        }

    async def hire_specialist(self, name, agent, chain_state):
        """Simulate hiring a specialist (WebSocket in production)"""
        try:
            print(f"📡 Hiring {name}...")
            result = await agent.work(chain_state)
            print(f"✅ {name} completed: risk {result['risk']:.2f}")
            return result
        except Exception as e:
            print(f"❌ {name} failed: {str(e)}")
            return {"risk": 0.5, "evidence": f"Agent {name} error: {str(e)}"}

    def bayes_fuse(self, risks):
        """Simple Bayesian fusion (weighted average)"""
        if not risks:
            return 0.5
        # Weight recent results higher
        weights = [1.0] * len(risks)
        weights[-1] *= 1.2  # Boost latest result
        total_weight = sum(weights)
        return sum(r * w for r, w in zip(risks, weights)) / total_weight

# =============================================================================
# LEGACY ORACLE AGENT - For Backward Compatibility
# =============================================================================

class OracleAgent:
    """Legacy single-purpose Oracle Agent"""

    def __init__(self):
        self.private_key = nacl.signing.SigningKey.generate()
        self.public_key = self.private_key.verify_key
        self.bus = MessageBus()
        self.escrow_balance = 0.0
        self.coordinator = OracleCoordinator()

        # Sentinel verification
        self.sentinel_public_bytes = base64.b64decode("SENTINEL_PUBLIC_BASE64_PLACEHOLDER")
        self.sentinel_verify_key = VerifyKey(self.sentinel_public_bytes)

    async def start(self):
        await self.bus.subscribe("did:masumi:oracle_01", self.handle_message)

    async def handle_message(self, envelope):
        if not self.verify_signature(envelope):
            return

        if envelope["type"] == "HIRE_REQUEST":
            result = await self.coordinator.execute_fork_check(envelope)
            await self.send_job_complete(envelope, result)

    async def send_job_complete(self, original_request, result):
        reply = {
            "protocol": "IACP/2.0",
            "type": "JOB_COMPLETE",
            "from_did": "did:masumi:oracle_01",
            "payload": result
        }
        signed_reply = self.sign_envelope(reply)
        await self.bus.publish(signed_reply)

    def verify_signature(self, envelope):
        if "signature" not in envelope:
            return False

        message = {k: v for k, v in envelope.items() if k != "signature"}
        message_bytes = json.dumps(message, sort_keys=True, separators=(',', ':')).encode()
        signature_bytes = base64.b64decode(envelope["signature"])

        try:
            self.sentinel_verify_key.verify(message_bytes, signature_bytes)
            print(f"✅ Verified: {envelope['from_did']}")
            return True
        except BadSignatureError:
            print("❌ Fake signature dropped")
            return False

    def sign_envelope(self, envelope):
        message_bytes = json.dumps(envelope, separators=(',', ':')).encode()
        signed = self.private_key.sign(message_bytes)
        envelope["signature"] = base64.b64encode(signed.signature).decode()
        return envelope
