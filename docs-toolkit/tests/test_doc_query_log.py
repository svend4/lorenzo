"""Tests for docstoolkit.doc_query_log."""
import threading

import pytest

from docstoolkit.doc_query_log import (
    DocQueryLog,
    QueryEntry,
    QueryStats,
    Trend,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestQueryEntry:
    def test_defaults(self):
        e = QueryEntry()
        assert e.query_id == 0
        assert e.query == ""
        assert e.user_id is None
        assert e.result_count == 0
        assert e.timestamp == 0.0
        assert e.selected_result is None
        assert e.latency_ms == 0.0

    def test_custom(self):
        e = QueryEntry(
            query_id=7,
            query="foo",
            user_id="u1",
            result_count=3,
            timestamp=100.0,
            selected_result="doc:1",
            latency_ms=12.5,
        )
        assert e.query_id == 7
        assert e.query == "foo"
        assert e.user_id == "u1"
        assert e.result_count == 3
        assert e.timestamp == 100.0
        assert e.selected_result == "doc:1"
        assert e.latency_ms == 12.5

    def test_mutability(self):
        e = QueryEntry()
        e.selected_result = "doc:2"
        assert e.selected_result == "doc:2"


class TestQueryStats:
    def test_defaults(self):
        s = QueryStats()
        assert s.total_queries == 0
        assert s.unique_queries == 0
        assert s.zero_result_count == 0
        assert s.avg_results == 0.0
        assert s.avg_latency_ms == 0.0
        assert s.top_queries == []
        assert s.top_users == []

    def test_independent_defaults(self):
        a = QueryStats()
        b = QueryStats()
        a.top_queries.append(("x", 1))
        assert b.top_queries == []


class TestTrend:
    def test_defaults(self):
        t = Trend()
        assert t.query == ""
        assert t.recent_count == 0
        assert t.older_count == 0
        assert t.growth_rate == 0.0

    def test_custom(self):
        t = Trend(query="rag", recent_count=10, older_count=2, growth_rate=4.0)
        assert t.query == "rag"
        assert t.recent_count == 10
        assert t.older_count == 2
        assert t.growth_rate == 4.0


# ---------------------------------------------------------------------------
# log()
# ---------------------------------------------------------------------------


class TestLog:
    def test_log_returns_entry(self):
        log = DocQueryLog()
        e = log.log("hello", result_count=5, user_id="u1", now=1.0)
        assert isinstance(e, QueryEntry)
        assert e.query == "hello"
        assert e.result_count == 5
        assert e.user_id == "u1"
        assert e.timestamp == 1.0

    def test_log_assigns_unique_ids(self):
        log = DocQueryLog()
        e1 = log.log("a", now=1.0)
        e2 = log.log("b", now=2.0)
        e3 = log.log("c", now=3.0)
        assert e1.query_id == 1
        assert e2.query_id == 2
        assert e3.query_id == 3

    def test_log_defaults(self):
        log = DocQueryLog()
        e = log.log("q")
        assert e.result_count == 0
        assert e.user_id is None
        assert e.selected_result is None
        assert e.latency_ms == 0.0
        assert e.timestamp == 0.0

    def test_log_appends(self):
        log = DocQueryLog()
        log.log("a", now=1.0)
        log.log("b", now=2.0)
        assert log.total_queries == 2

    def test_log_with_selected_result(self):
        log = DocQueryLog()
        e = log.log("q", selected_result="doc:42", now=1.0)
        assert e.selected_result == "doc:42"

    def test_log_thread_safe(self):
        log = DocQueryLog()

        def worker():
            for i in range(50):
                log.log("q", now=float(i))

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert log.total_queries == 200
        # All ids unique
        ids = {e.query_id for e in log.recent(500)}
        assert len(ids) == 200


# ---------------------------------------------------------------------------
# record_selection()
# ---------------------------------------------------------------------------


class TestRecordSelection:
    def test_record_selection_existing(self):
        log = DocQueryLog()
        e = log.log("q", now=1.0)
        ok = log.record_selection(e.query_id, "doc:1")
        assert ok is True
        same = log.queries_for_query("q")[0]
        assert same.selected_result == "doc:1"

    def test_record_selection_missing(self):
        log = DocQueryLog()
        log.log("q", now=1.0)
        ok = log.record_selection(999, "doc:1")
        assert ok is False

    def test_record_selection_overwrites(self):
        log = DocQueryLog()
        e = log.log("q", selected_result="doc:a", now=1.0)
        log.record_selection(e.query_id, "doc:b")
        assert log.queries_for_query("q")[0].selected_result == "doc:b"


# ---------------------------------------------------------------------------
# recent()
# ---------------------------------------------------------------------------


class TestRecent:
    def test_recent_reverse_chrono(self):
        log = DocQueryLog()
        log.log("a", now=1.0)
        log.log("b", now=2.0)
        log.log("c", now=3.0)
        r = log.recent(2)
        assert [e.query for e in r] == ["c", "b"]

    def test_recent_default(self):
        log = DocQueryLog()
        for i in range(20):
            log.log(f"q{i}", now=float(i))
        r = log.recent()
        assert len(r) == 10
        assert r[0].query == "q19"

    def test_recent_n_zero(self):
        log = DocQueryLog()
        log.log("a", now=1.0)
        assert log.recent(0) == []

    def test_recent_when_empty(self):
        log = DocQueryLog()
        assert log.recent(5) == []

    def test_recent_n_larger_than_size(self):
        log = DocQueryLog()
        log.log("a", now=1.0)
        log.log("b", now=2.0)
        assert len(log.recent(100)) == 2


# ---------------------------------------------------------------------------
# queries_by_user()
# ---------------------------------------------------------------------------


class TestQueriesByUser:
    def test_filter_by_user(self):
        log = DocQueryLog()
        log.log("a", user_id="u1", now=1.0)
        log.log("b", user_id="u2", now=2.0)
        log.log("c", user_id="u1", now=3.0)
        r = log.queries_by_user("u1")
        assert [e.query for e in r] == ["a", "c"]

    def test_no_match(self):
        log = DocQueryLog()
        log.log("a", user_id="u1", now=1.0)
        assert log.queries_by_user("ghost") == []

    def test_none_user_not_matched(self):
        log = DocQueryLog()
        log.log("a", now=1.0)  # user_id is None
        log.log("b", user_id="u1", now=2.0)
        assert [e.query for e in log.queries_by_user("u1")] == ["b"]


# ---------------------------------------------------------------------------
# queries_for_query()
# ---------------------------------------------------------------------------


class TestQueriesForQuery:
    def test_case_insensitive_default(self):
        log = DocQueryLog()
        log.log("Hello", now=1.0)
        log.log("HELLO", now=2.0)
        log.log("world", now=3.0)
        r = log.queries_for_query("hello")
        assert len(r) == 2

    def test_case_sensitive(self):
        log = DocQueryLog()
        log.log("Hello", now=1.0)
        log.log("hello", now=2.0)
        r = log.queries_for_query("hello", case_sensitive=True)
        assert len(r) == 1
        assert r[0].query == "hello"

    def test_no_match(self):
        log = DocQueryLog()
        log.log("foo", now=1.0)
        assert log.queries_for_query("bar") == []


# ---------------------------------------------------------------------------
# zero_result_queries()
# ---------------------------------------------------------------------------


class TestZeroResultQueries:
    def test_basic(self):
        log = DocQueryLog()
        log.log("a", result_count=0, now=1.0)
        log.log("b", result_count=5, now=2.0)
        log.log("c", result_count=0, now=3.0)
        r = log.zero_result_queries()
        assert {e.query for e in r} == {"a", "c"}

    def test_limit(self):
        log = DocQueryLog()
        for i in range(5):
            log.log(f"q{i}", result_count=0, now=float(i))
        assert len(log.zero_result_queries(limit=2)) == 2

    def test_no_zero_results(self):
        log = DocQueryLog()
        log.log("a", result_count=3, now=1.0)
        assert log.zero_result_queries() == []

    def test_limit_zero(self):
        log = DocQueryLog()
        log.log("a", result_count=0, now=1.0)
        assert log.zero_result_queries(limit=0) == []


# ---------------------------------------------------------------------------
# count_query()
# ---------------------------------------------------------------------------


class TestCountQuery:
    def test_count_case_insensitive(self):
        log = DocQueryLog()
        log.log("Foo", now=1.0)
        log.log("FOO", now=2.0)
        log.log("bar", now=3.0)
        assert log.count_query("foo") == 2

    def test_count_case_sensitive(self):
        log = DocQueryLog()
        log.log("Foo", now=1.0)
        log.log("foo", now=2.0)
        assert log.count_query("foo", case_sensitive=True) == 1

    def test_count_missing(self):
        log = DocQueryLog()
        log.log("foo", now=1.0)
        assert log.count_query("bar") == 0


# ---------------------------------------------------------------------------
# top_queries()
# ---------------------------------------------------------------------------


class TestTopQueries:
    def test_basic_order(self):
        log = DocQueryLog()
        for _ in range(3):
            log.log("a", now=1.0)
        for _ in range(2):
            log.log("b", now=1.0)
        log.log("c", now=1.0)
        top = log.top_queries(top_k=2)
        assert top == [("a", 3), ("b", 2)]

    def test_top_k_zero(self):
        log = DocQueryLog()
        log.log("a", now=1.0)
        assert log.top_queries(top_k=0) == []

    def test_since_filter(self):
        log = DocQueryLog()
        log.log("a", now=10.0)
        log.log("a", now=20.0)
        log.log("a", now=30.0)
        top = log.top_queries(top_k=10, since=15.0)
        assert top == [("a", 2)]

    def test_empty(self):
        log = DocQueryLog()
        assert log.top_queries() == []


# ---------------------------------------------------------------------------
# top_users()
# ---------------------------------------------------------------------------


class TestTopUsers:
    def test_basic(self):
        log = DocQueryLog()
        for _ in range(4):
            log.log("q", user_id="u1", now=1.0)
        for _ in range(2):
            log.log("q", user_id="u2", now=1.0)
        log.log("q", user_id="u3", now=1.0)
        top = log.top_users(top_k=2)
        assert top == [("u1", 4), ("u2", 2)]

    def test_skips_none(self):
        log = DocQueryLog()
        log.log("q", now=1.0)  # None user
        log.log("q", user_id="u1", now=1.0)
        top = log.top_users()
        assert top == [("u1", 1)]

    def test_top_k_zero(self):
        log = DocQueryLog()
        log.log("q", user_id="u1", now=1.0)
        assert log.top_users(top_k=0) == []


# ---------------------------------------------------------------------------
# click_through_rate()
# ---------------------------------------------------------------------------


class TestClickThroughRate:
    def test_overall_rate(self):
        log = DocQueryLog()
        log.log("a", selected_result="d1", now=1.0)
        log.log("b", now=2.0)
        log.log("c", selected_result="d2", now=3.0)
        log.log("d", now=4.0)
        assert log.click_through_rate() == 0.5

    def test_empty(self):
        log = DocQueryLog()
        assert log.click_through_rate() == 0.0

    def test_per_query(self):
        log = DocQueryLog()
        log.log("foo", selected_result="d1", now=1.0)
        log.log("foo", now=2.0)
        log.log("bar", selected_result="d2", now=3.0)
        assert log.click_through_rate("foo") == 0.5
        assert log.click_through_rate("bar") == 1.0

    def test_per_query_no_matches(self):
        log = DocQueryLog()
        log.log("foo", now=1.0)
        assert log.click_through_rate("bar") == 0.0


# ---------------------------------------------------------------------------
# avg_results_for()
# ---------------------------------------------------------------------------


class TestAvgResultsFor:
    def test_basic(self):
        log = DocQueryLog()
        log.log("foo", result_count=2, now=1.0)
        log.log("foo", result_count=4, now=2.0)
        log.log("bar", result_count=10, now=3.0)
        assert log.avg_results_for("foo") == 3.0

    def test_no_matches(self):
        log = DocQueryLog()
        log.log("foo", result_count=5, now=1.0)
        assert log.avg_results_for("bar") == 0.0

    def test_case_insensitive(self):
        log = DocQueryLog()
        log.log("Foo", result_count=2, now=1.0)
        log.log("FOO", result_count=4, now=2.0)
        assert log.avg_results_for("foo") == 3.0


# ---------------------------------------------------------------------------
# find_trends()
# ---------------------------------------------------------------------------


class TestFindTrends:
    def test_recent_growth(self):
        log = DocQueryLog()
        # older window: [-200, -100), recent: [-100, 0]
        log.log("rag", now=-150.0)
        log.log("rag", now=-50.0)
        log.log("rag", now=-25.0)
        trends = log.find_trends(recent_window=100.0, older_window=100.0, now=0.0)
        rag = next(t for t in trends if t.query == "rag")
        assert rag.recent_count == 2
        assert rag.older_count == 1
        assert rag.growth_rate == 1.0

    def test_new_query(self):
        log = DocQueryLog()
        log.log("brand-new", now=-10.0)
        trends = log.find_trends(recent_window=100.0, older_window=100.0, now=0.0)
        t = next(t for t in trends if t.query == "brand-new")
        assert t.older_count == 0
        assert t.recent_count == 1
        assert t.growth_rate == 1.0  # (1-0)/max(0,1) = 1

    def test_dropped_query(self):
        log = DocQueryLog()
        log.log("old", now=-150.0)
        log.log("old", now=-120.0)
        trends = log.find_trends(recent_window=100.0, older_window=100.0, now=0.0)
        t = next(t for t in trends if t.query == "old")
        assert t.recent_count == 0
        assert t.older_count == 2
        assert t.growth_rate == -1.0

    def test_sorted_by_growth(self):
        log = DocQueryLog()
        log.log("a", now=-150.0)  # older
        log.log("a", now=-10.0)   # recent
        log.log("b", now=-150.0)  # older
        log.log("b", now=-10.0)   # recent
        log.log("b", now=-5.0)    # recent
        trends = log.find_trends(recent_window=100.0, older_window=100.0, now=0.0)
        # Both have older=1; a has 1 recent (growth 0), b has 2 (growth 1)
        first = [t for t in trends if t.query in ("a", "b")]
        assert first[0].query == "b"

    def test_empty_log(self):
        log = DocQueryLog()
        assert log.find_trends(now=0.0) == []

    def test_outside_window_ignored(self):
        log = DocQueryLog()
        log.log("ancient", now=-1000.0)
        trends = log.find_trends(recent_window=100.0, older_window=100.0, now=0.0)
        assert all(t.query != "ancient" for t in trends)


# ---------------------------------------------------------------------------
# stats()
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self):
        log = DocQueryLog()
        s = log.stats()
        assert s.total_queries == 0
        assert s.unique_queries == 0
        assert s.zero_result_count == 0
        assert s.avg_results == 0.0
        assert s.avg_latency_ms == 0.0

    def test_aggregates(self):
        log = DocQueryLog()
        log.log("a", result_count=2, latency_ms=10.0, user_id="u1", now=1.0)
        log.log("a", result_count=4, latency_ms=20.0, user_id="u2", now=2.0)
        log.log("b", result_count=0, latency_ms=30.0, user_id="u1", now=3.0)
        s = log.stats()
        assert s.total_queries == 3
        assert s.unique_queries == 2
        assert s.zero_result_count == 1
        assert s.avg_results == pytest.approx(2.0)
        assert s.avg_latency_ms == pytest.approx(20.0)

    def test_top_lists(self):
        log = DocQueryLog()
        for _ in range(3):
            log.log("a", user_id="u1", now=1.0)
        log.log("b", user_id="u2", now=2.0)
        s = log.stats()
        assert s.top_queries[0] == ("a", 3)
        assert s.top_users[0] == ("u1", 3)


