"""Tests for docstoolkit.federated_eval — privacy-preserving federated golden datasets."""
import math
import pytest

from docstoolkit.federated_eval import (
    add_laplace_noise, PrivacyBudget, privatize_metrics,
    FederatedNode, NodeMetrics,
    SecureAggregator, AggregatedReport,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_metrics(node_id="node-1", query_count=100, precision_at_5=0.8,
                 recall_at_5=0.7, mrr=0.75, avg_latency_ms=42.0,
                 golden_queries=50, ts="2026-01-01T00:00:00") -> NodeMetrics:
    return NodeMetrics(
        node_id=node_id,
        query_count=query_count,
        precision_at_5=precision_at_5,
        recall_at_5=recall_at_5,
        mrr=mrr,
        avg_latency_ms=avg_latency_ms,
        golden_queries=golden_queries,
        ts=ts,
    )


# ===========================================================================
# PrivacyBudget
# ===========================================================================

class TestPrivacyBudget:
    def test_default_values(self):
        b = PrivacyBudget()
        assert b.epsilon == 1.0
        assert b.delta == 1e-5
        assert b.sensitivity == 1.0

    def test_noise_scale_basic(self):
        b = PrivacyBudget(epsilon=2.0, sensitivity=1.0)
        assert b.noise_scale() == pytest.approx(0.5)

    def test_noise_scale_sensitivity(self):
        b = PrivacyBudget(epsilon=1.0, sensitivity=2.0)
        assert b.noise_scale() == pytest.approx(2.0)

    def test_noise_scale_zero_epsilon(self):
        b = PrivacyBudget(epsilon=0.0)
        assert b.noise_scale() == float('inf')

    def test_noise_scale_negative_epsilon(self):
        b = PrivacyBudget(epsilon=-1.0)
        assert b.noise_scale() == float('inf')

    def test_is_valid_true(self):
        assert PrivacyBudget(epsilon=1.0, delta=1e-5, sensitivity=1.0).is_valid()

    def test_is_valid_zero_epsilon(self):
        assert not PrivacyBudget(epsilon=0.0).is_valid()

    def test_is_valid_negative_epsilon(self):
        assert not PrivacyBudget(epsilon=-0.1).is_valid()

    def test_is_valid_negative_delta(self):
        assert not PrivacyBudget(epsilon=1.0, delta=-0.1).is_valid()

    def test_is_valid_delta_equals_one(self):
        assert not PrivacyBudget(epsilon=1.0, delta=1.0).is_valid()

    def test_is_valid_zero_sensitivity(self):
        assert not PrivacyBudget(epsilon=1.0, sensitivity=0.0).is_valid()

    def test_is_valid_negative_sensitivity(self):
        assert not PrivacyBudget(epsilon=1.0, sensitivity=-1.0).is_valid()

    def test_noise_scale_formula(self):
        b = PrivacyBudget(epsilon=0.5, sensitivity=3.0)
        assert b.noise_scale() == pytest.approx(6.0)

    def test_is_valid_delta_zero(self):
        assert PrivacyBudget(epsilon=1.0, delta=0.0).is_valid()

    def test_custom_values(self):
        b = PrivacyBudget(epsilon=0.1, delta=1e-8, sensitivity=0.5)
        assert b.epsilon == 0.1
        assert b.delta == 1e-8
        assert b.sensitivity == 0.5


# ===========================================================================
# add_laplace_noise
# ===========================================================================

class TestAddLaplaceNoise:
    def test_returns_float(self):
        b = PrivacyBudget(epsilon=1.0)
        result = add_laplace_noise(0.5, b, seed=42)
        assert isinstance(result, float)

    def test_result_in_unit_interval(self):
        b = PrivacyBudget(epsilon=1.0)
        for seed in range(20):
            r = add_laplace_noise(0.5, b, seed=seed)
            assert 0.0 <= r <= 1.0

    def test_deterministic_with_same_seed(self):
        b = PrivacyBudget(epsilon=1.0)
        r1 = add_laplace_noise(0.6, b, seed=7)
        r2 = add_laplace_noise(0.6, b, seed=7)
        assert r1 == r2

    def test_different_seeds_give_different_results(self):
        b = PrivacyBudget(epsilon=1.0)
        results = {add_laplace_noise(0.5, b, seed=i) for i in range(10)}
        assert len(results) > 1

    def test_epsilon_zero_returns_value_unchanged(self):
        b = PrivacyBudget(epsilon=0.0)
        assert add_laplace_noise(0.7, b, seed=1) == 0.7

    def test_high_epsilon_small_noise(self):
        """Very high epsilon → very small noise → result close to input."""
        b = PrivacyBudget(epsilon=10000.0)
        for seed in range(10):
            r = add_laplace_noise(0.5, b, seed=seed)
            assert abs(r - 0.5) < 0.01

    def test_low_epsilon_large_noise(self):
        """Very low epsilon → large noise → results spread away from input."""
        b = PrivacyBudget(epsilon=0.001)
        results = [add_laplace_noise(0.5, b, seed=i) for i in range(30)]
        # With large noise we expect to hit both 0 and 1 boundaries frequently
        spread = max(results) - min(results)
        assert spread > 0.5

    def test_clipped_at_zero(self):
        """Result is always >= 0."""
        b = PrivacyBudget(epsilon=0.001)
        for seed in range(50):
            assert add_laplace_noise(0.0, b, seed=seed) >= 0.0

    def test_clipped_at_one(self):
        """Result is always <= 1."""
        b = PrivacyBudget(epsilon=0.001)
        for seed in range(50):
            assert add_laplace_noise(1.0, b, seed=seed) <= 1.0

    def test_seed_none_runs(self):
        b = PrivacyBudget(epsilon=1.0)
        r = add_laplace_noise(0.5, b, seed=None)
        assert 0.0 <= r <= 1.0

    def test_boundary_value_zero(self):
        b = PrivacyBudget(epsilon=1.0)
        r = add_laplace_noise(0.0, b, seed=42)
        assert 0.0 <= r <= 1.0

    def test_boundary_value_one(self):
        b = PrivacyBudget(epsilon=1.0)
        r = add_laplace_noise(1.0, b, seed=42)
        assert 0.0 <= r <= 1.0


# ===========================================================================
# privatize_metrics
# ===========================================================================

class TestPrivatizeMetrics:
    def test_float_values_get_noise(self):
        b = PrivacyBudget(epsilon=1.0)
        raw = {"precision": 0.8, "recall": 0.7}
        result = privatize_metrics(raw, b, seed=42)
        # keys preserved
        assert "precision" in result
        assert "recall" in result
        # values are floats in [0,1]
        assert isinstance(result["precision"], float)
        assert 0.0 <= result["precision"] <= 1.0

    def test_string_values_passed_through(self):
        b = PrivacyBudget(epsilon=1.0)
        raw = {"node_id": "abc", "ts": "2026-01-01"}
        result = privatize_metrics(raw, b, seed=1)
        assert result["node_id"] == "abc"
        assert result["ts"] == "2026-01-01"

    def test_int_values_returned_as_int(self):
        b = PrivacyBudget(epsilon=1.0)
        raw = {"query_count": 100, "golden_queries": 50}
        result = privatize_metrics(raw, b, seed=5)
        assert isinstance(result["query_count"], int)
        assert isinstance(result["golden_queries"], int)

    def test_int_values_clipped_non_negative(self):
        b = PrivacyBudget(epsilon=0.001)  # large noise
        raw = {"count": 1}
        for seed in range(30):
            result = privatize_metrics(raw, b, seed=seed)
            assert result["count"] >= 0

    def test_same_keys_in_result(self):
        b = PrivacyBudget(epsilon=1.0)
        raw = {"a": 0.5, "b": 10, "c": "hello"}
        result = privatize_metrics(raw, b, seed=0)
        assert set(result.keys()) == set(raw.keys())

    def test_empty_dict(self):
        b = PrivacyBudget(epsilon=1.0)
        assert privatize_metrics({}, b) == {}

    def test_high_epsilon_preserves_floats_approx(self):
        b = PrivacyBudget(epsilon=100000.0)
        raw = {"p": 0.8, "r": 0.6}
        result = privatize_metrics(raw, b, seed=1)
        assert abs(result["p"] - 0.8) < 0.001
        assert abs(result["r"] - 0.6) < 0.001

    def test_mixed_types(self):
        b = PrivacyBudget(epsilon=1.0)
        raw = {"node_id": "x", "count": 50, "score": 0.9}
        result = privatize_metrics(raw, b, seed=3)
        assert result["node_id"] == "x"
        assert isinstance(result["count"], int)
        assert isinstance(result["score"], float)

    def test_deterministic_with_seed(self):
        b = PrivacyBudget(epsilon=1.0)
        raw = {"p": 0.5, "q": 0.3}
        r1 = privatize_metrics(raw, b, seed=99)
        r2 = privatize_metrics(raw, b, seed=99)
        assert r1 == r2


# ===========================================================================
# NodeMetrics
# ===========================================================================

class TestNodeMetrics:
    def test_to_dict_keys(self):
        m = make_metrics()
        d = m.to_dict()
        expected_keys = {"node_id", "query_count", "precision_at_5",
                         "recall_at_5", "mrr", "avg_latency_ms", "golden_queries", "ts"}
        assert set(d.keys()) == expected_keys

    def test_to_dict_values(self):
        m = make_metrics(node_id="n1", query_count=200, precision_at_5=0.9)
        d = m.to_dict()
        assert d["node_id"] == "n1"
        assert d["query_count"] == 200
        assert d["precision_at_5"] == 0.9

    def test_from_dict_round_trip(self):
        m = make_metrics()
        d = m.to_dict()
        m2 = NodeMetrics.from_dict(d)
        assert m2.node_id == m.node_id
        assert m2.query_count == m.query_count
        assert m2.precision_at_5 == m.precision_at_5
        assert m2.recall_at_5 == m.recall_at_5
        assert m2.mrr == m.mrr
        assert m2.avg_latency_ms == m.avg_latency_ms
        assert m2.golden_queries == m.golden_queries

    def test_ts_auto_set_if_empty(self):
        m = NodeMetrics(
            node_id="x", query_count=1, precision_at_5=0.5,
            recall_at_5=0.5, mrr=0.5, avg_latency_ms=10.0, golden_queries=5
        )
        assert m.ts != ""
        assert len(m.ts) >= 10  # ISO format is at least 10 chars

    def test_ts_preserved_if_given(self):
        m = make_metrics(ts="2026-06-01T12:00:00")
        assert m.ts == "2026-06-01T12:00:00"

    def test_from_dict_defaults_missing_fields(self):
        d = {"node_id": "n1"}
        m = NodeMetrics.from_dict(d)
        assert m.query_count == 0
        assert m.precision_at_5 == 0.0
        assert m.mrr == 0.0

    def test_all_fields_present_in_dict(self):
        m = make_metrics()
        d = m.to_dict()
        for key in ("node_id", "query_count", "precision_at_5", "recall_at_5",
                    "mrr", "avg_latency_ms", "golden_queries", "ts"):
            assert key in d

    def test_from_dict_type_coercion(self):
        d = {"node_id": "n", "query_count": "50", "precision_at_5": "0.7",
             "recall_at_5": "0.6", "mrr": "0.65", "avg_latency_ms": "30.0",
             "golden_queries": "20", "ts": ""}
        m = NodeMetrics.from_dict(d)
        assert isinstance(m.query_count, int)
        assert isinstance(m.precision_at_5, float)


# ===========================================================================
# FederatedNode
# ===========================================================================

class TestFederatedNode:
    def test_default_privacy_budget_created(self):
        node = FederatedNode(node_id="n1")
        assert node.privacy_budget is not None
        assert isinstance(node.privacy_budget, PrivacyBudget)

    def test_custom_privacy_budget(self):
        b = PrivacyBudget(epsilon=0.5)
        node = FederatedNode(node_id="n1", privacy_budget=b)
        assert node.privacy_budget.epsilon == 0.5

    def test_submit_metrics_returns_dict(self):
        node = FederatedNode(node_id="n1")
        m = make_metrics()
        result = node.submit_metrics(m, seed=1)
        assert isinstance(result, dict)

    def test_submit_metrics_dict_has_correct_keys(self):
        node = FederatedNode(node_id="n1")
        m = make_metrics()
        result = node.submit_metrics(m, seed=1)
        assert "node_id" in result
        assert "precision_at_5" in result
        assert "query_count" in result

    def test_submit_metrics_values_are_privatized(self):
        """With moderate epsilon the values may differ from originals."""
        b = PrivacyBudget(epsilon=0.1)  # strong privacy → large noise
        node = FederatedNode(node_id="n1", privacy_budget=b)
        m = make_metrics(precision_at_5=0.8)
        results = [node.submit_metrics(m, seed=i)["precision_at_5"] for i in range(10)]
        # With heavy noise, not all results should be exactly 0.8
        assert not all(r == pytest.approx(0.8) for r in results)

    def test_history_grows_with_submissions(self):
        node = FederatedNode(node_id="n1")
        assert len(node.history()) == 0
        node.submit_metrics(make_metrics(), seed=0)
        assert len(node.history()) == 1
        node.submit_metrics(make_metrics(), seed=1)
        assert len(node.history()) == 2

    def test_history_contains_original_metrics(self):
        node = FederatedNode(node_id="n1")
        m = make_metrics(precision_at_5=0.9)
        node.submit_metrics(m, seed=0)
        assert node.history()[0].precision_at_5 == 0.9

    def test_history_is_copy(self):
        node = FederatedNode(node_id="n1")
        node.submit_metrics(make_metrics(), seed=0)
        h = node.history()
        h.clear()
        assert len(node.history()) == 1  # internal list unaffected

    def test_node_id_preserved_in_output(self):
        node = FederatedNode(node_id="alpha")
        m = make_metrics(node_id="alpha")
        result = node.submit_metrics(m, seed=0)
        assert result["node_id"] == "alpha"

    def test_multiple_nodes_independent(self):
        n1 = FederatedNode(node_id="n1")
        n2 = FederatedNode(node_id="n2")
        n1.submit_metrics(make_metrics(node_id="n1"), seed=0)
        assert len(n2.history()) == 0


# ===========================================================================
# AggregatedReport
# ===========================================================================

class TestAggregatedReport:
    def test_f1_formula(self):
        r = AggregatedReport(
            node_count=2, total_queries=200,
            avg_precision_at_5=0.8, avg_recall_at_5=0.6,
            avg_mrr=0.7, avg_latency_ms=30.0,
            total_golden_queries=100,
        )
        expected = 2 * 0.8 * 0.6 / (0.8 + 0.6)
        assert r.f1() == pytest.approx(expected)

    def test_f1_zero_when_both_zero(self):
        r = AggregatedReport(
            node_count=1, total_queries=0,
            avg_precision_at_5=0.0, avg_recall_at_5=0.0,
            avg_mrr=0.0, avg_latency_ms=0.0,
            total_golden_queries=0,
        )
        assert r.f1() == 0.0

    def test_f1_with_perfect_precision_recall(self):
        r = AggregatedReport(
            node_count=1, total_queries=50,
            avg_precision_at_5=1.0, avg_recall_at_5=1.0,
            avg_mrr=1.0, avg_latency_ms=10.0,
            total_golden_queries=20,
        )
        assert r.f1() == pytest.approx(1.0)

    def test_summary_contains_node_count(self):
        r = AggregatedReport(
            node_count=3, total_queries=300,
            avg_precision_at_5=0.8, avg_recall_at_5=0.7,
            avg_mrr=0.75, avg_latency_ms=25.0,
            total_golden_queries=90,
        )
        assert "nodes=3" in r.summary()

    def test_summary_contains_queries(self):
        r = AggregatedReport(
            node_count=1, total_queries=150,
            avg_precision_at_5=0.5, avg_recall_at_5=0.5,
            avg_mrr=0.5, avg_latency_ms=20.0,
            total_golden_queries=40,
        )
        assert "queries=150" in r.summary()

    def test_summary_contains_p_at_5(self):
        r = AggregatedReport(
            node_count=1, total_queries=10,
            avg_precision_at_5=0.123, avg_recall_at_5=0.456,
            avg_mrr=0.789, avg_latency_ms=5.0,
            total_golden_queries=5,
        )
        assert "P@5=0.123" in r.summary()

    def test_summary_contains_mrr(self):
        r = AggregatedReport(
            node_count=1, total_queries=10,
            avg_precision_at_5=0.5, avg_recall_at_5=0.5,
            avg_mrr=0.666, avg_latency_ms=5.0,
            total_golden_queries=5,
        )
        assert "MRR=0.666" in r.summary()

    def test_summary_contains_f1(self):
        r = AggregatedReport(
            node_count=1, total_queries=10,
            avg_precision_at_5=0.8, avg_recall_at_5=0.8,
            avg_mrr=0.8, avg_latency_ms=5.0,
            total_golden_queries=5,
        )
        assert "F1=" in r.summary()

    def test_node_ids_default_empty(self):
        r = AggregatedReport(
            node_count=0, total_queries=0,
            avg_precision_at_5=0.0, avg_recall_at_5=0.0,
            avg_mrr=0.0, avg_latency_ms=0.0,
            total_golden_queries=0,
        )
        assert r.node_ids == []

    def test_node_ids_stored(self):
        r = AggregatedReport(
            node_count=2, total_queries=100,
            avg_precision_at_5=0.7, avg_recall_at_5=0.7,
            avg_mrr=0.7, avg_latency_ms=20.0,
            total_golden_queries=50,
            node_ids=["n1", "n2"],
        )
        assert "n1" in r.node_ids
        assert "n2" in r.node_ids


# ===========================================================================
# SecureAggregator
# ===========================================================================

class TestSecureAggregator:
    def setup_method(self):
        self.agg = SecureAggregator()

    def test_aggregate_empty_list(self):
        report = self.agg.aggregate([])
        assert report.node_count == 0
        assert report.total_queries == 0
        assert report.avg_precision_at_5 == 0.0
        assert report.avg_recall_at_5 == 0.0
        assert report.avg_mrr == 0.0
        assert report.avg_latency_ms == 0.0
        assert report.total_golden_queries == 0

    def test_aggregate_single_report(self):
        reports = [{
            "node_id": "n1", "query_count": 100,
            "precision_at_5": 0.8, "recall_at_5": 0.7,
            "mrr": 0.75, "avg_latency_ms": 30.0,
            "golden_queries": 50, "ts": "2026-01-01T00:00:00",
        }]
        report = self.agg.aggregate(reports)
        assert report.node_count == 1
        assert report.total_queries == 100
        assert report.avg_precision_at_5 == pytest.approx(0.8)
        assert report.avg_recall_at_5 == pytest.approx(0.7)
        assert report.avg_mrr == pytest.approx(0.75)
        assert report.total_golden_queries == 50

    def test_aggregate_two_equal_reports(self):
        r = {
            "node_id": "n", "query_count": 100,
            "precision_at_5": 0.6, "recall_at_5": 0.5,
            "mrr": 0.55, "avg_latency_ms": 20.0,
            "golden_queries": 30,
        }
        report = self.agg.aggregate([r, r])
        assert report.node_count == 2
        assert report.total_queries == 200
        assert report.avg_precision_at_5 == pytest.approx(0.6)
        assert report.avg_recall_at_5 == pytest.approx(0.5)

    def test_weighted_average_by_query_count(self):
        """Weighted average: n1 has 100 queries P=1.0, n2 has 300 queries P=0.0 → avg=0.25"""
        r1 = {"node_id": "n1", "query_count": 100, "precision_at_5": 1.0,
              "recall_at_5": 0.0, "mrr": 0.0, "avg_latency_ms": 0.0, "golden_queries": 0}
        r2 = {"node_id": "n2", "query_count": 300, "precision_at_5": 0.0,
              "recall_at_5": 0.0, "mrr": 0.0, "avg_latency_ms": 0.0, "golden_queries": 0}
        report = self.agg.aggregate([r1, r2])
        assert report.avg_precision_at_5 == pytest.approx(0.25)

    def test_total_queries_sum(self):
        reports = [
            {"node_id": "a", "query_count": 50, "precision_at_5": 0.5,
             "recall_at_5": 0.5, "mrr": 0.5, "avg_latency_ms": 10.0, "golden_queries": 10},
            {"node_id": "b", "query_count": 75, "precision_at_5": 0.5,
             "recall_at_5": 0.5, "mrr": 0.5, "avg_latency_ms": 10.0, "golden_queries": 15},
            {"node_id": "c", "query_count": 25, "precision_at_5": 0.5,
             "recall_at_5": 0.5, "mrr": 0.5, "avg_latency_ms": 10.0, "golden_queries": 5},
        ]
        report = self.agg.aggregate(reports)
        assert report.total_queries == 150

    def test_total_golden_queries_sum(self):
        reports = [
            {"node_id": "a", "query_count": 100, "precision_at_5": 0.5,
             "recall_at_5": 0.5, "mrr": 0.5, "avg_latency_ms": 10.0, "golden_queries": 20},
            {"node_id": "b", "query_count": 100, "precision_at_5": 0.5,
             "recall_at_5": 0.5, "mrr": 0.5, "avg_latency_ms": 10.0, "golden_queries": 35},
        ]
        report = self.agg.aggregate(reports)
        assert report.total_golden_queries == 55

    def test_node_count_equals_len_reports(self):
        reports = [
            {"node_id": f"n{i}", "query_count": 10, "precision_at_5": 0.5,
             "recall_at_5": 0.5, "mrr": 0.5, "avg_latency_ms": 5.0, "golden_queries": 2}
            for i in range(5)
        ]
        report = self.agg.aggregate(reports)
        assert report.node_count == 5

    def test_node_ids_collected(self):
        reports = [
            {"node_id": "alpha", "query_count": 10, "precision_at_5": 0.5,
             "recall_at_5": 0.5, "mrr": 0.5, "avg_latency_ms": 5.0, "golden_queries": 2},
            {"node_id": "beta", "query_count": 10, "precision_at_5": 0.5,
             "recall_at_5": 0.5, "mrr": 0.5, "avg_latency_ms": 5.0, "golden_queries": 2},
        ]
        report = self.agg.aggregate(reports)
        assert "alpha" in report.node_ids
        assert "beta" in report.node_ids

    def test_aggregate_returns_aggregated_report(self):
        report = self.agg.aggregate([])
        assert isinstance(report, AggregatedReport)

    def test_aggregate_with_node_submit_metrics(self):
        """Integration: use FederatedNode.submit_metrics output as input to aggregator."""
        b = PrivacyBudget(epsilon=100.0)  # low noise for predictable test
        node = FederatedNode(node_id="n1", privacy_budget=b)
        m = make_metrics(node_id="n1", query_count=50, precision_at_5=0.9)
        privatized = node.submit_metrics(m, seed=42)
        report = self.agg.aggregate([privatized])
        assert report.node_count == 1
        assert report.total_queries == privatized["query_count"]

    def test_aggregate_three_nodes_mrr(self):
        reports = [
            {"node_id": "n1", "query_count": 200, "precision_at_5": 0.7,
             "recall_at_5": 0.6, "mrr": 0.8, "avg_latency_ms": 15.0, "golden_queries": 40},
            {"node_id": "n2", "query_count": 200, "precision_at_5": 0.7,
             "recall_at_5": 0.6, "mrr": 0.8, "avg_latency_ms": 15.0, "golden_queries": 40},
            {"node_id": "n3", "query_count": 200, "precision_at_5": 0.7,
             "recall_at_5": 0.6, "mrr": 0.8, "avg_latency_ms": 15.0, "golden_queries": 40},
        ]
        report = self.agg.aggregate(reports)
        assert report.avg_mrr == pytest.approx(0.8)
        assert report.total_queries == 600
