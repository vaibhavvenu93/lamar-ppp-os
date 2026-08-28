"""
FastAPI application for Lamar PPP OS.

The API exposes tested Lamar OS intelligence to web interfaces
without moving business logic into the presentation layer.

DEMO ENVIRONMENT:
Public-information-inspired context and synthetic project data only.
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from demo.executive_brief import (
    build_demo_project_financials,
    build_demo_signals,
)
from demo.opportunities import (
    build_demo_opportunities,
    opportunity_by_id,
)
from lamar_os.agents.document_workflow import (
    run_document_workflow,
)
from lamar_os.api.document import (
    DocumentIntelligenceResponse,
    document_intelligence_response,
)
from lamar_os.api.opportunity import (
    OpportunityDetailResponse,
    OpportunityPortfolioResponse,
    opportunity_detail,
    opportunity_summary,
)
from lamar_os.api.scenario import (
    ScenarioMetrics,
    ScenarioRequest,
    ScenarioResponse,
)
from lamar_os.engines.executive_engine import (
    build_executive_brief,
)
from lamar_os.engines.scenario_engine import (
    Scenario,
    run_scenario,
)


app = FastAPI(
    title="Lamar PPP OS",
    description=(
        "Experimental AI-native operating system for PPP "
        "infrastructure intelligence."
    ),
    version="0.1.0",
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIST = PROJECT_ROOT / "frontend" / "dist"
FRONTEND_ASSETS = FRONTEND_DIST / "assets"


if FRONTEND_ASSETS.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_ASSETS),
        name="frontend-assets",
    )


@app.get("/")
def root() -> dict:
    """Return basic product information."""

    return {
        "product": "Lamar PPP OS",
        "version": "0.1.0",
        "environment": "DEMO",
        "data_policy": (
            "Public context and synthetic project data only."
        ),
        "message": (
            "Infrastructure intelligence from opportunity "
            "discovery through operations."
        ),
    }


@app.get("/health")
def health() -> dict:
    """Simple deployment health check."""

    return {
        "status": "healthy",
        "service": "lamar-ppp-os",
    }


@app.get(
    "/api/opportunities",
    response_model=OpportunityPortfolioResponse,
)
def opportunity_portfolio() -> OpportunityPortfolioResponse:
    """
    Return the Phase 2 Opportunity Radar portfolio.

    Opportunities are synthetic demonstration records scored by the
    deterministic opportunity engine. The endpoint exposes pipeline
    prioritization without making a Bid / No-Bid decision.
    """

    opportunities = build_demo_opportunities()

    summaries = [
        opportunity_summary(opportunity)
        for opportunity in opportunities
    ]

    summaries.sort(
        key=lambda opportunity: (
            opportunity.overall_score
            if opportunity.overall_score is not None
            else -1
        ),
        reverse=True,
    )

    total_pipeline_capex_usd = sum(
        opportunity.estimated_capex_usd or 0
        for opportunity in opportunities
    )

    strategic_count = sum(
        1
        for opportunity in summaries
        if opportunity.priority == "STRATEGIC"
    )

    high_priority_count = sum(
        1
        for opportunity in summaries
        if opportunity.priority == "HIGH"
    )

    return OpportunityPortfolioResponse(
        opportunity_count=len(summaries),
        total_pipeline_capex_usd=(
            total_pipeline_capex_usd
        ),
        strategic_count=strategic_count,
        high_priority_count=high_priority_count,
        opportunities=summaries,
    )


@app.get(
    "/api/opportunities/{opportunity_id}",
    response_model=OpportunityDetailResponse,
)
def opportunity_investigation(
    opportunity_id: str,
) -> OpportunityDetailResponse:
    """
    Return the investigation view for one opportunity.

    The detailed response includes opportunity facts, known
    requirements, known risks, scoring dimensions, strengths,
    concerns, provenance boundaries, and the human decision gate.
    """

    try:
        opportunity = opportunity_by_id(
            opportunity_id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return opportunity_detail(
        opportunity
    )


@app.post(
    "/api/opportunities/{opportunity_id}/investigate",
    response_model=DocumentIntelligenceResponse,
)
def investigate_opportunity_documents(
    opportunity_id: str,
) -> DocumentIntelligenceResponse:
    """
    Execute the Document Agent for a supported demo opportunity.

    The current prototype has a synthetic tender package for the
    Eastern Province Independent Water Project. The workflow converts
    that package into evidence-backed requirements, obligations,
    critical dates, risks and clarification questions, and records an
    inspectable AgentRun in the Project Brain.

    No consequential Bid / No-Bid, contractual, legal or investment
    decision is made by this endpoint.
    """

    try:
        opportunity = opportunity_by_id(
            opportunity_id
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    if opportunity.opportunity_id != "OPP-WATER-001":
        raise HTTPException(
            status_code=409,
            detail=(
                "Document Intelligence is currently implemented "
                "for the synthetic Eastern Province Independent "
                "Water Project demo opportunity only."
            ),
        )

    analysis, _, agent_run = run_document_workflow()

    if analysis.opportunity_id != opportunity.opportunity_id:
        raise HTTPException(
            status_code=500,
            detail=(
                "Document Agent analysis does not match the "
                "requested opportunity."
            ),
        )

    return document_intelligence_response(
        analysis=analysis,
        agent_run=agent_run,
    )


@app.get("/api/executive-brief")
def executive_brief() -> dict:
    """
    Generate the current synthetic executive brief.

    The endpoint invokes the same tested intelligence pipeline used
    by the executable demo rather than returning hardcoded results.
    """

    signals = build_demo_signals()

    brief = build_executive_brief(
        signals=signals,
        top_n=3,
    )

    items = []

    for rank, item in enumerate(
        brief.top_signals,
        start=1,
    ):
        signal = item.signal

        items.append(
            {
                "rank": rank,
                "signal_id": signal.signal_id,
                "project_id": signal.project_id,
                "title": signal.title,
                "summary": signal.summary,
                "type": signal.signal_type.value,
                "priority": signal.priority.value,
                "attention_score": item.attention_score,
                "financial_exposure_usd": (
                    signal.financial_exposure_usd
                ),
                "days_to_deadline": (
                    signal.days_to_deadline
                ),
                "requires_decision": (
                    signal.requires_decision
                ),
                "recommended_action": (
                    signal.recommended_action
                ),
                "ranking_reason": (
                    item.ranking_reason
                ),
                "traceability": (
                    signal.source_reference
                ),
            }
        )

    return {
        "product": "Lamar PPP OS",
        "environment": "DEMO",
        "data_notice": (
            "Public-information-inspired context and "
            "synthetic project data only."
        ),
        "brief": {
            "title": brief.title,
            "greeting": "Good morning, Hani.",
            "summary": brief.summary,
            "total_signals_reviewed": (
                brief.total_signals_reviewed
            ),
            "critical_signal_count": (
                brief.critical_signal_count
            ),
            "items": items,
        },
        "governance": {
            "calculation_policy": (
                "Deterministic engines calculate and rank."
            ),
            "ai_policy": (
                "AI may interpret and explain."
            ),
            "decision_policy": (
                "Consequential project decisions remain "
                "with humans."
            ),
        },
    }


@app.post(
    "/api/scenario",
    response_model=ScenarioResponse,
)
def financial_scenario(
    request: ScenarioRequest,
) -> ScenarioResponse:
    """
    Run an interactive PPP Financial Twin scenario.

    User-controlled assumptions are passed into the deterministic
    scenario and financial engines. No language model performs
    the financial calculations.
    """

    assumptions = build_demo_project_financials()

    scenario = Scenario(
        name=request.name,
        description=(
            "Interactive executive scenario submitted "
            "through the Lamar PPP OS interface."
        ),
        capex_change_pct=request.capex_change_pct,
        revenue_change_pct=request.revenue_change_pct,
        opex_change_pct=request.opex_change_pct,
        interest_rate_change_pct=(
            request.interest_rate_change_pct
        ),
    )

    comparison = run_scenario(
        assumptions=assumptions,
        scenario=scenario,
    )

    base = comparison.base_results
    modeled = comparison.scenario_results

    return ScenarioResponse(
        scenario_name=scenario.name,
        base=ScenarioMetrics(
            equity_irr=base.equity_irr,
            project_npv_usd=base.project_npv_usd,
            minimum_dscr=base.minimum_dscr,
        ),
        scenario=ScenarioMetrics(
            equity_irr=modeled.equity_irr,
            project_npv_usd=(
                modeled.project_npv_usd
            ),
            minimum_dscr=modeled.minimum_dscr,
        ),
        equity_irr_change=(
            comparison.equity_irr_change
        ),
        project_npv_change_usd=(
            comparison.project_npv_change_usd
        ),
        minimum_dscr_change=(
            comparison.minimum_dscr_change
        ),
    )


@app.get("/app")
def dashboard():
    """
    Serve the Lamar PPP OS executive interface.

    The frontend is available after the React production build
    has generated frontend/dist.
    """

    index_file = FRONTEND_DIST / "index.html"

    if not index_file.exists():
        return {
            "status": "frontend_not_built",
            "message": (
                "Build the React frontend before serving "
                "the Lamar OS dashboard."
            ),
        }

    return FileResponse(index_file)
