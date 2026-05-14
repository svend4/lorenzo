"""E269 Document index manager — coordinates multiple per-doc indexes.

Public API
----------
:class:`IndexKind`        — kinds of indexes (KEYWORD, METADATA, etc.)
:class:`IndexDefinition`  — definition of a single registered index
:class:`IndexedTerm`      — single term entry stored in an index
:class:`DocIndexManager`  — manager coordinating multiple indexes
"""
from .manager import (
    DocIndexManager,
    IndexDefinition,
    IndexedTerm,
    IndexKind,
)

__all__ = [
    "DocIndexManager",
    "IndexDefinition",
    "IndexedTerm",
    "IndexKind",
]
