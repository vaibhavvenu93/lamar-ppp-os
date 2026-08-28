"""
Executive intelligence engine for Lamar PPP OS.

This module converts project risks, financial impacts, obligations,
and other structured signals into a prioritized executive brief.

The engine ranks attention items deterministically so executives
can understand why something has been escalated.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class ExecutiveSignalType(str, Enum):
    """Types of signals that may require executive attention."""

    RISK = "RISK"
    FINANCIAL = "FINANCIAL"
    OBLIGATION = "OBLIGATION"
    OPPORTUNITY = "OPPORTUNITY"
    CONSTRUCTION = "CONSTRUCTION"
    OPERATIONS = "OPERATIONS"
    DECISION = "DECISION"


class ExecutivePriority(str, Enum):
    """Executive priority levels."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class ExecutiveSignal:
    """
    A structured signal that may appear in an executive brief.

    Signals preserve their source and rationale so prioritization
    remains inspectable rather than becoming a black-box AI score.
    """

    signal_id: str
    project_id: str

    title: str
    summary: str

    signal_type: ExecutiveSignalType
    priority: ExecutivePriority

    financial_exposure_usd: Optional[float] = None
    days_to_deadline: Optional[int] = None

    requires_decision: bool = False
    recommended_action: Optional[str] = None

    source_reference: Optional[str] = None


@dataclass
class PrioritizedSignal:
    """An executive signal with its calculated attention score."""

    signal: ExecutiveSignal
    attention_score: float
    ranking_reason: str


@dataclass
class ExecutiveBrief:
    """Prioritized executive view across PPP projects."""

    title: str
    summary: str

    top_signals: List[PrioritizedSignal] = field(
        default_factory=list
    )

    total_signals_reviewed: int = 0
    critical_signal_count: int = 0


def calculate_attention_score(
    signal: ExecutiveSignal,
) -> float:
    """
    Calculate a deterministic executive-attention score.

    The score combines:
    - stated priority
    - financial exposure
    - deadline urgency
    - whether an executive decision is required

    Maximum score is capped at 100.
    """

    priority_scores = {
        ExecutivePriority.LOW: 10.0,
        ExecutivePriority.MEDIUM: 25.0,
        ExecutivePriority.HIGH: 45.0,
        ExecutivePriority.CRITICAL: 65.0,
    }

    score = priority_scores[signal.priority]

    if signal.financial_exposure_usd is not None:
        if signal.financial_exposure_usd >= 50_000_000:
            score += 20.0
        elif signal.financial_exposure_usd >= 10_000_000:
            score += 15.0
        elif signal.financial_exposure_usd >= 1_000_000:
            score += 8.0

    if signal.days_to_deadline is not None:
        if signal.days_to_deadline < 0:
            score += 20.0
        elif signal.days_to_deadline <= 3:
            score += 15.0
        elif signal.days_to_deadline <= 7:
            score += 10.0
        elif signal.days_to_deadline <= 14:
            score += 5.0

    if signal.requires_decision:
        score += 10.0

    return min(score, 100.0)


def explain_ranking(
    signal: ExecutiveSignal,
) -> str:
    """Explain why a signal received executive attention."""

    reasons: List[str] = [
        f"{signal.priority.value} priority"
    ]

    if (
        signal.financial_exposure_usd is not None
        and signal.financial_exposure_usd >= 10_000_000
    ):
        reasons.append(
            f"${signal.financial_exposure_usd:,.0f} financial exposure"
        )

    if signal.days_to_deadline is not None:
        if signal.days_to_deadline < 0:
            reasons.append("deadline overdue")
        elif signal.days_to_deadline <= 7:
            reasons.append(
                f"deadline in {signal.days_to_deadline} days"
            )

    if signal.requires_decision:
        reasons.append("executive decision required")

    return "; ".join(reasons)


def build_executive_brief(
    signals: List[ExecutiveSignal],
    top_n: int = 3,
) -> ExecutiveBrief:
    """
    Rank structured signals and return the highest-priority items.

    The default executive brief intentionally surfaces only three
    items to reduce noise and focus attention.
    """

    if top_n <= 0:
        raise ValueError(
            "Number of executive brief items must be greater than zero"
        )

    prioritized = [
        PrioritizedSignal(
            signal=signal,
            attention_score=calculate_attention_score(signal),
            ranking_reason=explain_ranking(signal),
        )
        for signal in signals
    ]

    prioritized.sort(
        key=lambda item: item.attention_score,
        reverse=True,
    )

    critical_count = sum(
        1
        for signal in signals
        if signal.priority == ExecutivePriority.CRITICAL
    )

    top_signals = prioritized[:top_n]

    if top_signals:
        summary = (
            f"{len(top_signals)} items require your attention "
            f"from {len(signals)} signals reviewed."
        )
    else:
        summary = "No executive attention items identified."

    return ExecutiveBrief(
        title="Lamar Executive Brief",
        summary=summary,
        top_signals=top_signals,
        total_signals_reviewed=len(signals),
        critical_signal_count=critical_count,
    )
