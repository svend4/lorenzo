"""Tests for docstoolkit.sliding_window (E94)."""
import threading
import time
import pytest

from docstoolkit.sliding_window import (
    WindowType,
    WindowConfig,
    SlidingWindow,
    WindowAggregator,
    WindowedStatistics,
)


# ---------------------------------------------------------------------------
# WindowConfig & WindowType
# ---------------------------------------------------------------------------

class TestWindowConfig:
    def test_defaults(self):
        cfg = WindowConfig(size=10.0)
        assert cfg.window_type == WindowType.TIME
        assert cfg.size == 10.0

    def test_count_type(self):
        cfg = WindowConfig(size=5, window_type=WindowType.COUNT)
        assert cfg.window_type == WindowType.COUNT

    def test_window_type_values(self):
        assert WindowType.TIME == "time"
        assert WindowType.COUNT == "count"


# ---------------------------------------------------------------------------
# SlidingWindow — TIME
# ---------------------------------------------------------------------------

class TestSlidingWindowTime:
    def _make(self, size=10.0):
        return SlidingWindow(WindowConfig(size=size, window_type=WindowType.TIME))

    def test_empty_window(self):
        w = self._make()
        assert w.count() == 0
        assert w.sum() == 0.0
        assert w.avg() == 0.0
        assert w.min() is None
        assert w.max() is None
        assert w.values() == []

    def test_add_and_sum(self):
        w = self._make(size=60.0)
        t = 1000.0
        w.add(1.0, now=t)
        w.add(2.0, now=t + 1)
        w.add(3.0, now=t + 2)
        assert w.sum(now=t + 2) == 6.0

    def test_add_and_count(self):
        w = self._make(size=60.0)
        t = 1000.0
        for _ in range(5):
            w.add(1.0, now=t)
        assert w.count(now=t) == 5

    def test_avg(self):
        w = self._make(size=60.0)
        t = 1000.0
        w.add(2.0, now=t)
        w.add(4.0, now=t + 1)
        assert w.avg(now=t + 1) == pytest.approx(3.0)

    def test_min_max(self):
        w = self._make(size=60.0)
        t = 1000.0
        w.add(5.0, now=t)
        w.add(1.0, now=t + 1)
        w.add(9.0, now=t + 2)
        assert w.min(now=t + 2) == 1.0
        assert w.max(now=t + 2) == 9.0

    def test_eviction_on_add(self):
        w = self._make(size=5.0)
        t = 1000.0
        w.add(1.0, now=t)
        w.add(2.0, now=t + 6)  # item at t is now outside window
        assert w.count(now=t + 6) == 1
        assert w.sum(now=t + 6) == 2.0

    def test_eviction_on_query(self):
        w = self._make(size=3.0)
        t = 1000.0
        w.add(10.0, now=t)
        w.add(20.0, now=t + 1)
        # at t+4 both items are outside 3s window
        assert w.count(now=t + 4) == 0
        assert w.sum(now=t + 4) == 0.0

    def test_boundary_exactly_at_cutoff(self):
        """Item at exactly cutoff (t - size) should be evicted."""
        w = self._make(size=5.0)
        t = 1000.0
        w.add(1.0, now=t)
        # cutoff = (t+5) - 5 = t; item at t has ts <= cutoff → evicted
        assert w.count(now=t + 5) == 0

    def test_values_returns_list(self):
        w = self._make(size=60.0)
        t = 1000.0
        w.add(7.0, now=t)
        w.add(8.0, now=t + 1)
        vals = w.values(now=t + 1)
        assert isinstance(vals, list)
        assert len(vals) == 2
        assert vals[0] == (t, 7.0)
        assert vals[1] == (t + 1, 8.0)

    def test_clear(self):
        w = self._make(size=60.0)
        t = 1000.0
        w.add(1.0, now=t)
        w.clear()
        assert w.count(now=t) == 0

    def test_default_value_is_one(self):
        w = self._make(size=60.0)
        t = 1000.0
        w.add(now=t)
        assert w.sum(now=t) == 1.0

    def test_multiple_evictions(self):
        w = self._make(size=2.0)
        for i in range(10):
            w.add(float(i), now=float(i))
        # Only items with ts > 10 - 2 = 8, so ts=9 → value=9
        # ts=8 is at or before cutoff (10-2=8), so evicted
        assert w.count(now=10.0) == 1
        assert w.sum(now=10.0) == 9.0


