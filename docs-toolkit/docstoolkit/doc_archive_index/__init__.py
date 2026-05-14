"""E432 DocArchiveIndex — searchable index of archived documents.

Public API
----------
:class:`ArchiveEntry`   — a single archive index entry
:class:`ArchiveStats`   — aggregate statistics
:class:`DocArchiveIndex` — main interface for archive indexing
"""

from .index import ArchiveEntry, ArchiveStats, DocArchiveIndex

__all__ = ["ArchiveEntry", "ArchiveStats", "DocArchiveIndex"]
