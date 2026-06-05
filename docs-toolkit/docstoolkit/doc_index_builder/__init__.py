"""E313 DocIndexBuilder — build and query composite document indexes.

Public API
----------
:class:`IndexField`     — a field definition for the index
:class:`IndexEntry`     — a single indexed document record
:class:`IndexStats`     — aggregate statistics
:class:`DocIndexBuilder` — main interface for index building and querying
"""

from .builder import IndexField, IndexEntry, IndexStats, DocIndexBuilder

__all__ = ["IndexField", "IndexEntry", "IndexStats", "DocIndexBuilder"]
