"""Subscription manager for document change notifications.

Supports filtering by doc_id, change kind, tags, priority, and batched delivery.
Uses stdlib threading only.
"""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional, Union


class ChangeKind(Enum):
    """Kinds of document changes."""

    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    TAGGED = "tagged"
    MOVED = "moved"


@dataclass
class DocChange:
    """A change event for a document."""

    doc_id: str
    kind: ChangeKind
    timestamp: float
    details: dict = field(default_factory=dict)


@dataclass
class SubscriptionFilter:
    """Filter criteria for subscriptions."""

    doc_ids: Optional[list[str]] = None
    kinds: Optional[list[ChangeKind]] = None
    tags: Optional[list[str]] = None
    min_priority: int = 0


@dataclass
class Subscription:
    """A subscription registration."""

    sub_id: str
    subscriber_id: str
    callback: Callable[[Union[DocChange, list[DocChange]]], None]
    filter: SubscriptionFilter
    created_at: float
    batch_size: int = 1
    _buffer: list[DocChange] = field(default_factory=list, repr=False)


class DocSubscriber:
    """Manages subscriptions to document change notifications."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._subs: dict[str, Subscription] = {}

    # ------------------------------------------------------------------
    # Subscription management
    # ------------------------------------------------------------------
    def subscribe(
        self,
        subscriber_id: str,
        callback: Callable,
        filter: Optional[SubscriptionFilter] = None,
        batch_size: int = 1,
        now: float = 0.0,
    ) -> str:
        """Register a subscription. Returns the new sub_id."""
        if batch_size < 1:
            raise ValueError("batch_size must be >= 1")
        if filter is None:
            filter = SubscriptionFilter()
        sub_id = uuid.uuid4().hex
        sub = Subscription(
            sub_id=sub_id,
            subscriber_id=subscriber_id,
            callback=callback,
            filter=filter,
            created_at=now,
            batch_size=batch_size,
        )
        with self._lock:
            self._subs[sub_id] = sub
        return sub_id

    def unsubscribe(self, sub_id: str) -> bool:
        """Remove a subscription. Returns True if it existed."""
        with self._lock:
            if sub_id in self._subs:
                del self._subs[sub_id]
                return True
            return False

    def unsubscribe_all(self, subscriber_id: str) -> int:
        """Remove all subscriptions for a subscriber. Returns count removed."""
        with self._lock:
            to_remove = [
                sid for sid, sub in self._subs.items()
                if sub.subscriber_id == subscriber_id
            ]
            for sid in to_remove:
                del self._subs[sid]
            return len(to_remove)

    # ------------------------------------------------------------------
    # Filter matching
    # ------------------------------------------------------------------
    @staticmethod
    def matches_filter(change: DocChange, filter: SubscriptionFilter) -> bool:
        """Return True if change matches the filter."""
        if filter.doc_ids is not None and change.doc_id not in filter.doc_ids:
            return False
        if filter.kinds is not None and change.kind not in filter.kinds:
            return False
        if filter.tags is not None:
            change_tags = change.details.get("tags") or []
            if not any(t in change_tags for t in filter.tags):
                return False
        priority = change.details.get("priority", 0)
        if priority < filter.min_priority:
            return False
        return True

    # ------------------------------------------------------------------
    # Notification
    # ------------------------------------------------------------------
    def notify(self, change: DocChange) -> int:
        """Deliver change to matching subscribers. Returns count notified."""
        # Collect deliveries inside lock, fire callbacks outside lock.
        single_deliveries: list[tuple[Callable, DocChange]] = []
        batch_deliveries: list[tuple[Callable, list[DocChange]]] = []

        with self._lock:
            matched = 0
            for sub in self._subs.values():
                if not self.matches_filter(change, sub.filter):
                    continue
                matched += 1
                if sub.batch_size == 1:
                    single_deliveries.append((sub.callback, change))
                else:
                    sub._buffer.append(change)
                    if len(sub._buffer) >= sub.batch_size:
                        batch_deliveries.append(
                            (sub.callback, list(sub._buffer))
                        )
                        sub._buffer.clear()

        # Fire callbacks outside the lock.
        for cb, c in single_deliveries:
            try:
                cb(c)
            except Exception:
                pass
        for cb, buf in batch_deliveries:
            try:
                cb(buf)
            except Exception:
                pass
        return matched

    def notify_batch(self, changes: list[DocChange]) -> int:
        """Deliver many changes. Returns total subscriber notifications."""
        total = 0
        for change in changes:
            total += self.notify(change)
        return total

    def flush(self, sub_id: Optional[str] = None) -> int:
        """Force delivery of buffered changes.

        If sub_id is given, flush only that subscription. Otherwise flush all.
        Returns the total number of buffered changes delivered.
        """
        deliveries: list[tuple[Callable, list[DocChange]]] = []
        delivered = 0
        with self._lock:
            if sub_id is not None:
                sub = self._subs.get(sub_id)
                if sub is not None and sub._buffer:
                    deliveries.append((sub.callback, list(sub._buffer)))
                    delivered += len(sub._buffer)
                    sub._buffer.clear()
            else:
                for sub in self._subs.values():
                    if sub._buffer:
                        deliveries.append((sub.callback, list(sub._buffer)))
                        delivered += len(sub._buffer)
                        sub._buffer.clear()

        for cb, buf in deliveries:
            try:
                cb(buf)
            except Exception:
                pass
        return delivered

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------
    def subscriptions_for(self, subscriber_id: str) -> list[Subscription]:
        """All subscriptions belonging to a subscriber."""
        with self._lock:
            return [
                sub for sub in self._subs.values()
                if sub.subscriber_id == subscriber_id
            ]

    @property
    def subscription_count(self) -> int:
        with self._lock:
            return len(self._subs)

    @property
    def subscriber_count(self) -> int:
        with self._lock:
            return len({sub.subscriber_id for sub in self._subs.values()})

    def pending_count(self, sub_id: str) -> int:
        """Number of changes currently buffered for a subscription."""
        with self._lock:
            sub = self._subs.get(sub_id)
            if sub is None:
                return 0
            return len(sub._buffer)

    def clear(self) -> None:
        """Remove all subscriptions and buffered changes."""
        with self._lock:
            self._subs.clear()
