"""E423 DocInboxRouter — route incoming document messages to inboxes.

Public API
----------
:class:`RoutingRule`     — a routing rule
:class:`RoutedMessage`   — a delivered routed message
:class:`RouterStats`     — aggregate statistics
:class:`DocInboxRouter`  — main interface for inbox routing
"""

from .router import RoutingRule, RoutedMessage, RouterStats, DocInboxRouter

__all__ = ["RoutingRule", "RoutedMessage", "RouterStats", "DocInboxRouter"]
