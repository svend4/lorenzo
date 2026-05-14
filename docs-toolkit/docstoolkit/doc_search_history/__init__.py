"""E325 DocSearchHistory — per-user search query history with analytics.

Public API
----------
:class:`SearchQuery`         — a single recorded search query
:class:`QueryStats`          — aggregate statistics for a query
:class:`HistoryStats`        — global aggregate statistics
:class:`DocSearchHistory`    — main interface for search history management
"""

from .history import SearchQuery, QueryStats, HistoryStats, DocSearchHistory

__all__ = ["SearchQuery", "QueryStats", "HistoryStats", "DocSearchHistory"]
