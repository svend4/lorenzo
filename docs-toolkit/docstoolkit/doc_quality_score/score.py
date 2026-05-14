"""E345 DocQualityScore — per-document quality dimension scoring.

Pure-stdlib, thread-safe quality scoring across user-defined dimensions
(e.g. ``clarity``, ``completeness``, ``accuracy``).  Each dimension has a
weight that contributes to a weighted overall score for every document.
"""

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Dimension:
    """A quality dimension definition."""

    name: str
    weight: float = 1.0
    description: str = ""


@dataclass
class DimensionScore:
    """A single dimension's score for a document."""

    doc_id: str
    dimension: str
    score: float
    evaluated_at: float = 0.0
    evaluator: str = ""


@dataclass
class QualityReport:
    """Aggregate scores for a document."""

    doc_id: str
    dimensions: dict = field(default_factory=dict)
    overall_score: float = 0.0
    dimension_count: int = 0


@dataclass
class QualityStats:
    """Global statistics about defined dimensions and recorded scores."""

    total_dimensions: int = 0
    total_evaluations: int = 0
    unique_docs: int = 0
    avg_overall_score: float = 0.0


class DocQualityScore:
    """Thread-safe per-document quality dimension scoring.

    Dimensions must be registered with :meth:`define_dimension` before
    scores can be recorded for them via :meth:`evaluate`.  A weighted
    overall score per document is produced by :meth:`report`, using only
    the dimensions that are currently defined.
    """

    def __init__(self) -> None:
        self._dimensions: dict = {}
        self._scores: dict = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Dimension management
    # ------------------------------------------------------------------
    def define_dimension(self, dim: Dimension) -> None:
        """Register a dimension or replace an existing one with the same name."""
        with self._lock:
            self._dimensions[dim.name] = dim

    def undefine_dimension(self, name: str) -> bool:
        """Remove a dimension and all scores for it.

        Returns ``True`` if the dimension existed (and was removed).
        """
        with self._lock:
            if name not in self._dimensions:
                return False
            del self._dimensions[name]
            keys = [k for k in self._scores if k[1] == name]
            for k in keys:
                del self._scores[k]
            return True

    def get_dimension(self, name: str) -> Optional[Dimension]:
        """Look up a dimension by name."""
        with self._lock:
            return self._dimensions.get(name)

    def list_dimensions(self) -> list:
        """Return all defined dimensions, sorted by name."""
        with self._lock:
            return sorted(self._dimensions.values(), key=lambda d: d.name)

    # ------------------------------------------------------------------
    # Score management
    # ------------------------------------------------------------------
    def evaluate(
        self,
        doc_id: str,
        dimension: str,
        score: float,
        evaluator: str = "",
        now: Optional[float] = None,
    ) -> Optional[DimensionScore]:
        """Record a score for ``doc_id`` along ``dimension``.

        Returns the stored :class:`DimensionScore`, or ``None`` if the
        dimension is not defined.
        """
        if now is None:
            now = time.time()
        with self._lock:
            if dimension not in self._dimensions:
                return None
            ds = DimensionScore(
                doc_id=doc_id,
                dimension=dimension,
                score=score,
                evaluated_at=now,
                evaluator=evaluator,
            )
            self._scores[(doc_id, dimension)] = ds
            return ds

    def get_score(self, doc_id: str, dimension: str) -> Optional[DimensionScore]:
        """Look up a single score for the given doc/dimension pair."""
        with self._lock:
            return self._scores.get((doc_id, dimension))

    def delete_score(self, doc_id: str, dimension: str) -> bool:
        """Delete a single score; ``True`` if it existed."""
        with self._lock:
            key = (doc_id, dimension)
            if key not in self._scores:
                return False
            del self._scores[key]
            return True

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------
    def report(self, doc_id: str) -> Optional[QualityReport]:
        """Build a :class:`QualityReport` for ``doc_id``.

        The overall score is a weighted average across the dimensions
        currently defined for which ``doc_id`` has a recorded score.
        Returns ``None`` if no scores at all exist for the document.
        """
        with self._lock:
            doc_scores = {
                dim: ds
                for (did, dim), ds in self._scores.items()
                if did == doc_id
            }
            if not doc_scores:
                return None

            total = 0.0
            weight_sum = 0.0
            considered: dict = {}
            for dim_name, ds in doc_scores.items():
                dim = self._dimensions.get(dim_name)
                if dim is None:
                    continue
                considered[dim_name] = ds
                total += ds.score * dim.weight
                weight_sum += dim.weight

            overall = total / weight_sum if weight_sum > 0 else 0.0
            return QualityReport(
                doc_id=doc_id,
                dimensions=considered,
                overall_score=overall,
                dimension_count=len(considered),
            )

    def scores_for_doc(self, doc_id: str) -> list:
        """All scores for one document, sorted by dimension name."""
        with self._lock:
            return sorted(
                (ds for (did, _dim), ds in self._scores.items() if did == doc_id),
                key=lambda d: d.dimension,
            )

    def scores_for_dimension(self, dimension: str) -> list:
        """All scores along one dimension, sorted by doc_id."""
        with self._lock:
            return sorted(
                (ds for (_did, dim), ds in self._scores.items() if dim == dimension),
                key=lambda d: d.doc_id,
            )

    # ------------------------------------------------------------------
    # Ranking
    # ------------------------------------------------------------------
    def _all_reports(self) -> list:
        """Compute reports for every document with at least one score."""
        # Note: called while not holding the lock; uses public report().
        doc_ids = self.all_doc_ids()
        reports = []
        for did in doc_ids:
            r = self.report(did)
            if r is not None:
                reports.append(r)
        return reports

    def top_docs(self, limit: int = 10) -> list:
        """Top documents by overall score (descending), then doc_id ascending."""
        reports = self._all_reports()
        reports.sort(key=lambda r: (-r.overall_score, r.doc_id))
        return [(r.doc_id, r.overall_score) for r in reports[:limit]]

    def bottom_docs(self, limit: int = 10) -> list:
        """Bottom documents by overall score (ascending), then doc_id ascending."""
        reports = self._all_reports()
        reports.sort(key=lambda r: (r.overall_score, r.doc_id))
        return [(r.doc_id, r.overall_score) for r in reports[:limit]]

    def all_doc_ids(self) -> list:
        """All documents that have at least one recorded score, sorted."""
        with self._lock:
            return sorted({did for (did, _dim) in self._scores})

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------
    def stats(self) -> QualityStats:
        """Global statistics, including average overall score across docs."""
        reports = self._all_reports()
        if reports:
            avg = sum(r.overall_score for r in reports) / len(reports)
        else:
            avg = 0.0
        with self._lock:
            return QualityStats(
                total_dimensions=len(self._dimensions),
                total_evaluations=len(self._scores),
                unique_docs=len({did for (did, _dim) in self._scores}),
                avg_overall_score=avg,
            )
