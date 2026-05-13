"""doc_keyword_index — efficient inverted keyword index with phrase support and snippets."""

from .index import (
    DocKeywordIndex,
    IndexEntry,
    IndexStats,
    MatchHit,
)

__all__ = [
    "DocKeywordIndex",
    "IndexEntry",
    "IndexStats",
    "MatchHit",
]
