"""Search index manager module for docs-toolkit (E62)."""
from docstoolkit.search_index_mgr.index import (
    IndexEntry,
    IndexStats,
)
from docstoolkit.search_index_mgr.manager import (
    IndexConfig,
    SearchIndexManager,
)
from docstoolkit.search_index_mgr.persistence import (
    IndexPersistence,
)

__all__ = [
    # index
    "IndexEntry",
    "IndexStats",
    # manager
    "IndexConfig",
    "SearchIndexManager",
    # persistence
    "IndexPersistence",
]
