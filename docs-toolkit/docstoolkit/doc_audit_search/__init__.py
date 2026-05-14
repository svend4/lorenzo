"""E343 DocAuditSearch — searchable audit log index for documents.

Public API
----------
:class:`AuditEntry`        — a single auditable action record
:class:`AuditSearchQuery`  — a search query against the audit log
:class:`AuditStats`        — aggregate statistics
:class:`DocAuditSearch`    — main interface for audit search
"""

from .search import AuditEntry, AuditSearchQuery, AuditStats, DocAuditSearch

__all__ = ["AuditEntry", "AuditSearchQuery", "AuditStats", "DocAuditSearch"]
