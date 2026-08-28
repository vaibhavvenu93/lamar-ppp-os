"""
Opportunity Radar API models for Lamar PPP OS.

These models expose the Phase 2 opportunity portfolio and its
deterministic strategic assessment to the executive interface.

The API deliberately distinguishes opportunity facts from scored
interpretation and preserves the human Bid / No-Bid boundary.
"""

from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from lamar_os.domain.opportunity import PPPOpportunity


class OpportunityScoreComponentResponse(BaseModel):
    """One explainable component of the Lamar-fit score."""

    name: str
    score: float
    weight: float
    weighted_score: float
    rationale: str
    evidence: Optional[str] = None


class OpportunityAssessmentResponse(BaseModel):
    """Explainable strategic assessment returned to the UI."""

    overall_score: float
    priority: str
    recommendation: str
    recommendation_reason: str

    strategic_fit: float
    sector_fit: float
    market_fit: float
    delivery_fit: float
    financing_fit: float
    consortium_readiness: float
    competitive_position: float

    strengths: List[str]
    concerns: List[str]

    components: List[
        OpportunityScoreComponentResponse
    ]

    human_decision_required: bool


class OpportunitySummaryResponse(BaseModel):
    """Executive pipeline representation of one opportunity."""

    opportunity_id: str
    name: str
    country: str
    sector: str
    authority: str

    procurement_model: str
    status: str

    estimated_capex_usd: Optional[float]
    concession_years: Optional[int]
    submission_deadline: Optional[date]

    strategic_theme: Optional[str]
    project_location: Optional[str]

    overall_score: Optional[float]
    priority: Optional[str]
    recommendation: Optional[str]

    known_risk_count: int
    known_requirement_count: int

    is_demo: bool
    data_classification: str


class OpportunityDetailResponse(BaseModel):
    """Full Opportunity Radar investigation response."""

    opportunity_id: str
    name: str
    country: str
    sector: str
    authority: str

    description: Optional[str]

    procurement_model: str
    status: str

    estimated_capex_usd: Optional[float]
    concession_years: Optional[int]
    submission_deadline: Optional[date]

    expected_revenue_model: Optional[str]
    project_location: Optional[str]
    strategic_theme: Optional[str]

    consortium_required: bool
    financing_required: bool

    known_requirements: List[str]
    known_risks: List[str]
    tags: List[str]

    assessment: Optional[
        OpportunityAssessmentResponse
    ]

    data_notice: str
    human_bid_decision_required: bool


class OpportunityPortfolioResponse(BaseModel):
    """Opportunity Radar pipeline response."""

    product: str = "Lamar PPP OS"
    module: str = "Opportunity Radar"

    opportunity_count: int
    total_pipeline_capex_usd: float

    strategic_count: int
    high_priority_count: int

    opportunities: List[
        OpportunitySummaryResponse
    ]

    scoring_policy: str = (
        "Opportunity scores are calculated by deterministic "
        "weighted rules. AI may support evidence gathering "
        "but does not authorize Bid / No-Bid decisions."
    )

    data_notice: str = (
        "Phase 2 demonstration portfolio. Opportunities and "
        "project assumptions are synthetic and do not represent "
        "Lamar Holding's confidential pipeline."
    )


def _assessment_response(
    opportunity: PPPOpportunity,
) -> Optional[OpportunityAssessmentResponse]:
    """Convert a domain assessment into an API response."""

    assessment = opportunity.assessment

    if assessment is None:
        return None

    return OpportunityAssessmentResponse(
        overall_score=assessment.overall_score,
        priority=assessment.priority.value,
        recommendation=assessment.recommendation,
        recommendation_reason=(
            assessment.recommendation_reason
        ),
        strategic_fit=assessment.strategic_fit,
        sector_fit=assessment.sector_fit,
        market_fit=assessment.market_fit,
        delivery_fit=assessment.delivery_fit,
        financing_fit=assessment.financing_fit,
        consortium_readiness=(
            assessment.consortium_readiness
        ),
        competitive_position=(
            assessment.competitive_position
        ),
        strengths=assessment.strengths,
        concerns=assessment.concerns,
        components=[
            OpportunityScoreComponentResponse(
                name=component.name,
                score=component.score,
                weight=component.weight,
                weighted_score=round(
                    component.weighted_score,
                    2,
                ),
                rationale=component.rationale,
                evidence=component.evidence,
            )
            for component in assessment.components
        ],
        human_decision_required=(
            assessment.human_decision_required
        ),
    )


def opportunity_summary(
    opportunity: PPPOpportunity,
) -> OpportunitySummaryResponse:
    """Convert one opportunity into a pipeline summary."""

    assessment = opportunity.assessment

    return OpportunitySummaryResponse(
        opportunity_id=opportunity.opportunity_id,
        name=opportunity.name,
        country=opportunity.country,
        sector=opportunity.sector.value,
        authority=opportunity.authority,
        procurement_model=(
            opportunity.procurement_model.value
        ),
        status=opportunity.status.value,
        estimated_capex_usd=(
            opportunity.estimated_capex_usd
        ),
        concession_years=(
            opportunity.concession_years
        ),
        submission_deadline=(
            opportunity.submission_deadline
        ),
        strategic_theme=opportunity.strategic_theme,
        project_location=opportunity.project_location,
        overall_score=(
            assessment.overall_score
            if assessment
            else None
        ),
        priority=(
            assessment.priority.value
            if assessment
            else None
        ),
        recommendation=(
            assessment.recommendation
            if assessment
            else None
        ),
        known_risk_count=len(
            opportunity.known_risks
        ),
        known_requirement_count=len(
            opportunity.known_requirements
        ),
        is_demo=opportunity.is_demo,
        data_classification=(
            opportunity.data_classification
        ),
    )


def opportunity_detail(
    opportunity: PPPOpportunity,
) -> OpportunityDetailResponse:
    """Convert one opportunity into investigation detail."""

    return OpportunityDetailResponse(
        opportunity_id=opportunity.opportunity_id,
        name=opportunity.name,
        country=opportunity.country,
        sector=opportunity.sector.value,
        authority=opportunity.authority,
        description=opportunity.description,
        procurement_model=(
            opportunity.procurement_model.value
        ),
        status=opportunity.status.value,
        estimated_capex_usd=(
            opportunity.estimated_capex_usd
        ),
        concession_years=(
            opportunity.concession_years
        ),
        submission_deadline=(
            opportunity.submission_deadline
        ),
        expected_revenue_model=(
            opportunity.expected_revenue_model
        ),
        project_location=opportunity.project_location,
        strategic_theme=opportunity.strategic_theme,
        consortium_required=(
            opportunity.consortium_required
        ),
        financing_required=(
            opportunity.financing_required
        ),
        known_requirements=(
            opportunity.known_requirements
        ),
        known_risks=opportunity.known_risks,
        tags=opportunity.tags,
        assessment=_assessment_response(
            opportunity
        ),
        data_notice=(
            "Synthetic demonstration opportunity. "
            "No Lamar confidential information is used."
        ),
        human_bid_decision_required=True,
    )
