"""Document-level metrics collection.

Tracks engagement events per document: views, edits, comments, shares,
exports, downloads and reactions. Computes counts, unique-user sets,
top-N rankings, engagement scores, churn rate and retention.

Storage:
    - collections.deque(maxlen=max_events) for FIFO eviction.
    - threading.Lock for safe concurrent record/query.
"""
from __future__ import annotations

import threading
import time
from collections import Counter, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class EventType(Enum):
    """Kinds of engagement events tracked per document."""

    VIEW = "view"
    EDIT = "edit"
    COMMENT = "comment"
    SHARE = "share"
    EXPORT = "export"
    DOWNLOAD = "download"
    REACTION = "reaction"


@dataclass
class DocEvent:
    """A single recorded engagement event for a document."""

    event_id: int
    doc_id: str
    event_type: EventType
    user_id: Optional[str] = None
    timestamp: float = 0.0
    metadata: dict = field(default_factory=dict)


@dataclass
class DocMetricsSnapshot:
    """Aggregate counts and unique-user counts for a single document."""

    doc_id: str
    view_count: int
    edit_count: int
    comment_count: int
    share_count: int
    unique_viewers: int
    unique_editors: int
    last_view: Optional[float] = None
    last_edit: Optional[float] = None


@dataclass
class EngagementScore:
    """Weighted engagement score for a single document."""

    doc_id: str
    score: float
    view_weight: float = 1.0
    edit_weight: float = 5.0
    comment_weight: float = 3.0
    share_weight: float = 4.0


