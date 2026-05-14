"""DocNotificationCenter — in-memory pub/sub notification center (E282).

Subscribe to topics using exact names or fnmatch patterns, publish messages,
pause/resume subscriptions, and query delivery history.

Usage::

    from docstoolkit.doc_notification_center import (
        DocNotificationCenter,
        Notification,
        NotifStats,
        Subscription,
    )

    center = DocNotificationCenter()
    sub = center.subscribe("doc.*", lambda n: print(n.payload))
    center.publish("doc.created", {"id": "abc"}, sender="api")
"""

from __future__ import annotations

from .center import DocNotificationCenter, Notification, NotifStats, Subscription

__all__ = [
    "DocNotificationCenter",
    "Notification",
    "NotifStats",
    "Subscription",
]
