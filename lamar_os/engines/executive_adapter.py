"""
Executive adapters for Lamar PPP OS.

Adapters convert outputs from domain engines into structured
executive signals without duplicating the underlying calculations.
"""

from lamar_os.domain.risk import RiskSeverity
from lamar_os.engines.executive_engine import (
    ExecutivePriority,
    ExecutiveSignal,
    ExecutiveSignalType,
)
from lamar_os.engines.risk_financial_engine import (
    RiskFinancialImpact,
)


def _map_risk_priority(
    severity: RiskSeverity,
) -> ExecutivePriority:
    """Map PPP risk severity into executive priority."""

    mapping = {
        RiskSeverity.LOW: ExecutivePriority.LOW,
        RiskSeverity.MEDIUM: ExecutivePriority.MEDIUM,
        RiskSeverity.HIGH: ExecutivePriority.HIGH,
        RiskSeverity.CRITICAL: ExecutivePriority.CRITICAL,
    }

    return mapping[severity]


def risk_financial_impact_to_signal(
    impact: RiskFinancialImpact,
) -> ExecutiveSignal:
    """
    Convert an assessed financial risk into an executive signal.

    The adapter uses calculated engine outputs rather than
    recalculating risk or financial metrics.
    """

    risk = impact.risk_assessment.risk

    expected_loss = (
        impact.risk_assessment.expected_loss_usd
    )

    comparison = impact.scenario_comparison

    summary_parts = [
        risk.description,
    ]

    if expected_loss is not None:
        summary_parts.append(
            f"Expected exposure: ${expected_loss:,.0f}."
        )

    if (
        comparison is not None
        and comparison.equity_irr_change is not None
    ):
        irr_change_percentage_points = (
            comparison.equity_irr_change * 100
        )

        summary_parts.append(
            "Modeled equity IRR change: "
            f"{irr_change_percentage_points:+.2f} pp."
        )

    if (
        comparison is not None
        and comparison.project_npv_change_usd is not None
    ):
        summary_parts.append(
            "Modeled project NPV change: "
            f"${comparison.project_npv_change_usd:,.0f}."
        )

    recommended_action = risk.mitigation

    if recommended_action is None:
        recommended_action = (
            "Review the risk, validate assumptions, and assign "
            "an accountable owner."
        )

    return ExecutiveSignal(
        signal_id=f"EXEC-{risk.risk_id}",
        project_id=risk.project_id,
        title=risk.title,
        summary=" ".join(summary_parts),
        signal_type=ExecutiveSignalType.RISK,
        priority=_map_risk_priority(risk.severity),
        financial_exposure_usd=expected_loss,
        requires_decision=(
            impact.risk_assessment.executive_attention
        ),
        recommended_action=recommended_action,
        source_reference=(
            impact.financial_translation
        ),
    )