# ---------------------------------------------------------------------------
# SlidingWindow — COUNT
# ---------------------------------------------------------------------------

class TestSlidingWindowCount:
    def _make(self, size=5):
        return SlidingWindow(WindowConfig(size=size, window_type=WindowType.COUNT))

    def test_empty_window(self):
        w = self._make()
        assert w.count() == 0
        assert w.sum() == 0.0
        assert w.min() is None
        assert w.max() is None

    def test_count_within_size(self):
        w = self._make(size=5)
        t = 1000.0
        for i in range(3):
            w.add(float(i), now=t + i)
        assert w.count(now=t + 2) == 3

    def test_count_exceeds_size(self):
        w = self._make(size=3)
        t = 1000.0
        for i in range(7):
            w.add(float(i), now=t + i)
        assert w.count(now=t + 6) == 3
        # Only last 3 values: 4, 5, 6
        assert w.sum(now=t + 6) == 15.0

    def test_exactly_at_size(self):
        w = self._make(size=4)
        t = 1000.0
        for i in range(4):
            w.add(float(i + 1), now=t + i)
        assert w.count(now=t + 3) == 4

    def test_one_over_size(self):
        w = self._make(size=2)
        t = 1000.0
        w.add(1.0, now=t)
        w.add(2.0, now=t + 1)
        w.add(3.0, now=t + 2)  # pushes out 1.0
        assert w.count(now=t + 2) == 2
        assert w.min(now=t + 2) == 2.0
        assert w.max(now=t + 2) == 3.0

    def test_size_one(self):
        w = self._make(size=1)
        t = 1000.0
        w.add(10.0, now=t)
        w.add(20.0, now=t + 1)
        assert w.count(now=t + 1) == 1
        assert w.sum(now=t + 1) == 20.0


# ---------------------------------------------------------------------------
# SlidingWindow — thread safety
# ---------------------------------------------------------------------------

class TestSlidingWindowThreadSafety:
    def test_concurrent_adds(self):
        w = SlidingWindow(WindowConfig(size=60.0))
        t = 1000.0
        errors = []

        def adder():
            try:
                for i in range(100):
                    w.add(1.0, now=t + i * 0.001)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=adder) for _ in range(5)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert not errors
        assert w.count(now=t + 1) == 500

    def test_concurrent_reads_and_writes(self):
        w = SlidingWindow(WindowConfig(size=60.0))
        errors = []
        stop_event = threading.Event()

        def writer():
            t = time.time()
            for i in range(50):
                w.add(float(i), now=t + i * 0.001)

        def reader():
            for _ in range(50):
                try:
                    _ = w.sum()
                    _ = w.count()
                except Exception as e:
                    errors.append(e)

        ts = [threading.Thread(target=writer)] + [threading.Thread(target=reader) for _ in range(3)]
        for th in ts:
            th.start()
        for th in ts:
            th.join()

        assert not errors


# ---------------------------------------------------------------------------
# WindowAggregator
# ---------------------------------------------------------------------------

