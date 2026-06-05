"""Secure share-link generation and management for documents.

Public API
----------
- ``ShareStatus``     — enum of share-link statuses (ACTIVE, EXPIRED, REVOKED, EXHAUSTED)
- ``PermissionLevel`` — enum of granted permissions (VIEW, COMMENT, EDIT)
- ``ShareLink``       — dataclass describing a share record
- ``AccessRecord``    — dataclass describing a single access attempt
- ``ShareStats``      — aggregate counters across the store
- ``DocShare``        — thread-safe in-memory manager

All cryptography is stdlib-only: ``secrets``, ``hashlib``, ``hmac``.
"""

from docstoolkit.doc_share.share import (
    ShareStatus,
    PermissionLevel,
    ShareLink,
    AccessRecord,
    ShareStats,
    DocShare,
)

__all__ = [
    "ShareStatus",
    "PermissionLevel",
    "ShareLink",
    "AccessRecord",
    "ShareStats",
    "DocShare",
]
