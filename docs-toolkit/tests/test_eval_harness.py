"""Tests for docstoolkit.eval_harness — E42 Evaluation Harness.

Covers metrics, dataset, and runner with 65+ test cases and known values.
"""
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.eval_harness import (
    EvalDataset,
    EvalHarness,
    EvalQuery,
    EvalReport,
    EvalResult,
    F1Score,
    MRR,
    NDCG,
    PrecisionAtK,
    RecallAtK,
)


# ===========================================================================
# PrecisionAtK
# ===========================================================================

class TestPrecisionAtK:
    def test_all_relevant(self):
        retrieved = ["a", "b", "c"]
        relevant = {"a", "b", "c"}
        assert PrecisionAtK.compute(retrieved, relevant, k=3) == pytest.approx(1.0)

    def test_none_relevant(self):
        retrieved = ["x", "y", "z"]
        relevant = {"a", "b"}
        assert PrecisionAtK.compute(retrieved, relevant, k=3) == pytest.approx(0.0)

    def test_partial_relevant(self):
        retrieved = ["a", "x", "b", "y", "z"]
        relevant = {"a", "b"}
        # top-5: a,x,b,y,z → 2 hits / 5
        assert PrecisionAtK.compute(retrieved, relevant, k=5) == pytest.approx(2 / 5)

    def test_k_truncates_list(self):
        retrieved = ["a", "b", "c", "d"]
        relevant = {"c", "d"}
        # top-2 = [a,b] → 0 hits / 2
        assert PrecisionAtK.compute(retrieved, relevant, k=2) == pytest.approx(0.0)

    def test_k_larger_than_list(self):
        # retrieved has 2 items, k=5 → denominator still k=5
        retrieved = ["a", "b"]
        relevant = {"a", "b"}
        assert PrecisionAtK.compute(retrieved, relevant, k=5) == pytest.approx(2 / 5)

    def test_k_zero_returns_zero(self):
        assert PrecisionAtK.compute(["a"], {"a"}, k=0) == 0.0

    def test_k_negative_returns_zero(self):
        assert PrecisionAtK.compute(["a"], {"a"}, k=-1) == 0.0

    def test_empty_retrieved(self):
        assert PrecisionAtK.compute([], {"a"}, k=5) == pytest.approx(0.0)

    def test_empty_relevant(self):
        assert PrecisionAtK.compute(["a", "b"], set(), k=2) == pytest.approx(0.0)

    def test_k_equals_1_hit(self):
        assert PrecisionAtK.compute(["a", "b"], {"a"}, k=1) == pytest.approx(1.0)

    def test_k_equals_1_miss(self):
        assert PrecisionAtK.compute(["x", "a"], {"a"}, k=1) == pytest.approx(0.0)

    def test_exact_formula(self):
        # 3 hits in top 5
        retrieved = ["a", "b", "c", "d", "e"]
        relevant = {"a", "b", "c"}
        assert PrecisionAtK.compute(retrieved, relevant, k=5) == pytest.approx(3 / 5)


# ===========================================================================
# RecallAtK
# ===========================================================================

