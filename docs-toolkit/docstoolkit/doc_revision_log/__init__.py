"""E340 DocRevisionLog — chronological revision log with revision content.

Public API
----------
:class:`Revision`          — a single revision of a document
:class:`RevisionLogStats`  — aggregate statistics
:class:`DocRevisionLog`    — main interface for revision log management
"""

from .log import Revision, RevisionLogStats, DocRevisionLog

__all__ = ["Revision", "RevisionLogStats", "DocRevisionLog"]
