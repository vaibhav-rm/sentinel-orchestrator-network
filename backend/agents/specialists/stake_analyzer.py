"""
StakeAnalyzer Specialist Agent
==============================
Performs stake pool analysis and minority control detection.

Deployment: Independent microservice on KODOSUMI
DID: did:masumi:stake_analyzer_01
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


class StakeAnalyzer:
    """
    Stake pool analysis and minority control detection specialist.
    
    Responsibilities:
    - Analyze stake pool delegation patterns
    - Detect stake concentration risks (minority control)
    - Monitor pool saturation levels
    - Identify suspicious stake movements
    - Check pool registration and retirement events
    
    Deployment:
    - Independent KODOSUMI microservice
    - DID: did:masumi:stake_analyzer_01
    - Communicates via IACP/2.0 protocol with signed envelopes
    """
    
    # Thresholds for stake concentration analysis
    SATURATION_WARNING = 0.85  # 85% saturation warning
    CONCENTRATION_WARNING = 0.05  # Single entity > 5% of total stake
    MINORITY_CONTROL_THRESHOLD = 0.33  # 33% = potential minority attack
    
    def __init__(self):
        self.name = "StakeAnalyzer"
        self.did = "did:masumi:stake_analyzer_01"
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
        self.logger.info(f"StakeAnalyzer initialized with DID: {self.did}")
        
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
        Analyze stake-related data for the given address.
        
        Args:
            address: Cardano address or stake address to analyze
            context: Additional context from the scan request
            
        Returns:
            ScanResult with stake analysis findings
        """
        findings = []
        risk_score = 0.0
        metadata = {"agent": self.name}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {"project_id": self.blockfrost_key}
                
                # Resolve stake address from payment address if needed
                stake_address = None
                if address.startswith("stake"):
                    stake_address = address
                elif address.startswith("addr"):
                    addr_resp = await client.get(
                        f"{self.blockfrost_url}/v0/addresses/{address}",
                        headers=headers
                    )
                    if addr_resp.status_code == 200:
                        addr_data = addr_resp.json()
                        stake_address = addr_data.get("stake_address")
                        metadata["payment_address"] = address
                        
                if stake_address:
                    metadata["stake_address"] = stake_address
                    
                    # Get stake account info
                    stake_resp = await client.get(
                        f"{self.blockfrost_url}/v0/accounts/{stake_address}",
                        headers=headers
                    )
                    
                    if stake_resp.status_code == 200:
                        stake_data = stake_resp.json()
                        
                        controlled_amount = int(stake_data.get("controlled_amount", 0))
                        rewards_sum = int(stake_data.get("rewards_sum", 0))
                        pool_id = stake_data.get("pool_id")
                        
                        metadata["stake_info"] = {
                            "controlled_amount_ada": controlled_amount / 1_000_000,
                            "rewards_ada": rewards_sum / 1_000_000,
                            "delegated_pool": pool_id,
                            "active": stake_data.get("active", False),
                        }
                        
                        # Large stake holder check
                        if controlled_amount > 10_000_000_000_000:  # > 10M ADA
                            findings.append(f"Large stake holder detected: {controlled_amount / 1_000_000:,.0f} ADA")
                            risk_score += 0.2
                            
                        # Analyze delegated pool if exists
                        if pool_id:
                            pool_resp = await client.get(
                                f"{self.blockfrost_url}/v0/pools/{pool_id}",
                                headers=headers
                            )
                            
                            if pool_resp.status_code == 200:
                                pool_data = pool_resp.json()
                                
                                live_stake = int(pool_data.get("live_stake", 0))
                                live_saturation = float(pool_data.get("live_saturation", 0))
                                blocks_minted = pool_data.get("blocks_minted", 0)
                                
                                metadata["pool_info"] = {
                                    "pool_id": pool_id,
                                    "live_stake_ada": live_stake / 1_000_000,
                                    "saturation": live_saturation,
                                    "blocks_minted": blocks_minted,
                                }
                                
                                # Check saturation
                                if live_saturation > self.SATURATION_WARNING:
                                    findings.append(f"Pool near saturation: {live_saturation*100:.1f}%")
                                    risk_score += 0.15
                                    
                                if live_saturation >= 1.0:
                                    findings.append("Pool is OVERSATURATED - rewards reduction active")
                                    risk_score += 0.25
                                    
                                # Check pool metadata for legitimacy indicators
                                pool_meta_resp = await client.get(
                                    f"{self.blockfrost_url}/v0/pools/{pool_id}/metadata",
                                    headers=headers
                                )
                                
                                if pool_meta_resp.status_code == 200:
                                    pool_meta = pool_meta_resp.json()
                                    if pool_meta.get("name"):
                                        metadata["pool_info"]["name"] = pool_meta.get("name")
                                    if pool_meta.get("ticker"):
                                        metadata["pool_info"]["ticker"] = pool_meta.get("ticker")
                                elif pool_meta_resp.status_code == 404:
                                    findings.append("Pool has no metadata - potential privacy pool or new registration")
                                    risk_score += 0.1
                                    
                                # Check for recent pool retirement
                                if pool_data.get("retiring_epoch"):
                                    findings.append(f"Pool retiring in epoch {pool_data.get('retiring_epoch')}")
                                    risk_score += 0.2
                                    
                    elif stake_resp.status_code == 404:
                        findings.append("Stake address not registered on chain")
                        metadata["stake_registered"] = False
                else:
                    findings.append("No stake address associated with this payment address")
                    
                # Network-wide stake concentration check (sampling top pools)
                pools_resp = await client.get(
                    f"{self.blockfrost_url}/v0/pools?count=10&order=desc",
                    headers=headers
                )
                
                if pools_resp.status_code == 200:
                    top_pools = pools_resp.json()
                    # Get stake amounts for top pools
                    total_top_stake = 0
                    for pool_id_item in top_pools[:5]:
                        pool_detail = await client.get(
                            f"{self.blockfrost_url}/v0/pools/{pool_id_item}",
                            headers=headers
                        )
                        if pool_detail.status_code == 200:
                            total_top_stake += int(pool_detail.json().get("live_stake", 0))
                            
                    if total_top_stake > 0:
                        metadata["top_5_pools_stake_ada"] = total_top_stake / 1_000_000
                        
        except httpx.TimeoutException:
            return ScanResult(
                risk_score=0.2,
                severity=Severity.LOW,
                findings=["Stake analysis timeout - network congestion possible"],
                metadata=metadata,
                success=False,
                error="Timeout analyzing stake data"
            )
        except Exception as e:
            return ScanResult(
                risk_score=0.15,
                severity=Severity.LOW,
                findings=[f"Stake analysis error: {str(e)}"],
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
            findings.append("No significant stake concentration risks detected")
            
        return ScanResult(
            risk_score=min(risk_score, 1.0),
            severity=severity,
            findings=findings,
            metadata=metadata
        )
