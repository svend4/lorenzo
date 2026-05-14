"""DocExpiryTracker — track document expiry dates and overdue status."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class ExpiryRecord:
    """Expiry metadata for a single document."""

    doc_id: str
    expires_at: float
    created_at: float = 0.0
    renewed_at: Optional[float] = None
    grace_seconds: float = 0.0
    label: str = ""


@dataclass
class ExpiryStats:
    """Aggregate statistics for all tracked documents."""

    total_tracked: int
    expired_count: int
    expiring_soon_count: int
    soon_seconds: float = 3600.0


class DocExpiryTracker:
    """Main interface for tracking document expiry dates.

    All public methods are thread-safe via an internal :class:`threading.Lock`.
    Time can be injected via the ``now`` parameter (Unix timestamp) to enable
    deterministic testing; when omitted, :func:`time.time` is used.
    """

    def __init__(self) -> None:
        self._records: dict[str, ExpiryRecord] = {}
        self._lock = threading.Lock()

    # ---------------------------------------------------------------------- #
    # Internal helpers
    # ---------------------------------------------------------------------- #

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return float(now) if now is not None else time.time()

    def _is_expired_record(self, record: ExpiryRecord, now: float) -> bool:
        """Return True if *record* is past its effective expiry (expires_at + grace)."""
        return now > record.expires_at + record.grace_seconds

    def _is_expiring_soon_record(
        self, record: ExpiryRecord, now: float, within_seconds: float
    ) -> bool:
        """Return True if record expires within *within_seconds* but is NOT yet expired."""
        effective_expiry = record.expires_at + record.grace_seconds
        return not self._is_expired_record(record, now) and (
            effective_expiry <= now + within_seconds
        )

    # ---------------------------------------------------------------------- #
    # Mutators
    # ---------------------------------------------------------------------- #

    def track(
        self,
        doc_id: str,
        expires_at: float,
        grace_seconds: float = 0.0,
        label: str = "",
        now: Optional[float] = None,
    ) -> ExpiryRecord:
        """Register or replace an expiry record for *doc_id*.

        Sets ``created_at`` to *now* (or :func:`time.time` if omitted).
        """
        ts = self._now(now)
        record = ExpiryRecord(
            doc_id=doc_id,
            expires_at=float(expires_at),
            created_at=ts,
            renewed_at=None,
            grace_seconds=float(grace_seconds),
            label=label,
        )
        with self._lock:
            self._records[doc_id] = record
        return record

    def renew(
        self,
        doc_id: str,
        new_expires_at: float,
        now: Optional[float] = None,
    ) -> Optional[ExpiryRecord]:
        """Update *expires_at* and set *renewed_at* to *now*.

        Returns the updated record, or ``None`` if *doc_id* is not tracked.
        """
        ts = self._now(now)
        with self._lock:
            record = self._records.get(doc_id)
            if record is None:
                return None
            record.expires_at = float(new_expires_at)
            record.renewed_at = ts
            return record

    def extend(
        self,
        doc_id: str,
        extra_seconds: float,
        now: Optional[float] = None,
    ) -> Optional[ExpiryRecord]:
        """Add *extra_seconds* to the current *expires_at*.

        Returns the updated record, or ``None`` if *doc_id* is not tracked.
        """
        ts = self._now(now)
        with self._lock:
            record = self._records.get(doc_id)
            if record is None:
                return None
            record.expires_at += float(extra_seconds)
            record.renewed_at = ts
            return record

    def untrack(self, doc_id: str) -> bool:
        """Remove *doc_id* from tracking.

        Returns ``True`` if the record existed and was removed, ``False`` otherwise.
        """
        with self._lock:
            if doc_id in self._records:
                del self._records[doc_id]
                return True
            return False

    # ---------------------------------------------------------------------- #
    # Lookups
    # ---------------------------------------------------------------------- #

    def get(self, doc_id: str) -> Optional[ExpiryRecord]:
        """Return the :class:`ExpiryRecord` for *doc_id*, or ``None`` if not tracked."""
        with self._lock:
            return self._records.get(doc_id)

    def is_expired(self, doc_id: str, now: Optional[float] = None) -> bool:
        """Return ``True`` if *now* > *expires_at* + *grace_seconds*.

        Returns ``False`` if *doc_id* is not tracked.
        """
        ts = self._now(now)
        with self._lock:
            record = self._records.get(doc_id)
            if record is None:
                return False
            return self._is_expired_record(record, ts)

    def time_until_expiry(
        self, doc_id: str, now: Optional[float] = None
    ) -> Optional[float]:
        """Return seconds until expiry (negative if already expired).

        Returns ``None`` if *doc_id* is not tracked.
        The effective expiry point is ``expires_at + grace_seconds``.
        """
        ts = self._now(now)
        with self._lock:
            record = self._records.get(doc_id)
            if record is None:
                return None
            return (record.expires_at + record.grace_seconds) - ts

    def expired_docs(self, now: Optional[float] = None) -> list[str]:
        """Return sorted list of doc_ids that are currently expired."""
        ts = self._now(now)
        with self._lock:
            return sorted(
                doc_id
                for doc_id, record in self._records.items()
                if self._is_expired_record(record, ts)
            )

    def expiring_soon(
        self, within_seconds: float = 3600.0, now: Optional[float] = None
    ) -> list[str]:
        """Return sorted doc_ids that expire within *within_seconds* but are NOT yet expired."""
        ts = self._now(now)
        with self._lock:
            return sorted(
                doc_id
                for doc_id, record in self._records.items()
                if self._is_expiring_soon_record(record, ts, within_seconds)
            )

    def all_records(self) -> list[ExpiryRecord]:
        """Return all :class:`ExpiryRecord` objects sorted by *expires_at*."""
        with self._lock:
            return sorted(self._records.values(), key=lambda r: r.expires_at)

    def stats(
        self,
        now: Optional[float] = None,
        soon_seconds: float = 3600.0,
    ) -> ExpiryStats:
        """Return aggregate :class:`ExpiryStats` for the current state."""
        ts = self._now(now)
        with self._lock:
            total = len(self._records)
            expired_count = sum(
                1
                for record in self._records.values()
                if self._is_expired_record(record, ts)
            )
            expiring_soon_count = sum(
                1
                for record in self._records.values()
                if self._is_expiring_soon_record(record, ts, soon_seconds)
            )
        return ExpiryStats(
            total_tracked=total,
            expired_count=expired_count,
            expiring_soon_count=expiring_soon_count,
            soon_seconds=soon_seconds,
        )
