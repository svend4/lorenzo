"""E411 DocObserverChain — chained observer notifications for doc events.

Public API
----------
:class:`Observer`         — a registered observer
:class:`NotifyResult`     — outcome of notifying observers
:class:`ChainStats`       — aggregate statistics
:class:`DocObserverChain` — main interface for observer chain
"""

from .chain import Observer, NotifyResult, ChainStats, DocObserverChain

__all__ = ["Observer", "NotifyResult", "ChainStats", "DocObserverChain"]
