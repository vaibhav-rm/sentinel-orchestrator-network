"""
TreasuryGuardian Agent
=====================
Uses Gemini AI for intelligent treasury withdrawal anomaly detection.
Combines statistical analysis with contextual reasoning.
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import httpx
from dotenv import load_dotenv

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

@dataclass
class TreasuryAnalysis:
    """Result from treasury analysis"""
    risk_score: float
    z_score: float
    contextual_risk: float
    ncl_violation: bool
    flags: List[str]
    reasoning: str

class TreasuryGuardian:
    """
    Agent that detects treasury withdrawal anomalies using Gemini AI.
    """

    NCL_ANNUAL_CAP = 47_250_000_000_000  # 47.25M ADA in lovelace
    KOIOS_BASE_URL = "https://api.koios.rest/api/v1"

    TREASURY_ANALYSIS_RULES = """
CARDANO TREASURY RISK ANALYSIS FRAMEWORK:

1. STATISTICAL ANOMALIES:
   - Z-score > 3: Highly unusual amount
   - Amount > 47.25M ADA: Violates Net Change Limit (15% of 315M treasury)

2. CONTEXTUAL RISK FACTORS:
   - New proposer (< 30 days): Higher risk
   - Vague justification: Lack of specific deliverables/milestones
   - Unusual timing: End of quarter/periods
   - Related party transactions: Conflicts of interest

3. HISTORICAL PATTERNS:
   - Compare against last 12 months treasury withdrawals
   - Flag amounts 2+ standard deviations from mean
   - Consider proposal frequency and proposer history

4. PROPOSAL QUALITY:
   - Clear budget breakdown required
   - Specific success metrics needed
   - Verifiable deliverables essential
   """

    def __init__(self):
        self.logger = logging.getLogger("SON.TreasuryGuardian")

        # Load environment variables
        load_dotenv()

        self.koios_client = httpx.AsyncClient(
            base_url=self.KOIOS_BASE_URL,
            headers={"accept": "application/json"}
        )

        # Initialize Gemini
        if GEMINI_AVAILABLE:
            api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel(
                    'gemini-2.0-flash-exp',
                    generation_config={
                        "response_mime_type": "application/json",
                        "temperature": 0.2
                    }
                )
                self.logger.info("TreasuryGuardian initialized with Gemini")
            else:
                self.model = None
                self.logger.warning("GEMINI_API_KEY not set")
        else:
            self.model = None
            self.logger.warning("google-generativeai not installed")

    async def analyze(self, proposal_metadata) -> TreasuryAnalysis:
        """
        Analyze treasury proposal for anomalies using Gemini AI.

        Args:
            proposal_metadata: Dict with proposal details

        Returns:
            TreasuryAnalysis with risk assessment
        """

        proposer = proposal_metadata.get('proposer', '')
        amount = proposal_metadata.get('amount', 0)
        amount_ada = amount / 1_000_000

        # 1. Fetch historical data for statistical analysis
        self.logger.info("Fetching historical treasury data")
        history = await self._fetch_history()
        z_score = self._calculate_zscore(amount, history)

        # 2. NCL check
        ncl_status = self._check_ncl(amount)

        # 3. Get proposer age (mock for now)
        proposer_age_days = await self._get_proposer_age(proposer)

        # 4. Gemini contextual analysis
        contextual_risk = await self._analyze_with_gemini(proposal_metadata, z_score, ncl_status)

        # 5. Calculate composite risk score
        risk_score = self._calculate_risk_score(z_score, contextual_risk, proposer_age_days)

        # 6. Generate flags
        flags = []
        if abs(z_score) > 3:
            flags.append(f"STATISTICAL_ANOMALY: Z-score {z_score:.2f} > 3")
        if ncl_status:
            flags.append("NCL_VIOLATION: Exceeds Net Change Limit (47.25M ADA)")
        if proposer_age_days < 30:
            flags.append(f"NEW_PROPOSER: Wallet age {proposer_age_days} days < 30")
        if contextual_risk > 0.7:
            flags.append(f"CONTEXTUAL_RISK: High contextual risk ({contextual_risk:.2f})")

        return TreasuryAnalysis(
            risk_score=risk_score,
            z_score=z_score,
            contextual_risk=contextual_risk,
            ncl_violation=ncl_status,
            flags=flags,
            reasoning=self._generate_reasoning(z_score, contextual_risk, ncl_status, proposer_age_days)
        )

    async def _analyze_with_gemini(self, proposal_metadata: Dict, z_score: float, ncl_violation: bool) -> float:
        """Use Gemini to analyze contextual risk factors"""
        if not self.model:
            # Fallback: simple heuristic
            text = (proposal_metadata.get('title', '') +
                   proposal_metadata.get('abstract', '') +
                   proposal_metadata.get('motivation', '')).lower()

            risk_factors = 0
            if 'urgent' in text or 'emergency' in text:
                risk_factors += 0.3
            if len(text.split()) < 50:  # Very short proposal
                risk_factors += 0.2
            if not any(word in text for word in ['milestone', 'deliverable', 'metric']):
                risk_factors += 0.3

            return min(risk_factors, 1.0)

        amount_ada = proposal_metadata.get('amount', 0) / 1_000_000

        prompt = f"""
You are a Cardano Treasury Risk Analyst AI. Analyze this treasury withdrawal proposal for contextual risk factors.

PROPOSAL DETAILS:
Title: {proposal_metadata.get('title', 'N/A')}
Abstract: {proposal_metadata.get('abstract', 'N/A')[:500]}
Motivation: {proposal_metadata.get('motivation', 'N/A')[:500]}
Amount: {amount_ada:,.0f} ADA ({proposal_metadata.get('amount', 0):,} lovelace)

