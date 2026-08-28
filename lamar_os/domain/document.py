"""
Document intelligence domain models for Lamar PPP OS.

The document layer converts large PPP tender and contract packages
into structured, evidence-backed records that specialist agents,
deterministic engines, and human decision-makers can use.

Core principle:

    Raw document
        -> section
        -> evidence
        -> structured extraction
        -> human review
        -> Project Brain

The system may interpret and structure source material, but it must
preserve provenance and must not silently convert model interpretation
into an approved contractual or investment decision.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional


class DocumentType(str, Enum):
    """Common document types found in PPP procurement packages."""

    TENDER = "TENDER"
    REQUEST_FOR_PROPOSAL = "REQUEST_FOR_PROPOSAL"
    REQUEST_FOR_QUALIFICATION = "REQUEST_FOR_QUALIFICATION"
    CONTRACT = "CONTRACT"
    CONCESSION_AGREEMENT = "CONCESSION_AGREEMENT"
    TECHNICAL_SCHEDULE = "TECHNICAL_SCHEDULE"
    COMMERCIAL_SCHEDULE = "COMMERCIAL_SCHEDULE"
    FINANCIAL_SCHEDULE = "FINANCIAL_SCHEDULE"
    LEGAL_SCHEDULE = "LEGAL_SCHEDULE"
    TECHNICAL_SPECIFICATION = "TECHNICAL_SPECIFICATION"
    ADDENDUM = "ADDENDUM"
    CLARIFICATION = "CLARIFICATION"
    OTHER = "OTHER"


class DocumentAnalysisStatus(str, Enum):
    """Lifecycle of a document-intelligence analysis."""

    NOT_STARTED = "NOT_STARTED"
    ANALYZING = "ANALYZING"
    COMPLETED = "COMPLETED"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"
    FAILED = "FAILED"


class RequirementCategory(str, Enum):
    """High-level categories for extracted bid requirements."""

    TECHNICAL = "TECHNICAL"
    COMMERCIAL = "COMMERCIAL"
    FINANCIAL = "FINANCIAL"
    LEGAL = "LEGAL"
    REGULATORY = "REGULATORY"
    ESG = "ESG"
    CONSORTIUM = "CONSORTIUM"
    SUBMISSION = "SUBMISSION"
    OPERATIONS = "OPERATIONS"
    OTHER = "OTHER"


class ObligationCategory(str, Enum):
    """High-level categories for contractual obligations."""

    DESIGN = "DESIGN"
    CONSTRUCTION = "CONSTRUCTION"
    FINANCING = "FINANCING"
    OPERATIONS = "OPERATIONS"
    MAINTENANCE = "MAINTENANCE"
    PERFORMANCE = "PERFORMANCE"
    REPORTING = "REPORTING"
    PAYMENT = "PAYMENT"
    INSURANCE = "INSURANCE"
    HANDOVER = "HANDOVER"
    COMPLIANCE = "COMPLIANCE"
    OTHER = "OTHER"


class ExtractedRiskCategory(str, Enum):
    """Risk themes discovered during document analysis."""

    CONSTRUCTION = "CONSTRUCTION"
    FINANCING = "FINANCING"
    DEMAND = "DEMAND"
    REVENUE = "REVENUE"
    OPERATIONS = "OPERATIONS"
    REGULATORY = "REGULATORY"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    COUNTERPARTY = "COUNTERPARTY"
    PERFORMANCE = "PERFORMANCE"
    PROCUREMENT = "PROCUREMENT"
    SCHEDULE = "SCHEDULE"
    CONTRACTUAL = "CONTRACTUAL"
    OTHER = "OTHER"


class ReviewStatus(str, Enum):
    """Human review state for an extracted intelligence object."""

    NOT_REQUIRED = "NOT_REQUIRED"
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"


@dataclass
class DocumentEvidence:
    """
    Precise provenance for an extracted statement.

    Evidence is intentionally first-class. Agents should not create
    important requirements, obligations, risks, or dates without
    preserving the source location that supports the extraction.
    """

    evidence_id: str
    document_id: str
    document_name: str
    page_number: Optional[int] = None
    clause_reference: Optional[str] = None
    section_title: Optional[str] = None
    source_text: Optional[str] = None
    confidence: float = 1.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "Document evidence confidence must be between 0 and 1."
            )


@dataclass
class DocumentSection:
    """A logical section of a procurement or project document."""

    section_id: str
    document_id: str
    title: str
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    clause_reference: Optional[str] = None
    text: Optional[str] = None
    evidence_ids: list[str] = field(default_factory=list)


@dataclass
class ProjectDocument:
    """
    A document available to the Project Brain.

    The demo may use synthetic documents, but the same model can later
    represent uploaded tender packages, contracts, schedules, reports,
    or other project evidence.
    """

    document_id: str
    project_id: str
    name: str
    document_type: DocumentType
    description: Optional[str] = None
    version: Optional[str] = None
    issued_by: Optional[str] = None
    issued_date: Optional[date] = None
    page_count: Optional[int] = None
    source_reference: Optional[str] = None
    sections: list[DocumentSection] = field(default_factory=list)
    is_synthetic: bool = False
    data_classification: str = "DEMO"


@dataclass
class ExtractedRequirement:
    """A bid requirement extracted from documentary evidence."""

    requirement_id: str
    project_id: str
    document_id: str
    title: str
    description: str
    category: RequirementCategory
    mandatory: bool = True
    responsible_party: Optional[str] = None
    due_date: Optional[date] = None
    evidence_ids: list[str] = field(default_factory=list)
    confidence: float = 1.0
    review_status: ReviewStatus = ReviewStatus.PENDING

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "Requirement confidence must be between 0 and 1."
            )


@dataclass
class ExtractedObligation:
    """A contractual or operational obligation found in a document."""

    obligation_id: str
    project_id: str
    document_id: str
    title: str
    description: str
    category: ObligationCategory
    obligated_party: Optional[str] = None
    beneficiary_party: Optional[str] = None
    trigger: Optional[str] = None
    deadline: Optional[date] = None
    financial_consequence_usd: Optional[float] = None
    consequence_description: Optional[str] = None
    evidence_ids: list[str] = field(default_factory=list)
    confidence: float = 1.0
    review_status: ReviewStatus = ReviewStatus.PENDING

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "Obligation confidence must be between 0 and 1."
            )


@dataclass
class ExtractedProjectDate:
    """A material date or deadline discovered in documentary evidence."""

    date_id: str
    project_id: str
    document_id: str
    title: str
    event_date: date
    description: Optional[str] = None
    critical: bool = False
    evidence_ids: list[str] = field(default_factory=list)
    confidence: float = 1.0
    review_status: ReviewStatus = ReviewStatus.PENDING

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "Project date confidence must be between 0 and 1."
            )


@dataclass
class ExtractedDocumentRisk:
    """
    A potential project risk surfaced from documentary evidence.

    This is intentionally separate from the canonical ProjectRisk model.
    A later translation step can convert reviewed document intelligence
    into the formal risk register.
    """

    risk_id: str
    project_id: str
    document_id: str
    title: str
    description: str
    category: ExtractedRiskCategory
    potential_impact: Optional[str] = None
    estimated_impact_usd: Optional[float] = None
    evidence_ids: list[str] = field(default_factory=list)
    confidence: float = 1.0
    review_status: ReviewStatus = ReviewStatus.PENDING

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "Document risk confidence must be between 0 and 1."
            )


@dataclass
class ClarificationQuestion:
    """
    A question the bid team may need to raise with the procuring authority.

    The agent may recommend a clarification, but humans determine whether
    it should actually be submitted.
    """

    clarification_id: str
    project_id: str
    title: str
    question: str
    rationale: str
    related_document_ids: list[str] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)
    priority: str = "MEDIUM"
    human_submission_required: bool = True
    review_status: ReviewStatus = ReviewStatus.PENDING


@dataclass
class DocumentAnalysis:
    """
    Structured output produced by document intelligence.

    This object is the handoff surface between the Document Agent and
    downstream systems such as the Bid Agent, Contract Agent, risk engine,
    Project Brain, and executive decision layer.
    """

    analysis_id: str
    project_id: str
    opportunity_id: Optional[str]
    status: DocumentAnalysisStatus
    document_ids: list[str] = field(default_factory=list)
    evidence: list[DocumentEvidence] = field(default_factory=list)
    requirements: list[ExtractedRequirement] = field(default_factory=list)
    obligations: list[ExtractedObligation] = field(default_factory=list)
    project_dates: list[ExtractedProjectDate] = field(default_factory=list)
    risks: list[ExtractedDocumentRisk] = field(default_factory=list)
    clarification_questions: list[ClarificationQuestion] = field(
        default_factory=list
    )
    executive_summary: Optional[str] = None
    analyzed_at: datetime = field(default_factory=datetime.utcnow)
    analyzed_by: str = "Document Agent"
    human_review_required: bool = True

    @property
    def requirement_count(self) -> int:
        return len(self.requirements)

    @property
    def obligation_count(self) -> int:
        return len(self.obligations)

    @property
    def risk_count(self) -> int:
        return len(self.risks)

    @property
    def clarification_count(self) -> int:
        return len(self.clarification_questions)

    @property
    def evidence_count(self) -> int:
        return len(self.evidence)

    def evidence_by_id(
        self,
        evidence_id: str,
    ) -> DocumentEvidence:
        """Return a specific evidence object or fail explicitly."""

        for item in self.evidence:
            if item.evidence_id == evidence_id:
                return item

        raise ValueError(
            f"Evidence '{evidence_id}' does not exist in analysis "
            f"'{self.analysis_id}'."
        )

    def pending_review_count(self) -> int:
        """Count extracted intelligence objects awaiting human review."""

        reviewable_items = [
            *self.requirements,
            *self.obligations,
            *self.project_dates,
            *self.risks,
            *self.clarification_questions,
        ]

        return sum(
            item.review_status == ReviewStatus.PENDING
            for item in reviewable_items
        )
