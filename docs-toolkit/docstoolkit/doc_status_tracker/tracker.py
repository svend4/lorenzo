"""Document lifecycle status tracker with full transition history.

Tracks document status (e.g. draft/review/published/archived) and records
every transition.  Pure stdlib, thread-safe via a single threading.Lock.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StatusTransition:
    """A single recorded status change for a document."""

    transition_id: int
    doc_id: str
    from_status: Optional[str]   # None when the status is set for the first time
    to_status: str
    changed_by: str
    reason: str = ""
    timestamp: float = 0.0


@dataclass
class DocStatus:
    """Current status snapshot for a single document."""

    doc_id: str
    current_status: str
    changed_by: str
    last_changed_at: float
    transition_count: int


@dataclass
class StatusStats:
    """Aggregate statistics across all tracked documents."""

    total_docs: int
    status_counts: dict  # status -> count of docs currently in that status
    total_transitions: int


class DocStatusTracker:
    """Tracks document lifecycle status with a full audit trail.

    Parameters
    ----------
    allowed_statuses:
        When provided, ``set_status`` raises ``ValueError`` for any status
        value not in this list.
    """

    def __init__(self, allowed_statuses: Optional[list] = None) -> None:
        self._allowed: Optional[frozenset] = (
            frozenset(allowed_statuses) if allowed_statuses is not None else None
        )
        # doc_id -> DocStatus
        self._current: dict = {}
        # doc_id -> list[StatusTransition] (append-only, chronological)
        self._history: dict = {}
        # auto-increment counter for transition IDs
        self._next_id: int = 1
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Core mutations
    # ------------------------------------------------------------------

    def set_status(
        self,
        doc_id: str,
        status: str,
        changed_by: str = "",
        reason: str = "",
        now: Optional[float] = None,
    ) -> StatusTransition:
        """Set or change the status of a document.

        Records a :class:`StatusTransition` capturing the previous status
        (``None`` when this is the first status assignment for the document).

        Parameters
        ----------
        doc_id:
            Unique identifier of the document.
        status:
            New status value to assign.
        changed_by:
            Actor responsible for the change (human name, system ID, …).
        reason:
            Optional free-text explanation for the transition.
        now:
            Timestamp to record; defaults to ``time.time()`` when ``None``.

        Raises
        ------
        ValueError
            If *allowed_statuses* was configured and *status* is not in it.
        """
        if self._allowed is not None and status not in self._allowed:
            raise ValueError(
                f"Status {status!r} is not in allowed_statuses: "
                f"{sorted(self._allowed)}"
            )

        ts = now if now is not None else time.time()

        with self._lock:
            existing = self._current.get(doc_id)
            from_status: Optional[str] = existing.current_status if existing else None

            tid = self._next_id
            self._next_id += 1

            transition = StatusTransition(
                transition_id=tid,
                doc_id=doc_id,
                from_status=from_status,
                to_status=status,
                changed_by=changed_by,
                reason=reason,
                timestamp=ts,
            )

            # Update or create current-status record
            if existing is not None:
                existing.current_status = status
                existing.changed_by = changed_by
                existing.last_changed_at = ts
                existing.transition_count += 1
            else:
                self._current[doc_id] = DocStatus(
                    doc_id=doc_id,
                    current_status=status,
                    changed_by=changed_by,
                    last_changed_at=ts,
                    transition_count=1,
                )
                self._history[doc_id] = []

            self._history[doc_id].append(transition)

        return transition

    def bulk_set(
        self,
        doc_ids: list,
        status: str,
        changed_by: str = "",
        now: Optional[float] = None,
    ) -> int:
        """Apply *status* to every document in *doc_ids*.

        Parameters
        ----------
        doc_ids:
            Documents to update.
        status:
            New status for all listed documents.
        changed_by:
            Actor performing the bulk operation.
        now:
            Timestamp; defaults to ``time.time()``.

        Returns
        -------
        int
            Number of documents whose status was successfully updated.
        """
        ts = now if now is not None else time.time()
        count = 0
        for doc_id in doc_ids:
            self.set_status(doc_id, status, changed_by=changed_by, now=ts)
            count += 1
        return count

    def delete_doc(self, doc_id: str) -> bool:
        """Remove all tracking data for *doc_id*.

        Returns
        -------
        bool
            ``True`` if the document existed and was removed; ``False``
            otherwise.
        """
        with self._lock:
            if doc_id not in self._current:
                return False
            del self._current[doc_id]
            del self._history[doc_id]
            return True

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_status(self, doc_id: str) -> Optional[DocStatus]:
        """Return the current status record, or ``None`` if never tracked."""
        with self._lock:
            return self._current.get(doc_id)

    def current_status(self, doc_id: str) -> Optional[str]:
        """Return just the status string, or ``None`` if never tracked."""
        with self._lock:
            rec = self._current.get(doc_id)
            return rec.current_status if rec is not None else None

    def history(self, doc_id: str, limit: Optional[int] = None) -> list:
        """Return the transition history for *doc_id*, newest first.

        Parameters
        ----------
        doc_id:
            Target document.
        limit:
            When set, return at most this many transitions (most recent).

        Returns
        -------
        list[StatusTransition]
            Empty list if the document has never been tracked.
        """
        with self._lock:
            entries: list = list(reversed(self._history.get(doc_id, [])))
        if limit is not None:
            entries = entries[:limit]
        return entries

    def docs_with_status(self, status: str) -> list:
        """Return a sorted list of doc_ids currently in *status*."""
        with self._lock:
            return sorted(
                doc_id
                for doc_id, rec in self._current.items()
                if rec.current_status == status
            )

    def transition_count(self, doc_id: str) -> int:
        """Return the number of status changes recorded for *doc_id* (0 if unknown)."""
        with self._lock:
            rec = self._current.get(doc_id)
            return rec.transition_count if rec is not None else 0

    def stats(self) -> StatusStats:
        """Return aggregate statistics about all tracked documents."""
        with self._lock:
            status_counts: dict = {}
            for rec in self._current.values():
                status_counts[rec.current_status] = (
                    status_counts.get(rec.current_status, 0) + 1
                )
            total_transitions = sum(
                len(transitions) for transitions in self._history.values()
            )
            return StatusStats(
                total_docs=len(self._current),
                status_counts=status_counts,
                total_transitions=total_transitions,
            )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def total_docs(self) -> int:
        """Number of documents currently tracked."""
        with self._lock:
            return len(self._current)

    @property
    def total_transitions(self) -> int:
        """Total number of status transitions recorded across all documents."""
        with self._lock:
            return sum(len(t) for t in self._history.values())
