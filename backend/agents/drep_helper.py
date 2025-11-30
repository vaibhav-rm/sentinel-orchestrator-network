"""
GovernanceOrchestrator
=====================
Orchestrates the 3-agent analysis pipeline and aggregates verdicts.
"""

import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from .proposal_fetcher import ProposalFetcher
from .policy_analyzer import PolicyAnalyzer
from .sentiment_analyzer import SentimentAnalyzer
from .treasury_guardian import TreasuryGuardian
from ..llm_config import AgentLLM

class GovernanceOrchestrator:
    """
    Orchestrates the 3-agent analysis pipeline.
    """
    
    def __init__(self):
        self.logger = logging.getLogger("SON.GovernanceOrchestrator")
        
        # Load environment variables from .env file
        load_dotenv()
        
        self.fetcher = ProposalFetcher()
        self.policy = PolicyAnalyzer()
        self.sentiment = SentimentAnalyzer()
        self.treasury = TreasuryGuardian()
        
        self.llm = AgentLLM("GovernanceOrchestrator")
        self.logger.info("GovernanceOrchestrator initialized with LLM capabilities")
    
    async def analyze_proposal(
        self,
        gov_action_id: str,
        ipfs_hash: str
    ) -> Dict[str, Any]:
        """
        Full analysis pipeline for a governance proposal.
        
        Args:
            gov_action_id: Governance action ID
            ipfs_hash: IPFS hash containing proposal metadata
            
        Returns:
            Dict with complete analysis and verdict
        """
        
        logs = []
        
        # Agent 1: Fetch metadata
        self.logger.info(f"Fetching metadata for {gov_action_id}")
        metadata = await self.fetcher.fetch_metadata(ipfs_hash)
        
        # LLM analysis of proposal content
        proposal_analysis = await self.fetcher.analyze_proposal_content(metadata)
        logs.append(self.fetcher.generate_log(metadata, proposal_analysis))
        
        # Agent 2: Policy analysis
        self.logger.info("Running policy compliance check")
        policy_analysis = await self.policy.analyze({
            'title': metadata.title,
            'abstract': metadata.abstract,
            'motivation': metadata.motivation,
            'rationale': metadata.rationale,
            'amount': metadata.amount
        })
        
        # LLM analysis of policy compliance
        policy_llm_analysis = await self.policy.analyze_with_llm({
            'title': metadata.title,
            'abstract': metadata.abstract,
            'motivation': metadata.motivation,
            'rationale': metadata.rationale,
            'amount': metadata.amount,
            'flags': policy_analysis.flags,
            'reasoning': policy_analysis.reasoning
        })
        logs.append(self.policy.generate_log(policy_analysis, policy_llm_analysis))
        
        # Agent 3: Sentiment analysis
        self.logger.info("Analyzing community sentiment")
        sentiment = await self.sentiment.analyze(gov_action_id)
        
        # LLM analysis of sentiment patterns
        sentiment_analysis = await self.sentiment.analyze_sentiment_patterns(sentiment, gov_action_id)
        logs.append(self.sentiment.generate_log(sentiment, sentiment_analysis))
        
        # Final LLM synthesis
        final_analysis = await self._synthesize_analysis(
            metadata, policy_analysis, sentiment, 
            proposal_analysis, policy_llm_analysis, sentiment_analysis
        )
        
        # Aggregate verdict
        verdict = self._aggregate_verdict(policy_analysis, sentiment, metadata)
        
        # Agent 4: Treasury risk analysis
        self.logger.info("Analyzing treasury withdrawal risks")
        treasury_analysis = await self.treasury.analyze({
            'proposer': getattr(metadata, 'proposer', 'unknown'),
            'amount': metadata.amount,
            'title': metadata.title,
            'abstract': metadata.abstract
        })
        logs.append(self.treasury.generate_log(treasury_analysis))

        # Aggregate verdict
        verdict = self._aggregate_verdict(policy_analysis, sentiment, metadata, treasury_analysis)
        
        return {
            "gov_action_id": gov_action_id,
            "metadata": {
                "title": metadata.title,
                "amount_ada": metadata.amount / 1_000_000
            },
            "policy_analysis": {
                "recommendation": policy_analysis.recommendation,
                "flags": policy_analysis.flags,
                "reasoning": policy_analysis.reasoning,
                "confidence": policy_analysis.confidence
            },
            "sentiment": {
                "category": sentiment.sentiment,
                "support": sentiment.support_percentage,
                "sample_size": sentiment.sample_size
            },
            "treasury_analysis": {
                "risk_score": treasury_analysis.risk_score,
                "z_score": treasury_analysis.z_score,
                "contextual_risk": treasury_analysis.contextual_risk,
                "ncl_violation": treasury_analysis.ncl_violation,
                "flags": treasury_analysis.flags,
                "reasoning": treasury_analysis.reasoning
            },
            "verdict": verdict,
            "llm_synthesis": final_analysis,
            "logs": logs
        }
    
    def _aggregate_verdict(self, policy, sentiment, metadata, treasury) -> Dict[str, Any]:
        """
        Agentic Logic: Combine agent recommendations.
        """
        
        # Rule 1: Treasury risk override - high risk proposals auto-reject
        if treasury.risk_score > 80:
            return {
                "recommendation": "NO",
                "reason": f"High treasury risk detected ({treasury.risk_score:.1f}/100) - {treasury.reasoning}",
                "confidence": 0.95,
                "auto_votable": True
            }

        # Rule 2: If 2+ policy flags, auto-reject
        if len(policy.flags) >= 2:
            return {
                "recommendation": "NO",
                "reason": f"Multiple compliance violations: {', '.join(policy.flags[:2])}",
                "confidence": 0.9,
                "auto_votable": True
            }
        
        # Rule 3: Strong community opposition overrides
        if sentiment.support_percentage < 30:
            return {
                "recommendation": "NO",
                "reason": f"Strong community opposition ({sentiment.support_percentage:.0f}% support)",
                "confidence": 0.85,
                "auto_votable": True
            }
        
        # Rule 4: High-value proposals require manual review
        amount = metadata.amount / 1_000_000
        if amount > 25_000_000:
            return {
                "recommendation": "ABSTAIN",
                "reason": f"High-value proposal ({amount:,.0f} ADA) requires manual review",
                "confidence": 0.7,
                "auto_votable": False
            }
        
        # Rule 5: Follow policy recommendation if confidence is high
        if policy.confidence > 0.7:
            return {
                "recommendation": policy.recommendation,
                "reason": policy.reasoning,
                "confidence": policy.confidence,
                "auto_votable": policy.recommendation in ['YES', 'NO']
            }
        
        # Default: Abstain if uncertain
        return {
            "recommendation": "ABSTAIN",
            "reason": "Insufficient data for confident recommendation",
            "confidence": 0.5,
            "auto_votable": False
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing method for BaseAgent compatibility.
        Expects input_data with 'proposal_id' and optionally 'ipfs_hash'.
        """
        proposal_id = input_data.get("proposal_id", "")
        ipfs_hash = input_data.get("ipfs_hash", "")

        if not proposal_id:
            return {
                "error": "Missing proposal_id",
                "status": "failed"
            }

        # For now, use a mock IPFS hash if not provided
        if not ipfs_hash:
            # Mock IPFS hash for demonstration
            ipfs_hash = "QmXyz1234567890abcdef"

        return await self.analyze_proposal(proposal_id, ipfs_hash)
    
    async def _synthesize_analysis(
        self,
        metadata,
        policy_analysis,
        sentiment,
        proposal_analysis,
        policy_llm_analysis,
        sentiment_analysis
    ) -> Optional[str]:
        """
        Use LLM to synthesize all analyses into comprehensive governance assessment.
        
        Returns:
            str synthesis or None if LLM unavailable
        """
        if not self.llm.is_available:
            self.logger.debug("LLM not available for final synthesis")
            return None
        
        try:
            prompt = self._build_synthesis_prompt(
                metadata, policy_analysis, sentiment,
                proposal_analysis, policy_llm_analysis, sentiment_analysis
            )
            synthesis = await self.llm._generate_content(prompt)
            return synthesis
        except Exception as e:
            self.logger.error(f"LLM synthesis failed: {e}")
            return None
    
    def _build_synthesis_prompt(
        self,
        metadata,
        policy_analysis,
        sentiment,
        proposal_analysis,
        policy_llm_analysis,
        sentiment_analysis
    ) -> str:
        """Build prompt for comprehensive governance analysis synthesis."""
        
        # Extract key data points
        proposal_quality = proposal_analysis.get('content_quality', {}).get('score', 'N/A') if proposal_analysis else 'N/A'
        risk_level = proposal_analysis.get('risk_assessment', {}).get('level', 'N/A') if proposal_analysis else 'N/A'
        alignment = proposal_analysis.get('alignment_score', {}).get('score', 'N/A') if proposal_analysis else 'N/A'
        recommendation = proposal_analysis.get('recommendation', {}).get('decision', 'N/A') if proposal_analysis else 'N/A'
        
        policy_flags = len(policy_analysis.flags)
        policy_confidence = policy_analysis.confidence
        
        sentiment_category = sentiment.sentiment
        support_pct = sentiment.support_percentage
        engagement = sentiment_analysis.get('engagement', {}).get('level', 'N/A') if sentiment_analysis else 'N/A'
        consensus = sentiment_analysis.get('consensus', {}).get('strength', 'N/A') if sentiment_analysis else 'N/A'
        
        return f"""You are a Cardano governance expert providing comprehensive analysis of a governance proposal.

**PROPOSAL OVERVIEW**
Title: {metadata.title}
Amount: {metadata.amount / 1_000_000:,.0f} ADA
Abstract: {metadata.abstract[:200]}...

**ANALYSIS SUMMARY**

Proposal Quality:
- Content Score: {proposal_quality}/10
- Risk Level: {risk_level}
- Alignment Score: {alignment}/10
- Initial Recommendation: {recommendation}

Policy Compliance:
- Flags Raised: {policy_flags}
- Confidence Level: {policy_confidence:.1f}
- Key Issues: {', '.join(policy_analysis.flags[:3]) if policy_analysis.flags else 'None'}

Community Sentiment:
- Sentiment Category: {sentiment_category}
- Support Percentage: {support_pct:.1f}%
- Engagement Level: {engagement}
- Consensus Strength: {consensus}

**SYNTHESIS REQUIREMENTS**

Provide a comprehensive governance assessment covering:

1. **OVERALL ASSESSMENT**: Holistic evaluation considering all factors
2. **KEY STRENGTHS**: Most compelling positive aspects
3. **PRIMARY CONCERNS**: Most significant risks or issues
4. **COMMUNITY ALIGNMENT**: How well this serves Cardano's interests
5. **FINAL RECOMMENDATION**: YES/NO/ABSTAIN with confidence level and reasoning

**FORMAT YOUR RESPONSE AS:**
OVERALL: [comprehensive assessment in 2-3 sentences]
STRENGTHS: [2-3 key positive factors]
CONCERNS: [2-3 main issues or risks]
ALIGNMENT: [assessment of Cardano fit]
RECOMMENDATION: [YES/NO/ABSTAIN] ([confidence 0-100]%) - [brief justification]

Be analytical, balanced, and focus on governance impact. Consider technical, financial, and community factors."""