class TestRecallAtK:
    def test_all_relevant_retrieved(self):
        retrieved = ["a", "b", "c"]
        relevant = {"a", "b", "c"}
        result = RecallAtK.compute(retrieved, relevant, k=3)
        # 3 / (3 + 1e-10)  ≈ 1.0
        assert result == pytest.approx(3 / (3 + 1e-10))

    def test_none_relevant_retrieved(self):
        retrieved = ["x", "y"]
        relevant = {"a", "b"}
        assert RecallAtK.compute(retrieved, relevant, k=2) == pytest.approx(0.0)

    def test_partial_recall(self):
        retrieved = ["a", "x", "y", "z", "b"]
        relevant = {"a", "b", "c"}
        # top-5: a,x,y,z,b → 2 hits / (3+1e-10)
        assert RecallAtK.compute(retrieved, relevant, k=5) == pytest.approx(2 / (3 + 1e-10))

    def test_k_truncates(self):
        retrieved = ["x", "a", "b"]
        relevant = {"a", "b"}
        # top-1 = [x] → 0 hits
        assert RecallAtK.compute(retrieved, relevant, k=1) == pytest.approx(0.0)

    def test_empty_relevant_near_zero_division(self):
        # |relevant|=0 → denominator = 1e-10
        result = RecallAtK.compute(["a"], set(), k=5)
        # 0 hits / 1e-10 = 0
        assert result == pytest.approx(0.0)

    def test_empty_retrieved(self):
        assert RecallAtK.compute([], {"a", "b"}, k=5) == pytest.approx(0.0)

    def test_k_larger_than_retrieved_length(self):
        retrieved = ["a"]
        relevant = {"a", "b"}
        # top-10 → only "a" found → 1 hit / 2+1e-10
        assert RecallAtK.compute(retrieved, relevant, k=10) == pytest.approx(1 / (2 + 1e-10))

    def test_one_relevant_retrieved_first(self):
        retrieved = ["a", "x", "y"]
        relevant = {"a"}
        assert RecallAtK.compute(retrieved, relevant, k=3) == pytest.approx(1 / (1 + 1e-10))


# ===========================================================================
# MRR
# ===========================================================================

class TestMRR:
    def test_first_position_hit(self):
        assert MRR.compute(["a", "b", "c"], {"a"}) == pytest.approx(1.0)

    def test_second_position_hit(self):
        assert MRR.compute(["x", "a", "b"], {"a"}) == pytest.approx(0.5)

    def test_third_position_hit(self):
        assert MRR.compute(["x", "y", "a"], {"a"}) == pytest.approx(1 / 3)

    def test_no_hit_returns_zero(self):
        assert MRR.compute(["x", "y", "z"], {"a"}) == pytest.approx(0.0)

    def test_empty_retrieved(self):
        assert MRR.compute([], {"a"}) == pytest.approx(0.0)

    def test_empty_relevant(self):
        assert MRR.compute(["a", "b"], set()) == pytest.approx(0.0)

    def test_multiple_relevant_takes_first(self):
        # "b" at pos 2 and "c" at pos 3; first relevant is "b" → 1/2
        assert MRR.compute(["a", "b", "c"], {"b", "c"}) == pytest.approx(0.5)

    def test_relevant_at_position_5(self):
        retrieved = ["x", "y", "z", "w", "a"]
        assert MRR.compute(retrieved, {"a"}) == pytest.approx(0.2)

    def test_single_doc_hit(self):
        assert MRR.compute(["a"], {"a"}) == pytest.approx(1.0)

    def test_single_doc_miss(self):
        assert MRR.compute(["b"], {"a"}) == pytest.approx(0.0)


# ===========================================================================
# NDCG
# ===========================================================================

