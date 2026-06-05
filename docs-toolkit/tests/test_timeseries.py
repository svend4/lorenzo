"""Tests for docstoolkit.timeseries — SQLite-backed time series store.

Coverage targets (≥75 tests):
- DataPoint / AggregatedPoint dataclasses
- TimeSeriesStore: write, write_batch, read, aggregate, metrics, count, latest, cleanup
- Window aggregation for all Aggregation variants
- Tag filtering: exact, multi-tag, partial no-match
- Edge cases: empty store, no-data reads, cleanup with no retention, max_points
"""
from __future__ import annotations

import math
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.timeseries import (
    Aggregation,
    AggregatedPoint,
    DataPoint,
    TimeSeriesConfig,
    TimeSeriesStore,
)


# ===========================================================================
# Helpers
# ===========================================================================

def _store(retention: float = 0.0, max_points: int = 0) -> TimeSeriesStore:
    """Return an in-memory store with optional config."""
    cfg = TimeSeriesConfig(retention_seconds=retention, max_points=max_points)
    return TimeSeriesStore(config=cfg)


def _dp(ts: float, value: float, metric: str = "m", tags: dict | None = None) -> DataPoint:
    return DataPoint(ts=ts, value=value, metric=metric, tags=tags or {})


# ===========================================================================
# DataPoint dataclass
# ===========================================================================

class TestDataPoint:
    def test_fields_present(self):
        p = DataPoint(ts=1.0, value=2.0)
        assert p.ts == 1.0
        assert p.value == 2.0

    def test_default_tags_empty_dict(self):
        p = DataPoint(ts=1.0, value=2.0)
        assert p.tags == {}

    def test_default_metric_empty_string(self):
        p = DataPoint(ts=1.0, value=2.0)
        assert p.metric == ""

    def test_custom_tags(self):
        p = DataPoint(ts=1.0, value=2.0, tags={"host": "web1"})
        assert p.tags == {"host": "web1"}

    def test_custom_metric(self):
        p = DataPoint(ts=1.0, value=2.0, metric="cpu")
        assert p.metric == "cpu"

    def test_tags_not_shared_between_instances(self):
        p1 = DataPoint(ts=1.0, value=1.0)
        p2 = DataPoint(ts=2.0, value=2.0)
        p1.tags["k"] = "v"
        assert "k" not in p2.tags

    def test_ts_float(self):
        p = DataPoint(ts=1_700_000_000.123, value=0.0)
        assert p.ts == pytest.approx(1_700_000_000.123)

    def test_negative_value(self):
        p = DataPoint(ts=1.0, value=-99.5)
        assert p.value == -99.5

    def test_zero_value(self):
        p = DataPoint(ts=0.0, value=0.0)
        assert p.value == 0.0


# ===========================================================================
# AggregatedPoint dataclass
# ===========================================================================

class TestAggregatedPoint:
    def test_fields_present(self):
        ap = AggregatedPoint(ts=0.0, value=5.0, count=3)
        assert ap.ts == 0.0
        assert ap.value == 5.0
        assert ap.count == 3

    def test_default_metric(self):
        ap = AggregatedPoint(ts=0.0, value=0.0, count=1)
        assert ap.metric == ""

    def test_custom_metric(self):
        ap = AggregatedPoint(ts=0.0, value=0.0, count=1, metric="cpu")
        assert ap.metric == "cpu"

    def test_count_positive(self):
        ap = AggregatedPoint(ts=10.0, value=100.0, count=42)
        assert ap.count == 42

    def test_value_float(self):
        ap = AggregatedPoint(ts=0.0, value=3.14, count=1)
        assert ap.value == pytest.approx(3.14)


# ===========================================================================
# Aggregation enum
# ===========================================================================

class TestAggregationEnum:
    def test_all_variants_exist(self):
        assert Aggregation.MEAN
        assert Aggregation.SUM
        assert Aggregation.MIN
        assert Aggregation.MAX
        assert Aggregation.COUNT
        assert Aggregation.LAST

    def test_values_are_strings(self):
        for agg in Aggregation:
            assert isinstance(agg.value, str)

    def test_distinct_values(self):
        values = [a.value for a in Aggregation]
        assert len(values) == len(set(values))


# ===========================================================================
# TimeSeriesConfig
# ===========================================================================