class DocMetrics:
    """Thread-safe in-memory store of document engagement events."""

    def __init__(self, max_events: int = 100_000) -> None:
        if max_events <= 0:
            raise ValueError("max_events must be positive")
        self._max_events = max_events
        self._events: deque = deque(maxlen=max_events)
        self._lock = threading.Lock()
        self._next_id = 1

    # ------------------------------------------------------------------ record

    def record_event(
        self,
        doc_id: str,
        event_type: EventType,
        user_id: Optional[str] = None,
        metadata: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> DocEvent:
        """Record an arbitrary event."""
        if not isinstance(event_type, EventType):
            raise TypeError("event_type must be an EventType")
        ts = time.time() if now is None else float(now)
        meta = dict(metadata) if metadata else {}
        with self._lock:
            event = DocEvent(
                event_id=self._next_id,
                doc_id=doc_id,
                event_type=event_type,
                user_id=user_id,
                timestamp=ts,
                metadata=meta,
            )
            self._next_id += 1
            self._events.append(event)
            return event

    def record_view(
        self,
        doc_id: str,
        user_id: Optional[str] = None,
        metadata: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> DocEvent:
        return self.record_event(doc_id, EventType.VIEW, user_id, metadata, now)

    def record_edit(
        self,
        doc_id: str,
        user_id: Optional[str] = None,
        metadata: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> DocEvent:
        return self.record_event(doc_id, EventType.EDIT, user_id, metadata, now)

    def record_comment(
        self,
        doc_id: str,
        user_id: Optional[str] = None,
        metadata: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> DocEvent:
        return self.record_event(doc_id, EventType.COMMENT, user_id, metadata, now)

    def record_share(
        self,
        doc_id: str,
        user_id: Optional[str] = None,
        metadata: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> DocEvent:
        return self.record_event(doc_id, EventType.SHARE, user_id, metadata, now)

    # ------------------------------------------------------------------ query

    def events_for_doc(
        self, doc_id: str, event_type: Optional[EventType] = None
    ) -> list:
        with self._lock:
            return [
                e
                for e in self._events
                if e.doc_id == doc_id
                and (event_type is None or e.event_type == event_type)
            ]

    def events_by_user(self, user_id: str) -> list:
        with self._lock:
            return [e for e in self._events if e.user_id == user_id]

    def events_in_range(self, start: float, end: float) -> list:
        if start > end:
            raise ValueError("start must be <= end")
        with self._lock:
            return [e for e in self._events if start <= e.timestamp <= end]

    def snapshot(self, doc_id: str) -> DocMetricsSnapshot:
        view_count = edit_count = comment_count = share_count = 0
        viewers: set = set()
        editors: set = set()
        last_view: Optional[float] = None
        last_edit: Optional[float] = None
        with self._lock:
            for e in self._events:
                if e.doc_id != doc_id:
                    continue
                if e.event_type == EventType.VIEW:
                    view_count += 1
                    if e.user_id is not None:
                        viewers.add(e.user_id)
                    if last_view is None or e.timestamp > last_view:
                        last_view = e.timestamp
                elif e.event_type == EventType.EDIT:
                    edit_count += 1
                    if e.user_id is not None:
                        editors.add(e.user_id)
                    if last_edit is None or e.timestamp > last_edit:
                        last_edit = e.timestamp
                elif e.event_type == EventType.COMMENT:
                    comment_count += 1
                elif e.event_type == EventType.SHARE:
                    share_count += 1
        return DocMetricsSnapshot(
            doc_id=doc_id,
            view_count=view_count,
            edit_count=edit_count,
            comment_count=comment_count,
            share_count=share_count,
            unique_viewers=len(viewers),
            unique_editors=len(editors),
            last_view=last_view,
            last_edit=last_edit,
        )

    def _count(
        self,
        doc_id: str,
        event_type: EventType,
        since: Optional[float] = None,
    ) -> int:
        with self._lock:
            return sum(
                1
                for e in self._events
                if e.doc_id == doc_id
                and e.event_type == event_type
                and (since is None or e.timestamp >= since)
            )

    def view_count(
        self,
        doc_id: str,
        since: Optional[float] = None,
        now: Optional[float] = None,
    ) -> int:
        # `now` retained per spec; not used in current count semantics
        return self._count(doc_id, EventType.VIEW, since)

    def edit_count(self, doc_id: str, since: Optional[float] = None) -> int:
        return self._count(doc_id, EventType.EDIT, since)

    def _unique_users(
        self,
        doc_id: str,
        event_type: EventType,
        since: Optional[float] = None,
    ) -> set:
        users: set = set()
        with self._lock:
            for e in self._events:
                if e.doc_id != doc_id or e.event_type != event_type:
                    continue
                if since is not None and e.timestamp < since:
                    continue
                if e.user_id is not None:
                    users.add(e.user_id)
        return users

    def unique_viewers(
        self, doc_id: str, since: Optional[float] = None
    ) -> set:
        return self._unique_users(doc_id, EventType.VIEW, since)

    def unique_editors(
        self, doc_id: str, since: Optional[float] = None
    ) -> set:
        return self._unique_users(doc_id, EventType.EDIT, since)

    def _top_docs(
        self,
        event_type: EventType,
        top_k: int,
        since: Optional[float] = None,
    ) -> list:
        if top_k < 0:
            raise ValueError("top_k must be non-negative")
        counter: Counter = Counter()
        with self._lock:
            for e in self._events:
                if e.event_type != event_type:
                    continue
                if since is not None and e.timestamp < since:
                    continue
                counter[e.doc_id] += 1
        return counter.most_common(top_k)

    def most_viewed_docs(
        self, top_k: int = 10, since: Optional[float] = None
    ) -> list:
        return self._top_docs(EventType.VIEW, top_k, since)

    def most_edited_docs(
        self, top_k: int = 10, since: Optional[float] = None
    ) -> list:
        return self._top_docs(EventType.EDIT, top_k, since)

    def engagement_score(
        self,
        doc_id: str,
        view_weight: float = 1.0,
        edit_weight: float = 5.0,
        comment_weight: float = 3.0,
        share_weight: float = 4.0,
    ) -> EngagementScore:
        snap = self.snapshot(doc_id)
        score = (
            snap.view_count * view_weight
            + snap.edit_count * edit_weight
            + snap.comment_count * comment_weight
            + snap.share_count * share_weight
        )
        return EngagementScore(
            doc_id=doc_id,
            score=float(score),
            view_weight=view_weight,
            edit_weight=edit_weight,
            comment_weight=comment_weight,
            share_weight=share_weight,
        )

    def churn_rate(self, start: float, end: float) -> float:
        """Churn rate between two equal-length windows.

        Returns 1 - (docs_viewed_in_both / docs_viewed_in_start_window).
        The "start window" is [start, midpoint) and the "end window" is
        [midpoint, end] where midpoint = (start + end) / 2.

        If no docs were viewed in the start window, returns 0.0.
        """
        if start > end:
            raise ValueError("start must be <= end")
        midpoint = (start + end) / 2.0
        start_docs: set = set()
        end_docs: set = set()
        with self._lock:
            for e in self._events:
                if e.event_type != EventType.VIEW:
                    continue
                if start <= e.timestamp < midpoint:
                    start_docs.add(e.doc_id)
                elif midpoint <= e.timestamp <= end:
                    end_docs.add(e.doc_id)
        if not start_docs:
            return 0.0
        retained = len(start_docs & end_docs)
        return 1.0 - (retained / len(start_docs))

    def retention(
        self,
        start: float,
        end: float,
        midpoint: Optional[float] = None,
    ) -> float:
        """Fraction of users active in both halves of [start, end]."""
        if start > end:
            raise ValueError("start must be <= end")
        mid = (start + end) / 2.0 if midpoint is None else float(midpoint)
        first_users: set = set()
        second_users: set = set()
        with self._lock:
            for e in self._events:
                if e.user_id is None:
                    continue
                if start <= e.timestamp < mid:
                    first_users.add(e.user_id)
                elif mid <= e.timestamp <= end:
                    second_users.add(e.user_id)
        if not first_users:
            return 0.0
        return len(first_users & second_users) / len(first_users)

    # ------------------------------------------------------------------ misc

    @property
    def total_events(self) -> int:
        with self._lock:
            return len(self._events)

    def clear(self) -> None:
        with self._lock:
            self._events.clear()
            self._next_id = 1
