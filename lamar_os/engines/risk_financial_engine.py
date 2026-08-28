"""
Risk-to-financial-impact engine for Lamar PPP OS.

This module connects structured PPP risks to the Financial Twin.

A project risk can therefore be evaluated not only by severity
and expected loss, but also by its modeled effect on project
returns and debt-service capacity.
"""

from dataclasses import dataclass
from typing import Optional

from lamar_os.domain.finance import FinancialAssumptions
from lamar_os.domain.risk import (
    ProjectRisk,
    RiskCategory,
)
from lamar_os.engines.risk_engine import (
    RiskAssessment,
    assess_risk,
)
from lamar_os.engines.scenario_engine import (
    Scenario,
    ScenarioComparison,
    run_scenario,
)


@dataclass
class RiskFinancialImpact:
    """
    Combined risk and financial assessment.

    This object connects risk governance with modeled project
    economics while preserving both calculations separately.
    """

    risk_assessment: RiskAssessment
    scenario_comparison: Optional[ScenarioComparison]

    financial_translation: Optional[str]


def _translate_risk_to_scenario(
    risk: ProjectRisk,
    assumptions: FinancialAssumptions,
) -> tuple[Optional[Scenario], Optional[str]]:
    """
    Translate supported project risks into financial scenarios.

    Translation rules are explicit and deterministic rather than
    inferred silently by a language model.
    """

    if risk.estimated_impact_usd is None:
        return (
            None,
            "Risk has no quantified financial impact.",
        )

    if risk.estimated_impact_usd < 0:
        raise ValueError(
            "Estimated financial impact cannot be negative"
        )

    if risk.category == RiskCategory.CONSTRUCTION:
        base_capex = assumptions.capital.total_capex_usd

        if base_capex <= 0:
            raise ValueError(
                "Project CAPEX must be greater than zero"
            )

        capex_change_pct = (
            risk.estimated_impact_usd / base_capex
        )

        return (
            Scenario(
                name=f"Risk Scenario: {risk.title}",
                description=(
                    "Translate construction risk financial impact "
                    "into an equivalent CAPEX increase."
                ),
                capex_change_pct=capex_change_pct,
            ),
            (
                f"${risk.estimated_impact_usd:,.0f} construction "
                "impact modeled as a "
                f"{capex_change_pct:.2%} CAPEX increase."
            ),
        )

    if risk.category == RiskCategory.REVENUE:
        base_revenue = (
            assumptions.operations.annual_revenue_usd
        )

        if base_revenue <= 0:
            raise ValueError(
                "Annual project revenue must be greater than zero"
            )

        revenue_change_pct = -(
            risk.estimated_impact_usd / base_revenue
        )

        return (
            Scenario(
                name=f"Risk Scenario: {risk.title}",
                description=(
                    "Translate revenue risk financial impact "
                    "into an equivalent annual revenue reduction."
                ),
                revenue_change_pct=revenue_change_pct,
            ),
            (
                f"${risk.estimated_impact_usd:,.0f} revenue "
                "impact modeled as a "
                f"{abs(revenue_change_pct):.2%} "
                "annual revenue reduction."
            ),
        )

    return (
        None,
        (
            "Risk category is not yet mapped to an automatic "
            "Financial Twin scenario."
        ),
    )


def assess_financial_risk(
    risk: ProjectRisk,
    assumptions: FinancialAssumptions,
) -> RiskFinancialImpact:
    """
    Evaluate a project risk and model its financial consequence.

    Unsupported risk categories remain valid risk assessments but
    are not converted into financial scenarios automatically.
    """

    risk_assessment = assess_risk(risk)

    scenario, translation = _translate_risk_to_scenario(
        risk=risk,
        assumptions=assumptions,
    )

    scenario_comparison = (
        run_scenario(
            assumptions=assumptions,
            scenario=scenario,
        )
        if scenario is not None
        else None
    )

    return RiskFinancialImpact(
        risk_assessment=risk_assessment,
        scenario_comparison=scenario_comparison,
        financial_translation=translation,
    )
