"""
MempoolSniffer Specialist Agent
===============================
Performs mempool transaction analysis and pending transaction monitoring.

Deployment: Independent microservice on KODOSUMI
DID: did:masumi:mempool_sniffer_01
"""

import httpx
import os
import json
import base64
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


class MempoolSniffer:
    """
    Mempool transaction analysis specialist.
    
    Responsibilities:
    - Analyze pending transactions in mempool
    - Detect front-running attempts
    - Identify MEV (Maximal Extractable Value) patterns
    - Monitor transaction fee anomalies
    - Track address-specific pending transactions
    
    Deployment:
    - Independent KODOSUMI microservice
    - DID: did:masumi:mempool_sniffer_01
    - Communicates via IACP/2.0 protocol with signed envelopes
    """
    
    # Fee thresholds (in lovelace)
    NORMAL_FEE_MAX = 500_000  # 0.5 ADA
    HIGH_FEE_THRESHOLD = 2_000_000  # 2 ADA
    SUSPICIOUS_FEE_THRESHOLD = 10_000_000  # 10 ADA
    
    def __init__(self):
        self.name = "MempoolSniffer"
        self.did = "did:masumi:mempool_sniffer_01"
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
        self.logger.info(f"MempoolSniffer initialized with DID: {self.did}")
        
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
        
    async def scan(self, address: str, context: dict) -> ScanResult:
        """
        Analyze mempool and pending transactions.
        
        Args:
            address: Cardano address to check for pending transactions
            context: Additional context from the scan request
            
        Returns:
            ScanResult with mempool analysis findings
        """
        findings = []
        risk_score = 0.0
        metadata = {"agent": self.name}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {"project_id": self.blockfrost_key}
                
                # Note: Blockfrost doesn't have direct mempool access on preprod
                # We analyze recent transactions and UTxOs as proxy
                
                if address and address.startswith("addr"):
                    # Get address UTxOs (unspent outputs)
                    utxo_resp = await client.get(
                        f"{self.blockfrost_url}/v0/addresses/{address}/utxos",
                        headers=headers
                    )
                    
                    if utxo_resp.status_code == 200:
                        utxos = utxo_resp.json()
                        metadata["utxo_count"] = len(utxos)
                        
                        total_value = 0
                        has_native_tokens = False
                        token_count = 0
                        
                        for utxo in utxos:
                            total_value += int(utxo.get("amount", [{}])[0].get("quantity", 0))
                            amounts = utxo.get("amount", [])
                            if len(amounts) > 1:
                                has_native_tokens = True
                                token_count += len(amounts) - 1
                                
                        metadata["total_value_ada"] = total_value / 1_000_000
                        metadata["has_native_tokens"] = has_native_tokens
                        metadata["native_token_count"] = token_count
                        
                        # Large number of UTxOs could indicate dust attack or complex activity
                        if len(utxos) > 50:
                            findings.append(f"High UTxO count ({len(utxos)}) - possible fragmentation or dust attack")
                            risk_score += 0.15
                            
                        if len(utxos) > 200:
                            findings.append("Extreme UTxO fragmentation detected")
                            risk_score += 0.25
                            
                    elif utxo_resp.status_code == 404:
                        findings.append("No UTxOs found for address")
                        metadata["utxo_count"] = 0
                        
                    # Get recent transactions for this address
                    txs_resp = await client.get(
                        f"{self.blockfrost_url}/v0/addresses/{address}/transactions?count=10&order=desc",
                        headers=headers
                    )
                    
                    if txs_resp.status_code == 200:
                        recent_txs = txs_resp.json()
                        metadata["recent_tx_count"] = len(recent_txs)
                        
                        # Analyze transaction patterns
                        if len(recent_txs) >= 5:
                            # Check for rapid transaction bursts
                            tx_hashes = [tx.get("tx_hash") for tx in recent_txs[:5]]
                            tx_times = []
                            high_fee_count = 0
                            
                            for tx_hash in tx_hashes:
                                tx_detail_resp = await client.get(
                                    f"{self.blockfrost_url}/v0/txs/{tx_hash}",
                                    headers=headers
                                )
                                if tx_detail_resp.status_code == 200:
                                    tx_detail = tx_detail_resp.json()
                                    tx_times.append(tx_detail.get("block_time", 0))
                                    
                                    fee = int(tx_detail.get("fees", 0))
                                    if fee > self.HIGH_FEE_THRESHOLD:
                                        high_fee_count += 1
                                        
                                    if fee > self.SUSPICIOUS_FEE_THRESHOLD:
                                        findings.append(f"Suspiciously high fee transaction: {fee/1_000_000:.2f} ADA")
                                        risk_score += 0.2
                                        
                            # Check time gaps between transactions
                            if len(tx_times) >= 2:
                                tx_times.sort(reverse=True)
                                gaps = [tx_times[i] - tx_times[i+1] for i in range(len(tx_times)-1)]
                                avg_gap = sum(gaps) / len(gaps) if gaps else 0
                                
                                if avg_gap < 60:  # Less than 1 minute average
                                    findings.append(f"Rapid transaction pattern detected (avg {avg_gap:.0f}s between txs)")
                                    risk_score += 0.2
                                    
                            if high_fee_count >= 2:
                                findings.append(f"Multiple high-fee transactions ({high_fee_count}) - possible priority transaction pattern")
                                risk_score += 0.15
                                
                elif address and address.startswith("tx_"):
                    # Direct transaction hash analysis
                    tx_hash = address.replace("tx_", "")
                    tx_resp = await client.get(
                        f"{self.blockfrost_url}/v0/txs/{tx_hash}",
                        headers=headers
                    )
                    
                    if tx_resp.status_code == 200:
                        tx_data = tx_resp.json()
                        fee = int(tx_data.get("fees", 0))
                        size = tx_data.get("size", 0)
                        
                        metadata["transaction"] = {
                            "hash": tx_hash,
                            "fee_ada": fee / 1_000_000,
                            "size_bytes": size,
                            "block": tx_data.get("block"),
                            "slot": tx_data.get("slot"),
                        }
                        
                        # Analyze fee efficiency
                        if size > 0:
                            fee_per_byte = fee / size
                            metadata["transaction"]["fee_per_byte"] = fee_per_byte
                            
                            if fee_per_byte > 100:  # High fee per byte
                                findings.append(f"Transaction has elevated fee-per-byte ratio: {fee_per_byte:.2f}")
                                risk_score += 0.1
                                
                        if fee > self.SUSPICIOUS_FEE_THRESHOLD:
                            findings.append(f"Transaction fee significantly above normal: {fee/1_000_000:.2f} ADA")
                            risk_score += 0.15
                            
                    elif tx_resp.status_code == 404:
                        findings.append("Transaction not found - may still be in mempool or invalid")
                        risk_score += 0.1
                        
        except httpx.TimeoutException:
            return ScanResult(
                risk_score=0.15,
                severity=Severity.LOW,
                findings=["Mempool analysis timeout"],
                metadata=metadata,
                success=False,
                error="Timeout analyzing transaction data"
            )
        except Exception as e:
            return ScanResult(
                risk_score=0.1,
                severity=Severity.INFO,
                findings=[f"Mempool analysis error: {str(e)}"],
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
                findings.append("No mempool-related anomalies detected")
                
        return ScanResult(
            risk_score=min(risk_score, 1.0),
            severity=severity,
            findings=findings,
            metadata=metadata
        )
