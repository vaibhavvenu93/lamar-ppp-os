"""
Lamar PPP OS — Executive Brief Demo.

This executable demo shows how structured PPP project information
can flow through financial, risk, and executive intelligence layers
to produce a concise decision-oriented morning brief.

DEMO ENVIRONMENT:
Public-information-inspired context and synthetic project data only.
No Lamar Holding internal or confidential information is used.
"""

from lamar_os.domain.finance import (
    CapitalStructure,
    FinancialAssumptions,
    OperatingAssumptions,
)
from lamar_os.domain.risk import (
    ProjectRisk,
    RiskAllocation,
    RiskCategory,
    RiskSeverity,
)
from lamar_os.engines.executive_adapter import (
    risk_financial_impact_to_signal,
)
from lamar_os.engines.executive_engine import (
    ExecutivePriority,
    ExecutiveSignal,
    ExecutiveSignalType,
    build_executive_brief,
)
from lamar_os.engines.risk_financial_engine import (
    assess_financial_risk,
)


def build_demo_project_financials() -> FinancialAssumptions:
    """Create synthetic financial assumptions for a water PPP."""

    return FinancialAssumptions(
        project_id="DEMO-WATER-001",
        capital=CapitalStructure(
            total_capex_usd=700_000_000,
            debt_ratio=0.70,
            equity_ratio=0.30,
            interest_rate=0.065,
            debt_tenor_years=15,
        ),
        operations=OperatingAssumptions(
            concession_years=20,
            annual_revenue_usd=110_000_000,
            annual_opex_usd=30_000_000,
            revenue_growth_rate=0.02,
            opex_growth_rate=0.02,
        ),
        construction_years=3,
        discount_rate=0.10,
        is_synthetic=True,
        assumption_note=(
            "Synthetic assumptions created for Lamar PPP OS demo."
        ),
    )


def build_construction_risk() -> ProjectRisk:
    """Create a synthetic construction risk."""

    return ProjectRisk(
        risk_id="RISK-CONSTRUCTION-001",
        project_id="DEMO-WATER-001",
        title="Construction Cost Exposure",
        description=(
            "A modeled construction event could increase "
            "project CAPEX by $30M."
        ),
        category=RiskCategory.CONSTRUCTION,
        allocation=RiskAllocation.PRIVATE,
        severity=RiskSeverity.HIGH,
        probability=0.40,
        estimated_impact_usd=30_000_000,
        owner="Project Company",
        mitigation=(
            "Review EPC protections, contingency reserves, "
            "procurement exposure, and schedule controls."
        ),
    )


def build_demo_signals() -> list[ExecutiveSignal]:
    """
    Build signals from both calculated intelligence and
    synthetic executive events.
    """

    assumptions = build_demo_project_financials()
    risk = build_construction_risk()

    financial_risk = assess_financial_risk(
        risk=risk,
        assumptions=assumptions,
    )

    risk_signal = risk_financial_impact_to_signal(
        financial_risk
    )

    obligation_signal = ExecutiveSignal(
        signal_id="EXEC-OBLIGATION-001",
        project_id="DEMO-PPP-002",
        title="Consortium Submission Approaching",
        summary=(
            "Synthetic bid package requires final consortium "
            "approval within three days."
        ),
        signal_type=ExecutiveSignalType.OBLIGATION,
        priority=ExecutivePriority.HIGH,
        days_to_deadline=3,
        requires_decision=True,
        recommended_action=(
            "Confirm consortium approval and submission readiness."
        ),
        source_reference="Synthetic demo obligation.",
    )

    financing_signal = ExecutiveSignal(
        signal_id="EXEC-FINANCE-001",
        project_id="DEMO-WATER-001",
        title="Debt-Service Coverage Watch",
        summary=(
            "Synthetic financing assumptions indicate a covenant "
            "metric that should remain under review."
        ),
        signal_type=ExecutiveSignalType.FINANCIAL,
        priority=ExecutivePriority.MEDIUM,
        financial_exposure_usd=2_000_000,
        days_to_deadline=14,
        recommended_action=(
            "Review downside DSCR scenarios before financing review."
        ),
        source_reference="Synthetic demo financing signal.",
    )

    opportunity_signal = ExecutiveSignal(
        signal_id="EXEC-OPPORTUNITY-001",
        project_id="DEMO-GCC-WATER-002",
        title="New GCC Water PPP Opportunity",
        summary=(
            "Synthetic opportunity identified for initial "
            "strategic-fit and consortium review."
        ),
        signal_type=ExecutiveSignalType.OPPORTUNITY,
        priority=ExecutivePriority.MEDIUM,
        requires_decision=True,
        recommended_action=(
            "Run bid/no-bid assessment and identify capability gaps."
        ),
        source_reference="Synthetic demo opportunity.",
    )

    operations_signal = ExecutiveSignal(
        signal_id="EXEC-OPS-001",
        project_id="DEMO-WATER-001",
        title="Routine Operating Variance",
        summary=(
            "Minor synthetic operating variance detected."
        ),
        signal_type=ExecutiveSignalType.OPERATIONS,
        priority=ExecutivePriority.LOW,
        financial_exposure_usd=200_000,
        recommended_action="Continue routine monitoring.",
        source_reference="Synthetic demo operating signal.",
    )

    return [
        risk_signal,
        obligation_signal,
        financing_signal,
        opportunity_signal,
        operations_signal,
    ]


def format_money(value: float | None) -> str:
    """Format optional USD values for executive display."""

    if value is None:
        return "Not quantified"

    return f"${value:,.0f}"


def print_executive_brief() -> None:
    """Generate and print the Lamar PPP OS morning brief."""

    signals = build_demo_signals()

    brief = build_executive_brief(
        signals=signals,
        top_n=3,
    )

    print("=" * 72)
    print("LAMAR PPP OS")
    print("DEMO ENVIRONMENT — PUBLIC CONTEXT + SYNTHETIC PROJECT DATA")
    print("=" * 72)

    print()
    print("GOOD MORNING, HANI.")
    print()
    print(brief.summary)
    print()

    for index, item in enumerate(
        brief.top_signals,
        start=1,
    ):
        signal = item.signal

        print("-" * 72)
        print(
            f"{index:02d}  "
            f"{signal.title.upper()}"
        )
        print("-" * 72)

        print(
            f"Project: {signal.project_id}"
        )
        print(
            f"Type: {signal.signal_type.value}"
        )
        print(
            f"Priority: {signal.priority.value}"
        )
        print(
            f"Attention score: "
            f"{item.attention_score:.0f}/100"
        )

        print()
        print(signal.summary)

        print()
        print(
            "Financial exposure: "
            f"{format_money(signal.financial_exposure_usd)}"
        )

        print(
            "Why this is ranked here: "
            f"{item.ranking_reason}"
        )

        if signal.recommended_action:
            print()
            print(
                "Recommended action: "
                f"{signal.recommended_action}"
            )

        if signal.source_reference:
            print()
            print(
                "Traceability: "
                f"{signal.source_reference}"
            )

        print()

    print("=" * 72)
    print(
        "AI may interpret and explain. "
        "Deterministic engines calculate and rank."
    )
    print(
        "Consequential project decisions remain with humans."
    )
    print("=" * 72)


if __name__ == "__main__":
    print_executive_brief()
