"""
Observable Document Agent workflow for Lamar PPP OS.

This layer connects the deterministic Document Agent to the persistent
Project Brain and records how the analysis was produced.

The workflow intentionally distinguishes:

    agent orchestration
    deterministic extraction
    evidence provenance
    persistent project records
    human approval

This gives the product an inspectable agent execution history instead
of presenting AI output as an unexplained answer.
"""

from datetime import datetime

from demo.tender_package import (
    PROJECT_ID,
    build_demo_tender_package,
)
from lamar_os.agents.document_agent import analyze_tender_package
from lamar_os.domain.document import DocumentAnalysis
from lamar_os.domain.project import (
    AgentRun,
    AgentRunStatus,
    ApprovalStatus,
    ProjectBrain,
    ProjectRecord,
    ProjectRecordType,
    RecordSource,
)


DOCUMENT_AGENT_TOOLS = [
    "tender_package_loader",
    "section_retrieval",
    "evidence_extraction",
    "requirement_extraction",
    "obligation_extraction",
    "critical_date_extraction",
    "risk_extraction",
    "clarification_generation",
]


def _document_record_ids(
    analysis: DocumentAnalysis,
) -> list[str]:
    return [
        f"RECORD-{document_id}"
        for document_id in analysis.document_ids
    ]


def _analysis_record_id(
    analysis: DocumentAnalysis,
) -> str:
    return f"RECORD-{analysis.analysis_id}"


def _build_document_records(
    analysis: DocumentAnalysis,
) -> list[ProjectRecord]:
    """
    Represent source documents inside the Project Brain.

    These records create the persistent link between the agent run and
    the procurement material it analyzed.
    """

    documents = build_demo_tender_package()

    return [
        ProjectRecord(
            record_id=f"RECORD-{document.document_id}",
            project_id=PROJECT_ID,
            record_type=ProjectRecordType.DOCUMENT,
            title=document.name,
            summary=(
                document.description
                or "PPP procurement document."
            ),
            source=RecordSource.DOCUMENT,
            source_reference=document.source_reference,
            payload={
                "document_id": document.document_id,
                "document_type": document.document_type.value,
                "version": document.version,
                "issued_by": document.issued_by,
                "issued_date": (
                    document.issued_date.isoformat()
                    if document.issued_date
                    else None
                ),
                "page_count": document.page_count,
                "section_count": len(document.sections),
                "is_synthetic": document.is_synthetic,
                "data_classification": (
                    document.data_classification
                ),
            },
            created_by="Document Agent",
            approval_status=ApprovalStatus.NOT_REQUIRED,
            tags=[
                "document",
                "synthetic-demo",
                "tender-package",
            ],
        )
        for document in documents
    ]


def _build_analysis_record(
    analysis: DocumentAnalysis,
) -> ProjectRecord:
    """Create the persistent Project Brain record for the analysis."""

    return ProjectRecord(
        record_id=_analysis_record_id(analysis),
        project_id=analysis.project_id,
        record_type=ProjectRecordType.DOCUMENT,
        title="Tender Package Intelligence",
        summary=(
            analysis.executive_summary
            or "Document Agent tender analysis."
        ),
        source=RecordSource.AGENT,
        source_reference=analysis.analysis_id,
        payload={
            "analysis_id": analysis.analysis_id,
            "opportunity_id": analysis.opportunity_id,
            "status": analysis.status.value,
            "document_count": len(analysis.document_ids),
            "evidence_count": analysis.evidence_count,
            "requirement_count": analysis.requirement_count,
            "obligation_count": analysis.obligation_count,
            "risk_count": analysis.risk_count,
            "clarification_count": analysis.clarification_count,
            "pending_review_count": (
                analysis.pending_review_count()
            ),
            "human_review_required": (
                analysis.human_review_required
            ),
        },
        created_by="Document Agent",
        approval_status=ApprovalStatus.PENDING,
        evidence_ids=[
            item.evidence_id
            for item in analysis.evidence
        ],
        tags=[
            "document-intelligence",
            "agent-output",
            "requires-review",
        ],
    )


def _build_agent_run(
    analysis: DocumentAnalysis,
    started_at: datetime,
    completed_at: datetime,
) -> AgentRun:
    """Build the inspectable execution trace for the Document Agent."""

    return AgentRun(
        run_id="RUN-DOCUMENT-WATER-001",
        project_id=analysis.project_id,
        agent_name="Document Agent",
        task=(
            "Analyze the synthetic PPP tender package and convert "
            "decision-relevant clauses into structured, evidence-backed "
            "project intelligence."
        ),
        status=AgentRunStatus.REQUIRES_REVIEW,
        input_record_ids=_document_record_ids(analysis),
        tools_used=DOCUMENT_AGENT_TOOLS,
        output_record_ids=[
            _analysis_record_id(analysis),
        ],
        evidence_ids=[
            item.evidence_id
            for item in analysis.evidence
        ],
        summary=(
            f"Analyzed {len(analysis.document_ids)} documents and "
            f"produced {analysis.requirement_count} requirements, "
            f"{analysis.obligation_count} obligations, "
            f"{analysis.risk_count} risks and "
            f"{analysis.clarification_count} clarification questions. "
            f"{analysis.pending_review_count()} extracted items remain "
            "subject to human review."
        ),
        started_at=started_at,
        completed_at=completed_at,
        human_review_required=True,
    )


def run_document_workflow(
    brain: ProjectBrain | None = None,
) -> tuple[DocumentAnalysis, ProjectBrain, AgentRun]:
    """
    Execute the prototype Document Agent workflow.

    Returns:
        DocumentAnalysis:
            Structured evidence-backed intelligence.

        ProjectBrain:
            Persistent project state containing source records,
            analysis output and agent execution history.

        AgentRun:
            Inspectable execution trace for this workflow.
    """

    project_brain = brain or ProjectBrain(
        project_id=PROJECT_ID,
    )

    if project_brain.project_id != PROJECT_ID:
        raise ValueError(
            "Document workflow Project Brain does not match "
            f"demo project '{PROJECT_ID}'."
        )

    started_at = datetime.utcnow()

    analysis = analyze_tender_package()

    document_records = _build_document_records(analysis)

    existing_record_ids = {
        record.record_id
        for record in project_brain.records
    }

    for record in document_records:
        if record.record_id not in existing_record_ids:
            project_brain.add_record(record)
            existing_record_ids.add(record.record_id)

    analysis_record = _build_analysis_record(analysis)

    if analysis_record.record_id not in existing_record_ids:
        project_brain.add_record(analysis_record)

    completed_at = datetime.utcnow()

    agent_run = _build_agent_run(
        analysis=analysis,
        started_at=started_at,
        completed_at=completed_at,
    )

    existing_run_ids = {
        run.run_id
        for run in project_brain.agent_runs
    }

    if agent_run.run_id not in existing_run_ids:
        project_brain.add_agent_run(agent_run)

    return analysis, project_brain, agent_run
