"""
Contract, obligation, and evidence models for Lamar PPP OS.

These models provide traceability from project obligations back
to the source documents and clauses from which they originated.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass
class Evidence:
    """
    Source evidence supporting a structured fact or obligation.

    AI-generated interpretations should retain a reference to
    their underlying source wherever possible.
    """

    document_name: str
    page_number: Optional[int] = None
    clause_reference: Optional[str] = None
    source_text: Optional[str] = None


@dataclass
class ContractClause:
    """A clause extracted from a PPP-related document."""

    clause_id: str
    title: str
    text: str
    evidence: Optional[Evidence] = None


@dataclass
class Obligation:
    """
    A contractual or project obligation assigned to a party.

    Obligations remain evidence-backed so users can inspect the
    source before taking consequential action.
    """

    obligation_id: str
    description: str
    responsible_party: str

    due_date: Optional[date] = None
    status: str = "OPEN"
    criticality: str = "MEDIUM"

    evidence: List[Evidence] = field(default_factory=list)


@dataclass
class Contract:
    """A contract or agreement associated with a PPP project."""

    contract_id: str
    project_id: str
    name: str
    contract_type: str

    parties: List[str] = field(default_factory=list)
    clauses: List[ContractClause] = field(default_factory=list)
    obligations: List[Obligation] = field(default_factory=list)

    data_classification: str = "PUBLIC"