# ---------------------------------------------------------------------------
# clear()
# ---------------------------------------------------------------------------


class TestClear:
    def test_clear_empties(self):
        log = DocQueryLog()
        log.log("a", now=1.0)
        log.log("b", now=2.0)
        log.clear()
        assert log.total_queries == 0
        assert log.recent() == []

    def test_clear_preserves_id_counter(self):
        log = DocQueryLog()
        log.log("a", now=1.0)
        log.clear()
        e = log.log("b", now=2.0)
        # Counter not reset (next id is 2 after first log)
        assert e.query_id == 2


# ---------------------------------------------------------------------------
# total_queries property
# ---------------------------------------------------------------------------


class TestTotalQueries:
    def test_zero(self):
        assert DocQueryLog().total_queries == 0

    def test_grows(self):
        log = DocQueryLog()
        log.log("a", now=1.0)
        log.log("b", now=2.0)
        assert log.total_queries == 2

    def test_is_property(self):
        log = DocQueryLog()
        # Calling as attr, not method
        assert isinstance(DocQueryLog.total_queries, property)
        _ = log.total_queries  # no parentheses needed


# ---------------------------------------------------------------------------
# purge_older_than()
# ---------------------------------------------------------------------------


class TestPurgeOlderThan:
    def test_basic(self):
        log = DocQueryLog()
        log.log("a", now=10.0)
        log.log("b", now=20.0)
        log.log("c", now=30.0)
        removed = log.purge_older_than(older_than=15.0, now=30.0)
        # cutoff = 30 - 15 = 15; entries < 15 removed -> "a"
        assert removed == 1
        remaining = {e.query for e in log.recent(10)}
        assert remaining == {"b", "c"}

    def test_nothing_to_purge(self):
        log = DocQueryLog()
        log.log("a", now=10.0)
        removed = log.purge_older_than(older_than=100.0, now=20.0)
        assert removed == 0
        assert log.total_queries == 1

    def test_purge_all(self):
        log = DocQueryLog()
        log.log("a", now=1.0)
        log.log("b", now=2.0)
        removed = log.purge_older_than(older_than=0.0, now=100.0)
        assert removed == 2
        assert log.total_queries == 0


