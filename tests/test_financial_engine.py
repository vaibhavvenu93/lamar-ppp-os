import pytest

from lamar_os.domain.finance import (
    CapitalStructure,
    FinancialAssumptions,
    OperatingAssumptions,
)
from lamar_os.engines.financial_engine import calculate_financials


def build_demo_assumptions() -> FinancialAssumptions:
    """Create synthetic assumptions for testing the financial engine."""

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
            "Synthetic PPP assumptions used only for testing."
        ),
    )


def test_capital_structure_is_calculated_correctly():
    assumptions = build_demo_assumptions()

    results = calculate_financials(assumptions)

    assert results.debt_amount_usd == pytest.approx(
        490_000_000
    )
    assert results.equity_amount_usd == pytest.approx(
        210_000_000
    )


def test_engine_generates_full_concession_cash_flows():
    assumptions = build_demo_assumptions()

    results = calculate_financials(assumptions)

    assert len(results.annual_cash_flows) == 20
    assert results.annual_cash_flows[0].year == 1
    assert results.annual_cash_flows[-1].year == 20


def test_dscr_is_calculated_during_debt_tenor():
    assumptions = build_demo_assumptions()

    results = calculate_financials(assumptions)

    assert results.minimum_dscr is not None
    assert results.average_dscr is not None
    assert results.minimum_dscr > 1.0


def test_equity_irr_is_calculated():
    assumptions = build_demo_assumptions()

    results = calculate_financials(assumptions)

    assert results.equity_irr is not None
    assert results.equity_irr > 0


def test_invalid_capital_structure_is_rejected():
    assumptions = build_demo_assumptions()

    assumptions.capital.debt_ratio = 0.80
    assumptions.capital.equity_ratio = 0.30

    with pytest.raises(ValueError):
        calculate_financials(assumptions)
