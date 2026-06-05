"""Self-organizing taxonomy: emergent document categorization via clustering."""
from docstoolkit.taxonomy.node import TaxonomyNode, TaxonomyTree
from docstoolkit.taxonomy.builder import build_taxonomy, TaxonomyConfig
from docstoolkit.taxonomy.drift import detect_drift, DriftReport, TaxonomySnapshot

__all__ = [
    "TaxonomyNode", "TaxonomyTree",
    "build_taxonomy", "TaxonomyConfig",
    "detect_drift", "DriftReport", "TaxonomySnapshot",
]
