import pytest

from lamar_os.domain.finance import (
    CapitalStructure,
    FinancialAssumptions,
    OperatingAssumptions,
)
from lamar_os.domain.risk import (
    ProjectRisk,
    RiskAllocation,
    RiskCategory,
    RiskSeverity,
)
from lamar_os.engines.risk_financial_engine import (
    assess_financial_risk,
)


def build_demo_assumptions() -> FinancialAssumptions:
    """Create synthetic PPP assumptions for integrated risk testing."""

    return FinancialAssumptions(
        project_id="DEMO-WATER-001",
        capital=CapitalStructure(
            total_capex_usd=700_000_000,
            debt_ratio=0.70,
            equity_ratio=0.30,
            interest_rate=0.065,
            debt_tenor_years=15,
        ),
        operations=OperatingAssumptions(
            concession_years=20,
            annual_revenue_usd=110_000_000,
            annual_opex_usd=30_000_000,
            revenue_growth_rate=0.02,
            opex_growth_rate=0.02,
        ),
        construction_years=3,
        discount_rate=0.10,
        is_synthetic=True,
        assumption_note=(
            "Synthetic assumptions used for integrated testing."
        ),
    )


def build_construction_risk() -> ProjectRisk:
    """Create a quantified synthetic construction risk."""

    return ProjectRisk(
        risk_id="RISK-CONSTRUCTION-001",
        project_id="DEMO-WATER-001",
        title="Construction Cost Overrun",
        description=(
            "Potential $30M construction cost overrun."
        ),
        category=RiskCategory.CONSTRUCTION,
        allocation=RiskAllocation.PRIVATE,
        severity=RiskSeverity.HIGH,
        probability=0.40,
        estimated_impact_usd=30_000_000,
        owner="Project Company",
    )


def test_construction_risk_becomes_capex_scenario():
    assumptions = build_demo_assumptions()
    risk = build_construction_risk()

    result = assess_financial_risk(
        risk=risk,
        assumptions=assumptions,
    )

    assert result.scenario_comparison is not None

    scenario = result.scenario_comparison.scenario

    assert scenario.capex_change_pct == pytest.approx(
        30_000_000 / 700_000_000
    )

    assert scenario.capex_change_pct == pytest.approx(
        0.04285714285714286
    )


def test_construction_risk_reduces_equity_irr():
    assumptions = build_demo_assumptions()
    risk = build_construction_risk()

    result = assess_financial_risk(
        risk=risk,
        assumptions=assumptions,
    )

    comparison = result.scenario_comparison

    assert comparison is not None
    assert comparison.base_results.equity_irr is not None
    assert comparison.scenario_results.equity_irr is not None

    assert (
        comparison.scenario_results.equity_irr
        < comparison.base_results.equity_irr
    )


def test_construction_risk_reduces_project_npv():
    assumptions = build_demo_assumptions()
    risk = build_construction_risk()

    result = assess_financial_risk(
        risk=risk,
        assumptions=assumptions,
    )

    comparison = result.scenario_comparison

    assert comparison is not None
    assert comparison.project_npv_change_usd is not None
    assert comparison.project_npv_change_usd < 0


def test_construction_risk_is_escalated():
    assumptions = build_demo_assumptions()
    risk = build_construction_risk()

    result = assess_financial_risk(
        risk=risk,
        assumptions=assumptions,
    )

    assert result.risk_assessment.expected_loss_usd == (
        pytest.approx(12_000_000)
    )

    assert (
        result.risk_assessment.executive_attention
        is True
    )


def test_financial_translation_is_explainable():
    assumptions = build_demo_assumptions()
    risk = build_construction_risk()

    result = assess_financial_risk(
        risk=risk,
        assumptions=assumptions,
    )

    assert result.financial_translation is not None
    assert "$30,000,000" in result.financial_translation
    assert "4.29%" in result.financial_translation


def test_unsupported_risk_is_not_force_modeled():
    assumptions = build_demo_assumptions()

    risk = ProjectRisk(
        risk_id="RISK-REGULATORY-001",
        project_id="DEMO-WATER-001",
        title="Regulatory Change",
        description=(
            "Potential regulatory change with uncertain "
            "financial transmission."
        ),
        category=RiskCategory.REGULATORY,
        allocation=RiskAllocation.SHARED,
        severity=RiskSeverity.HIGH,
        probability=0.30,
        estimated_impact_usd=20_000_000,
    )

    result = assess_financial_risk(
        risk=risk,
        assumptions=assumptions,
    )

    assert result.scenario_comparison is None

    assert result.financial_translation == (
        "Risk category is not yet mapped to an automatic "
        "Financial Twin scenario."
    )
