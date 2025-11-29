"""
ReplayDetector Specialist Agent
===============================
Performs transaction replay detection and double-spend analysis.

Deployment: Independent microservice on KODOSUMI
DID: did:masumi:replay_detector_01
"""

import httpx
import os
import json
import base64
import hashlib
import logging
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum

import nacl.signing
from nacl.signing import SigningKey


class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class ScanResult:
    """Result from a specialist scan operation."""
    risk_score: float  # 0.0 - 1.0
    severity: Severity
    findings: list[str]
    metadata: dict
    success: bool = True
    error: Optional[str] = None


class ReplayDetector:
    """
    Transaction replay detection specialist.
    
    Responsibilities:
    - Detect potential transaction replay attacks
    - Identify double-spend attempts
    - Analyze transaction input/output patterns
    - Check for UTxO reuse anomalies
    - Monitor script validation failures
    
    Deployment:
    - Independent KODOSUMI microservice
    - DID: did:masumi:replay_detector_01
    - Communicates via IACP/2.0 protocol with signed envelopes
    """
    
    def __init__(self):
        self.name = "ReplayDetector"
        self.did = "did:masumi:replay_detector_01"
        self.blockfrost_url = os.getenv("BLOCKFROST_API_URL", "https://cardano-preprod.blockfrost.io/api")
        self.blockfrost_key = os.getenv("BLOCKFROST_API_KEY", "")
        
        # Setup logging
        self.logger = logging.getLogger(f"SON.{self.name}")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                f'[%(asctime)s] [{self.name.upper()}] %(levelname)s: %(message)s'
            ))
            self.logger.addHandler(handler)
        
        # Cryptographic keypair for message signing
        self.private_key = SigningKey.generate()
        self.public_key = self.private_key.verify_key
        self.logger.info(f"ReplayDetector initialized with DID: {self.did}")
        
        # In production, this would be a persistent cache (Redis, etc.)
        self._seen_tx_patterns: dict[str, int] = {}
        
    def get_public_key_b64(self) -> str:
        """Get base64-encoded public key for registration."""
        return base64.b64encode(bytes(self.public_key)).decode()
    
    def get_did(self) -> str:
        """Get the DID for this specialist."""
        return self.did
    
    def _sign_response(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Sign a response envelope using Ed25519."""
        envelope = {
            "protocol": "IACP/2.0",
            "type": "SCAN_RESPONSE",
            "from_did": self.did,
            "payload": payload,
            "timestamp": self._get_timestamp(),
        }
        
        message_bytes = json.dumps(
            envelope, sort_keys=True, separators=(',', ':')
        ).encode()
        
        signed = self.private_key.sign(message_bytes)
        signature = base64.b64encode(signed.signature).decode()
        
        return {**envelope, "signature": signature}
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current UTC timestamp in ISO 8601 format."""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        
    def _compute_tx_pattern_hash(self, inputs: list, outputs: list) -> str:
        """Compute a hash of transaction input/output pattern for replay detection."""
        pattern_data = []
        
        # Normalize inputs
        for inp in sorted(inputs, key=lambda x: x.get("tx_hash", "") + str(x.get("output_index", 0))):
            pattern_data.append(f"i:{inp.get('tx_hash', '')}:{inp.get('output_index', 0)}")
            
        # Normalize outputs (by address and amount)
        for out in sorted(outputs, key=lambda x: x.get("address", "")):
            amounts = out.get("amount", [])
            for amt in amounts:
                pattern_data.append(f"o:{out.get('address', '')}:{amt.get('unit', '')}:{amt.get('quantity', '')}")
                
        pattern_str = "|".join(pattern_data)
        return hashlib.sha256(pattern_str.encode()).hexdigest()[:16]
        
    async def scan(self, address: str, context: dict) -> ScanResult:
        """
        Analyze for replay attacks and double-spend attempts.
        
        Args:
            address: Cardano address or transaction hash to analyze
            context: Additional context from the scan request
            
        Returns:
            ScanResult with replay detection findings
        """
        findings = []
        risk_score = 0.0
        metadata = {"agent": self.name}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {"project_id": self.blockfrost_key}
                
                transactions_to_analyze = []
                
                if address.startswith("tx_") or len(address) == 64:
                    # Direct transaction hash
                    tx_hash = address.replace("tx_", "")
                    transactions_to_analyze.append(tx_hash)
                elif address.startswith("addr"):
                    # Get recent transactions for address
                    txs_resp = await client.get(
                        f"{self.blockfrost_url}/v0/addresses/{address}/transactions?count=20&order=desc",
                        headers=headers
                    )
                    
                    if txs_resp.status_code == 200:
                        recent_txs = txs_resp.json()
                        transactions_to_analyze = [tx.get("tx_hash") for tx in recent_txs[:10]]
                        metadata["transactions_analyzed"] = len(transactions_to_analyze)
                        
                # Analyze each transaction
                for tx_hash in transactions_to_analyze:
                    # Get full transaction details
                    tx_resp = await client.get(
                        f"{self.blockfrost_url}/v0/txs/{tx_hash}",
                        headers=headers
                    )
                    
                    if tx_resp.status_code != 200:
                        continue
                        
                    tx_data = tx_resp.json()
                    
                    # Get UTxOs (inputs and outputs)
                    utxo_resp = await client.get(
                        f"{self.blockfrost_url}/v0/txs/{tx_hash}/utxos",
                        headers=headers
                    )
                    
                    if utxo_resp.status_code != 200:
                        continue
                        
                    utxo_data = utxo_resp.json()
                    inputs = utxo_data.get("inputs", [])
                    outputs = utxo_data.get("outputs", [])
                    
                    # Compute pattern hash
                    pattern_hash = self._compute_tx_pattern_hash(inputs, outputs)
                    
                    # Check for similar patterns (potential replay)
                    if pattern_hash in self._seen_tx_patterns:
                        prev_count = self._seen_tx_patterns[pattern_hash]
                        findings.append(f"Similar transaction pattern detected (seen {prev_count + 1} times)")
                        risk_score += 0.3
                        self._seen_tx_patterns[pattern_hash] = prev_count + 1
                    else:
                        self._seen_tx_patterns[pattern_hash] = 1
                        
                    # Check for script validation issues
                    if tx_data.get("valid_contract") is False:
                        findings.append(f"Transaction {tx_hash[:16]}... has invalid contract execution")
                        risk_score += 0.4
                        
                    # Check redeemers (script executions)
                    redeemers_resp = await client.get(
                        f"{self.blockfrost_url}/v0/txs/{tx_hash}/redeemers",
                        headers=headers
                    )
                    
                    if redeemers_resp.status_code == 200:
                        redeemers = redeemers_resp.json()
                        if redeemers:
                            metadata["has_scripts"] = True
                            metadata["redeemer_count"] = len(redeemers)
                            
                            for redeemer in redeemers:
                                # Check execution units
                                ex_units = redeemer.get("unit_mem", 0), redeemer.get("unit_steps", 0)
                                if ex_units[0] > 10_000_000 or ex_units[1] > 5_000_000_000:
                                    findings.append("High execution unit consumption - complex script execution")
                                    risk_score += 0.1
                                    
                    # Analyze input patterns for double-spend indicators
                    input_addresses = set()
                    for inp in inputs:
                        inp_addr = inp.get("address", "")
                        if inp_addr in input_addresses:
                            findings.append("Multiple inputs from same address in single transaction")
                            # This is actually normal, just noting it
                        input_addresses.add(inp_addr)
                        
                        # Check if input was recently created and quickly spent
                        if inp.get("data_hash"):
                            findings.append("Transaction uses datum-locked input (script validation)")
                            
                    # Check for circular transaction patterns
                    output_addresses = set(out.get("address", "") for out in outputs)
                    overlap = input_addresses & output_addresses
                    
                    if overlap and len(overlap) == len(input_addresses) == len(output_addresses):
                        findings.append("Circular transaction pattern detected (outputs return to input addresses)")
                        risk_score += 0.2
                        
                    # Check for dust outputs (potential spam/attack)
                    dust_outputs = 0
                    for out in outputs:
                        amounts = out.get("amount", [])
                        ada_amount = 0
                        for amt in amounts:
                            if amt.get("unit") == "lovelace":
                                ada_amount = int(amt.get("quantity", 0))
                                break
                        if ada_amount < 1_500_000:  # Less than 1.5 ADA (min UTxO)
                            dust_outputs += 1
                            
                    if dust_outputs > 2:
                        findings.append(f"Multiple dust outputs ({dust_outputs}) - possible fragmentation attack")
                        risk_score += 0.15
                        
                # Network-level check: recent failed transactions
                if address.startswith("addr"):
                    # This would require indexing failed txs which Blockfrost doesn't directly expose
                    # In production, you'd have your own node or specialized indexer
                    pass
                    
        except httpx.TimeoutException:
            return ScanResult(
                risk_score=0.2,
                severity=Severity.LOW,
                findings=["Replay detection timeout - high network load"],
                metadata=metadata,
                success=False,
                error="Timeout during replay analysis"
            )
        except Exception as e:
            return ScanResult(
                risk_score=0.15,
                severity=Severity.LOW,
                findings=[f"Replay detection error: {str(e)}"],
                metadata=metadata,
                success=False,
                error=str(e)
            )
            
        # Determine severity
        if risk_score >= 0.7:
            severity = Severity.CRITICAL
        elif risk_score >= 0.5:
            severity = Severity.HIGH
        elif risk_score >= 0.3:
            severity = Severity.MEDIUM
        elif risk_score >= 0.1:
            severity = Severity.LOW
        else:
            severity = Severity.INFO
            if not findings:
                findings.append("No replay attack indicators detected")
                
        return ScanResult(
            risk_score=min(risk_score, 1.0),
            severity=severity,
            findings=findings,
            metadata=metadata
        )
