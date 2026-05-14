"""DocReadTracker — track document read events per user."""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ReadEvent:
    """A single read event record."""

    event_id: int
    doc_id: str
    user_id: str
    read_at: float = 0.0
    duration_seconds: float = 0.0  # 0 = unknown


@dataclass
class ReadStats:
    """Aggregate read statistics for a document."""

    doc_id: str
    total_reads: int
    unique_readers: int
    avg_duration: float  # average of non-zero durations; 0.0 if none
    last_read_at: float


class DocReadTracker:
    """Thread-safe tracker for document read events."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._next_id: int = 1
        self._events: list[ReadEvent] = []
        self._by_doc: dict[str, list[ReadEvent]] = {}
        self._by_user: dict[str, list[ReadEvent]] = {}

    # ------------------------------------------------------------------ record

    def record(
        self,
        doc_id: str,
        user_id: str,
        duration_seconds: float = 0.0,
        now: Optional[float] = None,
    ) -> ReadEvent:
        """Record a read event and return the new ReadEvent.

        ``now`` overrides the timestamp (useful in tests); when omitted
        ``time.time()`` is used.  ``event_id`` auto-increments from 1.
        """
        ts = now if now is not None else time.time()
        with self._lock:
            eid = self._next_id
            self._next_id += 1
            event = ReadEvent(
                event_id=eid,
                doc_id=doc_id,
                user_id=user_id,
                read_at=ts,
                duration_seconds=duration_seconds,
            )
            self._events.append(event)
            self._by_doc.setdefault(doc_id, []).append(event)
            self._by_user.setdefault(user_id, []).append(event)
        return event

    # ------------------------------------------------------------------ queries

    def events_for_doc(
        self,
        doc_id: str,
        limit: Optional[int] = None,
    ) -> list[ReadEvent]:
        """Return events for *doc_id* in insertion order, optionally limited."""
        with self._lock:
            evts = list(self._by_doc.get(doc_id, []))
        if limit is not None:
            evts = evts[:limit]
        return evts

    def events_for_user(
        self,
        user_id: str,
        limit: Optional[int] = None,
    ) -> list[ReadEvent]:
        """Return events for *user_id* in insertion order, optionally limited."""
        with self._lock:
            evts = list(self._by_user.get(user_id, []))
        if limit is not None:
            evts = evts[:limit]
        return evts

    def has_read(self, user_id: str, doc_id: str) -> bool:
        """Return True if *user_id* has at least one read event for *doc_id*."""
        with self._lock:
            for evt in self._by_user.get(user_id, []):
                if evt.doc_id == doc_id:
                    return True
        return False

    def read_count(self, doc_id: str) -> int:
        """Return the total number of read events for *doc_id* (0 if unknown)."""
        with self._lock:
            return len(self._by_doc.get(doc_id, []))

    def unique_readers(self, doc_id: str) -> list[str]:
        """Return sorted list of distinct user_ids that have read *doc_id*."""
        with self._lock:
            evts = self._by_doc.get(doc_id, [])
            readers = {e.user_id for e in evts}
        return sorted(readers)

    def most_read_docs(self, limit: int = 10) -> list[tuple[str, int]]:
        """Return (doc_id, read_count) tuples sorted by count desc, doc_id asc."""
        with self._lock:
            counts = {doc: len(evts) for doc, evts in self._by_doc.items()}
        ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        return ranked[:limit]

    def recent_events(self, limit: int = 10) -> list[ReadEvent]:
        """Return the *limit* most recently recorded events (tail of global list)."""
        with self._lock:
            tail = list(self._events[-limit:]) if limit > 0 else []
        return tail

    def stats_for_doc(self, doc_id: str) -> ReadStats:
        """Return aggregate statistics for *doc_id*."""
        with self._lock:
            evts = list(self._by_doc.get(doc_id, []))

        total_reads = len(evts)
        unique_readers = len({e.user_id for e in evts})
        last_read_at = max((e.read_at for e in evts), default=0.0)

        durations = [e.duration_seconds for e in evts if e.duration_seconds != 0.0]
        avg_duration = sum(durations) / len(durations) if durations else 0.0

        return ReadStats(
            doc_id=doc_id,
            total_reads=total_reads,
            unique_readers=unique_readers,
            avg_duration=avg_duration,
            last_read_at=last_read_at,
        )

    def all_doc_ids(self) -> list[str]:
        """Return a sorted list of all tracked doc_ids."""
        with self._lock:
            ids = list(self._by_doc.keys())
        return sorted(ids)
