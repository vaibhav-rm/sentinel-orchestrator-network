"""
=============================================================================
Sentinel Orchestrator Network (SON) - LLM Configuration
=============================================================================

This module provides the Gemini LLM configuration for all SON agents.
It initializes the Google Generative AI client and provides helper functions
for agent reasoning capabilities.

=============================================================================
"""

import os
import logging
from typing import Any, Dict, List, Optional

# Try to import google.generativeai, handle gracefully if not installed
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =============================================================================
# LLM CONFIGURATION
# =============================================================================

# Environment variable for Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
LLM_ENABLED = os.getenv("LLM_ENABLED", "true").lower() == "true"

# Logger for LLM operations
logger = logging.getLogger("SON.llm")


# =============================================================================
# LLM CLIENT INITIALIZATION
# =============================================================================

def init_gemini_client() -> bool:
    """
    Initialize the Gemini API client with the configured API key.
    
    Returns:
        bool: True if initialization succeeded, False otherwise
    """
    if not GEMINI_AVAILABLE:
        logger.warning("google-generativeai package not installed. LLM features disabled.")
        return False
    
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY not set in environment. LLM features disabled.")
        return False
    
    if not LLM_ENABLED:
        logger.info("LLM features disabled via LLM_ENABLED=false")
        return False
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        logger.info(f"Gemini client initialized with model: {GEMINI_MODEL}")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Gemini client: {e}")
        return False


def get_gemini_model():
    """
    Get the configured Gemini model instance.
    
    Returns:
        GenerativeModel or None if not available
    """
    if not GEMINI_AVAILABLE or not GEMINI_API_KEY or not LLM_ENABLED:
        return None
    
    try:
        return genai.GenerativeModel(GEMINI_MODEL)
    except Exception as e:
        logger.error(f"Failed to get Gemini model: {e}")
        return None


# =============================================================================
# LLM HELPER CLASS
# =============================================================================

