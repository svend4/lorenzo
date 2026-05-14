"""E433 DocPublicationState — implementation.

Tracks the publication lifecycle of documents through the states:
``draft``, ``review``, ``scheduled``, ``published``, ``unpublished``, ``archived``.

Pure standard library (``threading``, ``dataclasses``, ``time``). Thread-safe
via an internal :class:`threading.Lock`. All time-based methods accept a
deterministic ``now`` parameter (seconds since epoch) so behaviour can be
tested without ``time.sleep``.
"""
from __future__ import annotations

import threading
import time as _time
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class PublicationRecord:
    """Publication state for a single document."""

    doc_id: str
    state: str
    state_changed_at: float = 0.0
    published_at: Optional[float] = None
    scheduled_for: Optional[float] = None
    published_by: str = ""


@dataclass
class PublicationStats:
    """Aggregate publication statistics."""

    total_docs: int
    state_counts: Dict[str, int] = field(default_factory=dict)
    scheduled_pending: int = 0


# ---------------------------------------------------------------------------
# Valid states and transitions
# ---------------------------------------------------------------------------


VALID_STATES = frozenset(
    {"draft", "review", "scheduled", "published", "unpublished", "archived"}
)

# Allowed transitions: source state -> set of allowed destination states.
_TRANSITIONS: Dict[str, frozenset] = {
    "draft": frozenset({"review", "scheduled", "published"}),
    "review": frozenset({"draft", "scheduled", "published"}),
    "scheduled": frozenset({"draft", "published", "unpublished"}),
    "published": frozenset({"unpublished", "archived"}),
    "unpublished": frozenset({"draft", "published", "archived"}),
    "archived": frozenset(),  # terminal
}


# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------


