"""Full-text positional index with light stemming and proximity search."""

from .index import DocIndexFull, IndexEntry, IndexStats, Match

__all__ = ["DocIndexFull", "IndexEntry", "IndexStats", "Match"]
