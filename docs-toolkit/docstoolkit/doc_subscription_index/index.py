"""Implementation of E408 DocSubscriptionIndex.

A thread-safe, pure-stdlib subscription index that maps subscribers to topics
and supports efficient lookup in either direction.
"""

from __future__ import annotations

import threading
import time
import uuid
from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class SubscriptionEntry:
    """A single subscription tying a subscriber to a topic."""

    sub_id: str
    subscriber_id: str
    topic: str
    created_at: float = 0.0
    active: bool = True


@dataclass
class IndexStats:
    """Aggregate statistics for a :class:`DocSubscriptionIndex`."""

    total_subscriptions: int
    active_subscriptions: int
    unique_topics: int
    unique_subscribers: int


class DocSubscriptionIndex:
    """Efficient, thread-safe subscription index keyed by topic and subscriber.

    Topics are matched exactly (no wildcards). All public methods are safe to
    call from multiple threads.
    """

    def __init__(self) -> None:
        self._subs: Dict[str, SubscriptionEntry] = {}
        self._by_topic: Dict[str, Set[str]] = {}
        self._by_subscriber: Dict[str, Set[str]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def subscribe(
        self,
        subscriber_id: str,
        topic: str,
        now: Optional[float] = None,
    ) -> SubscriptionEntry:
        """Create a new active subscription and return it."""
        if not subscriber_id:
            raise ValueError("subscriber_id must be non-empty")
        if not topic:
            raise ValueError("topic must be non-empty")

        created_at = float(now) if now is not None else time.time()
        sub_id = uuid.uuid4().hex
        entry = SubscriptionEntry(
            sub_id=sub_id,
            subscriber_id=subscriber_id,
            topic=topic,
            created_at=created_at,
            active=True,
        )
        with self._lock:
            self._subs[sub_id] = entry
            self._by_topic.setdefault(topic, set()).add(sub_id)
            self._by_subscriber.setdefault(subscriber_id, set()).add(sub_id)
        return entry

    def unsubscribe(self, sub_id: str) -> bool:
        """Deactivate a subscription. Returns True if the id existed."""
        with self._lock:
            entry = self._subs.get(sub_id)
            if entry is None:
                return False
            entry.active = False
            return True

    def delete(self, sub_id: str) -> bool:
        """Fully remove a subscription. Returns True if the id existed."""
        with self._lock:
            entry = self._subs.pop(sub_id, None)
            if entry is None:
                return False
            topic_subs = self._by_topic.get(entry.topic)
            if topic_subs is not None:
                topic_subs.discard(sub_id)
                if not topic_subs:
                    self._by_topic.pop(entry.topic, None)
            sub_subs = self._by_subscriber.get(entry.subscriber_id)
            if sub_subs is not None:
                sub_subs.discard(sub_id)
                if not sub_subs:
                    self._by_subscriber.pop(entry.subscriber_id, None)
            return True

    def clear_topic(self, topic: str) -> int:
        """Delete every subscription for the given topic. Returns count."""
        with self._lock:
            sub_ids = list(self._by_topic.get(topic, set()))
        count = 0
        for sid in sub_ids:
            if self.delete(sid):
                count += 1
        return count

    def clear_subscriber(self, subscriber_id: str) -> int:
        """Delete every subscription for the given subscriber. Returns count."""
        with self._lock:
            sub_ids = list(self._by_subscriber.get(subscriber_id, set()))
        count = 0
        for sid in sub_ids:
            if self.delete(sid):
                count += 1
        return count

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(self, sub_id: str) -> Optional[SubscriptionEntry]:
        """Return the entry for ``sub_id`` or None."""
        with self._lock:
            return self._subs.get(sub_id)

    def is_subscribed(self, subscriber_id: str, topic: str) -> bool:
        """Return True iff an active subscription exists for the pair."""
        with self._lock:
            sub_ids = self._by_subscriber.get(subscriber_id, set())
            for sid in sub_ids:
                entry = self._subs.get(sid)
                if entry is not None and entry.active and entry.topic == topic:
                    return True
            return False

    def subscribers_for_topic(
        self, topic: str, active_only: bool = True
    ) -> List[str]:
        """Return sorted unique subscriber ids for ``topic``."""
        result: Set[str] = set()
        with self._lock:
            for sid in self._by_topic.get(topic, set()):
                entry = self._subs.get(sid)
                if entry is None:
                    continue
                if active_only and not entry.active:
                    continue
                result.add(entry.subscriber_id)
        return sorted(result)

    def topics_for_subscriber(
        self, subscriber_id: str, active_only: bool = True
    ) -> List[str]:
        """Return sorted unique topic names for ``subscriber_id``."""
        result: Set[str] = set()
        with self._lock:
            for sid in self._by_subscriber.get(subscriber_id, set()):
                entry = self._subs.get(sid)
                if entry is None:
                    continue
                if active_only and not entry.active:
                    continue
                result.add(entry.topic)
        return sorted(result)

    def subscriptions_for_subscriber(
        self, subscriber_id: str, active_only: bool = True
    ) -> List[SubscriptionEntry]:
        """Return entries for ``subscriber_id`` sorted by ``created_at``."""
        with self._lock:
            entries = [
                self._subs[sid]
                for sid in self._by_subscriber.get(subscriber_id, set())
                if sid in self._subs
            ]
        if active_only:
            entries = [e for e in entries if e.active]
        entries.sort(key=lambda e: (e.created_at, e.sub_id))
        return entries

    def subscriptions_for_topic(
        self, topic: str, active_only: bool = True
    ) -> List[SubscriptionEntry]:
        """Return entries for ``topic`` sorted by ``created_at``."""
        with self._lock:
            entries = [
                self._subs[sid]
                for sid in self._by_topic.get(topic, set())
                if sid in self._subs
            ]
        if active_only:
            entries = [e for e in entries if e.active]
        entries.sort(key=lambda e: (e.created_at, e.sub_id))
        return entries

    def all_topics(self) -> List[str]:
        """Return sorted unique topic names with at least one subscription."""
        with self._lock:
            return sorted(self._by_topic.keys())

    def all_subscribers(self) -> List[str]:
        """Return sorted unique subscriber ids with at least one subscription."""
        with self._lock:
            return sorted(self._by_subscriber.keys())

    def top_topics(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Return ``[(topic, subscriber_count), ...]`` sorted by count desc.

        Counts only active subscriptions and distinct subscribers per topic.
        Ties are broken by topic name (ascending) for deterministic output.
        """
        if limit < 0:
            raise ValueError("limit must be non-negative")
        counts: Counter[str] = Counter()
        with self._lock:
            for topic, sub_ids in self._by_topic.items():
                seen: Set[str] = set()
                for sid in sub_ids:
                    entry = self._subs.get(sid)
                    if entry is None or not entry.active:
                        continue
                    seen.add(entry.subscriber_id)
                if seen:
                    counts[topic] = len(seen)
        ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        return ranked[:limit]

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def stats(self) -> IndexStats:
        """Return aggregate :class:`IndexStats`."""
        with self._lock:
            total = len(self._subs)
            active = sum(1 for e in self._subs.values() if e.active)
            unique_topics = len(self._by_topic)
            unique_subscribers = len(self._by_subscriber)
        return IndexStats(
            total_subscriptions=total,
            active_subscriptions=active,
            unique_topics=unique_topics,
            unique_subscribers=unique_subscribers,
        )
