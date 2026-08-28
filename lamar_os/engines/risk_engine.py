"""
Deterministic PPP risk engine for Lamar PPP OS.

This engine evaluates structured project risks using probability,
financial impact, severity, and risk allocation.

AI may help identify candidate risks from project documents, but
risk calculations and executive-attention rules remain deterministic.
"""

from dataclasses import dataclass
from typing import Optional

from lamar_os.domain.risk import (
    ProjectRisk,
    RiskSeverity,
)


@dataclass
class RiskAssessment:
    """Calculated assessment of a structured PPP project risk."""

    risk: ProjectRisk

    expected_loss_usd: Optional[float]
    risk_score: Optional[float]

    executive_attention: bool
    attention_reason: str


def calculate_expected_loss(
    risk: ProjectRisk,
) -> Optional[float]:
    """
    Calculate probability-weighted financial exposure.

    Expected Loss = Probability × Estimated Financial Impact
    """

    if (
        risk.probability is None
        or risk.estimated_impact_usd is None
    ):
        return None

    if not 0 <= risk.probability <= 1:
        raise ValueError(
            "Risk probability must be between 0 and 1"
        )

    if risk.estimated_impact_usd < 0:
        raise ValueError(
            "Estimated financial impact cannot be negative"
        )

    return (
        risk.probability
        * risk.estimated_impact_usd
    )


def calculate_risk_score(
    risk: ProjectRisk,
) -> Optional[float]:
    """
    Calculate a normalized risk score from probability and severity.

    Score range:
        0.0 = negligible
        1.0 = maximum modeled risk
    """

    if risk.probability is None:
        return None

    if not 0 <= risk.probability <= 1:
        raise ValueError(
            "Risk probability must be between 0 and 1"
        )

    severity_weights = {
        RiskSeverity.LOW: 0.25,
        RiskSeverity.MEDIUM: 0.50,
        RiskSeverity.HIGH: 0.75,
        RiskSeverity.CRITICAL: 1.00,
    }

    severity_weight = severity_weights[risk.severity]

    return risk.probability * severity_weight


def requires_executive_attention(
    risk: ProjectRisk,
    expected_loss_usd: Optional[float],
    risk_score: Optional[float],
) -> tuple[bool, str]:
    """
    Determine whether a risk should be escalated to executives.

    Thresholds are explicit so they can later become configurable
    governance policies rather than hidden AI judgments.
    """

    if risk.requires_executive_attention:
        return (
            True,
            "Risk was explicitly flagged for executive attention.",
        )

    if risk.severity == RiskSeverity.CRITICAL:
        return (
            True,
            "Risk severity is CRITICAL.",
        )

    if (
        expected_loss_usd is not None
        and expected_loss_usd >= 10_000_000
    ):
        return (
            True,
            "Expected financial exposure is at least $10M.",
        )

    if (
        risk_score is not None
        and risk_score >= 0.50
    ):
        return (
            True,
            "Probability-weighted risk score is at least 0.50.",
        )

    return (
        False,
        "Risk remains below current executive escalation thresholds.",
    )


def assess_risk(
    risk: ProjectRisk,
) -> RiskAssessment:
    """Run the complete deterministic assessment for a project risk."""

    expected_loss = calculate_expected_loss(risk)
    risk_score = calculate_risk_score(risk)

    executive_attention, attention_reason = (
        requires_executive_attention(
            risk=risk,
            expected_loss_usd=expected_loss,
            risk_score=risk_score,
        )
    )

    return RiskAssessment(
        risk=risk,
        expected_loss_usd=expected_loss,
        risk_score=risk_score,
        executive_attention=executive_attention,
        attention_reason=attention_reason,
    )
