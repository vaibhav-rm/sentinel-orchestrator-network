"""
VoteDoctor Specialist Agent
===========================
Performs governance vote analysis and voting pattern detection.

Deployment: Independent microservice on KODOSUMI
DID: did:masumi:vote_doctor_01
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


class VoteDoctor:
    """
    Governance vote analysis specialist.
    
    Responsibilities:
    - Analyze governance proposal voting patterns
    - Detect vote manipulation attempts
    - Monitor DRep (Delegated Representative) behavior
    - Track governance action submissions
    - Identify suspicious voting timing patterns
    
    Deployment:
    - Independent KODOSUMI microservice
    - DID: did:masumi:vote_doctor_01
    - Communicates via IACP/2.0 protocol with signed envelopes
    """
    
    def __init__(self):
        self.name = "VoteDoctor"
        self.did = "did:masumi:vote_doctor_01"
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
        self.logger.info(f"VoteDoctor initialized with DID: {self.did}")
        
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
        Analyze governance-related activity for the given address.
        
        Args:
            address: Cardano address to analyze for governance activity
            context: Additional context from the scan request
            
        Returns:
            ScanResult with governance analysis findings
        """
        findings = []
        risk_score = 0.0
        metadata = {"agent": self.name}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {"project_id": self.blockfrost_key}
                
                # Resolve stake address for governance checks
                stake_address = None
                if address.startswith("stake"):
                    stake_address = address
                elif address.startswith("addr"):
                    addr_resp = await client.get(
                        f"{self.blockfrost_url}/v0/addresses/{address}",
                        headers=headers
                    )
                    if addr_resp.status_code == 200:
                        stake_address = addr_resp.json().get("stake_address")
                        
                if stake_address:
                    metadata["stake_address"] = stake_address
                    
                    # Check if address is registered as a DRep
                    drep_resp = await client.get(
                        f"{self.blockfrost_url}/v0/governance/dreps/{stake_address}",
                        headers=headers
                    )
                    
                    if drep_resp.status_code == 200:
                        drep_data = drep_resp.json()
                        metadata["drep_info"] = {
                            "is_drep": True,
                            "drep_id": drep_data.get("drep_id"),
                            "active": drep_data.get("active", False),
                            "amount": int(drep_data.get("amount", 0)) / 1_000_000,
                        }
                        findings.append(f"Address is registered as DRep with {metadata['drep_info']['amount']:,.0f} ADA voting power")
                        
                        # Large DRep voting power could indicate concentration
                        if metadata["drep_info"]["amount"] > 50_000_000:  # > 50M ADA
                            findings.append("DRep has significant voting power concentration")
                            risk_score += 0.25
                            
                    elif drep_resp.status_code == 404:
                        metadata["drep_info"] = {"is_drep": False}
                        
                    # Check DRep delegation for this stake address
                    account_resp = await client.get(
                        f"{self.blockfrost_url}/v0/accounts/{stake_address}",
                        headers=headers
                    )
                    
                    if account_resp.status_code == 200:
                        account_data = account_resp.json()
                        drep_delegation = account_data.get("drep_id")
                        
                        if drep_delegation:
                            metadata["delegated_to_drep"] = drep_delegation
                            
                            # Check if delegated to "Always Abstain" or "Always No Confidence"
                            if drep_delegation == "drep_always_abstain":
                                findings.append("Address uses 'Always Abstain' governance delegation")
                            elif drep_delegation == "drep_always_no_confidence":
                                findings.append("Address uses 'Always No Confidence' governance delegation")
                                risk_score += 0.1  # Could indicate dissatisfaction or attack preparation
                                
                # Get recent governance actions
                gov_actions_resp = await client.get(
                    f"{self.blockfrost_url}/v0/governance/proposals?count=20&order=desc",
                    headers=headers
                )
                
                if gov_actions_resp.status_code == 200:
                    proposals = gov_actions_resp.json()
                    metadata["recent_proposals_count"] = len(proposals)
                    
                    # Analyze proposal types
                    action_types = {}
                    for proposal in proposals:
                        action_type = proposal.get("governance_type", "unknown")
                        action_types[action_type] = action_types.get(action_type, 0) + 1
                        
                    metadata["proposal_types"] = action_types
                    
                    # Check for concerning governance actions
                    concerning_actions = ["HardForkInitiation", "NoConfidence", "NewConstitution"]
                    for action_type, count in action_types.items():
                        if action_type in concerning_actions:
                            findings.append(f"Active {action_type} proposals detected ({count} total)")
                            risk_score += 0.15
                            
                    # Check for treasury withdrawal proposals
                    if "TreasuryWithdrawals" in action_types:
                        findings.append(f"Treasury withdrawal proposals active: {action_types['TreasuryWithdrawals']}")
                        risk_score += 0.1
                        
                elif gov_actions_resp.status_code == 404:
                    findings.append("No governance proposals found (may be pre-Conway era)")
                    
                # Check epoch-level governance parameters
                epoch_resp = await client.get(
                    f"{self.blockfrost_url}/v0/epochs/latest/parameters",
                    headers=headers
                )
                
                if epoch_resp.status_code == 200:
                    params = epoch_resp.json()
                    if params.get("drep_deposit"):
                        metadata["governance_params"] = {
                            "drep_deposit_ada": int(params.get("drep_deposit", 0)) / 1_000_000,
                            "gov_action_deposit_ada": int(params.get("gov_action_deposit", 0)) / 1_000_000,
                        }
                        
        except httpx.TimeoutException:
            return ScanResult(
                risk_score=0.15,
                severity=Severity.LOW,
                findings=["Governance data fetch timeout"],
                metadata=metadata,
                success=False,
                error="Timeout analyzing governance data"
            )
        except Exception as e:
            return ScanResult(
                risk_score=0.1,
                severity=Severity.INFO,
                findings=[f"Governance analysis error: {str(e)}"],
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
                findings.append("No governance-related risks detected")
                
        return ScanResult(
            risk_score=min(risk_score, 1.0),
            severity=severity,
            findings=findings,
            metadata=metadata
        )
