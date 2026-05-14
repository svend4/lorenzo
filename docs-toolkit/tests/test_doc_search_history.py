"""Tests for docstoolkit.doc_search_history."""
import threading

import pytest

from docstoolkit.doc_search_history import (
    DocSearchHistory,
    HistoryStats,
    QueryStats,
    SearchQuery,
)


# --------------------------------------------------------------------- helpers
def _h():
    return DocSearchHistory()


def _seed(h, user="u1", text="hello", n=3, base_now=1.0, result_count=5):
    out = []
    for i in range(n):
        q = h.record(user, text, result_count=result_count, now=base_now + i)
        out.append(q)
    return out


# --------------------------------------------------------------------- SearchQuery dataclass
class TestSearchQueryDataclass:
    def test_basic_construction(self):
        q = SearchQuery(query_id=1, user_id="u", query_text="t")
        assert q.query_id == 1
        assert q.user_id == "u"
        assert q.query_text == "t"

    def test_default_executed_at_zero(self):
        q = SearchQuery(query_id=1, user_id="u", query_text="t")
        assert q.executed_at == 0.0

    def test_default_result_count_zero(self):
        q = SearchQuery(query_id=1, user_id="u", query_text="t")
        assert q.result_count == 0

    def test_default_clicked_doc_id_none(self):
        q = SearchQuery(query_id=1, user_id="u", query_text="t")
        assert q.clicked_doc_id is None

    def test_with_all_fields(self):
        q = SearchQuery(
            query_id=7, user_id="alice", query_text="foo",
            executed_at=1.5, result_count=10, clicked_doc_id="d1",
        )
        assert q.executed_at == 1.5
        assert q.result_count == 10
        assert q.clicked_doc_id == "d1"

    def test_equality(self):
        a = SearchQuery(query_id=1, user_id="u", query_text="t")
        b = SearchQuery(query_id=1, user_id="u", query_text="t")
        assert a == b


# --------------------------------------------------------------------- QueryStats dataclass
class TestQueryStatsDataclass:
    def test_construction(self):
        s = QueryStats(
            query_text="x", total_executions=3, unique_users=2,
            avg_result_count=4.5, click_through_count=1,
        )
        assert s.query_text == "x"
        assert s.total_executions == 3
        assert s.unique_users == 2
        assert s.avg_result_count == 4.5
        assert s.click_through_count == 1

    def test_equality(self):
        a = QueryStats("x", 1, 1, 1.0, 0)
        b = QueryStats("x", 1, 1, 1.0, 0)
        assert a == b


# --------------------------------------------------------------------- HistoryStats dataclass
class TestHistoryStatsDataclass:
    def test_construction(self):
        s = HistoryStats(total_queries=10, unique_users=2, unique_query_texts=5)
        assert s.total_queries == 10
        assert s.unique_users == 2
        assert s.unique_query_texts == 5

    def test_equality(self):
        assert HistoryStats(1, 1, 1) == HistoryStats(1, 1, 1)


# --------------------------------------------------------------------- Construction
class TestConstruction:
    def test_empty_history(self):
        h = _h()
        assert h.stats().total_queries == 0

    def test_initial_next_id(self):
        h = _h()
        q = h.record("u", "t")
        assert q.query_id == 1

    def test_no_users_initially(self):
        h = _h()
        assert h.all_users() == []

    def test_no_recent_queries(self):
        h = _h()
        assert h.recent_queries() == []


# --------------------------------------------------------------------- record
class TestRecord:
    def test_returns_search_query(self):
        h = _h()
        q = h.record("u", "t")
        assert isinstance(q, SearchQuery)

    def test_id_starts_at_one(self):
        h = _h()
        assert h.record("u", "t").query_id == 1

    def test_id_increments(self):
        h = _h()
        ids = [h.record("u", "t").query_id for _ in range(5)]
        assert ids == [1, 2, 3, 4, 5]

    def test_explicit_now(self):
        h = _h()
        q = h.record("u", "t", now=1234.5)
        assert q.executed_at == 1234.5

    def test_default_now_set(self):
        h = _h()
        q = h.record("u", "t")
        assert q.executed_at > 0

    def test_result_count_stored(self):
        h = _h()
        q = h.record("u", "t", result_count=42)
        assert q.result_count == 42

    def test_clicked_doc_id_stored(self):
        h = _h()
        q = h.record("u", "t", clicked_doc_id="d99")
        assert q.clicked_doc_id == "d99"

    def test_user_indexed(self):
        h = _h()
        h.record("alice", "t")
        assert "alice" in h.all_users()

    def test_text_indexed(self):
        h = _h()
        h.record("u", "hello")
        assert h.queries_for_text("hello")


