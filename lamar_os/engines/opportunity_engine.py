"""
Explainable PPP opportunity scoring engine for Lamar PPP OS.

The engine converts structured opportunity-fit inputs into a
deterministic strategic assessment.

AI may later help gather or interpret the underlying evidence, but
the score itself is calculated from explicit weights and rules so an
executive can inspect why an opportunity received its rating.
"""

from dataclasses import dataclass
from typing import Dict, List

from lamar_os.domain.opportunity import (
    OpportunityAssessment,
    OpportunityPriority,
    OpportunityScoreComponent,
    PPPOpportunity,
)


@dataclass
class OpportunityFitInputs:
    """
    Normalized opportunity-fit inputs.

    Every value must be between 0 and 100.

    These inputs can eventually be produced from public market data,
    Lamar project history, specialist-agent outputs, consortium
    readiness, financing information, and human assessments.
    """

    strategic_fit: float
    sector_fit: float
    market_fit: float
    delivery_fit: float
    financing_fit: float
    consortium_readiness: float
    competitive_position: float


WEIGHTS: Dict[str, float] = {
    "strategic_fit": 0.20,
    "sector_fit": 0.15,
    "market_fit": 0.15,
    "delivery_fit": 0.15,
    "financing_fit": 0.12,
    "consortium_readiness": 0.13,
    "competitive_position": 0.10,
}


LABELS: Dict[str, str] = {
    "strategic_fit": "Strategic Fit",
    "sector_fit": "Sector Fit",
    "market_fit": "Market Fit",
    "delivery_fit": "Delivery Fit",
    "financing_fit": "Financing Fit",
    "consortium_readiness": "Consortium Readiness",
    "competitive_position": "Competitive Position",
}


def _validate_score(
    name: str,
    score: float,
) -> None:
    """Ensure a normalized score is between 0 and 100."""

    if score < 0 or score > 100:
        raise ValueError(
            f"{name} must be between 0 and 100."
        )


def _priority_from_score(
    score: float,
) -> OpportunityPriority:
    """Convert the overall score into executive priority."""

    if score >= 85:
        return OpportunityPriority.STRATEGIC

    if score >= 70:
        return OpportunityPriority.HIGH

    if score >= 55:
        return OpportunityPriority.MEDIUM

    return OpportunityPriority.LOW


def _recommendation_from_score(
    score: float,
) -> str:
    """Return an initial pursuit recommendation."""

    if score >= 85:
        return "PRIORITIZE"

    if score >= 70:
        return "INVESTIGATE"

    if score >= 55:
        return "REVIEW"

    return "PASS"


def _component_rationale(
    component_name: str,
    score: float,
) -> str:
    """
    Produce a deterministic explanation for a score.

    This is deliberately rule-based. A future AI interpretation layer
    can provide richer evidence while leaving the scoring logic
    inspectable.
    """

    label = LABELS[component_name]

    if score >= 90:
        return (
            f"{label} is exceptionally strong for "
            "this opportunity."
        )

    if score >= 80:
        return (
            f"{label} is a material advantage for "
            "this opportunity."
        )

    if score >= 70:
        return (
            f"{label} supports pursuit but should "
            "remain under review."
        )

    if score >= 55:
        return (
            f"{label} is acceptable but contains "
            "meaningful uncertainty."
        )

    return (
        f"{label} is currently a material concern "
        "for pursuit."
    )


def _build_strengths(
    values: Dict[str, float],
) -> List[str]:
    """Return the strongest dimensions of the assessment."""

    ranked = sorted(
        values.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return [
        (
            f"{LABELS[name]} is strong "
            f"at {score:.0f}/100."
        )
        for name, score in ranked
        if score >= 80
    ][:3]


def _build_concerns(
    values: Dict[str, float],
) -> List[str]:
    """Return dimensions requiring further investigation."""

    ranked = sorted(
        values.items(),
        key=lambda item: item[1],
    )

    concerns = [
        (
            f"{LABELS[name]} requires attention "
            f"at {score:.0f}/100."
        )
        for name, score in ranked
        if score < 70
    ][:3]

    if concerns:
        return concerns

    return [
        (
            f"{LABELS[name]} is the weakest current "
            f"dimension at {score:.0f}/100."
        )
        for name, score in ranked[:1]
    ]


def assess_opportunity(
    opportunity: PPPOpportunity,
    fit: OpportunityFitInputs,
) -> OpportunityAssessment:
    """
    Calculate an explainable opportunity assessment.

    The function does not make the Bid / No-Bid decision.

    It produces a deterministic recommendation that can be consumed
    by the Opportunity Radar, Bid Agent, and executive workflow.
    """

    values = {
        "strategic_fit": fit.strategic_fit,
        "sector_fit": fit.sector_fit,
        "market_fit": fit.market_fit,
        "delivery_fit": fit.delivery_fit,
        "financing_fit": fit.financing_fit,
        "consortium_readiness": (
            fit.consortium_readiness
        ),
        "competitive_position": (
            fit.competitive_position
        ),
    }

    for name, score in values.items():
        _validate_score(name, score)

    components: List[
        OpportunityScoreComponent
    ] = []

    for name, score in values.items():
        components.append(
            OpportunityScoreComponent(
                name=LABELS[name],
                score=score,
                weight=WEIGHTS[name],
                rationale=_component_rationale(
                    name,
                    score,
                ),
            )
        )

    overall_score = sum(
        component.weighted_score
        for component in components
    )

    overall_score = round(
        overall_score,
        2,
    )

    priority = _priority_from_score(
        overall_score,
    )

    recommendation = _recommendation_from_score(
        overall_score,
    )

    strengths = _build_strengths(
        values,
    )

    concerns = _build_concerns(
        values,
    )

    recommendation_reason = (
        f"The opportunity scored "
        f"{overall_score:.1f}/100 using seven "
        "weighted strategic, market, delivery, "
        "financing, consortium, and competitive "
        "dimensions. The score supports a "
        f"{recommendation} recommendation, subject "
        "to human Bid / No-Bid review."
    )

    assessment = OpportunityAssessment(
        opportunity_id=opportunity.opportunity_id,
        strategic_fit=fit.strategic_fit,
        sector_fit=fit.sector_fit,
        market_fit=fit.market_fit,
        delivery_fit=fit.delivery_fit,
        financing_fit=fit.financing_fit,
        consortium_readiness=(
            fit.consortium_readiness
        ),
        competitive_position=(
            fit.competitive_position
        ),
        overall_score=overall_score,
        priority=priority,
        recommendation=recommendation,
        recommendation_reason=(
            recommendation_reason
        ),
        strengths=strengths,
        concerns=concerns,
        components=components,
        human_decision_required=True,
    )

    opportunity.attach_assessment(
        assessment,
    )

    return assessment
