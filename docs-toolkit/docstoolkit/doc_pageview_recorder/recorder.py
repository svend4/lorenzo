"""Pageview recording and statistics — pure stdlib, thread-safe."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Pageview:
    """A single pageview event."""

    view_id: int = 0
    doc_id: str = ""
    user_id: str = ""
    referrer: str = ""
    viewed_at: float = 0.0


@dataclass
class DocViewStats:
    """Pageview statistics for a single doc."""

    doc_id: str
    total_views: int
    unique_users: int
    first_viewed_at: float
    last_viewed_at: float


@dataclass
class RecorderStats:
    """Aggregate recorder statistics."""

    total_pageviews: int
    unique_docs: int
    unique_users: int
    anonymous_views: int


class DocPageviewRecorder:
    """Track page views and metrics per document.

    Thread-safe via an internal :class:`threading.Lock`.
    """

    def __init__(self) -> None:
        self._views: list[Pageview] = []
        self._by_doc: dict[str, list[int]] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ record
    def record(
        self,
        doc_id: str,
        user_id: str = "",
        referrer: str = "",
        now: Optional[float] = None,
    ) -> Pageview:
        """Record a new pageview and return it."""
        ts = now if now is not None else time.time()
        with self._lock:
            view = Pageview(
                view_id=self._next_id,
                doc_id=doc_id,
                user_id=user_id,
                referrer=referrer,
                viewed_at=ts,
            )
            self._next_id += 1
            self._views.append(view)
            self._by_doc.setdefault(doc_id, []).append(view.view_id)
            return view

    # ------------------------------------------------------------------ helpers
    def _view_by_id(self, view_id: int) -> Optional[Pageview]:
        # view_ids are 1-based and assigned in order
        idx = view_id - 1
        if 0 <= idx < len(self._views):
            v = self._views[idx]
            if v.view_id == view_id:
                return v
        # fallback linear scan (shouldn't happen normally)
        for v in self._views:
            if v.view_id == view_id:
                return v
        return None

    # ----------------------------------------------------------- views_for_doc
    def views_for_doc(
        self, doc_id: str, limit: Optional[int] = None
    ) -> list[Pageview]:
        """Return views for a doc, most recent first."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
        views = []
        for vid in ids:
            v = self._view_by_id(vid)
            if v is not None:
                views.append(v)
        # most recent first: sort by viewed_at desc, tiebreak by view_id desc
        views.sort(key=lambda v: (v.viewed_at, v.view_id), reverse=True)
        if limit is not None:
            views = views[:limit]
        return views

    # ----------------------------------------------------------------- counts
    def view_count(self, doc_id: str) -> int:
        with self._lock:
            return len(self._by_doc.get(doc_id, []))

    def unique_user_count(self, doc_id: str) -> int:
        """Unique non-anonymous users for a doc."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
        users: set[str] = set()
        for vid in ids:
            v = self._view_by_id(vid)
            if v is not None and v.user_id:
                users.add(v.user_id)
        return len(users)

    # ---------------------------------------------------------- stats_for_doc
    def stats_for_doc(self, doc_id: str) -> Optional[DocViewStats]:
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
        if not ids:
            return None
        views = [self._view_by_id(vid) for vid in ids]
        views = [v for v in views if v is not None]
        if not views:
            return None
        users = {v.user_id for v in views if v.user_id}
        first = min(v.viewed_at for v in views)
        last = max(v.viewed_at for v in views)
        return DocViewStats(
            doc_id=doc_id,
            total_views=len(views),
            unique_users=len(users),
            first_viewed_at=first,
            last_viewed_at=last,
        )

    # --------------------------------------------------------------- top_docs
    def top_docs(self, limit: int = 10) -> list[tuple]:
        """Top docs by view count. Sorted by count desc, then doc_id asc."""
        with self._lock:
            counts = [(d, len(ids)) for d, ids in self._by_doc.items() if ids]
        counts.sort(key=lambda t: (-t[1], t[0]))
        if limit is not None:
            counts = counts[:limit]
        return counts

    # ---------------------------------------------------------- views_by_user
    def views_by_user(
        self, user_id: str, limit: Optional[int] = None
    ) -> list[Pageview]:
        """Return views by a user, most recent first."""
        with self._lock:
            snapshot = list(self._views)
        views = [v for v in snapshot if v.user_id == user_id]
        views.sort(key=lambda v: (v.viewed_at, v.view_id), reverse=True)
        if limit is not None:
            views = views[:limit]
        return views

    # --------------------------------------------------------- views_in_range
    def views_in_range(
        self,
        start_time: float,
        end_time: float,
        doc_id: Optional[str] = None,
    ) -> list[Pageview]:
        """Views with viewed_at in [start_time, end_time] inclusive, sorted asc."""
        with self._lock:
            snapshot = list(self._views)
        result = []
        for v in snapshot:
            if v.viewed_at < start_time or v.viewed_at > end_time:
                continue
            if doc_id is not None and v.doc_id != doc_id:
                continue
            result.append(v)
        result.sort(key=lambda v: (v.viewed_at, v.view_id))
        return result

    # -------------------------------------------------------------- clear ops
    def clear_doc(self, doc_id: str) -> int:
        """Remove a doc from the index. Returns number of views cleared."""
        with self._lock:
            ids = self._by_doc.pop(doc_id, [])
            return len(ids)

    def clear_all(self) -> int:
        """Clear all indexes and views. Returns total count cleared."""
        with self._lock:
            count = len(self._views)
            self._views.clear()
            self._by_doc.clear()
            self._next_id = 1
            return count

    # ----------------------------------------------------------- all_doc_ids
    def all_doc_ids(self) -> list[str]:
        """Sorted list of doc_ids with at least one view."""
        with self._lock:
            return sorted(d for d, ids in self._by_doc.items() if ids)

    # ----------------------------------------------------------------- stats
    def stats(self) -> RecorderStats:
        with self._lock:
            snapshot = list(self._views)
            unique_docs = sum(1 for ids in self._by_doc.values() if ids)
        users: set[str] = set()
        anon = 0
        for v in snapshot:
            if v.user_id:
                users.add(v.user_id)
            else:
                anon += 1
        return RecorderStats(
            total_pageviews=len(snapshot),
            unique_docs=unique_docs,
            unique_users=len(users),
            anonymous_views=anon,
        )
