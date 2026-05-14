"""Incremental indexing module for docs-toolkit (E32)."""
from docstoolkit.incremental_index.change import (
    ChangeType,
    DocumentChange,
    ChangeDetector,
)
from docstoolkit.incremental_index.queue import (
    IndexJob,
    IndexQueue,
)
from docstoolkit.incremental_index.indexer import (
    IndexConfig,
    IndexStats,
    IncrementalIndexer,
)

__all__ = [
    # change
    "ChangeType",
    "DocumentChange",
    "ChangeDetector",
    # queue
    "IndexJob",
    "IndexQueue",
    # indexer
    "IndexConfig",
    "IndexStats",
    "IncrementalIndexer",
]
