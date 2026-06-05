"""E378 DocFacetIndex — inverted index for faceted document search.

Public API
----------
:class:`FacetValue`   — a single facet value with count
:class:`FacetResult`  — facet breakdown
:class:`FacetStats`   — aggregate statistics
:class:`DocFacetIndex` — main interface for facet indexing
"""

from .index import FacetValue, FacetResult, FacetStats, DocFacetIndex

__all__ = ["FacetValue", "FacetResult", "FacetStats", "DocFacetIndex"]
