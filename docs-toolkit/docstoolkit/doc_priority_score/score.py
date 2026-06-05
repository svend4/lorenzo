"""E376 DocPriorityScore — weighted priority score implementation."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ScoreFactor:
    """A named weighted factor used in priority computation."""

    name: str
    weight: float = 1.0
    description: str = ""


@dataclass
class PriorityScore:
    """Computed priority score for a single document."""

    doc_id: str
    total_score: float
    factor_scores: dict = field(default_factory=dict)
    computed_at: float = 0.0


@dataclass
class PriorityStats:
    """Aggregate statistics over the score store."""

    total_factors: int
    total_scores: int
    unique_docs: int
    avg_score: float


class DocPriorityScore:
    """Weighted priority score store for documents.

    Thread-safe; uses a single :class:`threading.Lock` to guard all state.
    """

    def __init__(self) -> None:
        self._factors: dict[str, ScoreFactor] = {}
        self._values: dict[tuple, float] = {}
        self._cached_scores: dict[str, PriorityScore] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ factors
    def define_factor(self, factor: ScoreFactor) -> None:
        """Define (or replace) a factor by name. Invalidates cached scores."""
        with self._lock:
            self._factors[factor.name] = factor
            self._cached_scores.clear()

    def remove_factor(self, name: str) -> bool:
        """Remove a factor and all its values. Returns True if removed."""
        with self._lock:
            if name not in self._factors:
                return False
            del self._factors[name]
            affected_docs = set()
            for key in list(self._values.keys()):
                doc_id, factor_name = key
                if factor_name == name:
                    del self._values[key]
                    affected_docs.add(doc_id)
            for doc_id in affected_docs:
                self._cached_scores.pop(doc_id, None)
            return True

    def get_factor(self, name: str) -> Optional[ScoreFactor]:
        with self._lock:
            return self._factors.get(name)

    def list_factors(self) -> list[ScoreFactor]:
        with self._lock:
            return sorted(self._factors.values(), key=lambda f: f.name)

    # ------------------------------------------------------------------- values
    def set_value(self, doc_id: str, factor_name: str, value: float) -> bool:
        """Store a raw value for (doc, factor). Returns True if factor defined."""
        with self._lock:
            if factor_name not in self._factors:
                return False
            self._values[(doc_id, factor_name)] = float(value)
            self._cached_scores.pop(doc_id, None)
            return True

    def get_value(self, doc_id: str, factor_name: str) -> Optional[float]:
        with self._lock:
            return self._values.get((doc_id, factor_name))

    # ------------------------------------------------------------------ compute
    def _compute_locked(self, doc_id: str, now: Optional[float]) -> PriorityScore:
        total = 0.0
        contributions: dict = {}
        for (d_id, f_name), value in self._values.items():
            if d_id != doc_id:
                continue
            factor = self._factors.get(f_name)
            if factor is None:
                continue
            contribution = value * factor.weight
            contributions[f_name] = contribution
            total += contribution
        ts = now if now is not None else time.time()
        score = PriorityScore(
            doc_id=doc_id,
            total_score=total,
            factor_scores=contributions,
            computed_at=ts,
        )
        self._cached_scores[doc_id] = score
        return score

    def compute(self, doc_id: str, now: Optional[float] = None) -> PriorityScore:
        with self._lock:
            return self._compute_locked(doc_id, now)

    def score_for(
        self, doc_id: str, now: Optional[float] = None
    ) -> Optional[PriorityScore]:
        with self._lock:
            cached = self._cached_scores.get(doc_id)
            if cached is not None:
                return cached
            has_values = any(d_id == doc_id for (d_id, _) in self._values.keys())
            if not has_values:
                return None
            return self._compute_locked(doc_id, now)

    # ------------------------------------------------------------------- docs
    def clear_doc(self, doc_id: str) -> int:
        with self._lock:
            removed = 0
            for key in list(self._values.keys()):
                d_id, _ = key
                if d_id == doc_id:
                    del self._values[key]
                    removed += 1
            self._cached_scores.pop(doc_id, None)
            return removed

    def _doc_ids_with_values_locked(self) -> set:
        return {d_id for (d_id, _) in self._values.keys()}

    def top_docs(
        self, limit: int = 10, now: Optional[float] = None
    ) -> list[tuple]:
        with self._lock:
            doc_ids = self._doc_ids_with_values_locked()
            scored = [
                (d, self._compute_locked(d, now).total_score) for d in doc_ids
            ]
            scored.sort(key=lambda x: (-x[1], x[0]))
            return scored[:limit]

    def bottom_docs(
        self, limit: int = 10, now: Optional[float] = None
    ) -> list[tuple]:
        with self._lock:
            doc_ids = self._doc_ids_with_values_locked()
            scored = [
                (d, self._compute_locked(d, now).total_score) for d in doc_ids
            ]
            scored.sort(key=lambda x: (x[1], x[0]))
            return scored[:limit]

    def all_doc_ids(self) -> list[str]:
        with self._lock:
            return sorted(self._doc_ids_with_values_locked())

    # -------------------------------------------------------------------- stats
    def stats(self) -> PriorityStats:
        with self._lock:
            doc_ids = self._doc_ids_with_values_locked()
            unique = len(doc_ids)
            totals = [self._compute_locked(d, None).total_score for d in doc_ids]
            avg = (sum(totals) / len(totals)) if totals else 0.0
            return PriorityStats(
                total_factors=len(self._factors),
                total_scores=len(self._cached_scores),
                unique_docs=unique,
                avg_score=avg,
            )