class TestTimeSeriesConfig:
    def test_defaults(self):
        cfg = TimeSeriesConfig()
        assert cfg.retention_seconds == 0.0
        assert cfg.max_points == 0

    def test_custom_retention(self):
        cfg = TimeSeriesConfig(retention_seconds=3600.0)
        assert cfg.retention_seconds == 3600.0

    def test_custom_max_points(self):
        cfg = TimeSeriesConfig(max_points=100)
        assert cfg.max_points == 100


# ===========================================================================
# TimeSeriesStore — write / write_batch
# ===========================================================================

class TestWrite:
    def test_write_single(self):
        s = _store()
        s.write(_dp(1.0, 10.0))
        assert s.count("m") == 1
        s.close()

    def test_write_increments_count(self):
        s = _store()
        for i in range(5):
            s.write(_dp(float(i), float(i)))
        assert s.count("m") == 5
        s.close()

    def test_write_batch_empty(self):
        s = _store()
        s.write_batch([])
        assert s.count("m") == 0
        s.close()

    def test_write_batch_multiple(self):
        s = _store()
        points = [_dp(float(i), float(i)) for i in range(10)]
        s.write_batch(points)
        assert s.count("m") == 10
        s.close()

    def test_write_batch_single_transaction(self):
        """write_batch should store all or nothing (tested via count consistency)."""
        s = _store()
        s.write_batch([_dp(1.0, 1.0), _dp(2.0, 2.0), _dp(3.0, 3.0)])
        assert s.count("m") == 3
        s.close()

    def test_write_different_metrics(self):
        s = _store()
        s.write(_dp(1.0, 1.0, metric="a"))
        s.write(_dp(1.0, 2.0, metric="b"))
        assert s.count("a") == 1
        assert s.count("b") == 1
        s.close()

    def test_write_with_tags(self):
        s = _store()
        s.write(_dp(1.0, 5.0, tags={"env": "prod"}))
        pts = s.read("m")
        assert pts[0].tags == {"env": "prod"}
        s.close()

    def test_write_preserves_ts_precision(self):
        s = _store()
        ts = 1_700_000_000.999
        s.write(_dp(ts, 1.0))
        pts = s.read("m")
        assert pts[0].ts == pytest.approx(ts)
        s.close()


# ===========================================================================
# TimeSeriesStore — read
# ===========================================================================

class TestRead:
    def test_read_empty(self):
        s = _store()
        assert s.read("m") == []
        s.close()

    def test_read_returns_all_points(self):
        s = _store()
        s.write_batch([_dp(1.0, 1.0), _dp(2.0, 2.0), _dp(3.0, 3.0)])
        pts = s.read("m")
        assert len(pts) == 3
        s.close()

    def test_read_sorted_by_ts_asc(self):
        s = _store()
        s.write_batch([_dp(3.0, 3.0), _dp(1.0, 1.0), _dp(2.0, 2.0)])
        pts = s.read("m")
        assert [p.ts for p in pts] == [1.0, 2.0, 3.0]
        s.close()

    def test_read_since(self):
        s = _store()
        s.write_batch([_dp(1.0, 1.0), _dp(2.0, 2.0), _dp(3.0, 3.0)])
        pts = s.read("m", since=2.0)
        assert len(pts) == 2
        assert pts[0].ts == 2.0
        s.close()

    def test_read_until(self):
        s = _store()
        s.write_batch([_dp(1.0, 1.0), _dp(2.0, 2.0), _dp(3.0, 3.0)])
        pts = s.read("m", until=2.0)
        assert len(pts) == 2
        assert pts[-1].ts == 2.0
        s.close()

    def test_read_since_and_until(self):
        s = _store()
        s.write_batch([_dp(float(i), float(i)) for i in range(10)])
        pts = s.read("m", since=3.0, until=6.0)
        assert len(pts) == 4
        assert pts[0].ts == 3.0
        assert pts[-1].ts == 6.0
        s.close()

    def test_read_since_exclusive_below(self):
        s = _store()
        s.write_batch([_dp(1.0, 1.0), _dp(2.0, 2.0)])
        pts = s.read("m", since=1.5)
        assert len(pts) == 1
        assert pts[0].ts == 2.0
        s.close()

    def test_read_wrong_metric_empty(self):
        s = _store()
        s.write(_dp(1.0, 1.0, metric="a"))
        assert s.read("b") == []
        s.close()

    def test_read_returns_datapoints(self):
        s = _store()
        s.write(_dp(1.0, 42.0))
        pts = s.read("m")
        assert isinstance(pts[0], DataPoint)
        s.close()

    def test_read_metric_field_set(self):
        s = _store()
        s.write(_dp(1.0, 1.0, metric="cpu"))
        pts = s.read("cpu")
        assert pts[0].metric == "cpu"
        s.close()


