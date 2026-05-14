"""E321 DocSubscriptionManager — thread-safe subscription management.

Pure stdlib, no third-party dependencies.
Thread-safe via threading.Lock.
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Subscription:
    """A user's subscription to a document or topic."""

    sub_id: str
    user_id: str
    target: str  # doc_id, topic, or pattern e.g. "doc:123", "topic:updates", "*"
    events: list[str] = field(default_factory=list)  # empty = all events
    created_at: float = 0.0
    active: bool = True


@dataclass
class SubscriptionStats:
    """Aggregate statistics over all subscriptions."""

    total_subscriptions: int
    active_subscriptions: int
    unique_users: int
    unique_targets: int


class DocSubscriptionManager:
    """Thread-safe manager for user subscriptions to document events.

    Internal indexes are kept in sync on every mutating operation so that
    read queries never need to iterate the full ``_subs`` dict.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._subs: dict[str, Subscription] = {}
        self._by_user: dict[str, list[str]] = {}
        self._by_target: dict[str, list[str]] = {}

    # ------------------------------------------------------------------
    # Write operations
    # ------------------------------------------------------------------

    def subscribe(
        self,
        user_id: str,
        target: str,
        events: Optional[list[str]] = None,
        now: Optional[float] = None,
    ) -> Subscription:
        """Create a new active subscription and return it."""
        sub_id = str(uuid.uuid4())
        created_at = now if now is not None else time.time()
        sub = Subscription(
            sub_id=sub_id,
            user_id=user_id,
            target=target,
            events=list(events) if events is not None else [],
            created_at=created_at,
            active=True,
        )
        with self._lock:
            self._subs[sub_id] = sub
            self._by_user.setdefault(user_id, []).append(sub_id)
            self._by_target.setdefault(target, []).append(sub_id)
        return sub

    def unsubscribe(self, sub_id: str) -> bool:
        """Set active=False. Return True if found, False if not."""
        with self._lock:
            sub = self._subs.get(sub_id)
            if sub is None:
                return False
            sub.active = False
            return True

    def reactivate(self, sub_id: str) -> bool:
        """Set active=True. Return True if found, False if not."""
        with self._lock:
            sub = self._subs.get(sub_id)
            if sub is None:
                return False
            sub.active = True
            return True

    def delete(self, sub_id: str) -> bool:
        """Fully remove a subscription from all indexes. Return True if existed."""
        with self._lock:
            sub = self._subs.pop(sub_id, None)
            if sub is None:
                return False
            user_list = self._by_user.get(sub.user_id, [])
            if sub_id in user_list:
                user_list.remove(sub_id)
            target_list = self._by_target.get(sub.target, [])
            if sub_id in target_list:
                target_list.remove(sub_id)
            return True

    def deactivate_all(self, user_id: str) -> int:
        """Deactivate all active subscriptions for a user. Return count deactivated."""
        count = 0
        with self._lock:
            for sub_id in self._by_user.get(user_id, []):
                sub = self._subs.get(sub_id)
                if sub is not None and sub.active:
                    sub.active = False
                    count += 1
        return count

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def get(self, sub_id: str) -> Optional[Subscription]:
        """Return the subscription with the given id, or None."""
        with self._lock:
            return self._subs.get(sub_id)

    def subscriptions_for_user(
        self, user_id: str, active_only: bool = True
    ) -> list[Subscription]:
        """Return subscriptions for a user, sorted by created_at ascending."""
        with self._lock:
            subs = [
                self._subs[sid]
                for sid in self._by_user.get(user_id, [])
                if sid in self._subs
            ]
        if active_only:
            subs = [s for s in subs if s.active]
        return sorted(subs, key=lambda s: s.created_at)

    def subscriptions_for_target(
        self, target: str, active_only: bool = True
    ) -> list[Subscription]:
        """Return subscriptions for a target, sorted by created_at ascending."""
        with self._lock:
            subs = [
                self._subs[sid]
                for sid in self._by_target.get(target, [])
                if sid in self._subs
            ]
        if active_only:
            subs = [s for s in subs if s.active]
        return sorted(subs, key=lambda s: s.created_at)

    def subscribers_for_target(self, target: str) -> list[str]:
        """Return sorted unique user_ids with active subscriptions to target."""
        with self._lock:
            user_ids = {
                self._subs[sid].user_id
                for sid in self._by_target.get(target, [])
                if sid in self._subs and self._subs[sid].active
            }
        return sorted(user_ids)

    def matches(
        self, user_id: str, target: str, event_type: str
    ) -> list[Subscription]:
        """Return active subscriptions for user where sub.target == target AND
        (sub.events is empty OR event_type in sub.events)."""
        with self._lock:
            candidate_ids = set(self._by_user.get(user_id, [])) & set(
                self._by_target.get(target, [])
            )
            result = []
            for sid in candidate_ids:
                sub = self._subs.get(sid)
                if sub is None or not sub.active:
                    continue
                if not sub.events or event_type in sub.events:
                    result.append(sub)
        return result

    def stats(self) -> SubscriptionStats:
        """Return aggregate statistics."""
        with self._lock:
            all_subs = list(self._subs.values())
        active = [s for s in all_subs if s.active]
        unique_users = len({s.user_id for s in all_subs})
        unique_targets = len({s.target for s in all_subs})
        return SubscriptionStats(
            total_subscriptions=len(all_subs),
            active_subscriptions=len(active),
            unique_users=unique_users,
            unique_targets=unique_targets,
        )
