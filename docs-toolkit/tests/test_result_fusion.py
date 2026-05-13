"""Tests for docstoolkit.result_fusion — E17 Result Fusion module."""
from __future__ import annotations

import pytest

from docstoolkit.result_fusion import (
    SearchResult,
    FusionMethod,
    FusionConfig,
    FusionResult,
    ResultFusion,
    ResultDeduplicator,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sr(doc_id: str, score: float, source: str = "s1", rank: int = 0) -> SearchResult:
    return SearchResult(doc_id=doc_id, score=score, source=source, rank=rank)


def _ranked(*doc_ids: str, source: str = "s1", base_score: float = 1.0) -> list[SearchResult]:
    """Return a ranked list where rank i has score base_score - i*0.1."""
    return [
        SearchResult(
            doc_id=d,
            score=round(base_score - i * 0.1, 6),
            source=source,
            rank=i + 1,
        )
        for i, d in enumerate(doc_ids)
    ]


# ---------------------------------------------------------------------------
# SearchResult
# ---------------------------------------------------------------------------

class TestSearchResultFields:
    def test_required_fields(self):
        r = SearchResult(doc_id="x", score=0.9, source="bm25")
        assert r.doc_id == "x"
        assert r.score == 0.9
        assert r.source == "bm25"

    def test_default_rank_zero(self):
        r = SearchResult(doc_id="x", score=0.5, source="bm25")
        assert r.rank == 0

    def test_default_metadata_empty(self):
        r = SearchResult(doc_id="x", score=0.5, source="bm25")
        assert r.metadata == {}

    def test_metadata_not_shared_between_instances(self):
        r1 = SearchResult(doc_id="x", score=0.5, source="bm25")
        r2 = SearchResult(doc_id="y", score=0.3, source="bm25")
        r1.metadata["key"] = "val"
        assert "key" not in r2.metadata

    def test_custom_rank(self):
        r = SearchResult(doc_id="x", score=0.5, source="bm25", rank=3)
        assert r.rank == 3

    def test_custom_metadata(self):
        r = SearchResult(doc_id="x", score=0.5, source="bm25", metadata={"title": "Doc X"})
        assert r.metadata["title"] == "Doc X"


class TestNormalizedScore:
    def test_min_equals_max_returns_half(self):
        r = _sr("x", 0.7)
        assert r.normalized_score(0.7, 0.7) == pytest.approx(0.5)

    def test_score_at_min_returns_zero(self):
        r = _sr("x", 0.0)
        assert r.normalized_score(0.0, 1.0) == pytest.approx(0.0)

    def test_score_at_max_returns_one(self):
        r = _sr("x", 1.0)
        assert r.normalized_score(0.0, 1.0) == pytest.approx(1.0)

    def test_midpoint(self):
        r = _sr("x", 0.5)
        assert r.normalized_score(0.0, 1.0) == pytest.approx(0.5)

    def test_arbitrary_range(self):
        r = _sr("x", 3.0)
        assert r.normalized_score(1.0, 5.0) == pytest.approx(0.5)

    def test_returns_float(self):
        r = _sr("x", 0.5)
        assert isinstance(r.normalized_score(0.0, 1.0), float)

    def test_negative_scores(self):
        r = _sr("x", -1.0)
        result = r.normalized_score(-3.0, 1.0)
        assert result == pytest.approx(0.5)


# ---------------------------------------------------------------------------
# FusionMethod enum
# ---------------------------------------------------------------------------

class TestFusionMethodEnum:
    def test_rrf_value(self):
        assert FusionMethod.RRF.value == "rrf"

    def test_weighted_sum_value(self):
        assert FusionMethod.WEIGHTED_SUM.value == "weighted_sum"

    def test_borda_value(self):
        assert FusionMethod.BORDA.value == "borda"

    def test_max_score_value(self):
        assert FusionMethod.MAX_SCORE.value == "max_score"

    def test_four_methods(self):
        assert len(FusionMethod) == 4


# ---------------------------------------------------------------------------
# FusionConfig
# ---------------------------------------------------------------------------

class TestFusionConfig:
    def test_defaults(self):
        cfg = FusionConfig()
        assert cfg.method == FusionMethod.RRF
        assert cfg.rrf_k == 60
        assert cfg.weights == {}

    def test_custom_method(self):
        cfg = FusionConfig(method=FusionMethod.BORDA)
        assert cfg.method == FusionMethod.BORDA

    def test_custom_rrf_k(self):
        cfg = FusionConfig(rrf_k=10)
        assert cfg.rrf_k == 10

    def test_custom_weights(self):
        cfg = FusionConfig(weights={"bm25": 2.0, "dense": 1.0})
        assert cfg.weights["bm25"] == pytest.approx(2.0)

    def test_weights_not_shared(self):
        cfg1 = FusionConfig()
        cfg2 = FusionConfig()
        cfg1.weights["x"] = 5.0
        assert "x" not in cfg2.weights


# ---------------------------------------------------------------------------
# FusionResult helpers
# ---------------------------------------------------------------------------

class TestFusionResultTop:
    def _make(self) -> FusionResult:
        results = [_sr(f"d{i}", float(10 - i), "s1", rank=i + 1) for i in range(5)]
        return FusionResult(results=results, method=FusionMethod.RRF, source_counts={"s1": 5})

    def test_top_returns_first_n(self):
        fr = self._make()
        assert len(fr.top(3)) == 3

    def test_top_preserves_order(self):
        fr = self._make()
        top3 = fr.top(3)
        assert [r.doc_id for r in top3] == ["d0", "d1", "d2"]

    def test_top_zero(self):
        fr = self._make()
        assert fr.top(0) == []

    def test_top_larger_than_list(self):
        fr = self._make()
        assert len(fr.top(100)) == 5


class TestFusionResultByDocId:
    def _make(self) -> FusionResult:
        results = [_sr(f"d{i}", float(i), "s1") for i in range(4)]
        return FusionResult(results=results, method=FusionMethod.RRF, source_counts={"s1": 4})

    def test_found_existing(self):
        fr = self._make()
        r = fr.by_doc_id("d2")
        assert r is not None
        assert r.doc_id == "d2"

    def test_not_found_returns_none(self):
        fr = self._make()
        assert fr.by_doc_id("missing") is None

    def test_returns_correct_score(self):
        fr = self._make()
        r = fr.by_doc_id("d3")
        assert r.score == pytest.approx(3.0)


# ---------------------------------------------------------------------------
# ResultFusion — RRF
# ---------------------------------------------------------------------------

class TestRRFFusion:
    def test_single_source_score_formula(self):
        k = 60
        lists = {"s1": _ranked("a", "b", "c")}
        fused = ResultFusion().fuse(lists, FusionConfig(method=FusionMethod.RRF, rrf_k=k))
        score_map = {r.doc_id: r.score for r in fused.results}
        assert score_map["a"] == pytest.approx(1.0 / (k + 1))
        assert score_map["b"] == pytest.approx(1.0 / (k + 2))
        assert score_map["c"] == pytest.approx(1.0 / (k + 3))

    def test_overlapping_results_scores_summed(self):
        k = 60
        lists = {
            "s1": _ranked("a", "b"),
            "s2": _ranked("a", "c"),
        }
        fused = ResultFusion().fuse(lists, FusionConfig(method=FusionMethod.RRF, rrf_k=k))
        score_a = fused.by_doc_id("a").score
        expected = 1.0 / (k + 1) + 1.0 / (k + 1)
        assert score_a == pytest.approx(expected)

    def test_doc_appearing_in_multiple_lists_ranks_higher(self):
        lists = {
            "s1": _ranked("a", "b", "c"),
            "s2": _ranked("b", "d"),
        }
        fused = ResultFusion().fuse(lists, FusionConfig(method=FusionMethod.RRF))
        # "b" appears in both lists at rank 2 and 1, should outscore "a" (rank 1 only) or "d"
        rank_map = {r.doc_id: r.rank for r in fused.results}
        assert rank_map["b"] < rank_map["a"] or rank_map["b"] < rank_map["d"]

    def test_results_sorted_descending(self):
        lists = {
            "s1": _ranked("a", "b", "c"),
            "s2": _ranked("c", "b"),
        }
        fused = ResultFusion().fuse(lists, FusionConfig(method=FusionMethod.RRF))
        scores = [r.score for r in fused.results]
        assert scores == sorted(scores, reverse=True)

    def test_all_unique_docs_present(self):
        lists = {
            "s1": _ranked("a", "b"),
            "s2": _ranked("c", "d"),
        }
        fused = ResultFusion().fuse(lists, FusionConfig(method=FusionMethod.RRF))
        doc_ids = {r.doc_id for r in fused.results}
        assert doc_ids == {"a", "b", "c", "d"}

    def test_ranks_reassigned_from_one(self):
        lists = {"s1": _ranked("a", "b", "c")}
        fused = ResultFusion().fuse(lists, FusionConfig(method=FusionMethod.RRF))
        ranks = [r.rank for r in fused.results]
        assert ranks == list(range(1, len(ranks) + 1))

    def test_default_config_uses_rrf(self):
        lists = {"s1": _ranked("a", "b")}
        fused = ResultFusion().fuse(lists)
        assert fused.method == FusionMethod.RRF

    def test_custom_k(self):
        k = 10
        lists = {"s1": _ranked("x")}
        fused = ResultFusion().fuse(lists, FusionConfig(method=FusionMethod.RRF, rrf_k=k))
        assert fused.results[0].score == pytest.approx(1.0 / (k + 1))

    def test_source_counts_populated(self):
        lists = {
            "bm25": _ranked("a", "b", "c"),
            "dense": _ranked("a", "d"),
        }
        fused = ResultFusion().fuse(lists, FusionConfig(method=FusionMethod.RRF))
        assert fused.source_counts["bm25"] == 3
        assert fused.source_counts["dense"] == 2

    def test_empty_input(self):
        fused = ResultFusion().fuse({})
        assert fused.results == []

    def test_empty_list_in_source(self):
        lists = {"s1": _ranked("a", "b"), "s2": []}
        fused = ResultFusion().fuse(lists, FusionConfig(method=FusionMethod.RRF))
        doc_ids = {r.doc_id for r in fused.results}
        assert doc_ids == {"a", "b"}


# ---------------------------------------------------------------------------
# ResultFusion — WEIGHTED_SUM
# ---------------------------------------------------------------------------

class TestWeightedSumFusion:
    def test_default_weight_one(self):
        lists = {"s1": _ranked("a", "b", "c")}
        cfg = FusionConfig(method=FusionMethod.WEIGHTED_SUM)
        fused = ResultFusion().fuse(lists, cfg)
        assert len(fused.results) == 3

    def test_higher_weight_source_dominates(self):
        # s1 gets weight 3, s2 gets weight 1; doc "x" only in s1 → should rank high
        lists = {
            "s1": [SearchResult(doc_id="x", score=1.0, source="s1", rank=1)],
            "s2": [SearchResult(doc_id="y", score=1.0, source="s2", rank=1)],
        }
        cfg = FusionConfig(method=FusionMethod.WEIGHTED_SUM, weights={"s1": 3.0, "s2": 1.0})
        fused = ResultFusion().fuse(lists, cfg)
        # "x" should have score 3 * 0.5 = 1.5, "y" score 1 * 0.5 = 0.5
        assert fused.results[0].doc_id == "x"

    def test_normalized_per_source_not_global(self):
        # Even if scores differ by scale across sources, normalization is per source
        lists = {
            "s1": [
                SearchResult(doc_id="a", score=100.0, source="s1", rank=1),
                SearchResult(doc_id="b", score=50.0, source="s1", rank=2),
            ],
            "s2": [
                SearchResult(doc_id="a", score=1.0, source="s2", rank=1),
                SearchResult(doc_id="c", score=0.5, source="s2", rank=2),
            ],
        }
        cfg = FusionConfig(method=FusionMethod.WEIGHTED_SUM)
        fused = ResultFusion().fuse(lists, cfg)
        # "a" gets 1.0 + 1.0 = 2.0 (top normalized in both); "b" gets 0.0 (bottom of s1)
        score_a = fused.by_doc_id("a").score
        score_b = fused.by_doc_id("b").score
        assert score_a > score_b

    def test_results_sorted_descending(self):
        lists = {
            "s1": _ranked("a", "b", "c"),
            "s2": _ranked("b", "a"),
        }
        cfg = FusionConfig(method=FusionMethod.WEIGHTED_SUM)
        fused = ResultFusion().fuse(lists, cfg)
        scores = [r.score for r in fused.results]
        assert scores == sorted(scores, reverse=True)

    def test_method_recorded(self):
        lists = {"s1": _ranked("a")}
        cfg = FusionConfig(method=FusionMethod.WEIGHTED_SUM)
        fused = ResultFusion().fuse(lists, cfg)
        assert fused.method == FusionMethod.WEIGHTED_SUM


# ---------------------------------------------------------------------------
# ResultFusion — BORDA
# ---------------------------------------------------------------------------

class TestBordaFusion:
    def test_single_list_scores(self):
        lists = {"s1": _ranked("a", "b", "c")}
        cfg = FusionConfig(method=FusionMethod.BORDA)
        fused = ResultFusion().fuse(lists, cfg)
        score_map = {r.doc_id: r.score for r in fused.results}
        # n=3: rank1→2, rank2→1, rank3→0
        assert score_map["a"] == pytest.approx(2.0)
        assert score_map["b"] == pytest.approx(1.0)
        assert score_map["c"] == pytest.approx(0.0)

    def test_two_lists_scores_summed(self):
        lists = {
            "s1": _ranked("a", "b"),   # a→1, b→0
            "s2": _ranked("b", "a"),   # b→1, a→0
        }
        cfg = FusionConfig(method=FusionMethod.BORDA)
        fused = ResultFusion().fuse(lists, cfg)
        score_map = {r.doc_id: r.score for r in fused.results}
        assert score_map["a"] == pytest.approx(1.0)
        assert score_map["b"] == pytest.approx(1.0)

    def test_results_sorted_descending(self):
        lists = {
            "s1": _ranked("a", "b", "c", "d"),
            "s2": _ranked("d", "c", "b", "a"),
        }
        cfg = FusionConfig(method=FusionMethod.BORDA)
        fused = ResultFusion().fuse(lists, cfg)
        scores = [r.score for r in fused.results]
        assert scores == sorted(scores, reverse=True)

    def test_method_recorded(self):
        lists = {"s1": _ranked("a")}
        cfg = FusionConfig(method=FusionMethod.BORDA)
        fused = ResultFusion().fuse(lists, cfg)
        assert fused.method == FusionMethod.BORDA

    def test_ranks_from_one(self):
        lists = {"s1": _ranked("a", "b", "c")}
        cfg = FusionConfig(method=FusionMethod.BORDA)
        fused = ResultFusion().fuse(lists, cfg)
        ranks = sorted(r.rank for r in fused.results)
        assert ranks == [1, 2, 3]


# ---------------------------------------------------------------------------
# ResultFusion — MAX_SCORE
# ---------------------------------------------------------------------------

class TestMaxScoreFusion:
    def test_takes_max_across_sources(self):
        lists = {
            "s1": [SearchResult(doc_id="a", score=0.9, source="s1", rank=1),
                   SearchResult(doc_id="b", score=0.1, source="s1", rank=2)],
            "s2": [SearchResult(doc_id="a", score=0.2, source="s2", rank=1),
                   SearchResult(doc_id="b", score=0.8, source="s2", rank=2)],
        }
        cfg = FusionConfig(method=FusionMethod.MAX_SCORE)
        fused = ResultFusion().fuse(lists, cfg)
        # Both "a" and "b" should get normalized score 1.0 (each is top in its source)
        score_a = fused.by_doc_id("a").score
        score_b = fused.by_doc_id("b").score
        assert score_a == pytest.approx(1.0)
        assert score_b == pytest.approx(1.0)

    def test_single_source_max_normalized(self):
        lists = {
            "s1": [
                SearchResult(doc_id="a", score=1.0, source="s1", rank=1),
                SearchResult(doc_id="b", score=0.0, source="s1", rank=2),
            ]
        }
        cfg = FusionConfig(method=FusionMethod.MAX_SCORE)
        fused = ResultFusion().fuse(lists, cfg)
        assert fused.by_doc_id("a").score == pytest.approx(1.0)
        assert fused.by_doc_id("b").score == pytest.approx(0.0)

    def test_results_sorted_descending(self):
        lists = {
            "s1": _ranked("a", "b", "c"),
            "s2": _ranked("c", "b"),
        }
        cfg = FusionConfig(method=FusionMethod.MAX_SCORE)
        fused = ResultFusion().fuse(lists, cfg)
        scores = [r.score for r in fused.results]
        assert scores == sorted(scores, reverse=True)

    def test_method_recorded(self):
        lists = {"s1": _ranked("a")}
        cfg = FusionConfig(method=FusionMethod.MAX_SCORE)
        fused = ResultFusion().fuse(lists, cfg)
        assert fused.method == FusionMethod.MAX_SCORE


# ---------------------------------------------------------------------------
# ResultDeduplicator — exact dedup
# ---------------------------------------------------------------------------

class TestResultDeduplicatorExact:
    def test_no_duplicates_unchanged(self):
        results = [_sr("a", 0.9), _sr("b", 0.8), _sr("c", 0.7)]
        dedup = ResultDeduplicator()
        out = dedup.deduplicate(results)
        assert [r.doc_id for r in out] == ["a", "b", "c"]

    def test_keeps_highest_score_duplicate(self):
        results = [_sr("a", 0.5), _sr("a", 0.9), _sr("b", 0.7)]
        dedup = ResultDeduplicator()
        out = dedup.deduplicate(results)
        ids = [r.doc_id for r in out]
        assert ids.count("a") == 1
        a_result = next(r for r in out if r.doc_id == "a")
        assert a_result.score == pytest.approx(0.9)

    def test_preserves_relative_order(self):
        results = [_sr("b", 0.8), _sr("a", 0.9), _sr("c", 0.7), _sr("b", 0.3)]
        dedup = ResultDeduplicator()
        out = dedup.deduplicate(results)
        assert [r.doc_id for r in out] == ["b", "a", "c"]

    def test_empty_input(self):
        dedup = ResultDeduplicator()
        assert dedup.deduplicate([]) == []

    def test_single_element(self):
        dedup = ResultDeduplicator()
        r = _sr("x", 1.0)
        out = dedup.deduplicate([r])
        assert len(out) == 1
        assert out[0].doc_id == "x"

    def test_all_same_doc_id(self):
        results = [_sr("a", float(i)) for i in range(5)]
        dedup = ResultDeduplicator()
        out = dedup.deduplicate(results)
        assert len(out) == 1
        assert out[0].score == pytest.approx(4.0)


# ---------------------------------------------------------------------------
# ResultDeduplicator — prefix dedup
# ---------------------------------------------------------------------------

class TestResultDeduplicatorPrefix:
    def test_prefix_collapses_similar_ids(self):
        # With threshold=0.5, "doc_a" and "doc_b" share prefix "doc" (len=3 of 5)
        results = [
            SearchResult(doc_id="doc_a", score=0.9, source="s1", rank=1),
            SearchResult(doc_id="doc_b", score=0.8, source="s1", rank=2),
            SearchResult(doc_id="xyz_c", score=0.7, source="s1", rank=3),
        ]
        dedup = ResultDeduplicator()
        out = dedup.deduplicate(results, similarity_threshold=0.5)
        # "doc_a" and "doc_b" have same 3-char prefix "doc"; only first survives
        doc_ids = [r.doc_id for r in out]
        assert "doc_a" in doc_ids
        assert "doc_b" not in doc_ids
        assert "xyz_c" in doc_ids

    def test_exact_threshold_does_not_use_prefix(self):
        results = [
            SearchResult(doc_id="doc_a", score=0.9, source="s1", rank=1),
            SearchResult(doc_id="doc_b", score=0.8, source="s1", rank=2),
        ]
        dedup = ResultDeduplicator()
        out = dedup.deduplicate(results, similarity_threshold=1.0)
        # With exact dedup both should survive (different doc_ids)
        assert len(out) == 2


# ---------------------------------------------------------------------------
# ResultDeduplicator — merge_sources
# ---------------------------------------------------------------------------

class TestMergeSources:
    def test_single_source_unchanged_structure(self):
        results = [_sr("a", 0.9, "bm25"), _sr("b", 0.8, "bm25")]
        dedup = ResultDeduplicator()
        out = dedup.merge_sources(results)
        assert len(out) == 2

    def test_merges_same_doc_different_sources(self):
        results = [
            SearchResult(doc_id="a", score=0.9, source="bm25", rank=1),
            SearchResult(doc_id="a", score=0.7, source="dense", rank=2),
        ]
        dedup = ResultDeduplicator()
        out = dedup.merge_sources(results)
        assert len(out) == 1
        assert out[0].doc_id == "a"

    def test_keeps_highest_score(self):
        results = [
            SearchResult(doc_id="a", score=0.7, source="bm25", rank=1),
            SearchResult(doc_id="a", score=0.9, source="dense", rank=1),
        ]
        dedup = ResultDeduplicator()
        out = dedup.merge_sources(results)
        assert out[0].score == pytest.approx(0.9)

    def test_sources_in_metadata(self):
        results = [
            SearchResult(doc_id="a", score=0.7, source="bm25", rank=1),
            SearchResult(doc_id="a", score=0.9, source="dense", rank=1),
            SearchResult(doc_id="a", score=0.5, source="graph", rank=1),
        ]
        dedup = ResultDeduplicator()
        out = dedup.merge_sources(results)
        assert "sources" in out[0].metadata
        assert set(out[0].metadata["sources"]) == {"bm25", "dense", "graph"}

    def test_sources_sorted(self):
        results = [
            SearchResult(doc_id="a", score=0.5, source="z_source", rank=1),
            SearchResult(doc_id="a", score=0.9, source="a_source", rank=1),
        ]
        dedup = ResultDeduplicator()
        out = dedup.merge_sources(results)
        assert out[0].metadata["sources"] == sorted(out[0].metadata["sources"])

    def test_single_source_metadata_still_has_sources(self):
        results = [SearchResult(doc_id="a", score=0.9, source="bm25", rank=1)]
        dedup = ResultDeduplicator()
        out = dedup.merge_sources(results)
        assert out[0].metadata["sources"] == ["bm25"]

    def test_preserves_order_of_first_occurrence(self):
        results = [
            SearchResult(doc_id="b", score=0.8, source="s1", rank=1),
            SearchResult(doc_id="a", score=0.9, source="s1", rank=2),
            SearchResult(doc_id="b", score=0.6, source="s2", rank=1),
        ]
        dedup = ResultDeduplicator()
        out = dedup.merge_sources(results)
        assert [r.doc_id for r in out] == ["b", "a"]

    def test_empty_input(self):
        dedup = ResultDeduplicator()
        assert dedup.merge_sources([]) == []

    def test_source_field_from_best(self):
        results = [
            SearchResult(doc_id="a", score=0.4, source="bm25", rank=1),
            SearchResult(doc_id="a", score=0.9, source="dense", rank=1),
        ]
        dedup = ResultDeduplicator()
        out = dedup.merge_sources(results)
        assert out[0].source == "dense"


# ---------------------------------------------------------------------------
# Integration — fuse then dedup
# ---------------------------------------------------------------------------

class TestIntegrationFuseThenDedup:
    def test_fuse_rrf_then_merge(self):
        lists = {
            "bm25": _ranked("a", "b", "c"),
            "dense": _ranked("b", "a", "d"),
        }
        fused = ResultFusion().fuse(lists, FusionConfig(method=FusionMethod.RRF))
        # fused results already have unique doc_ids; merge_sources should be no-op count-wise
        dedup = ResultDeduplicator()
        merged = dedup.merge_sources(fused.results)
        assert len(merged) == len(fused.results)

    def test_fuse_deduplicate_pipeline(self):
        raw = [
            SearchResult(doc_id="a", score=0.9, source="bm25", rank=1),
            SearchResult(doc_id="a", score=0.7, source="dense", rank=1),
            SearchResult(doc_id="b", score=0.8, source="bm25", rank=2),
        ]
        dedup = ResultDeduplicator()
        merged = dedup.merge_sources(raw)
        assert len(merged) == 2
        a = next(r for r in merged if r.doc_id == "a")
        assert a.score == pytest.approx(0.9)
        assert "bm25" in a.metadata["sources"]
        assert "dense" in a.metadata["sources"]