class AgentLLM:
    """
    LLM helper class for SON agents.
    
    Provides convenient methods for agents to use Gemini for:
    - Threat analysis reasoning
    - Evidence interpretation
    - Cross-verification logic
    - Natural language explanations
    """
    
    def __init__(self, agent_name: str):
        """
        Initialize the LLM helper for a specific agent.
        
        Args:
            agent_name: Name of the agent using this LLM helper
        """
        self.agent_name = agent_name
        self.logger = logging.getLogger(f"SON.{agent_name}.llm")
        self.model = None
        self.enabled = False
        
        # Try to initialize
        if init_gemini_client():
            self.model = get_gemini_model()
            self.enabled = self.model is not None
            if self.enabled:
                self.logger.info(f"LLM enabled for {agent_name} agent")
            else:
                self.logger.warning(f"LLM model not available for {agent_name} agent")
        else:
            self.logger.info(f"LLM disabled for {agent_name} agent - using rule-based logic only")
    
    @property
    def is_available(self) -> bool:
        """Check if LLM is available for use."""
        return self.enabled and self.model is not None
    
    async def analyze_threat(
        self,
        contract_data: Dict[str, Any],
        findings: List[Dict[str, Any]],
        context: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Use LLM to analyze threats and provide reasoning.
        
        Args:
            contract_data: Contract information (CBOR, metadata, source)
            findings: List of detected threat findings
            context: Additional context for analysis
            
        Returns:
            Dict with LLM analysis or None if LLM unavailable
        """
        if not self.is_available:
            return None
        
        try:
            prompt = self._build_threat_analysis_prompt(contract_data, findings, context)
            response = await self._generate_content(prompt)
            
            return {
                "llm_analysis": response,
                "model_used": GEMINI_MODEL,
                "agent": self.agent_name
            }
        except Exception as e:
            self.logger.error(f"LLM threat analysis failed: {e}")
            return None
    
    async def explain_verdict(
        self,
        verdict: str,
        score: int,
        findings: List[Dict[str, Any]],
        vote_breakdown: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Generate a natural language explanation for a verdict.
        
        Args:
            verdict: SAFE, WARNING, or DANGER
            score: Risk score (0-100)
            findings: List of threat findings
            vote_breakdown: Optional breakdown of all agent votes
            
        Returns:
            str explanation or None if LLM unavailable
        """
        if not self.is_available:
            return None
        
        try:
            prompt = self._build_explanation_prompt(verdict, score, findings, vote_breakdown)
            response = await self._generate_content(prompt)
            return response
        except Exception as e:
            self.logger.error(f"LLM explanation generation failed: {e}")
            return None
    
    async def cross_verify_analysis(
        self,
        sentinel_findings: Dict[str, Any],
        external_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Use LLM to cross-verify Sentinel findings with external data.
        
        Args:
            sentinel_findings: Findings from Sentinel Agent
            external_data: Liquidity, holder data, etc.
            
        Returns:
            Dict with verification analysis or None if LLM unavailable
        """
        if not self.is_available:
            return None
        
        try:
            prompt = self._build_verification_prompt(sentinel_findings, external_data)
            response = await self._generate_content(prompt)
            
            return {
                "llm_verification": response,
                "model_used": GEMINI_MODEL,
                "agent": self.agent_name
            }
        except Exception as e:
            self.logger.error(f"LLM cross-verification failed: {e}")
            return None
    
    async def assess_compliance_risk(
        self,
        wallet_data: Dict[str, Any],
        risk_indicators: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Use LLM to assess compliance risk based on wallet analysis.
        
        Args:
            wallet_data: Wallet analysis data (age, transactions, etc.)
            risk_indicators: List of identified risk indicators
            
        Returns:
            Dict with compliance assessment or None if LLM unavailable
        """
        if not self.is_available:
            return None
        
        try:
            prompt = self._build_compliance_prompt(wallet_data, risk_indicators)
            response = await self._generate_content(prompt)
            
            return {
                "llm_compliance_assessment": response,
                "model_used": GEMINI_MODEL,
                "agent": self.agent_name
            }
        except Exception as e:
            self.logger.error(f"LLM compliance assessment failed: {e}")
            return None
    
    async def generate_consensus_summary(
        self,
        vote_breakdown: Dict[str, Any],
        final_verdict: str,
        final_score: int
    ) -> Optional[str]:
        """
        Generate a summary of the consensus decision.
        
        Args:
            vote_breakdown: All agent votes and weights
            final_verdict: Final consensus verdict
            final_score: Final weighted score
            
        Returns:
            str summary or None if LLM unavailable
        """
        if not self.is_available:
            return None
        
        try:
            prompt = self._build_consensus_prompt(vote_breakdown, final_verdict, final_score)
            response = await self._generate_content(prompt)
            return response
        except Exception as e:
            self.logger.error(f"LLM consensus summary failed: {e}")
            return None
    
    # -------------------------------------------------------------------------
    # PRIVATE METHODS
    # -------------------------------------------------------------------------
    
    async def _generate_content(self, prompt: str) -> str:
        """
        Generate content using the Gemini model.
        
        Args:
            prompt: The prompt to send to the model
            
        Returns:
            str: The model's response text
        """
        if not self.model:
            raise RuntimeError("LLM model not initialized")
        
        # Use async generation if available, otherwise sync
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            self.logger.error(f"Gemini generation error: {e}")
            raise
    
    def _build_threat_analysis_prompt(
        self,
        contract_data: Dict[str, Any],
        findings: List[Dict[str, Any]],
        context: Optional[str]
    ) -> str:
        """Build prompt for threat analysis."""
        findings_str = "\n".join([
            f"- {f.get('type', 'unknown')}: {f.get('description', '')} (severity: {f.get('severity', 'unknown')})"
            for f in findings
        ]) if findings else "No threats detected."
        
        return f"""You are a security expert analyzing a Cardano smart contract for potential threats.

**Contract Information:**
- Policy ID: {contract_data.get('policy_id', 'unknown')[:32]}...
- Metadata: {contract_data.get('metadata', {})}

**Detected Findings:**
{findings_str}

**Additional Context:**
{context or 'No additional context provided.'}

**Task:**
Provide a brief security analysis (2-3 sentences) explaining:
1. The overall risk level of this contract
2. Key concerns if any threats were detected
3. Confidence in the assessment

Keep the response concise and actionable."""
    
    def _build_explanation_prompt(
        self,
        verdict: str,
        score: int,
        findings: List[Dict[str, Any]],
        vote_breakdown: Optional[Dict[str, Any]]
    ) -> str:
        """Build prompt for verdict explanation."""
        findings_str = ", ".join([f.get("type", "unknown") for f in findings]) if findings else "none"
        
        return f"""You are explaining a security scan result to a user.

**Verdict:** {verdict}
**Risk Score:** {score}/100
**Detected Issues:** {findings_str}

Generate a clear, user-friendly explanation (2-3 sentences) of what this means for the user.
Use simple language and be direct about any risks or safety concerns."""
    
    def _build_verification_prompt(
        self,
        sentinel_findings: Dict[str, Any],
        external_data: Dict[str, Any]
    ) -> str:
        """Build prompt for cross-verification."""
        return f"""You are cross-verifying threat detection findings with external market data.

**Sentinel Agent Findings:**
- Risk Score: {sentinel_findings.get('risk_score', 0)}
- Vote: {sentinel_findings.get('vote', 'unknown')}
- Findings Count: {len(sentinel_findings.get('findings', []))}

**External Market Data:**
- Liquidity (ADA): {external_data.get('total_liquidity_ada', 0):,}
- Holder Count: {external_data.get('total_holders', 0)}
- Top 10 Concentration: {external_data.get('top10_percentage', 0)}%

**Task:**
In 1-2 sentences, assess whether the external data confirms or contradicts the Sentinel's findings.
Focus on liquidity health and holder distribution as key verification signals."""
    
    def _build_compliance_prompt(
        self,
        wallet_data: Dict[str, Any],
        risk_indicators: List[Dict[str, Any]]
    ) -> str:
        """Build prompt for compliance assessment."""
        indicators_str = "\n".join([
            f"- {ind.get('indicator', 'unknown')}: {ind.get('description', '')}"
            for ind in risk_indicators
        ]) if risk_indicators else "No risk indicators."
        
        return f"""You are a compliance analyst assessing wallet risk.

**Wallet Profile:**
- Age: {wallet_data.get('age_days', 0)} days
- Transaction Count: {wallet_data.get('tx_count', 0)}
- Unique Interactions: {wallet_data.get('unique_interactions', 0)}

**Risk Indicators:**
{indicators_str}

**Task:**
Provide a brief compliance assessment (1-2 sentences) focusing on:
1. Whether the wallet profile raises regulatory concerns
2. Recommended risk level adjustment"""
    
    def _build_consensus_prompt(
        self,
        vote_breakdown: Dict[str, Any],
        final_verdict: str,
        final_score: int
    ) -> str:
        """Build prompt for consensus summary."""
        votes_str = "\n".join([
            f"- {agent}: {data.get('vote', 'unknown')} (weight: {data.get('weight', 0)*100:.0f}%)"
            for agent, data in vote_breakdown.items()
        ])
        
        return f"""You are summarizing a multi-agent consensus decision.

**Agent Votes:**
{votes_str}

**Final Result:**
- Verdict: {final_verdict}
- Score: {final_score}/100

**Task:**
Generate a brief summary (2-3 sentences) explaining how the agents reached this consensus.
Highlight any notable agreements or disagreements between agents."""


# =============================================================================
# MODULE INITIALIZATION
# =============================================================================

# Initialize Gemini client on module import
_client_initialized = init_gemini_client()

if _client_initialized:
    logger.info(f"SON LLM module ready with Gemini model: {GEMINI_MODEL}")
else:
    logger.info("SON LLM module loaded in rule-based mode (no LLM)")
