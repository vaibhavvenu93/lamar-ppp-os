"""
Synthetic PPP tender package for Lamar PPP OS.

This fixture represents selected material sections from a fictional
486-page procurement package for the Eastern Province Independent
Water Project.

It is intentionally synthetic.

The purpose is to demonstrate how Lamar PPP OS can convert a large
infrastructure procurement package into evidence-backed project
intelligence without using Lamar Holding confidential information.
"""

from datetime import date

from lamar_os.domain.document import (
    DocumentSection,
    DocumentType,
    ProjectDocument,
)


PROJECT_ID = "DEMO-WATER-001"
OPPORTUNITY_ID = "OPP-WATER-001"


def build_demo_tender_package() -> list[ProjectDocument]:
    """
    Build the synthetic procurement package used by the Document Agent.

    The package represents seven documents and 486 total pages.
    Only decision-relevant sections are materialized in the demo.
    """

    return [
        ProjectDocument(
            document_id="DOC-WATER-RFP-001",
            project_id=PROJECT_ID,
            name="Volume I - Request for Proposal",
            document_type=DocumentType.REQUEST_FOR_PROPOSAL,
            description=(
                "Procurement instructions, bidder qualification, "
                "submission requirements and evaluation framework."
            ),
            version="1.0",
            issued_by="Synthetic Water Authority",
            issued_date=date(2026, 8, 15),
            page_count=82,
            source_reference="DEMO/RFP/VOL-I",
            is_synthetic=True,
            sections=[
                DocumentSection(
                    section_id="SEC-RFP-3.2",
                    document_id="DOC-WATER-RFP-001",
                    title="Consortium Qualification",
                    page_start=24,
                    page_end=27,
                    clause_reference="3.2",
                    text=(
                        "The Bidder shall demonstrate experience in the "
                        "development, financing, construction and operation "
                        "of at least two water infrastructure projects with "
                        "aggregate capital value exceeding USD 500 million. "
                        "Where the Bidder is a consortium, the Lead Member "
                        "shall maintain not less than 35 percent economic "
                        "interest through financial close."
                    ),
                ),
                DocumentSection(
                    section_id="SEC-RFP-4.1",
                    document_id="DOC-WATER-RFP-001",
                    title="Bid Submission Deadline",
                    page_start=31,
                    page_end=31,
                    clause_reference="4.1",
                    text=(
                        "Technical and Commercial Proposals shall be "
                        "submitted no later than 14:00 local time on "
                        "30 October 2026. Late submissions may be rejected."
                    ),
                ),
                DocumentSection(
                    section_id="SEC-RFP-4.4",
                    document_id="DOC-WATER-RFP-001",
                    title="Bid Security",
                    page_start=34,
                    page_end=35,
                    clause_reference="4.4",
                    text=(
                        "Each Bidder shall provide an unconditional bid "
                        "security in the amount of USD 10 million, valid "
                        "for 180 days following the Proposal Due Date."
                    ),
                ),
                DocumentSection(
                    section_id="SEC-RFP-5.3",
                    document_id="DOC-WATER-RFP-001",
                    title="Committed Financing Plan",
                    page_start=46,
                    page_end=49,
                    clause_reference="5.3",
                    text=(
                        "The Commercial Proposal shall include a committed "
                        "financing plan identifying proposed debt and equity "
                        "sources, financing assumptions, expected tenor, "
                        "security package and evidence of lender engagement."
                    ),
                ),
                DocumentSection(
                    section_id="SEC-RFP-6.2",
                    document_id="DOC-WATER-RFP-001",
                    title="Clarification Procedure",
                    page_start=57,
                    page_end=58,
                    clause_reference="6.2",
                    text=(
                        "Requests for clarification shall be submitted to "
                        "the Authority no later than 25 September 2026. "
                        "The Authority may issue responses or addenda at "
                        "its sole discretion."
                    ),
                ),
            ],
        ),
        ProjectDocument(
            document_id="DOC-WATER-TECH-002",
            project_id=PROJECT_ID,
            name="Volume II - Technical Requirements",
            document_type=DocumentType.TECHNICAL_SPECIFICATION,
            description=(
                "Plant capacity, water quality, availability, energy "
                "performance and technical delivery requirements."
            ),
            version="1.0",
            issued_by="Synthetic Water Authority",
            issued_date=date(2026, 8, 15),
            page_count=118,
            source_reference="DEMO/RFP/VOL-II",
            is_synthetic=True,
            sections=[
                DocumentSection(
                    section_id="SEC-TECH-8.4.2",
                    document_id="DOC-WATER-TECH-002",
                    title="Guaranteed Production Capacity",
                    page_start=67,
                    page_end=69,
                    clause_reference="8.4.2",
                    text=(
                        "The Facility shall provide a Guaranteed Production "
                        "Capacity of not less than 80,000 cubic metres per "
                        "day of potable water at the Delivery Point."
                    ),
                ),
                DocumentSection(
                    section_id="SEC-TECH-8.5.1",
                    document_id="DOC-WATER-TECH-002",
                    title="Plant Availability",
                    page_start=72,
                    page_end=74,
                    clause_reference="8.5.1",
                    text=(
                        "Annual Facility Availability shall be not less "
                        "than 96 percent, excluding approved scheduled "
                        "maintenance periods. Failure to achieve the "
                        "availability requirement may result in payment "
                        "deductions under the Water Purchase Agreement."
                    ),
                ),
                DocumentSection(
                    section_id="SEC-TECH-9.3",
                    document_id="DOC-WATER-TECH-002",
                    title="Specific Energy Consumption",
                    page_start=83,
                    page_end=86,
                    clause_reference="9.3",
                    text=(
                        "The Bidder shall state the guaranteed Specific "
                        "Energy Consumption of the desalination facility. "
                        "Energy consumption above the guaranteed level "
                        "shall remain at the Project Company's economic risk."
                    ),
                ),
                DocumentSection(
                    section_id="SEC-TECH-10.2",
                    document_id="DOC-WATER-TECH-002",
                    title="Critical Equipment",
                    page_start=94,
                    page_end=98,
                    clause_reference="10.2",
                    text=(
                        "The Bidder shall identify long-lead desalination "
                        "equipment including high-pressure pumps, membranes, "
                        "energy recovery devices and major electrical "
                        "equipment together with the proposed procurement "
                        "and delivery programme."
                    ),
                ),
            ],
        ),
        ProjectDocument(
            document_id="DOC-WATER-WPA-003",
            project_id=PROJECT_ID,
            name="Draft Water Purchase Agreement",
            document_type=DocumentType.CONCESSION_AGREEMENT,
            description=(
                "Synthetic long-term offtake agreement defining payment, "
                "performance and operating obligations."
            ),
            version="Draft 1",
            issued_by="Synthetic Water Authority",
            issued_date=date(2026, 8, 15),
            page_count=96,
            source_reference="DEMO/WPA/DRAFT",
            is_synthetic=True,
            sections=[
                DocumentSection(
                    section_id="SEC-WPA-12.1",
                    document_id="DOC-WATER-WPA-003",
                    title="Availability Payment",
                    page_start=41,
                    page_end=44,
                    clause_reference="12.1",
                    text=(
                        "Subject to Facility Availability and compliance "
                        "with the Water Quality Requirements, the Offtaker "
                        "shall pay the Project Company a monthly Availability "
                        "Payment calculated in accordance with Schedule 6."
                    ),
                ),
                DocumentSection(
                    section_id="SEC-WPA-12.4",
                    document_id="DOC-WATER-WPA-003",
                    title="Availability Deductions",
                    page_start=47,
                    page_end=50,
                    clause_reference="12.4",
                    text=(
                        "Where Facility Availability falls below 96 percent, "
                        "the monthly Availability Payment shall be subject "
                        "to deductions. Repeated availability below "
                        "92 percent may constitute a Project Company Event "
                        "of Default following applicable cure periods."
                    ),
                ),
                DocumentSection(
                    section_id="SEC-WPA-14.3",
                    document_id="DOC-WATER-WPA-003",
                    title="Energy Price Exposure",
                    page_start=57,
                    page_end=59,
                    clause_reference="14.3",
                    text=(
                        "The Project Company shall bear electricity costs "
                        "associated with Facility operation except to the "
                        "extent expressly adjusted under the Energy Price "
                        "Indexation Mechanism. No adjustment shall apply "
                        "for consumption exceeding the Guaranteed Specific "
                        "Energy Consumption."
                    ),
                ),
                DocumentSection(
                    section_id="SEC-WPA-18.2",
                    document_id="DOC-WATER-WPA-003",
                    title="Reporting Obligation",
                    page_start=73,
                    page_end=75,
                    clause_reference="18.2",
                    text=(
                        "The Project Company shall provide monthly operating "
                        "reports within ten Business Days following each "
                        "month end, including production, availability, "
                        "water quality, energy consumption and maintenance "
                        "performance."
                    ),
                ),
            ],
        ),
        ProjectDocument(
            document_id="DOC-WATER-IMPL-004",
            project_id=PROJECT_ID,
            name="Draft Implementation Agreement",
            document_type=DocumentType.CONTRACT,
            description=(
                "Synthetic project implementation agreement covering "
                "delivery, delay, government support and termination."
            ),
            version="Draft 1",
            issued_by="Synthetic Government Entity",
            issued_date=date(2026, 8, 15),
            page_count=74,
            source_reference="DEMO/IA/DRAFT",
            is_synthetic=True,
            sections=[
                DocumentSection(
                    section_id="SEC-IA-7.1",
                    document_id="DOC-WATER-IMPL-004",
                    title="Scheduled Commercial Operation Date",
                    page_start=29,
                    page_end=31,
                    clause_reference="7.1",
                    text=(
                        "The Project Company shall achieve Commercial "
                        "Operation no later than 36 months following the "
                        "Effective Date, subject only to relief expressly "
                        "provided under this Agreement."
                    ),
                ),
                DocumentSection(
                    section_id="SEC-IA-7.4",
                    document_id="DOC-WATER-IMPL-004",
                    title="Delay Liquidated Damages",
                    page_start=34,
                    page_end=36,
                    clause_reference="7.4",
                    text=(
                        "Delay Liquidated Damages shall accrue at USD "
                        "150,000 for each day of Project Company delay "
                        "following the Scheduled Commercial Operation Date, "
                        "subject to an aggregate cap of USD 25 million."
                    ),
                ),
                DocumentSection(
                    section_id="SEC-IA-15.2",
                    document_id="DOC-WATER-IMPL-004",
                    title="Change in Law",
                    page_start=58,
                    page_end=61,
                    clause_reference="15.2",
                    text=(
                        "Qualifying Change in Law relief shall be available "
                        "only where the Project Company demonstrates a "
                        "material project-specific cost or schedule impact "
                        "and complies with the applicable notice procedure."
                    ),
                ),
            ],
        ),
        ProjectDocument(
            document_id="DOC-WATER-COMM-005",
            project_id=PROJECT_ID,
            name="Commercial Schedules",
            document_type=DocumentType.COMMERCIAL_SCHEDULE,
            description=(
                "Synthetic commercial schedules containing payment and "
                "performance assumptions."
            ),
            version="1.0",
            issued_by="Synthetic Water Authority",
            issued_date=date(2026, 8, 15),
            page_count=48,
            source_reference="DEMO/COMM/SCHEDULES",
            is_synthetic=True,
            sections=[
                DocumentSection(
                    section_id="SEC-COMM-6.1",
                    document_id="DOC-WATER-COMM-005",
                    title="Payment Structure",
                    page_start=16,
                    page_end=20,
                    clause_reference="Schedule 6.1",
                    text=(
                        "The proposed payment mechanism consists primarily "
                        "of a capacity-based Availability Payment subject "
                        "to performance deductions and indexation provisions."
                    ),
                ),
                DocumentSection(
                    section_id="SEC-COMM-9.2",
                    document_id="DOC-WATER-COMM-005",
                    title="Performance Security",
                    page_start=31,
                    page_end=33,
                    clause_reference="Schedule 9.2",
                    text=(
                        "Prior to the Effective Date, the Project Company "
                        "shall provide Performance Security equal to "
                        "5 percent of total EPC Contract value."
                    ),
                ),
            ],
        ),
        ProjectDocument(
            document_id="DOC-WATER-FIN-006",
            project_id=PROJECT_ID,
            name="Financing Requirements",
            document_type=DocumentType.FINANCIAL_SCHEDULE,
            description=(
                "Synthetic financing conditions and financial close "
                "requirements."
            ),
            version="1.0",
            issued_by="Synthetic Water Authority",
            issued_date=date(2026, 8, 15),
            page_count=36,
            source_reference="DEMO/FIN/REQ",
            is_synthetic=True,
            sections=[
                DocumentSection(
                    section_id="SEC-FIN-3.1",
                    document_id="DOC-WATER-FIN-006",
                    title="Financial Close",
                    page_start=11,
                    page_end=14,
                    clause_reference="3.1",
                    text=(
                        "The Preferred Bidder shall achieve Financial Close "
                        "within 180 days following award unless extended "
                        "by the Authority in writing."
                    ),
                ),
                DocumentSection(
                    section_id="SEC-FIN-4.2",
                    document_id="DOC-WATER-FIN-006",
                    title="Minimum Equity Commitment",
                    page_start=18,
                    page_end=20,
                    clause_reference="4.2",
                    text=(
                        "The Project Company shall be funded with not less "
                        "than 25 percent equity at Financial Close unless "
                        "otherwise approved by the Authority."
                    ),
                ),
            ],
        ),
        ProjectDocument(
            document_id="DOC-WATER-ESG-007",
            project_id=PROJECT_ID,
            name="Environmental and Social Requirements",
            document_type=DocumentType.LEGAL_SCHEDULE,
            description=(
                "Synthetic environmental, permitting and social "
                "compliance requirements."
            ),
            version="1.0",
            issued_by="Synthetic Water Authority",
            issued_date=date(2026, 8, 15),
            page_count=32,
            source_reference="DEMO/ESG/REQ",
            is_synthetic=True,
            sections=[
                DocumentSection(
                    section_id="SEC-ESG-5.1",
                    document_id="DOC-WATER-ESG-007",
                    title="Environmental Permitting",
                    page_start=14,
                    page_end=17,
                    clause_reference="5.1",
                    text=(
                        "The Project Company shall obtain and maintain all "
                        "environmental permits required for construction "
                        "and operation of the Facility."
                    ),
                ),
                DocumentSection(
                    section_id="SEC-ESG-6.3",
                    document_id="DOC-WATER-ESG-007",
                    title="Marine Discharge Compliance",
                    page_start=22,
                    page_end=25,
                    clause_reference="6.3",
                    text=(
                        "Brine discharge and other marine discharges shall "
                        "comply with applicable environmental standards and "
                        "the approved marine environmental management plan."
                    ),
                ),
            ],
        ),
    ]


def tender_package_page_count(
    documents: list[ProjectDocument],
) -> int:
    """Return the represented total page count."""

    return sum(
        document.page_count or 0
        for document in documents
    )


def tender_package_section_count(
    documents: list[ProjectDocument],
) -> int:
    """Return the number of materialized demo sections."""

    return sum(
        len(document.sections)
        for document in documents
    )


def tender_package_summary() -> dict[str, object]:
    """Return basic metadata for the synthetic tender package."""

    documents = build_demo_tender_package()

    return {
        "project_id": PROJECT_ID,
        "opportunity_id": OPPORTUNITY_ID,
        "document_count": len(documents),
        "page_count": tender_package_page_count(documents),
        "materialized_section_count": tender_package_section_count(
            documents
        ),
        "data_classification": "SYNTHETIC_DEMO",
        "confidential_information_used": False,
    }
