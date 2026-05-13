"""doc_search_v2 — enhanced document search with BM25, prefix, exact, facets."""

from .search import (
    DocSearchV2,
    Facet,
    MatchMode,
    SearchHit,
    SearchRequest,
    SearchResult,
)

__all__ = [
    "DocSearchV2",
    "Facet",
    "MatchMode",
    "SearchHit",
    "SearchRequest",
    "SearchResult",
]
