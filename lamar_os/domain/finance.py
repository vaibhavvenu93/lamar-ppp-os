"""
Financial domain models for Lamar PPP OS.

These models represent the capital structure, operating assumptions,
and calculated financial outputs of a PPP infrastructure project.

Financial calculations are performed deterministically by dedicated
engines rather than by language models.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CapitalStructure:
    """Debt and equity structure used to finance a PPP project."""

    total_capex_usd: float
    debt_ratio: float
    equity_ratio: float
    interest_rate: float
    debt_tenor_years: int

    def validate(self) -> None:
        """Validate basic capital structure assumptions."""

        if abs((self.debt_ratio + self.equity_ratio) - 1.0) > 0.0001:
            raise ValueError("Debt ratio and equity ratio must sum to 1.0")

        if self.total_capex_usd <= 0:
            raise ValueError("Total CAPEX must be greater than zero")

        if not 0 <= self.interest_rate <= 1:
            raise ValueError("Interest rate must be expressed as a decimal")


@dataclass
class OperatingAssumptions:
    """Operating assumptions for the project concession period."""

    concession_years: int
    annual_revenue_usd: float
    annual_opex_usd: float

    revenue_growth_rate: float = 0.0
    opex_growth_rate: float = 0.0
    tax_rate: float = 0.0


@dataclass
class FinancialAssumptions:
    """Complete financial assumptions for a PPP project."""

    project_id: str
    capital: CapitalStructure
    operations: OperatingAssumptions

    construction_years: int = 2
    discount_rate: float = 0.10

    is_synthetic: bool = True
    assumption_note: Optional[str] = None


@dataclass
class AnnualCashFlow:
    """Calculated financial performance for a single project year."""

    year: int

    revenue_usd: float = 0.0
    opex_usd: float = 0.0

    operating_cash_flow_usd: float = 0.0

    debt_service_usd: float = 0.0
    equity_cash_flow_usd: float = 0.0

    dscr: Optional[float] = None


@dataclass
class FinancialResults:
    """Calculated outputs produced by the financial engine."""

    project_id: str

    debt_amount_usd: float
    equity_amount_usd: float

    project_npv_usd: Optional[float] = None
    equity_irr: Optional[float] = None
    minimum_dscr: Optional[float] = None
    average_dscr: Optional[float] = None

    annual_cash_flows: List[AnnualCashFlow] = field(default_factory=list)
