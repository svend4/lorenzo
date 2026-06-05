"""Tests for docstoolkit.search_analytics (E12)."""
import pytest
from datetime import datetime, timedelta

from docstoolkit.search_analytics import (
    QueryTracker, QueryRecord,
    TrendAnalyzer, TrendReport, QueryTrend,
    ZeroResultMonitor, ZeroResultAlert,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_tracker(*records):
    """Create an in-memory QueryTracker pre-populated with QueryRecords."""
    tracker = QueryTracker()
    for r in records:
        tracker.record(r)
    return tracker


def make_record(query="test", result_count=5, latency_ms=10.0, clicked="", ts="", user_id="", session_id=""):
    return QueryRecord(
        query=query,
        result_count=result_count,
        latency_ms=latency_ms,
        clicked_doc_id=clicked,
        ts=ts,
        user_id=user_id,
        session_id=session_id,
    )


# ---------------------------------------------------------------------------
# QueryRecord — fields and defaults
# ---------------------------------------------------------------------------

class TestQueryRecord:
    def test_fields_stored(self):
        r = QueryRecord(query="hello", result_count=3, latency_ms=5.5)
        assert r.query == "hello"
        assert r.result_count == 3
        assert r.latency_ms == 5.5

    def test_default_user_id_empty(self):
        r = QueryRecord(query="x", result_count=0, latency_ms=1.0)
        assert r.user_id == ""

    def test_default_session_id_empty(self):
        r = QueryRecord(query="x", result_count=0, latency_ms=1.0)
        assert r.session_id == ""

    def test_default_clicked_doc_id_empty(self):
        r = QueryRecord(query="x", result_count=0, latency_ms=1.0)
        assert r.clicked_doc_id == ""

    def test_ts_auto_set_when_empty(self):
        r = QueryRecord(query="x", result_count=1, latency_ms=1.0)
        assert r.ts != ""

    def test_ts_auto_set_is_valid_iso(self):
        r = QueryRecord(query="x", result_count=1, latency_ms=1.0)
        # Should not raise
        datetime.fromisoformat(r.ts)

    def test_ts_explicit_preserved(self):
        explicit = "2025-01-15T10:00:00"
        r = QueryRecord(query="x", result_count=1, latency_ms=1.0, ts=explicit)
        assert r.ts == explicit

    def test_is_zero_result_true_when_zero(self):
        r = QueryRecord(query="x", result_count=0, latency_ms=1.0)
        assert r.is_zero_result() is True

    def test_is_zero_result_false_when_nonzero(self):
        r = QueryRecord(query="x", result_count=1, latency_ms=1.0)
        assert r.is_zero_result() is False

    def test_is_zero_result_false_when_large(self):
        r = QueryRecord(query="x", result_count=100, latency_ms=1.0)
        assert r.is_zero_result() is False

    def test_user_id_stored(self):
        r = QueryRecord(query="x", result_count=1, latency_ms=1.0, user_id="alice")
        assert r.user_id == "alice"

    def test_session_id_stored(self):
        r = QueryRecord(query="x", result_count=1, latency_ms=1.0, session_id="sess-42")
        assert r.session_id == "sess-42"

    def test_clicked_doc_id_stored(self):
        r = QueryRecord(query="x", result_count=5, latency_ms=1.0, clicked_doc_id="doc-99")
        assert r.clicked_doc_id == "doc-99"


# ---------------------------------------------------------------------------
# QueryTracker
# ---------------------------------------------------------------------------

class TestQueryTrackerBasics:
    def test_empty_tracker_total_zero(self):
        t = QueryTracker()
        assert t.total_queries() == 0

    def test_record_increments_total(self):
        t = QueryTracker()
        t.record(make_record())
        assert t.total_queries() == 1

    def test_multiple_records_counted(self):
        t = QueryTracker()
        for _ in range(5):
            t.record(make_record())
        assert t.total_queries() == 5

    def test_record_stores_query_text(self):
        t = QueryTracker()
        t.record(make_record(query="alpha"))
        top = t.top_queries(limit=1)
        assert top[0][0] == "alpha"

    def test_record_distinct_queries_both_stored(self):
        t = QueryTracker()
        t.record(make_record(query="alpha"))
        t.record(make_record(query="beta"))
        assert t.total_queries() == 2


class TestQueryTrackerZeroResults:
    def test_zero_result_queries_empty_when_no_queries(self):
        t = QueryTracker()
        assert t.zero_result_queries() == []

    def test_zero_result_queries_empty_when_all_have_results(self):
        t = make_tracker(make_record(result_count=3), make_record(result_count=10))
        assert t.zero_result_queries() == []

    def test_zero_result_queries_returns_zero_only(self):
        t = make_tracker(
            make_record(query="found", result_count=5),
            make_record(query="missing", result_count=0),
        )
        pairs = t.zero_result_queries()
        assert len(pairs) == 1
        assert pairs[0][0] == "missing"

    def test_zero_result_queries_count_correct(self):
        t = make_tracker(
            make_record(query="missing", result_count=0),
            make_record(query="missing", result_count=0),
            make_record(query="missing", result_count=0),
        )
        pairs = t.zero_result_queries()
        assert pairs[0] == ("missing", 3)

    def test_zero_result_queries_sorted_by_count_desc(self):
        t = make_tracker(
            make_record(query="rare", result_count=0),
            make_record(query="common", result_count=0),
            make_record(query="common", result_count=0),
            make_record(query="common", result_count=0),
        )
        pairs = t.zero_result_queries()
        assert pairs[0][0] == "common"
        assert pairs[1][0] == "rare"

    def test_zero_result_queries_excludes_nonzero(self):
        t = make_tracker(
            make_record(query="q", result_count=0),
            make_record(query="q", result_count=5),  # same query, different result_count
        )
        pairs = t.zero_result_queries()
        # Only the zero-result occurrence should be counted
        assert pairs[0] == ("q", 1)


class TestQueryTrackerTopQueries:
    def test_top_queries_empty(self):
        t = QueryTracker()
        assert t.top_queries() == []

    def test_top_queries_returns_tuples(self):
        t = make_tracker(make_record(query="hello"))
        top = t.top_queries()
        assert isinstance(top[0], tuple)
        assert len(top[0]) == 2

    def test_top_queries_sorted_by_count_desc(self):
        t = make_tracker(
            make_record(query="popular"),
            make_record(query="popular"),
            make_record(query="rare"),
        )
        top = t.top_queries()
        assert top[0] == ("popular", 2)
        assert top[1] == ("rare", 1)

    def test_top_queries_respects_limit(self):
        t = make_tracker(
            make_record(query="a"),
            make_record(query="b"),
            make_record(query="c"),
        )
        assert len(t.top_queries(limit=2)) == 2

    def test_top_queries_limit_larger_than_available(self):
        t = make_tracker(make_record(query="only"))
        assert len(t.top_queries(limit=100)) == 1

    def test_top_queries_same_query_aggregated(self):
        t = make_tracker(
            make_record(query="same"),
            make_record(query="same"),
            make_record(query="same"),
        )
        top = t.top_queries()
        assert len(top) == 1
        assert top[0] == ("same", 3)


class TestQueryTrackerLatency:
    def test_avg_latency_empty_returns_zero(self):
        t = QueryTracker()
        assert t.avg_latency_ms() == 0.0

    def test_avg_latency_single_record(self):
        t = make_tracker(make_record(latency_ms=20.0))
        assert t.avg_latency_ms() == 20.0

    def test_avg_latency_multiple_records(self):
        t = make_tracker(
            make_record(latency_ms=10.0),
            make_record(latency_ms=30.0),
        )
        assert t.avg_latency_ms() == 20.0

    def test_avg_latency_float_precision(self):
        t = make_tracker(
            make_record(latency_ms=1.5),
            make_record(latency_ms=2.5),
            make_record(latency_ms=3.0),
        )
        assert abs(t.avg_latency_ms() - 7.0 / 3) < 1e-9


class TestQueryTrackerCTR:
    def test_ctr_empty_returns_zero(self):
        t = QueryTracker()
        assert t.click_through_rate() == 0.0

    def test_ctr_no_clicks(self):
        t = make_tracker(make_record(clicked=""), make_record(clicked=""))
        assert t.click_through_rate() == 0.0

    def test_ctr_all_clicked(self):
        t = make_tracker(
            make_record(clicked="doc1"),
            make_record(clicked="doc2"),
        )
        assert t.click_through_rate() == 1.0

    def test_ctr_half_clicked(self):
        t = make_tracker(
            make_record(clicked="doc1"),
            make_record(clicked=""),
        )
        assert t.click_through_rate() == 0.5

    def test_ctr_fraction(self):
        t = make_tracker(
            make_record(clicked="doc1"),
            make_record(clicked="doc2"),
            make_record(clicked=""),
        )
        assert abs(t.click_through_rate() - 2 / 3) < 1e-9


# ---------------------------------------------------------------------------
# QueryTrend
# ---------------------------------------------------------------------------

class TestQueryTrend:
    def test_is_rising_above_threshold(self):
        t = QueryTrend(query="q", count_recent=20, count_previous=10, change_pct=100.0)
        assert t.is_rising() is True

    def test_is_rising_exactly_at_threshold_is_false(self):
        t = QueryTrend(query="q", count_recent=11, count_previous=10, change_pct=10.0)
        assert t.is_rising() is False  # must be > 10

    def test_is_rising_below_threshold_false(self):
        t = QueryTrend(query="q", count_recent=10, count_previous=10, change_pct=0.0)
        assert t.is_rising() is False

    def test_is_falling_below_threshold(self):
        t = QueryTrend(query="q", count_recent=5, count_previous=10, change_pct=-50.0)
        assert t.is_falling() is True

    def test_is_falling_exactly_at_threshold_is_false(self):
        t = QueryTrend(query="q", count_recent=9, count_previous=10, change_pct=-10.0)
        assert t.is_falling() is False  # must be < -10

    def test_is_falling_above_threshold_false(self):
        t = QueryTrend(query="q", count_recent=10, count_previous=10, change_pct=0.0)
        assert t.is_falling() is False

    def test_neither_rising_nor_falling_in_band(self):
        t = QueryTrend(query="q", count_recent=10, count_previous=10, change_pct=5.0)
        assert not t.is_rising()
        assert not t.is_falling()

    def test_change_pct_stored(self):
        t = QueryTrend(query="q", count_recent=15, count_previous=10, change_pct=50.0)
        assert t.change_pct == 50.0


# ---------------------------------------------------------------------------
# TrendReport
# ---------------------------------------------------------------------------

class TestTrendReport:
    def test_total_trends_empty(self):
        r = TrendReport(window_hours=24)
        assert r.total_trends() == 0

    def test_total_trends_only_rising(self):
        trend = QueryTrend("q", 10, 5, 100.0)
        r = TrendReport(window_hours=24, rising=[trend])
        assert r.total_trends() == 1

    def test_total_trends_only_falling(self):
        trend = QueryTrend("q", 2, 10, -80.0)
        r = TrendReport(window_hours=24, falling=[trend])
        assert r.total_trends() == 1

    def test_total_trends_only_new(self):
        trend = QueryTrend("q", 5, 0, 0.0)
        r = TrendReport(window_hours=24, new_queries=[trend])
        assert r.total_trends() == 1

    def test_total_trends_sum_all_buckets(self):
        r = TrendReport(
            window_hours=24,
            rising=[QueryTrend("r", 10, 5, 100.0)],
            falling=[QueryTrend("f", 2, 10, -80.0)],
            new_queries=[QueryTrend("n", 3, 0, 0.0), QueryTrend("m", 1, 0, 0.0)],
        )
        assert r.total_trends() == 4

    def test_window_hours_stored(self):
        r = TrendReport(window_hours=48)
        assert r.window_hours == 48


# ---------------------------------------------------------------------------
# TrendAnalyzer
# ---------------------------------------------------------------------------

class TestTrendAnalyzer:
    def test_empty_tracker_returns_trend_report(self):
        t = QueryTracker()
        analyzer = TrendAnalyzer()
        report = analyzer.analyze(t, window_hours=24)
        assert isinstance(report, TrendReport)

    def test_empty_tracker_all_lists_empty(self):
        t = QueryTracker()
        analyzer = TrendAnalyzer()
        report = analyzer.analyze(t, window_hours=24)
        assert report.rising == []
        assert report.falling == []
        assert report.new_queries == []

    def test_window_hours_stored_in_report(self):
        t = QueryTracker()
        analyzer = TrendAnalyzer()
        report = analyzer.analyze(t, window_hours=12)
        assert report.window_hours == 12

    def test_new_query_appears_in_new_queries(self):
        """A query with no history (only in recent window) goes to new_queries."""
        t = QueryTracker()
        analyzer = TrendAnalyzer()
        # Insert a record with a recent ts (now)
        now_ts = datetime.now().isoformat(timespec='seconds')
        t.record(QueryRecord(query="brand_new", result_count=5, latency_ms=5.0, ts=now_ts))
        report = analyzer.analyze(t, window_hours=24)
        new_qs = [tr.query for tr in report.new_queries]
        assert "brand_new" in new_qs

    def test_trend_report_lists_are_lists(self):
        t = QueryTracker()
        analyzer = TrendAnalyzer()
        report = analyzer.analyze(t)
        assert isinstance(report.rising, list)
        assert isinstance(report.falling, list)
        assert isinstance(report.new_queries, list)

    def test_query_trend_objects_have_correct_type(self):
        t = QueryTracker()
        now_ts = datetime.now().isoformat(timespec='seconds')
        t.record(QueryRecord(query="q", result_count=2, latency_ms=5.0, ts=now_ts))
        analyzer = TrendAnalyzer()
        report = analyzer.analyze(t, window_hours=24)
        for trend in report.new_queries:
            assert isinstance(trend, QueryTrend)


# ---------------------------------------------------------------------------
# ZeroResultAlert
# ---------------------------------------------------------------------------

class TestZeroResultAlert:
    def test_is_high_severity_true_for_high(self):
        a = ZeroResultAlert(query="q", occurrence_count=10, last_seen_ts="ts", severity="high")
        assert a.is_high_severity() is True

    def test_is_high_severity_false_for_medium(self):
        a = ZeroResultAlert(query="q", occurrence_count=5, last_seen_ts="ts", severity="medium")
        assert a.is_high_severity() is False

    def test_is_high_severity_false_for_low(self):
        a = ZeroResultAlert(query="q", occurrence_count=1, last_seen_ts="ts", severity="low")
        assert a.is_high_severity() is False

    def test_severity_field_stored(self):
        a = ZeroResultAlert(query="q", occurrence_count=3, last_seen_ts="ts", severity="medium")
        assert a.severity == "medium"

    def test_occurrence_count_stored(self):
        a = ZeroResultAlert(query="q", occurrence_count=7, last_seen_ts="ts", severity="medium")
        assert a.occurrence_count == 7

    def test_last_seen_ts_stored(self):
        a = ZeroResultAlert(query="q", occurrence_count=1, last_seen_ts="2025-01-01T00:00:00", severity="low")
        assert a.last_seen_ts == "2025-01-01T00:00:00"

    def test_query_stored(self):
        a = ZeroResultAlert(query="missing_topic", occurrence_count=1, last_seen_ts="ts", severity="low")
        assert a.query == "missing_topic"


# ---------------------------------------------------------------------------
# ZeroResultMonitor
# ---------------------------------------------------------------------------

class TestZeroResultMonitor:
    def test_scan_empty_tracker(self):
        t = QueryTracker()
        monitor = ZeroResultMonitor()
        assert monitor.scan(t) == []

    def test_scan_no_zero_results(self):
        t = make_tracker(make_record(result_count=5), make_record(result_count=10))
        monitor = ZeroResultMonitor()
        assert monitor.scan(t) == []

    def test_scan_returns_list_of_alerts(self):
        t = make_tracker(make_record(query="missing", result_count=0))
        monitor = ZeroResultMonitor()
        alerts = monitor.scan(t)
        assert isinstance(alerts, list)
        assert isinstance(alerts[0], ZeroResultAlert)

    def test_scan_low_severity_single_occurrence(self):
        t = make_tracker(make_record(query="rare", result_count=0))
        monitor = ZeroResultMonitor()
        alerts = monitor.scan(t)
        assert alerts[0].severity == "low"

    def test_scan_low_severity_two_occurrences(self):
        t = make_tracker(
            make_record(query="rare", result_count=0),
            make_record(query="rare", result_count=0),
        )
        monitor = ZeroResultMonitor()
        alerts = monitor.scan(t)
        assert alerts[0].severity == "low"

    def test_scan_medium_severity_three_occurrences(self):
        t = make_tracker(
            make_record(query="mid", result_count=0),
            make_record(query="mid", result_count=0),
            make_record(query="mid", result_count=0),
        )
        monitor = ZeroResultMonitor()
        alerts = monitor.scan(t)
        assert alerts[0].severity == "medium"

    def test_scan_medium_severity_nine_occurrences(self):
        t = QueryTracker()
        for _ in range(9):
            t.record(make_record(query="mid9", result_count=0))
        monitor = ZeroResultMonitor()
        alerts = monitor.scan(t)
        assert alerts[0].severity == "medium"

    def test_scan_high_severity_ten_occurrences(self):
        t = QueryTracker()
        for _ in range(10):
            t.record(make_record(query="frequent", result_count=0))
        monitor = ZeroResultMonitor()
        alerts = monitor.scan(t)
        assert alerts[0].severity == "high"

    def test_scan_high_severity_many_occurrences(self):
        t = QueryTracker()
        for _ in range(25):
            t.record(make_record(query="very_frequent", result_count=0))
        monitor = ZeroResultMonitor()
        alerts = monitor.scan(t)
        assert alerts[0].severity == "high"

    def test_scan_sorted_by_occurrence_count_desc(self):
        t = QueryTracker()
        for _ in range(5):
            t.record(make_record(query="common_zero", result_count=0))
        t.record(make_record(query="rare_zero", result_count=0))
        monitor = ZeroResultMonitor()
        alerts = monitor.scan(t)
        assert alerts[0].query == "common_zero"
        assert alerts[1].query == "rare_zero"

    def test_scan_last_seen_ts_populated(self):
        ts = "2025-06-01T12:00:00"
        t = make_tracker(make_record(query="q", result_count=0, ts=ts))
        monitor = ZeroResultMonitor()
        alerts = monitor.scan(t)
        assert alerts[0].last_seen_ts == ts

    def test_scan_occurrence_count_correct(self):
        t = QueryTracker()
        for _ in range(4):
            t.record(make_record(query="q4", result_count=0))
        monitor = ZeroResultMonitor()
        alerts = monitor.scan(t)
        assert alerts[0].occurrence_count == 4

    def test_scan_custom_high_threshold(self):
        t = QueryTracker()
        for _ in range(5):
            t.record(make_record(query="q", result_count=0))
        monitor = ZeroResultMonitor(high_threshold=5)
        alerts = monitor.scan(t)
        assert alerts[0].severity == "high"

    def test_scan_excludes_queries_with_results(self):
        t = make_tracker(
            make_record(query="found", result_count=3),
            make_record(query="missing", result_count=0),
        )
        monitor = ZeroResultMonitor()
        alerts = monitor.scan(t)
        assert len(alerts) == 1
        assert alerts[0].query == "missing"
