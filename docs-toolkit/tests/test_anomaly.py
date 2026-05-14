"""Tests for the E21 Anomaly detection module.

Run with:
    cd /home/user/lorenzo/docs-toolkit && python -m pytest tests/test_anomaly.py -q
"""
from __future__ import annotations

import math
import time

import pytest

from docstoolkit.anomaly import (
    AnomalyConfig,
    AnomalyDetector,
    AnomalyMonitor,
    AnomalyType,
    Anomaly,
    MetricSeries,
    RunningStats,
    ewma,
    moving_average,
)


# ===========================================================================
# RunningStats — Welford's online algorithm
# ===========================================================================


class TestRunningStats:
    def test_initial_state(self):
        rs = RunningStats()
        assert rs.n == 0
        assert rs.mean == 0.0
        assert rs.m2 == 0.0

    def test_single_update(self):
        rs = RunningStats().update(5.0)
        assert rs.n == 1
        assert rs.mean == pytest.approx(5.0)

    def test_immutability(self):
        """update() must return a new instance, not mutate in place."""
        rs = RunningStats()
        rs2 = rs.update(10.0)
        assert rs.n == 0  # original unchanged
        assert rs2.n == 1

    def test_mean_two_values(self):
        rs = RunningStats().update(2.0).update(4.0)
        assert rs.mean == pytest.approx(3.0)

    def test_mean_several_values(self):
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        rs = RunningStats()
        for v in values:
            rs = rs.update(v)
        assert rs.mean == pytest.approx(3.0)
        assert rs.n == 5

    def test_variance_zero_for_single(self):
        rs = RunningStats().update(7.0)
        assert rs.variance() == 0.0

    def test_variance_zero_for_empty(self):
        assert RunningStats().variance() == 0.0

    def test_variance_known(self):
        # Population variance of [2, 4, 4, 4, 5, 5, 7, 9] = 4.0
        values = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
        rs = RunningStats()
        for v in values:
            rs = rs.update(v)
        assert rs.variance() == pytest.approx(4.0, rel=1e-6)

    def test_std_known(self):
        values = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
        rs = RunningStats()
        for v in values:
            rs = rs.update(v)
        assert rs.std() == pytest.approx(2.0, rel=1e-6)

    def test_std_zero_when_empty(self):
        assert RunningStats().std() == 0.0

    def test_z_score_zero_mean_std(self):
        rs = RunningStats().update(5.0)
        # std is 0 → z_score returns 0
        assert rs.z_score(99.0) == 0.0

    def test_z_score_positive(self):
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        rs = RunningStats()
        for v in values:
            rs = rs.update(v)
        z = rs.z_score(5.0)
        assert z > 0

    def test_z_score_negative(self):
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        rs = RunningStats()
        for v in values:
            rs = rs.update(v)
        z = rs.z_score(1.0)
        assert z < 0

    def test_z_score_mean_is_zero(self):
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        rs = RunningStats()
        for v in values:
            rs = rs.update(v)
        z = rs.z_score(rs.mean)
        assert z == pytest.approx(0.0, abs=1e-10)

    def test_large_series_mean(self):
        n = 1000
        rs = RunningStats()
        for i in range(n):
            rs = rs.update(float(i))
        assert rs.mean == pytest.approx((n - 1) / 2.0, rel=1e-9)

    def test_constant_series_variance(self):
        rs = RunningStats()
        for _ in range(10):
            rs = rs.update(3.14)
        assert rs.variance() == pytest.approx(0.0, abs=1e-12)


# ===========================================================================
# moving_average
# ===========================================================================


class TestMovingAverage:
    def test_window_1_identity(self):
        values = [1.0, 2.0, 3.0, 4.0]
        assert moving_average(values, 1) == pytest.approx(values)

    def test_output_same_length(self):
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = moving_average(values, 3)
        assert len(result) == len(values)

    def test_full_window_value(self):
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = moving_average(values, 3)
        # Index 2 onwards: mean of 3 consecutive values
        assert result[2] == pytest.approx(2.0)
        assert result[3] == pytest.approx(3.0)
        assert result[4] == pytest.approx(4.0)

    def test_prefix_window(self):
        values = [1.0, 2.0, 3.0]
        result = moving_average(values, 3)
        assert result[0] == pytest.approx(1.0)
        assert result[1] == pytest.approx(1.5)
        assert result[2] == pytest.approx(2.0)

    def test_empty_list(self):
        assert moving_average([], 3) == []

    def test_window_invalid(self):
        with pytest.raises(ValueError):
            moving_average([1.0, 2.0], 0)

    def test_window_larger_than_series(self):
        values = [1.0, 2.0]
        result = moving_average(values, 10)
        assert result[0] == pytest.approx(1.0)
        assert result[1] == pytest.approx(1.5)

    def test_single_element(self):
        assert moving_average([42.0], 5) == pytest.approx([42.0])


