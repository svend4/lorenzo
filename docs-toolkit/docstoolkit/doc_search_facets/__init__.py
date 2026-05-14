"""Faceted search module with filter aggregation and hierarchical drill-down."""

from .facets import (
    DocSearchFacets,
    FacetedQuery,
    FacetedSearchResult,
    FacetField,
    FacetResult,
    FacetType,
    FacetValue,
)

__all__ = [
    "DocSearchFacets",
    "FacetField",
    "FacetType",
    "FacetValue",
    "FacetResult",
    "FacetedQuery",
    "FacetedSearchResult",
]
