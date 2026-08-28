import pytest

from lamar_os.engines.executive_engine import (
    ExecutivePriority,
    ExecutiveSignal,
    ExecutiveSignalType,
    build_executive_brief,
    calculate_attention_score,
)


def build_demo_signals() -> list[ExecutiveSignal]:
    """Create synthetic signals competing for executive attention."""

    return [
        ExecutiveSignal(
            signal_id="SIG-RISK-001",
            project_id="DEMO-WATER-001",
            title="Construction Cost Overrun",
            summary=(
                "Potential construction cost overrun requires "
                "executive review."
            ),
            signal_type=ExecutiveSignalType.RISK,
            priority=ExecutivePriority.HIGH,
            financial_exposure_usd=30_000_000,
            requires_decision=True,
            recommended_action=(
                "Review EPC protections and contingency strategy."
            ),
        ),
        ExecutiveSignal(
            signal_id="SIG-OBLIGATION-001",
            project_id="DEMO-WATER-001",
            title="Bid Submission Deadline",
            summary=(
                "Consortium submission package is approaching "
                "its deadline."
            ),
            signal_type=ExecutiveSignalType.OBLIGATION,
            priority=ExecutivePriority.HIGH,
            days_to_deadline=3,
            requires_decision=True,
            recommended_action=(
                "Confirm final consortium submission approval."
            ),
        ),
        ExecutiveSignal(
            signal_id="SIG-OPPORTUNITY-001",
            project_id="DEMO-WATER-002",
            title="New Water PPP Opportunity",
            summary=(
                "New infrastructure opportunity requires "
                "a bid or no-bid decision."
            ),
            signal_type=ExecutiveSignalType.OPPORTUNITY,
            priority=ExecutivePriority.MEDIUM,
            requires_decision=True,
            recommended_action=(
                "Review strategic fit and consortium requirements."
            ),
        ),
        ExecutiveSignal(
            signal_id="SIG-OPS-001",
            project_id="DEMO-WATER-001",
            title="Routine Operating Variance",
            summary="Minor operating variance detected.",
            signal_type=ExecutiveSignalType.OPERATIONS,
            priority=ExecutivePriority.LOW,
            financial_exposure_usd=200_000,
        ),
        ExecutiveSignal(
            signal_id="SIG-FINANCE-001",
            project_id="DEMO-WATER-001",
            title="Financing Covenant Watch",
            summary=(
                "Debt-service coverage requires monitoring."
            ),
            signal_type=ExecutiveSignalType.FINANCIAL,
            priority=ExecutivePriority.MEDIUM,
            financial_exposure_usd=2_000_000,
            days_to_deadline=14,
        ),
    ]


def test_high_exposure_decision_receives_high_score():
    signal = build_demo_signals()[0]

    score = calculate_attention_score(signal)

    assert score == pytest.approx(70.0)


def test_executive_brief_returns_only_top_three():
    signals = build_demo_signals()

    brief = build_executive_brief(
        signals=signals,
        top_n=3,
    )

    assert len(brief.top_signals) == 3
    assert brief.total_signals_reviewed == 5


def test_construction_risk_ranks_first():
    signals = build_demo_signals()

    brief = build_executive_brief(signals)

    assert (
        brief.top_signals[0].signal.signal_id
        == "SIG-RISK-001"
    )

    assert (
        brief.top_signals[0].signal.title
        == "Construction Cost Overrun"
    )


def test_routine_noise_is_excluded_from_top_three():
    signals = build_demo_signals()

    brief = build_executive_brief(signals)

    top_ids = {
        item.signal.signal_id
        for item in brief.top_signals
    }

    assert "SIG-OPS-001" not in top_ids


def test_ranking_reason_is_explainable():
    signals = build_demo_signals()

    brief = build_executive_brief(signals)

    top_item = brief.top_signals[0]

    assert "HIGH priority" in top_item.ranking_reason
    assert "$30,000,000 financial exposure" in (
        top_item.ranking_reason
    )
    assert "executive decision required" in (
        top_item.ranking_reason
    )


def test_invalid_top_n_is_rejected():
    signals = build_demo_signals()

    with pytest.raises(ValueError):
        build_executive_brief(
            signals=signals,
            top_n=0,
        )
