"""
Evidence-first Document Agent for Lamar PPP OS.

The prototype agent operates over the synthetic tender package and
demonstrates the orchestration contract that a production document
intelligence pipeline could later implement with OCR, retrieval,
structured LLM extraction, validation and human review.

Important:

    Documents provide evidence.
    The agent structures interpretation.
    Humans approve consequential conclusions.
"""

from datetime import date

from demo.tender_package import (
    OPPORTUNITY_ID,
    PROJECT_ID,
    build_demo_tender_package,
)
from lamar_os.domain.document import (
    ClarificationQuestion,
    DocumentAnalysis,
    DocumentAnalysisStatus,
    DocumentEvidence,
    ExtractedDocumentRisk,
    ExtractedObligation,
    ExtractedProjectDate,
    ExtractedRequirement,
    ExtractedRiskCategory,
    ObligationCategory,
    ProjectDocument,
    RequirementCategory,
)


AGENT_NAME = "Document Agent"


def _find_document(
    documents: list[ProjectDocument],
    document_id: str,
) -> ProjectDocument:
    for document in documents:
        if document.document_id == document_id:
            return document

    raise ValueError(
        f"Document '{document_id}' does not exist in the tender package."
    )


def _evidence_from_section(
    documents: list[ProjectDocument],
    document_id: str,
    section_id: str,
    evidence_id: str,
    confidence: float = 0.97,
) -> DocumentEvidence:
    """
    Create evidence directly from a known source section.

    This keeps every material extraction traceable back to the
    procurement package.
    """

    document = _find_document(documents, document_id)

    for section in document.sections:
        if section.section_id == section_id:
            return DocumentEvidence(
                evidence_id=evidence_id,
                document_id=document.document_id,
                document_name=document.name,
                page_number=section.page_start,
                clause_reference=section.clause_reference,
                section_title=section.title,
                source_text=section.text,
                confidence=confidence,
            )

    raise ValueError(
        f"Section '{section_id}' does not exist in "
        f"document '{document_id}'."
    )


def _build_evidence(
    documents: list[ProjectDocument],
) -> list[DocumentEvidence]:
    """Build the evidence set used by structured extractions."""

    evidence_specs = [
        (
            "EV-001",
            "DOC-WATER-RFP-001",
            "SEC-RFP-3.2",
            0.98,
        ),
        (
            "EV-002",
            "DOC-WATER-RFP-001",
            "SEC-RFP-4.1",
            0.99,
        ),
        (
            "EV-003",
            "DOC-WATER-RFP-001",
            "SEC-RFP-4.4",
            0.99,
        ),
        (
            "EV-004",
            "DOC-WATER-RFP-001",
            "SEC-RFP-5.3",
            0.97,
        ),
        (
            "EV-005",
            "DOC-WATER-RFP-001",
            "SEC-RFP-6.2",
            0.99,
        ),
        (
            "EV-006",
            "DOC-WATER-TECH-002",
            "SEC-TECH-8.4.2",
            0.99,
        ),
        (
            "EV-007",
            "DOC-WATER-TECH-002",
            "SEC-TECH-8.5.1",
            0.98,
        ),
        (
            "EV-008",
            "DOC-WATER-TECH-002",
            "SEC-TECH-9.3",
            0.96,
        ),
        (
            "EV-009",
            "DOC-WATER-TECH-002",
            "SEC-TECH-10.2",
            0.96,
        ),
        (
            "EV-010",
            "DOC-WATER-WPA-003",
            "SEC-WPA-12.1",
            0.98,
        ),
        (
            "EV-011",
            "DOC-WATER-WPA-003",
            "SEC-WPA-12.4",
            0.98,
        ),
        (
            "EV-012",
            "DOC-WATER-WPA-003",
            "SEC-WPA-14.3",
            0.97,
        ),
        (
            "EV-013",
            "DOC-WATER-WPA-003",
            "SEC-WPA-18.2",
            0.98,
        ),
        (
            "EV-014",
            "DOC-WATER-IMPL-004",
            "SEC-IA-7.1",
            0.98,
        ),
        (
            "EV-015",
            "DOC-WATER-IMPL-004",
            "SEC-IA-7.4",
            0.99,
        ),
        (
            "EV-016",
            "DOC-WATER-IMPL-004",
            "SEC-IA-15.2",
            0.95,
        ),
        (
            "EV-017",
            "DOC-WATER-COMM-005",
            "SEC-COMM-6.1",
            0.97,
        ),
        (
            "EV-018",
            "DOC-WATER-COMM-005",
            "SEC-COMM-9.2",
            0.98,
        ),
        (
            "EV-019",
            "DOC-WATER-FIN-006",
            "SEC-FIN-3.1",
            0.98,
        ),
        (
            "EV-020",
            "DOC-WATER-FIN-006",
            "SEC-FIN-4.2",
            0.98,
        ),
        (
            "EV-021",
            "DOC-WATER-ESG-007",
            "SEC-ESG-5.1",
            0.97,
        ),
        (
            "EV-022",
            "DOC-WATER-ESG-007",
            "SEC-ESG-6.3",
            0.96,
        ),
    ]

    return [
        _evidence_from_section(
            documents=documents,
            document_id=document_id,
            section_id=section_id,
            evidence_id=evidence_id,
            confidence=confidence,
        )
        for (
            evidence_id,
            document_id,
            section_id,
            confidence,
        ) in evidence_specs
    ]


