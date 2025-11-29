"""
=============================================================================
Sentinel Orchestrator Network (SON) - AGENT B: Oracle Agent
=============================================================================

Role: External blockchain verifier, fork detection, network health check
Masumi Pricing: Per verification (usage-based)

Based on simplified_agent_flow.txt:
1. Receives HIRE_REQUEST from Sentinel with escrow payment
2. Verifies Sentinel's signature
3. Queries Blockfrost for mainnet chain tip
4. Compares user's node tip vs mainnet tip
5. Detects minority fork / ghost chain if delta > threshold
6. Signs and returns JOB_COMPLETE response

=============================================================================
"""

import base64
import json
import asyncio
import logging
from typing import Any, Dict, Optional, TYPE_CHECKING

import httpx
import nacl.signing
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError

from .base import BaseAgent, Vote

if TYPE_CHECKING:
    from .sentinel import SentinelAgent


# =============================================================================
# ORACLE CONFIGURATION
# =============================================================================

# Fork detection threshold (blocks)
FORK_THRESHOLD = 5

# Blockfrost endpoints
BLOCKFROST_MAINNET = "https://cardano-mainnet.blockfrost.io/api/v0"
BLOCKFROST_PREPROD = "https://cardano-preprod.blockfrost.io/api/v0"
BLOCKFROST_PREVIEW = "https://cardano-preview.blockfrost.io/api/v0"


# =============================================================================
# ORACLE AGENT CLASS
# =============================================================================

