"""doc_revision — numbered revision manager with diff, blame, and rollback."""

from .revision import (
    BlameLine,
    DocRevision,
    Revision,
    RevisionDiff,
    RevisionStats,
)

__all__ = [
    "BlameLine",
    "DocRevision",
    "Revision",
    "RevisionDiff",
    "RevisionStats",
]
