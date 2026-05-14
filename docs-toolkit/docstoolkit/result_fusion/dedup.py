"""Result-level deduplication for the result fusion module (E17).

This is distinct from the request deduplication in E13 (docstoolkit.dedup):
it operates on :class:`~docstoolkit.result_fusion.result.SearchResult` objects
after fusion, removing or merging results that refer to the same document.
"""
from __future__ import annotations

from docstoolkit.result_fusion.result import SearchResult


class ResultDeduplicator:
    """Remove or merge duplicate :class:`SearchResult` objects in a result list.

    Two deduplication modes are supported:

    * **Exact** (``similarity_threshold=1.0``): keeps only the highest-scoring
      result for each ``doc_id``.
    * **Prefix** (``similarity_threshold < 1.0``): additionally collapses
      results whose ``doc_id`` prefixes of length
      ``floor(threshold * len(doc_id))`` collide, keeping the highest score.

    Usage::

        dedup = ResultDeduplicator()
        unique = dedup.deduplicate(results)
        merged = dedup.merge_sources(results)
    """

    def deduplicate(
        self,
        results: list[SearchResult],
        similarity_threshold: float = 1.0,
    ) -> list[SearchResult]:
        """Remove duplicates from *results*.

        Parameters
        ----------
        results:              Input result list (order preserved for survivors).
        similarity_threshold: 1.0 → exact ``doc_id`` dedup (keep highest score).
                              < 1.0 → also remove results whose ``doc_id``
                              prefix of length
                              ``int(threshold * len(doc_id))`` matches an
                              already-seen prefix.

        Returns
        -------
        Deduplicated list in the same relative order, with the highest-scoring
        representative retained for each group.
        """
        if similarity_threshold == 1.0:
            return self._exact_dedup(results)
        return self._prefix_dedup(results, similarity_threshold)

    def merge_sources(self, results: list[SearchResult]) -> list[SearchResult]:
        """Combine results with the same ``doc_id`` from multiple sources.

        For each group of results sharing a ``doc_id``:

        * The result with the **highest score** is kept as the base.
        * All contributing source names are collected into
          ``metadata["sources"]`` (a sorted list of unique source names).
        * The ``source`` field on the merged result is set to the source of
          the highest-scoring original.

        The output list preserves the relative order of first occurrences.

        Parameters
        ----------
        results: Input result list, possibly containing duplicate ``doc_id``
                 values from different retrieval sources.

        Returns
        -------
        Deduplicated list where each ``doc_id`` appears exactly once.
        """
        # Group by doc_id, preserving insertion order.
        groups: dict[str, list[SearchResult]] = {}
        for r in results:
            groups.setdefault(r.doc_id, []).append(r)

        merged: list[SearchResult] = []
        for doc_id, group in groups.items():
            best = max(group, key=lambda r: r.score)
            all_sources = sorted({r.source for r in group})
            meta = dict(best.metadata)
            meta["sources"] = all_sources
            merged.append(
                SearchResult(
                    doc_id=doc_id,
                    score=best.score,
                    source=best.source,
                    rank=best.rank,
                    metadata=meta,
                )
            )
        return merged

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _exact_dedup(results: list[SearchResult]) -> list[SearchResult]:
        """Keep the highest-scoring result per doc_id."""
        best: dict[str, SearchResult] = {}
        for r in results:
            if r.doc_id not in best or r.score > best[r.doc_id].score:
                best[r.doc_id] = r
        # Preserve original relative order (first occurrence wins for ordering).
        seen: set[str] = set()
        out: list[SearchResult] = []
        for r in results:
            if r.doc_id not in seen:
                seen.add(r.doc_id)
                out.append(best[r.doc_id])
        return out

    @staticmethod
    def _prefix_dedup(
        results: list[SearchResult],
        threshold: float,
    ) -> list[SearchResult]:
        """Keep the highest-scoring result per doc_id prefix group."""
        # Build best-score map per doc_id first (exact level).
        best: dict[str, SearchResult] = {}
        for r in results:
            if r.doc_id not in best or r.score > best[r.doc_id].score:
                best[r.doc_id] = r

        seen_prefixes: set[str] = set()
        seen_doc_ids: set[str] = set()
        out: list[SearchResult] = []

        for r in results:
            if r.doc_id in seen_doc_ids:
                continue
            prefix_len = int(threshold * len(r.doc_id))
            prefix = r.doc_id[:prefix_len] if prefix_len > 0 else r.doc_id
            if prefix in seen_prefixes:
                # This doc_id's prefix is already represented; skip unless
                # this result scores higher than the one already added.
                seen_doc_ids.add(r.doc_id)
                continue
            seen_prefixes.add(prefix)
            seen_doc_ids.add(r.doc_id)
            out.append(best[r.doc_id])

        return out
