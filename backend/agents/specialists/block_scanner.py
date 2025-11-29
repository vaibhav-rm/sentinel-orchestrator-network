"""
BlockScanner Specialist Agent
=============================
Performs block height comparison and fork detection analysis.

Deployment: Independent microservice on KODOSUMI
DID: did:masumi:block_scanner_01
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


class BlockScanner:
    """
    Block height comparison and fork detection specialist.
    
    Responsibilities:
    - Compare block heights across multiple sources
    - Detect potential chain forks
    - Identify block propagation anomalies
    - Analyze slot leader schedule consistency
    
    Deployment:
    - Independent KODOSUMI microservice
    - DID: did:masumi:block_scanner_01
    - Communicates via IACP/2.0 protocol with signed envelopes
    """
    
    def __init__(self):
        self.name = "BlockScanner"
        self.did = "did:masumi:block_scanner_01"
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
        self.logger.info(f"BlockScanner initialized with DID: {self.did}")
        
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
        Analyze block-level data for anomalies.
        
        Args:
            address: Cardano address or transaction hash to analyze
            context: Additional context from the scan request
            
        Returns:
            ScanResult with risk assessment and findings
        """
        findings = []
        risk_score = 0.0
        metadata = {"agent": self.name}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {"project_id": self.blockfrost_key}
                
                # Get latest block info
                block_resp = await client.get(
                    f"{self.blockfrost_url}/v0/blocks/latest",
                    headers=headers
                )
                
                if block_resp.status_code == 200:
                    block_data = block_resp.json()
                    metadata["latest_block"] = {
                        "height": block_data.get("height"),
                        "hash": block_data.get("hash"),
                        "slot": block_data.get("slot"),
                        "epoch": block_data.get("epoch"),
                        "block_vrf": block_data.get("block_vrf"),
                    }
                    
                    # Check block time consistency
                    block_time = block_data.get("time", 0)
                    import time
                    current_time = int(time.time())
                    time_diff = abs(current_time - block_time)
                    
                    if time_diff > 120:  # More than 2 minutes behind
                        findings.append(f"Block propagation delay detected: {time_diff}s behind")
                        risk_score += 0.2
                        
                    if time_diff > 300:  # More than 5 minutes
                        findings.append("Severe block propagation issue - possible fork")
                        risk_score += 0.3
                        
                    # Check slot leader consistency (if pool_id present)
                    if block_data.get("slot_leader"):
                        metadata["slot_leader"] = block_data.get("slot_leader")
                        
                    # Get previous blocks to check chain continuity
                    prev_hash = block_data.get("previous_block")
                    if prev_hash:
                        prev_resp = await client.get(
                            f"{self.blockfrost_url}/v0/blocks/{prev_hash}",
                            headers=headers
                        )
                        if prev_resp.status_code == 200:
                            prev_data = prev_resp.json()
                            height_diff = block_data.get("height", 0) - prev_data.get("height", 0)
                            if height_diff != 1:
                                findings.append(f"Chain continuity issue: height gap of {height_diff}")
                                risk_score += 0.4
                else:
                    findings.append(f"Failed to fetch block data: HTTP {block_resp.status_code}")
                    risk_score += 0.1
                    
                # If address provided, check address-specific block activity
                if address and not address.startswith("tx_"):
                    addr_resp = await client.get(
                        f"{self.blockfrost_url}/v0/addresses/{address}",
                        headers=headers
                    )
                    if addr_resp.status_code == 200:
                        addr_data = addr_resp.json()
                        metadata["address_info"] = {
                            "stake_address": addr_data.get("stake_address"),
                            "type": addr_data.get("type"),
                        }
                    elif addr_resp.status_code == 404:
                        findings.append("Address not found on chain - may be new or invalid")
                        risk_score += 0.05
                        
        except httpx.TimeoutException:
            return ScanResult(
                risk_score=0.3,
                severity=Severity.MEDIUM,
                findings=["Block data fetch timeout - network issues possible"],
                metadata=metadata,
                success=False,
                error="Timeout connecting to blockchain"
            )
        except Exception as e:
            return ScanResult(
                risk_score=0.2,
                severity=Severity.LOW,
                findings=[f"Block scan error: {str(e)}"],
                metadata=metadata,
                success=False,
                error=str(e)
            )
            
        # Determine severity based on risk score
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
            findings.append("No block-level anomalies detected")
            
        return ScanResult(
            risk_score=min(risk_score, 1.0),
            severity=severity,
            findings=findings,
            metadata=metadata
        )
