import pytest

from lamar_os.domain.risk import (
    ProjectRisk,
    RiskAllocation,
    RiskCategory,
    RiskSeverity,
)
from lamar_os.engines.risk_engine import (
    assess_risk,
    calculate_expected_loss,
    calculate_risk_score,
)


def build_construction_risk() -> ProjectRisk:
    """Create a synthetic construction risk for testing."""

    return ProjectRisk(
        risk_id="RISK-CONSTRUCTION-001",
        project_id="DEMO-WATER-001",
        title="Construction Cost Overrun",
        description=(
            "Potential construction cost overrun caused by "
            "schedule delay and procurement pressure."
        ),
        category=RiskCategory.CONSTRUCTION,
        allocation=RiskAllocation.PRIVATE,
        severity=RiskSeverity.HIGH,
        probability=0.40,
        estimated_impact_usd=30_000_000,
        owner="Project Company",
        mitigation=(
            "Review EPC protections, contingency reserves, "
            "procurement exposure, and schedule controls."
        ),
    )


def test_expected_loss_is_probability_weighted():
    risk = build_construction_risk()

    expected_loss = calculate_expected_loss(risk)

    assert expected_loss == pytest.approx(
        12_000_000
    )


def test_high_risk_receives_normalized_score():
    risk = build_construction_risk()

    score = calculate_risk_score(risk)

    assert score == pytest.approx(
        0.30
    )


def test_12m_expected_loss_requires_executive_attention():
    risk = build_construction_risk()

    assessment = assess_risk(risk)

    assert assessment.executive_attention is True
    assert assessment.expected_loss_usd == pytest.approx(
        12_000_000
    )
    assert "$10M" in assessment.attention_reason


def test_low_exposure_risk_is_not_escalated():
    risk = ProjectRisk(
        risk_id="RISK-LOW-001",
        project_id="DEMO-WATER-001",
        title="Minor Operating Variance",
        description="Small operational variance.",
        category=RiskCategory.OPERATIONS,
        allocation=RiskAllocation.PRIVATE,
        severity=RiskSeverity.LOW,
        probability=0.20,
        estimated_impact_usd=500_000,
    )

    assessment = assess_risk(risk)

    assert assessment.executive_attention is False
    assert assessment.expected_loss_usd == pytest.approx(
        100_000
    )


def test_invalid_probability_is_rejected():
    risk = build_construction_risk()

    risk.probability = 1.20

    with pytest.raises(ValueError):
        assess_risk(risk)


def test_critical_risk_is_always_escalated():
    risk = ProjectRisk(
        risk_id="RISK-CRITICAL-001",
        project_id="DEMO-WATER-001",
        title="Critical Counterparty Failure",
        description=(
            "Potential failure of a critical project counterparty."
        ),
        category=RiskCategory.COUNTERPARTY,
        allocation=RiskAllocation.SHARED,
        severity=RiskSeverity.CRITICAL,
        probability=0.05,
        estimated_impact_usd=1_000_000,
    )

    assessment = assess_risk(risk)

    assert assessment.executive_attention is True
    assert assessment.attention_reason == (
        "Risk severity is CRITICAL."
    )
