"""doc_change_queue — FIFO priority queue for pending document changes (E287)."""
from docstoolkit.doc_change_queue.queue import (
    ChangeItem,
    ProcessResult,
    QueueStats,
    DocChangeQueue,
)

__all__ = [
    "ChangeItem",
    "ProcessResult",
    "QueueStats",
    "DocChangeQueue",
]
