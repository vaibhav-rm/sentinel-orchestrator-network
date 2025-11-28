"""
=============================================================================
Sentinel Orchestrator Network (SON) - Agents Package
=============================================================================

FINAL AGENTIC ARCHITECTURE (5-AGENT VERSION)
CrewAI + Masumi Node + Kodosumi Runtime + Hydra + Cardano L1

This package contains all 5 AI agent modules that form the SON multi-agent
swarm. Each agent is orchestrated by CrewAI and runs inside the Kodosumi
Runtime environment.

Workflow Order:
    Sentinel Agent → Oracle Agent → Compliance Agent → ZK-Prover Agent → Consensus Agent

Agents:
    - sentinel.py   : Agent A - Primary detector & analyzer (expert_detector)
    - oracle.py     : Agent B - External data & liquidity verifier (external_data_verifier)
    - compliance.py : Agent C - Regulatory risk assessment (compliance_checker)
    - zk_prover.py  : Agent D - Privacy-preserving proof generation (privacy_guardian)
    - consensus.py  : Agent E - Final arbiter & capsule writer (consensus_mediator)

Integration Points:
    - CrewAI: Internal multi-agent orchestration and task sequencing
    - Masumi: Agent registry, pricing, micropayments, reputation
    - Kodosumi Runtime: Containerized execution sandbox
    - Hydra: L2 consensus (ZK-Prover + Consensus agents only)
    - Cardano L1: ThreatProof Capsule storage

Owner: Member 2 (The Brain)

=============================================================================
"""

# Agent imports for CrewAI crew definition
# from .sentinel import SentinelAgent
# from .oracle import OracleAgent
# from .compliance import ComplianceAgent
# from .zk_prover import ZKProverAgent
# from .consensus import ConsensusAgent
# from .crew import SONThreatDetectionCrew
