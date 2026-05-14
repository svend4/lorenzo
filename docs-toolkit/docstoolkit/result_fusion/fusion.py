"""Result fusion strategies for combining ranked lists from multiple sources (E17)."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from docstoolkit.result_fusion.result import SearchResult


class FusionMethod(Enum):
    """Supported fusion algorithms."""

    RRF = "rrf"                  # Reciprocal Rank Fusion
    WEIGHTED_SUM = "weighted_sum"
    BORDA = "borda"
    MAX_SCORE = "max_score"


@dataclass
class FusionConfig:
    """Configuration for :class:`ResultFusion`.

    Parameters
    ----------
    method:   Fusion algorithm to use (default: RRF).
    rrf_k:    Stability constant for RRF denominator (default: 60).
    weights:  Per-source weight mapping used by WEIGHTED_SUM (default: 1.0
              for any source not listed).
    """

    method: FusionMethod = FusionMethod.RRF
    rrf_k: int = 60
    weights: dict[str, float] = field(default_factory=dict)


@dataclass
class FusionResult:
    """Container returned by :class:`ResultFusion.fuse`.

    Parameters
    ----------
    results:       Final ranked list of :class:`SearchResult`, sorted by
                   fused score descending with ``rank`` re-assigned from 1.
    method:        The :class:`FusionMethod` that produced these results.
    source_counts: Number of results contributed by each source.
    """

    results: list[SearchResult]
    method: FusionMethod
    source_counts: dict[str, int]

    def top(self, n: int) -> list[SearchResult]:
        """Return the top-*n* results (by fused score)."""
        return self.results[:n]

    def by_doc_id(self, doc_id: str) -> Optional[SearchResult]:
        """Return the result with the given *doc_id*, or ``None`` if absent."""
        for r in self.results:
            if r.doc_id == doc_id:
                return r
        return None


class ResultFusion:
    """Combine ranked result lists from multiple retrieval sources.

    Supported methods: RRF, WEIGHTED_SUM, BORDA, MAX_SCORE.

    Usage::

        fusion = ResultFusion()
        fused = fusion.fuse(
            {"bm25": bm25_results, "dense": dense_results},
            FusionConfig(method=FusionMethod.RRF, rrf_k=60),
        )
        top5 = fused.top(5)
    """

    def fuse(
        self,
        result_lists: dict[str, list[SearchResult]],
        config: FusionConfig = None,
    ) -> FusionResult:
        """Fuse *result_lists* using the algorithm specified in *config*.

        Parameters
        ----------
        result_lists: Mapping from source name to ordered list of
                      :class:`SearchResult`.  Results must already be ordered
                      by descending relevance for rank-based methods.
        config:       Fusion configuration; defaults to
                      ``FusionConfig()`` (RRF, k=60) when omitted.

        Returns
        -------
        FusionResult with final ranked list and provenance metadata.
        """
        if config is None:
            config = FusionConfig()

        source_counts: dict[str, int] = {
            src: len(lst) for src, lst in result_lists.items()
        }

        method = config.method
        if method == FusionMethod.RRF:
            fused_scores = self._rrf(result_lists, config.rrf_k)
        elif method == FusionMethod.WEIGHTED_SUM:
            fused_scores = self._weighted_sum(result_lists, config.weights)
        elif method == FusionMethod.BORDA:
            fused_scores = self._borda(result_lists)
        elif method == FusionMethod.MAX_SCORE:
            fused_scores = self._max_score(result_lists)
        else:
            raise ValueError(f"Unknown fusion method: {method}")

        # Build final SearchResult list, sorted descending by fused score.
        # Use the first occurrence of each doc_id to carry metadata/source.
        doc_meta: dict[str, SearchResult] = {}
        for results in result_lists.values():
            for r in results:
                if r.doc_id not in doc_meta:
                    doc_meta[r.doc_id] = r

        sorted_ids = sorted(fused_scores, key=lambda d: fused_scores[d], reverse=True)
        final: list[SearchResult] = []
        for rank, doc_id in enumerate(sorted_ids, start=1):
            proto = doc_meta[doc_id]
            merged = SearchResult(
                doc_id=doc_id,
                score=fused_scores[doc_id],
                source=proto.source,
                rank=rank,
                metadata=dict(proto.metadata),
            )
            final.append(merged)

        return FusionResult(results=final, method=method, source_counts=source_counts)

    # ------------------------------------------------------------------
    # Private fusion implementations
    # ------------------------------------------------------------------

    @staticmethod
    def _rrf(
        result_lists: dict[str, list[SearchResult]],
        k: int,
    ) -> dict[str, float]:
        """Reciprocal Rank Fusion: score = sum(1 / (k + rank))."""
        scores: dict[str, float] = {}
        for results in result_lists.values():
            for r in results:
                # Use 1-based position within this list.
                rank = r.rank if r.rank >= 1 else (results.index(r) + 1)
                scores[r.doc_id] = scores.get(r.doc_id, 0.0) + 1.0 / (k + rank)
        return scores

    @staticmethod
    def _weighted_sum(
        result_lists: dict[str, list[SearchResult]],
        weights: dict[str, float],
    ) -> dict[str, float]:
        """Normalize scores per source, then sum * source_weight."""
        scores: dict[str, float] = {}
        for source, results in result_lists.items():
            if not results:
                continue
            w = weights.get(source, 1.0)
            raw_scores = [r.score for r in results]
            min_s = min(raw_scores)
            max_s = max(raw_scores)
            for r in results:
                norm = r.normalized_score(min_s, max_s)
                scores[r.doc_id] = scores.get(r.doc_id, 0.0) + norm * w
        return scores

    @staticmethod
    def _borda(result_lists: dict[str, list[SearchResult]]) -> dict[str, float]:
        """Borda count: score = sum(n_results - rank) across lists."""
        scores: dict[str, float] = {}
        for results in result_lists.values():
            n = len(results)
            for r in results:
                rank = r.rank if r.rank >= 1 else (results.index(r) + 1)
                # Borda: full list of n items → ranks 1..n → points n-rank
                scores[r.doc_id] = scores.get(r.doc_id, 0.0) + float(n - rank)
        return scores

    @staticmethod
    def _max_score(result_lists: dict[str, list[SearchResult]]) -> dict[str, float]:
        """Take the maximum normalized score across all sources."""
        # Collect per-source normalized scores for each doc.
        doc_norm: dict[str, float] = {}
        for results in result_lists.values():
            if not results:
                continue
            raw_scores = [r.score for r in results]
            min_s = min(raw_scores)
            max_s = max(raw_scores)
            for r in results:
                norm = r.normalized_score(min_s, max_s)
                if r.doc_id not in doc_norm or norm > doc_norm[r.doc_id]:
                    doc_norm[r.doc_id] = norm
        return doc_norm