class DocPublicationState:
    """In-memory, thread-safe publication state tracker."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._records: Dict[str, PublicationRecord] = {}

    # ------------------------------------------------------------------
    # Internal helpers (must be called with the lock held)
    # ------------------------------------------------------------------

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return _time.time() if now is None else now

    # ------------------------------------------------------------------
    # State setters
    # ------------------------------------------------------------------

    def set_state(
        self,
        doc_id: str,
        state: str,
        by: str = "",
        now: Optional[float] = None,
    ) -> PublicationRecord:
        """Set state directly (no transition validation).

        Creates the record if missing. Always updates ``state_changed_at``.
        Raises :class:`ValueError` if ``state`` is not a valid state name.
        """
        if state not in VALID_STATES:
            raise ValueError(f"invalid state: {state!r}")
        ts = self._now(now)
        with self._lock:
            rec = self._records.get(doc_id)
            if rec is None:
                rec = PublicationRecord(
                    doc_id=doc_id,
                    state=state,
                    state_changed_at=ts,
                )
                self._records[doc_id] = rec
            else:
                rec.state = state
                rec.state_changed_at = ts
            if state == "published":
                rec.published_at = ts
                if by:
                    rec.published_by = by
            elif by:
                # record the actor even on non-publish transitions
                rec.published_by = by
            return rec

    def transition(
        self,
        doc_id: str,
        to_state: str,
        by: str = "",
        now: Optional[float] = None,
    ) -> Optional[PublicationRecord]:
        """Validate and perform a transition.

        Returns the updated record on success, or ``None`` if the document
        does not exist, the destination state is unknown, or the transition
        is not allowed from the current state.
        """
        if to_state not in VALID_STATES:
            return None
        ts = self._now(now)
        with self._lock:
            rec = self._records.get(doc_id)
            if rec is None:
                return None
            allowed = _TRANSITIONS.get(rec.state, frozenset())
            if to_state not in allowed:
                return None
            rec.state = to_state
            rec.state_changed_at = ts
            if to_state == "published":
                rec.published_at = ts
                if by:
                    rec.published_by = by
            elif by:
                rec.published_by = by
            return rec

    # ------------------------------------------------------------------
    # Convenience operations
    # ------------------------------------------------------------------

    def schedule(
        self,
        doc_id: str,
        scheduled_for: float,
        by: str = "",
        now: Optional[float] = None,
    ) -> Optional[PublicationRecord]:
        """Set state="scheduled" and remember ``scheduled_for``.

        Validates the transition from the current state. Returns ``None`` if
        the document does not exist or the transition is not allowed.
        """
        ts = self._now(now)
        with self._lock:
            rec = self._records.get(doc_id)
            if rec is None:
                return None
            allowed = _TRANSITIONS.get(rec.state, frozenset())
            if "scheduled" not in allowed:
                return None
            rec.state = "scheduled"
            rec.state_changed_at = ts
            rec.scheduled_for = scheduled_for
            if by:
                rec.published_by = by
            return rec

    def publish(
        self,
        doc_id: str,
        by: str = "",
        now: Optional[float] = None,
    ) -> Optional[PublicationRecord]:
        """Transition to ``published`` and stamp ``published_at``."""
        ts = self._now(now)
        with self._lock:
            rec = self._records.get(doc_id)
            if rec is None:
                return None
            allowed = _TRANSITIONS.get(rec.state, frozenset())
            if "published" not in allowed:
                return None
            rec.state = "published"
            rec.state_changed_at = ts
            rec.published_at = ts
            if by:
                rec.published_by = by
            return rec

    def unpublish(
        self,
        doc_id: str,
        by: str = "",
        now: Optional[float] = None,
    ) -> Optional[PublicationRecord]:
        """Transition to ``unpublished``."""
        ts = self._now(now)
        with self._lock:
            rec = self._records.get(doc_id)
            if rec is None:
                return None
            allowed = _TRANSITIONS.get(rec.state, frozenset())
            if "unpublished" not in allowed:
                return None
            rec.state = "unpublished"
            rec.state_changed_at = ts
            if by:
                rec.published_by = by
            return rec

    def archive(
        self,
        doc_id: str,
        by: str = "",
        now: Optional[float] = None,
    ) -> Optional[PublicationRecord]:
        """Transition to ``archived`` (terminal)."""
        ts = self._now(now)
        with self._lock:
            rec = self._records.get(doc_id)
            if rec is None:
                return None
            allowed = _TRANSITIONS.get(rec.state, frozenset())
            if "archived" not in allowed:
                return None
            rec.state = "archived"
            rec.state_changed_at = ts
            if by:
                rec.published_by = by
            return rec

    # ------------------------------------------------------------------
    # Time-driven
    # ------------------------------------------------------------------

    def process_scheduled(self, now: Optional[float] = None) -> List[str]:
        """Publish all scheduled docs whose ``scheduled_for`` is in the past.

        Returns the sorted list of newly-published doc ids.
        """
        ts = self._now(now)
        published: List[str] = []
        with self._lock:
            for doc_id, rec in self._records.items():
                if rec.state != "scheduled":
                    continue
                if rec.scheduled_for is None:
                    continue
                if rec.scheduled_for <= ts:
                    rec.state = "published"
                    rec.state_changed_at = ts
                    rec.published_at = ts
                    published.append(doc_id)
        published.sort()
        return published

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_record(self, doc_id: str) -> Optional[PublicationRecord]:
        """Return the record for ``doc_id`` (or ``None``)."""
        with self._lock:
            return self._records.get(doc_id)

    def state_of(self, doc_id: str) -> Optional[str]:
        """Return the current state of ``doc_id`` (or ``None``)."""
        with self._lock:
            rec = self._records.get(doc_id)
            return rec.state if rec is not None else None

    def docs_in_state(self, state: str) -> List[str]:
        """Return a sorted list of doc ids currently in ``state``."""
        with self._lock:
            return sorted(
                doc_id for doc_id, rec in self._records.items() if rec.state == state
            )

    def published_docs(self) -> List[str]:
        """Return a sorted list of doc ids in state ``published``."""
        return self.docs_in_state("published")

    def scheduled_docs(self) -> List[PublicationRecord]:
        """Return scheduled records sorted by ``scheduled_for`` ascending.

        Records without a ``scheduled_for`` are sorted last.
        """
        with self._lock:
            recs = [r for r in self._records.values() if r.state == "scheduled"]
        recs.sort(key=lambda r: (r.scheduled_for is None, r.scheduled_for or 0.0))
        return recs

    def delete(self, doc_id: str) -> bool:
        """Forget the record for ``doc_id``. Returns ``True`` if removed."""
        with self._lock:
            return self._records.pop(doc_id, None) is not None

    def clear_all(self) -> int:
        """Remove all records. Returns the number of records removed."""
        with self._lock:
            n = len(self._records)
            self._records.clear()
            return n

    def stats(self, now: Optional[float] = None) -> PublicationStats:
        """Aggregate statistics."""
        ts = self._now(now)
        with self._lock:
            counts: Dict[str, int] = {s: 0 for s in VALID_STATES}
            scheduled_pending = 0
            for rec in self._records.values():
                counts[rec.state] = counts.get(rec.state, 0) + 1
                if (
                    rec.state == "scheduled"
                    and rec.scheduled_for is not None
                    and rec.scheduled_for > ts
                ):
                    scheduled_pending += 1
            return PublicationStats(
                total_docs=len(self._records),
                state_counts=counts,
                scheduled_pending=scheduled_pending,
            )
