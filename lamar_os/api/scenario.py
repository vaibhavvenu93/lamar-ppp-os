"""
Financial scenario API models for Lamar PPP OS.

These models define the contract between the executive interface
and the deterministic PPP Financial Twin.
"""

from pydantic import BaseModel, Field


class ScenarioRequest(BaseModel):
    """
    User-controlled assumptions for a Financial Twin scenario.
    """

    name: str = "Executive downside scenario"

    capex_change_pct: float = Field(
        default=0.0,
        ge=-0.50,
        le=1.00,
        description=(
            "Percentage change to total project CAPEX. "
            "Example: 0.10 represents a 10% increase."
        ),
    )

    revenue_change_pct: float = Field(
        default=0.0,
        ge=-0.50,
        le=0.50,
        description=(
            "Percentage change to annual project revenue."
        ),
    )

    opex_change_pct: float = Field(
        default=0.0,
        ge=-0.50,
        le=1.00,
        description=(
            "Percentage change to annual operating expenditure."
        ),
    )

    interest_rate_change_pct: float = Field(
        default=0.0,
        ge=-0.05,
        le=0.10,
        description=(
            "Absolute change to the debt interest rate. "
            "Example: 0.01 represents +1 percentage point."
        ),
    )


class ScenarioMetrics(BaseModel):
    """Financial outputs for one scenario state."""

    equity_irr: float | None
    project_npv_usd: float | None
    minimum_dscr: float | None


class ScenarioResponse(BaseModel):
    """
    Comparison returned by the deterministic Financial Twin.
    """

    scenario_name: str

    base: ScenarioMetrics
    scenario: ScenarioMetrics

    equity_irr_change: float | None
    project_npv_change_usd: float | None
    minimum_dscr_change: float | None

    calculation_engine: str = (
        "Lamar PPP OS deterministic Financial Twin"
    )

    data_notice: str = (
        "Synthetic project assumptions only."
    )

    human_decision_required: bool = True
