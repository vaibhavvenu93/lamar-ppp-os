from __future__ import annotations

from datetime import datetime

from lamar_os.domain.bid import (
    BidDecision,
    BidFactor,
    BidIssue,
    BidIssueSeverity,
    BidIssueType,
    BidReadiness,
    BidRecommendation,
    BidStrength,
    BidWorkstream,
)
from lamar_os.domain.project import (
    AgentRun,
    AgentRunStatus,
    ApprovalStatus,
    ProjectBrain,
    ProjectRecord,
    ProjectRecordType,
    RecordSource,
    RecordStatus,
)


def _factor(
    factor_id: str,
    name: str,
    category: str,
    score: float,
    weight: float,
    rationale: str,
    evidence_ids: list[str] | None = None,
) -> BidFactor:
    return BidFactor(
        factor_id=factor_id,
        name=name,
        category=category,
        score=score,
        weight=weight,
        rationale=rationale,
        evidence_ids=evidence_ids or [],
    )


def _issue(
    issue_id: str,
    title: str,
    description: str,
    issue_type: BidIssueType,
    severity: BidIssueSeverity,
    blocking: bool,
    estimated_exposure_usd: float | None = None,
    owner: str | None = None,
    resolution_required: str | None = None,
    evidence_ids: list[str] | None = None,
) -> BidIssue:
    return BidIssue(
        issue_id=issue_id,
        title=title,
        description=description,
        issue_type=issue_type,
        severity=severity,
        blocking=blocking,
        estimated_exposure_usd=estimated_exposure_usd,
        owner=owner,
        resolution_required=resolution_required,
        evidence_ids=evidence_ids or [],
    )


def calculate_readiness_score(
    factors: list[BidFactor],
) -> float:
    total_weight = sum(
        factor.weight
        for factor in factors
    )

    if total_weight <= 0:
        return 0.0

    weighted_total = sum(
        factor.weighted_score
        for factor in factors
    )

    return round(
        weighted_total / total_weight,
        1,
    )


def determine_recommendation(
    readiness_score: float,
    issues: list[BidIssue],
) -> tuple[
    BidRecommendation,
    BidReadiness,
]:
    critical_blockers = [
        issue
        for issue in issues
        if (
            issue.blocking
            and issue.severity
            == BidIssueSeverity.CRITICAL
        )
    ]

    high_blockers = [
        issue
        for issue in issues
        if (
            issue.blocking
            and issue.severity
            == BidIssueSeverity.HIGH
        )
    ]

    if len(critical_blockers) >= 2:
        return (
            BidRecommendation.NO_BID,
            BidReadiness.NOT_READY,
        )

    if readiness_score < 55:
        return (
            BidRecommendation.NO_BID,
            BidReadiness.NOT_READY,
        )

    if critical_blockers:
        return (
            BidRecommendation.HOLD,
            BidReadiness.NOT_READY,
        )

    if high_blockers or readiness_score < 80:
        return (
            BidRecommendation.CONDITIONAL_PURSUE,
            BidReadiness.CONDITIONAL,
        )

    return (
        BidRecommendation.PURSUE,
        BidReadiness.READY,
    )


