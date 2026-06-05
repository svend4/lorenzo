"""Tests for E204 doc_stats module."""
from __future__ import annotations

import math

import pytest

from docstoolkit.doc_stats import (
    ComparisonResult,
    Distribution,
    DocStat,
    DocStats,
    GroupedStats,
    MetricType,
)


# --------------------------------------------------------------------- fixtures


@pytest.fixture
def simple_docs():
    return [
        {"id": 1, "size": 10, "category": "a"},
        {"id": 2, "size": 20, "category": "a"},
        {"id": 3, "size": 30, "category": "b"},
        {"id": 4, "size": 40, "category": "b"},
        {"id": 5, "size": 50, "category": "c"},
    ]


@pytest.fixture
def nested_docs():
    return [
        {"id": 1, "metadata": {"size": 100, "tags": ["x"]}},
        {"id": 2, "metadata": {"size": 200, "tags": ["y"]}},
        {"id": 3, "metadata": {"size": 300, "tags": ["x"]}},
    ]


@pytest.fixture
def stats():
    return DocStats()


# ============================================================== TestMetricType


class TestMetricType:
    def test_count_value(self):
        assert MetricType.COUNT.value == "count"

    def test_avg_value(self):
        assert MetricType.AVG.value == "avg"

    def test_p99_value(self):
        assert MetricType.P99.value == "p99"

    def test_all_members_present(self):
        names = {m.name for m in MetricType}
        for required in [
            "COUNT", "SUM", "AVG", "MEDIAN", "MIN", "MAX",
            "STDDEV", "P25", "P50", "P75", "P90", "P99",
        ]:
            assert required in names


# ============================================================== TestDocStat


class TestDocStat:
    def test_create(self):
        s = DocStat(metric_type=MetricType.AVG, value=1.5, field="x")
        assert s.metric_type == MetricType.AVG
        assert s.value == 1.5
        assert s.field == "x"


# ============================================================== TestGroupedStats


class TestGroupedStats:
    def test_create(self):
        g = GroupedStats(
            group_key="a",
            count=3,
            stats={"size": {MetricType.AVG: 10.0}},
        )
        assert g.group_key == "a"
        assert g.count == 3
        assert g.stats["size"][MetricType.AVG] == 10.0

    def test_default_stats(self):
        g = GroupedStats(group_key="x", count=0)
        assert g.stats == {}


# ============================================================== TestDistribution


class TestDistribution:
    def test_create(self):
        d = Distribution(
            field="size",
            histogram={"[0, 10)": 2},
            bin_count=5,
            min_value=0.0,
            max_value=10.0,
        )
        assert d.field == "size"
        assert d.bin_count == 5
        assert d.histogram["[0, 10)"] == 2


# ============================================================== TestComparisonResult


class TestComparisonResult:
    def test_create(self):
        c = ComparisonResult(
            field="size",
            metric=MetricType.AVG,
            value_a=10.0,
            value_b=20.0,
            delta=10.0,
            pct_change=100.0,
        )
        assert c.field == "size"
        assert c.delta == 10.0


# ============================================================== TestCompute


class TestCompute:
    def test_compute_count(self, stats, simple_docs):
        r = stats.compute(simple_docs, "size", MetricType.COUNT)
        assert r.value == 5.0
        assert r.field == "size"

    def test_compute_sum(self, stats, simple_docs):
        r = stats.compute(simple_docs, "size", MetricType.SUM)
        assert r.value == 150.0

    def test_compute_avg(self, stats, simple_docs):
        r = stats.compute(simple_docs, "size", MetricType.AVG)
        assert r.value == 30.0

    def test_compute_median(self, stats, simple_docs):
        r = stats.compute(simple_docs, "size", MetricType.MEDIAN)
        assert r.value == 30.0

    def test_compute_min(self, stats, simple_docs):
        r = stats.compute(simple_docs, "size", MetricType.MIN)
        assert r.value == 10.0

    def test_compute_max(self, stats, simple_docs):
        r = stats.compute(simple_docs, "size", MetricType.MAX)
        assert r.value == 50.0

    def test_compute_stddev(self, stats, simple_docs):
        r = stats.compute(simple_docs, "size", MetricType.STDDEV)
        assert r.value == pytest.approx(15.81, abs=0.01)

    def test_compute_p25(self, stats, simple_docs):
        r = stats.compute(simple_docs, "size", MetricType.P25)
        assert r.value == 20.0

    def test_compute_p50(self, stats, simple_docs):
        r = stats.compute(simple_docs, "size", MetricType.P50)
        assert r.value == 30.0

    def test_compute_p75(self, stats, simple_docs):
        r = stats.compute(simple_docs, "size", MetricType.P75)
        assert r.value == 40.0

    def test_compute_empty(self, stats):
        r = stats.compute([], "size", MetricType.AVG)
        assert r.value == 0.0