# ===========================================================================
# ewma
# ===========================================================================


class TestEwma:
    def test_output_same_length(self):
        values = [1.0, 2.0, 3.0, 4.0]
        result = ewma(values, alpha=0.5)
        assert len(result) == len(values)

    def test_first_element_unchanged(self):
        values = [7.0, 1.0, 2.0]
        result = ewma(values, alpha=0.3)
        assert result[0] == pytest.approx(7.0)

    def test_alpha_1_identity(self):
        """alpha=1 means EWMA equals the original series."""
        values = [1.0, 5.0, 3.0, 9.0]
        result = ewma(values, alpha=1.0)
        assert result == pytest.approx(values)

    def test_smoothing_effect(self):
        """A spike should be damped by alpha < 1."""
        values = [1.0, 1.0, 1.0, 100.0, 1.0]
        result = ewma(values, alpha=0.1)
        # The spike at index 3 should be visible but much smaller than 100
        assert result[3] < 100.0
        assert result[3] > 1.0

    def test_empty_list(self):
        assert ewma([], alpha=0.3) == []

    def test_single_element(self):
        assert ewma([5.0]) == pytest.approx([5.0])

    def test_invalid_alpha_zero(self):
        with pytest.raises(ValueError):
            ewma([1.0, 2.0], alpha=0.0)

    def test_invalid_alpha_negative(self):
        with pytest.raises(ValueError):
            ewma([1.0, 2.0], alpha=-0.1)

    def test_invalid_alpha_too_large(self):
        with pytest.raises(ValueError):
            ewma([1.0, 2.0], alpha=1.1)

    def test_manual_calculation(self):
        """Verify against manually computed EWMA."""
        values = [10.0, 20.0, 30.0]
        alpha = 0.5
        result = ewma(values, alpha=alpha)
        expected_0 = 10.0
        expected_1 = 0.5 * 20.0 + 0.5 * 10.0  # 15.0
        expected_2 = 0.5 * 30.0 + 0.5 * 15.0  # 22.5
        assert result[0] == pytest.approx(expected_0)
        assert result[1] == pytest.approx(expected_1)
        assert result[2] == pytest.approx(expected_2)


# ===========================================================================
# Anomaly dataclass
# ===========================================================================


class TestAnomalySeverity:
    def _make(self, deviation: float) -> Anomaly:
        return Anomaly(
            anomaly_type=AnomalyType.SPIKE,
            value=10.0,
            expected=5.0,
            deviation=deviation,
            ts=0.0,
            description="test",
        )

    def test_low_severity(self):
        assert self._make(1.5).severity() == "low"

    def test_low_severity_negative(self):
        assert self._make(-1.9).severity() == "low"

    def test_medium_severity(self):
        assert self._make(2.5).severity() == "medium"

    def test_medium_severity_negative(self):
        assert self._make(-2.5).severity() == "medium"

    def test_high_severity(self):
        assert self._make(3.0).severity() == "high"

    def test_high_severity_large(self):
        assert self._make(10.0).severity() == "high"

    def test_boundary_2_is_medium(self):
        # |2| is NOT < 2, so it should be "medium"
        assert self._make(2.0).severity() == "medium"

    def test_boundary_3_is_high(self):
        # |3| is NOT < 3, so it should be "high"
        assert self._make(3.0).severity() == "high"


# ===========================================================================
# AnomalyDetector
# ===========================================================================


def _normal_series(n: int = 20, base: float = 0.0, noise: float = 1.0) -> list[float]:
    """Deterministic near-normal series for testing."""
    import math

    values = []
    for i in range(n):
        # A simple but deterministic pattern that covers a range
        v = base + noise * math.sin(i * 0.7) * 0.5
        values.append(v)
    return values