# ===========================================================================
# TimeSeriesStore — tag filtering
# ===========================================================================

class TestTagFiltering:
    def test_single_tag_match(self):
        s = _store()
        s.write(_dp(1.0, 1.0, tags={"host": "web1"}))
        s.write(_dp(2.0, 2.0, tags={"host": "web2"}))
        pts = s.read("m", tags={"host": "web1"})
        assert len(pts) == 1
        assert pts[0].value == 1.0
        s.close()

    def test_single_tag_no_match(self):
        s = _store()
        s.write(_dp(1.0, 1.0, tags={"host": "web1"}))
        pts = s.read("m", tags={"host": "db1"})
        assert pts == []
        s.close()

    def test_multi_tag_all_match(self):
        s = _store()
        s.write(_dp(1.0, 1.0, tags={"host": "web1", "env": "prod"}))
        s.write(_dp(2.0, 2.0, tags={"host": "web1", "env": "dev"}))
        pts = s.read("m", tags={"host": "web1", "env": "prod"})
        assert len(pts) == 1
        assert pts[0].value == 1.0
        s.close()

    def test_multi_tag_partial_no_match(self):
        s = _store()
        s.write(_dp(1.0, 1.0, tags={"host": "web1", "env": "prod"}))
        pts = s.read("m", tags={"host": "web1", "env": "staging"})
        assert pts == []
        s.close()

    def test_no_tags_filter_returns_all(self):
        s = _store()
        s.write(_dp(1.0, 1.0, tags={"host": "web1"}))
        s.write(_dp(2.0, 2.0, tags={"host": "web2"}))
        pts = s.read("m")
        assert len(pts) == 2
        s.close()

    def test_tag_filter_combined_with_since(self):
        s = _store()
        s.write(_dp(1.0, 1.0, tags={"env": "prod"}))
        s.write(_dp(2.0, 2.0, tags={"env": "prod"}))
        s.write(_dp(3.0, 3.0, tags={"env": "dev"}))
        pts = s.read("m", since=1.5, tags={"env": "prod"})
        assert len(pts) == 1
        assert pts[0].ts == 2.0
        s.close()

    def test_empty_tags_filter_returns_all(self):
        s = _store()
        s.write(_dp(1.0, 1.0, tags={"k": "v"}))
        s.write(_dp(2.0, 2.0))
        pts = s.read("m", tags={})
        assert len(pts) == 2
        s.close()


# ===========================================================================
# TimeSeriesStore — aggregate
# ===========================================================================

