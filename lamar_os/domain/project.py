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

    BID_ISSUE = "BID_ISSUE"
    WORKSTREAM = "WORKSTREAM"
    CLARIFICATION = "CLARIFICATION"

    CONTRACT_TERM = "CONTRACT_TERM"
    CONTRACT_RISK = "CONTRACT_RISK"

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


class RecordStatus(str, Enum):
    """
    Lifecycle state of a Project Brain record.

    Approval status answers whether a human has authorized a
    consequential record.

    Record status answers whether the underlying issue, obligation,
    workstream, signal, or other item remains operationally active.
    """

    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    SUPERSEDED = "SUPERSEDED"
    CLOSED = "CLOSED"


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
    financial assumption, bid issue, workstream, milestone, project
    decision, construction signal, or operating signal.

    `payload` contains record-specific structured information while
    the common fields provide provenance, relationships, lifecycle
    state, and governance.
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
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None

    status: RecordStatus = RecordStatus.OPEN

    approval_status: ApprovalStatus = (
        ApprovalStatus.NOT_REQUIRED
    )

    evidence_ids: List[str] = field(
        default_factory=list,
    )

    related_record_ids: List[str] = field(
        default_factory=list,
    )

    parent_record_id: Optional[str] = None

    owner: Optional[str] = None
    priority: Optional[str] = None

    tags: List[str] = field(
        default_factory=list,
    )

    def touch(self) -> None:
        """Update the record modification timestamp."""

        self.updated_at = datetime.utcnow()

    def resolve(self) -> None:
        """Mark the record as operationally resolved."""

        self.status = RecordStatus.RESOLVED
        self.touch()

    def close(self) -> None:
        """Mark the record as closed."""

        self.status = RecordStatus.CLOSED
        self.touch()

    def supersede(self) -> None:
        """Mark the record as superseded by newer project state."""

        self.status = RecordStatus.SUPERSEDED
        self.touch()


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

    Records use stable identifiers. A specialist agent may therefore
    update an existing record rather than creating disconnected copies
    every time it runs.
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

    def _touch(self) -> None:
        """Update the Project Brain modification timestamp."""

        self.last_updated_at = datetime.utcnow()

    def add_record(
        self,
        record: ProjectRecord,
    ) -> None:
        """
        Add a new record belonging to this project.

        Duplicate record identifiers are rejected so agents cannot
        silently create conflicting project state.
        """

        if record.project_id != self.project_id:
            raise ValueError(
                "Project record belongs to a different project."
            )

        if self.record_by_id(record.record_id) is not None:
            raise ValueError(
                f"Project record already exists: "
                f"{record.record_id}"
            )

        now = datetime.utcnow()

        if record.created_at is None:
            record.created_at = now

        record.updated_at = now

        self.records.append(record)
        self._touch()

    def upsert_record(
        self,
        record: ProjectRecord,
    ) -> None:
        """
        Insert or replace a record using its stable record ID.

        This is the primary write primitive for agent-generated
        Project Brain state. Re-running an agent updates the same
        logical record instead of accumulating duplicate outputs.
        """

        if record.project_id != self.project_id:
            raise ValueError(
                "Project record belongs to a different project."
            )

        existing = self.record_by_id(
            record.record_id,
        )

        now = datetime.utcnow()

        if existing is None:
            if record.created_at is None:
                record.created_at = now

            record.updated_at = now

            self.records.append(record)
            self._touch()
            return

        if record.created_at is None:
            record.created_at = existing.created_at

        record.updated_at = now

        index = self.records.index(existing)
        self.records[index] = record

        self._touch()

    def add_decision(
        self,
        decision: ProjectDecision,
    ) -> None:
        """Record an authorized project decision."""

        if decision.project_id != self.project_id:
            raise ValueError(
                "Project decision belongs to a different project."
            )

        if self.decision_by_id(
            decision.decision_id
        ) is not None:
            raise ValueError(
                f"Project decision already exists: "
                f"{decision.decision_id}"
            )

        self.decisions.append(decision)
        self._touch()

    def add_milestone(
        self,
        milestone: ProjectMilestone,
    ) -> None:
        """Add a project lifecycle milestone."""

        if milestone.project_id != self.project_id:
            raise ValueError(
                "Project milestone belongs to a different project."
            )

        if self.milestone_by_id(
            milestone.milestone_id
        ) is not None:
            raise ValueError(
                f"Project milestone already exists: "
                f"{milestone.milestone_id}"
            )

        self.milestones.append(milestone)
        self._touch()

    def add_agent_run(
        self,
        run: AgentRun,
    ) -> None:
        """Store a traceable specialist-agent execution."""

        if run.project_id != self.project_id:
            raise ValueError(
                "Agent run belongs to a different project."
            )

        if self.agent_run_by_id(
            run.run_id
        ) is not None:
            raise ValueError(
                f"Agent run already exists: "
                f"{run.run_id}"
            )

        self.agent_runs.append(run)
        self._touch()

    def record_by_id(
        self,
        record_id: str,
    ) -> Optional[ProjectRecord]:
        """Return one Project Brain record by stable identifier."""

        for record in self.records:
            if record.record_id == record_id:
                return record

        return None

    def decision_by_id(
        self,
        decision_id: str,
    ) -> Optional[ProjectDecision]:
        """Return one human decision by identifier."""

        for decision in self.decisions:
            if decision.decision_id == decision_id:
                return decision

        return None

    def milestone_by_id(
        self,
        milestone_id: str,
    ) -> Optional[ProjectMilestone]:
        """Return one project milestone by identifier."""

        for milestone in self.milestones:
            if milestone.milestone_id == milestone_id:
                return milestone

        return None

    def agent_run_by_id(
        self,
        run_id: str,
    ) -> Optional[AgentRun]:
        """Return one specialist-agent execution by identifier."""

        for run in self.agent_runs:
            if run.run_id == run_id:
                return run

        return None

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

    def records_by_status(
        self,
        status: RecordStatus,
    ) -> List[ProjectRecord]:
        """Return records in a specific lifecycle state."""

        return [
            record
            for record in self.records
            if record.status == status
        ]

    def records_by_owner(
        self,
        owner: str,
    ) -> List[ProjectRecord]:
        """Return project records assigned to one owner."""

        return [
            record
            for record in self.records
            if record.owner == owner
        ]

    def records_with_tag(
        self,
        tag: str,
    ) -> List[ProjectRecord]:
        """Return records carrying a specific tag."""

        return [
            record
            for record in self.records
            if tag in record.tags
        ]

    def related_records(
        self,
        record_id: str,
    ) -> List[ProjectRecord]:
        """
        Return records explicitly related to a Project Brain record.

        Relationships may be declared from either side, allowing
        agents to traverse the shared state without requiring every
        producer to duplicate relationship metadata.
        """

        related: List[ProjectRecord] = []

        for record in self.records:
            if (
                record.record_id == record_id
                or record_id in record.related_record_ids
            ):
                continue

            source = self.record_by_id(
                record_id,
            )

            if source is None:
                return []

            if (
                record.record_id
                in source.related_record_ids
                or record_id
                in record.related_record_ids
                or record.parent_record_id == record_id
                or source.parent_record_id
                == record.record_id
            ):
                related.append(record)

        return related

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

    def open_records(
        self,
    ) -> List[ProjectRecord]:
        """Return unresolved operational project state."""

        return [
            record
            for record in self.records
            if record.status
            in {
                RecordStatus.OPEN,
                RecordStatus.IN_PROGRESS,
            }
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

    def evidence_ids(
        self,
    ) -> List[str]:
        """Return unique evidence IDs referenced by project state."""

        evidence = {
            evidence_id
            for record in self.records
            for evidence_id in record.evidence_ids
        }

        evidence.update(
            evidence_id
            for decision in self.decisions
            for evidence_id in decision.evidence_ids
        )

        evidence.update(
            evidence_id
            for run in self.agent_runs
            for evidence_id in run.evidence_ids
        )

        return sorted(evidence)

    def record_counts(
        self,
    ) -> Dict[str, int]:
        """Return Project Brain record counts grouped by type."""

        counts: Dict[str, int] = {}

        for record in self.records:
            key = record.record_type.value
            counts[key] = counts.get(key, 0) + 1

        return counts

    def status_counts(
        self,
    ) -> Dict[str, int]:
        """Return Project Brain record counts grouped by status."""

        counts: Dict[str, int] = {}

        for record in self.records:
            key = record.status.value
            counts[key] = counts.get(key, 0) + 1

        return counts

    def snapshot(
        self,
    ) -> Dict[str, Any]:
        """
        Return an inspectable summary of current shared project state.

        This is intentionally a deterministic state summary rather
        than an AI-generated executive narrative. Specialist agents,
        API routes, and the Deal Room can consume this snapshot
        without independently reconstructing the project.
        """

        return {
            "project_id": self.project_id,
            "record_count": len(self.records),
            "decision_count": len(self.decisions),
            "milestone_count": len(self.milestones),
            "agent_run_count": len(self.agent_runs),
            "pending_approval_count": len(
                self.pending_approvals()
            ),
            "open_record_count": len(
                self.open_records()
            ),
            "record_counts": self.record_counts(),
            "status_counts": self.status_counts(),
            "evidence_count": len(
                self.evidence_ids()
            ),
            "agents": sorted(
                {
                    run.agent_name
                    for run in self.agent_runs
                }
            ),
            "last_updated_at": (
                self.last_updated_at.isoformat()
                if self.last_updated_at
                else None
            ),
        }


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
