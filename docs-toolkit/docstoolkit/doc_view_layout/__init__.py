"""E396 DocViewLayout — per-user view layout preferences.

Public API
----------
:class:`ViewLayout`        — a single saved view layout
:class:`ViewLayoutStats`   — aggregate statistics
:class:`DocViewLayout`     — main interface for view layout management
"""

from .layout import ViewLayout, ViewLayoutStats, DocViewLayout

__all__ = ["ViewLayout", "ViewLayoutStats", "DocViewLayout"]
