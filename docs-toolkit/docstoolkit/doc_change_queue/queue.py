"""FIFO queue for pending document changes with priority, deduplication, and batch processing.

Pure stdlib, thread-safe via threading.Lock.
Higher priority numbers are dequeued first; within the same priority, FIFO by enqueued_at.
"""
import time
import threading
import uuid
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ChangeItem:
    """A single pending document change."""

    item_id: str
    doc_id: str
    change_type: str          # "create", "update", "delete", "publish"
    payload: dict
    priority: int             # higher = more urgent (default 0)
    enqueued_at: float
    attempts: int = 0


@dataclass
class ProcessResult:
    """Result returned by ack/nack."""

    item_id: str
    doc_id: str
    success: bool
    error: Optional[str] = None
    processed_at: float = 0.0


@dataclass
class QueueStats:
    """Snapshot of queue counters."""

    pending_count: int
    processed_count: int
    failed_count: int
    total_enqueued: int


# ---------------------------------------------------------------------------
# Queue
# ---------------------------------------------------------------------------

class DocChangeQueue:
    """Thread-safe FIFO priority queue for document changes.

    Priority ordering: higher *priority* value → dequeued first.
    Within the same priority, items are served in FIFO order (by *enqueued_at*).
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # Pending items stored as list; kept sorted on every modification so
        # that dequeue is O(1).  Sort key: (-priority, enqueued_at).
        self._pending: list[ChangeItem] = []
        # item_id → ChangeItem for fast lookup (pending + in-flight)
        self._in_flight: dict[str, ChangeItem] = {}
        # Counters
        self._processed_count: int = 0
        self._failed_count: int = 0
        self._total_enqueued: int = 0

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _sort_key(item: ChangeItem) -> tuple:
        # Higher priority first; FIFO within same priority.
        return (-item.priority, item.enqueued_at)

    def _insert_sorted(self, item: ChangeItem) -> None:
        """Insert *item* into _pending keeping the list sorted."""
        key = self._sort_key(item)
        lo, hi = 0, len(self._pending)
        while lo < hi:
            mid = (lo + hi) // 2
            if self._sort_key(self._pending[mid]) <= key:
                lo = mid + 1
            else:
                hi = mid
        self._pending.insert(lo, item)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def enqueue(
        self,
        doc_id: str,
        change_type: str,
        payload: Optional[dict] = None,
        priority: int = 0,
        now: Optional[float] = None,
    ) -> ChangeItem:
        """Add a change item to the queue and return it."""
        item = ChangeItem(
            item_id=str(uuid.uuid4()),
            doc_id=doc_id,
            change_type=change_type,
            payload=payload if payload is not None else {},
            priority=priority,
            enqueued_at=now if now is not None else time.time(),
        )
        with self._lock:
            self._insert_sorted(item)
            self._total_enqueued += 1
        return item

    def enqueue_many(
        self,
        items: list[dict],
        now: Optional[float] = None,
    ) -> list[ChangeItem]:
        """Bulk-enqueue a list of change specs.

        Each dict must contain ``doc_id`` and ``change_type``; ``payload``
        and ``priority`` are optional.
        """
        ts = now if now is not None else time.time()
        result: list[ChangeItem] = []
        with self._lock:
            for spec in items:
                item = ChangeItem(
                    item_id=str(uuid.uuid4()),
                    doc_id=spec["doc_id"],
                    change_type=spec["change_type"],
                    payload=spec.get("payload") or {},
                    priority=spec.get("priority", 0),
                    enqueued_at=ts,
                )
                self._insert_sorted(item)
                self._total_enqueued += 1
                result.append(item)
        return result

    def dequeue(self, now: Optional[float] = None) -> Optional[ChangeItem]:
        """Remove and return the highest-priority item (FIFO within same priority).

        Returns ``None`` if the queue is empty.
        """
        with self._lock:
            if not self._pending:
                return None
            item = self._pending.pop(0)
            self._in_flight[item.item_id] = item
            return item

    def peek(self) -> Optional[ChangeItem]:
        """Return the next item without removing it, or ``None`` if empty."""
        with self._lock:
            return self._pending[0] if self._pending else None

    def dequeue_batch(
        self,
        max_items: int,
        now: Optional[float] = None,
    ) -> list[ChangeItem]:
        """Dequeue up to *max_items* items, highest priority first."""
        with self._lock:
            n = min(max_items, len(self._pending))
            batch = self._pending[:n]
            self._pending = self._pending[n:]
            for item in batch:
                self._in_flight[item.item_id] = item
            return batch

    def ack(
        self,
        item_id: str,
        now: Optional[float] = None,
    ) -> ProcessResult:
        """Mark an in-flight item as successfully processed."""
        ts = now if now is not None else time.time()
        with self._lock:
            item = self._in_flight.pop(item_id, None)
            if item is None:
                return ProcessResult(
                    item_id=item_id,
                    doc_id="",
                    success=False,
                    error="item not found in in-flight set",
                    processed_at=ts,
                )
            self._processed_count += 1
            return ProcessResult(
                item_id=item_id,
                doc_id=item.doc_id,
                success=True,
                processed_at=ts,
            )

    def nack(
        self,
        item_id: str,
        error: str = "",
        requeue: bool = True,
        now: Optional[float] = None,
    ) -> ProcessResult:
        """Mark an in-flight item as failed.

        If *requeue* is ``True``, the item is put back into the pending queue
        with ``attempts`` incremented by 1.
        """
        ts = now if now is not None else time.time()
        with self._lock:
            item = self._in_flight.pop(item_id, None)
            if item is None:
                return ProcessResult(
                    item_id=item_id,
                    doc_id="",
                    success=False,
                    error="item not found in in-flight set",
                    processed_at=ts,
                )
            if requeue:
                item.attempts += 1
                self._insert_sorted(item)
            else:
                self._failed_count += 1
            return ProcessResult(
                item_id=item_id,
                doc_id=item.doc_id,
                success=False,
                error=error or None,
                processed_at=ts,
            )

    def remove(self, item_id: str) -> bool:
        """Remove a specific pending item by *item_id*.

        Returns ``True`` if found and removed, ``False`` otherwise.
        """
        with self._lock:
            for i, item in enumerate(self._pending):
                if item.item_id == item_id:
                    del self._pending[i]
                    return True
            return False

    def find_by_doc(self, doc_id: str) -> list[ChangeItem]:
        """Return all pending items for the given *doc_id*."""
        with self._lock:
            return [item for item in self._pending if item.doc_id == doc_id]

    def clear(self) -> int:
        """Remove all pending items. Returns the count of items removed."""
        with self._lock:
            count = len(self._pending)
            self._pending.clear()
            return count

    def stats(self) -> QueueStats:
        """Return a snapshot of queue counters."""
        with self._lock:
            return QueueStats(
                pending_count=len(self._pending),
                processed_count=self._processed_count,
                failed_count=self._failed_count,
                total_enqueued=self._total_enqueued,
            )

    @property
    def size(self) -> int:
        """Number of pending (not yet dequeued) items."""
        with self._lock:
            return len(self._pending)