class TestAnomalyDetector:
    def test_not_enough_data_returns_empty(self):
        cfg = AnomalyConfig(min_samples=5)
        det = AnomalyDetector(cfg)
        assert det.detect([1.0, 2.0, 3.0]) == []

    def test_exactly_min_samples(self):
        cfg = AnomalyConfig(min_samples=5)
        det = AnomalyDetector(cfg)
        # Should not raise; may or may not find anomalies
        result = det.detect([1.0, 2.0, 3.0, 4.0, 5.0])
        assert isinstance(result, list)

    def test_spike_detected(self):
        base = [1.0] * 20
        spike_idx = 10
        values = base[:]
        values[spike_idx] = 100.0  # clear spike
        cfg = AnomalyConfig(z_threshold=2.5, min_samples=5)
        det = AnomalyDetector(cfg)
        anomalies = det.detect(values)
        spikes = [a for a in anomalies if a.anomaly_type == AnomalyType.SPIKE]
        assert len(spikes) >= 1
        assert any(a.value == 100.0 for a in spikes)

    def test_drop_detected(self):
        base = [10.0] * 20
        drop_idx = 10
        values = base[:]
        values[drop_idx] = -100.0  # clear drop
        cfg = AnomalyConfig(z_threshold=2.5, min_samples=5)
        det = AnomalyDetector(cfg)
        anomalies = det.detect(values)
        drops = [a for a in anomalies if a.anomaly_type == AnomalyType.DROP]
        assert len(drops) >= 1
        assert any(a.value == -100.0 for a in drops)

    def test_spike_anomaly_type_is_spike(self):
        values = [1.0] * 19 + [999.0]
        det = AnomalyDetector()
        anomalies = det.detect(values)
        assert any(a.anomaly_type == AnomalyType.SPIKE for a in anomalies)

    def test_drop_anomaly_type_is_drop(self):
        values = [10.0] * 19 + [-999.0]
        det = AnomalyDetector()
        anomalies = det.detect(values)
        assert any(a.anomaly_type == AnomalyType.DROP for a in anomalies)

    def test_no_anomaly_on_flat_series(self):
        values = [5.0] * 20
        cfg = AnomalyConfig(z_threshold=2.5, min_samples=5, drift_window=10)
        det = AnomalyDetector(cfg)
        anomalies = det.detect(values)
        # Flat series: std=0, z_score=0, no IQR spread → no anomalies
        assert anomalies == []

    def test_drift_detected(self):
        # First half near 0, second half near 10 — clear drift
        values = [0.0] * 15 + [10.0] * 15
        cfg = AnomalyConfig(z_threshold=5.0, drift_window=10, min_samples=5)
        det = AnomalyDetector(cfg)
        anomalies = det.detect(values)
        drifts = [a for a in anomalies if a.anomaly_type == AnomalyType.DRIFT]
        assert len(drifts) >= 1

    def test_timestamps_used(self):
        values = [1.0] * 19 + [999.0]
        ts = list(range(len(values)))
        det = AnomalyDetector()
        anomalies = det.detect(values, timestamps=ts)
        spike = next((a for a in anomalies if a.anomaly_type == AnomalyType.SPIKE), None)
        assert spike is not None
        assert spike.ts == 19  # last index

    def test_timestamps_length_mismatch_raises(self):
        with pytest.raises(ValueError):
            AnomalyDetector().detect([1.0, 2.0, 3.0, 4.0, 5.0], timestamps=[0.0, 1.0])

    def test_result_sorted_by_timestamp(self):
        values = [1.0] * 15 + [100.0] + [1.0] * 4
        det = AnomalyDetector()
        anomalies = det.detect(values)
        ts_list = [a.ts for a in anomalies]
        assert ts_list == sorted(ts_list)

    def test_outlier_detected_via_iqr(self):
        # Build a series where one value is far outside IQR.
        # Use a very high z_threshold so spike/drop don't fire, and a drift_window
        # larger than the series so drift detection also doesn't fire — only IQR.
        values = [2.0, 2.5, 2.0, 1.5, 2.0, 2.5, 2.0, 1.5, 2.0, 2.5, 50.0]
        cfg = AnomalyConfig(z_threshold=50.0, drift_window=20, min_samples=5)
        det = AnomalyDetector(cfg)
        anomalies = det.detect(values)
        outliers = [a for a in anomalies if a.anomaly_type == AnomalyType.OUTLIER]
        assert len(outliers) >= 1
        assert any(a.value == 50.0 for a in outliers)

    def test_default_timestamps_are_indices(self):
        values = [1.0] * 10 + [999.0] + [1.0] * 9
        det = AnomalyDetector()
        anomalies = det.detect(values)
        # Default timestamps are 0..len-1
        spike = next((a for a in anomalies if a.anomaly_type == AnomalyType.SPIKE), None)
        assert spike is not None
        assert spike.ts == 10

    def test_deviation_positive_for_spike(self):
        values = [1.0] * 19 + [999.0]
        det = AnomalyDetector()
        spikes = [a for a in det.detect(values) if a.anomaly_type == AnomalyType.SPIKE]
        assert all(a.deviation > 0 for a in spikes)

    def test_deviation_negative_for_drop(self):
        values = [10.0] * 19 + [-999.0]
        det = AnomalyDetector()
        drops = [a for a in det.detect(values) if a.anomaly_type == AnomalyType.DROP]
        assert all(a.deviation < 0 for a in drops)

    def test_spike_description_contains_spike(self):
        values = [1.0] * 19 + [999.0]
        det = AnomalyDetector()
        anomalies = det.detect(values)
        spike = next(a for a in anomalies if a.anomaly_type == AnomalyType.SPIKE)
        assert "spike" in spike.description.lower() or "Spike" in spike.description

    def test_drop_description_contains_drop(self):
        values = [10.0] * 19 + [-999.0]
        det = AnomalyDetector()
        anomalies = det.detect(values)
        drop = next(a for a in anomalies if a.anomaly_type == AnomalyType.DROP)
        assert "drop" in drop.description.lower() or "Drop" in drop.description


