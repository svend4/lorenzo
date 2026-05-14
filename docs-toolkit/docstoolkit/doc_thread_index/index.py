"""E442 DocThreadIndex implementation.

A pure-stdlib, thread-safe index of comment threads associated with documents.
Supports lookups by thread id, document id, and participant, plus simple
lifecycle operations (create/delete/resolve/reopen) and message bookkeeping.
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ThreadRef:
    """Reference to a single comment thread."""

    thread_id: str
    doc_id: str
    title: str = ""
    created_by: str = ""
    created_at: float = 0.0
    last_activity_at: float = 0.0
    message_count: int = 0
    participants: list[str] = field(default_factory=list)
    resolved: bool = False


@dataclass
class ThreadStats:
    """Aggregate statistics over the entire index."""

    total_threads: int
    unresolved_count: int
    unique_docs: int
    total_messages: int


class DocThreadIndex:
    """Thread-safe index of :class:`ThreadRef` objects."""

    def __init__(self) -> None:
        self._threads: dict[str, ThreadRef] = {}
        self._by_doc: dict[str, set[str]] = {}
        self._by_participant: dict[str, set[str]] = {}
        self._lock = threading.Lock()

    # -- internal helpers ------------------------------------------------

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return time.time() if now is None else float(now)

    def _index_participant(self, participant: str, thread_id: str) -> None:
        if not participant:
            return
        self._by_participant.setdefault(participant, set()).add(thread_id)

    def _deindex_participant(self, participant: str, thread_id: str) -> None:
        bucket = self._by_participant.get(participant)
        if not bucket:
            return
        bucket.discard(thread_id)
        if not bucket:
            self._by_participant.pop(participant, None)

    # -- lifecycle -------------------------------------------------------

    def create_thread(
        self,
        doc_id: str,
        title: str = "",
        created_by: str = "",
        now: Optional[float] = None,
    ) -> ThreadRef:
        """Create a new thread under ``doc_id``."""
        ts = self._now(now)
        thread_id = str(uuid.uuid4())
        ref = ThreadRef(
            thread_id=thread_id,
            doc_id=doc_id,
            title=title,
            created_by=created_by,
            created_at=ts,
            last_activity_at=ts,
            message_count=0,
            participants=[],
            resolved=False,
        )
        with self._lock:
            if created_by:
                ref.participants.append(created_by)
            self._threads[thread_id] = ref
            self._by_doc.setdefault(doc_id, set()).add(thread_id)
            if created_by:
                self._index_participant(created_by, thread_id)
        return ref

    def delete_thread(self, thread_id: str) -> bool:
        """Remove a thread by id. Returns ``True`` if it existed."""
        with self._lock:
            ref = self._threads.pop(thread_id, None)
            if ref is None:
                return False
            doc_bucket = self._by_doc.get(ref.doc_id)
            if doc_bucket is not None:
                doc_bucket.discard(thread_id)
                if not doc_bucket:
                    self._by_doc.pop(ref.doc_id, None)
            for p in ref.participants:
                self._deindex_participant(p, thread_id)
            return True

    def get_thread(self, thread_id: str) -> Optional[ThreadRef]:
        """Fetch a thread by id."""
        with self._lock:
            return self._threads.get(thread_id)

    # -- messages & participants ----------------------------------------

    def add_message(
        self,
        thread_id: str,
        participant: str,
        now: Optional[float] = None,
    ) -> bool:
        """Record a new message in ``thread_id`` from ``participant``.

        Increments ``message_count``, updates ``last_activity_at``, and
        registers ``participant`` if not already present.
        """
        ts = self._now(now)
        with self._lock:
            ref = self._threads.get(thread_id)
            if ref is None:
                return False
            ref.message_count += 1
            ref.last_activity_at = ts
            if participant and participant not in ref.participants:
                ref.participants.append(participant)
                self._index_participant(participant, thread_id)
            return True

    def add_participant(self, thread_id: str, participant: str) -> bool:
        """Add ``participant`` to ``thread_id`` if not already present."""
        with self._lock:
            ref = self._threads.get(thread_id)
            if ref is None:
                return False
            if not participant or participant in ref.participants:
                return False
            ref.participants.append(participant)
            self._index_participant(participant, thread_id)
            return True

    def remove_participant(self, thread_id: str, participant: str) -> bool:
        """Remove ``participant`` from ``thread_id``."""
        with self._lock:
            ref = self._threads.get(thread_id)
            if ref is None:
                return False
            if participant not in ref.participants:
                return False
            ref.participants.remove(participant)
            self._deindex_participant(participant, thread_id)
            return True

    # -- resolution -----------------------------------------------------

    def resolve(self, thread_id: str) -> bool:
        with self._lock:
            ref = self._threads.get(thread_id)
            if ref is None:
                return False
            ref.resolved = True
            return True

    def reopen(self, thread_id: str) -> bool:
        with self._lock:
            ref = self._threads.get(thread_id)
            if ref is None:
                return False
            ref.resolved = False
            return True

    # -- queries --------------------------------------------------------

    def threads_for_doc(
        self,
        doc_id: str,
        resolved: Optional[bool] = None,
    ) -> list[ThreadRef]:
        """Return threads for ``doc_id`` sorted by ``last_activity_at`` desc."""
        with self._lock:
            ids = self._by_doc.get(doc_id, set())
            refs = [self._threads[t] for t in ids if t in self._threads]
            if resolved is not None:
                refs = [r for r in refs if r.resolved == resolved]
            refs.sort(key=lambda r: r.last_activity_at, reverse=True)
            return refs

    def threads_for_participant(self, participant: str) -> list[ThreadRef]:
        """Return threads in which ``participant`` is involved."""
        with self._lock:
            ids = self._by_participant.get(participant, set())
            refs = [self._threads[t] for t in ids if t in self._threads]
            refs.sort(key=lambda r: r.last_activity_at, reverse=True)
            return refs

    def active_threads(
        self,
        within_seconds: float = 86400,
        now: Optional[float] = None,
    ) -> list[ThreadRef]:
        """Threads with activity in the last ``within_seconds`` window."""
        ts = self._now(now)
        cutoff = ts - float(within_seconds)
        with self._lock:
            refs = [r for r in self._threads.values() if r.last_activity_at >= cutoff]
            refs.sort(key=lambda r: r.last_activity_at, reverse=True)
            return refs

    def unresolved_threads(self) -> list[ThreadRef]:
        """All unresolved threads, oldest first."""
        with self._lock:
            refs = [r for r in self._threads.values() if not r.resolved]
            refs.sort(key=lambda r: r.created_at)
            return refs

    def clear_doc(self, doc_id: str) -> int:
        """Delete all threads attached to ``doc_id``. Returns count removed."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, set()))
            removed = 0
            for t in ids:
                ref = self._threads.pop(t, None)
                if ref is None:
                    continue
                for p in ref.participants:
                    self._deindex_participant(p, t)
                removed += 1
            self._by_doc.pop(doc_id, None)
            return removed

    def all_doc_ids(self) -> list[str]:
        """Return all known doc ids, sorted."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def stats(self) -> ThreadStats:
        """Aggregate statistics across the index."""
        with self._lock:
            total = len(self._threads)
            unresolved = sum(1 for r in self._threads.values() if not r.resolved)
            unique_docs = len(self._by_doc)
            messages = sum(r.message_count for r in self._threads.values())
            return ThreadStats(
                total_threads=total,
                unresolved_count=unresolved,
                unique_docs=unique_docs,
                total_messages=messages,
            )