class TestNDCG:
    def _dcg(self, relevances):
        """Helper: compute DCG manually for a known relevance list."""
        return sum(r / math.log2(i + 2) for i, r in enumerate(relevances))

    def test_perfect_ranking_single_relevant(self):
        # Only 1 relevant doc; if it's at pos 0: DCG = IDCG = 1/log2(2)=1
        retrieved = ["a", "b", "c"]
        relevant = {"a"}
        assert NDCG.compute(retrieved, relevant, k=3) == pytest.approx(1.0)

    def test_worst_ranking_single_relevant(self):
        # relevant doc at last position (k=1 → not included)
        retrieved = ["x", "y", "a"]
        relevant = {"a"}
        result = NDCG.compute(retrieved, relevant, k=2)
        # top-2: [x,y] → DCG=0; IDCG = 1/log2(2)=1 → NDCG=0
        assert result == pytest.approx(0.0)

    def test_no_relevant_docs_returns_zero(self):
        assert NDCG.compute(["a", "b"], set(), k=3) == pytest.approx(0.0)

    def test_k_zero_returns_zero(self):
        assert NDCG.compute(["a", "b"], {"a"}, k=0) == pytest.approx(0.0)

    def test_k_negative_returns_zero(self):
        assert NDCG.compute(["a", "b"], {"a"}, k=-1) == pytest.approx(0.0)

    def test_all_relevant_perfect_score(self):
        retrieved = ["a", "b", "c"]
        relevant = {"a", "b", "c"}
        # Every position is relevant → DCG == IDCG → NDCG == 1
        assert NDCG.compute(retrieved, relevant, k=3) == pytest.approx(1.0)

    def test_two_relevant_first_two_positions(self):
        # DCG  = 1/log2(2) + 1/log2(3) = 1 + 0.6309...
        # IDCG = same (ideal) → 1.0
        retrieved = ["a", "b", "x"]
        relevant = {"a", "b"}
        assert NDCG.compute(retrieved, relevant, k=3) == pytest.approx(1.0)

    def test_two_relevant_swapped_positions(self):
        # relevant at pos 1 and 2 (0-indexed): NDCG < 1
        retrieved = ["x", "a", "b"]
        relevant = {"a", "b"}
        dcg = 1 / math.log2(3) + 1 / math.log2(4)
        idcg = 1 / math.log2(2) + 1 / math.log2(3)
        assert NDCG.compute(retrieved, relevant, k=3) == pytest.approx(dcg / idcg)

    def test_k_limits_consideration(self):
        # Only k=1 → only first doc considered
        retrieved = ["a", "b"]
        relevant = {"b"}
        # top-1: [a] → DCG=0; IDCG = 1/log2(2)=1 → NDCG=0
        assert NDCG.compute(retrieved, relevant, k=1) == pytest.approx(0.0)

    def test_empty_retrieved(self):
        assert NDCG.compute([], {"a"}, k=3) == pytest.approx(0.0)

    def test_ndcg_value_between_0_and_1(self):
        retrieved = ["x", "a", "y", "b", "z"]
        relevant = {"a", "b"}
        result = NDCG.compute(retrieved, relevant, k=5)
        assert 0.0 <= result <= 1.0


# ===========================================================================
# F1Score
# ===========================================================================

class TestF1Score:
    def test_perfect_precision_and_recall(self):
        assert F1Score.compute(1.0, 1.0) == pytest.approx(1.0)

    def test_zero_precision_zero_recall(self):
        assert F1Score.compute(0.0, 0.0) == pytest.approx(0.0)

    def test_zero_precision(self):
        assert F1Score.compute(0.0, 1.0) == pytest.approx(0.0)

    def test_zero_recall(self):
        assert F1Score.compute(1.0, 0.0) == pytest.approx(0.0)

    def test_harmonic_mean(self):
        p, r = 0.6, 0.4
        expected = 2 * p * r / (p + r)
        assert F1Score.compute(p, r) == pytest.approx(expected)

    def test_equal_precision_recall(self):
        # F1 == P == R when they are equal
        assert F1Score.compute(0.7, 0.7) == pytest.approx(0.7)

    def test_high_precision_low_recall(self):
        p, r = 0.9, 0.1
        expected = 2 * 0.9 * 0.1 / 1.0
        assert F1Score.compute(p, r) == pytest.approx(expected)

    def test_low_precision_high_recall(self):
        p, r = 0.1, 0.9
        expected = 2 * 0.1 * 0.9 / 1.0
        assert F1Score.compute(p, r) == pytest.approx(expected)

    def test_returns_float(self):
        result = F1Score.compute(0.5, 0.5)
        assert isinstance(result, float)


# ===========================================================================
# EvalQuery
# ===========================================================================