def _build_requirements() -> list[ExtractedRequirement]:
    """Build material bid requirements identified by the agent."""

    return [
        ExtractedRequirement(
            requirement_id="REQ-001",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-RFP-001",
            title="Water infrastructure track record",
            description=(
                "Bidder must demonstrate development, financing, "
                "construction and operating experience across at least "
                "two water infrastructure projects with aggregate "
                "capital value above USD 500 million."
            ),
            category=RequirementCategory.CONSORTIUM,
            evidence_ids=["EV-001"],
            confidence=0.98,
        ),
        ExtractedRequirement(
            requirement_id="REQ-002",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-RFP-001",
            title="Lead member economic interest",
            description=(
                "Consortium Lead Member must maintain at least "
                "35 percent economic interest through financial close."
            ),
            category=RequirementCategory.CONSORTIUM,
            evidence_ids=["EV-001"],
            confidence=0.98,
        ),
        ExtractedRequirement(
            requirement_id="REQ-003",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-RFP-001",
            title="Proposal submission",
            description=(
                "Technical and Commercial Proposals must be submitted "
                "by the stated proposal deadline."
            ),
            category=RequirementCategory.SUBMISSION,
            due_date=date(2026, 10, 30),
            evidence_ids=["EV-002"],
            confidence=0.99,
        ),
        ExtractedRequirement(
            requirement_id="REQ-004",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-RFP-001",
            title="USD 10 million bid security",
            description=(
                "Bidder must provide unconditional USD 10 million "
                "bid security valid for 180 days after the proposal "
                "due date."
            ),
            category=RequirementCategory.COMMERCIAL,
            evidence_ids=["EV-003"],
            confidence=0.99,
        ),
        ExtractedRequirement(
            requirement_id="REQ-005",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-RFP-001",
            title="Committed financing plan",
            description=(
                "Commercial Proposal must identify debt and equity "
                "sources, financing assumptions, tenor, security "
                "package and evidence of lender engagement."
            ),
            category=RequirementCategory.FINANCIAL,
            evidence_ids=["EV-004"],
            confidence=0.97,
        ),
        ExtractedRequirement(
            requirement_id="REQ-006",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-TECH-002",
            title="Minimum production capacity",
            description=(
                "Facility must provide at least 80,000 cubic metres "
                "per day of potable water."
            ),
            category=RequirementCategory.TECHNICAL,
            evidence_ids=["EV-006"],
            confidence=0.99,
        ),
        ExtractedRequirement(
            requirement_id="REQ-007",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-TECH-002",
            title="Minimum annual availability",
            description=(
                "Facility must maintain annual availability of at "
                "least 96 percent excluding approved scheduled "
                "maintenance."
            ),
            category=RequirementCategory.OPERATIONS,
            evidence_ids=["EV-007"],
            confidence=0.98,
        ),
        ExtractedRequirement(
            requirement_id="REQ-008",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-TECH-002",
            title="Guaranteed energy consumption",
            description=(
                "Bidder must state a guaranteed Specific Energy "
                "Consumption for the desalination facility."
            ),
            category=RequirementCategory.TECHNICAL,
            evidence_ids=["EV-008"],
            confidence=0.96,
        ),
        ExtractedRequirement(
            requirement_id="REQ-009",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-TECH-002",
            title="Long-lead procurement programme",
            description=(
                "Bidder must identify critical long-lead desalination "
                "and electrical equipment and provide a procurement "
                "and delivery programme."
            ),
            category=RequirementCategory.TECHNICAL,
            evidence_ids=["EV-009"],
            confidence=0.96,
        ),
        ExtractedRequirement(
            requirement_id="REQ-010",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-COMM-005",
            title="Performance security",
            description=(
                "Project Company must provide performance security "
                "equal to 5 percent of EPC Contract value before the "
                "Effective Date."
            ),
            category=RequirementCategory.COMMERCIAL,
            evidence_ids=["EV-018"],
            confidence=0.98,
        ),
        ExtractedRequirement(
            requirement_id="REQ-011",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-FIN-006",
            title="Minimum equity commitment",
            description=(
                "Project Company must be funded with at least "
                "25 percent equity at Financial Close unless otherwise "
                "approved."
            ),
            category=RequirementCategory.FINANCIAL,
            evidence_ids=["EV-020"],
            confidence=0.98,
        ),
        ExtractedRequirement(
            requirement_id="REQ-012",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-ESG-007",
            title="Environmental permitting",
            description=(
                "Project Company must obtain and maintain all "
                "environmental permits required for construction "
                "and operation."
            ),
            category=RequirementCategory.ESG,
            evidence_ids=["EV-021"],
            confidence=0.97,
        ),
        ExtractedRequirement(
            requirement_id="REQ-013",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-ESG-007",
            title="Marine discharge compliance",
            description=(
                "Brine and other marine discharges must comply with "
                "applicable environmental standards and the approved "
                "marine environmental management plan."
            ),
            category=RequirementCategory.ESG,
            evidence_ids=["EV-022"],
            confidence=0.96,
        ),
    ]


