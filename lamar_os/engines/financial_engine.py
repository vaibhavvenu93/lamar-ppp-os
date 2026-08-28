"""
Deterministic PPP financial engine for Lamar PPP OS.

The engine converts structured project assumptions into financial
outputs including debt service, DSCR, NPV, and equity IRR.

Language models do not perform these calculations.
"""

from typing import List

from lamar_os.domain.finance import (
    AnnualCashFlow,
    FinancialAssumptions,
    FinancialResults,
)


def _annual_debt_service(
    principal: float,
    annual_rate: float,
    tenor_years: int,
) -> float:
    """Calculate level annual debt service using an annuity structure."""

    if principal <= 0:
        return 0.0

    if tenor_years <= 0:
        raise ValueError("Debt tenor must be greater than zero")

    if annual_rate == 0:
        return principal / tenor_years

    factor = (1 + annual_rate) ** tenor_years

    return principal * (
        annual_rate * factor
    ) / (
        factor - 1
    )


def _npv(
    cash_flows: List[float],
    discount_rate: float,
) -> float:
    """Calculate net present value of a cash-flow series."""

    return sum(
        cash_flow / ((1 + discount_rate) ** year)
        for year, cash_flow in enumerate(cash_flows)
    )


def _irr(
    cash_flows: List[float],
    tolerance: float = 1e-7,
    max_iterations: int = 500,
) -> float | None:
    """
    Estimate IRR using bisection.

    Returns None when a meaningful IRR cannot be found inside
    the supported search interval.
    """

    if not cash_flows:
        return None

    if not any(value < 0 for value in cash_flows):
        return None

    if not any(value > 0 for value in cash_flows):
        return None

    lower = -0.9999
    upper = 10.0

    lower_npv = _npv(cash_flows, lower)
    upper_npv = _npv(cash_flows, upper)

    if lower_npv * upper_npv > 0:
        return None

    for _ in range(max_iterations):
        midpoint = (lower + upper) / 2
        midpoint_npv = _npv(cash_flows, midpoint)

        if abs(midpoint_npv) < tolerance:
            return midpoint

        if lower_npv * midpoint_npv <= 0:
            upper = midpoint
        else:
            lower = midpoint
            lower_npv = midpoint_npv

    return (lower + upper) / 2


def calculate_financials(
    assumptions: FinancialAssumptions,
) -> FinancialResults:
    """
    Calculate deterministic financial outputs for a PPP project.

    This is intentionally a simplified v0.1 project-finance model.
    It is designed to establish an auditable calculation layer
    before more advanced financing mechanics are introduced.
    """

    assumptions.capital.validate()

    capital = assumptions.capital
    operations = assumptions.operations

    if operations.concession_years <= 0:
        raise ValueError("Concession period must be greater than zero")

    if assumptions.discount_rate <= -1:
        raise ValueError("Discount rate must be greater than -100%")

    debt_amount = capital.total_capex_usd * capital.debt_ratio
    equity_amount = capital.total_capex_usd * capital.equity_ratio

    annual_debt_service = _annual_debt_service(
        principal=debt_amount,
        annual_rate=capital.interest_rate,
        tenor_years=capital.debt_tenor_years,
    )

    annual_cash_flows: List[AnnualCashFlow] = []

    project_cash_flows: List[float] = [-capital.total_capex_usd]
    equity_cash_flows: List[float] = [-equity_amount]

    dscr_values: List[float] = []

    for year in range(1, operations.concession_years + 1):
        revenue = operations.annual_revenue_usd * (
            (1 + operations.revenue_growth_rate) ** (year - 1)
        )

        opex = operations.annual_opex_usd * (
            (1 + operations.opex_growth_rate) ** (year - 1)
        )

        operating_cash_flow = revenue - opex

        debt_service = (
            annual_debt_service
            if year <= capital.debt_tenor_years
            else 0.0
        )

        dscr = (
            operating_cash_flow / debt_service
            if debt_service > 0
            else None
        )

        equity_cash_flow = operating_cash_flow - debt_service

        annual_cash_flows.append(
            AnnualCashFlow(
                year=year,
                revenue_usd=revenue,
                opex_usd=opex,
                operating_cash_flow_usd=operating_cash_flow,
                debt_service_usd=debt_service,
                equity_cash_flow_usd=equity_cash_flow,
                dscr=dscr,
            )
        )

        project_cash_flows.append(operating_cash_flow)
        equity_cash_flows.append(equity_cash_flow)

        if dscr is not None:
            dscr_values.append(dscr)

    project_npv = _npv(
        project_cash_flows,
        assumptions.discount_rate,
    )

    equity_irr = _irr(equity_cash_flows)

    minimum_dscr = min(dscr_values) if dscr_values else None

    average_dscr = (
        sum(dscr_values) / len(dscr_values)
        if dscr_values
        else None
    )

    return FinancialResults(
        project_id=assumptions.project_id,
        debt_amount_usd=debt_amount,
        equity_amount_usd=equity_amount,
        project_npv_usd=project_npv,
        equity_irr=equity_irr,
        minimum_dscr=minimum_dscr,
        average_dscr=average_dscr,
        annual_cash_flows=annual_cash_flows,
    )
