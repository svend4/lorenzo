"""E352 DocTaskQueue — heapq-based priority queue for document tasks.

Thread-safe via :class:`threading.Lock`. Uses only Python stdlib.

Priority semantics: higher numeric ``priority`` value pops first.
Within the same priority, items are FIFO by ``enqueued_at``.
"""

from __future__ import annotations

import heapq
import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class QueueItem:
    """A single queued document task."""

    item_id: int = 0
    doc_id: str = ""
    payload: dict = field(default_factory=dict)
    priority: int = 0
    enqueued_at: float = 0.0
    status: str = "queued"


@dataclass
class QueueStats:
    """Aggregate counts for the queue."""

    total: int = 0
    queued: int = 0
    processed: int = 0
    skipped: int = 0


class DocTaskQueue:
    """Priority queue of document tasks backed by :mod:`heapq`."""

    def __init__(self) -> None:
        self._items: dict[int, QueueItem] = {}
        self._heap: list[tuple[int, float, int]] = []
        self._next_id: int = 1
        self._lock = threading.Lock()

    # ---------------------------------------------------------------- enqueue
    def enqueue(
        self,
        doc_id: str,
        payload: Optional[dict] = None,
        priority: int = 0,
        now: Optional[float] = None,
    ) -> QueueItem:
        """Push a new task onto the heap and return it."""
        with self._lock:
            item_id = self._next_id
            self._next_id += 1
            ts = float(now) if now is not None else time.time()
            item = QueueItem(
                item_id=item_id,
                doc_id=doc_id,
                payload=dict(payload) if payload else {},
                priority=int(priority),
                enqueued_at=ts,
                status="queued",
            )
            self._items[item_id] = item
            heapq.heappush(self._heap, (-item.priority, item.enqueued_at, item_id))
            return item

    # -------------------------------------------------------------------- pop
    def pop(self) -> Optional[QueueItem]:
        """Return highest-priority queued item, mark as ``processed``.

        Stale heap entries (items not currently ``queued``) are skipped.
        Returns ``None`` when no queued items remain.
        """
        with self._lock:
            while self._heap:
                _, _, item_id = heapq.heappop(self._heap)
                item = self._items.get(item_id)
                if item is None:
                    continue
                if item.status != "queued":
                    continue
                item.status = "processed"
                return item
            return None

    # ------------------------------------------------------------------- peek
    def peek(self) -> Optional[QueueItem]:
        """Return highest-priority queued item without state change."""
        with self._lock:
            # Drain stale entries off the top, but DO restore unique heap state
            # without altering item status.
            while self._heap:
                key = self._heap[0]
                item_id = key[2]
                item = self._items.get(item_id)
                if item is None or item.status != "queued":
                    heapq.heappop(self._heap)
                    continue
                return item
            return None

    # -------------------------------------------------------- mark_processed
    def mark_processed(self, item_id: int) -> bool:
        """Mark a queued item as ``processed``. Returns True on success."""
        with self._lock:
            item = self._items.get(item_id)
            if item is None or item.status != "queued":
                return False
            item.status = "processed"
            return True

    # ---------------------------------------------------------- mark_skipped
    def mark_skipped(self, item_id: int) -> bool:
        """Mark a queued item as ``skipped``. Returns True on success."""
        with self._lock:
            item = self._items.get(item_id)
            if item is None or item.status != "queued":
                return False
            item.status = "skipped"
            return True

    # ---------------------------------------------------------------- requeue
    def requeue(self, item_id: int, now: Optional[float] = None) -> bool:
        """Re-add a processed/skipped item to the heap.

        Returns True if the item existed and was not already queued.
        """
        with self._lock:
            item = self._items.get(item_id)
            if item is None:
                return False
            if item.status == "queued":
                return False
            ts = float(now) if now is not None else time.time()
            item.enqueued_at = ts
            item.status = "queued"
            heapq.heappush(self._heap, (-item.priority, item.enqueued_at, item_id))
            return True

    # -------------------------------------------------------------------- get
    def get(self, item_id: int) -> Optional[QueueItem]:
        """Return the item by id, or ``None``."""
        with self._lock:
            return self._items.get(item_id)

    # ---------------------------------------------------------- queued_items
    def queued_items(self) -> list[QueueItem]:
        """Return all currently queued items, sorted by (-priority, enqueued_at)."""
        with self._lock:
            items = [it for it in self._items.values() if it.status == "queued"]
        items.sort(key=lambda it: (-it.priority, it.enqueued_at, it.item_id))
        return items

    # --------------------------------------------------------- items_for_doc
    def items_for_doc(self, doc_id: str) -> list[QueueItem]:
        """Return all items for a given doc_id, sorted by enqueued_at."""
        with self._lock:
            items = [it for it in self._items.values() if it.doc_id == doc_id]
        items.sort(key=lambda it: (it.enqueued_at, it.item_id))
        return items

    # -------------------------------------------------------- items_by_status
    def items_by_status(self, status: str) -> list[QueueItem]:
        """Return all items having ``status``, sorted by enqueued_at."""
        with self._lock:
            items = [it for it in self._items.values() if it.status == status]
        items.sort(key=lambda it: (it.enqueued_at, it.item_id))
        return items

    # ------------------------------------------------------- clear_processed
    def clear_processed(self) -> int:
        """Remove processed and skipped items. Return count removed."""
        with self._lock:
            to_remove = [
                iid for iid, it in self._items.items()
                if it.status in ("processed", "skipped")
            ]
            for iid in to_remove:
                del self._items[iid]
            return len(to_remove)

    # ------------------------------------------------------------- queue_size
    def queue_size(self) -> int:
        """Number of currently queued items."""
        with self._lock:
            return sum(1 for it in self._items.values() if it.status == "queued")

    # ------------------------------------------------------------------ stats
    def stats(self) -> QueueStats:
        """Aggregate counts by status."""
        with self._lock:
            total = len(self._items)
            queued = sum(1 for it in self._items.values() if it.status == "queued")
            processed = sum(1 for it in self._items.values() if it.status == "processed")
            skipped = sum(1 for it in self._items.values() if it.status == "skipped")
        return QueueStats(total=total, queued=queued, processed=processed, skipped=skipped)
