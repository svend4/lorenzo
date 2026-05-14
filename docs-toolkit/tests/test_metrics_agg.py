"""Tests for docstoolkit.metrics_agg — E75 Metrics Aggregator.

Coverage targets
----------------
- MetricType enum values
- MetricSample construction (defaults and explicit fields)
- MetricFamily: add_sample, latest
- AggregationWindow: mean / sum_ / min_ / max_ / count / percentile
- MetricsAggregator: record, window, rate, histogram_buckets,
                     label_values, names
- MetricsReporter: report (all / filtered), to_text format, export_json
- Edge cases: empty window, single sample, percentile on empty,
              rate with no counters, histogram with unsorted buckets
"""
from __future__ import annotations

import json
import math
import os
import tempfile
import time

import pytest

from docstoolkit.metrics_agg import (
    AggregationWindow,
    MetricFamily,
    MetricSample,
    MetricType,
    MetricsAggregator,
    MetricsReport,
    MetricsReporter,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sample(
    name: str = "m",
    value: float = 1.0,
    labels: dict | None = None,
    ts: float = 1000.0,
    metric_type: MetricType = MetricType.GAUGE,
) -> MetricSample:
    return MetricSample(
        name=name,
        value=value,
        labels=labels if labels is not None else {},
        ts=ts,
        metric_type=metric_type,
    )


def _window(*values: float, start: float = 0.0, end: float = 9999.0) -> AggregationWindow:
    samples = [_sample(value=v, ts=start + i) for i, v in enumerate(values)]
    return AggregationWindow(start_ts=start, end_ts=end, samples=samples)


# ===========================================================================
# MetricType
# ===========================================================================

class TestMetricType:
    def test_counter_value(self):
        assert MetricType.COUNTER.value == "counter"

    def test_gauge_value(self):
        assert MetricType.GAUGE.value == "gauge"

    def test_histogram_value(self):
        assert MetricType.HISTOGRAM.value == "histogram"

    def test_summary_value(self):
        assert MetricType.SUMMARY.value == "summary"

    def test_all_four_members(self):
        names = {m.name for m in MetricType}
        assert names == {"COUNTER", "GAUGE", "HISTOGRAM", "SUMMARY"}

    def test_enum_identity(self):
        assert MetricType("counter") is MetricType.COUNTER


# ===========================================================================
# MetricSample
# ===========================================================================

class TestMetricSample:
    def test_explicit_fields(self):
        s = MetricSample(
            name="cpu",
            value=0.75,
            labels={"host": "a"},
            ts=1234.5,
            metric_type=MetricType.GAUGE,
        )
        assert s.name == "cpu"
        assert s.value == 0.75
        assert s.labels == {"host": "a"}
        assert s.ts == 1234.5
        assert s.metric_type == MetricType.GAUGE

    def test_default_labels_empty_dict(self):
        s = MetricSample(name="x", value=1.0)
        assert s.labels == {}

    def test_default_metric_type_gauge(self):
        s = MetricSample(name="x", value=1.0)
        assert s.metric_type == MetricType.GAUGE

    def test_default_ts_is_recent(self):
        before = time.time()
        s = MetricSample(name="x", value=0.0)
        after = time.time()
        assert before <= s.ts <= after

    def test_labels_independent_between_instances(self):
        s1 = MetricSample(name="x", value=1.0)
        s2 = MetricSample(name="y", value=2.0)
        s1.labels["k"] = "v"
        assert "k" not in s2.labels

    def test_counter_type(self):
        s = MetricSample(name="req", value=10.0, metric_type=MetricType.COUNTER)
        assert s.metric_type == MetricType.COUNTER

    def test_histogram_type(self):
        s = MetricSample(name="lat", value=0.1, metric_type=MetricType.HISTOGRAM)
        assert s.metric_type == MetricType.HISTOGRAM


# ===========================================================================
# MetricFamily
# ===========================================================================

class TestMetricFamily:
    def test_basic_construction(self):
        mf = MetricFamily(name="req", metric_type=MetricType.COUNTER)
        assert mf.name == "req"
        assert mf.metric_type == MetricType.COUNTER
        assert mf.description == ""
        assert mf.samples == []

    def test_description(self):
        mf = MetricFamily(name="q", metric_type=MetricType.GAUGE, description="help")
        assert mf.description == "help"

    def test_latest_empty(self):
        mf = MetricFamily(name="q", metric_type=MetricType.GAUGE)
        assert mf.latest() is None

    def test_add_sample_increases_count(self):
        mf = MetricFamily(name="q", metric_type=MetricType.GAUGE)
        mf.add_sample(1.0)
        assert len(mf.samples) == 1

    def test_add_sample_value(self):
        mf = MetricFamily(name="q", metric_type=MetricType.GAUGE)
        mf.add_sample(42.0)
        assert mf.samples[0].value == 42.0

    def test_add_sample_name_matches_family(self):
        mf = MetricFamily(name="myfam", metric_type=MetricType.COUNTER)
        mf.add_sample(1.0)
        assert mf.samples[0].name == "myfam"

    def test_add_sample_with_labels(self):
        mf = MetricFamily(name="q", metric_type=MetricType.GAUGE)
        mf.add_sample(5.0, labels={"env": "prod"})
        assert mf.samples[0].labels == {"env": "prod"}

    def test_add_sample_no_labels_defaults_empty(self):
        mf = MetricFamily(name="q", metric_type=MetricType.GAUGE)
        mf.add_sample(3.0)
        assert mf.samples[0].labels == {}

    def test_add_sample_ts_is_recent(self):
        before = time.time()
        mf = MetricFamily(name="q", metric_type=MetricType.GAUGE)
        mf.add_sample(0.0)
        after = time.time()
        assert before <= mf.samples[0].ts <= after

    def test_latest_returns_last(self):
        mf = MetricFamily(name="q", metric_type=MetricType.GAUGE)
        mf.add_sample(1.0)
        mf.add_sample(2.0)
        mf.add_sample(3.0)
        assert mf.latest() == 3.0

    def test_latest_single(self):
        mf = MetricFamily(name="q", metric_type=MetricType.GAUGE)
        mf.add_sample(99.0)
        assert mf.latest() == 99.0

    def test_samples_independent_between_families(self):
        mf1 = MetricFamily(name="a", metric_type=MetricType.GAUGE)
        mf2 = MetricFamily(name="b", metric_type=MetricType.GAUGE)
        mf1.add_sample(1.0)
        assert len(mf2.samples) == 0

    def test_add_sample_metric_type_matches_family(self):
        mf = MetricFamily(name="c", metric_type=MetricType.HISTOGRAM)
        mf.add_sample(0.5)
        assert mf.samples[0].metric_type == MetricType.HISTOGRAM


# ===========================================================================
# AggregationWindow
# ===========================================================================

class TestAggregationWindowEmpty:
    def setup_method(self):
        self.w = AggregationWindow(start_ts=0.0, end_ts=100.0)

    def test_count_empty(self):
        assert self.w.count() == 0

    def test_mean_empty(self):
        assert self.w.mean() == 0.0

    def test_sum_empty(self):
        assert self.w.sum_() == 0.0

    def test_min_empty(self):
        assert self.w.min_() == 0.0

    def test_max_empty(self):
        assert self.w.max_() == 0.0

    def test_percentile_empty_raises(self):
        with pytest.raises((ValueError, ZeroDivisionError, IndexError, Exception)):
            self.w.percentile(50)


class TestAggregationWindowSingle:
    def setup_method(self):
        self.w = _window(7.0)

    def test_count(self):
        assert self.w.count() == 1

    def test_mean(self):
        assert self.w.mean() == 7.0

    def test_sum(self):
        assert self.w.sum_() == 7.0

    def test_min(self):
        assert self.w.min_() == 7.0

    def test_max(self):
        assert self.w.max_() == 7.0

    def test_percentile_0(self):
        assert self.w.percentile(0) == 7.0

    def test_percentile_50(self):
        assert self.w.percentile(50) == 7.0

    def test_percentile_100(self):
        assert self.w.percentile(100) == 7.0


class TestAggregationWindowMultiple:
    def setup_method(self):
        # values: 1, 2, 3, 4, 5
        self.w = _window(1.0, 2.0, 3.0, 4.0, 5.0)

    def test_count(self):
        assert self.w.count() == 5

    def test_mean(self):
        assert self.w.mean() == pytest.approx(3.0)

    def test_sum(self):
        assert self.w.sum_() == pytest.approx(15.0)

    def test_min(self):
        assert self.w.min_() == pytest.approx(1.0)

    def test_max(self):
        assert self.w.max_() == pytest.approx(5.0)

    def test_percentile_0(self):
        assert self.w.percentile(0) == pytest.approx(1.0)

    def test_percentile_100(self):
        assert self.w.percentile(100) == pytest.approx(5.0)

    def test_percentile_50(self):
        # median of [1,2,3,4,5] = 3.0
        assert self.w.percentile(50) == pytest.approx(3.0)

    def test_percentile_25(self):
        # rank = 0.25 * 4 = 1.0 → vals[1] = 2.0
        assert self.w.percentile(25) == pytest.approx(2.0)

    def test_percentile_75(self):
        # rank = 0.75 * 4 = 3.0 → vals[3] = 4.0
        assert self.w.percentile(75) == pytest.approx(4.0)

    def test_percentile_interpolation(self):
        # rank = 0.40 * 4 = 1.6 → 2.0 + 0.6 * 1.0 = 2.6
        result = self.w.percentile(40)
        assert result == pytest.approx(2.6)


# ===========================================================================
# MetricsAggregator
# ===========================================================================

class TestMetricsAggregatorBasic:
    def setup_method(self):
        self.agg = MetricsAggregator()

    def test_names_empty(self):
        assert self.agg.names() == []

    def test_record_one(self):
        self.agg.record(_sample("cpu", 0.5))
        assert "cpu" in self.agg.names()

    def test_names_unique(self):
        self.agg.record(_sample("cpu", 0.1))
        self.agg.record(_sample("cpu", 0.2))
        assert self.agg.names().count("cpu") == 1

    def test_names_order_first_seen(self):
        self.agg.record(_sample("b"))
        self.agg.record(_sample("a"))
        self.agg.record(_sample("c"))
        assert self.agg.names() == ["b", "a", "c"]

    def test_multiple_metrics(self):
        self.agg.record(_sample("x"))
        self.agg.record(_sample("y"))
        assert set(self.agg.names()) == {"x", "y"}


class TestMetricsAggregatorWindow:
    def setup_method(self):
        self.agg = MetricsAggregator()
        for i in range(5):
            self.agg.record(_sample("m", value=float(i), ts=float(i) + 1.0))

    # samples at ts 1.0, 2.0, 3.0, 4.0, 5.0

    def test_window_all(self):
        w = self.agg.window("m", 1.0, 5.0)
        assert w.count() == 5

    def test_window_partial(self):
        w = self.agg.window("m", 2.0, 3.0)
        assert w.count() == 2

    def test_window_none(self):
        w = self.agg.window("m", 10.0, 20.0)
        assert w.count() == 0

    def test_window_different_name(self):
        w = self.agg.window("other", 0.0, 99.0)
        assert w.count() == 0

    def test_window_label_filter_match(self):
        agg = MetricsAggregator()
        agg.record(_sample("n", labels={"env": "prod"}, ts=1.0))
        agg.record(_sample("n", labels={"env": "dev"}, ts=2.0))
        w = agg.window("n", 0.0, 5.0, labels={"env": "prod"})
        assert w.count() == 1
        assert w.samples[0].labels["env"] == "prod"

    def test_window_label_filter_no_match(self):
        agg = MetricsAggregator()
        agg.record(_sample("n", labels={"env": "prod"}, ts=1.0))
        w = agg.window("n", 0.0, 5.0, labels={"env": "qa"})
        assert w.count() == 0

    def test_window_no_label_filter_includes_all_labels(self):
        agg = MetricsAggregator()
        agg.record(_sample("n", labels={"env": "prod"}, ts=1.0))
        agg.record(_sample("n", labels={"env": "dev"}, ts=2.0))
        w = agg.window("n", 0.0, 5.0)
        assert w.count() == 2

    def test_window_boundary_inclusive(self):
        w = self.agg.window("m", 1.0, 1.0)
        assert w.count() == 1

    def test_window_correct_values(self):
        w = self.agg.window("m", 2.0, 4.0)
        vals = sorted(s.value for s in w.samples)
        assert vals == [1.0, 2.0, 3.0]


class TestMetricsAggregatorRate:
    def setup_method(self):
        self.agg = MetricsAggregator()

    def test_rate_empty(self):
        r = self.agg.rate("req", 60.0, now=1000.0)
        assert r == 0.0

    def test_rate_single_counter(self):
        self.agg.record(
            MetricSample(name="req", value=10.0, ts=950.0, metric_type=MetricType.COUNTER)
        )
        r = self.agg.rate("req", 60.0, now=1000.0)
        assert r == pytest.approx(10.0 / 60.0)

    def test_rate_multiple_counters(self):
        for ts in [940.0, 960.0, 980.0]:
            self.agg.record(
                MetricSample(name="req", value=5.0, ts=ts, metric_type=MetricType.COUNTER)
            )
        r = self.agg.rate("req", 60.0, now=1000.0)
        assert r == pytest.approx(15.0 / 60.0)

    def test_rate_excludes_outside_window(self):
        # inside window
        self.agg.record(
            MetricSample(name="req", value=5.0, ts=990.0, metric_type=MetricType.COUNTER)
        )
        # outside window (too old)
        self.agg.record(
            MetricSample(name="req", value=100.0, ts=500.0, metric_type=MetricType.COUNTER)
        )
        r = self.agg.rate("req", 60.0, now=1000.0)
        assert r == pytest.approx(5.0 / 60.0)

    def test_rate_ignores_gauge(self):
        self.agg.record(
            MetricSample(name="req", value=50.0, ts=990.0, metric_type=MetricType.GAUGE)
        )
        r = self.agg.rate("req", 60.0, now=1000.0)
        assert r == 0.0

    def test_rate_different_metric_name(self):
        self.agg.record(
            MetricSample(name="other", value=10.0, ts=990.0, metric_type=MetricType.COUNTER)
        )
        r = self.agg.rate("req", 60.0, now=1000.0)
        assert r == 0.0


class TestMetricsAggregatorHistogram:
    def setup_method(self):
        self.agg = MetricsAggregator()
        for v in [0.1, 0.3, 0.5, 0.7, 1.0]:
            self.agg.record(_sample("lat", value=v))

    def test_histogram_all_below_max(self):
        buckets = self.agg.histogram_buckets("lat", [10.0])
        assert buckets[10.0] == 5

    def test_histogram_none_below_min(self):
        buckets = self.agg.histogram_buckets("lat", [0.0])
        assert buckets[0.0] == 0

    def test_histogram_partial(self):
        buckets = self.agg.histogram_buckets("lat", [0.5])
        assert buckets[0.5] == 3  # 0.1, 0.3, 0.5

    def test_histogram_multiple_buckets(self):
        buckets = self.agg.histogram_buckets("lat", [0.3, 0.7, 1.0])
        assert buckets[0.3] == 2
        assert buckets[0.7] == 4
        assert buckets[1.0] == 5

    def test_histogram_unsorted_buckets(self):
        buckets = self.agg.histogram_buckets("lat", [1.0, 0.3])
        assert buckets[1.0] == 5
        assert buckets[0.3] == 2

    def test_histogram_empty_metric(self):
        buckets = self.agg.histogram_buckets("unknown", [1.0])
        assert buckets[1.0] == 0

    def test_histogram_returns_all_keys(self):
        thresholds = [0.1, 0.5, 1.0]
        buckets = self.agg.histogram_buckets("lat", thresholds)
        assert set(buckets.keys()) == set(thresholds)


class TestMetricsAggregatorLabelValues:
    def setup_method(self):
        self.agg = MetricsAggregator()
        for env in ["prod", "dev", "prod", "staging"]:
            self.agg.record(_sample("n", labels={"env": env}))

    def test_distinct_values(self):
        vals = self.agg.label_values("n", "env")
        assert set(vals) == {"prod", "dev", "staging"}

    def test_order_first_seen(self):
        vals = self.agg.label_values("n", "env")
        assert vals[0] == "prod"
        assert vals[1] == "dev"
        assert vals[2] == "staging"

    def test_missing_label_key(self):
        vals = self.agg.label_values("n", "nonexistent")
        assert vals == []

    def test_different_metric_name(self):
        vals = self.agg.label_values("other", "env")
        assert vals == []

    def test_no_labels(self):
        agg = MetricsAggregator()
        agg.record(_sample("m"))
        assert agg.label_values("m", "env") == []


# ===========================================================================
# MetricsReporter
# ===========================================================================

class TestMetricsReporterReport:
    def setup_method(self):
        self.agg = MetricsAggregator()
        self.agg.record(_sample("cpu", 0.5, ts=1000.0))
        self.agg.record(_sample("cpu", 0.7, ts=1001.0))
        self.agg.record(_sample("mem", 200.0, ts=1000.0))
        self.reporter = MetricsReporter(self.agg)

    def test_report_all_names(self):
        rpt = self.reporter.report()
        assert set(rpt.metrics.keys()) == {"cpu", "mem"}

    def test_report_filtered_names(self):
        rpt = self.reporter.report(names=["cpu"])
        assert list(rpt.metrics.keys()) == ["cpu"]
        assert "mem" not in rpt.metrics

    def test_report_count(self):
        rpt = self.reporter.report()
        assert rpt.metrics["cpu"]["count"] == 2
        assert rpt.metrics["mem"]["count"] == 1

    def test_report_mean(self):
        rpt = self.reporter.report()
        assert rpt.metrics["cpu"]["mean"] == pytest.approx(0.6)

    def test_report_min(self):
        rpt = self.reporter.report()
        assert rpt.metrics["cpu"]["min"] == pytest.approx(0.5)

    def test_report_max(self):
        rpt = self.reporter.report()
        assert rpt.metrics["cpu"]["max"] == pytest.approx(0.7)

    def test_report_samples_list(self):
        rpt = self.reporter.report()
        assert len(rpt.metrics["cpu"]["samples"]) == 2

    def test_report_sample_fields(self):
        rpt = self.reporter.report()
        s = rpt.metrics["cpu"]["samples"][0]
        assert "name" in s
        assert "value" in s
        assert "labels" in s
        assert "ts" in s
        assert "metric_type" in s

    def test_report_generated_at_recent(self):
        before = time.time()
        rpt = self.reporter.report()
        after = time.time()
        assert before <= rpt.generated_at <= after

    def test_report_empty_aggregator(self):
        reporter = MetricsReporter(MetricsAggregator())
        rpt = reporter.report()
        assert rpt.metrics == {}

    def test_report_unknown_name(self):
        rpt = self.reporter.report(names=["nonexistent"])
        assert rpt.metrics["nonexistent"]["count"] == 0

    def test_report_mean_empty_metric(self):
        rpt = self.reporter.report(names=["nonexistent"])
        assert rpt.metrics["nonexistent"]["mean"] == 0.0


class TestMetricsReporterToText:
    def setup_method(self):
        self.agg = MetricsAggregator()
        self.agg.record(
            MetricSample(name="cpu", value=0.5, labels={}, ts=1000.0, metric_type=MetricType.GAUGE)
        )
        self.agg.record(
            MetricSample(name="req", value=3.0, labels={"method": "GET"}, ts=2000.0, metric_type=MetricType.COUNTER)
        )
        self.reporter = MetricsReporter(self.agg)

    def test_to_text_not_empty(self):
        rpt = self.reporter.report()
        text = rpt.to_text()
        assert len(text) > 0

    def test_to_text_contains_metric_name(self):
        text = self.reporter.report().to_text()
        assert "cpu" in text

    def test_to_text_no_label_format(self):
        text = self.reporter.report(names=["cpu"]).to_text()
        # No braces for label-less sample
        assert "cpu 0.5 1000.0" in text

    def test_to_text_with_label_format(self):
        text = self.reporter.report(names=["req"]).to_text()
        assert "req{method=GET} 3.0 2000.0" in text

    def test_to_text_ends_with_newline(self):
        text = self.reporter.report().to_text()
        assert text.endswith("\n")

    def test_to_text_empty_report_is_empty_string(self):
        reporter = MetricsReporter(MetricsAggregator())
        rpt = reporter.report()
        assert rpt.to_text() == ""

    def test_to_text_multiple_lines(self):
        text = self.reporter.report().to_text()
        lines = [l for l in text.split("\n") if l]
        assert len(lines) == 2

    def test_to_text_multiple_labels_sorted(self):
        agg = MetricsAggregator()
        agg.record(
            MetricSample(
                name="x", value=1.0,
                labels={"z": "3", "a": "1", "m": "2"},
                ts=500.0
            )
        )
        reporter = MetricsReporter(agg)
        text = reporter.report().to_text()
        assert "x{a=1,m=2,z=3}" in text


class TestMetricsReporterExportJson:
    def test_export_creates_file(self):
        agg = MetricsAggregator()
        agg.record(_sample("m", 1.0))
        reporter = MetricsReporter(agg)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.json")
            reporter.export_json(path)
            assert os.path.exists(path)

    def test_export_valid_json(self):
        agg = MetricsAggregator()
        agg.record(_sample("m", 1.0))
        reporter = MetricsReporter(agg)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.json")
            reporter.export_json(path)
            with open(path) as fh:
                data = json.load(fh)
        assert "generated_at" in data
        assert "metrics" in data

    def test_export_contains_metric(self):
        agg = MetricsAggregator()
        agg.record(_sample("mymetric", 42.0))
        reporter = MetricsReporter(agg)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.json")
            reporter.export_json(path)
            with open(path) as fh:
                data = json.load(fh)
        assert "mymetric" in data["metrics"]

    def test_export_count_correct(self):
        agg = MetricsAggregator()
        agg.record(_sample("m", 1.0))
        agg.record(_sample("m", 2.0))
        reporter = MetricsReporter(agg)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "out.json")
            reporter.export_json(path)
            with open(path) as fh:
                data = json.load(fh)
        assert data["metrics"]["m"]["count"] == 2

    def test_export_path_as_pathlib(self):
        from pathlib import Path
        agg = MetricsAggregator()
        agg.record(_sample("m"))
        reporter = MetricsReporter(agg)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "report.json"
            reporter.export_json(path)
            assert path.exists()

    def test_export_overwrites_existing(self):
        agg = MetricsAggregator()
        agg.record(_sample("m", 1.0))
        reporter = MetricsReporter(agg)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "report.json")
            # write first version
            reporter.export_json(path)
            # add more data and overwrite
            agg.record(_sample("m", 2.0))
            reporter.export_json(path)
            with open(path) as fh:
                data = json.load(fh)
        assert data["metrics"]["m"]["count"] == 2


# ===========================================================================
# Public __init__ exports
# ===========================================================================

class TestPublicExports:
    def test_metric_type_exported(self):
        from docstoolkit.metrics_agg import MetricType
        assert MetricType.GAUGE

    def test_metric_sample_exported(self):
        from docstoolkit.metrics_agg import MetricSample
        assert MetricSample

    def test_metric_family_exported(self):
        from docstoolkit.metrics_agg import MetricFamily
        assert MetricFamily

    def test_aggregation_window_exported(self):
        from docstoolkit.metrics_agg import AggregationWindow
        assert AggregationWindow

    def test_metrics_aggregator_exported(self):
        from docstoolkit.metrics_agg import MetricsAggregator
        assert MetricsAggregator

    def test_metrics_report_exported(self):
        from docstoolkit.metrics_agg import MetricsReport
        assert MetricsReport

    def test_metrics_reporter_exported(self):
        from docstoolkit.metrics_agg import MetricsReporter
        assert MetricsReporter
