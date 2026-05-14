"""E402 DocShareAudit — auditable sharing event log for documents.

Public API
----------
:class:`ShareEvent`    — a single share/unshare audit event
:class:`AuditStats`    — aggregate statistics
:class:`DocShareAudit` — main interface for share audit
"""

from .audit import ShareEvent, AuditStats, DocShareAudit

__all__ = ["ShareEvent", "AuditStats", "DocShareAudit"]