# --------------------------------------------------------------------- get_query
class TestGetQuery:
    def test_found(self):
        h = _h()
        q = h.record("u", "t")
        assert h.get_query(q.query_id) is q or h.get_query(q.query_id) == q

    def test_not_found(self):
        h = _h()
        assert h.get_query(999) is None

    def test_zero_id_not_found(self):
        h = _h()
        h.record("u", "t")
        assert h.get_query(0) is None

    def test_negative_id_not_found(self):
        h = _h()
        assert h.get_query(-1) is None


# --------------------------------------------------------------------- record_click
class TestRecordClick:
    def test_sets_clicked_doc_id(self):
        h = _h()
        q = h.record("u", "t")
        h.record_click(q.query_id, "d1")
        assert h.get_query(q.query_id).clicked_doc_id == "d1"

    def test_returns_true_when_found(self):
        h = _h()
        q = h.record("u", "t")
        assert h.record_click(q.query_id, "d1") is True

    def test_returns_false_when_missing(self):
        h = _h()
        assert h.record_click(999, "d1") is False

    def test_overwrite(self):
        h = _h()
        q = h.record("u", "t", clicked_doc_id="old")
        h.record_click(q.query_id, "new")
        assert h.get_query(q.query_id).clicked_doc_id == "new"


# --------------------------------------------------------------------- queries_for_user
class TestQueriesForUser:
    def test_empty_user(self):
        h = _h()
        assert h.queries_for_user("ghost") == []

    def test_most_recent_first(self):
        h = _h()
        h.record("u", "a", now=1.0)
        h.record("u", "b", now=2.0)
        h.record("u", "c", now=3.0)
        texts = [q.query_text for q in h.queries_for_user("u")]
        assert texts == ["c", "b", "a"]

    def test_limit(self):
        h = _h()
        _seed(h, n=5)
        assert len(h.queries_for_user("u1", limit=2)) == 2

    def test_limit_none_returns_all(self):
        h = _h()
        _seed(h, n=4)
        assert len(h.queries_for_user("u1")) == 4

    def test_only_user_queries(self):
        h = _h()
        h.record("a", "x")
        h.record("b", "y")
        out = h.queries_for_user("a")
        assert len(out) == 1 and out[0].user_id == "a"


# --------------------------------------------------------------------- queries_for_text
class TestQueriesForText:
    def test_empty_text(self):
        h = _h()
        assert h.queries_for_text("nope") == []

    def test_sorted_by_executed_at(self):
        h = _h()
        h.record("u", "q", now=3.0)
        h.record("u", "q", now=1.0)
        h.record("u", "q", now=2.0)
        out = h.queries_for_text("q")
        assert [q.executed_at for q in out] == [1.0, 2.0, 3.0]

    def test_only_matching_text(self):
        h = _h()
        h.record("u", "a")
        h.record("u", "b")
        assert len(h.queries_for_text("a")) == 1


# --------------------------------------------------------------------- recent_queries
class TestRecentQueries:
    def test_empty(self):
        assert _h().recent_queries() == []

    def test_most_recent_first(self):
        h = _h()
        h.record("u", "a", now=1.0)
        h.record("u", "b", now=2.0)
        h.record("u", "c", now=3.0)
        out = h.recent_queries()
        assert [q.query_text for q in out] == ["c", "b", "a"]

    def test_limit(self):
        h = _h()
        for i in range(10):
            h.record("u", f"q{i}", now=float(i))
        assert len(h.recent_queries(limit=3)) == 3

    def test_limit_larger_than_size(self):
        h = _h()
        h.record("u", "x", now=1.0)
        assert len(h.recent_queries(limit=100)) == 1

    def test_default_limit_ten(self):
        h = _h()
        for i in range(25):
            h.record("u", f"q{i}", now=float(i))
        assert len(h.recent_queries()) == 10


# --------------------------------------------------------------------- top_queries
class TestTopQueries:
    def test_empty(self):
        assert _h().top_queries() == []

    def test_sorted_by_count_desc(self):
        h = _h()
        for _ in range(3):
            h.record("u", "popular")
        for _ in range(1):
            h.record("u", "rare")
        out = h.top_queries()
        assert out[0] == ("popular", 3)
        assert out[1] == ("rare", 1)

    def test_tie_break_by_text_asc(self):
        h = _h()
        h.record("u", "bbb")
        h.record("u", "aaa")
        out = h.top_queries()
        assert out[0][0] == "aaa"
        assert out[1][0] == "bbb"

    def test_limit(self):
        h = _h()
        for t in ["a", "b", "c", "d"]:
            h.record("u", t)
        assert len(h.top_queries(limit=2)) == 2

    def test_count_correct(self):
        h = _h()
        for _ in range(5):
            h.record("u", "x")
        assert h.top_queries()[0] == ("x", 5)


