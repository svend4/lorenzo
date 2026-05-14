"""E393 DocChangeSubscriber implementation.

Pure stdlib, thread-safe subscription manager that records delivered
notifications for later inspection.
"""
from __future__ import annotations

import fnmatch
import threading
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Subscription:
    """A single subscription registration."""

    sub_id: str
    user_id: str
    doc_pattern: str
    change_types: list[str] = field(default_factory=list)
    created_at: float = 0.0
    active: bool = True


@dataclass
class DeliveryRecord:
    """A delivered notification record."""

    record_id: int
    sub_id: str
    doc_id: str
    change_type: str
    delivered_at: float = 0.0


@dataclass
class SubscriberStats:
    """Aggregate statistics for the subscriber."""

    total_subscriptions: int
    active_subscriptions: int
    total_deliveries: int
    unique_subscribers: int


class DocChangeSubscriber:
    """Subscription manager with persistent delivery history.

    Stores subscriptions and delivered :class:`DeliveryRecord` entries in
    memory. Matching is by :mod:`fnmatch` pattern on doc_id plus an optional
    change-type allow-list.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._subs: dict[str, Subscription] = {}
        self._deliveries: list[DeliveryRecord] = []
        self._next_record_id: int = 1

    # ------------------------------------------------------------------
    # Subscription management
    # ------------------------------------------------------------------
    def subscribe(
        self,
        user_id: str,
        doc_pattern: str,
        change_types: Optional[list[str]] = None,
        now: Optional[float] = None,
    ) -> Subscription:
        """Register a new subscription. Returns the Subscription object."""
        sub = Subscription(
            sub_id=uuid.uuid4().hex,
            user_id=user_id,
            doc_pattern=doc_pattern,
            change_types=list(change_types) if change_types else [],
            created_at=now if now is not None else 0.0,
            active=True,
        )
        with self._lock:
            self._subs[sub.sub_id] = sub
        return sub

    def unsubscribe(self, sub_id: str) -> bool:
        """Deactivate a subscription. Returns True if it existed and was active."""
        with self._lock:
            sub = self._subs.get(sub_id)
            if sub is None:
                return False
            if not sub.active:
                return False
            sub.active = False
            return True

    def delete_subscription(self, sub_id: str) -> bool:
        """Delete a subscription entirely. Returns True if it existed."""
        with self._lock:
            if sub_id in self._subs:
                del self._subs[sub_id]
                return True
            return False

    def get_subscription(self, sub_id: str) -> Optional[Subscription]:
        """Look up a subscription by id."""
        with self._lock:
            return self._subs.get(sub_id)

    def subscriptions_for_user(
        self, user_id: str, active_only: bool = True
    ) -> list[Subscription]:
        """All subscriptions belonging to user_id, ordered by created_at."""
        with self._lock:
            subs = [
                s for s in self._subs.values()
                if s.user_id == user_id and (not active_only or s.active)
            ]
        subs.sort(key=lambda s: s.created_at)
        return subs

    # ------------------------------------------------------------------
    # Matching and dispatch
    # ------------------------------------------------------------------
    def matching_subscriptions(
        self, doc_id: str, change_type: str
    ) -> list[Subscription]:
        """Active subscriptions whose pattern matches doc_id and change_type."""
        with self._lock:
            matched: list[Subscription] = []
            for sub in self._subs.values():
                if not sub.active:
                    continue
                if not fnmatch.fnmatchcase(doc_id, sub.doc_pattern):
                    continue
                if sub.change_types and change_type not in sub.change_types:
                    continue
                matched.append(sub)
        return matched

    def dispatch(
        self,
        doc_id: str,
        change_type: str,
        now: Optional[float] = None,
    ) -> list[DeliveryRecord]:
        """Create delivery records for every matching active subscription."""
        ts = now if now is not None else 0.0
        records: list[DeliveryRecord] = []
        with self._lock:
            for sub in self._subs.values():
                if not sub.active:
                    continue
                if not fnmatch.fnmatchcase(doc_id, sub.doc_pattern):
                    continue
                if sub.change_types and change_type not in sub.change_types:
                    continue
                rec = DeliveryRecord(
                    record_id=self._next_record_id,
                    sub_id=sub.sub_id,
                    doc_id=doc_id,
                    change_type=change_type,
                    delivered_at=ts,
                )
                self._next_record_id += 1
                self._deliveries.append(rec)
                records.append(rec)
        return records

    # ------------------------------------------------------------------
    # Delivery introspection
    # ------------------------------------------------------------------
    def deliveries_for_sub(
        self, sub_id: str, limit: Optional[int] = None
    ) -> list[DeliveryRecord]:
        """Records for a subscription, most recent first."""
        with self._lock:
            results = [r for r in self._deliveries if r.sub_id == sub_id]
        results.reverse()
        if limit is not None:
            results = results[:limit]
        return results

    def deliveries_for_user(
        self, user_id: str, limit: Optional[int] = None
    ) -> list[DeliveryRecord]:
        """Records for all subscriptions of a user, most recent first."""
        with self._lock:
            user_sub_ids = {
                sid for sid, sub in self._subs.items() if sub.user_id == user_id
            }
            results = [r for r in self._deliveries if r.sub_id in user_sub_ids]
        results.reverse()
        if limit is not None:
            results = results[:limit]
        return results

    def clear_deliveries(self) -> int:
        """Drop all delivery records. Returns number cleared."""
        with self._lock:
            count = len(self._deliveries)
            self._deliveries.clear()
            return count

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------
    def stats(self) -> SubscriberStats:
        """Snapshot of aggregate counters."""
        with self._lock:
            total = len(self._subs)
            active = sum(1 for s in self._subs.values() if s.active)
            users = {s.user_id for s in self._subs.values()}
            return SubscriberStats(
                total_subscriptions=total,
                active_subscriptions=active,
                total_deliveries=len(self._deliveries),
                unique_subscribers=len(users),
            )
