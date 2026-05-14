"""E427 DocVersioningIndex — fast lookup index of doc versions.

Public API
----------
:class:`VersionRef`        — a version reference
:class:`VersioningStats`   — aggregate statistics
:class:`DocVersioningIndex` — main interface for versioning index
"""

from .index import VersionRef, VersioningStats, DocVersioningIndex

__all__ = ["VersionRef", "VersioningStats", "DocVersioningIndex"]