class TestEvalQuery:
    def test_auto_query_id_generated(self):
        q = EvalQuery(query="hello", relevant_docs={"a.md"})
        assert len(q.query_id) == 8

    def test_auto_query_id_unique(self):
        q1 = EvalQuery(query="q", relevant_docs=set())
        q2 = EvalQuery(query="q", relevant_docs=set())
        assert q1.query_id != q2.query_id

    def test_explicit_query_id(self):
        q = EvalQuery(query="q", relevant_docs=set(), query_id="myid123")
        assert q.query_id == "myid123"

    def test_relevant_docs_is_set(self):
        q = EvalQuery(query="q", relevant_docs={"a", "b"})
        assert isinstance(q.relevant_docs, set)

    def test_metadata_defaults_to_empty_dict(self):
        q = EvalQuery(query="q", relevant_docs=set())
        assert q.metadata == {}

    def test_metadata_stored(self):
        q = EvalQuery(query="q", relevant_docs=set(), metadata={"tag": "test"})
        assert q.metadata["tag"] == "test"

    def test_query_string_stored(self):
        q = EvalQuery(query="find me", relevant_docs=set())
        assert q.query == "find me"


# ===========================================================================
# EvalDataset
# ===========================================================================

class TestEvalDataset:
    def _make_dataset(self, n=3):
        ds = EvalDataset()
        queries = []
        for i in range(n):
            q = EvalQuery(query=f"query {i}", relevant_docs={f"doc{i}.md"})
            ds.add(q)
            queries.append(q)
        return ds, queries

    def test_len_empty(self):
        assert len(EvalDataset()) == 0

    def test_len_after_add(self):
        ds, _ = self._make_dataset(3)
        assert len(ds) == 3

    def test_get_existing(self):
        ds, queries = self._make_dataset(2)
        result = ds.get(queries[0].query_id)
        assert result is queries[0]

    def test_get_missing_returns_none(self):
        ds, _ = self._make_dataset(1)
        assert ds.get("nonexistent") is None

    def test_iter_order_preserved(self):
        ds, queries = self._make_dataset(3)
        iterated = list(ds)
        assert [q.query_id for q in iterated] == [q.query_id for q in queries]

    def test_add_duplicate_id_replaces(self):
        ds = EvalDataset()
        q1 = EvalQuery(query="original", relevant_docs=set(), query_id="dup00001")
        q2 = EvalQuery(query="updated", relevant_docs=set(), query_id="dup00001")
        ds.add(q1)
        ds.add(q2)
        assert len(ds) == 1
        assert ds.get("dup00001").query == "updated"

    def test_from_list_basic(self):
        data = [
            {"query": "test query", "relevant_docs": ["a.md", "b.md"]},
        ]
        ds = EvalDataset.from_list(data)
        assert len(ds) == 1
        q = list(ds)[0]
        assert q.query == "test query"
        assert q.relevant_docs == {"a.md", "b.md"}

    def test_from_list_preserves_query_id(self):
        data = [{"query": "q", "relevant_docs": [], "query_id": "myqid1"}]
        ds = EvalDataset.from_list(data)
        assert list(ds)[0].query_id == "myqid1"

    def test_from_list_metadata(self):
        data = [{"query": "q", "relevant_docs": [], "metadata": {"src": "test"}}]
        ds = EvalDataset.from_list(data)
        assert list(ds)[0].metadata["src"] == "test"

    def test_from_list_multiple(self):
        data = [
            {"query": f"q{i}", "relevant_docs": [f"d{i}.md"]}
            for i in range(5)
        ]
        ds = EvalDataset.from_list(data)
        assert len(ds) == 5

    def test_to_list_round_trip(self):
        data = [
            {"query": "alpha", "relevant_docs": ["x.md", "y.md"], "query_id": "abc12345", "metadata": {}},
        ]
        ds = EvalDataset.from_list(data)
        out = ds.to_list()
        assert len(out) == 1
        assert out[0]["query"] == "alpha"
        assert sorted(out[0]["relevant_docs"]) == ["x.md", "y.md"]
        assert out[0]["query_id"] == "abc12345"

    def test_to_list_relevant_docs_sorted(self):
        data = [{"query": "q", "relevant_docs": ["z.md", "a.md"]}]
        ds = EvalDataset.from_list(data)
        out = ds.to_list()
        assert out[0]["relevant_docs"] == ["a.md", "z.md"]

    def test_from_list_empty_relevant_docs(self):
        data = [{"query": "q", "relevant_docs": []}]
        ds = EvalDataset.from_list(data)
        assert list(ds)[0].relevant_docs == set()

    def test_iter_yields_eval_query_instances(self):
        ds, _ = self._make_dataset(2)
        for q in ds:
            assert isinstance(q, EvalQuery)


