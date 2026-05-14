"""doc_word_index — inverted word index for fast full-text lookup across documents (E293)."""

from .index import (
    DocWordIndex,
    IndexEntry,
    IndexStats,
    SearchResult,
)

__all__ = [
    "DocWordIndex",
    "IndexEntry",
    "IndexStats",
    "SearchResult",
]
