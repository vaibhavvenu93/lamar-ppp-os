"""
Canonical PPP project model for Lamar PPP OS.

This module defines the core representation of an infrastructure
project that other engines and agents can operate on.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class ProjectStage(str, Enum):
    """Lifecycle stages of a PPP infrastructure project."""

    DISCOVERY = "DISCOVERY"
    BID = "BID"
    STRUCTURING = "STRUCTURING"
    FINANCING = "FINANCING"
    CONSTRUCTION = "CONSTRUCTION"
    OPERATIONS = "OPERATIONS"
    TRANSFER = "TRANSFER"


class InfrastructureSector(str, Enum):
    """Infrastructure sectors supported by the project model."""

    WATER = "WATER"
    ENERGY = "ENERGY"
    SOCIAL_INFRASTRUCTURE = "SOCIAL_INFRASTRUCTURE"
    TRANSPORT = "TRANSPORT"
    OTHER = "OTHER"


@dataclass
class ProjectParty:
    """An organisation participating in the PPP project."""

    name: str
    role: str
    country: Optional[str] = None


@dataclass
class PPPProject:
    """
    Canonical representation of a PPP infrastructure project.

    The model intentionally separates factual project information
    from AI-generated interpretation so downstream systems can
    maintain traceability.
    """

    project_id: str
    name: str
    country: str
    sector: InfrastructureSector
    stage: ProjectStage

    description: Optional[str] = None
    concession_years: Optional[int] = None
    estimated_capex_usd: Optional[float] = None

    parties: List[ProjectParty] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    is_demo: bool = False
    data_classification: str = "PUBLIC"
