"""E408 DocSubscriptionIndex — efficient subscription index by topic.

Public API
----------
:class:`SubscriptionEntry`  — a single subscription
:class:`IndexStats`         — aggregate statistics
:class:`DocSubscriptionIndex` — main interface for subscription indexing
"""

from .index import SubscriptionEntry, IndexStats, DocSubscriptionIndex

__all__ = ["SubscriptionEntry", "IndexStats", "DocSubscriptionIndex"]
