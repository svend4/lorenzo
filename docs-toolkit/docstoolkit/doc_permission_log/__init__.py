"""doc_permission_log — append-only permission audit log (E296).

Provides grant/deny/revoke event tracking for documents with
thread-safe, pure-stdlib in-memory storage.
"""
from docstoolkit.doc_permission_log.log import (
    DocPermissionLog,
    PermissionEvent,
    PermissionSummary,
    PermLogStats,
)

__all__ = [
    "DocPermissionLog",
    "PermissionEvent",
    "PermissionSummary",
    "PermLogStats",
]
