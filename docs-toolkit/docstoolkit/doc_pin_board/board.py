"""E306 DocPinBoard — per-user document pinning with ordered pin lists.

Pure stdlib, no third-party dependencies.  Thread-safe via
``threading.Lock``.  All public types are dataclasses.

Design
------
* Each (user_id, doc_id) pair is unique — attempting to pin the same
  document twice returns ``False`` without modifying the store.
* ``position`` reflects display order: 0 = highest priority.
  Positions are always kept as a contiguous sequence 0…N-1.
* ``_user_pins`` tracks insertion order so that ``pins_for_user``
  returns documents in the order they were originally pinned
  (subject to moves made via ``move_pin``).
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class PinnedDoc:
    """A single pinned document entry owned by one user."""

    user_id: str
    doc_id: str
    pinned_at: float = 0.0
    position: int = 0
    note: str = ""


@dataclass
class PinBoardStats:
    """Aggregate statistics across all users and documents."""

    total_pins: int
    unique_users: int
    unique_docs: int
    avg_pins_per_user: float


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------


class DocPinBoard:
    """Thread-safe in-memory per-user document pin board.

    Internal storage
    ----------------
    ``_pins``      – (user_id, doc_id) → :class:`PinnedDoc`
    ``_user_pins`` – user_id → ordered list[doc_id] (insertion / move order)
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._pins: Dict[Tuple[str, str], PinnedDoc] = {}
        self._user_pins: Dict[str, List[str]] = {}

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return now if now is not None else time.time()

    def _reassign_positions(self, user_id: str) -> None:
        """Rewrite sequential positions 0…N-1 for *user_id*'s pin list."""
        for idx, doc_id in enumerate(self._user_pins[user_id]):
            self._pins[(user_id, doc_id)].position = idx

    # ------------------------------------------------------------------
    # Core mutations
    # ------------------------------------------------------------------

    def pin(
        self,
        user_id: str,
        doc_id: str,
        note: str = "",
        now: Optional[float] = None,
    ) -> bool:
        """Pin *doc_id* for *user_id*.

        Returns ``True`` if newly pinned, ``False`` if already pinned.
        Position is set to ``len(current_pins)`` before appending
        (i.e. appended at the end).
        """
        ts = self._now(now)
        with self._lock:
            key = (user_id, doc_id)
            if key in self._pins:
                return False
            doc_list = self._user_pins.setdefault(user_id, [])
            position = len(doc_list)
            pinned = PinnedDoc(
                user_id=user_id,
                doc_id=doc_id,
                pinned_at=ts,
                position=position,
                note=note,
            )
            self._pins[key] = pinned
            doc_list.append(doc_id)
            return True

    def unpin(self, user_id: str, doc_id: str) -> bool:
        """Remove the pin for *(user_id, doc_id)*.

        Returns ``True`` if the pin existed and was removed.
        Remaining pins for *user_id* are re-numbered sequentially.
        """
        with self._lock:
            key = (user_id, doc_id)
            if key not in self._pins:
                return False
            del self._pins[key]
            doc_list = self._user_pins.get(user_id, [])
            doc_list.remove(doc_id)
            if not doc_list:
                del self._user_pins[user_id]
            else:
                self._reassign_positions(user_id)
            return True

    def move_pin(self, user_id: str, doc_id: str, new_position: int) -> bool:
        """Reorder *doc_id* to *new_position* within *user_id*'s pin list.

        *new_position* is clamped to ``[0, len-1]``.  The pin is removed
        from its current slot and inserted at the (clamped) target slot,
        then all positions are renumbered sequentially.

        Returns ``False`` if the pin does not exist.
        """
        with self._lock:
            key = (user_id, doc_id)
            if key not in self._pins:
                return False
            doc_list = self._user_pins[user_id]
            n = len(doc_list)
            clamped = max(0, min(new_position, n - 1))
            doc_list.remove(doc_id)
            doc_list.insert(clamped, doc_id)
            self._reassign_positions(user_id)
            return True

    def update_note(self, user_id: str, doc_id: str, note: str) -> bool:
        """Update the note for *(user_id, doc_id)*.

        Returns ``False`` if the pin does not exist.
        """
        with self._lock:
            pinned = self._pins.get((user_id, doc_id))
            if pinned is None:
                return False
            pinned.note = note
            return True

    def unpin_all(self, user_id: str) -> int:
        """Remove every pin for *user_id*.

        Returns the number of pins removed.
        """
        with self._lock:
            doc_list = self._user_pins.pop(user_id, [])
            count = len(doc_list)
            for doc_id in doc_list:
                self._pins.pop((user_id, doc_id), None)
            return count

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def is_pinned(self, user_id: str, doc_id: str) -> bool:
        """Return ``True`` if *doc_id* is pinned by *user_id*."""
        with self._lock:
            return (user_id, doc_id) in self._pins

    def get_pin(self, user_id: str, doc_id: str) -> Optional[PinnedDoc]:
        """Return the :class:`PinnedDoc` or ``None``."""
        with self._lock:
            return self._pins.get((user_id, doc_id))

    def pins_for_user(self, user_id: str) -> List[PinnedDoc]:
        """Return all pins for *user_id*, sorted by ``position`` ascending."""
        with self._lock:
            doc_list = self._user_pins.get(user_id, [])
            result = [self._pins[(user_id, doc_id)] for doc_id in doc_list]
            result.sort(key=lambda p: p.position)
            return result

    def users_who_pinned(self, doc_id: str) -> List[str]:
        """Return sorted list of user_ids that have *doc_id* pinned."""
        with self._lock:
            users = [
                user_id
                for (user_id, did) in self._pins
                if did == doc_id
            ]
            return sorted(users)

    def all_users(self) -> List[str]:
        """Return sorted list of users with at least one pin."""
        with self._lock:
            return sorted(self._user_pins.keys())

    def all_pinned_docs(self) -> List[str]:
        """Return sorted list of unique doc_ids pinned by anyone."""
        with self._lock:
            docs = {did for (_, did) in self._pins}
            return sorted(docs)

    def stats(self) -> PinBoardStats:
        """Return aggregate statistics."""
        with self._lock:
            total = len(self._pins)
            unique_users = len(self._user_pins)
            unique_docs = len({did for (_, did) in self._pins})
            avg = total / unique_users if unique_users > 0 else 0.0
            return PinBoardStats(
                total_pins=total,
                unique_users=unique_users,
                unique_docs=unique_docs,
                avg_pins_per_user=avg,
            )
