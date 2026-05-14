"""Notification router: route events to registered handlers by channel.

Public API
----------
- ``DeliveryStatus``     — SENT | FAILED | FILTERED
- ``Notification``       — an event to be delivered (event_type, channel, payload, …)
- ``DeliveryRecord``     — result of one delivery attempt
- ``HandlerConfig``      — binds a callable to a channel with optional filters
- ``NotificationRouter`` — registry and dispatcher with full delivery history
"""

from docstoolkit.notification_router.router import (
    DeliveryStatus,
    Notification,
    DeliveryRecord,
    HandlerConfig,
    NotificationRouter,
)

__all__ = [
    "DeliveryStatus",
    "Notification",
    "DeliveryRecord",
    "HandlerConfig",
    "NotificationRouter",
]
