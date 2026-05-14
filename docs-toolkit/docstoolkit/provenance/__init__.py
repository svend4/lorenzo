"""Span-level provenance and bootstrap confidence intervals for RAG answers."""
from docstoolkit.provenance.claims import Claim, Source, extract_claims, link_sources
from docstoolkit.provenance.answer import ProvenancedAnswer, ask_with_provenance
from docstoolkit.provenance.bootstrap import bootstrap_ci, BootstrapCI

__all__ = [
    "Claim", "Source", "extract_claims", "link_sources",
    "ProvenancedAnswer", "ask_with_provenance",
    "bootstrap_ci", "BootstrapCI",
]