# ============================================================== TestComputeMany


class TestComputeMany:
    def test_default_metrics(self, stats, simple_docs):
        result = stats.compute_many(simple_docs, "size")
        assert MetricType.COUNT in result
        assert MetricType.AVG in result
        assert result[MetricType.COUNT] == 5.0
        assert result[MetricType.AVG] == 30.0

    def test_custom_metrics(self, stats, simple_docs):
        result = stats.compute_many(
            simple_docs, "size", metrics=[MetricType.MIN, MetricType.MAX]
        )
        assert set(result.keys()) == {MetricType.MIN, MetricType.MAX}
        assert result[MetricType.MIN] == 10.0
        assert result[MetricType.MAX] == 50.0

    def test_empty_docs(self, stats):
        result = stats.compute_many([], "size", metrics=[MetricType.AVG])
        assert result[MetricType.AVG] == 0.0


# ============================================================== TestGroupBy


class TestGroupBy:
    def test_group_basic(self, stats, simple_docs):
        groups = stats.group_by(simple_docs, "category", ["size"])
        keys = [g.group_key for g in groups]
        assert keys == ["a", "b", "c"]

    def test_group_counts(self, stats, simple_docs):
        groups = stats.group_by(simple_docs, "category", ["size"])
        bykey = {g.group_key: g for g in groups}
        assert bykey["a"].count == 2
        assert bykey["b"].count == 2
        assert bykey["c"].count == 1

    def test_group_stats(self, stats, simple_docs):
        groups = stats.group_by(
            simple_docs, "category", ["size"], metrics=[MetricType.AVG]
        )
        bykey = {g.group_key: g for g in groups}
        assert bykey["a"].stats["size"][MetricType.AVG] == 15.0
        assert bykey["b"].stats["size"][MetricType.AVG] == 35.0

    def test_group_skip_missing_key(self, stats):
        docs = [{"x": 1, "g": "a"}, {"x": 2}]  # missing g
        groups = stats.group_by(docs, "g", ["x"])
        assert len(groups) == 1
        assert groups[0].group_key == "a"

    def test_group_empty_docs(self, stats):
        groups = stats.group_by([], "category", ["size"])
        assert groups == []


# ============================================================== TestCountBy


class TestCountBy:
    def test_count_by_basic(self, stats, simple_docs):
        result = stats.count_by(simple_docs, "category")
        assert result == {"a": 2, "b": 2, "c": 1}

    def test_count_by_missing(self, stats):
        docs = [{"x": 1}, {"x": 1}, {"y": 2}]
        result = stats.count_by(docs, "x")
        assert result == {1: 2}

    def test_count_by_empty(self, stats):
        assert stats.count_by([], "x") == {}

    def test_count_by_unhashable_value(self, stats):
        docs = [{"tags": ["a", "b"]}, {"tags": ["a", "b"]}]
        result = stats.count_by(docs, "tags")
        # Lists coerced to string keys.
        assert sum(result.values()) == 2


# ============================================================== TestDistribution


class TestDistributionCompute:
    def test_distribution_basic(self, stats, simple_docs):
        d = stats.distribution(simple_docs, "size", bins=5)
        assert d.field == "size"
        assert d.bin_count == 5
        assert d.min_value == 10.0
        assert d.max_value == 50.0
        assert sum(d.histogram.values()) == 5

    def test_distribution_default_bins(self, stats, simple_docs):
        d = stats.distribution(simple_docs, "size")
        assert d.bin_count == 10

    def test_distribution_empty(self, stats):
        d = stats.distribution([], "size", bins=5)
        assert d.histogram == {}
        assert d.min_value == 0.0
        assert d.max_value == 0.0

    def test_distribution_all_same(self, stats):
        docs = [{"x": 5} for _ in range(4)]
        d = stats.distribution(docs, "x", bins=3)
        assert sum(d.histogram.values()) == 4
        assert d.min_value == 5.0
        assert d.max_value == 5.0

    def test_distribution_bins_lower_clamp(self, stats, simple_docs):
        d = stats.distribution(simple_docs, "size", bins=0)
        # Clamped to at least 1.
        assert d.bin_count >= 1


# ============================================================== TestCompare


