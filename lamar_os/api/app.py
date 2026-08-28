"""
FastAPI application for Lamar PPP OS.

The API exposes tested Lamar OS intelligence to web interfaces
without moving business logic into the presentation layer.

DEMO ENVIRONMENT:
Public-information-inspired context and synthetic project data only.
"""

from fastapi import FastAPI

from demo.executive_brief import build_demo_signals
from lamar_os.engines.executive_engine import (
    build_executive_brief,
)


app = FastAPI(
    title="Lamar PPP OS",
    description=(
        "Experimental AI-native operating system for PPP "
        "infrastructure intelligence."
    ),
    version="0.1.0",
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
