"""DocBreadcrumbStore — navigation breadcrumb trail per user.

Pure stdlib in-memory store backed by dict indexes and protected by a
``threading.Lock``. Each user has a private trail of recent document
visits which is trimmed to ``max_per_user`` entries (oldest dropped).
"""
from __future__ import annotations

import threading
import time
from collections import Counter
from dataclasses import dataclass
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Breadcrumb:
    """A single breadcrumb (visit) entry."""

    entry_id: int
    user_id: str
    doc_id: str
    title: str = ""
    visited_at: float = 0.0


@dataclass
class BreadcrumbStats:
    """Aggregate statistics across the whole store."""

    total_entries: int
    unique_users: int
    unique_docs: int


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------


class DocBreadcrumbStore:
    """Thread-safe in-memory breadcrumb trail manager."""

    def __init__(self, max_per_user: int = 50) -> None:
        if max_per_user < 1:
            raise ValueError("max_per_user must be >= 1")
        self._lock = threading.Lock()
        self._entries: dict[int, Breadcrumb] = {}
        self._by_user: dict[str, list[int]] = {}
        self._next_id: int = 1
        self._max_per_user: int = max_per_user

    # ---- helpers --------------------------------------------------------

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return now if now is not None else time.time()

    # ---- mutations ------------------------------------------------------

    def visit(
        self,
        user_id: str,
        doc_id: str,
        title: str = "",
        now: Optional[float] = None,
    ) -> Breadcrumb:
        """Record a visit for ``user_id`` to ``doc_id``.

        Returns the created :class:`Breadcrumb`. The user's trail is
        trimmed to ``max_per_user``; the oldest entries are dropped and
        removed from the internal store.
        """
        ts = self._now(now)
        with self._lock:
            entry_id = self._next_id
            self._next_id += 1
            crumb = Breadcrumb(
                entry_id=entry_id,
                user_id=user_id,
                doc_id=doc_id,
                title=title,
                visited_at=ts,
            )
            self._entries[entry_id] = crumb
            trail = self._by_user.setdefault(user_id, [])
            trail.append(entry_id)
            # Trim oldest entries.
            while len(trail) > self._max_per_user:
                old_id = trail.pop(0)
                self._entries.pop(old_id, None)
            return crumb

    def clear_user(self, user_id: str) -> int:
        """Remove all entries for ``user_id``. Returns count cleared."""
        with self._lock:
            trail = self._by_user.pop(user_id, [])
            for entry_id in trail:
                self._entries.pop(entry_id, None)
            return len(trail)

    def clear_all(self) -> int:
        """Remove all entries. Returns count cleared."""
        with self._lock:
            count = len(self._entries)
            self._entries.clear()
            self._by_user.clear()
            return count

    # ---- queries --------------------------------------------------------

    def trail_for(
        self, user_id: str, limit: Optional[int] = None
    ) -> list[Breadcrumb]:
        """Return ``user_id``'s breadcrumbs, most recent first.

        Default limit is ``max_per_user``; an explicit ``limit`` overrides.
        """
        with self._lock:
            trail = self._by_user.get(user_id, [])
            if not trail:
                return []
            effective_limit = (
                limit if limit is not None else self._max_per_user
            )
            if effective_limit < 0:
                effective_limit = 0
            # Most recent first.
            reversed_ids = list(reversed(trail))[:effective_limit]
            return [
                self._entries[eid]
                for eid in reversed_ids
                if eid in self._entries
            ]

    def recent_doc(self, user_id: str) -> Optional[Breadcrumb]:
        """Return the most recent visit for ``user_id`` (or ``None``)."""
        with self._lock:
            trail = self._by_user.get(user_id, [])
            if not trail:
                return None
            return self._entries.get(trail[-1])

    def previous_doc(self, user_id: str) -> Optional[Breadcrumb]:
        """Return the second-most-recent visit (or ``None`` if ≤1)."""
        with self._lock:
            trail = self._by_user.get(user_id, [])
            if len(trail) < 2:
                return None
            return self._entries.get(trail[-2])

    def users_with_history(self) -> list[str]:
        """Sorted list of users that have at least one breadcrumb."""
        with self._lock:
            return sorted(
                u for u, trail in self._by_user.items() if trail
            )

    def unique_docs_visited(self, user_id: str) -> list[str]:
        """Sorted unique ``doc_id`` values present in user's trail."""
        with self._lock:
            trail = self._by_user.get(user_id, [])
            docs = {
                self._entries[eid].doc_id
                for eid in trail
                if eid in self._entries
            }
            return sorted(docs)

    def frequency_for_doc(self, user_id: str, doc_id: str) -> int:
        """Number of times ``doc_id`` appears in user's trail."""
        with self._lock:
            trail = self._by_user.get(user_id, [])
            count = 0
            for eid in trail:
                crumb = self._entries.get(eid)
                if crumb is not None and crumb.doc_id == doc_id:
                    count += 1
            return count

    def most_visited_docs(
        self, user_id: str, limit: int = 5
    ) -> list[tuple[str, int]]:
        """Return ``(doc_id, count)`` pairs sorted by count desc, doc asc."""
        with self._lock:
            trail = self._by_user.get(user_id, [])
            counter: Counter[str] = Counter()
            for eid in trail:
                crumb = self._entries.get(eid)
                if crumb is not None:
                    counter[crumb.doc_id] += 1
            items = sorted(
                counter.items(), key=lambda kv: (-kv[1], kv[0])
            )
            if limit < 0:
                limit = 0
            return items[:limit]

    def stats(self) -> BreadcrumbStats:
        """Aggregate statistics across the whole store."""
        with self._lock:
            unique_users = sum(
                1 for trail in self._by_user.values() if trail
            )
            unique_docs = {c.doc_id for c in self._entries.values()}
            return BreadcrumbStats(
                total_entries=len(self._entries),
                unique_users=unique_users,
                unique_docs=len(unique_docs),
            )
