"""E352 DocTaskQueue — priority queue for document tasks (heapq-based).

Public API
----------
:class:`QueueItem`     — a queued document task
:class:`QueueStats`    — aggregate statistics
:class:`DocTaskQueue`  — main interface for priority queue management
"""

from .queue import QueueItem, QueueStats, DocTaskQueue

__all__ = ["QueueItem", "QueueStats", "DocTaskQueue"]
