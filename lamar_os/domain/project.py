"""
Canonical PPP project and Project Brain models for Lamar PPP OS.

The Project Brain is the shared state layer for the PPP lifecycle.
Opportunity intelligence, agents, deterministic engines, project
execution systems, and executive workflows operate against this
canonical representation rather than maintaining disconnected state.

The model deliberately separates factual project state from AI
interpretation so that outputs remain traceable and consequential
changes can remain subject to human approval.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ProjectStage(str, Enum):
    """Lifecycle stages of a PPP infrastructure project."""

    DISCOVERY = "DISCOVERY"
    BID = "BID"
    STRUCTURING = "STRUCTURING"
    FINANCING = "FINANCING"
    CONSTRUCTION = "CONSTRUCTION"
    OPERATIONS = "OPERATIONS"
    TRANSFER = "TRANSFER"


class InfrastructureSector(str, Enum):
    """Infrastructure sectors supported by Lamar PPP OS."""

    WATER = "WATER"
    ENERGY = "ENERGY"
    SOCIAL_INFRASTRUCTURE = "SOCIAL_INFRASTRUCTURE"
    TRANSPORT = "TRANSPORT"
    OTHER = "OTHER"


class ProjectRecordType(str, Enum):
    """
    Types of structured information stored in the Project Brain.

    These records allow multiple modules and agents to operate over
    the same project context without each module creating its own
    disconnected representation.
    """

    OPPORTUNITY = "OPPORTUNITY"
    DOCUMENT = "DOCUMENT"
    REQUIREMENT = "REQUIREMENT"
    OBLIGATION = "OBLIGATION"
    RISK = "RISK"
    FINANCIAL_ASSUMPTION = "FINANCIAL_ASSUMPTION"
    MILESTONE = "MILESTONE"
    DECISION = "DECISION"
    CONSTRUCTION_SIGNAL = "CONSTRUCTION_SIGNAL"
    OPERATIONS_SIGNAL = "OPERATIONS_SIGNAL"
    MEMORY = "MEMORY"
    EVIDENCE = "EVIDENCE"


class RecordSource(str, Enum):
    """Origin of a Project Brain record."""

    HUMAN = "HUMAN"
    DOCUMENT = "DOCUMENT"
    AGENT = "AGENT"
    ENGINE = "ENGINE"
    SYSTEM = "SYSTEM"


class ApprovalStatus(str, Enum):
    """Human-governance state for consequential records."""

    NOT_REQUIRED = "NOT_REQUIRED"
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class AgentRunStatus(str, Enum):
    """Execution state for a specialist agent run."""

    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"


@dataclass
class ProjectParty:
    """An organisation participating in the PPP project."""

    name: str
    role: str
    country: Optional[str] = None


@dataclass
class ProjectRecord:
    """
    A traceable unit of structured project knowledge.

    Examples include a tender requirement, contractual obligation,
    financial assumption, milestone, project decision, or operating
    signal.

    `payload` contains record-specific structured information while
    the common fields provide provenance and governance.
    """

    record_id: str
    project_id: str
    record_type: ProjectRecordType
    title: str

    summary: Optional[str] = None
    source: RecordSource = RecordSource.SYSTEM
    source_reference: Optional[str] = None

    payload: Dict[str, Any] = field(
        default_factory=dict,
    )

    created_at: Optional[datetime] = None
    created_by: Optional[str] = None

    approval_status: ApprovalStatus = (
        ApprovalStatus.NOT_REQUIRED
    )

    evidence_ids: List[str] = field(
        default_factory=list,
    )

    tags: List[str] = field(
        default_factory=list,
    )


@dataclass
class ProjectDecision:
    """
    A human decision recorded against the project.

    Agents and engines may recommend actions, but consequential
    decisions are represented separately so the system never
    confuses machine recommendations with human authorization.
    """

    decision_id: str
    project_id: str
    title: str
    decision: str

    rationale: Optional[str] = None
    decided_by: Optional[str] = None
    decided_at: Optional[datetime] = None

    related_record_ids: List[str] = field(
        default_factory=list,
    )

    evidence_ids: List[str] = field(
        default_factory=list,
    )


@dataclass
class ProjectMilestone:
    """A lifecycle milestone tracked by the Project Brain."""

    milestone_id: str
    project_id: str
    name: str

    status: str = "PENDING"
    planned_date: Optional[str] = None
    actual_date: Optional[str] = None

    owner: Optional[str] = None

    related_record_ids: List[str] = field(
        default_factory=list,
    )


@dataclass
class AgentRun:
    """
    Traceable execution record for a specialist Lamar OS agent.

    This is intentionally explicit about input, tools, outputs,
    evidence, and human review so an executive can inspect how an
    agent reached its result.
    """

    run_id: str
    project_id: str
    agent_name: str
    task: str

    status: AgentRunStatus = (
        AgentRunStatus.QUEUED
    )

    input_record_ids: List[str] = field(
        default_factory=list,
    )

    tools_used: List[str] = field(
        default_factory=list,
    )

    output_record_ids: List[str] = field(
        default_factory=list,
    )

    evidence_ids: List[str] = field(
        default_factory=list,
    )

    summary: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    human_review_required: bool = True
    reviewed_by: Optional[str] = None


@dataclass
class ProjectBrain:
    """
    Shared project intelligence and memory layer.

    All Lamar PPP OS modules operate against this object.

    The Project Brain is not an autonomous decision-maker. It stores
    factual project state, traceable machine outputs, human decisions,
    lifecycle milestones, and agent activity so the complete project
    history can be inspected and reused.
    """

    project_id: str

    records: List[ProjectRecord] = field(
        default_factory=list,
    )

    decisions: List[ProjectDecision] = field(
        default_factory=list,
    )

    milestones: List[ProjectMilestone] = field(
        default_factory=list,
    )

    agent_runs: List[AgentRun] = field(
        default_factory=list,
    )

    last_updated_at: Optional[datetime] = None

    def add_record(
        self,
        record: ProjectRecord,
    ) -> None:
        """Add a record belonging to this project."""

        if record.project_id != self.project_id:
            raise ValueError(
                "Project record belongs to a different project."
            )

        self.records.append(record)
        self.last_updated_at = datetime.utcnow()

    def add_decision(
        self,
        decision: ProjectDecision,
    ) -> None:
        """Record an authorized project decision."""

        if decision.project_id != self.project_id:
            raise ValueError(
                "Project decision belongs to a different project."
            )

        self.decisions.append(decision)
        self.last_updated_at = datetime.utcnow()

    def add_milestone(
        self,
        milestone: ProjectMilestone,
    ) -> None:
        """Add a project lifecycle milestone."""

        if milestone.project_id != self.project_id:
            raise ValueError(
                "Project milestone belongs to a different project."
            )

        self.milestones.append(milestone)
        self.last_updated_at = datetime.utcnow()

    def add_agent_run(
        self,
        run: AgentRun,
    ) -> None:
        """Store a traceable specialist-agent execution."""

        if run.project_id != self.project_id:
            raise ValueError(
                "Agent run belongs to a different project."
            )

        self.agent_runs.append(run)
        self.last_updated_at = datetime.utcnow()

    def records_by_type(
        self,
        record_type: ProjectRecordType,
    ) -> List[ProjectRecord]:
        """Return project records of a specific type."""

        return [
            record
            for record in self.records
            if record.record_type == record_type
        ]

    def pending_approvals(
        self,
    ) -> List[ProjectRecord]:
        """Return records waiting for human approval."""

        return [
            record
            for record in self.records
            if record.approval_status
            == ApprovalStatus.PENDING
        ]

    def runs_by_agent(
        self,
        agent_name: str,
    ) -> List[AgentRun]:
        """Return execution history for one specialist agent."""

        return [
            run
            for run in self.agent_runs
            if run.agent_name == agent_name
        ]


@dataclass
class PPPProject:
    """
    Canonical representation of a PPP infrastructure project.

    `PPPProject` stores stable project identity and metadata.

    `brain` stores the evolving intelligence, evidence, agent
    activity, milestones, and human decisions accumulated throughout
    the PPP lifecycle.

    This separation allows Lamar OS to preserve factual project state
    while still supporting AI-native workflows.
    """

    project_id: str
    name: str
    country: str
    sector: InfrastructureSector
    stage: ProjectStage

    description: Optional[str] = None
    concession_years: Optional[int] = None
    estimated_capex_usd: Optional[float] = None

    parties: List[ProjectParty] = field(
        default_factory=list,
    )

    tags: List[str] = field(
        default_factory=list,
    )

    is_demo: bool = False
    data_classification: str = "PUBLIC"

    brain: Optional[ProjectBrain] = None

    def ensure_brain(self) -> ProjectBrain:
        """
        Return the project's Project Brain, creating it when needed.

        This keeps existing Phase 1 project construction compatible
        while allowing Phase 2 workflows to opt into shared state.
        """

        if self.brain is None:
            self.brain = ProjectBrain(
                project_id=self.project_id,
            )

        return self.brain