def _build_obligations() -> list[ExtractedObligation]:
    """Build contractual and operational obligations."""

    return [
        ExtractedObligation(
            obligation_id="OBL-001",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-WPA-003",
            title="Maintain facility availability",
            description=(
                "Project Company must maintain contractual facility "
                "availability to protect the availability payment."
            ),
            category=ObligationCategory.PERFORMANCE,
            obligated_party="Project Company",
            beneficiary_party="Offtaker",
            consequence_description=(
                "Payment deductions apply below the contractual "
                "availability threshold."
            ),
            evidence_ids=["EV-007", "EV-011"],
            confidence=0.98,
        ),
        ExtractedObligation(
            obligation_id="OBL-002",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-WPA-003",
            title="Bear excess energy consumption cost",
            description=(
                "Project Company bears operating electricity cost "
                "exposure above the guaranteed Specific Energy "
                "Consumption."
            ),
            category=ObligationCategory.PERFORMANCE,
            obligated_party="Project Company",
            beneficiary_party="Offtaker",
            consequence_description=(
                "No energy-price adjustment applies to consumption "
                "above the guaranteed level."
            ),
            evidence_ids=["EV-008", "EV-012"],
            confidence=0.97,
        ),
        ExtractedObligation(
            obligation_id="OBL-003",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-WPA-003",
            title="Monthly operating reporting",
            description=(
                "Project Company must submit monthly production, "
                "availability, water quality, energy consumption and "
                "maintenance reports."
            ),
            category=ObligationCategory.REPORTING,
            obligated_party="Project Company",
            beneficiary_party="Offtaker",
            trigger="Each month end",
            consequence_description=(
                "Report due within ten Business Days after month end."
            ),
            evidence_ids=["EV-013"],
            confidence=0.98,
        ),
        ExtractedObligation(
            obligation_id="OBL-004",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-IMPL-004",
            title="Achieve commercial operation",
            description=(
                "Project Company must achieve Commercial Operation "
                "within 36 months following the Effective Date."
            ),
            category=ObligationCategory.CONSTRUCTION,
            obligated_party="Project Company",
            beneficiary_party="Authority",
            trigger="Effective Date",
            consequence_description=(
                "Project Company delay may trigger liquidated damages."
            ),
            evidence_ids=["EV-014", "EV-015"],
            confidence=0.98,
        ),
        ExtractedObligation(
            obligation_id="OBL-005",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-ESG-007",
            title="Maintain environmental permits",
            description=(
                "Project Company must obtain and maintain required "
                "environmental permits throughout construction and "
                "operations."
            ),
            category=ObligationCategory.COMPLIANCE,
            obligated_party="Project Company",
            beneficiary_party="Authority",
            evidence_ids=["EV-021"],
            confidence=0.97,
        ),
    ]


