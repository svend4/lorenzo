"""E136 Document index — fast in-memory multi-field index, stdlib only.

Public API
----------
:class:`IndexedDoc`   — a document held in the index
:class:`IndexEntry`   — a single (doc, field) search result
:class:`IndexConfig`  — configuration for :class:`DocIndex`
:class:`DocIndex`     — the index itself, with add/remove/update/search
"""
from .index import DocIndex, IndexConfig, IndexedDoc, IndexEntry

__all__ = [
    "DocIndex",
    "IndexConfig",
    "IndexedDoc",
    "IndexEntry",
]
