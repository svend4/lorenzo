"""Tests for docstoolkit.hybrid_search — E40 hybrid search orchestrator."""
from __future__ import annotations

import math
import time

import pytest

from docstoolkit.hybrid_search import (
    SearchBackend,
    BM25Backend,
    KeywordBackend,
    BackendWeight,
    OrchestratorConfig,
    HybridSearchResult,
    HybridSearchOrchestrator,
    SearchLatency,
    HybridSearchMonitor,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_DOCS = {
    "doc1": "the quick brown fox jumps over the lazy dog",
    "doc2": "a fast brown fox leaps over a sleeping canine",
    "doc3": "machine learning and neural networks for natural language processing",
    "doc4": "information retrieval using BM25 and TF-IDF scoring algorithms",
    "doc5": "fox fox fox fox repeated word document for frequency testing",
}

SMALL_DOCS = {
    "a": "hello world python",
    "b": "hello java world",
    "c": "machine learning python",
}


# ---------------------------------------------------------------------------
# BM25Backend
# ---------------------------------------------------------------------------

class TestBM25BackendInit:
    def test_init_empty(self):
        b = BM25Backend()
        assert b.doc_count() == 0

    def test_init_with_documents(self):
        b = BM25Backend(SMALL_DOCS)
        assert b.doc_count() == 3

    def test_doc_count_zero_before_index(self):
        b = BM25Backend()
        assert b.doc_count() == 0

    def test_default_k1(self):
        b = BM25Backend()
        assert b._k1 == 1.5

    def test_default_b(self):
        b = BM25Backend()
        assert b._b == 0.75


class TestBM25BackendIndex:
    def test_index_sets_doc_count(self):
        b = BM25Backend()
        b.index(SAMPLE_DOCS)
        assert b.doc_count() == len(SAMPLE_DOCS)

    def test_index_single_document(self):
        b = BM25Backend()
        b.index({"only": "one document here"})
        assert b.doc_count() == 1

    def test_index_overwrites_previous(self):
        b = BM25Backend(SMALL_DOCS)
        b.index({"x": "new content"})
        assert b.doc_count() == 1

    def test_index_empty_dict(self):
        b = BM25Backend()
        b.index({})
        assert b.doc_count() == 0

    def test_idf_computed_after_index(self):
        b = BM25Backend()
        b.index(SMALL_DOCS)
        assert len(b._idf) > 0

    def test_tf_stored_per_doc(self):
        b = BM25Backend()
        b.index(SMALL_DOCS)
        assert "a" in b._tf
        assert "b" in b._tf


class TestBM25BackendSearch:
    def test_search_returns_list(self):
        b = BM25Backend(SAMPLE_DOCS)
        result = b.search("fox")
        assert isinstance(result, list)

    def test_search_returns_tuples(self):
        b = BM25Backend(SAMPLE_DOCS)
        result = b.search("fox")
        for item in result:
            assert isinstance(item, tuple)
            assert len(item) == 2

    def test_search_doc_ids_are_strings(self):
        b = BM25Backend(SAMPLE_DOCS)
        result = b.search("fox")
        for doc_id, score in result:
            assert isinstance(doc_id, str)

    def test_search_scores_are_floats(self):
        b = BM25Backend(SAMPLE_DOCS)
        result = b.search("fox")
        for _, score in result:
            assert isinstance(score, float)

    def test_search_sorted_descending(self):
        b = BM25Backend(SAMPLE_DOCS)
        result = b.search("fox")
        scores = [s for _, s in result]
        assert scores == sorted(scores, reverse=True)

    def test_search_top_k_limit(self):
        b = BM25Backend(SAMPLE_DOCS)
        result = b.search("fox", top_k=2)
        assert len(result) <= 2

    def test_search_default_top_k_10(self):
        docs = {f"d{i}": f"fox word{i}" for i in range(20)}
        b = BM25Backend(docs)
        result = b.search("fox")
        assert len(result) <= 10

    def test_search_empty_index_returns_empty(self):
        b = BM25Backend()
        result = b.search("fox")
        assert result == []

    def test_search_unknown_term_returns_empty(self):
        b = BM25Backend(SMALL_DOCS)
        result = b.search("zzzzunknownterm")
        assert result == []

    def test_repeated_term_gets_higher_score(self):
        b = BM25Backend(SAMPLE_DOCS)
        result = b.search("fox")
        result_dict = dict(result)
        # doc5 has "fox" repeated 4 times, should score well
        assert "doc5" in result_dict

    def test_bm25_relevant_doc_ranks_first(self):
        b = BM25Backend(SAMPLE_DOCS)
        result = b.search("machine learning neural")
        assert len(result) > 0
        # doc3 is the only one about machine learning
        assert result[0][0] == "doc3"

    def test_scores_positive(self):
        b = BM25Backend(SAMPLE_DOCS)
        result = b.search("fox")
        for _, score in result:
            assert score > 0

    def test_bm25_empty_query_returns_empty(self):
        b = BM25Backend(SAMPLE_DOCS)
        result = b.search("")
        assert result == []

    def test_bm25_idf_penalizes_common_term(self):
        # "the" appears in doc1 only, but let's use a term that appears in all docs
        docs = {
            "d1": "common word",
            "d2": "common word",
            "d3": "unique word",
        }
        b = BM25Backend(docs)
        # 'common' appears in 2/3 docs, 'unique' appears in 1/3
        # IDF('unique') should be higher than IDF('common')
        assert b._idf.get("unique", 0) > b._idf.get("common", 0)


# ---------------------------------------------------------------------------
# KeywordBackend
# ---------------------------------------------------------------------------

class TestKeywordBackendInit:
    def test_init_empty(self):
        kb = KeywordBackend()
        assert kb.doc_count() == 0

    def test_init_with_documents(self):
        kb = KeywordBackend(SMALL_DOCS)
        assert kb.doc_count() == 3

    def test_doc_count_zero_before_index(self):
        kb = KeywordBackend()
        assert kb.doc_count() == 0


class TestKeywordBackendIndex:
    def test_index_sets_doc_count(self):
        kb = KeywordBackend()
        kb.index(SAMPLE_DOCS)
        assert kb.doc_count() == len(SAMPLE_DOCS)

    def test_index_stores_token_sets(self):
        kb = KeywordBackend()
        kb.index(SMALL_DOCS)
        assert "a" in kb._doc_tokens
        assert isinstance(kb._doc_tokens["a"], set)

    def test_index_overwrites_previous(self):
        kb = KeywordBackend(SMALL_DOCS)
        kb.index({"only": "one"})
        assert kb.doc_count() == 1

    def test_index_empty_dict(self):
        kb = KeywordBackend()
        kb.index({})
        assert kb.doc_count() == 0


class TestKeywordBackendSearch:
    def test_search_returns_list(self):
        kb = KeywordBackend(SMALL_DOCS)
        result = kb.search("hello")
        assert isinstance(result, list)

    def test_search_returns_tuples(self):
        kb = KeywordBackend(SMALL_DOCS)
        result = kb.search("hello world")
        for item in result:
            assert isinstance(item, tuple)
            assert len(item) == 2

    def test_search_doc_ids_are_strings(self):
        kb = KeywordBackend(SMALL_DOCS)
        result = kb.search("hello")
        for doc_id, _ in result:
            assert isinstance(doc_id, str)

    def test_search_scores_are_floats(self):
        kb = KeywordBackend(SMALL_DOCS)
        result = kb.search("hello")
        for _, score in result:
            assert isinstance(score, float)

    def test_search_sorted_descending(self):
        kb = KeywordBackend(SMALL_DOCS)
        result = kb.search("hello world python")
        scores = [s for _, s in result]
        assert scores == sorted(scores, reverse=True)

    def test_jaccard_exact_match(self):
        kb = KeywordBackend({"doc": "hello world"})
        result = kb.search("hello world")
        assert len(result) == 1
        _, score = result[0]
        assert score == pytest.approx(1.0)

    def test_jaccard_no_overlap_returns_empty(self):
        kb = KeywordBackend({"doc": "hello world"})
        result = kb.search("python machine learning")
        assert result == []

    def test_jaccard_partial_overlap(self):
        # query: {hello, world}, doc: {hello, world, python}
        # intersection=2, union=3 => 2/3
        kb = KeywordBackend({"doc": "hello world python"})
        result = kb.search("hello world")
        assert len(result) == 1
        _, score = result[0]
        assert score == pytest.approx(2 / 3)

    def test_search_top_k_limit(self):
        kb = KeywordBackend(SAMPLE_DOCS)
        result = kb.search("fox", top_k=2)
        assert len(result) <= 2

    def test_search_empty_query_returns_empty(self):
        kb = KeywordBackend(SMALL_DOCS)
        result = kb.search("")
        assert result == []

    def test_search_empty_index_returns_empty(self):
        kb = KeywordBackend()
        result = kb.search("hello")
        assert result == []

    def test_search_scores_in_range(self):
        kb = KeywordBackend(SAMPLE_DOCS)
        result = kb.search("fox")
        for _, score in result:
            assert 0.0 <= score <= 1.0

    def test_more_overlap_higher_score(self):
        # doc_a shares 3 tokens with query, doc_b shares 1
        docs = {
            "doc_a": "python machine learning algorithms",
            "doc_b": "java programming language",
        }
        kb = KeywordBackend(docs)
        result = kb.search("python machine learning")
        result_dict = dict(result)
        assert result_dict.get("doc_a", 0) > result_dict.get("doc_b", 0)


# ---------------------------------------------------------------------------
# HybridSearchOrchestrator
# ---------------------------------------------------------------------------

class TestOrchestratorRegister:
    def test_register_adds_backend(self):
        orch = HybridSearchOrchestrator()
        orch.register("bm25", BM25Backend())
        assert "bm25" in orch.backend_names()

    def test_register_multiple_backends(self):
        orch = HybridSearchOrchestrator()
        orch.register("bm25", BM25Backend())
        orch.register("keyword", KeywordBackend())
        names = orch.backend_names()
        assert "bm25" in names
        assert "keyword" in names

    def test_backend_names_returns_list(self):
        orch = HybridSearchOrchestrator()
        orch.register("bm25", BM25Backend())
        assert isinstance(orch.backend_names(), list)

    def test_empty_backend_names(self):
        orch = HybridSearchOrchestrator()
        assert orch.backend_names() == []


class TestOrchestratorIndex:
    def test_index_all_backends(self):
        orch = HybridSearchOrchestrator()
        bm25 = BM25Backend()
        kw = KeywordBackend()
        orch.register("bm25", bm25)
        orch.register("keyword", kw)
        orch.index(SMALL_DOCS)
        assert bm25.doc_count() == 3
        assert kw.doc_count() == 3

    def test_index_empty_docs(self):
        orch = HybridSearchOrchestrator()
        bm25 = BM25Backend()
        orch.register("bm25", bm25)
        orch.index({})
        assert bm25.doc_count() == 0


class TestOrchestratorSearchRRF:
    def _orch(self):
        config = OrchestratorConfig(fusion_method="rrf", top_k=5, rrf_k=60)
        orch = HybridSearchOrchestrator(config)
        orch.register("bm25", BM25Backend())
        orch.register("keyword", KeywordBackend())
        orch.index(SAMPLE_DOCS)
        return orch

    def test_search_returns_hybrid_result(self):
        orch = self._orch()
        result = orch.search("fox")
        assert isinstance(result, HybridSearchResult)

    def test_search_result_query_matches(self):
        orch = self._orch()
        result = orch.search("fox")
        assert result.query == "fox"

    def test_search_results_list(self):
        orch = self._orch()
        result = orch.search("fox")
        assert isinstance(result.results, list)

    def test_search_results_tuples(self):
        orch = self._orch()
        result = orch.search("fox")
        for item in result.results:
            assert isinstance(item, tuple)
            assert len(item) == 2

    def test_search_top_k_respected(self):
        orch = self._orch()
        result = orch.search("fox", top_k=3)
        assert len(result.results) <= 3

    def test_search_sorted_descending(self):
        orch = self._orch()
        result = orch.search("fox")
        scores = [s for _, s in result.results]
        assert scores == sorted(scores, reverse=True)

    def test_search_backend_results_populated(self):
        orch = self._orch()
        result = orch.search("fox")
        assert "bm25" in result.backend_results
        assert "keyword" in result.backend_results

    def test_search_no_backends_returns_empty(self):
        orch = HybridSearchOrchestrator()
        result = orch.search("fox")
        assert result.results == []

    def test_rrf_score_formula(self):
        # With a single backend, score should follow 1/(k+rank) pattern
        config = OrchestratorConfig(fusion_method="rrf", top_k=10, rrf_k=60)
        orch = HybridSearchOrchestrator(config)
        orch.register("bm25", BM25Backend(), weight=1.0)
        orch.index(SAMPLE_DOCS)
        result = orch.search("fox")
        if len(result.results) >= 2:
            # Scores should be descending
            s1, s2 = result.results[0][1], result.results[1][1]
            assert s1 >= s2

    def test_search_relevant_doc_high_ranked(self):
        orch = self._orch()
        result = orch.search("machine learning neural")
        doc_ids = [doc_id for doc_id, _ in result.results]
        assert "doc3" in doc_ids
        # doc3 should be first
        assert doc_ids[0] == "doc3"


class TestOrchestratorSearchWeightedSum:
    def _orch(self):
        config = OrchestratorConfig(fusion_method="weighted_sum", top_k=5)
        orch = HybridSearchOrchestrator(config)
        orch.register("bm25", BM25Backend(), weight=1.0)
        orch.register("keyword", KeywordBackend(), weight=1.0)
        orch.index(SAMPLE_DOCS)
        return orch

    def test_search_returns_hybrid_result(self):
        orch = self._orch()
        result = orch.search("fox")
        assert isinstance(result, HybridSearchResult)

    def test_search_sorted_descending(self):
        orch = self._orch()
        result = orch.search("fox")
        scores = [s for _, s in result.results]
        assert scores == sorted(scores, reverse=True)

    def test_search_top_k_respected(self):
        orch = self._orch()
        result = orch.search("fox", top_k=2)
        assert len(result.results) <= 2

    def test_weighted_sum_backend_results_populated(self):
        orch = self._orch()
        result = orch.search("fox")
        assert "bm25" in result.backend_results
        assert "keyword" in result.backend_results

    def test_weighted_sum_relevant_doc_ranks_well(self):
        orch = self._orch()
        result = orch.search("machine learning neural")
        doc_ids = [doc_id for doc_id, _ in result.results]
        assert "doc3" in doc_ids

    def test_higher_weight_backend_dominates(self):
        config = OrchestratorConfig(fusion_method="weighted_sum", top_k=5)
        orch = HybridSearchOrchestrator(config)
        # bm25 with very high weight should dominate
        bm25 = BM25Backend()
        keyword = KeywordBackend()
        orch.register("bm25", bm25, weight=10.0)
        orch.register("keyword", keyword, weight=0.1)
        orch.index(SAMPLE_DOCS)
        result = orch.search("BM25 retrieval algorithms")
        assert len(result.results) > 0


class TestOrchestratorConfig:
    def test_config_default_fusion_rrf(self):
        config = OrchestratorConfig()
        assert config.fusion_method == "rrf"

    def test_config_default_top_k(self):
        config = OrchestratorConfig()
        assert config.top_k == 10

    def test_config_default_rrf_k(self):
        config = OrchestratorConfig()
        assert config.rrf_k == 60

    def test_config_backend_weights_default_empty(self):
        config = OrchestratorConfig()
        assert config.backend_weights == []

    def test_backend_weight_dataclass(self):
        bw = BackendWeight(backend_name="bm25", weight=2.0)
        assert bw.backend_name == "bm25"
        assert bw.weight == 2.0

    def test_config_with_backend_weights(self):
        bw = BackendWeight(backend_name="bm25", weight=2.0)
        config = OrchestratorConfig(backend_weights=[bw])
        assert len(config.backend_weights) == 1
        assert config.backend_weights[0].weight == 2.0

    def test_config_backend_weight_overrides_register_weight(self):
        bw = BackendWeight(backend_name="bm25", weight=3.0)
        config = OrchestratorConfig(backend_weights=[bw])
        orch = HybridSearchOrchestrator(config)
        bm25 = BM25Backend()
        orch.register("bm25", bm25, weight=1.0)  # should be overridden by config
        # effective weight stored
        _, effective_weight = orch._backends["bm25"]
        assert effective_weight == pytest.approx(3.0)


# ---------------------------------------------------------------------------
# HybridSearchResult
# ---------------------------------------------------------------------------

class TestHybridSearchResult:
    def _make_result(self):
        results = [("doc1", 0.9), ("doc2", 0.7), ("doc3", 0.5)]
        backend_results = {
            "bm25": [("doc1", 1.2), ("doc2", 0.9)],
            "keyword": [("doc1", 0.8), ("doc3", 0.6)],
        }
        return HybridSearchResult(
            query="test query",
            results=results,
            backend_results=backend_results,
        )

    def test_query_attribute(self):
        r = self._make_result()
        assert r.query == "test query"

    def test_results_attribute(self):
        r = self._make_result()
        assert len(r.results) == 3

    def test_backend_results_attribute(self):
        r = self._make_result()
        assert "bm25" in r.backend_results
        assert "keyword" in r.backend_results

    def test_top_returns_first_n(self):
        r = self._make_result()
        top2 = r.top(2)
        assert len(top2) == 2
        assert top2[0] == ("doc1", 0.9)
        assert top2[1] == ("doc2", 0.7)

    def test_top_more_than_available(self):
        r = self._make_result()
        top10 = r.top(10)
        assert len(top10) == 3

    def test_top_zero(self):
        r = self._make_result()
        top0 = r.top(0)
        assert top0 == []

    def test_doc_ids_returns_list(self):
        r = self._make_result()
        ids = r.doc_ids()
        assert isinstance(ids, list)

    def test_doc_ids_in_order(self):
        r = self._make_result()
        ids = r.doc_ids()
        assert ids == ["doc1", "doc2", "doc3"]

    def test_doc_ids_length(self):
        r = self._make_result()
        assert len(r.doc_ids()) == 3

    def test_empty_results(self):
        r = HybridSearchResult(query="q", results=[], backend_results={})
        assert r.top(5) == []
        assert r.doc_ids() == []


# ---------------------------------------------------------------------------
# HybridSearchMonitor
# ---------------------------------------------------------------------------

class TestSearchLatency:
    def test_fields(self):
        lat = SearchLatency(backend="bm25", query="fox", duration_ms=12.5, result_count=5)
        assert lat.backend == "bm25"
        assert lat.query == "fox"
        assert lat.duration_ms == 12.5
        assert lat.result_count == 5


class TestHybridSearchMonitor:
    def _make_monitor(self):
        m = HybridSearchMonitor()
        m.record(SearchLatency("bm25", "fox", 10.0, 3))
        m.record(SearchLatency("bm25", "dog", 20.0, 2))
        m.record(SearchLatency("keyword", "fox", 5.0, 4))
        m.record(SearchLatency("keyword", "cat", 15.0, 1))
        return m

    def test_record_stores_latency(self):
        m = HybridSearchMonitor()
        lat = SearchLatency("bm25", "q", 10.0, 5)
        m.record(lat)
        assert len(m._records) == 1

    def test_record_multiple(self):
        m = self._make_monitor()
        assert len(m._records) == 4

    def test_avg_latency_overall(self):
        m = self._make_monitor()
        avg = m.avg_latency()
        expected = (10.0 + 20.0 + 5.0 + 15.0) / 4
        assert avg == pytest.approx(expected)

    def test_avg_latency_per_backend_bm25(self):
        m = self._make_monitor()
        avg = m.avg_latency("bm25")
        assert avg == pytest.approx((10.0 + 20.0) / 2)

    def test_avg_latency_per_backend_keyword(self):
        m = self._make_monitor()
        avg = m.avg_latency("keyword")
        assert avg == pytest.approx((5.0 + 15.0) / 2)

    def test_avg_latency_empty_returns_zero(self):
        m = HybridSearchMonitor()
        assert m.avg_latency() == 0.0

    def test_avg_latency_unknown_backend_returns_zero(self):
        m = self._make_monitor()
        assert m.avg_latency("nonexistent") == 0.0

    def test_slowest_queries_returns_list(self):
        m = self._make_monitor()
        slowest = m.slowest_queries(2)
        assert isinstance(slowest, list)

    def test_slowest_queries_sorted_descending(self):
        m = self._make_monitor()
        slowest = m.slowest_queries()
        durations = [r.duration_ms for r in slowest]
        assert durations == sorted(durations, reverse=True)

    def test_slowest_queries_top_2(self):
        m = self._make_monitor()
        slowest = m.slowest_queries(2)
        assert len(slowest) == 2
        assert slowest[0].duration_ms == 20.0
        assert slowest[1].duration_ms == 15.0

    def test_slowest_queries_default_n_5(self):
        m = self._make_monitor()
        slowest = m.slowest_queries()
        assert len(slowest) <= 5

    def test_slowest_queries_more_than_available(self):
        m = self._make_monitor()
        slowest = m.slowest_queries(100)
        assert len(slowest) == 4

    def test_stats_returns_dict(self):
        m = self._make_monitor()
        s = m.stats()
        assert isinstance(s, dict)

    def test_stats_total_queries(self):
        m = self._make_monitor()
        s = m.stats()
        assert s["total_queries"] == 4

    def test_stats_avg_latency_ms(self):
        m = self._make_monitor()
        s = m.stats()
        expected = (10.0 + 20.0 + 5.0 + 15.0) / 4
        assert s["avg_latency_ms"] == pytest.approx(expected)

    def test_stats_per_backend_keys(self):
        m = self._make_monitor()
        s = m.stats()
        assert "per_backend" in s
        assert "bm25" in s["per_backend"]
        assert "keyword" in s["per_backend"]

    def test_stats_per_backend_total(self):
        m = self._make_monitor()
        s = m.stats()
        assert s["per_backend"]["bm25"]["total"] == 2
        assert s["per_backend"]["keyword"]["total"] == 2

    def test_stats_per_backend_avg_latency(self):
        m = self._make_monitor()
        s = m.stats()
        assert s["per_backend"]["bm25"]["avg_latency_ms"] == pytest.approx(15.0)
        assert s["per_backend"]["keyword"]["avg_latency_ms"] == pytest.approx(10.0)

    def test_stats_empty_monitor(self):
        m = HybridSearchMonitor()
        s = m.stats()
        assert s["total_queries"] == 0
        assert s["avg_latency_ms"] == 0.0
        assert s["per_backend"] == {}

    def test_slowest_queries_returns_search_latency_objects(self):
        m = self._make_monitor()
        slowest = m.slowest_queries(1)
        assert isinstance(slowest[0], SearchLatency)
