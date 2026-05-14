"""E360 DocDLQStore — dead letter queue for failed document operations.

Public API
----------
:class:`DLQEntry`     — a single failed operation entry
:class:`DLQStats`     — aggregate statistics
:class:`DocDLQStore`  — main interface for DLQ management
"""

from .store import DLQEntry, DLQStats, DocDLQStore

__all__ = ["DLQEntry", "DLQStats", "DocDLQStore"]