class TestWindowAggregator:
    def test_invalid_window_size(self):
        with pytest.raises(ValueError):
            WindowAggregator(window_size=0)
        with pytest.raises(ValueError):
            WindowAggregator(window_size=-1.0)

    def test_invalid_bucket_count(self):
        with pytest.raises(ValueError):
            WindowAggregator(window_size=10.0, bucket_count=0)

    def test_empty_aggregator(self):
        agg = WindowAggregator(window_size=60.0, bucket_count=6)
        assert agg.total() == 0.0
        assert agg.count() == 0
        assert agg.rate() == pytest.approx(0.0)
        assert agg.buckets() == []

    def test_record_and_total(self):
        agg = WindowAggregator(window_size=60.0, bucket_count=6)
        t = 1000.0
        agg.record(1.0, now=t)
        agg.record(2.0, now=t + 1)
        agg.record(3.0, now=t + 2)
        assert agg.total(now=t + 2) == pytest.approx(6.0)

    def test_record_and_count(self):
        agg = WindowAggregator(window_size=60.0, bucket_count=6)
        t = 1000.0
        for _ in range(5):
            agg.record(now=t)
        assert agg.count(now=t) == 5

    def test_rate_calculation(self):
        agg = WindowAggregator(window_size=10.0, bucket_count=5)
        t = 1000.0
        for _ in range(10):
            agg.record(1.0, now=t)
        assert agg.rate(now=t) == pytest.approx(1.0)  # 10 events / 10s

    def test_eviction_of_old_buckets(self):
        agg = WindowAggregator(window_size=10.0, bucket_count=5)
        t = 1000.0
        agg.record(100.0, now=t)
        # At t+15 the bucket at t is expired
        agg.record(5.0, now=t + 11)
        assert agg.total(now=t + 11) == pytest.approx(5.0)

    def test_buckets_returns_tuples(self):
        agg = WindowAggregator(window_size=60.0, bucket_count=6)
        t = 1000.0
        agg.record(7.0, now=t)
        result = agg.buckets(now=t)
        assert len(result) == 1
        start, s, c = result[0]
        assert isinstance(start, float)
        assert s == pytest.approx(7.0)
        assert c == 1

    def test_multiple_events_same_bucket(self):
        agg = WindowAggregator(window_size=60.0, bucket_count=6)
        t = 1000.0
        # bucket_duration = 60/6 = 10s; all within same bucket
        for i in range(5):
            agg.record(2.0, now=t + i)
        result = agg.buckets(now=t + 4)
        assert len(result) == 1
        assert result[0][1] == pytest.approx(10.0)
        assert result[0][2] == 5

    def test_clear(self):
        agg = WindowAggregator(window_size=60.0, bucket_count=6)
        t = 1000.0
        agg.record(1.0, now=t)
        agg.clear()
        assert agg.total(now=t) == 0.0
        assert agg.count(now=t) == 0

    def test_properties(self):
        agg = WindowAggregator(window_size=30.0, bucket_count=3)
        assert agg.window_size == 30.0
        assert agg.bucket_count == 3

    def test_thread_safe_concurrent_records(self):
        agg = WindowAggregator(window_size=60.0, bucket_count=6)
        t = 1000.0
        errors = []

        def record_fn():
            try:
                for i in range(50):
                    agg.record(1.0, now=t + i * 0.01)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=record_fn) for _ in range(4)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert not errors
        assert agg.count(now=t + 1) == 200


# ---------------------------------------------------------------------------
# WindowedStatistics
# ---------------------------------------------------------------------------