class TestAggregate:
    def test_aggregate_empty(self):
        s = _store()
        result = s.aggregate("m", Aggregation.MEAN, 60.0)
        assert result == []
        s.close()

    def test_aggregate_mean_single_window(self):
        s = _store()
        s.write_batch([_dp(0.0, 10.0), _dp(30.0, 20.0), _dp(59.0, 30.0)])
        result = s.aggregate("m", Aggregation.MEAN, 60.0)
        assert len(result) == 1
        assert result[0].value == pytest.approx(20.0)
        assert result[0].count == 3
        s.close()

    def test_aggregate_sum_single_window(self):
        s = _store()
        s.write_batch([_dp(0.0, 1.0), _dp(1.0, 2.0), _dp(2.0, 3.0)])
        result = s.aggregate("m", Aggregation.SUM, 60.0)
        assert len(result) == 1
        assert result[0].value == pytest.approx(6.0)
        s.close()

    def test_aggregate_min_single_window(self):
        s = _store()
        s.write_batch([_dp(0.0, 5.0), _dp(1.0, 1.0), _dp(2.0, 3.0)])
        result = s.aggregate("m", Aggregation.MIN, 60.0)
        assert result[0].value == pytest.approx(1.0)
        s.close()

    def test_aggregate_max_single_window(self):
        s = _store()
        s.write_batch([_dp(0.0, 5.0), _dp(1.0, 100.0), _dp(2.0, 3.0)])
        result = s.aggregate("m", Aggregation.MAX, 60.0)
        assert result[0].value == pytest.approx(100.0)
        s.close()

    def test_aggregate_count_single_window(self):
        s = _store()
        s.write_batch([_dp(float(i), float(i)) for i in range(7)])
        result = s.aggregate("m", Aggregation.COUNT, 60.0)
        assert result[0].value == pytest.approx(7.0)
        assert result[0].count == 7
        s.close()

    def test_aggregate_last_single_window(self):
        s = _store()
        s.write_batch([_dp(0.0, 10.0), _dp(1.0, 20.0), _dp(2.0, 30.0)])
        result = s.aggregate("m", Aggregation.LAST, 60.0)
        assert result[0].value == pytest.approx(30.0)
        s.close()

    def test_aggregate_multiple_windows(self):
        s = _store()
        # window 0: ts 0, 30, 59  — window 60: ts 60, 90
        s.write_batch([
            _dp(0.0, 1.0), _dp(30.0, 2.0), _dp(59.0, 3.0),
            _dp(60.0, 4.0), _dp(90.0, 5.0),
        ])
        result = s.aggregate("m", Aggregation.MEAN, 60.0)
        assert len(result) == 2
        # window starts
        assert result[0].ts == pytest.approx(0.0)
        assert result[1].ts == pytest.approx(60.0)
        s.close()

    def test_aggregate_window_counts(self):
        s = _store()
        s.write_batch([_dp(0.0, 1.0), _dp(10.0, 2.0), _dp(60.0, 3.0)])
        result = s.aggregate("m", Aggregation.SUM, 60.0)
        assert result[0].count == 2
        assert result[1].count == 1
        s.close()

    def test_aggregate_sorted_by_window_ts(self):
        s = _store()
        s.write_batch([_dp(120.0, 1.0), _dp(0.0, 2.0), _dp(60.0, 3.0)])
        result = s.aggregate("m", Aggregation.COUNT, 60.0)
        assert [r.ts for r in result] == [0.0, 60.0, 120.0]
        s.close()

    def test_aggregate_metric_field_set(self):
        s = _store()
        s.write(_dp(0.0, 1.0, metric="cpu"))
        result = s.aggregate("cpu", Aggregation.MEAN, 60.0)
        assert result[0].metric == "cpu"
        s.close()

    def test_aggregate_with_since_filter(self):
        s = _store()
        s.write_batch([_dp(0.0, 100.0), _dp(60.0, 5.0), _dp(120.0, 5.0)])
        result = s.aggregate("m", Aggregation.SUM, 60.0, since=60.0)
        assert len(result) == 2
        assert result[0].ts == pytest.approx(60.0)
        s.close()

    def test_aggregate_with_until_filter(self):
        s = _store()
        s.write_batch([_dp(0.0, 5.0), _dp(60.0, 5.0), _dp(120.0, 100.0)])
        result = s.aggregate("m", Aggregation.SUM, 60.0, until=119.0)
        assert len(result) == 2
        assert result[-1].ts == pytest.approx(60.0)
        s.close()

    def test_aggregate_window_floor_alignment(self):
        s = _store()
        # window_seconds=10: ts=5 → bucket 0, ts=15 → bucket 10, ts=25 → bucket 20
        s.write_batch([_dp(5.0, 1.0), _dp(15.0, 2.0), _dp(25.0, 3.0)])
        result = s.aggregate("m", Aggregation.LAST, 10.0)
        assert len(result) == 3
        assert result[0].ts == pytest.approx(0.0)
        assert result[1].ts == pytest.approx(10.0)
        assert result[2].ts == pytest.approx(20.0)
        s.close()

    def test_aggregate_invalid_window_raises(self):
        s = _store()
        with pytest.raises(ValueError):
            s.aggregate("m", Aggregation.MEAN, 0.0)
        s.close()

    def test_aggregate_mean_two_values(self):
        s = _store()
        s.write_batch([_dp(0.0, 10.0), _dp(1.0, 20.0)])
        result = s.aggregate("m", Aggregation.MEAN, 60.0)
        assert result[0].value == pytest.approx(15.0)
        s.close()

    def test_aggregate_last_is_highest_ts_in_window(self):
        s = _store()
        # Insert in non-ts order — store orders by ts, so last in window = highest ts
        s.write_batch([_dp(50.0, 999.0), _dp(10.0, 1.0), _dp(40.0, 2.0)])
        result = s.aggregate("m", Aggregation.LAST, 60.0)
        assert result[0].value == pytest.approx(999.0)
        s.close()

    def test_aggregate_negative_values_min(self):
        s = _store()
        s.write_batch([_dp(0.0, -5.0), _dp(1.0, -10.0), _dp(2.0, -1.0)])
        result = s.aggregate("m", Aggregation.MIN, 60.0)
        assert result[0].value == pytest.approx(-10.0)
        s.close()


