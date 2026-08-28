"""
FastAPI application for Lamar PPP OS.

The API exposes tested Lamar OS intelligence to web interfaces
without moving business logic into the presentation layer.

DEMO ENVIRONMENT:
Public-information-inspired context and synthetic project data only.
"""

from dataclasses import asdict
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
from lamar_os.api.project_brain import (
    ProjectBrainResponse,
    project_brain_response,
)
from lamar_os.api.scenario import (
    ScenarioMetrics,
    ScenarioRequest,
    ScenarioResponse,
)
from lamar_os.engines.bid_agent import (
    run_water_ppp_bid_agent,
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


def _build_bid_project_brain(
    opportunity_id: str,
):
    """
    Build connected Document + Bid intelligence for one opportunity.

    Both agents operate on the same Project Brain instance so the
    resulting state can be inspected by the Deal Room.

    This is deterministic demo workflow state, not database-backed
    persistence across requests.
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
                "Connected Project Brain intelligence is currently "
                "implemented for the synthetic Eastern Province "
                "Independent Water Project demo opportunity only."
            ),
        )

    analysis, project_brain, document_agent_run = (
        run_document_workflow()
    )

    if analysis.opportunity_id != opportunity.opportunity_id:
        raise HTTPException(
            status_code=500,
            detail=(
                "Document Agent analysis does not match the "
                "requested opportunity."
            ),
        )

    if project_brain.project_id != analysis.project_id:
        raise HTTPException(
            status_code=500,
            detail=(
                "Document Agent Project Brain does not match "
                "the analyzed project."
            ),
        )

    decision = run_water_ppp_bid_agent(
        opportunity_id=opportunity.opportunity_id,
        project_id=analysis.project_id,
        project_brain=project_brain,
    )

    bid_agent_runs = project_brain.runs_by_agent(
        "Bid Agent"
    )

    if not bid_agent_runs:
        raise HTTPException(
            status_code=500,
            detail=(
                "Bid Agent completed without recording its "
                "execution in the Project Brain."
            ),
        )

    bid_agent_run = bid_agent_runs[-1]

    return (
        opportunity,
        analysis,
        project_brain,
        document_agent_run,
        decision,
        bid_agent_run,
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


@app.post(
    "/api/opportunities/{opportunity_id}/evaluate-bid",
)
def evaluate_bid(
    opportunity_id: str,
) -> dict:
    """
    Execute the deterministic Bid Agent for a supported opportunity.

    The Document Agent first structures the synthetic tender package
    and writes its outputs into a Project Brain. The same Project
    Brain instance is then supplied to the Bid Agent.

    The Bid Agent reasons over that structured intelligence, produces
    a pursuit recommendation, and persists its issues, workstreams,
    recommendation, evidence relationships and execution history into
    the same shared project state.

    The recommendation is advisory only. The system cannot approve
    its own Bid / No-Bid recommendation.
    """

    (
        opportunity,
        analysis,
        project_brain,
        document_agent_run,
        decision,
        bid_agent_run,
    ) = _build_bid_project_brain(
        opportunity_id
    )

    response = asdict(decision)

    response["blocking_issue_count"] = (
        decision.blocking_issue_count
    )
    response["critical_issue_count"] = (
        decision.critical_issue_count
    )
    response["total_estimated_exposure_usd"] = (
        decision.total_estimated_exposure_usd
    )
    response["can_auto_approve"] = (
        decision.can_auto_approve
    )

    response["agent_chain"] = {
        "document_agent": {
            "run_id": document_agent_run.run_id,
            "agent_name": document_agent_run.agent_name,
            "status": document_agent_run.status,
            "evidence_count": len(
                document_agent_run.evidence_ids
            ),
        },
        "bid_agent": {
            "run_id": bid_agent_run.run_id,
            "agent_name": bid_agent_run.agent_name,
            "mode": "DETERMINISTIC",
            "status": bid_agent_run.status,
            "recommendation": (
                decision.recommendation.value
            ),
            "human_approval_required": (
                decision.human_approval_required
            ),
            "output_record_count": len(
                bid_agent_run.output_record_ids
            ),
        },
    }

    response["project_brain"] = {
        "snapshot": project_brain.snapshot(),
        "bid_issue_ids": [
            issue.issue_id
            for issue in decision.issues
        ],
        "workstream_ids": [
            workstream.workstream_id
            for workstream in decision.workstreams
        ],
        "decision_record_id": (
            f"BID-DECISION-{decision.opportunity_id}"
        ),
        "bid_agent_output_record_ids": list(
            bid_agent_run.output_record_ids
        ),
    }

    response["governance"] = {
        "recommendation_policy": (
            "The Bid Agent may recommend pursuit actions."
        ),
        "approval_policy": (
            "Bid / No-Bid approval remains with a human."
        ),
        "calculation_policy": (
            "Readiness scoring and decision gates are "
            "deterministic and inspectable."
        ),
        "evidence_policy": (
            "Material conclusions preserve source evidence "
            "references from Document Intelligence."
        ),
        "state_policy": (
            "Document and Bid Agent outputs are written into "
            "the same traceable Project Brain state."
        ),
    }

    response["data_notice"] = (
        "DEMO ENVIRONMENT — PUBLIC INFORMATION + "
        "SYNTHETIC PROJECT DATA. NOT LAMAR INTERNAL DATA."
    )

    return response


@app.get(
    "/api/opportunities/{opportunity_id}/project-brain",
    response_model=ProjectBrainResponse,
)
def opportunity_project_brain(
    opportunity_id: str,
) -> ProjectBrainResponse:
    """
    Return the connected Project Brain for the Deal Room.

    The endpoint reconstructs the current deterministic demo workflow:

    Document Agent
        -> shared Project Brain
        -> Bid Agent
        -> shared Project Brain
        -> Deal Room API contract

    The returned state includes traceable project records, cross-record
    relationships, agent execution history and pending human gates.

    This prototype currently reconstructs deterministic workflow state
    per request. It does not claim database persistence across server
    restarts or independent requests.
    """

    (
        _,
        _,
        project_brain,
        _,
        _,
        _,
    ) = _build_bid_project_brain(
        opportunity_id
    )

    return project_brain_response(
        project_brain
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
