"""E321 DocSubscriptionManager — manage user subscriptions to document events.

Public API
----------
:class:`Subscription`        — a user's subscription to a doc or topic
:class:`SubscriptionStats`   — aggregate statistics
:class:`DocSubscriptionManager` — main interface for subscription management
"""

from .manager import Subscription, SubscriptionStats, DocSubscriptionManager

__all__ = ["Subscription", "SubscriptionStats", "DocSubscriptionManager"]