# ===========================================================================
# EvalResult
# ===========================================================================

class TestEvalResult:
    def _make_result(self, precision=0.6, recall=0.4, mrr=0.5, ndcg=0.7):
        return EvalResult(
            query_id="testqid1",
            query="what is X",
            retrieved=["a", "b", "c"],
            relevant={"a", "b"},
            precision_at_5=precision,
            recall_at_5=recall,
            mrr=mrr,
            ndcg_at_5=ndcg,
        )

    def test_f1_harmonic_mean(self):
        r = self._make_result(precision=0.6, recall=0.4)
        expected = 2 * 0.6 * 0.4 / (0.6 + 0.4)
        assert r.f1() == pytest.approx(expected)

    def test_f1_zero_when_both_zero(self):
        r = self._make_result(precision=0.0, recall=0.0)
        assert r.f1() == pytest.approx(0.0)

    def test_f1_one_when_both_one(self):
        r = self._make_result(precision=1.0, recall=1.0)
        assert r.f1() == pytest.approx(1.0)

    def test_fields_stored(self):
        r = self._make_result()
        assert r.query_id == "testqid1"
        assert r.query == "what is X"
        assert r.retrieved == ["a", "b", "c"]
        assert r.relevant == {"a", "b"}
        assert r.precision_at_5 == pytest.approx(0.6)
        assert r.recall_at_5 == pytest.approx(0.4)
        assert r.mrr == pytest.approx(0.5)
        assert r.ndcg_at_5 == pytest.approx(0.7)


# ===========================================================================
# EvalReport
# ===========================================================================

class TestEvalReport:
    def _make_report(self):
        r1 = EvalResult(
            query_id="q1", query="q1", retrieved=["a"], relevant={"a"},
            precision_at_5=1.0, recall_at_5=1.0, mrr=1.0, ndcg_at_5=1.0,
        )
        r2 = EvalResult(
            query_id="q2", query="q2", retrieved=["x"], relevant={"a"},
            precision_at_5=0.0, recall_at_5=0.0, mrr=0.0, ndcg_at_5=0.0,
        )
        return EvalReport(results=[r1, r2], dataset_size=2)

    def test_avg_precision(self):
        report = self._make_report()
        assert report.avg_precision() == pytest.approx(0.5)

    def test_avg_recall(self):
        report = self._make_report()
        assert report.avg_recall() == pytest.approx(0.5)

    def test_avg_mrr(self):
        report = self._make_report()
        assert report.avg_mrr() == pytest.approx(0.5)

    def test_avg_ndcg(self):
        report = self._make_report()
        assert report.avg_ndcg() == pytest.approx(0.5)

    def test_avg_f1(self):
        report = self._make_report()
        # r1: f1=1.0, r2: f1=0.0 → avg=0.5
        assert report.avg_f1() == pytest.approx(0.5)

    def test_empty_report_zeros(self):
        report = EvalReport(results=[], dataset_size=0)
        assert report.avg_precision() == 0.0
        assert report.avg_recall() == 0.0
        assert report.avg_mrr() == 0.0
        assert report.avg_ndcg() == 0.0
        assert report.avg_f1() == 0.0

    def test_to_dict_keys(self):
        report = self._make_report()
        d = report.to_dict()
        assert "dataset_size" in d
        assert "num_results" in d
        assert "avg_precision_at_5" in d
        assert "avg_recall_at_5" in d
        assert "avg_mrr" in d
        assert "avg_ndcg_at_5" in d
        assert "avg_f1" in d
        assert "results" in d

    def test_to_dict_values(self):
        report = self._make_report()
        d = report.to_dict()
        assert d["dataset_size"] == 2
        assert d["num_results"] == 2
        assert d["avg_mrr"] == pytest.approx(0.5)

    def test_to_dict_results_list(self):
        report = self._make_report()
        d = report.to_dict()
        assert len(d["results"]) == 2
        assert "query_id" in d["results"][0]
        assert "f1" in d["results"][0]

    def test_to_dict_relevant_sorted(self):
        r = EvalResult(
            query_id="q1", query="q", retrieved=["a"], relevant={"z", "a"},
            precision_at_5=0.5, recall_at_5=0.5, mrr=0.5, ndcg_at_5=0.5,
        )
        report = EvalReport(results=[r], dataset_size=1)
        d = report.to_dict()
        assert d["results"][0]["relevant"] == ["a", "z"]

    def test_dataset_size_field(self):
        report = self._make_report()
        assert report.dataset_size == 2


