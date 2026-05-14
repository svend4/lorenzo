"""E143 Document search — boolean and phrase search, stdlib only.

Public API
----------
:class:`MatchType`   — enum of match strategies (EXACT, PHRASE, FUZZY, REGEX)
:class:`SearchHit`   — a single result with score, snippets, match count
:class:`SearchQuery` — structured query for :meth:`DocSearch.search_advanced`
:class:`DocSearch`   — index/search engine over a collection of documents
"""
from .search import DocSearch, MatchType, SearchHit, SearchQuery

__all__ = [
    "DocSearch",
    "MatchType",
    "SearchHit",
    "SearchQuery",
]
