from lamar_os.domain.finance import (
    CapitalStructure,
    FinancialAssumptions,
    OperatingAssumptions,
)
from lamar_os.engines.scenario_engine import (
    Scenario,
    run_scenario,
)


def build_demo_assumptions() -> FinancialAssumptions:
    """Create synthetic PPP assumptions for scenario testing."""

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
            "Synthetic assumptions used only for scenario testing."
        ),
    )


def test_capex_overrun_reduces_equity_irr():
    assumptions = build_demo_assumptions()

    scenario = Scenario(
        name="8% CAPEX Overrun",
        description=(
            "Test the impact of an 8% construction cost overrun."
        ),
        capex_change_pct=0.08,
    )

    comparison = run_scenario(
        assumptions,
        scenario,
    )

    assert comparison.base_results.equity_irr is not None
    assert comparison.scenario_results.equity_irr is not None

    assert (
        comparison.scenario_results.equity_irr
        < comparison.base_results.equity_irr
    )

    assert comparison.equity_irr_change is not None
    assert comparison.equity_irr_change < 0


def test_capex_overrun_reduces_project_npv():
    assumptions = build_demo_assumptions()

    scenario = Scenario(
        name="8% CAPEX Overrun",
        description="Construction cost stress test.",
        capex_change_pct=0.08,
    )

    comparison = run_scenario(
        assumptions,
        scenario,
    )

    assert comparison.project_npv_change_usd is not None
    assert comparison.project_npv_change_usd < 0


def test_revenue_reduction_hurts_dscr():
    assumptions = build_demo_assumptions()

    scenario = Scenario(
        name="10% Revenue Downside",
        description=(
            "Test the impact of annual revenue being 10% lower."
        ),
        revenue_change_pct=-0.10,
    )

    comparison = run_scenario(
        assumptions,
        scenario,
    )

    assert comparison.minimum_dscr_change is not None
    assert comparison.minimum_dscr_change < 0


def test_scenario_does_not_mutate_base_assumptions():
    assumptions = build_demo_assumptions()

    original_capex = assumptions.capital.total_capex_usd

    scenario = Scenario(
        name="CAPEX Stress",
        description="Test assumption isolation.",
        capex_change_pct=0.08,
    )

    run_scenario(
        assumptions,
        scenario,
    )

    assert assumptions.capital.total_capex_usd == original_capex
