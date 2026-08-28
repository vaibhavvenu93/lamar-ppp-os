"""
API response contract for Lamar PPP OS Document Intelligence.

The API exposes evidence-backed output from the Document Agent without
requiring the frontend to understand internal domain dataclasses.

Consequential conclusions remain subject to human review.
"""

from datetime import date, datetime

from pydantic import BaseModel

from lamar_os.domain.document import DocumentAnalysis
from lamar_os.domain.project import AgentRun


class DocumentPackageSummaryResponse(BaseModel):
    project_id: str
    opportunity_id: str | None
    analysis_id: str
    status: str

    document_count: int
    evidence_count: int
    requirement_count: int
    obligation_count: int
    risk_count: int
    clarification_count: int
    pending_review_count: int

    executive_summary: str | None
    human_review_required: bool


class DocumentEvidenceResponse(BaseModel):
    evidence_id: str
    document_id: str
    document_name: str
    page_number: int | None
    clause_reference: str | None
    section_title: str | None
    source_text: str | None
    confidence: float


class RequirementResponse(BaseModel):
    requirement_id: str
    title: str
    description: str
    category: str
    mandatory: bool
    responsible_party: str | None
    due_date: date | None
    evidence_ids: list[str]
    confidence: float
    review_status: str


class ObligationResponse(BaseModel):
    obligation_id: str
    title: str
    description: str
    category: str
    obligated_party: str | None
    beneficiary_party: str | None
    trigger: str | None
    deadline: date | None
    financial_consequence_usd: float | None
    consequence_description: str | None
    evidence_ids: list[str]
    confidence: float
    review_status: str


class ProjectDateResponse(BaseModel):
    date_id: str
    title: str
    event_date: date
    description: str | None
    critical: bool
    evidence_ids: list[str]
    confidence: float
    review_status: str


class DocumentRiskResponse(BaseModel):
    risk_id: str
    title: str
    description: str
    category: str
    potential_impact: str | None
    estimated_impact_usd: float | None
    evidence_ids: list[str]
    confidence: float
    review_status: str


class ClarificationResponse(BaseModel):
    clarification_id: str
    title: str
    question: str
    rationale: str
    related_document_ids: list[str]
    evidence_ids: list[str]
    priority: str
    human_submission_required: bool
    review_status: str


class AgentRunResponse(BaseModel):
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


class DocumentIntelligenceResponse(BaseModel):
    summary: DocumentPackageSummaryResponse
    requirements: list[RequirementResponse]
    obligations: list[ObligationResponse]
    project_dates: list[ProjectDateResponse]
    risks: list[DocumentRiskResponse]
    clarifications: list[ClarificationResponse]
    evidence: list[DocumentEvidenceResponse]
    agent_run: AgentRunResponse

    data_notice: str
    governance_notice: str


def document_intelligence_response(
    analysis: DocumentAnalysis,
    agent_run: AgentRun,
) -> DocumentIntelligenceResponse:
    """Convert domain output into the frontend API contract."""

    return DocumentIntelligenceResponse(
        summary=DocumentPackageSummaryResponse(
            project_id=analysis.project_id,
            opportunity_id=analysis.opportunity_id,
            analysis_id=analysis.analysis_id,
            status=analysis.status.value,
            document_count=len(analysis.document_ids),
            evidence_count=analysis.evidence_count,
            requirement_count=analysis.requirement_count,
            obligation_count=analysis.obligation_count,
            risk_count=analysis.risk_count,
            clarification_count=analysis.clarification_count,
            pending_review_count=analysis.pending_review_count(),
            executive_summary=analysis.executive_summary,
            human_review_required=analysis.human_review_required,
        ),
        requirements=[
            RequirementResponse(
                requirement_id=item.requirement_id,
                title=item.title,
                description=item.description,
                category=item.category.value,
                mandatory=item.mandatory,
                responsible_party=item.responsible_party,
                due_date=item.due_date,
                evidence_ids=item.evidence_ids,
                confidence=item.confidence,
                review_status=item.review_status.value,
            )
            for item in analysis.requirements
        ],
        obligations=[
            ObligationResponse(
                obligation_id=item.obligation_id,
                title=item.title,
                description=item.description,
                category=item.category.value,
                obligated_party=item.obligated_party,
                beneficiary_party=item.beneficiary_party,
                trigger=item.trigger,
                deadline=item.deadline,
                financial_consequence_usd=(
                    item.financial_consequence_usd
                ),
                consequence_description=(
                    item.consequence_description
                ),
                evidence_ids=item.evidence_ids,
                confidence=item.confidence,
                review_status=item.review_status.value,
            )
            for item in analysis.obligations
        ],
        project_dates=[
            ProjectDateResponse(
                date_id=item.date_id,
                title=item.title,
                event_date=item.event_date,
                description=item.description,
                critical=item.critical,
                evidence_ids=item.evidence_ids,
                confidence=item.confidence,
                review_status=item.review_status.value,
            )
            for item in analysis.project_dates
        ],
        risks=[
            DocumentRiskResponse(
                risk_id=item.risk_id,
                title=item.title,
                description=item.description,
                category=item.category.value,
                potential_impact=item.potential_impact,
                estimated_impact_usd=item.estimated_impact_usd,
                evidence_ids=item.evidence_ids,
                confidence=item.confidence,
                review_status=item.review_status.value,
            )
            for item in analysis.risks
        ],
        clarifications=[
            ClarificationResponse(
                clarification_id=item.clarification_id,
                title=item.title,
                question=item.question,
                rationale=item.rationale,
                related_document_ids=item.related_document_ids,
                evidence_ids=item.evidence_ids,
                priority=item.priority,
                human_submission_required=(
                    item.human_submission_required
                ),
                review_status=item.review_status.value,
            )
            for item in analysis.clarification_questions
        ],
        evidence=[
            DocumentEvidenceResponse(
                evidence_id=item.evidence_id,
                document_id=item.document_id,
                document_name=item.document_name,
                page_number=item.page_number,
                clause_reference=item.clause_reference,
                section_title=item.section_title,
                source_text=item.source_text,
                confidence=item.confidence,
            )
            for item in analysis.evidence
        ],
        agent_run=AgentRunResponse(
            run_id=agent_run.run_id,
            project_id=agent_run.project_id,
            agent_name=agent_run.agent_name,
            task=agent_run.task,
            status=agent_run.status.value,
            input_record_ids=agent_run.input_record_ids,
            tools_used=agent_run.tools_used,
            output_record_ids=agent_run.output_record_ids,
            evidence_ids=agent_run.evidence_ids,
            summary=agent_run.summary,
            started_at=agent_run.started_at,
            completed_at=agent_run.completed_at,
            human_review_required=agent_run.human_review_required,
            reviewed_by=agent_run.reviewed_by,
        ),
        data_notice=(
            "DEMO ENVIRONMENT — PUBLIC INFORMATION + SYNTHETIC "
            "PROJECT DATA. NOT LAMAR INTERNAL DATA."
        ),
        governance_notice=(
            "The Document Agent structures and traces procurement "
            "intelligence. Extracted requirements, obligations, risks "
            "and clarification questions remain subject to human review."
        ),
    )