def _build_dates() -> list[ExtractedProjectDate]:
    """Build material procurement dates."""

    return [
        ExtractedProjectDate(
            date_id="DATE-001",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-RFP-001",
            title="Clarification deadline",
            event_date=date(2026, 9, 25),
            description=(
                "Final date for bidder clarification requests."
            ),
            critical=True,
            evidence_ids=["EV-005"],
            confidence=0.99,
        ),
        ExtractedProjectDate(
            date_id="DATE-002",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-RFP-001",
            title="Proposal due date",
            event_date=date(2026, 10, 30),
            description=(
                "Technical and Commercial Proposal submission deadline."
            ),
            critical=True,
            evidence_ids=["EV-002"],
            confidence=0.99,
        ),
    ]


def _build_risks() -> list[ExtractedDocumentRisk]:
    """Build document-derived project risks."""

    return [
        ExtractedDocumentRisk(
            risk_id="DOC-RISK-001",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-TECH-002",
            title="Long-lead equipment procurement",
            description=(
                "Critical desalination and electrical equipment may "
                "create schedule exposure within the 36-month delivery "
                "requirement."
            ),
            category=ExtractedRiskCategory.PROCUREMENT,
            potential_impact=(
                "Commercial operation delay and liquidated damages."
            ),
            estimated_impact_usd=25_000_000,
            evidence_ids=["EV-009", "EV-014", "EV-015"],
            confidence=0.94,
        ),
        ExtractedDocumentRisk(
            risk_id="DOC-RISK-002",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-WPA-003",
            title="Availability payment deductions",
            description=(
                "Availability below 96 percent reduces revenue and "
                "repeated performance below 92 percent may escalate "
                "toward default."
            ),
            category=ExtractedRiskCategory.REVENUE,
            potential_impact=(
                "Reduced availability payments and potential default "
                "exposure."
            ),
            evidence_ids=["EV-007", "EV-010", "EV-011"],
            confidence=0.97,
        ),
        ExtractedDocumentRisk(
            risk_id="DOC-RISK-003",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-WPA-003",
            title="Energy efficiency downside",
            description=(
                "Electricity consumption above the guaranteed energy "
                "level remains an economic risk of the Project Company."
            ),
            category=ExtractedRiskCategory.OPERATIONS,
            potential_impact=(
                "Higher operating cost and lower project returns."
            ),
            evidence_ids=["EV-008", "EV-012"],
            confidence=0.96,
        ),
        ExtractedDocumentRisk(
            risk_id="DOC-RISK-004",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-IMPL-004",
            title="Delay liquidated damages",
            description=(
                "Project Company delay beyond scheduled commercial "
                "operation attracts daily liquidated damages."
            ),
            category=ExtractedRiskCategory.SCHEDULE,
            potential_impact=(
                "USD 150,000 per day up to USD 25 million."
            ),
            estimated_impact_usd=25_000_000,
            evidence_ids=["EV-014", "EV-015"],
            confidence=0.99,
        ),
        ExtractedDocumentRisk(
            risk_id="DOC-RISK-005",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-IMPL-004",
            title="Change in law relief conditions",
            description=(
                "Change in Law relief depends on demonstrating material "
                "project-specific impact and satisfying notice procedures."
            ),
            category=ExtractedRiskCategory.CONTRACTUAL,
            potential_impact=(
                "Cost or schedule exposure may remain with the Project "
                "Company if relief conditions are not satisfied."
            ),
            evidence_ids=["EV-016"],
            confidence=0.93,
        ),
        ExtractedDocumentRisk(
            risk_id="DOC-RISK-006",
            project_id=PROJECT_ID,
            document_id="DOC-WATER-ESG-007",
            title="Marine environmental compliance",
            description=(
                "Desalination brine discharge creates environmental "
                "permitting and ongoing compliance exposure."
            ),
            category=ExtractedRiskCategory.ENVIRONMENTAL,
            potential_impact=(
                "Permitting delay, remediation cost or operating "
                "restriction."
            ),
            evidence_ids=["EV-021", "EV-022"],
            confidence=0.94,
        ),
    ]


