"""IndexEntry and IndexStats dataclasses for the search index manager (E62)."""
from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class IndexEntry:
    """Represents a single document in the search index."""

    doc_id: str
    title: str
    content: str
    tags: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    indexed_at: float = field(default_factory=time.time)


@dataclass
class IndexStats:
    """Aggregate statistics for a SearchIndexManager instance."""

    total_docs: int
    total_terms: int
    avg_doc_length: float
    last_updated: float
