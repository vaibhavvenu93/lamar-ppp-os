"""
Scenario analysis engine for Lamar PPP OS.

This engine applies controlled changes to project assumptions and
compares the resulting financial performance against a base case.

Scenario calculations remain deterministic.
"""

from copy import deepcopy
from dataclasses import dataclass
from typing import Optional

from lamar_os.domain.finance import (
    FinancialAssumptions,
    FinancialResults,
)
from lamar_os.engines.financial_engine import calculate_financials


@dataclass
class Scenario:
    """A controlled set of changes applied to financial assumptions."""

    name: str
    description: str

    capex_change_pct: float = 0.0
    revenue_change_pct: float = 0.0
    opex_change_pct: float = 0.0
    interest_rate_change_pct: float = 0.0


@dataclass
class ScenarioComparison:
    """Comparison between base-case and scenario financial results."""

    scenario: Scenario

    base_results: FinancialResults
    scenario_results: FinancialResults

    equity_irr_change: Optional[float]
    project_npv_change_usd: Optional[float]
    minimum_dscr_change: Optional[float]


def _difference(
    scenario_value: Optional[float],
    base_value: Optional[float],
) -> Optional[float]:
    """Return the difference between two optional numeric values."""

    if scenario_value is None or base_value is None:
        return None

    return scenario_value - base_value


def run_scenario(
    assumptions: FinancialAssumptions,
    scenario: Scenario,
) -> ScenarioComparison:
    """
    Run a financial scenario against a project's base assumptions.

    A deep copy is used so scenario analysis never mutates the
    original project assumptions.
    """

    base_results = calculate_financials(assumptions)

    stressed = deepcopy(assumptions)

    stressed.capital.total_capex_usd *= (
        1 + scenario.capex_change_pct
    )

    stressed.operations.annual_revenue_usd *= (
        1 + scenario.revenue_change_pct
    )

    stressed.operations.annual_opex_usd *= (
        1 + scenario.opex_change_pct
    )

    stressed.capital.interest_rate += (
        scenario.interest_rate_change_pct
    )

    scenario_results = calculate_financials(stressed)

    return ScenarioComparison(
        scenario=scenario,
        base_results=base_results,
        scenario_results=scenario_results,
        equity_irr_change=_difference(
            scenario_results.equity_irr,
            base_results.equity_irr,
        ),
        project_npv_change_usd=_difference(
            scenario_results.project_npv_usd,
            base_results.project_npv_usd,
        ),
        minimum_dscr_change=_difference(
            scenario_results.minimum_dscr,
            base_results.minimum_dscr,
        ),
    )