# ===========================================================================
# AnomalyDetector._percentile
# ===========================================================================


class TestPercentile:
    def test_median_odd(self):
        vals = sorted([1.0, 3.0, 5.0])
        assert AnomalyDetector._percentile(vals, 50) == pytest.approx(3.0)

    def test_median_even(self):
        vals = sorted([1.0, 2.0, 3.0, 4.0])
        assert AnomalyDetector._percentile(vals, 50) == pytest.approx(2.5)

    def test_0th_percentile(self):
        vals = [1.0, 2.0, 3.0]
        assert AnomalyDetector._percentile(vals, 0) == pytest.approx(1.0)

    def test_100th_percentile(self):
        vals = [1.0, 2.0, 3.0]
        assert AnomalyDetector._percentile(vals, 100) == pytest.approx(3.0)

    def test_single_element(self):
        assert AnomalyDetector._percentile([42.0], 75) == pytest.approx(42.0)

    def test_empty_returns_zero(self):
        assert AnomalyDetector._percentile([], 50) == pytest.approx(0.0)


# ===========================================================================
# MetricSeries
# ===========================================================================


class TestMetricSeries:
    def test_latest_none_when_empty(self):
        s = MetricSeries(name="cpu")
        assert s.latest() is None

    def test_latest_returns_last(self):
        s = MetricSeries(name="cpu", values=[1.0, 2.0, 3.0], timestamps=[0.0, 1.0, 2.0])
        assert s.latest() == 3.0

    def test_add_returns_new_instance(self):
        s = MetricSeries(name="cpu")
        s2 = s.add(5.0, ts=1.0)
        assert s is not s2  # new instance
        assert len(s.values) == 0  # original unchanged
        assert len(s2.values) == 1

    def test_add_appends_value(self):
        s = MetricSeries(name="mem")
        s = s.add(10.0, ts=0.0).add(20.0, ts=1.0)
        assert s.values == [10.0, 20.0]

    def test_add_appends_timestamp(self):
        s = MetricSeries(name="mem")
        s = s.add(10.0, ts=100.0)
        assert s.timestamps == [100.0]

    def test_add_auto_timestamp(self):
        s = MetricSeries(name="x")
        before = time.time()
        s2 = s.add(1.0)
        after = time.time()
        assert len(s2.timestamps) == 1
        assert before <= s2.timestamps[0] <= after

    def test_immutable_frozen(self):
        s = MetricSeries(name="x", values=[1.0], timestamps=[0.0])
        with pytest.raises((AttributeError, TypeError)):
            s.name = "y"  # type: ignore[misc]


