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
from lamar_os.engines.executive_adapter import (
    risk_financial_impact_to_signal,
)
from lamar_os.engines.executive_engine import (
    ExecutivePriority,
    ExecutiveSignalType,
)
from lamar_os.engines.risk_financial_engine import (
    assess_financial_risk,
)


def build_demo_assumptions() -> FinancialAssumptions:
    """Create synthetic financial assumptions for integration testing."""

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
    )


def build_demo_risk() -> ProjectRisk:
    """Create a synthetic construction risk."""

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
        mitigation=(
            "Review EPC protections and contingency strategy."
        ),
    )


def build_executive_signal():
    """Run the complete risk-to-executive intelligence chain."""

    assumptions = build_demo_assumptions()
    risk = build_demo_risk()

    impact = assess_financial_risk(
        risk=risk,
        assumptions=assumptions,
    )

    return risk_financial_impact_to_signal(impact)


def test_risk_becomes_executive_signal():
    signal = build_executive_signal()

    assert signal.signal_id == "EXEC-RISK-CONSTRUCTION-001"
    assert signal.signal_type == ExecutiveSignalType.RISK
    assert signal.priority == ExecutivePriority.HIGH


def test_expected_loss_flows_into_executive_signal():
    signal = build_executive_signal()

    assert signal.financial_exposure_usd == pytest.approx(
        12_000_000
    )

    assert "$12,000,000" in signal.summary


def test_financial_twin_impact_appears_in_summary():
    signal = build_executive_signal()

    assert "Modeled equity IRR change:" in signal.summary
    assert "Modeled project NPV change:" in signal.summary


def test_executive_decision_flag_flows_from_risk_engine():
    signal = build_executive_signal()

    assert signal.requires_decision is True


def test_mitigation_becomes_recommended_action():
    signal = build_executive_signal()

    assert signal.recommended_action == (
        "Review EPC protections and contingency strategy."
    )


def test_financial_translation_is_preserved():
    signal = build_executive_signal()

    assert signal.source_reference is not None
    assert "$30,000,000" in signal.source_reference
    assert "4.29%" in signal.source_reference
