"""
PPP risk models for Lamar PPP OS.

This module represents project risks, their allocation,
financial exposure, supporting evidence, and mitigation actions.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from .contract import Evidence


class RiskCategory(str, Enum):
    """Common risk categories across PPP infrastructure projects."""

    CONSTRUCTION = "CONSTRUCTION"
    FINANCING = "FINANCING"
    DEMAND = "DEMAND"
    REVENUE = "REVENUE"
    OPERATIONS = "OPERATIONS"
    REGULATORY = "REGULATORY"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    COUNTERPARTY = "COUNTERPARTY"
    FORCE_MAJEURE = "FORCE_MAJEURE"
    OTHER = "OTHER"


class RiskAllocation(str, Enum):
    """Party primarily responsible for bearing a project risk."""

    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    SHARED = "SHARED"
    UNALLOCATED = "UNALLOCATED"


class RiskSeverity(str, Enum):
    """Executive severity assigned to a project risk."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class ProjectRisk:
    """
    Structured representation of a PPP project risk.

    Financial calculations are stored separately from AI reasoning.
    Evidence links the identified risk back to its source material.
    """

    risk_id: str
    project_id: str
    title: str
    description: str

    category: RiskCategory
    allocation: RiskAllocation
    severity: RiskSeverity

    probability: Optional[float] = None
    estimated_impact_usd: Optional[float] = None
    estimated_irr_impact_pct: Optional[float] = None

    owner: Optional[str] = None
    mitigation: Optional[str] = None

    evidence: List[Evidence] = field(default_factory=list)

    requires_executive_attention: bool = False
