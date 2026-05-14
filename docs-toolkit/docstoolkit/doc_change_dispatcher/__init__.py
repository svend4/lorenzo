"""E405 DocChangeDispatcher — dispatch document changes to handlers.

Public API
----------
:class:`Handler`              — a registered handler
:class:`DispatchResult`       — outcome of dispatching one change
:class:`DispatcherStats`      — aggregate statistics
:class:`DocChangeDispatcher`  — main interface for change dispatch
"""

from .dispatcher import Handler, DispatchResult, DispatcherStats, DocChangeDispatcher

__all__ = ["Handler", "DispatchResult", "DispatcherStats", "DocChangeDispatcher"]
