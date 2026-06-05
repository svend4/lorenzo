"""E380 DocEventFilter — filter chain for document event streams.

Public API
----------
:class:`FilterRule`     — a single filter rule
:class:`FilterResult`   — outcome of applying filters to an event
:class:`FilterStats`    — aggregate statistics
:class:`DocEventFilter` — main interface for event filtering
"""

from .filter import FilterRule, FilterResult, FilterStats, DocEventFilter

__all__ = ["FilterRule", "FilterResult", "FilterStats", "DocEventFilter"]