# ===========================================================================
# TimeSeriesStore — metrics / count / latest
# ===========================================================================

class TestMetricsCountLatest:
    def test_metrics_empty(self):
        s = _store()
        assert s.metrics() == []
        s.close()

    def test_metrics_single(self):
        s = _store()
        s.write(_dp(1.0, 1.0, metric="cpu"))
        assert s.metrics() == ["cpu"]
        s.close()

    def test_metrics_multiple_distinct(self):
        s = _store()
        s.write(_dp(1.0, 1.0, metric="cpu"))
        s.write(_dp(1.0, 2.0, metric="mem"))
        s.write(_dp(2.0, 3.0, metric="cpu"))
        assert sorted(s.metrics()) == ["cpu", "mem"]
        s.close()

    def test_metrics_sorted(self):
        s = _store()
        for name in ["z_metric", "a_metric", "m_metric"]:
            s.write(_dp(1.0, 1.0, metric=name))
        names = s.metrics()
        assert names == sorted(names)
        s.close()

    def test_count_empty(self):
        s = _store()
        assert s.count("m") == 0
        s.close()

    def test_count_after_writes(self):
        s = _store()
        s.write_batch([_dp(float(i), float(i)) for i in range(7)])
        assert s.count("m") == 7
        s.close()

    def test_count_specific_metric(self):
        s = _store()
        s.write_batch([_dp(1.0, 1.0, metric="a"), _dp(2.0, 2.0, metric="b")])
        assert s.count("a") == 1
        assert s.count("b") == 1
        s.close()

    def test_latest_empty(self):
        s = _store()
        assert s.latest("m") is None
        s.close()

    def test_latest_single(self):
        s = _store()
        s.write(_dp(42.0, 99.0))
        p = s.latest("m")
        assert p is not None
        assert p.ts == pytest.approx(42.0)
        assert p.value == pytest.approx(99.0)
        s.close()

    def test_latest_returns_highest_ts(self):
        s = _store()
        s.write_batch([_dp(1.0, 1.0), _dp(100.0, 100.0), _dp(50.0, 50.0)])
        p = s.latest("m")
        assert p.ts == pytest.approx(100.0)
        s.close()

    def test_latest_returns_datapoint_type(self):
        s = _store()
        s.write(_dp(1.0, 1.0))
        p = s.latest("m")
        assert isinstance(p, DataPoint)
        s.close()

    def test_latest_wrong_metric_none(self):
        s = _store()
        s.write(_dp(1.0, 1.0, metric="a"))
        assert s.latest("b") is None
        s.close()

    def test_latest_preserves_tags(self):
        s = _store()
        s.write(_dp(1.0, 1.0, tags={"region": "eu"}))
        p = s.latest("m")
        assert p.tags == {"region": "eu"}
        s.close()


# ===========================================================================
# TimeSeriesStore — cleanup / retention
# ===========================================================================