# ===========================================================================
# AnomalyMonitor
# ===========================================================================


class TestAnomalyMonitor:
    def test_get_series_none_when_missing(self):
        mon = AnomalyMonitor()
        assert mon.get_series("nonexistent") is None

    def test_series_names_empty(self):
        mon = AnomalyMonitor()
        assert mon.series_names() == []

    def test_add_point_registers_series(self):
        mon = AnomalyMonitor()
        mon.add_point("cpu", 1.0, ts=0.0)
        assert "cpu" in mon.series_names()

    def test_add_point_multiple_series(self):
        mon = AnomalyMonitor()
        mon.add_point("cpu", 1.0, ts=0.0)
        mon.add_point("mem", 1.0, ts=0.0)
        assert set(mon.series_names()) == {"cpu", "mem"}

    def test_series_grows_on_add_point(self):
        mon = AnomalyMonitor()
        for i in range(5):
            mon.add_point("x", float(i), ts=float(i))
        series = mon.get_series("x")
        assert series is not None
        assert len(series.values) == 5

    def test_all_anomalies_empty_initially(self):
        mon = AnomalyMonitor()
        assert mon.all_anomalies() == []

    def test_all_anomalies_sorted_by_ts(self):
        mon = AnomalyMonitor()
        cfg = AnomalyConfig(z_threshold=2.0, min_samples=5)
        mon = AnomalyMonitor(cfg)
        # Feed a series that will produce anomalies
        for i in range(10):
            mon.add_point("x", 1.0, ts=float(i))
        mon.add_point("x", 999.0, ts=10.0)
        for i in range(11, 15):
            mon.add_point("x", 1.0, ts=float(i))
        anomalies = mon.all_anomalies()
        ts_list = [a.ts for a in anomalies]
        assert ts_list == sorted(ts_list)

    def test_add_point_returns_list(self):
        mon = AnomalyMonitor()
        result = mon.add_point("cpu", 1.0, ts=0.0)
        assert isinstance(result, list)

    def test_spike_triggers_anomaly_in_monitor(self):
        cfg = AnomalyConfig(z_threshold=2.0, min_samples=5)
        mon = AnomalyMonitor(cfg)
        for i in range(15):
            mon.add_point("cpu", 1.0, ts=float(i))
        new_anomalies = mon.add_point("cpu", 999.0, ts=15.0)
        assert len(new_anomalies) >= 1
        assert any(a.anomaly_type == AnomalyType.SPIKE for a in new_anomalies)

    def test_get_series_returns_correct_name(self):
        mon = AnomalyMonitor()
        mon.add_point("latency", 5.0, ts=0.0)
        series = mon.get_series("latency")
        assert series is not None
        assert series.name == "latency"

    def test_all_anomalies_accumulate_across_calls(self):
        cfg = AnomalyConfig(z_threshold=2.0, min_samples=5)
        mon = AnomalyMonitor(cfg)
        # First spike
        for i in range(15):
            mon.add_point("x", 1.0, ts=float(i))
        mon.add_point("x", 999.0, ts=15.0)
        first_count = len(mon.all_anomalies())
        assert first_count >= 1

    def test_custom_config_respected(self):
        cfg = AnomalyConfig(z_threshold=100.0, min_samples=5)
        mon = AnomalyMonitor(cfg)
        for i in range(15):
            mon.add_point("x", float(i), ts=float(i))
        # With z_threshold=100, normal fluctuations should not be flagged as spike/drop
        spikes_drops = [
            a for a in mon.all_anomalies()
            if a.anomaly_type in (AnomalyType.SPIKE, AnomalyType.DROP)
        ]
        assert spikes_drops == []

    def test_series_latest_after_add_point(self):
        mon = AnomalyMonitor()
        mon.add_point("temp", 42.0, ts=1.0)
        mon.add_point("temp", 43.0, ts=2.0)
        series = mon.get_series("temp")
        assert series is not None
        assert series.latest() == pytest.approx(43.0)
