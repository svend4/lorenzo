"""E393 DocChangeSubscriber — subscribe to document change events with delivery.

Public API
----------
:class:`Subscription`          — a single subscription
:class:`DeliveryRecord`        — a delivered notification record
:class:`SubscriberStats`       — aggregate statistics
:class:`DocChangeSubscriber`   — main interface for subscription management
"""

from .subscriber import Subscription, DeliveryRecord, SubscriberStats, DocChangeSubscriber

__all__ = ["Subscription", "DeliveryRecord", "SubscriberStats", "DocChangeSubscriber"]