def write_bid_decision_to_project_brain(
    decision: BidDecision,
    brain: ProjectBrain,
) -> AgentRun:
    """
    Persist deterministic Bid Agent output into shared project state.

    The Bid Agent remains a recommendation system. Writing its
    recommendation into the Project Brain does not constitute human
    Bid / No-Bid approval.
    """

    if brain.project_id != decision.project_id:
        raise ValueError(
            "Bid decision belongs to a different Project Brain."
        )

    now = datetime.utcnow()

    for issue in decision.issues:
        related_record_ids = [
            *issue.evidence_ids,
        ]

        brain.upsert_record(
            ProjectRecord(
                record_id=issue.issue_id,
                project_id=decision.project_id,
                record_type=ProjectRecordType.BID_ISSUE,
                title=issue.title,
                summary=issue.description,
                source=RecordSource.AGENT,
                source_reference="Bid Agent",
                payload={
                    "issue_type": issue.issue_type.value,
                    "severity": issue.severity.value,
                    "blocking": issue.blocking,
                    "estimated_exposure_usd": (
                        issue.estimated_exposure_usd
                    ),
                    "resolution_required": (
                        issue.resolution_required
                    ),
                },
                created_by="Bid Agent",
                status=RecordStatus.OPEN,
                approval_status=(
                    ApprovalStatus.PENDING
                    if issue.blocking
                    else ApprovalStatus.NOT_REQUIRED
                ),
                evidence_ids=list(
                    issue.evidence_ids
                ),
                related_record_ids=related_record_ids,
                owner=issue.owner,
                priority=issue.severity.value,
                tags=[
                    "BID",
                    "ISSUE",
                    issue.issue_type.value,
                    issue.severity.value,
                    *(
                        ["BLOCKER"]
                        if issue.blocking
                        else []
                    ),
                ],
            )
        )

    for workstream in decision.workstreams:
        brain.upsert_record(
            ProjectRecord(
                record_id=workstream.workstream_id,
                project_id=decision.project_id,
                record_type=ProjectRecordType.WORKSTREAM,
                title=workstream.name,
                summary=workstream.objective,
                source=RecordSource.AGENT,
                source_reference="Bid Agent",
                payload={
                    "objective": workstream.objective,
                    "status": workstream.status,
                    "dependencies": list(
                        workstream.dependencies
                    ),
                },
                created_by="Bid Agent",
                status=(
                    RecordStatus.IN_PROGRESS
                    if workstream.status
                    == "IN_PROGRESS"
                    else RecordStatus.OPEN
                ),
                approval_status=(
                    ApprovalStatus.NOT_REQUIRED
                ),
                evidence_ids=list(
                    workstream.evidence_ids
                ),
                related_record_ids=[
                    *workstream.dependencies,
                    *workstream.evidence_ids,
                ],
                owner=workstream.owner,
                priority=workstream.priority,
                tags=[
                    "BID",
                    "WORKSTREAM",
                    workstream.priority,
                ],
            )
        )

    decision_record_id = (
        f"BID-DECISION-{decision.opportunity_id}"
    )

    brain.upsert_record(
        ProjectRecord(
            record_id=decision_record_id,
            project_id=decision.project_id,
            record_type=ProjectRecordType.DECISION,
            title="Bid Agent pursuit recommendation",
            summary=decision.executive_thesis,
            source=RecordSource.AGENT,
            source_reference="Bid Agent",
            payload={
                "opportunity_id": (
                    decision.opportunity_id
                ),
                "recommendation": (
                    decision.recommendation.value
                ),
                "readiness": (
                    decision.readiness.value
                ),
                "readiness_score": (
                    decision.readiness_score
                ),
                "confidence": decision.confidence,
                "decision_rationale": (
                    decision.decision_rationale
                ),
                "unresolved_blockers": list(
                    decision.unresolved_blockers
                ),
                "clarification_ids": list(
                    decision.clarification_ids
                ),
                "human_approval_required": (
                    decision.human_approval_required
                ),
                "approved": decision.approved,
            },
            created_by="Bid Agent",
            status=RecordStatus.OPEN,
            approval_status=(
                ApprovalStatus.PENDING
                if decision.human_approval_required
                and not decision.approved
                else ApprovalStatus.NOT_REQUIRED
            ),
            evidence_ids=list(
                decision.evidence_ids
            ),
            related_record_ids=[
                *[
                    issue.issue_id
                    for issue in decision.issues
                ],
                *[
                    workstream.workstream_id
                    for workstream
                    in decision.workstreams
                ],
                *decision.clarification_ids,
            ],
            owner="Investment Committee",
            priority="HIGH",
            tags=[
                "BID",
                "DECISION",
                decision.recommendation.value,
            ],
        )
    )

    run_id = (
        f"AGENT-RUN-BID-{decision.opportunity_id}"
    )

    existing_run = brain.agent_run_by_id(
        run_id
    )

    if existing_run is not None:
        brain.agent_runs.remove(
            existing_run
        )

    output_record_ids = [
        *[
            issue.issue_id
            for issue in decision.issues
        ],
        *[
            workstream.workstream_id
            for workstream in decision.workstreams
        ],
        decision_record_id,
    ]

    run = AgentRun(
        run_id=run_id,
        project_id=decision.project_id,
        agent_name="Bid Agent",
        task=(
            "Evaluate pursuit readiness and convert "
            "decision gaps into governed Project Brain state."
        ),
        status=AgentRunStatus.COMPLETED,
        input_record_ids=[
            *decision.clarification_ids,
            *decision.evidence_ids,
        ],
        tools_used=[
            "deterministic_bid_scoring",
            "issue_classification",
            "workstream_generation",
            "project_brain_writer",
        ],
        output_record_ids=output_record_ids,
        evidence_ids=list(
            decision.evidence_ids
        ),
        summary=(
            f"{decision.recommendation.value}: "
            f"{decision.readiness_score:.1f}/100 readiness, "
            f"{decision.blocking_issue_count} blockers, "
            f"{len(decision.workstreams)} workstreams."
        ),
        started_at=now,
        completed_at=now,
        human_review_required=(
            decision.human_approval_required
        ),
    )

    brain.add_agent_run(run)

    return run


