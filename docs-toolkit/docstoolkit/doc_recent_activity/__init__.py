"""E416 DocRecentActivity — track and query recent document activities.

Public API
----------
:class:`Activity`            — a single activity event
:class:`ActivityStats`       — aggregate statistics
:class:`DocRecentActivity`   — main interface for activity tracking
"""

from .activity import Activity, ActivityStats, DocRecentActivity

__all__ = ["Activity", "ActivityStats", "DocRecentActivity"]
