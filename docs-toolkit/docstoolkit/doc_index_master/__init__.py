"""E223 Document index master — registry coordinating multiple indexes.

Public API
----------
:class:`IndexType`      — kinds of registered indexes
:class:`IndexHealth`    — health states for registered indexes
:class:`IndexEntry`     — record describing one registered index
:class:`RegistryStats`  — aggregate statistics about the registry
:class:`DocIndexMaster` — the registry itself, with dispatch/health logic
"""
from .master import (
    DocIndexMaster,
    IndexEntry,
    IndexHealth,
    IndexType,
    IndexUpdater,
    RegistryStats,
)

__all__ = [
    "DocIndexMaster",
    "IndexEntry",
    "IndexHealth",
    "IndexType",
    "IndexUpdater",
    "RegistryStats",
]