def run_water_ppp_bid_agent(
    opportunity_id: str = "OPP-WATER-001",
    project_id: str = "DEMO-WATER-001",
    project_brain: ProjectBrain | None = None,
) -> BidDecision:
    """
    Deterministic Bid Agent demonstration for the synthetic
    Eastern Province Independent Water Project.

    The agent reasons over structured opportunity and tender
    intelligence. It does not approve the pursuit decision.

    When a Project Brain is supplied, the resulting issues,
    workstreams, recommendation, evidence relationships, and
    agent execution are persisted into shared project state.
    """

    factors = [
        _factor(
            factor_id="BID-FAC-001",
            name="Strategic fit",
            category="STRATEGY",
            score=94.0,
            weight=0.18,
            rationale=(
                "Water security infrastructure aligns strongly "
                "with the platform's demonstrated PPP thesis."
            ),
            evidence_ids=[],
        ),
        _factor(
            factor_id="BID-FAC-002",
            name="Sector fit",
            category="SECTOR",
            score=96.0,
            weight=0.14,
            rationale=(
                "The opportunity sits directly within water "
                "infrastructure and long-term concession delivery."
            ),
            evidence_ids=[],
        ),
        _factor(
            factor_id="BID-FAC-003",
            name="Commercial attractiveness",
            category="COMMERCIAL",
            score=86.0,
            weight=0.16,
            rationale=(
                "Availability-based payments provide attractive "
                "long-duration revenue visibility, subject to "
                "performance deductions."
            ),
            evidence_ids=[
                "EVD-019",
                "EVD-020",
            ],
        ),
        _factor(
            factor_id="BID-FAC-004",
            name="Financing readiness",
            category="FINANCIAL",
            score=72.0,
            weight=0.15,
            rationale=(
                "The project is financeable in structure, but "
                "minimum equity commitment, bid security and "
                "lender engagement require resolution."
            ),
            evidence_ids=[
                "EVD-005",
                "EVD-011",
            ],
        ),
        _factor(
            factor_id="BID-FAC-005",
            name="Delivery confidence",
            category="DELIVERY",
            score=68.0,
            weight=0.15,
            rationale=(
                "The 36-month COD obligation and long-lead "
                "equipment programme create material schedule "
                "execution pressure."
            ),
            evidence_ids=[
                "EVD-009",
                "EVD-016",
            ],
        ),
        _factor(
            factor_id="BID-FAC-006",
            name="Operating resilience",
            category="OPERATIONS",
            score=74.0,
            weight=0.12,
            rationale=(
                "The minimum annual availability requirement "
                "creates meaningful lifecycle performance risk."
            ),
            evidence_ids=[
                "EVD-007",
                "EVD-018",
            ],
        ),
        _factor(
            factor_id="BID-FAC-007",
            name="Risk-adjusted pursuit quality",
            category="RISK",
            score=70.0,
            weight=0.10,
            rationale=(
                "The opportunity remains attractive, but energy "
                "exposure, schedule obligations and security "
                "requirements must be actively mitigated."
            ),
            evidence_ids=[
                "EVD-008",
                "EVD-015",
                "EVD-017",
            ],
        ),
    ]

    issues = [
        _issue(
            issue_id="BID-ISS-001",
            title="USD 10 million bid security",
            description=(
                "The tender requires unconditional bid security "
                "valid beyond proposal submission."
            ),
            issue_type=BidIssueType.FINANCIAL,
            severity=BidIssueSeverity.HIGH,
            blocking=True,
            estimated_exposure_usd=10_000_000.0,
            owner="Finance",
            resolution_required=(
                "Confirm issuing bank, facility availability, "
                "pricing and internal approval."
            ),
            evidence_ids=["EVD-004"],
        ),
        _issue(
            issue_id="BID-ISS-002",
            title="Minimum equity commitment",
            description=(
                "The Project Company must maintain at least "
                "25 percent equity at Financial Close."
            ),
            issue_type=BidIssueType.FINANCIAL,
            severity=BidIssueSeverity.HIGH,
            blocking=True,
            owner="Investment",
            resolution_required=(
                "Validate sponsor equity capacity and target "
                "consortium capital structure."
            ),
            evidence_ids=["EVD-011"],
        ),
        _issue(
            issue_id="BID-ISS-003",
            title="36-month COD schedule",
            description=(
                "The delivery programme must support commercial "
                "operation within the contractual schedule."
            ),
            issue_type=BidIssueType.DELIVERY,
            severity=BidIssueSeverity.HIGH,
            blocking=False,
            estimated_exposure_usd=25_000_000.0,
            owner="Project Development",
            resolution_required=(
                "Run EPC schedule challenge and validate "
                "critical-path procurement assumptions."
            ),
            evidence_ids=[
                "EVD-009",
                "EVD-016",
            ],
        ),
        _issue(
            issue_id="BID-ISS-004",
            title="96 percent annual availability",
            description=(
                "Availability deductions may impair project "
                "economics if operational performance falls "
                "below the contractual threshold."
            ),
            issue_type=BidIssueType.OPERATIONS,
            severity=BidIssueSeverity.MEDIUM,
            blocking=False,
            owner="Operations",
            resolution_required=(
                "Model lifecycle availability, redundancy, "
                "maintenance and deduction scenarios."
            ),
            evidence_ids=[
                "EVD-007",
                "EVD-018",
            ],
        ),
        _issue(
            issue_id="BID-ISS-005",
            title="Residual energy-price exposure",
            description=(
                "Guaranteed energy consumption and residual "
                "energy-price allocation can materially change "
                "operating margins."
            ),
            issue_type=BidIssueType.COMMERCIAL,
            severity=BidIssueSeverity.HIGH,
            blocking=False,
            owner="Commercial",
            resolution_required=(
                "Confirm tariff indexation and energy-risk "
                "allocation before locking bid economics."
            ),
            evidence_ids=[
                "EVD-008",
                "EVD-017",
            ],
        ),
        _issue(
            issue_id="BID-ISS-006",
            title="Long-lead desalination equipment",
            description=(
                "Critical desalination and electrical equipment "
                "may constrain the construction schedule."
            ),
            issue_type=BidIssueType.PROCUREMENT,
            severity=BidIssueSeverity.MEDIUM,
            blocking=False,
            owner="EPC / Procurement",
            resolution_required=(
                "Identify critical packages, supplier lead "
                "times and early procurement requirements."
            ),
            evidence_ids=["EVD-009"],
        ),
    ]

    strengths = [
        BidStrength(
            strength_id="BID-STR-001",
            title="Strong strategic alignment",
            description=(
                "Water security and infrastructure PPP delivery "
                "fit the opportunity thesis strongly."
            ),
            score=95.0,
        ),
        BidStrength(
            strength_id="BID-STR-002",
            title="Long-duration contracted revenue",
            description=(
                "Availability-based revenue creates attractive "
                "long-term cash-flow visibility."
            ),
            score=90.0,
            evidence_ids=[
                "EVD-019",
                "EVD-020",
            ],
        ),
        BidStrength(
            strength_id="BID-STR-003",
            title="Material project scale",
            description=(
                "The project is sufficiently large to justify "
                "senior pursuit attention if key blockers clear."
            ),
            score=88.0,
        ),
    ]

    workstreams = [
        BidWorkstream(
            workstream_id="BID-WS-001",
            name="Financing and security",
            objective=(
                "Resolve bid security, equity commitment and "
                "lender-readiness requirements."
            ),
            owner="Finance / Investment",
            priority="IMMEDIATE",
            status="OPEN",
            dependencies=[
                "BID-ISS-001",
                "BID-ISS-002",
            ],
            evidence_ids=[
                "EVD-004",
                "EVD-011",
            ],
        ),
        BidWorkstream(
            workstream_id="BID-WS-002",
            name="EPC schedule challenge",
            objective=(
                "Validate whether procurement and construction "
                "can credibly achieve contractual COD."
            ),
            owner="Project Development / EPC",
            priority="IMMEDIATE",
            status="OPEN",
            dependencies=[
                "BID-ISS-003",
                "BID-ISS-006",
            ],
            evidence_ids=[
                "EVD-009",
                "EVD-016",
            ],
        ),
        BidWorkstream(
            workstream_id="BID-WS-003",
            name="Commercial risk allocation",
            objective=(
                "Resolve energy exposure and availability "
                "deduction assumptions before final pricing."
            ),
            owner="Commercial / Operations",
            priority="HIGH",
            status="OPEN",
            dependencies=[
                "BID-ISS-004",
                "BID-ISS-005",
            ],
            evidence_ids=[
                "EVD-007",
                "EVD-008",
                "EVD-017",
                "EVD-018",
            ],
        ),
        BidWorkstream(
            workstream_id="BID-WS-004",
            name="Authority clarifications",
            objective=(
                "Close material ambiguities identified by the "
                "Document Agent before bid commitment."
            ),
            owner="Bid Director",
            priority="HIGH",
            status="OPEN",
            dependencies=[
                "CLR-001",
                "CLR-002",
                "CLR-003",
                "CLR-004",
            ],
        ),
    ]

    readiness_score = calculate_readiness_score(
        factors
    )

    recommendation, readiness = (
        determine_recommendation(
            readiness_score,
            issues,
        )
    )

    unresolved_blockers = [
        issue.issue_id
        for issue in issues
        if issue.blocking
    ]

    evidence_ids = sorted({
        evidence_id
        for collection in (
            factors,
            issues,
            strengths,
            workstreams,
        )
        for record in collection
        for evidence_id in record.evidence_ids
    })

    decision = BidDecision(
        opportunity_id=opportunity_id,
        project_id=project_id,
        recommendation=recommendation,
        readiness=readiness,
        readiness_score=readiness_score,
        confidence=0.91,
        executive_thesis=(
            "Pursue the opportunity conditionally. Strategic "
            "and sector fit are strong, but Lamar should not "
            "commit full bid resources until financing security "
            "and minimum equity requirements are confirmed."
        ),
        decision_rationale=(
            "The project combines strong strategic alignment "
            "and contracted revenue visibility with manageable "
            "but material financing, schedule, energy and "
            "operating risks. The current decision is therefore "
            "a gated pursuit rather than an unconditional bid."
        ),
        factors=factors,
        strengths=strengths,
        issues=issues,
        workstreams=workstreams,
        unresolved_blockers=unresolved_blockers,
        clarification_ids=[
            "CLR-001",
            "CLR-002",
            "CLR-003",
            "CLR-004",
        ],
        evidence_ids=evidence_ids,
        human_approval_required=True,
        approved=False,
    )

    if project_brain is not None:
        write_bid_decision_to_project_brain(
            decision=decision,
            brain=project_brain,
        )

    return decision
