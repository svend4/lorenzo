"""E326 DocNotificationInbox — per-user notification inbox with read/unread state.

Public API
----------
:class:`Notification`        — a single notification
:class:`InboxStats`          — aggregate statistics
:class:`DocNotificationInbox` — main interface for inbox management
"""

from .inbox import Notification, InboxStats, DocNotificationInbox

__all__ = ["Notification", "InboxStats", "DocNotificationInbox"]
