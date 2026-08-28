from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class BidRecommendation(str, Enum):
    PURSUE = "PURSUE"
    CONDITIONAL_PURSUE = "CONDITIONAL_PURSUE"
    HOLD = "HOLD"
    NO_BID = "NO_BID"


class BidReadiness(str, Enum):
    READY = "READY"
    CONDITIONAL = "CONDITIONAL"
    NOT_READY = "NOT_READY"


class BidIssueSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class BidIssueType(str, Enum):
    COMMERCIAL = "COMMERCIAL"
    FINANCIAL = "FINANCIAL"
    TECHNICAL = "TECHNICAL"
    DELIVERY = "DELIVERY"
    CONTRACTUAL = "CONTRACTUAL"
    OPERATIONS = "OPERATIONS"
    ESG = "ESG"
    CONSORTIUM = "CONSORTIUM"
    PROCUREMENT = "PROCUREMENT"


@dataclass(frozen=True)
class BidFactor:
    factor_id: str
    name: str
    category: str
    score: float
    weight: float
    rationale: str
    evidence_ids: list[str] = field(default_factory=list)

    @property
    def weighted_score(self) -> float:
        return self.score * self.weight


@dataclass(frozen=True)
class BidIssue:
    issue_id: str
    title: str
    description: str
    issue_type: BidIssueType
    severity: BidIssueSeverity
    blocking: bool
    estimated_exposure_usd: Optional[float] = None
    owner: Optional[str] = None
    resolution_required: Optional[str] = None
    evidence_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class BidStrength:
    strength_id: str
    title: str
    description: str
    score: float
    evidence_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class BidWorkstream:
    workstream_id: str
    name: str
    objective: str
    owner: str
    priority: str
    status: str
    dependencies: list[str] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class BidDecision:
    opportunity_id: str
    project_id: str
    recommendation: BidRecommendation
    readiness: BidReadiness
    readiness_score: float
    confidence: float

    executive_thesis: str
    decision_rationale: str

    factors: list[BidFactor] = field(default_factory=list)
    strengths: list[BidStrength] = field(default_factory=list)
    issues: list[BidIssue] = field(default_factory=list)
    workstreams: list[BidWorkstream] = field(default_factory=list)

    unresolved_blockers: list[str] = field(default_factory=list)
    clarification_ids: list[str] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)

    human_approval_required: bool = True
    approved: bool = False

    @property
    def blocking_issue_count(self) -> int:
        return sum(
            1
            for issue in self.issues
            if issue.blocking
        )

    @property
    def critical_issue_count(self) -> int:
        return sum(
            1
            for issue in self.issues
            if issue.severity == BidIssueSeverity.CRITICAL
        )

    @property
    def total_estimated_exposure_usd(self) -> float:
        return sum(
            issue.estimated_exposure_usd or 0.0
            for issue in self.issues
        )

    @property
    def can_auto_approve(self) -> bool:
        return False