class TestCompare:
    def test_compare_basic(self, stats):
        a = [{"x": 10}, {"x": 20}]
        b = [{"x": 20}, {"x": 40}]
        results = stats.compare(a, b, "x", metrics=[MetricType.AVG])
        assert len(results) == 1
        assert results[0].value_a == 15.0
        assert results[0].value_b == 30.0
        assert results[0].delta == 15.0
        assert results[0].pct_change == 100.0

    def test_compare_default_metrics(self, stats):
        a = [{"x": 1}]
        b = [{"x": 2}]
        results = stats.compare(a, b, "x")
        metrics_present = {r.metric for r in results}
        assert MetricType.AVG in metrics_present
        assert MetricType.SUM in metrics_present

    def test_compare_zero_baseline(self, stats):
        a: list[dict] = []
        b = [{"x": 5}]
        results = stats.compare(a, b, "x", metrics=[MetricType.SUM])
        # SUM of empty == 0, comparing with non-zero → inf
        assert math.isinf(results[0].pct_change)

    def test_compare_both_zero(self, stats):
        results = stats.compare([], [], "x", metrics=[MetricType.SUM])
        assert results[0].pct_change == 0.0

    def test_compare_count(self, stats):
        a = [{"x": 1}, {"x": 2}]
        b = [{"x": 1}, {"x": 2}, {"x": 3}]
        results = stats.compare(a, b, "x", metrics=[MetricType.COUNT])
        assert results[0].value_a == 2.0
        assert results[0].value_b == 3.0
        assert results[0].delta == 1.0


# ============================================================== TestTopN


class TestTopN:
    def test_top_n_default(self, stats, simple_docs):
        result = stats.top_n(simple_docs, "size", n=2)
        assert len(result) == 2
        assert result[0]["size"] == 50
        assert result[1]["size"] == 40

    def test_top_n_all(self, stats, simple_docs):
        result = stats.top_n(simple_docs, "size", n=100)
        assert len(result) == 5

    def test_top_n_empty(self, stats):
        assert stats.top_n([], "size") == []

    def test_top_n_zero(self, stats, simple_docs):
        assert stats.top_n(simple_docs, "size", n=0) == []

    def test_top_n_skip_missing(self, stats):
        docs = [{"x": 5}, {"y": 10}, {"x": 7}]
        result = stats.top_n(docs, "x", n=5)
        assert len(result) == 2
        assert result[0]["x"] == 7


# ============================================================== TestBottomN


class TestBottomN:
    def test_bottom_n_default(self, stats, simple_docs):
        result = stats.bottom_n(simple_docs, "size", n=2)
        assert len(result) == 2
        assert result[0]["size"] == 10
        assert result[1]["size"] == 20

    def test_bottom_n_all(self, stats, simple_docs):
        result = stats.bottom_n(simple_docs, "size", n=100)
        assert len(result) == 5
        assert result[0]["size"] == 10

    def test_bottom_n_empty(self, stats):
        assert stats.bottom_n([], "size") == []


# ============================================================== TestPercentile


class TestPercentile:
    def test_percentile_50(self, stats, simple_docs):
        v = stats.percentile(simple_docs, "size", 50)
        assert v == 30.0

    def test_percentile_0(self, stats, simple_docs):
        v = stats.percentile(simple_docs, "size", 0)
        assert v == 10.0

    def test_percentile_100(self, stats, simple_docs):
        v = stats.percentile(simple_docs, "size", 100)
        assert v == 50.0

    def test_percentile_empty(self, stats):
        assert stats.percentile([], "x", 50) == 0.0

    def test_percentile_single(self, stats):
        assert stats.percentile([{"x": 42}], "x", 75) == 42.0

    def test_percentile_arbitrary(self, stats, simple_docs):
        v = stats.percentile(simple_docs, "size", 25)
        assert v == 20.0


# ============================================================== TestCorrelation


class TestCorrelation:
    def test_perfect_positive(self, stats):
        docs = [{"a": i, "b": 2 * i} for i in range(1, 6)]
        c = stats.correlation(docs, "a", "b")
        assert c == pytest.approx(1.0, abs=1e-9)

    def test_perfect_negative(self, stats):
        docs = [{"a": i, "b": -2 * i} for i in range(1, 6)]
        c = stats.correlation(docs, "a", "b")
        assert c == pytest.approx(-1.0, abs=1e-9)

    def test_no_correlation_constant(self, stats):
        docs = [{"a": i, "b": 5} for i in range(5)]
        # b is constant → variance 0 → return 0.0
        c = stats.correlation(docs, "a", "b")
        assert c == 0.0

    def test_empty(self, stats):
        assert stats.correlation([], "a", "b") == 0.0

    def test_single_pair(self, stats):
        # Need at least 2 pairs.
        c = stats.correlation([{"a": 1, "b": 2}], "a", "b")
        assert c == 0.0

    def test_skip_missing(self, stats):
        docs = [
            {"a": 1, "b": 2},
            {"a": 2},  # missing b
            {"a": 3, "b": 6},
            {"a": 4, "b": 8},
        ]
        c = stats.correlation(docs, "a", "b")
        assert c == pytest.approx(1.0, abs=1e-9)


