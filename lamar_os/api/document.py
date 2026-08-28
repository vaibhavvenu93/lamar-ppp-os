"""
API response contract for Lamar PPP OS Project Brain.

The Project Brain API exposes shared, traceable project state without
requiring the frontend to understand internal domain dataclasses.

It is designed to power the Deal Room and later specialist-agent
workflows across bid, contract, finance, construction and operations.

Machine recommendations remain distinct from authorized human
decisions.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from lamar_os.domain.project import (
    AgentRun,
    ProjectBrain,
    ProjectDecision,
    ProjectMilestone,
    ProjectRecord,
)


class ProjectBrainRecordResponse(BaseModel):
    record_id: str
    project_id: str
    record_type: str
    title: str

    summary: str | None
    source: str
    source_reference: str | None

    payload: dict[str, Any]

    created_at: datetime | None
    updated_at: datetime | None
    created_by: str | None

    status: str
    approval_status: str

    evidence_ids: list[str]
    related_record_ids: list[str]
    parent_record_id: str | None

    owner: str | None
    priority: str | None

    tags: list[str]


class ProjectBrainDecisionResponse(BaseModel):
    decision_id: str
    project_id: str
    title: str
    decision: str

    rationale: str | None
    decided_by: str | None
    decided_at: datetime | None

    related_record_ids: list[str]
    evidence_ids: list[str]


class ProjectBrainMilestoneResponse(BaseModel):
    milestone_id: str
    project_id: str
    name: str

    status: str
    planned_date: str | None
    actual_date: str | None
    owner: str | None

    related_record_ids: list[str]


class ProjectBrainAgentRunResponse(BaseModel):
    run_id: str
    project_id: str
    agent_name: str
    task: str

    status: str

    input_record_ids: list[str]
    tools_used: list[str]
    output_record_ids: list[str]
    evidence_ids: list[str]

    summary: str | None

    started_at: datetime | None
    completed_at: datetime | None

    human_review_required: bool
    reviewed_by: str | None


class ProjectBrainSnapshotResponse(BaseModel):
    project_id: str

    record_count: int
    decision_count: int
    milestone_count: int
    agent_run_count: int

    pending_approval_count: int
    open_record_count: int

    record_counts: dict[str, int]
    status_counts: dict[str, int]

    evidence_count: int
    agents: list[str]

    last_updated_at: str | None


class ProjectBrainRelationshipResponse(BaseModel):
    """
    One inspectable relationship between two Project Brain records.

    This allows the Deal Room to show why a bid issue, workstream,
    contract term, financial assumption or risk exists rather than
    presenting intelligence as disconnected cards.
    """

    source_record_id: str
    target_record_id: str
    relationship: str


class ProjectBrainResponse(BaseModel):
    """
    Frontend-safe representation of shared project intelligence.
    """

    project_id: str

    snapshot: ProjectBrainSnapshotResponse

    records: list[ProjectBrainRecordResponse]
    decisions: list[ProjectBrainDecisionResponse]
    milestones: list[ProjectBrainMilestoneResponse]
    agent_runs: list[ProjectBrainAgentRunResponse]

    relationships: list[
        ProjectBrainRelationshipResponse
    ]

    pending_approval_ids: list[str]
    open_record_ids: list[str]

    data_notice: str
    governance_notice: str


def _record_response(
    record: ProjectRecord,
) -> ProjectBrainRecordResponse:
    """Convert one Project Brain record to its API contract."""

    return ProjectBrainRecordResponse(
        record_id=record.record_id,
        project_id=record.project_id,
        record_type=record.record_type.value,
        title=record.title,
        summary=record.summary,
        source=record.source.value,
        source_reference=record.source_reference,
        payload=record.payload,
        created_at=record.created_at,
        updated_at=record.updated_at,
        created_by=record.created_by,
        status=record.status.value,
        approval_status=record.approval_status.value,
        evidence_ids=record.evidence_ids,
        related_record_ids=record.related_record_ids,
        parent_record_id=record.parent_record_id,
        owner=record.owner,
        priority=record.priority,
        tags=record.tags,
    )


def _decision_response(
    decision: ProjectDecision,
) -> ProjectBrainDecisionResponse:
    """Convert one authorized human decision."""

    return ProjectBrainDecisionResponse(
        decision_id=decision.decision_id,
        project_id=decision.project_id,
        title=decision.title,
        decision=decision.decision,
        rationale=decision.rationale,
        decided_by=decision.decided_by,
        decided_at=decision.decided_at,
        related_record_ids=decision.related_record_ids,
        evidence_ids=decision.evidence_ids,
    )


def _milestone_response(
    milestone: ProjectMilestone,
) -> ProjectBrainMilestoneResponse:
    """Convert one lifecycle milestone."""

    return ProjectBrainMilestoneResponse(
        milestone_id=milestone.milestone_id,
        project_id=milestone.project_id,
        name=milestone.name,
        status=milestone.status,
        planned_date=milestone.planned_date,
        actual_date=milestone.actual_date,
        owner=milestone.owner,
        related_record_ids=milestone.related_record_ids,
    )


def _agent_run_response(
    run: AgentRun,
) -> ProjectBrainAgentRunResponse:
    """Convert one specialist-agent execution."""

    return ProjectBrainAgentRunResponse(
        run_id=run.run_id,
        project_id=run.project_id,
        agent_name=run.agent_name,
        task=run.task,
        status=run.status.value,
        input_record_ids=run.input_record_ids,
        tools_used=run.tools_used,
        output_record_ids=run.output_record_ids,
        evidence_ids=run.evidence_ids,
        summary=run.summary,
        started_at=run.started_at,
        completed_at=run.completed_at,
        human_review_required=run.human_review_required,
        reviewed_by=run.reviewed_by,
    )


def _relationships(
    brain: ProjectBrain,
) -> list[ProjectBrainRelationshipResponse]:
    """
    Build deterministic record-to-record relationships.

    Only relationships where both endpoints are Project Brain records
    are emitted. Evidence references that have not themselves been
    stored as ProjectRecord objects remain available through each
    record's evidence_ids.
    """

    record_ids = {
        record.record_id
        for record in brain.records
    }

    relationships: list[
        ProjectBrainRelationshipResponse
    ] = []

    seen: set[
        tuple[str, str, str]
    ] = set()

    for record in brain.records:
        for related_id in record.related_record_ids:
            if related_id not in record_ids:
                continue

            key = (
                record.record_id,
                related_id,
                "RELATED_TO",
            )

            if key in seen:
                continue

            seen.add(key)

            relationships.append(
                ProjectBrainRelationshipResponse(
                    source_record_id=record.record_id,
                    target_record_id=related_id,
                    relationship="RELATED_TO",
                )
            )

        if (
            record.parent_record_id is not None
            and record.parent_record_id in record_ids
        ):
            key = (
                record.record_id,
                record.parent_record_id,
                "CHILD_OF",
            )

            if key not in seen:
                seen.add(key)

                relationships.append(
                    ProjectBrainRelationshipResponse(
                        source_record_id=record.record_id,
                        target_record_id=(
                            record.parent_record_id
                        ),
                        relationship="CHILD_OF",
                    )
                )

    relationships.sort(
        key=lambda relationship: (
            relationship.source_record_id,
            relationship.target_record_id,
            relationship.relationship,
        )
    )

    return relationships


def project_brain_response(
    brain: ProjectBrain,
) -> ProjectBrainResponse:
    """
    Convert shared project state into the Deal Room API contract.

    This function does not generate new intelligence. It exposes the
    current deterministic Project Brain state in an inspectable form.
    """

    snapshot = brain.snapshot()

    return ProjectBrainResponse(
        project_id=brain.project_id,
        snapshot=ProjectBrainSnapshotResponse(
            project_id=snapshot["project_id"],
            record_count=snapshot["record_count"],
            decision_count=snapshot["decision_count"],
            milestone_count=snapshot["milestone_count"],
            agent_run_count=snapshot["agent_run_count"],
            pending_approval_count=(
                snapshot["pending_approval_count"]
            ),
            open_record_count=(
                snapshot["open_record_count"]
            ),
            record_counts=snapshot["record_counts"],
            status_counts=snapshot["status_counts"],
            evidence_count=snapshot["evidence_count"],
            agents=snapshot["agents"],
            last_updated_at=snapshot["last_updated_at"],
        ),
        records=[
            _record_response(record)
            for record in brain.records
        ],
        decisions=[
            _decision_response(decision)
            for decision in brain.decisions
        ],
        milestones=[
            _milestone_response(milestone)
            for milestone in brain.milestones
        ],
        agent_runs=[
            _agent_run_response(run)
            for run in brain.agent_runs
        ],
        relationships=_relationships(brain),
        pending_approval_ids=[
            record.record_id
            for record in brain.pending_approvals()
        ],
        open_record_ids=[
            record.record_id
            for record in brain.open_records()
        ],
        data_notice=(
            "DEMO ENVIRONMENT — PUBLIC INFORMATION + SYNTHETIC "
            "PROJECT DATA. NOT LAMAR INTERNAL DATA."
        ),
        governance_notice=(
            "The Project Brain stores traceable project state and "
            "machine recommendations. Agent-generated records do not "
            "constitute human approval of Bid / No-Bid, contractual, "
            "investment, financing, engineering or operating decisions."
        ),
    )