# ---------------------------------------------------------------------------
# Max entries / FIFO eviction
# ---------------------------------------------------------------------------


class TestMaxEntries:
    def test_eviction(self):
        log = DocQueryLog(max_entries=3)
        log.log("a", now=1.0)
        log.log("b", now=2.0)
        log.log("c", now=3.0)
        log.log("d", now=4.0)
        assert log.total_queries == 3
        queries = [e.query for e in log.recent(10)]
        # most recent first
        assert queries == ["d", "c", "b"]

    def test_ids_monotonic_after_eviction(self):
        log = DocQueryLog(max_entries=2)
        log.log("a", now=1.0)
        log.log("b", now=2.0)
        log.log("c", now=3.0)
        ids = [e.query_id for e in log.recent(10)]
        # latest two are id=3 (c) then id=2 (b)
        assert ids == [3, 2]

    def test_invalid_max_entries(self):
        with pytest.raises(ValueError):
            DocQueryLog(max_entries=0)
        with pytest.raises(ValueError):
            DocQueryLog(max_entries=-1)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_query_string(self):
        log = DocQueryLog()
        log.log("", now=1.0)
        assert log.count_query("") == 1

    def test_unicode_query(self):
        log = DocQueryLog()
        log.log("агент памяти", now=1.0)
        assert log.count_query("агент памяти") == 1

    def test_negative_timestamps(self):
        log = DocQueryLog()
        log.log("a", now=-100.0)
        log.log("b", now=-50.0)
        # find_trends with now=0 should still work
        trends = log.find_trends(recent_window=60.0, older_window=60.0, now=0.0)
        assert any(t.query == "b" for t in trends)

    def test_concurrent_log_and_stats(self):
        log = DocQueryLog()

        def writer():
            for i in range(100):
                log.log("q", result_count=i, now=float(i))

        def reader():
            for _ in range(50):
                log.stats()
                log.recent(5)
                log.top_queries()

        ts = [threading.Thread(target=writer) for _ in range(2)] + \
             [threading.Thread(target=reader) for _ in range(2)]
        for t in ts:
            t.start()
        for t in ts:
            t.join()
        assert log.total_queries == 200
