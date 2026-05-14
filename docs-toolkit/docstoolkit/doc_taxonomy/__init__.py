"""Document taxonomy module: manages term hierarchies, categories and classification rules."""

from .taxonomy import (
    Classification,
    ClassificationRule,
    DocTaxonomy,
    TaxonomyTerm,
)

__all__ = [
    "Classification",
    "ClassificationRule",
    "DocTaxonomy",
    "TaxonomyTerm",
]
