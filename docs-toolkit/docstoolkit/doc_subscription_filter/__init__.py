"""E422 DocSubscriptionFilter — filter rules on subscription events.

Public API
----------
:class:`SubFilter`            — a subscription filter rule
:class:`FilterMatchResult`    — outcome of a filter evaluation
:class:`SubFilterStats`       — aggregate statistics
:class:`DocSubscriptionFilter` — main interface for subscription filtering
"""

from .filter import SubFilter, FilterMatchResult, SubFilterStats, DocSubscriptionFilter

__all__ = ["SubFilter", "FilterMatchResult", "SubFilterStats", "DocSubscriptionFilter"]