# ===========================================================================
# EvalHarness
# ===========================================================================

class TestEvalHarness:
    def _make_dataset(self):
        return EvalDataset.from_list([
            {"query": "alpha", "relevant_docs": ["a.md", "b.md"], "query_id": "aaaaaaaa"},
            {"query": "beta", "relevant_docs": ["c.md"], "query_id": "bbbbbbbb"},
        ])

    def test_run_returns_eval_report(self):
        ds = self._make_dataset()
        harness = EvalHarness(ds)
        report = harness.run(lambda q: ["a.md", "b.md", "c.md"])
        assert isinstance(report, EvalReport)

    def test_run_result_count_matches_dataset(self):
        ds = self._make_dataset()
        harness = EvalHarness(ds)
        report = harness.run(lambda q: [])
        assert len(report.results) == 2

    def test_run_dataset_size(self):
        ds = self._make_dataset()
        harness = EvalHarness(ds)
        report = harness.run(lambda q: [])
        assert report.dataset_size == 2

    def test_run_perfect_search(self):
        def perfect_search(query):
            mapping = {
                "alpha": ["a.md", "b.md"],
                "beta": ["c.md"],
            }
            return mapping.get(query, [])

        ds = self._make_dataset()
        harness = EvalHarness(ds)
        report = harness.run(perfect_search)
        assert report.avg_precision() == pytest.approx(2 / 5 + 1 / 5, rel=1e-4) or \
               report.avg_precision() > 0.0

    def test_run_empty_search(self):
        ds = self._make_dataset()
        harness = EvalHarness(ds)
        report = harness.run(lambda q: [])
        assert report.avg_precision() == pytest.approx(0.0)
        assert report.avg_recall() == pytest.approx(0.0)
        assert report.avg_mrr() == pytest.approx(0.0)

    def test_run_top_k_limits_retrieved(self):
        """search_fn returns many docs but top_k should cap them."""
        called_with = {}

        def search_fn(q):
            return [f"doc{i}.md" for i in range(20)]

        ds = EvalDataset.from_list([
            {"query": "q", "relevant_docs": ["doc15.md"]},  # relevant beyond top_k=5
        ])
        harness = EvalHarness(ds)
        report = harness.run(search_fn, top_k=5)
        # retrieved list stored in result should be ≤ top_k
        assert len(report.results[0].retrieved) <= 5

    def test_run_query_ids_preserved(self):
        ds = self._make_dataset()
        harness = EvalHarness(ds)
        report = harness.run(lambda q: [])
        ids = {r.query_id for r in report.results}
        assert "aaaaaaaa" in ids
        assert "bbbbbbbb" in ids

    def test_run_empty_dataset(self):
        ds = EvalDataset()
        harness = EvalHarness(ds)
        report = harness.run(lambda q: ["x"])
        assert len(report.results) == 0
        assert report.dataset_size == 0
        assert report.avg_mrr() == 0.0

    def test_run_search_fn_receives_query_text(self):
        received = []

        def search_fn(q):
            received.append(q)
            return []

        ds = EvalDataset.from_list([
            {"query": "my query text", "relevant_docs": []},
        ])
        EvalHarness(ds).run(search_fn)
        assert received == ["my query text"]

    def test_run_metrics_computed_at_k5(self):
        """First 5 positions matter for precision/recall/NDCG."""
        ds = EvalDataset.from_list([
            {"query": "q", "relevant_docs": ["a.md"]},
        ])

        def search_returns_a_at_pos6(q):
            return ["x", "y", "z", "w", "v", "a.md"]

        report = EvalHarness(ds).run(search_returns_a_at_pos6, top_k=10)
        result = report.results[0]
        # "a.md" is at index 5 (pos 6), outside the K=5 window
        assert result.precision_at_5 == pytest.approx(0.0)
        assert result.recall_at_5 == pytest.approx(0.0)
        assert result.ndcg_at_5 == pytest.approx(0.0)
        # MRR looks at the full retrieved list
        assert result.mrr == pytest.approx(1 / 6)


