"""
PPP opportunity intelligence models for Lamar PPP OS.

An opportunity represents a potential infrastructure project before
Lamar commits resources to a bid.

The model separates factual opportunity information from scored
strategic interpretation so every Bid / No-Bid recommendation can be
explained and inspected.
"""

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import List, Optional

from lamar_os.domain.project import InfrastructureSector


class OpportunityStatus(str, Enum):
    """Lifecycle state of a potential PPP opportunity."""

    DISCOVERED = "DISCOVERED"
    INVESTIGATING = "INVESTIGATING"
    QUALIFIED = "QUALIFIED"
    BID_REVIEW = "BID_REVIEW"
    PURSUING = "PURSUING"
    PASSED = "PASSED"


class ProcurementModel(str, Enum):
    """Common infrastructure procurement structures."""

    PPP = "PPP"
    BOOT = "BOOT"
    BOT = "BOT"
    DBFOM = "DBFOM"
    BOO = "BOO"
    EPC = "EPC"
    OTHER = "OTHER"


class OpportunityPriority(str, Enum):
    """Executive opportunity priority."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    STRATEGIC = "STRATEGIC"


@dataclass
class OpportunitySource:
    """
    Provenance for an opportunity.

    Phase 2 demo opportunities may use public or synthetic sources.
    Production systems could later connect procurement portals,
    government announcements, partner pipelines, and market feeds.
    """

    source_name: str
    source_type: str

    source_reference: Optional[str] = None
    discovered_at: Optional[date] = None

    is_public: bool = True
    is_synthetic: bool = False


@dataclass
class OpportunityScoreComponent:
    """
    One explainable component of an opportunity score.

    `score` is expressed from 0 to 100.

    `weight` is expressed from 0 to 1.

    The weighted contribution is calculated deterministically rather
    than delegated to an LLM.
    """

    name: str
    score: float
    weight: float
    rationale: str

    evidence: Optional[str] = None

    @property
    def weighted_score(self) -> float:
        """Return this component's weighted contribution."""

        return self.score * self.weight


@dataclass
class OpportunityAssessment:
    """
    Explainable strategic assessment of an opportunity.

    The assessment may contain machine-generated observations, but
    the final Bid / No-Bid decision remains a human decision.
    """

    opportunity_id: str

    strategic_fit: float
    sector_fit: float
    market_fit: float
    delivery_fit: float
    financing_fit: float
    consortium_readiness: float
    competitive_position: float

    overall_score: float

    priority: OpportunityPriority

    recommendation: str
    recommendation_reason: str

    strengths: List[str] = field(
        default_factory=list,
    )

    concerns: List[str] = field(
        default_factory=list,
    )

    components: List[OpportunityScoreComponent] = field(
        default_factory=list,
    )

    human_decision_required: bool = True


@dataclass
class PPPOpportunity:
    """
    Canonical representation of a potential PPP opportunity.

    This object is intentionally richer than a dashboard card. It
    contains the project facts required by Opportunity Radar and the
    Bid Agent while preserving source provenance and uncertainty.
    """

    opportunity_id: str
    name: str
    country: str
    sector: InfrastructureSector

    authority: str

    description: Optional[str] = None

    procurement_model: ProcurementModel = (
        ProcurementModel.PPP
    )

    status: OpportunityStatus = (
        OpportunityStatus.DISCOVERED
    )

    estimated_capex_usd: Optional[float] = None
    concession_years: Optional[int] = None

    submission_deadline: Optional[date] = None

    expected_revenue_model: Optional[str] = None
    project_location: Optional[str] = None

    strategic_theme: Optional[str] = None

    consortium_required: bool = True
    financing_required: bool = True

    sources: List[OpportunitySource] = field(
        default_factory=list,
    )

    known_requirements: List[str] = field(
        default_factory=list,
    )

    known_risks: List[str] = field(
        default_factory=list,
    )

    tags: List[str] = field(
        default_factory=list,
    )

    assessment: Optional[OpportunityAssessment] = None

    is_demo: bool = False
    data_classification: str = "PUBLIC"

    def days_to_deadline(
        self,
        today: date,
    ) -> Optional[int]:
        """Return calendar days remaining until submission."""

        if self.submission_deadline is None:
            return None

        return (
            self.submission_deadline - today
        ).days

    def attach_assessment(
        self,
        assessment: OpportunityAssessment,
    ) -> None:
        """
        Attach an assessment to this opportunity.

        Reject assessments belonging to another opportunity so
        downstream Bid Agent workflows cannot accidentally mix
        project contexts.
        """

        if (
            assessment.opportunity_id
            != self.opportunity_id
        ):
            raise ValueError(
                "Opportunity assessment belongs to "
                "a different opportunity."
            )

        self.assessment = assessment