# ============================================================== TestSummary


class TestSummary:
    def test_summary_basic(self, stats, simple_docs):
        s = stats.summary(simple_docs, "size")
        assert s["count"] == 5
        assert s["min"] == 10.0
        assert s["max"] == 50.0
        assert s["avg"] == 30.0
        assert s["median"] == 30.0
        assert s["stddev"] == pytest.approx(15.81, abs=0.01)

    def test_summary_empty(self, stats):
        s = stats.summary([], "size")
        assert s["count"] == 0
        assert s["min"] == 0.0
        assert s["max"] == 0.0
        assert s["stddev"] == 0.0

    def test_summary_single_value(self, stats):
        s = stats.summary([{"x": 7}], "x")
        assert s["count"] == 1
        assert s["min"] == 7.0
        assert s["max"] == 7.0
        assert s["stddev"] == 0.0


# ============================================================== TestExtractValues


class TestExtractValues:
    def test_extract_basic(self, stats, simple_docs):
        v = stats.extract_values(simple_docs, "size")
        assert v == [10.0, 20.0, 30.0, 40.0, 50.0]

    def test_extract_skip_missing(self, stats):
        docs = [{"x": 1}, {"y": 2}, {"x": 3}]
        v = stats.extract_values(docs, "x")
        assert v == [1.0, 3.0]

    def test_extract_skip_non_numeric(self, stats):
        docs = [{"x": 1}, {"x": "hello"}, {"x": None}, {"x": True}, {"x": 4}]
        v = stats.extract_values(docs, "x")
        # bool excluded as non-numeric
        assert v == [1.0, 4.0]

    def test_extract_empty(self, stats):
        assert stats.extract_values([], "x") == []

    def test_extract_skip_nan_inf(self, stats):
        docs = [{"x": 1.0}, {"x": float("nan")}, {"x": float("inf")}, {"x": 2.0}]
        v = stats.extract_values(docs, "x")
        assert v == [1.0, 2.0]


# ============================================================== TestDottedFields


class TestDottedFields:
    def test_dotted_extract(self, stats, nested_docs):
        v = stats.extract_values(nested_docs, "metadata.size")
        assert v == [100.0, 200.0, 300.0]

    def test_dotted_compute(self, stats, nested_docs):
        r = stats.compute(nested_docs, "metadata.size", MetricType.AVG)
        assert r.value == 200.0

    def test_dotted_missing_intermediate(self, stats):
        docs = [{"a": {"b": 1}}, {"a": 5}, {"x": 99}]
        v = stats.extract_values(docs, "a.b")
        assert v == [1.0]

    def test_dotted_group_by(self, stats):
        docs = [
            {"meta": {"cat": "x"}, "size": 1},
            {"meta": {"cat": "x"}, "size": 2},
            {"meta": {"cat": "y"}, "size": 3},
        ]
        groups = stats.group_by(docs, "meta.cat", ["size"])
        assert len(groups) == 2


# ============================================================== TestEdgeCases


class TestEdgeCases:
    def test_compute_non_numeric_field(self, stats):
        docs = [{"x": "abc"}, {"x": "def"}]
        r = stats.compute(docs, "x", MetricType.AVG)
        assert r.value == 0.0

    def test_stddev_single_value(self, stats):
        r = stats.compute([{"x": 5}], "x", MetricType.STDDEV)
        assert r.value == 0.0

    def test_compute_missing_field(self, stats, simple_docs):
        r = stats.compute(simple_docs, "nonexistent", MetricType.AVG)
        assert r.value == 0.0

    def test_doc_not_dict(self, stats):
        # extract_values must not crash on a list of non-dicts.
        v = stats.extract_values([None, 1, "str"], "x")
        assert v == []

    def test_distribution_with_outlier(self, stats):
        docs = [{"x": 1}, {"x": 2}, {"x": 3}, {"x": 1000}]
        d = stats.distribution(docs, "x", bins=4)
        assert sum(d.histogram.values()) == 4
        assert d.min_value == 1.0
        assert d.max_value == 1000.0
