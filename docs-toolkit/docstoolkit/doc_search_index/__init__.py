"""E300 DocSearchIndex — inverted index for full-text document search.

Public API
----------
:class:`IndexedDoc`    — a single indexed document entry
:class:`SearchResult`  — a single search result with score
:class:`IndexStats`    — aggregate statistics for the index
:class:`DocSearchIndex` — main interface for indexing and searching
"""

from .index import IndexedDoc, SearchResult, IndexStats, DocSearchIndex

__all__ = ["IndexedDoc", "SearchResult", "IndexStats", "DocSearchIndex"]
