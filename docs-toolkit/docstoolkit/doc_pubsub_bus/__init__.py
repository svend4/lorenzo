"""E338 DocPubSubBus — simple in-process pub/sub bus with wildcard subscriptions.

Public API
----------
:class:`PubSubEvent`    — a single event dispatched on the bus
:class:`SubscriberInfo` — info about a registered subscriber
:class:`PubSubStats`    — aggregate statistics
:class:`DocPubSubBus`   — main interface for event publishing and subscription
"""

from .bus import PubSubEvent, SubscriberInfo, PubSubStats, DocPubSubBus

__all__ = ["PubSubEvent", "SubscriberInfo", "PubSubStats", "DocPubSubBus"]
