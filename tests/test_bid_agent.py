from lamar_os.domain.bid import (
    BidIssue,
    BidIssueSeverity,
    BidIssueType,
    BidReadiness,
    BidRecommendation,
)
from lamar_os.engines.bid_agent import (
    determine_recommendation,
    run_water_ppp_bid_agent,
)


def test_water_ppp_bid_agent_returns_expected_project():
    decision = run_water_ppp_bid_agent()

    assert decision.opportunity_id == "OPP-WATER-001"
    assert decision.project_id == "DEMO-WATER-001"


def test_water_ppp_is_conditional_pursue():
    decision = run_water_ppp_bid_agent()

    assert (
        decision.recommendation
        == BidRecommendation.CONDITIONAL_PURSUE
    )
    assert (
        decision.readiness
        == BidReadiness.CONDITIONAL
    )


def test_bid_readiness_score_is_deterministic():
    decision = run_water_ppp_bid_agent()

    assert decision.readiness_score == 81.9


def test_bid_agent_identifies_financing_blockers():
    decision = run_water_ppp_bid_agent()

    assert decision.blocking_issue_count == 2

    assert "BID-ISS-001" in decision.unresolved_blockers
    assert "BID-ISS-002" in decision.unresolved_blockers


def test_bid_agent_quantifies_known_exposure():
    decision = run_water_ppp_bid_agent()

    assert (
        decision.total_estimated_exposure_usd
        == 35_000_000.0
    )


def test_bid_agent_preserves_evidence_traceability():
    decision = run_water_ppp_bid_agent()

    assert "EVD-004" in decision.evidence_ids
    assert "EVD-011" in decision.evidence_ids
    assert "EVD-009" in decision.evidence_ids
    assert len(decision.evidence_ids) > 0


def test_bid_agent_creates_execution_workstreams():
    decision = run_water_ppp_bid_agent()

    workstream_ids = {
        workstream.workstream_id
        for workstream in decision.workstreams
    }

    assert "BID-WS-001" in workstream_ids
    assert "BID-WS-002" in workstream_ids
    assert "BID-WS-003" in workstream_ids
    assert "BID-WS-004" in workstream_ids


def test_bid_agent_never_auto_approves():
    decision = run_water_ppp_bid_agent()

    assert decision.human_approval_required is True
    assert decision.approved is False
    assert decision.can_auto_approve is False


def test_critical_blockers_force_no_bid():
    issues = [
        BidIssue(
            issue_id="TEST-001",
            title="Critical blocker one",
            description="Synthetic test blocker.",
            issue_type=BidIssueType.FINANCIAL,
            severity=BidIssueSeverity.CRITICAL,
            blocking=True,
        ),
        BidIssue(
            issue_id="TEST-002",
            title="Critical blocker two",
            description="Synthetic test blocker.",
            issue_type=BidIssueType.DELIVERY,
            severity=BidIssueSeverity.CRITICAL,
            blocking=True,
        ),
    ]

    recommendation, readiness = determine_recommendation(
        readiness_score=95.0,
        issues=issues,
    )

    assert recommendation == BidRecommendation.NO_BID
    assert readiness == BidReadiness.NOT_READY


def test_single_critical_blocker_forces_hold():
    issues = [
        BidIssue(
            issue_id="TEST-003",
            title="Critical blocker",
            description="Synthetic test blocker.",
            issue_type=BidIssueType.CONTRACTUAL,
            severity=BidIssueSeverity.CRITICAL,
            blocking=True,
        ),
    ]

    recommendation, readiness = determine_recommendation(
        readiness_score=92.0,
        issues=issues,
    )

    assert recommendation == BidRecommendation.HOLD
    assert readiness == BidReadiness.NOT_READY