class TestWindowedStatistics:
    def test_invalid_window_size(self):
        with pytest.raises(ValueError):
            WindowedStatistics(window_size=0.0)
        with pytest.raises(ValueError):
            WindowedStatistics(window_size=-5.0)

    def test_empty_mean(self):
        ws = WindowedStatistics(window_size=60.0)
        assert ws.mean() == 0.0

    def test_empty_stddev(self):
        ws = WindowedStatistics(window_size=60.0)
        assert ws.stddev() == 0.0

    def test_empty_percentile_raises(self):
        ws = WindowedStatistics(window_size=60.0)
        with pytest.raises(ValueError):
            ws.percentile(50.0)

    def test_percentile_out_of_range(self):
        ws = WindowedStatistics(window_size=60.0)
        t = 1000.0
        ws.record(1.0, now=t)
        with pytest.raises(ValueError):
            ws.percentile(-1.0, now=t)
        with pytest.raises(ValueError):
            ws.percentile(101.0, now=t)

    def test_single_value_percentile(self):
        ws = WindowedStatistics(window_size=60.0)
        t = 1000.0
        ws.record(42.0, now=t)
        assert ws.percentile(0.0, now=t) == pytest.approx(42.0)
        assert ws.percentile(50.0, now=t) == pytest.approx(42.0)
        assert ws.percentile(100.0, now=t) == pytest.approx(42.0)

    def test_mean(self):
        ws = WindowedStatistics(window_size=60.0)
        t = 1000.0
        ws.record(2.0, now=t)
        ws.record(4.0, now=t + 1)
        ws.record(6.0, now=t + 2)
        assert ws.mean(now=t + 2) == pytest.approx(4.0)

    def test_stddev(self):
        ws = WindowedStatistics(window_size=60.0)
        t = 1000.0
        for v in [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]:
            ws.record(v, now=t)
        sd = ws.stddev(now=t)
        assert sd == pytest.approx(2.0, abs=0.01)

    def test_stddev_single_value(self):
        ws = WindowedStatistics(window_size=60.0)
        t = 1000.0
        ws.record(5.0, now=t)
        assert ws.stddev(now=t) == 0.0

    def test_percentile_p0_p100(self):
        ws = WindowedStatistics(window_size=60.0)
        t = 1000.0
        for v in [1.0, 2.0, 3.0, 4.0, 5.0]:
            ws.record(v, now=t)
        assert ws.percentile(0.0, now=t) == pytest.approx(1.0)
        assert ws.percentile(100.0, now=t) == pytest.approx(5.0)

    def test_percentile_p50_odd(self):
        ws = WindowedStatistics(window_size=60.0)
        t = 1000.0
        for v in [1.0, 3.0, 5.0]:
            ws.record(v, now=t)
        assert ws.percentile(50.0, now=t) == pytest.approx(3.0)

    def test_percentile_p50_even(self):
        ws = WindowedStatistics(window_size=60.0)
        t = 1000.0
        for v in [1.0, 2.0, 3.0, 4.0]:
            ws.record(v, now=t)
        assert ws.percentile(50.0, now=t) == pytest.approx(2.5)

    def test_percentile_p95(self):
        ws = WindowedStatistics(window_size=60.0)
        t = 1000.0
        for v in range(1, 101):
            ws.record(float(v), now=t)
        p95 = ws.percentile(95.0, now=t)
        assert 94.0 <= p95 <= 96.0

    def test_summary_empty(self):
        ws = WindowedStatistics(window_size=60.0)
        s = ws.summary()
        assert s["count"] == 0
        assert s["mean"] == 0.0
        assert s["min"] is None
        assert s["max"] is None
        assert s["stddev"] == 0.0

    def test_summary_non_empty(self):
        ws = WindowedStatistics(window_size=60.0)
        t = 1000.0
        for v in [1.0, 2.0, 3.0, 4.0, 5.0]:
            ws.record(v, now=t)
        s = ws.summary(now=t)
        assert s["count"] == 5
        assert s["mean"] == pytest.approx(3.0)
        assert s["min"] == 1.0
        assert s["max"] == 5.0
        assert s["p50"] == pytest.approx(3.0)
        assert "p95" in s
        assert "p99" in s

    def test_eviction_in_stats(self):
        ws = WindowedStatistics(window_size=5.0)
        t = 1000.0
        ws.record(100.0, now=t)
        ws.record(1.0, now=t + 6)  # 100.0 now expired
        assert ws.mean(now=t + 6) == pytest.approx(1.0)
        assert ws.count_in_window(now=t + 6) == 1

    def test_count_in_window(self):
        ws = WindowedStatistics(window_size=60.0)
        t = 1000.0
        for _ in range(7):
            ws.record(1.0, now=t)
        assert ws.count_in_window(now=t) == 7