STATISTICAL CONTEXT:
- Z-Score: {z_score:.2f}
- NCL Violation: {'YES' if ncl_violation else 'NO'}

TREASURY RISK FRAMEWORK:
{self.TREASURY_ANALYSIS_RULES}

OUTPUT FORMAT (strict JSON):
{{
  "contextual_risk_score": 0.0-1.0,
  "risk_factors": ["FACTOR_1: explanation", "FACTOR_2: explanation"],
  "recommendation": "LOW_RISK" | "MEDIUM_RISK" | "HIGH_RISK" | "REJECT",
  "reasoning": "2-3 sentence explanation of risk assessment"
}}

CRITICAL RISK INDICATORS:
- Score > 0.8: Immediate rejection recommended
- Vague or incomplete proposals: +0.3 risk
- New/unverified proposers: +0.2 risk
- Unusual amounts: +0.2 risk
- Poor justification: +0.3 risk
        """

        try:
            response = self.model.generate_content(prompt)
            analysis_dict = json.loads(response.text)

            self.logger.info(f"Gemini contextual analysis: {analysis_dict.get('recommendation', 'UNKNOWN')}")
            return analysis_dict.get('contextual_risk_score', 0.5)

        except Exception as e:
            self.logger.error(f"Gemini analysis failed: {e}")
            return 0.5  # Neutral fallback

    async def _fetch_history(self) -> List[float]:
        """Fetch historical treasury withdrawals from Koios"""
        try:
            # Query recent transactions (mock treasury detection)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)

            params = {
                "select": "amount",
                "_tx_hash->>is_valid": "eq.true",
                "_and": [
                    {"tx_timestamp": f"gte.{start_date.isoformat()}"},
                    {"tx_timestamp": f"lte.{end_date.isoformat()}"}
                ],
                "limit": "500"
            }

            response = await self.koios_client.get("/tx_info", params=params)
            data = response.json()

            # Extract transaction amounts (mock treasury filtering)
            amounts = []
            for tx in data:
                if tx.get('amount') and tx['amount'] > 1_000_000_000:  # > 1k ADA
                    amounts.append(float(tx['amount']))

            self.logger.info(f"Fetched {len(amounts)} historical transactions")
            return amounts[:100] if amounts else [10_000_000_000_000] * 30  # Fallback

        except Exception as e:
            self.logger.error(f"Failed to fetch history: {e}")
            return [10_000_000_000_000, 5_000_000_000_000, 25_000_000_000_000] * 30

    def _calculate_zscore(self, amount: float, history: List[float]) -> float:
        """Calculate Z-score for proposal amount"""
        if not history:
            return 0.0

        mean = sum(history) / len(history)
        std_dev = (sum((x - mean) ** 2 for x in history) / len(history)) ** 0.5

        if std_dev == 0:
            return 0.0

        return (amount - mean) / std_dev

    def _check_ncl(self, amount: float) -> bool:
        """Check if amount violates Net Change Limit"""
        return amount > self.NCL_ANNUAL_CAP

    async def _get_proposer_age(self, proposer: str) -> int:
        """Get proposer wallet age in days (mock implementation)"""
        # In production: query wallet creation date from blockchain
        return 60  # Mock: 60 days old

    def _calculate_risk_score(self, z_score: float, contextual_risk: float, proposer_age_days: int) -> float:
        """Calculate composite risk score (0-100)"""
        # Statistical component (30%)
        z_component = min(abs(z_score) / 3.0, 1.0)

        # Contextual component (40%)
        contextual_component = contextual_risk

        # Proposer risk component (20%)
        proposer_risk = 1.0 if proposer_age_days < 30 else 0.0

        # NCL component (10%) - handled separately in flags
        ncl_risk = 0.0  # Already flagged separately

        risk_score = (
            z_component * 0.3 +
            contextual_component * 0.4 +
            proposer_risk * 0.2 +
            ncl_risk * 0.1
        ) * 100

        return min(risk_score, 100.0)

    def _generate_reasoning(self, z_score: float, contextual_risk: float,
                          ncl_violation: bool, proposer_age_days: int) -> str:
        """Generate human-readable reasoning"""
        reasons = []

        if abs(z_score) > 3:
            reasons.append(f"statistically anomalous (Z-score: {z_score:.2f})")
        if ncl_violation:
            reasons.append("violates Net Change Limit")
        if contextual_risk > 0.7:
            reasons.append("high contextual risk factors")
        if proposer_age_days < 30:
            reasons.append("new proposer (< 30 days)")

        if not reasons:
            return "No significant risk factors detected"

        return f"Risk due to: {', '.join(reasons)}"

    def generate_log(self, analysis: TreasuryAnalysis) -> str:
        """Generate Matrix-style terminal log output"""
        flags_str = "\n".join([f"   🚨 {flag}" for flag in analysis.flags])

        return f"""
[TREASURY GUARDIAN] Risk Analysis Complete
├─ Risk Score: {analysis.risk_score:.1f}/100
├─ Z-Score: {analysis.z_score:.2f}
├─ Contextual Risk: {analysis.contextual_risk:.3f}
├─ NCL Violation: {'YES' if analysis.ncl_violation else 'NO'}
├─ Flags Raised: {len(analysis.flags)}
{flags_str if flags_str else '   ✓ No anomalies detected'}
└─ Reasoning: {analysis.reasoning}
        """

    async def close(self):
        """Cleanup resources"""
        await self.koios_client.aclose()