class TestCleanup:
    def test_cleanup_no_retention_returns_zero(self):
        s = _store(retention=0.0)
        s.write_batch([_dp(float(i), float(i)) for i in range(5)])
        deleted = s.cleanup(now=1_000_000.0)
        assert deleted == 0
        assert s.count("m") == 5
        s.close()

    def test_cleanup_removes_old_points(self):
        s = _store(retention=60.0)
        # Points at ts=0..4 (old) and ts=1000..1004 (recent)
        old = [_dp(float(i), float(i)) for i in range(5)]
        recent = [_dp(1000.0 + i, float(i)) for i in range(5)]
        s.write_batch(old + recent)
        deleted = s.cleanup(now=1059.0)   # cutoff = 1059 - 60 = 999 → keeps 1000..1004
        assert deleted == 5
        assert s.count("m") == 5
        s.close()

    def test_cleanup_returns_deleted_count(self):
        s = _store(retention=100.0)
        s.write_batch([_dp(float(i), float(i)) for i in range(10)])
        deleted = s.cleanup(now=200.0)   # cutoff=100 → ts<100 → removes ts 0..99 (all 10)
        assert deleted == 10
        s.close()

    def test_cleanup_nothing_old(self):
        s = _store(retention=3600.0)
        now = time.time()
        s.write(_dp(now, 1.0))
        deleted = s.cleanup(now=now)
        assert deleted == 0
        s.close()

    def test_cleanup_uses_default_now(self):
        s = _store(retention=1.0)
        # Write a very old point
        s.write(_dp(0.0, 1.0))
        deleted = s.cleanup()   # now defaults to time.time()
        assert deleted == 1
        s.close()

    def test_cleanup_boundary_exactly_at_cutoff(self):
        """Points exactly at cutoff ts are NOT deleted (ts >= cutoff kept)."""
        s = _store(retention=60.0)
        s.write(_dp(940.0, 1.0))   # cutoff = 1000-60 = 940 → ts 940 NOT deleted (ts < 940 is deleted)
        s.write(_dp(939.9, 2.0))   # ts < 940 → deleted
        deleted = s.cleanup(now=1000.0)
        assert deleted == 1
        assert s.count("m") == 1
        s.close()

    def test_cleanup_multiple_metrics(self):
        s = _store(retention=50.0)
        s.write(_dp(0.0, 1.0, metric="a"))
        s.write(_dp(0.0, 2.0, metric="b"))
        s.write(_dp(100.0, 3.0, metric="a"))
        deleted = s.cleanup(now=100.0)
        # cutoff = 50 → removes ts=0 for both a and b
        assert deleted == 2
        assert s.count("a") == 1
        assert s.count("b") == 0
        s.close()


# ===========================================================================
# TimeSeriesStore — max_points enforcement
# ===========================================================================

class TestMaxPoints:
    def test_max_points_enforced_on_write(self):
        s = _store(max_points=3)
        for i in range(5):
            s.write(_dp(float(i), float(i)))
        assert s.count("m") == 3
        s.close()

    def test_max_points_keeps_newest(self):
        s = _store(max_points=3)
        for i in range(5):
            s.write(_dp(float(i), float(i)))
        pts = s.read("m")
        ts_values = [p.ts for p in pts]
        assert max(ts_values) == pytest.approx(4.0)
        s.close()

    def test_max_points_zero_unlimited(self):
        s = _store(max_points=0)
        for i in range(20):
            s.write(_dp(float(i), float(i)))
        assert s.count("m") == 20
        s.close()

    def test_max_points_on_write_batch(self):
        s = _store(max_points=5)
        s.write_batch([_dp(float(i), float(i)) for i in range(10)])
        assert s.count("m") == 5
        s.close()

    def test_max_points_per_metric_independent(self):
        s = _store(max_points=2)
        s.write_batch([
            _dp(1.0, 1.0, metric="a"),
            _dp(2.0, 2.0, metric="a"),
            _dp(3.0, 3.0, metric="a"),
            _dp(1.0, 1.0, metric="b"),
        ])
        assert s.count("a") == 2
        assert s.count("b") == 1
        s.close()


# ===========================================================================
# TimeSeriesStore — persistence (file-backed)
# ===========================================================================

class TestFilePersistence:
    def test_persist_and_reload(self, tmp_path):
        db_file = tmp_path / "ts.db"
        s1 = TimeSeriesStore(db_path=db_file)
        s1.write(_dp(1.0, 42.0, metric="cpu"))
        s1.close()

        s2 = TimeSeriesStore(db_path=db_file)
        pts = s2.read("cpu")
        s2.close()

        assert len(pts) == 1
        assert pts[0].value == pytest.approx(42.0)

    def test_persist_path_object(self, tmp_path):
        db_file = tmp_path / "ts2.db"
        s = TimeSeriesStore(db_path=Path(db_file))
        s.write(_dp(1.0, 1.0))
        s.close()
        assert db_file.exists()


# ===========================================================================
# TimeSeriesStore — default config
# ===========================================================================

class TestDefaultConfig:
    def test_no_config_creates_store(self):
        s = TimeSeriesStore()
        s.write(_dp(1.0, 1.0))
        assert s.count("m") == 1
        s.close()

    def test_none_config_uses_defaults(self):
        s = TimeSeriesStore(config=None)
        s.write(_dp(1.0, 1.0))
        deleted = s.cleanup(now=1_000_000_000.0)
        assert deleted == 0   # no retention
        s.close()