# --------------------------------------------------------------------- query_stats
class TestQueryStats:
    def test_none_for_unknown(self):
        assert _h().query_stats("ghost") is None

    def test_total_executions(self):
        h = _h()
        _seed(h, n=4, text="q")
        assert h.query_stats("q").total_executions == 4

    def test_unique_users(self):
        h = _h()
        h.record("a", "q")
        h.record("b", "q")
        h.record("a", "q")
        assert h.query_stats("q").unique_users == 2

    def test_avg_result_count(self):
        h = _h()
        h.record("u", "q", result_count=2)
        h.record("u", "q", result_count=4)
        assert h.query_stats("q").avg_result_count == 3.0

    def test_click_through_count(self):
        h = _h()
        h.record("u", "q", clicked_doc_id="d1")
        h.record("u", "q")
        h.record("u", "q", clicked_doc_id="d2")
        assert h.query_stats("q").click_through_count == 2

    def test_query_text_in_stats(self):
        h = _h()
        h.record("u", "hello")
        assert h.query_stats("hello").query_text == "hello"


# --------------------------------------------------------------------- clear_user
class TestClearUser:
    def test_returns_count(self):
        h = _h()
        _seed(h, n=3)
        assert h.clear_user("u1") == 3

    def test_returns_zero_for_unknown(self):
        h = _h()
        assert h.clear_user("ghost") == 0

    def test_removes_from_user_index(self):
        h = _h()
        _seed(h, n=2)
        h.clear_user("u1")
        assert h.queries_for_user("u1") == []

    def test_removes_from_text_index(self):
        h = _h()
        h.record("u1", "only-u1")
        h.clear_user("u1")
        assert h.queries_for_text("only-u1") == []

    def test_preserves_other_users(self):
        h = _h()
        h.record("u1", "x")
        h.record("u2", "y")
        h.clear_user("u1")
        assert len(h.queries_for_user("u2")) == 1

    def test_global_list_preserved(self):
        h = _h()
        q = h.record("u1", "x")
        h.clear_user("u1")
        # get_query still returns the entry from the global list
        assert h.get_query(q.query_id) is not None


# --------------------------------------------------------------------- all_users
class TestAllUsers:
    def test_empty(self):
        assert _h().all_users() == []

    def test_sorted(self):
        h = _h()
        h.record("charlie", "x")
        h.record("alice", "x")
        h.record("bob", "x")
        assert h.all_users() == ["alice", "bob", "charlie"]

    def test_unique(self):
        h = _h()
        h.record("a", "x")
        h.record("a", "y")
        assert h.all_users() == ["a"]


# --------------------------------------------------------------------- stats
class TestStats:
    def test_empty(self):
        s = _h().stats()
        assert s.total_queries == 0
        assert s.unique_users == 0
        assert s.unique_query_texts == 0

    def test_total_queries(self):
        h = _h()
        _seed(h, n=4)
        assert h.stats().total_queries == 4

    def test_unique_users(self):
        h = _h()
        h.record("a", "x")
        h.record("b", "x")
        h.record("a", "y")
        assert h.stats().unique_users == 2

    def test_unique_query_texts(self):
        h = _h()
        h.record("a", "x")
        h.record("a", "y")
        h.record("a", "x")
        assert h.stats().unique_query_texts == 2


# --------------------------------------------------------------------- thread safety
class TestThreadSafety:
    def test_concurrent_record(self):
        h = _h()
        N = 50
        T = 8

        def worker():
            for i in range(N):
                h.record("u", f"q{i % 5}", result_count=i)

        threads = [threading.Thread(target=worker) for _ in range(T)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert h.stats().total_queries == N * T

    def test_concurrent_record_unique_ids(self):
        h = _h()
        ids: list[int] = []
        lock = threading.Lock()

        def worker():
            for _ in range(50):
                q = h.record("u", "q")
                with lock:
                    ids.append(q.query_id)

        threads = [threading.Thread(target=worker) for _ in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(ids) == len(set(ids))

    def test_concurrent_record_and_click(self):
        h = _h()

        def writer():
            for i in range(40):
                h.record("u", f"q{i}", result_count=i)

        def clicker():
            for i in range(1, 40):
                h.record_click(i, f"d{i}")

        ts = [threading.Thread(target=writer) for _ in range(3)]
        ts += [threading.Thread(target=clicker) for _ in range(2)]
        for t in ts:
            t.start()
        for t in ts:
            t.join()
        # No exceptions and totals at least sensible
        assert h.stats().total_queries == 120
