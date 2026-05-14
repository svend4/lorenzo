"""E370 DocFreshnessScanner — implementation."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FreshnessRecord:
    """Recorded last-touched timestamp for a single document."""

    doc_id: str
    last_modified: float
    last_reviewed: Optional[float] = None
    expected_review_interval: float = 0.0


@dataclass
class StaleDoc:
    """Doc identified as stale or overdue for review."""

    doc_id: str
    staleness_seconds: float
    overdue_review: bool
    reason: str


@dataclass
class FreshnessStats:
    """Aggregate freshness statistics."""

    total_records: int
    stale_count: int
    overdue_review_count: int
    avg_age_seconds: float


class DocFreshnessScanner:
    """Tracks per-document freshness and identifies stale or overdue docs."""

    def __init__(self) -> None:
        self._records: dict[str, FreshnessRecord] = {}
        self._lock = threading.Lock()

    # -- mutation ----------------------------------------------------------
    def record(
        self,
        doc_id: str,
        last_modified: float,
        expected_review_interval: float = 0.0,
        last_reviewed: Optional[float] = None,
    ) -> FreshnessRecord:
        """Create or replace a freshness record."""
        rec = FreshnessRecord(
            doc_id=doc_id,
            last_modified=last_modified,
            last_reviewed=last_reviewed,
            expected_review_interval=expected_review_interval,
        )
        with self._lock:
            self._records[doc_id] = rec
        return rec

    def update_modified(self, doc_id: str, last_modified: float) -> bool:
        with self._lock:
            rec = self._records.get(doc_id)
            if rec is None:
                return False
            rec.last_modified = last_modified
            return True

    def update_reviewed(self, doc_id: str, last_reviewed: float) -> bool:
        with self._lock:
            rec = self._records.get(doc_id)
            if rec is None:
                return False
            rec.last_reviewed = last_reviewed
            return True

    def remove(self, doc_id: str) -> bool:
        with self._lock:
            return self._records.pop(doc_id, None) is not None

    def clear(self) -> int:
        with self._lock:
            n = len(self._records)
            self._records.clear()
            return n

    # -- reads -------------------------------------------------------------
    def get(self, doc_id: str) -> Optional[FreshnessRecord]:
        with self._lock:
            return self._records.get(doc_id)

    def _now(self, now: Optional[float]) -> float:
        return time.time() if now is None else now

    def find_stale(
        self, older_than_seconds: float, now: Optional[float] = None
    ) -> list[StaleDoc]:
        t = self._now(now)
        result: list[StaleDoc] = []
        with self._lock:
            for rec in self._records.values():
                age = t - rec.last_modified
                if age >= older_than_seconds:
                    overdue = (
                        rec.expected_review_interval > 0
                        and (
                            rec.last_reviewed is None
                            or rec.last_reviewed + rec.expected_review_interval < t
                        )
                    )
                    result.append(
                        StaleDoc(
                            doc_id=rec.doc_id,
                            staleness_seconds=age,
                            overdue_review=overdue,
                            reason=f"unmodified for {age:.0f}s (>= {older_than_seconds:.0f}s)",
                        )
                    )
        result.sort(key=lambda s: s.staleness_seconds, reverse=True)
        return result

    def find_overdue_reviews(self, now: Optional[float] = None) -> list[StaleDoc]:
        t = self._now(now)
        result: list[StaleDoc] = []
        with self._lock:
            for rec in self._records.values():
                if rec.expected_review_interval <= 0:
                    continue
                if rec.last_reviewed is None:
                    result.append(
                        StaleDoc(
                            doc_id=rec.doc_id,
                            staleness_seconds=t - rec.last_modified,
                            overdue_review=True,
                            reason="never reviewed",
                        )
                    )
                elif rec.last_reviewed + rec.expected_review_interval < t:
                    result.append(
                        StaleDoc(
                            doc_id=rec.doc_id,
                            staleness_seconds=t - rec.last_modified,
                            overdue_review=True,
                            reason=(
                                f"review overdue since "
                                f"{rec.last_reviewed + rec.expected_review_interval:.0f}"
                            ),
                        )
                    )
        result.sort(key=lambda s: s.doc_id)
        return result

    def freshest_docs(
        self, limit: int = 10, now: Optional[float] = None
    ) -> list[tuple]:
        t = self._now(now)
        with self._lock:
            pairs = [(rec.doc_id, t - rec.last_modified) for rec in self._records.values()]
        pairs.sort(key=lambda p: p[1])
        return pairs[:limit]

    def stalest_docs(
        self, limit: int = 10, now: Optional[float] = None
    ) -> list[tuple]:
        t = self._now(now)
        with self._lock:
            pairs = [(rec.doc_id, t - rec.last_modified) for rec in self._records.values()]
        pairs.sort(key=lambda p: p[1], reverse=True)
        return pairs[:limit]

    def stats(
        self,
        stale_threshold: float = 30 * 24 * 3600,
        now: Optional[float] = None,
    ) -> FreshnessStats:
        t = self._now(now)
        with self._lock:
            recs = list(self._records.values())
        total = len(recs)
        if total == 0:
            return FreshnessStats(0, 0, 0, 0.0)

        ages = [t - r.last_modified for r in recs]
        avg = sum(ages) / total
        stale_count = sum(1 for a in ages if a >= stale_threshold)
        overdue = 0
        for r in recs:
            if r.expected_review_interval <= 0:
                continue
            if r.last_reviewed is None or r.last_reviewed + r.expected_review_interval < t:
                overdue += 1
        return FreshnessStats(
            total_records=total,
            stale_count=stale_count,
            overdue_review_count=overdue,
            avg_age_seconds=avg,
        )