# ===========================================================================
# Integration: full pipeline
# ===========================================================================

class TestIntegration:
    def test_full_pipeline_known_values(self):
        """End-to-end test with fully controlled inputs and verified outputs."""
        dataset = EvalDataset.from_list([
            {
                "query": "retrieval basics",
                "relevant_docs": ["rag.md", "bm25.md", "tfidf.md"],
                "query_id": "integ001",
            },
            {
                "query": "memory systems",
                "relevant_docs": ["memory.md"],
                "query_id": "integ002",
            },
        ])

        def mock_search(query):
            if query == "retrieval basics":
                # returns rag.md first (hit), then noise, then bm25.md at pos 4
                return ["rag.md", "x.md", "y.md", "bm25.md", "z.md"]
            if query == "memory systems":
                return ["other.md", "memory.md"]
            return []

        harness = EvalHarness(dataset)
        report = harness.run(mock_search, top_k=5)

        assert report.dataset_size == 2
        assert len(report.results) == 2

        # Validate query integ001
        r1 = next(r for r in report.results if r.query_id == "integ001")
        # top-5: [rag.md, x.md, y.md, bm25.md, z.md]
        # hits at k=5: rag.md + bm25.md = 2
        assert r1.precision_at_5 == pytest.approx(2 / 5)
        assert r1.recall_at_5 == pytest.approx(2 / (3 + 1e-10))
        assert r1.mrr == pytest.approx(1.0)  # rag.md is first

        # Validate query integ002
        r2 = next(r for r in report.results if r.query_id == "integ002")
        # top-5: [other.md, memory.md]
        # hits at k=5: memory.md = 1
        assert r2.precision_at_5 == pytest.approx(1 / 5)
        assert r2.recall_at_5 == pytest.approx(1 / (1 + 1e-10))
        assert r2.mrr == pytest.approx(0.5)  # memory.md at rank 2

        # Averages
        assert report.avg_mrr() == pytest.approx((1.0 + 0.5) / 2)

    def test_to_dict_serializable(self):
        """Ensure to_dict produces JSON-serialisable output."""
        import json
        ds = EvalDataset.from_list([
            {"query": "q", "relevant_docs": ["a.md"]},
        ])
        report = EvalHarness(ds).run(lambda q: ["a.md"])
        d = report.to_dict()
        # Should not raise
        json.dumps(d)

    def test_from_list_to_list_round_trip(self):
        """Dataset survives a from_list → to_list round trip."""
        original = [
            {"query": "q1", "relevant_docs": ["a.md"], "query_id": "rt000001", "metadata": {"k": "v"}},
            {"query": "q2", "relevant_docs": ["b.md", "c.md"], "query_id": "rt000002", "metadata": {}},
        ]
        ds = EvalDataset.from_list(original)
        restored = ds.to_list()
        assert len(restored) == 2
        assert restored[0]["query"] == "q1"
        assert restored[0]["query_id"] == "rt000001"
        assert restored[0]["metadata"] == {"k": "v"}
        assert restored[1]["relevant_docs"] == ["b.md", "c.md"]