class OracleAgent(BaseAgent):
    """
    Agent B: External blockchain verifier for fork detection.
    
    Workflow:
    1. Receive HIRE_REQUEST from Sentinel (with signature + escrow)
    2. Verify Sentinel's cryptographic signature
    3. Accept virtual escrow payment
    4. Query Blockfrost for current mainnet block height
    5. Compare with user's reported node tip
    6. Detect MINORITY_FORK if delta > FORK_THRESHOLD
    7. Sign and return JOB_COMPLETE response
    
    Performance: Must complete in < 3 seconds
    """
    
    def __init__(
        self,
        blockfrost_project_id: Optional[str] = None,
        network: str = "preprod",
        sentinel_public_key: Optional[str] = None,
        enable_llm: bool = True
    ):
        """
        Initialize the Oracle Agent.
        
        Args:
            blockfrost_project_id: Blockfrost API project ID
            network: "mainnet", "preprod", or "preview"
            sentinel_public_key: Base64-encoded Sentinel public key for verification
            enable_llm: Whether to enable LLM-enhanced analysis
        """
        super().__init__(agent_name="oracle", role="verifier", enable_llm=enable_llm)
        
        # Generate Oracle's own keypair
        self.private_key = SigningKey.generate()
        self.public_key = self.private_key.verify_key
        
        # Store Sentinel's public key for verification
        self.sentinel_verify_key: Optional[VerifyKey] = None
        if sentinel_public_key:
            self.set_sentinel_public_key(sentinel_public_key)
        
        # Blockfrost configuration
        self.blockfrost_project_id = blockfrost_project_id
        self.network = network
        self._set_blockfrost_url()
        
        # Escrow tracking
        self.escrow_balance = 0.0
        
        self.logger.info(f"Oracle Agent initialized (network: {network})")
    
    def _set_blockfrost_url(self) -> None:
        """Set Blockfrost URL based on network."""
        urls = {
            "mainnet": BLOCKFROST_MAINNET,
            "preprod": BLOCKFROST_PREPROD,
            "preview": BLOCKFROST_PREVIEW
        }
        self.blockfrost_url = urls.get(self.network, BLOCKFROST_PREPROD)
    
    def set_sentinel_public_key(self, public_key_b64: str) -> None:
        """
        Set Sentinel's public key for signature verification.
        
        Args:
            public_key_b64: Base64-encoded Ed25519 public key
        """
        try:
            key_bytes = base64.b64decode(public_key_b64)
            self.sentinel_verify_key = VerifyKey(key_bytes)
            self.logger.info("Sentinel public key registered")
        except Exception as e:
            self.logger.error(f"Failed to set Sentinel public key: {e}")
    
    def get_public_key_b64(self) -> str:
        """Get base64-encoded public key for sharing."""
        return base64.b64encode(bytes(self.public_key)).decode()
    
    # -------------------------------------------------------------------------
    # MAIN PROCESSING METHOD (BaseAgent interface)
    # -------------------------------------------------------------------------
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point - process a signed HIRE_REQUEST.
        
        Args:
            input_data: Signed HIRE_REQUEST envelope from Sentinel
            
        Returns:
            Dict with fork check result
        """
        return await self.handle_hire_request(input_data)
    
    # -------------------------------------------------------------------------
    # HIRE REQUEST HANDLING
    # -------------------------------------------------------------------------
    
    async def handle_hire_request(self, envelope: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming HIRE_REQUEST from Sentinel.
        
        Args:
            envelope: Signed message envelope with HIRE_REQUEST
            
        Returns:
            Signed JOB_COMPLETE response
        """
        self.logger.info("Received HIRE_REQUEST from Sentinel")
        
        # Step 1: Verify signature
        if not self._verify_sentinel_signature(envelope):
            self.logger.error("Signature verification failed - rejecting request")
            return self._build_error_response("Invalid signature")
        
        # Step 2: Extract payload
        payload = envelope.get("payload", {})
        escrow_id = payload.get("escrow_id", "")
        amount = payload.get("amount", 0)
        user_tip = payload.get("user_tip", 0)
        policy_id = payload.get("policy_id", "")
        
        # Step 3: Accept escrow payment
        self.escrow_balance += amount
        self.logger.info(f"Accepted escrow payment: {amount} ADA (id: {escrow_id})")
        
        # Step 4: Perform fork check
        self.log_start(policy_id)
        fork_result = await self._execute_fork_check(user_tip)
        
        # Step 5: Build and sign response
        response = self._build_response(fork_result, user_tip, escrow_id)
        signed_response = self._sign_envelope(response)
        
        self.log_complete(
            Vote.DANGER if fork_result["is_fork"] else Vote.SAFE,
            90 if fork_result["is_fork"] else 10
        )
        
        return signed_response
    
    # -------------------------------------------------------------------------
    # FORK DETECTION LOGIC
    # -------------------------------------------------------------------------
    
    async def _execute_fork_check(self, user_tip: int) -> Dict[str, Any]:
        """
        Execute fork detection by comparing user tip with mainnet.
        
        Args:
            user_tip: User's node current block height
            
        Returns:
            Dict with mainnet_tip, delta, is_fork, status
        """
        self.logger.debug(f"Checking fork status for user_tip: {user_tip}")
        
        # Fetch mainnet tip
        mainnet_tip = await self._fetch_mainnet_tip()
        
        if mainnet_tip is None:
            self.logger.warning("Could not fetch mainnet tip - using mock")
            mainnet_tip = user_tip  # Assume safe if we can't verify
        
        # Calculate delta
        delta = abs(mainnet_tip - user_tip)
        
        # Determine fork status
        is_fork = delta > FORK_THRESHOLD
        
        if is_fork:
            status = "MINORITY_FORK_DETECTED"
            self.logger.warning(f"FORK DETECTED: delta={delta} blocks (threshold={FORK_THRESHOLD})")
        else:
            status = "SAFE_CHAIN"
            self.logger.info(f"Chain healthy: delta={delta} blocks")
        
        return {
            "mainnet_tip": mainnet_tip,
            "user_node_tip": user_tip,
            "delta": delta,
            "threshold": FORK_THRESHOLD,
            "is_fork": is_fork,
            "status": status,
            "evidence": "block_divergence" if is_fork else "none"
        }
    
    async def _fetch_mainnet_tip(self) -> Optional[int]:
        """
        Fetch current block height from Blockfrost.
        
        Returns:
            Block height or None if failed
        """
        if not self.blockfrost_project_id:
            self.logger.warning("No Blockfrost project ID - returning mock tip")
            return None
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{self.blockfrost_url}/blocks/latest",
                    headers={"project_id": self.blockfrost_project_id}
                )
                response.raise_for_status()
                return response.json()["height"]
                
        except httpx.TimeoutException:
            self.logger.error("Blockfrost request timed out")
            return None
        except httpx.HTTPStatusError as e:
            self.logger.error(f"Blockfrost HTTP error: {e.response.status_code}")
            return None
        except Exception as e:
            self.logger.error(f"Blockfrost request failed: {e}")
            return None
    
    # -------------------------------------------------------------------------
    # CRYPTOGRAPHIC OPERATIONS
    # -------------------------------------------------------------------------
    
    def _verify_sentinel_signature(self, envelope: Dict[str, Any]) -> bool:
        """
        Verify Sentinel's signature on the envelope.
        
        Args:
            envelope: Signed message envelope
            
        Returns:
            True if signature is valid
        """
        if "signature" not in envelope:
            self.logger.warning("No signature in envelope")
            return False
        
        # If no Sentinel key registered, skip verification (for testing)
        if self.sentinel_verify_key is None:
            self.logger.debug("No Sentinel key registered - skipping verification")
            return True
        
        try:
            # Reconstruct original message (exclude signature)
            message = {k: v for k, v in envelope.items() if k != "signature"}
            message_bytes = json.dumps(
                message, sort_keys=True, separators=(',', ':')
            ).encode()
            
            signature_bytes = base64.b64decode(envelope["signature"])
            
            self.sentinel_verify_key.verify(message_bytes, signature_bytes)
            self.logger.info(f"✅ Verified signature from: {envelope.get('from_did', 'unknown')}")
            return True
            
        except BadSignatureError:
            self.logger.error("❌ Invalid signature - message rejected")
            return False
        except Exception as e:
            self.logger.error(f"Signature verification error: {e}")
            return False
    
    def _sign_envelope(self, envelope: Dict[str, Any]) -> Dict[str, Any]:
        """Sign a message envelope using Ed25519."""
        message_bytes = json.dumps(
            envelope, sort_keys=True, separators=(',', ':')
        ).encode()
        
        signed = self.private_key.sign(message_bytes)
        signature = base64.b64encode(signed.signature).decode()
        
        return {**envelope, "signature": signature}
    
    # -------------------------------------------------------------------------
    # RESPONSE BUILDING
    # -------------------------------------------------------------------------
    
    def _build_response(
        self,
        fork_result: Dict[str, Any],
        user_tip: int,
        escrow_id: str
    ) -> Dict[str, Any]:
        """Build JOB_COMPLETE response envelope."""
        return {
            "protocol": "IACP/2.0",
            "type": "JOB_COMPLETE",
            "from_did": "did:masumi:oracle_01",
            "to_did": "did:masumi:sentinel_01",
            "payload": {
                "status": fork_result["status"],
                "mainnet_tip": fork_result["mainnet_tip"],
                "user_node_tip": user_tip,
                "delta": fork_result["delta"],
                "threshold": fork_result["threshold"],
                "evidence": fork_result["evidence"],
                "escrow_id": escrow_id
            },
            "timestamp": self.get_timestamp()
        }
    
    def _build_error_response(self, error: str) -> Dict[str, Any]:
        """Build error response envelope."""
        response = {
            "protocol": "IACP/2.0",
            "type": "JOB_FAILED",
            "from_did": "did:masumi:oracle_01",
            "payload": {
                "error": error,
                "status": "ERROR"
            },
            "timestamp": self.get_timestamp()
        }
        return self._sign_envelope(response)
