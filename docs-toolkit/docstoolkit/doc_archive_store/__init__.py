"""E316 DocArchiveStore — archive and restore document versions.

Public API
----------
:class:`ArchivedDoc`    — a single archived document snapshot
:class:`ArchiveStats`   — aggregate statistics
:class:`DocArchiveStore` — main interface for archiving and restoring
"""

from .store import ArchivedDoc, ArchiveStats, DocArchiveStore

__all__ = ["ArchivedDoc", "ArchiveStats", "DocArchiveStore"]
