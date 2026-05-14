"""E303 DocExpiryTracker — track document expiry dates and overdue status.

Public API
----------
:class:`ExpiryRecord`    — expiry metadata for a single document
:class:`ExpiryStats`     — aggregate statistics
:class:`DocExpiryTracker` — main interface for expiry tracking
"""

from .tracker import ExpiryRecord, ExpiryStats, DocExpiryTracker

__all__ = ["ExpiryRecord", "ExpiryStats", "DocExpiryTracker"]