def _build_clarifications() -> list[ClarificationQuestion]:
    """Build recommended clarification questions for human review."""

    return [
        ClarificationQuestion(
            clarification_id="CLR-001",
            project_id=PROJECT_ID,
            title="Availability deduction curve",
            question=(
                "Please provide the complete deduction curve and worked "
                "examples applicable where annual or monthly Facility "
                "Availability falls below 96 percent."
            ),
            rationale=(
                "The draft agreement identifies deductions but the "
                "materialized sections do not quantify the revenue "
                "sensitivity required for bankability analysis."
            ),
            related_document_ids=[
                "DOC-WATER-WPA-003",
                "DOC-WATER-COMM-005",
            ],
            evidence_ids=["EV-011", "EV-017"],
            priority="HIGH",
        ),
        ClarificationQuestion(
            clarification_id="CLR-002",
            project_id=PROJECT_ID,
            title="Energy price indexation",
            question=(
                "Please clarify the Energy Price Indexation Mechanism, "
                "including the proportion of electricity-price movement "
                "passed through to the Availability Payment."
            ),
            rationale=(
                "Energy cost is a material operating exposure and the "
                "current clause does not provide enough information to "
                "model the residual risk."
            ),
            related_document_ids=["DOC-WATER-WPA-003"],
            evidence_ids=["EV-012"],
            priority="HIGH",
        ),
        ClarificationQuestion(
            clarification_id="CLR-003",
            project_id=PROJECT_ID,
            title="Effective Date assumptions",
            question=(
                "Please confirm the expected Effective Date and whether "
                "any permitting or site-access conditions precedent "
                "delay commencement of the 36-month construction period."
            ),
            rationale=(
                "The commercial operation obligation is measured from "
                "Effective Date, making commencement assumptions material "
                "to schedule risk."
            ),
            related_document_ids=["DOC-WATER-IMPL-004"],
            evidence_ids=["EV-014", "EV-015"],
            priority="HIGH",
        ),
        ClarificationQuestion(
            clarification_id="CLR-004",
            project_id=PROJECT_ID,
            title="Change in law threshold",
            question=(
                "Please clarify any monetary or schedule threshold used "
                "to determine whether a Change in Law impact is material."
            ),
            rationale=(
                "The draft clause requires material impact but the "
                "materialized language does not define the threshold."
            ),
            related_document_ids=["DOC-WATER-IMPL-004"],
            evidence_ids=["EV-016"],
            priority="MEDIUM",
        ),
    ]


def analyze_tender_package(
    documents: list[ProjectDocument] | None = None,
) -> DocumentAnalysis:
    """
    Run the deterministic prototype Document Agent.

    A production implementation could replace the extraction helpers
    with OCR, retrieval and structured model calls while retaining this
    DocumentAnalysis contract.
    """

    package = documents or build_demo_tender_package()

    evidence = _build_evidence(package)
    requirements = _build_requirements()
    obligations = _build_obligations()
    project_dates = _build_dates()
    risks = _build_risks()
    clarifications = _build_clarifications()

    return DocumentAnalysis(
        analysis_id="DOC-ANALYSIS-WATER-001",
        project_id=PROJECT_ID,
        opportunity_id=OPPORTUNITY_ID,
        status=DocumentAnalysisStatus.REQUIRES_REVIEW,
        document_ids=[
            document.document_id
            for document in package
        ],
        evidence=evidence,
        requirements=requirements,
        obligations=obligations,
        project_dates=project_dates,
        risks=risks,
        clarification_questions=clarifications,
        executive_summary=(
            "The tender package presents a strategically attractive "
            "water PPP with clear long-term availability-based revenue, "
            "but diligence should focus on construction schedule, "
            "long-lead equipment, availability deductions, residual "
            "energy-price exposure, financing commitments and marine "
            "environmental compliance. Four clarification questions "
            "should be reviewed before submission to the Authority."
        ),
        analyzed_by=AGENT_NAME,
        human_review_required=True,
    )
