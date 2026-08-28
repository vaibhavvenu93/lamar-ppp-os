from demo.tender_package import (
    PROJECT_ID,
    build_demo_tender_package,
    tender_package_page_count,
    tender_package_section_count,
)
from lamar_os.agents.document_agent import analyze_tender_package
from lamar_os.agents.document_workflow import run_document_workflow
from lamar_os.domain.document import (
    DocumentAnalysisStatus,
    ReviewStatus,
)
from lamar_os.domain.project import (
    AgentRunStatus,
    ApprovalStatus,
    ProjectRecordType,
    RecordSource,
)


def test_demo_tender_package_has_expected_shape():
    documents = build_demo_tender_package()

    assert len(documents) == 7
    assert tender_package_page_count(documents) == 486
    assert tender_package_section_count(documents) == 22

    assert all(
        document.project_id == PROJECT_ID
        for document in documents
    )

    assert all(
        document.is_synthetic
        for document in documents
    )


def test_document_agent_produces_structured_analysis():
    analysis = analyze_tender_package()

    assert analysis.project_id == PROJECT_ID
    assert analysis.status == DocumentAnalysisStatus.REQUIRES_REVIEW

    assert len(analysis.document_ids) == 7
    assert analysis.evidence_count == 22
    assert analysis.requirement_count == 13
    assert analysis.obligation_count == 5
    assert analysis.risk_count == 6
    assert analysis.clarification_count == 4

    assert analysis.human_review_required is True


def test_every_material_extraction_has_evidence():
    analysis = analyze_tender_package()

    evidence_ids = {
        evidence.evidence_id
        for evidence in analysis.evidence
    }

    extracted_items = [
        *analysis.requirements,
        *analysis.obligations,
        *analysis.project_dates,
        *analysis.risks,
        *analysis.clarification_questions,
    ]

    assert extracted_items

    for item in extracted_items:
        assert item.evidence_ids

        for evidence_id in item.evidence_ids:
            assert evidence_id in evidence_ids


def test_evidence_preserves_source_trace():
    analysis = analyze_tender_package()

    evidence = analysis.evidence_by_id("EV-015")

    assert evidence.document_id == "DOC-WATER-IMPL-004"
    assert evidence.document_name == "Draft Implementation Agreement"
    assert evidence.page_number == 34
    assert evidence.clause_reference == "7.4"
    assert evidence.source_text is not None
    assert "150,000" in evidence.source_text
    assert evidence.confidence == 0.99


def test_delay_risk_is_linked_to_financial_exposure():
    analysis = analyze_tender_package()

    delay_risk = next(
        risk
        for risk in analysis.risks
        if risk.risk_id == "DOC-RISK-004"
    )

    assert delay_risk.estimated_impact_usd == 25_000_000
    assert "EV-014" in delay_risk.evidence_ids
    assert "EV-015" in delay_risk.evidence_ids


def test_extracted_items_default_to_human_review():
    analysis = analyze_tender_package()

    reviewable_items = [
        *analysis.requirements,
        *analysis.obligations,
        *analysis.project_dates,
        *analysis.risks,
        *analysis.clarification_questions,
    ]

    assert all(
        item.review_status == ReviewStatus.PENDING
        for item in reviewable_items
    )

    assert analysis.pending_review_count() == len(reviewable_items)


def test_document_workflow_persists_source_documents():
    analysis, brain, _ = run_document_workflow()

    document_records = [
        record
        for record in brain.records
        if (
            record.record_type == ProjectRecordType.DOCUMENT
            and record.source == RecordSource.DOCUMENT
        )
    ]

    assert len(document_records) == 7

    persisted_document_ids = {
        record.payload["document_id"]
        for record in document_records
    }

    assert persisted_document_ids == set(analysis.document_ids)


def test_document_workflow_persists_analysis_output():
    analysis, brain, _ = run_document_workflow()

    analysis_record = next(
        record
        for record in brain.records
        if record.source_reference == analysis.analysis_id
    )

    assert analysis_record.source == RecordSource.AGENT
    assert analysis_record.approval_status == ApprovalStatus.PENDING

    assert (
        analysis_record.payload["requirement_count"]
        == analysis.requirement_count
    )

    assert (
        analysis_record.payload["risk_count"]
        == analysis.risk_count
    )

    assert (
        analysis_record.payload["human_review_required"]
        is True
    )


def test_document_workflow_records_agent_execution():
    analysis, brain, agent_run = run_document_workflow()

    assert len(brain.agent_runs) == 1
    assert brain.agent_runs[0].run_id == agent_run.run_id

    assert agent_run.agent_name == "Document Agent"
    assert agent_run.status == AgentRunStatus.REQUIRES_REVIEW

    assert len(agent_run.input_record_ids) == 7
    assert len(agent_run.output_record_ids) == 1
    assert len(agent_run.evidence_ids) == analysis.evidence_count

    assert "evidence_extraction" in agent_run.tools_used
    assert "risk_extraction" in agent_run.tools_used
    assert "clarification_generation" in agent_run.tools_used

    assert agent_run.human_review_required is True


def test_document_workflow_is_idempotent_for_same_brain():
    _, brain, _ = run_document_workflow()

    initial_record_count = len(brain.records)
    initial_run_count = len(brain.agent_runs)

    _, updated_brain, _ = run_document_workflow(brain)

    assert updated_brain is brain
    assert len(updated_brain.records) == initial_record_count
    assert len(updated_brain.agent_runs) == initial_run_count
