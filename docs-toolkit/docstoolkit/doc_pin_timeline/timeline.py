"""E435 DocPinTimeline — time-bounded document pinning.

Pure stdlib, no third-party dependencies. Thread-safe via
``threading.Lock``. All public types are dataclasses.

Design
------
* Each pin has a unique ``pin_id`` (UUID4 hex).
* Pins may be permanent (``expires_at is None``) or time-bounded.
* A pin with ``expires_at <= now`` is considered *expired*; expired
  pins remain stored until explicitly purged via :meth:`purge_expired`
  or :meth:`unpin`/:meth:`clear_all`.
* Active pin ordering: ``(-priority, pinned_at)`` — highest priority
  first; ties broken by earliest ``pinned_at``.
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class TimedPin:
    """A pinning entry with optional expiry."""

    pin_id: str
    doc_id: str
    pinned_by: str = ""
    pinned_at: float = 0.0
    expires_at: Optional[float] = None
    priority: int = 0
    note: str = ""


@dataclass
class TimelineStats:
    """Aggregate statistics for the timeline."""

    total_pins: int          # non-expired
    expired_count: int
    unique_docs: int
    permanent_count: int     # pins with expires_at is None


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------


class DocPinTimeline:
    """Thread-safe in-memory time-bounded document pin manager.

    Internal storage
    ----------------
    ``_pins``    – pin_id → :class:`TimedPin`
    ``_by_doc``  – doc_id → set[pin_id]
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._pins: Dict[str, TimedPin] = {}
        self._by_doc: Dict[str, Set[str]] = {}

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return now if now is not None else time.time()

    @staticmethod
    def _is_expired(pin: TimedPin, now: float) -> bool:
        return pin.expires_at is not None and pin.expires_at <= now

    # ------------------------------------------------------------------
    # Core mutations
    # ------------------------------------------------------------------

    def pin(
        self,
        doc_id: str,
        pinned_by: str = "",
        expires_at: Optional[float] = None,
        duration_seconds: Optional[float] = None,
        priority: int = 0,
        note: str = "",
        now: Optional[float] = None,
    ) -> TimedPin:
        """Create a new timed pin for *doc_id*.

        If *duration_seconds* is supplied it overrides *expires_at* —
        the computed expiry is ``now + duration_seconds``.
        """
        ts = self._now(now)
        if duration_seconds is not None:
            effective_expiry: Optional[float] = ts + duration_seconds
        else:
            effective_expiry = expires_at
        pin_id = uuid.uuid4().hex
        pin = TimedPin(
            pin_id=pin_id,
            doc_id=doc_id,
            pinned_by=pinned_by,
            pinned_at=ts,
            expires_at=effective_expiry,
            priority=priority,
            note=note,
        )
        with self._lock:
            self._pins[pin_id] = pin
            self._by_doc.setdefault(doc_id, set()).add(pin_id)
        return pin

    def unpin(self, pin_id: str) -> bool:
        """Remove a single pin by id. Returns ``True`` if removed."""
        with self._lock:
            pin = self._pins.pop(pin_id, None)
            if pin is None:
                return False
            doc_set = self._by_doc.get(pin.doc_id)
            if doc_set is not None:
                doc_set.discard(pin_id)
                if not doc_set:
                    del self._by_doc[pin.doc_id]
            return True

    def unpin_all_for_doc(self, doc_id: str) -> int:
        """Remove every pin for *doc_id*. Returns count removed."""
        with self._lock:
            doc_set = self._by_doc.pop(doc_id, None)
            if doc_set is None:
                return 0
            count = 0
            for pin_id in doc_set:
                if self._pins.pop(pin_id, None) is not None:
                    count += 1
            return count

    def extend(
        self,
        pin_id: str,
        additional_seconds: float,
        now: Optional[float] = None,
    ) -> bool:
        """Extend the expiry of *pin_id* by *additional_seconds*.

        * If the pin currently has an ``expires_at``, it is incremented.
        * If the pin is permanent, ``expires_at`` is set to
          ``now + additional_seconds``.
        Returns ``False`` if the pin does not exist.
        """
        ts = self._now(now)
        with self._lock:
            pin = self._pins.get(pin_id)
            if pin is None:
                return False
            if pin.expires_at is None:
                pin.expires_at = ts + additional_seconds
            else:
                pin.expires_at = pin.expires_at + additional_seconds
            return True

    def make_permanent(self, pin_id: str) -> bool:
        """Set ``expires_at`` to ``None``. Returns ``False`` if missing."""
        with self._lock:
            pin = self._pins.get(pin_id)
            if pin is None:
                return False
            pin.expires_at = None
            return True

    def purge_expired(self, now: Optional[float] = None) -> int:
        """Permanently remove all expired pins. Returns count removed."""
        ts = self._now(now)
        with self._lock:
            to_remove = [
                pid for pid, p in self._pins.items() if self._is_expired(p, ts)
            ]
            for pid in to_remove:
                pin = self._pins.pop(pid)
                doc_set = self._by_doc.get(pin.doc_id)
                if doc_set is not None:
                    doc_set.discard(pid)
                    if not doc_set:
                        del self._by_doc[pin.doc_id]
            return len(to_remove)

    def clear_all(self) -> int:
        """Remove every pin. Returns count removed."""
        with self._lock:
            count = len(self._pins)
            self._pins.clear()
            self._by_doc.clear()
            return count

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_pin(self, pin_id: str) -> Optional[TimedPin]:
        """Return the :class:`TimedPin` or ``None``."""
        with self._lock:
            return self._pins.get(pin_id)

    def is_pinned(self, doc_id: str, now: Optional[float] = None) -> bool:
        """Return ``True`` if *doc_id* has at least one non-expired pin."""
        ts = self._now(now)
        with self._lock:
            doc_set = self._by_doc.get(doc_id)
            if not doc_set:
                return False
            for pin_id in doc_set:
                pin = self._pins.get(pin_id)
                if pin is not None and not self._is_expired(pin, ts):
                    return True
            return False

    def active_pins(self, now: Optional[float] = None) -> List[TimedPin]:
        """Return non-expired pins, sorted by (-priority, pinned_at)."""
        ts = self._now(now)
        with self._lock:
            result = [
                p for p in self._pins.values() if not self._is_expired(p, ts)
            ]
        result.sort(key=lambda p: (-p.priority, p.pinned_at))
        return result

    def pins_for_doc(
        self,
        doc_id: str,
        now: Optional[float] = None,
        include_expired: bool = False,
    ) -> List[TimedPin]:
        """Return pins for *doc_id*, sorted by (-priority, pinned_at)."""
        ts = self._now(now)
        with self._lock:
            doc_set = self._by_doc.get(doc_id, set())
            pins = [self._pins[pid] for pid in doc_set if pid in self._pins]
        if not include_expired:
            pins = [p for p in pins if not self._is_expired(p, ts)]
        pins.sort(key=lambda p: (-p.priority, p.pinned_at))
        return pins

    def expired_pins(self, now: Optional[float] = None) -> List[TimedPin]:
        """Return expired pins, sorted by ``expires_at`` ascending."""
        ts = self._now(now)
        with self._lock:
            result = [
                p for p in self._pins.values() if self._is_expired(p, ts)
            ]
        # expired pins always have a non-None expires_at by definition
        result.sort(key=lambda p: p.expires_at if p.expires_at is not None else 0.0)
        return result

    def expiring_soon(
        self,
        within_seconds: float,
        now: Optional[float] = None,
    ) -> List[TimedPin]:
        """Return non-expired pins whose ``expires_at`` falls within the
        next *within_seconds*. Sorted ascending by ``expires_at``.
        """
        ts = self._now(now)
        cutoff = ts + within_seconds
        with self._lock:
            result = [
                p
                for p in self._pins.values()
                if p.expires_at is not None
                and not self._is_expired(p, ts)
                and p.expires_at <= cutoff
            ]
        result.sort(key=lambda p: p.expires_at if p.expires_at is not None else 0.0)
        return result

    def all_doc_ids(self, now: Optional[float] = None) -> List[str]:
        """Return sorted unique doc ids that have at least one active pin."""
        ts = self._now(now)
        with self._lock:
            docs: Set[str] = set()
            for p in self._pins.values():
                if not self._is_expired(p, ts):
                    docs.add(p.doc_id)
        return sorted(docs)

    def stats(self, now: Optional[float] = None) -> TimelineStats:
        """Return aggregate statistics evaluated at *now*."""
        ts = self._now(now)
        with self._lock:
            total = 0
            expired = 0
            permanent = 0
            active_docs: Set[str] = set()
            for p in self._pins.values():
                if self._is_expired(p, ts):
                    expired += 1
                else:
                    total += 1
                    active_docs.add(p.doc_id)
                    if p.expires_at is None:
                        permanent += 1
            return TimelineStats(
                total_pins=total,
                expired_count=expired,
                unique_docs=len(active_docs),
                permanent_count=permanent,
            )
