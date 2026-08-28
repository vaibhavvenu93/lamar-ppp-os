"""
Synthetic opportunity portfolio for Lamar PPP OS Phase 2.

The portfolio provides realistic but synthetic GCC infrastructure
opportunities for demonstrating Opportunity Radar, explainable
opportunity scoring, Bid / No-Bid workflows, and downstream Project
Brain creation.

These records are demonstration data only. They do not represent
current Lamar Holding opportunities or confidential information.
"""

from datetime import date
from typing import Dict, List

from lamar_os.domain.opportunity import (
    OpportunitySource,
    OpportunityStatus,
    PPPOpportunity,
    ProcurementModel,
)
from lamar_os.domain.project import InfrastructureSector
from lamar_os.engines.opportunity_engine import (
    OpportunityFitInputs,
    assess_opportunity,
)


def _source(
    reference: str,
) -> OpportunitySource:
    """Create provenance for a synthetic demo opportunity."""

    return OpportunitySource(
        source_name="Lamar PPP OS Demo Pipeline",
        source_type="SYNTHETIC_DEMO",
        source_reference=reference,
        discovered_at=date(2026, 8, 20),
        is_public=False,
        is_synthetic=True,
    )


def build_demo_opportunities() -> List[PPPOpportunity]:
    """
    Build the Phase 2 opportunity portfolio.

    The portfolio deliberately spans sectors, markets, procurement
    structures, project sizes, and strategic-fit profiles so the
    Opportunity Radar can demonstrate prioritization rather than
    simply presenting identical cards.
    """

    opportunities = [
        PPPOpportunity(
            opportunity_id="OPP-WATER-001",
            name="Eastern Province Independent Water Project",
            country="Saudi Arabia",
            sector=InfrastructureSector.WATER,
            authority="Synthetic Water Authority",
            description=(
                "Development, financing, construction and operation "
                "of a large-scale seawater reverse-osmosis facility "
                "with associated transmission infrastructure."
            ),
            procurement_model=ProcurementModel.BOOT,
            status=OpportunityStatus.INVESTIGATING,
            estimated_capex_usd=700_000_000,
            concession_years=20,
            submission_deadline=date(2026, 10, 30),
            expected_revenue_model=(
                "Long-term availability and water purchase payments"
            ),
            project_location="Eastern Province",
            strategic_theme="Water Security",
            consortium_required=True,
            financing_required=True,
            sources=[
                _source("SYNTHETIC-WATER-001"),
            ],
            known_requirements=[
                "Minimum production capacity of 80,000 m3/day",
                "Long-term operations capability",
                "Committed financing plan",
                "Consortium technical qualification",
            ],
            known_risks=[
                "Desalination equipment procurement exposure",
                "Construction cost escalation",
                "Energy-price sensitivity",
            ],
            tags=[
                "water",
                "desalination",
                "BOOT",
                "Saudi Arabia",
            ],
            is_demo=True,
            data_classification="SYNTHETIC",
        ),
        PPPOpportunity(
            opportunity_id="OPP-ENERGY-002",
            name="GCC Industrial Solar and Storage PPP",
            country="Saudi Arabia",
            sector=InfrastructureSector.ENERGY,
            authority="Synthetic Industrial Authority",
            description=(
                "Utility-scale solar generation and battery storage "
                "supporting a major industrial development under a "
                "long-term contracted revenue structure."
            ),
            procurement_model=ProcurementModel.BOO,
            status=OpportunityStatus.DISCOVERED,
            estimated_capex_usd=520_000_000,
            concession_years=25,
            submission_deadline=date(2026, 11, 18),
            expected_revenue_model=(
                "Long-term contracted capacity and energy payments"
            ),
            project_location="Western Region",
            strategic_theme="Energy Transition",
            consortium_required=True,
            financing_required=True,
            sources=[
                _source("SYNTHETIC-ENERGY-002"),
            ],
            known_requirements=[
                "Utility-scale solar development experience",
                "Battery integration capability",
                "Committed project financing",
            ],
            known_risks=[
                "Battery replacement economics",
                "Grid interconnection schedule",
                "Equipment supply-chain exposure",
            ],
            tags=[
                "energy",
                "solar",
                "storage",
                "Saudi Arabia",
            ],
            is_demo=True,
            data_classification="SYNTHETIC",
        ),
        PPPOpportunity(
            opportunity_id="OPP-SOCIAL-003",
            name="Riyadh Schools Infrastructure Programme",
            country="Saudi Arabia",
            sector=(
                InfrastructureSector.SOCIAL_INFRASTRUCTURE
            ),
            authority="Synthetic Education Authority",
            description=(
                "Design, build, finance and maintain a portfolio of "
                "education facilities under an availability-based "
                "PPP structure."
            ),
            procurement_model=ProcurementModel.DBFOM,
            status=OpportunityStatus.QUALIFIED,
            estimated_capex_usd=310_000_000,
            concession_years=20,
            submission_deadline=date(2026, 12, 5),
            expected_revenue_model=(
                "Availability-based government payments"
            ),
            project_location="Riyadh",
            strategic_theme="Social Infrastructure",
            consortium_required=True,
            financing_required=True,
            sources=[
                _source("SYNTHETIC-SOCIAL-003"),
            ],
            known_requirements=[
                "Multi-site delivery capability",
                "Facilities management plan",
                "Lifecycle maintenance model",
            ],
            known_risks=[
                "Multi-site construction coordination",
                "Lifecycle maintenance cost uncertainty",
            ],
            tags=[
                "schools",
                "social infrastructure",
                "DBFOM",
                "Riyadh",
            ],
            is_demo=True,
            data_classification="SYNTHETIC",
        ),
        PPPOpportunity(
            opportunity_id="OPP-WATER-004",
            name="Oman Regional Wastewater Reuse PPP",
            country="Oman",
            sector=InfrastructureSector.WATER,
            authority="Synthetic Oman Utilities Authority",
            description=(
                "Wastewater treatment, reuse infrastructure and "
                "associated network upgrades serving a growing "
                "regional urban corridor."
            ),
            procurement_model=ProcurementModel.BOT,
            status=OpportunityStatus.DISCOVERED,
            estimated_capex_usd=240_000_000,
            concession_years=22,
            submission_deadline=date(2027, 1, 12),
            expected_revenue_model=(
                "Treatment-volume and availability payments"
            ),
            project_location="Northern Oman",
            strategic_theme="Water Reuse",
            consortium_required=True,
            financing_required=True,
            sources=[
                _source("SYNTHETIC-WATER-004"),
            ],
            known_requirements=[
                "Wastewater treatment experience",
                "Network rehabilitation capability",
                "Long-term O&M plan",
            ],
            known_risks=[
                "Influent volume variability",
                "Network rehabilitation uncertainty",
            ],
            tags=[
                "water",
                "wastewater",
                "reuse",
                "Oman",
            ],
            is_demo=True,
            data_classification="SYNTHETIC",
        ),
        PPPOpportunity(
            opportunity_id="OPP-HEALTH-005",
            name="Gulf Healthcare Campus PPP",
            country="United Arab Emirates",
            sector=(
                InfrastructureSector.SOCIAL_INFRASTRUCTURE
            ),
            authority="Synthetic Health Authority",
            description=(
                "Development and lifecycle maintenance of an "
                "integrated healthcare campus using an "
                "availability-based PPP model."
            ),
            procurement_model=ProcurementModel.DBFOM,
            status=OpportunityStatus.DISCOVERED,
            estimated_capex_usd=860_000_000,
            concession_years=25,
            submission_deadline=date(2027, 2, 8),
            expected_revenue_model=(
                "Long-term availability payments"
            ),
            project_location="United Arab Emirates",
            strategic_theme="Healthcare Infrastructure",
            consortium_required=True,
            financing_required=True,
            sources=[
                _source("SYNTHETIC-HEALTH-005"),
            ],
            known_requirements=[
                "Complex healthcare infrastructure delivery",
                "Clinical-interface planning",
                "Long-term facilities management capability",
            ],
            known_risks=[
                "Complex stakeholder environment",
                "Specialist delivery requirements",
                "Lifecycle cost uncertainty",
            ],
            tags=[
                "healthcare",
                "social infrastructure",
                "UAE",
            ],
            is_demo=True,
            data_classification="SYNTHETIC",
        ),
        PPPOpportunity(
            opportunity_id="OPP-TRANSPORT-006",
            name="Regional Logistics Corridor PPP",
            country="Saudi Arabia",
            sector=InfrastructureSector.TRANSPORT,
            authority="Synthetic Logistics Authority",
            description=(
                "Development and operation of logistics-support "
                "infrastructure serving a strategic industrial "
                "corridor."
            ),
            procurement_model=ProcurementModel.PPP,
            status=OpportunityStatus.DISCOVERED,
            estimated_capex_usd=1_150_000_000,
            concession_years=30,
            submission_deadline=date(2027, 3, 15),
            expected_revenue_model=(
                "Mixed availability and usage-linked payments"
            ),
            project_location="Saudi Arabia",
            strategic_theme="Logistics Infrastructure",
            consortium_required=True,
            financing_required=True,
            sources=[
                _source("SYNTHETIC-TRANSPORT-006"),
            ],
            known_requirements=[
                "Large-scale transport delivery capability",
                "Traffic and demand modelling",
                "Long-tenor financing plan",
            ],
            known_risks=[
                "Demand risk",
                "Large capital requirement",
                "Complex interface management",
            ],
            tags=[
                "transport",
                "logistics",
                "Saudi Arabia",
            ],
            is_demo=True,
            data_classification="SYNTHETIC",
        ),
    ]

    fit_inputs: Dict[
        str,
        OpportunityFitInputs,
    ] = {
        "OPP-WATER-001": OpportunityFitInputs(
            strategic_fit=94,
            sector_fit=96,
            market_fit=92,
            delivery_fit=88,
            financing_fit=86,
            consortium_readiness=82,
            competitive_position=78,
        ),
        "OPP-ENERGY-002": OpportunityFitInputs(
            strategic_fit=91,
            sector_fit=84,
            market_fit=90,
            delivery_fit=78,
            financing_fit=82,
            consortium_readiness=74,
            competitive_position=72,
        ),
        "OPP-SOCIAL-003": OpportunityFitInputs(
            strategic_fit=86,
            sector_fit=79,
            market_fit=91,
            delivery_fit=81,
            financing_fit=80,
            consortium_readiness=76,
            competitive_position=74,
        ),
        "OPP-WATER-004": OpportunityFitInputs(
            strategic_fit=79,
            sector_fit=91,
            market_fit=73,
            delivery_fit=84,
            financing_fit=75,
            consortium_readiness=71,
            competitive_position=77,
        ),
        "OPP-HEALTH-005": OpportunityFitInputs(
            strategic_fit=72,
            sector_fit=63,
            market_fit=78,
            delivery_fit=58,
            financing_fit=76,
            consortium_readiness=61,
            competitive_position=59,
        ),
        "OPP-TRANSPORT-006": OpportunityFitInputs(
            strategic_fit=68,
            sector_fit=54,
            market_fit=84,
            delivery_fit=57,
            financing_fit=66,
            consortium_readiness=60,
            competitive_position=55,
        ),
    }

    for opportunity in opportunities:
        assess_opportunity(
            opportunity=opportunity,
            fit=fit_inputs[
                opportunity.opportunity_id
            ],
        )

    return opportunities


def opportunity_by_id(
    opportunity_id: str,
) -> PPPOpportunity:
    """Return one demo opportunity by identifier."""

    for opportunity in build_demo_opportunities():
        if opportunity.opportunity_id == opportunity_id:
            return opportunity

    raise ValueError(
        f"Unknown demo opportunity: {opportunity_id}"
    )
