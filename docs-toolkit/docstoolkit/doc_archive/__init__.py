"""E181 Document archive — compressed archival with retention policies.

Public API
----------
:class:`ArchivedDoc`     — metadata describing one archived document
:class:`RetentionPolicy` — policy controlling automatic eviction
:class:`ArchiveStats`    — aggregate statistics over the archive
:class:`DocArchive`      — main archive class (gzip + SQLite)
"""
from docstoolkit.doc_archive.archive import (
    ArchivedDoc,
    ArchiveStats,
    DocArchive,
    RetentionPolicy,
)

__all__ = [
    "ArchivedDoc",
    "ArchiveStats",
    "DocArchive",
    "RetentionPolicy",
]
