"""Tests for E375 DocPageviewRecorder."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_pageview_recorder import (
    DocPageviewRecorder,
    DocViewStats,
    Pageview,
    RecorderStats,
)


# --------------------------------------------------------------------- Pageview
class TestPageviewDataclass:
    def test_defaults(self):
        v = Pageview()
        assert v.view_id == 0
        assert v.doc_id == ""
        assert v.user_id == ""
        assert v.referrer == ""
        assert v.viewed_at == 0.0

    def test_construct_with_fields(self):
        v = Pageview(view_id=1, doc_id="d1", user_id="u1",
                     referrer="r", viewed_at=10.0)
        assert v.view_id == 1
        assert v.doc_id == "d1"
        assert v.user_id == "u1"
        assert v.referrer == "r"
        assert v.viewed_at == 10.0

    def test_equality(self):
        a = Pageview(view_id=1, doc_id="d", user_id="u", viewed_at=1.0)
        b = Pageview(view_id=1, doc_id="d", user_id="u", viewed_at=1.0)
        assert a == b


# ----------------------------------------------------------------- DocViewStats
class TestDocViewStatsDataclass:
    def test_construct(self):
        s = DocViewStats(doc_id="d", total_views=3, unique_users=2,
                         first_viewed_at=1.0, last_viewed_at=5.0)
        assert s.doc_id == "d"
        assert s.total_views == 3
        assert s.unique_users == 2
        assert s.first_viewed_at == 1.0
        assert s.last_viewed_at == 5.0

    def test_equality(self):
        a = DocViewStats("d", 1, 1, 0.0, 0.0)
        b = DocViewStats("d", 1, 1, 0.0, 0.0)
        assert a == b


# ---------------------------------------------------------------- RecorderStats
class TestRecorderStatsDataclass:
    def test_construct(self):
        s = RecorderStats(total_pageviews=10, unique_docs=3,
                          unique_users=4, anonymous_views=2)
        assert s.total_pageviews == 10
        assert s.unique_docs == 3
        assert s.unique_users == 4
        assert s.anonymous_views == 2

    def test_equality(self):
        a = RecorderStats(1, 1, 1, 0)
        b = RecorderStats(1, 1, 1, 0)
        assert a == b


# ----------------------------------------------------------------- Construction
class TestConstruction:
    def test_empty(self):
        r = DocPageviewRecorder()
        assert r.view_count("d") == 0
        assert r.all_doc_ids() == []

    def test_stats_on_empty(self):
        r = DocPageviewRecorder()
        s = r.stats()
        assert s.total_pageviews == 0
        assert s.unique_docs == 0
        assert s.unique_users == 0
        assert s.anonymous_views == 0


# ----------------------------------------------------------------------- Record
class TestRecord:
    def test_record_returns_pageview(self):
        r = DocPageviewRecorder()
        v = r.record("d1", "u1", now=10.0)
        assert isinstance(v, Pageview)
        assert v.doc_id == "d1"
        assert v.user_id == "u1"
        assert v.viewed_at == 10.0

    def test_view_id_starts_at_1(self):
        r = DocPageviewRecorder()
        v = r.record("d", now=1.0)
        assert v.view_id == 1

    def test_view_ids_increment(self):
        r = DocPageviewRecorder()
        a = r.record("d", now=1.0)
        b = r.record("d", now=2.0)
        c = r.record("d", now=3.0)
        assert (a.view_id, b.view_id, c.view_id) == (1, 2, 3)

    def test_record_anonymous(self):
        r = DocPageviewRecorder()
        v = r.record("d", now=1.0)
        assert v.user_id == ""

    def test_record_with_referrer(self):
        r = DocPageviewRecorder()
        v = r.record("d", referrer="https://example.com", now=1.0)
        assert v.referrer == "https://example.com"

    def test_record_uses_time_when_now_none(self):
        r = DocPageviewRecorder()
        v = r.record("d")
        assert v.viewed_at > 0.0


# ---------------------------------------------------------------- ViewsForDoc
class TestViewsForDoc:
    def test_empty(self):
        r = DocPageviewRecorder()
        assert r.views_for_doc("d") == []

    def test_returns_recent_first(self):
        r = DocPageviewRecorder()
        r.record("d", now=1.0)
        r.record("d", now=2.0)
        r.record("d", now=3.0)
        views = r.views_for_doc("d")
        assert [v.viewed_at for v in views] == [3.0, 2.0, 1.0]

    def test_filtered_by_doc(self):
        r = DocPageviewRecorder()
        r.record("d1", now=1.0)
        r.record("d2", now=2.0)
        assert len(r.views_for_doc("d1")) == 1
        assert r.views_for_doc("d1")[0].doc_id == "d1"

    def test_limit(self):
        r = DocPageviewRecorder()
        for i in range(5):
            r.record("d", now=float(i))
        assert len(r.views_for_doc("d", limit=3)) == 3

    def test_limit_zero(self):
        r = DocPageviewRecorder()
        r.record("d", now=1.0)
        assert r.views_for_doc("d", limit=0) == []


# ----------------------------------------------------------------- ViewCount
class TestViewCount:
    def test_empty(self):
        assert DocPageviewRecorder().view_count("d") == 0

    def test_single(self):
        r = DocPageviewRecorder()
        r.record("d", now=1.0)
        assert r.view_count("d") == 1

    def test_multiple(self):
        r = DocPageviewRecorder()
        for _ in range(5):
            r.record("d", now=1.0)
        assert r.view_count("d") == 5

    def test_separate_docs(self):
        r = DocPageviewRecorder()
        r.record("d1", now=1.0)
        r.record("d2", now=1.0)
        r.record("d1", now=2.0)
        assert r.view_count("d1") == 2
        assert r.view_count("d2") == 1


# -------------------------------------------------------------- UniqueUserCount
class TestUniqueUserCount:
    def test_empty(self):
        assert DocPageviewRecorder().unique_user_count("d") == 0

    def test_unique_users(self):
        r = DocPageviewRecorder()
        r.record("d", "u1", now=1.0)
        r.record("d", "u2", now=2.0)
        r.record("d", "u1", now=3.0)
        assert r.unique_user_count("d") == 2

    def test_anonymous_excluded(self):
        r = DocPageviewRecorder()
        r.record("d", "", now=1.0)
        r.record("d", "", now=2.0)
        r.record("d", "u1", now=3.0)
        assert r.unique_user_count("d") == 1

    def test_only_anonymous(self):
        r = DocPageviewRecorder()
        r.record("d", "", now=1.0)
        r.record("d", "", now=2.0)
        assert r.unique_user_count("d") == 0


# --------------------------------------------------------------- StatsForDoc
class TestStatsForDoc:
    def test_none_for_empty(self):
        assert DocPageviewRecorder().stats_for_doc("d") is None

    def test_first_last(self):
        r = DocPageviewRecorder()
        r.record("d", "u1", now=5.0)
        r.record("d", "u2", now=10.0)
        r.record("d", "u1", now=1.0)
        s = r.stats_for_doc("d")
        assert s is not None
        assert s.first_viewed_at == 1.0
        assert s.last_viewed_at == 10.0

    def test_total_views(self):
        r = DocPageviewRecorder()
        for i in range(4):
            r.record("d", now=float(i))
        s = r.stats_for_doc("d")
        assert s.total_views == 4

    def test_unique_users_excludes_anon(self):
        r = DocPageviewRecorder()
        r.record("d", "", now=1.0)
        r.record("d", "u1", now=2.0)
        r.record("d", "u2", now=3.0)
        s = r.stats_for_doc("d")
        assert s.unique_users == 2

    def test_doc_id_matches(self):
        r = DocPageviewRecorder()
        r.record("xyz", now=1.0)
        s = r.stats_for_doc("xyz")
        assert s.doc_id == "xyz"


# ------------------------------------------------------------------ TopDocs
class TestTopDocs:
    def test_empty(self):
        assert DocPageviewRecorder().top_docs() == []

    def test_sorted_desc(self):
        r = DocPageviewRecorder()
        r.record("a", now=1.0)
        r.record("b", now=1.0)
        r.record("b", now=2.0)
        r.record("c", now=1.0)
        r.record("c", now=2.0)
        r.record("c", now=3.0)
        top = r.top_docs()
        assert top == [("c", 3), ("b", 2), ("a", 1)]

    def test_tiebreak_by_doc_id(self):
        r = DocPageviewRecorder()
        r.record("zebra", now=1.0)
        r.record("apple", now=1.0)
        top = r.top_docs()
        # equal counts → doc_id asc
        assert top[0][0] == "apple"
        assert top[1][0] == "zebra"

    def test_limit(self):
        r = DocPageviewRecorder()
        for d in "abcdef":
            r.record(d, now=1.0)
        top = r.top_docs(limit=3)
        assert len(top) == 3


# ---------------------------------------------------------------- ViewsByUser
class TestViewsByUser:
    def test_empty(self):
        assert DocPageviewRecorder().views_by_user("u1") == []

    def test_recent_first(self):
        r = DocPageviewRecorder()
        r.record("d1", "u1", now=1.0)
        r.record("d2", "u1", now=2.0)
        r.record("d3", "u1", now=3.0)
        views = r.views_by_user("u1")
        assert [v.viewed_at for v in views] == [3.0, 2.0, 1.0]

    def test_filter(self):
        r = DocPageviewRecorder()
        r.record("d", "u1", now=1.0)
        r.record("d", "u2", now=2.0)
        views = r.views_by_user("u1")
        assert len(views) == 1
        assert views[0].user_id == "u1"

    def test_limit(self):
        r = DocPageviewRecorder()
        for i in range(5):
            r.record("d", "u1", now=float(i))
        assert len(r.views_by_user("u1", limit=2)) == 2

    def test_anonymous_with_empty_id(self):
        r = DocPageviewRecorder()
        r.record("d", "", now=1.0)
        r.record("d", "u1", now=2.0)
        # querying "" returns the anonymous view
        anon = r.views_by_user("")
        assert len(anon) == 1


# --------------------------------------------------------------- ViewsInRange
class TestViewsInRange:
    def test_empty(self):
        assert DocPageviewRecorder().views_in_range(0, 100) == []

    def test_inclusive_bounds(self):
        r = DocPageviewRecorder()
        r.record("d", now=1.0)
        r.record("d", now=5.0)
        r.record("d", now=10.0)
        result = r.views_in_range(1.0, 10.0)
        assert len(result) == 3

    def test_excludes_outside(self):
        r = DocPageviewRecorder()
        r.record("d", now=1.0)
        r.record("d", now=5.0)
        r.record("d", now=10.0)
        result = r.views_in_range(2.0, 9.0)
        assert len(result) == 1
        assert result[0].viewed_at == 5.0

    def test_sorted_asc(self):
        r = DocPageviewRecorder()
        r.record("d", now=5.0)
        r.record("d", now=1.0)
        r.record("d", now=3.0)
        result = r.views_in_range(0.0, 10.0)
        assert [v.viewed_at for v in result] == [1.0, 3.0, 5.0]

    def test_doc_filter(self):
        r = DocPageviewRecorder()
        r.record("d1", now=1.0)
        r.record("d2", now=2.0)
        r.record("d1", now=3.0)
        result = r.views_in_range(0.0, 10.0, doc_id="d1")
        assert len(result) == 2
        assert all(v.doc_id == "d1" for v in result)


# ------------------------------------------------------------------ ClearDoc
class TestClearDoc:
    def test_clear_returns_count(self):
        r = DocPageviewRecorder()
        r.record("d", now=1.0)
        r.record("d", now=2.0)
        assert r.clear_doc("d") == 2

    def test_clear_missing(self):
        assert DocPageviewRecorder().clear_doc("nope") == 0

    def test_clear_makes_count_zero(self):
        r = DocPageviewRecorder()
        r.record("d", now=1.0)
        r.clear_doc("d")
        assert r.view_count("d") == 0

    def test_clear_only_one_doc(self):
        r = DocPageviewRecorder()
        r.record("d1", now=1.0)
        r.record("d2", now=2.0)
        r.clear_doc("d1")
        assert r.view_count("d1") == 0
        assert r.view_count("d2") == 1


# ------------------------------------------------------------------ ClearAll
class TestClearAll:
    def test_clear_all_count(self):
        r = DocPageviewRecorder()
        r.record("d1", now=1.0)
        r.record("d2", now=2.0)
        r.record("d3", now=3.0)
        assert r.clear_all() == 3

    def test_clear_all_empty(self):
        assert DocPageviewRecorder().clear_all() == 0

    def test_after_clear_all(self):
        r = DocPageviewRecorder()
        r.record("d", now=1.0)
        r.clear_all()
        assert r.view_count("d") == 0
        assert r.all_doc_ids() == []
        v = r.record("d", now=2.0)
        # next_id reset to 1
        assert v.view_id == 1


# ------------------------------------------------------------------ AllDocIds
class TestAllDocIds:
    def test_empty(self):
        assert DocPageviewRecorder().all_doc_ids() == []

    def test_sorted(self):
        r = DocPageviewRecorder()
        r.record("zebra", now=1.0)
        r.record("apple", now=2.0)
        r.record("mango", now=3.0)
        assert r.all_doc_ids() == ["apple", "mango", "zebra"]

    def test_unique(self):
        r = DocPageviewRecorder()
        r.record("d", now=1.0)
        r.record("d", now=2.0)
        assert r.all_doc_ids() == ["d"]

    def test_excludes_cleared(self):
        r = DocPageviewRecorder()
        r.record("d1", now=1.0)
        r.record("d2", now=2.0)
        r.clear_doc("d1")
        assert r.all_doc_ids() == ["d2"]


# --------------------------------------------------------------------- Stats
class TestStats:
    def test_totals(self):
        r = DocPageviewRecorder()
        r.record("d1", "u1", now=1.0)
        r.record("d2", "u2", now=2.0)
        r.record("d1", "u1", now=3.0)
        s = r.stats()
        assert s.total_pageviews == 3
        assert s.unique_docs == 2
        assert s.unique_users == 2
        assert s.anonymous_views == 0

    def test_anonymous_views(self):
        r = DocPageviewRecorder()
        r.record("d", "", now=1.0)
        r.record("d", "", now=2.0)
        r.record("d", "u1", now=3.0)
        s = r.stats()
        assert s.anonymous_views == 2
        assert s.unique_users == 1

    def test_unique_users_dedup(self):
        r = DocPageviewRecorder()
        r.record("d", "u1", now=1.0)
        r.record("d", "u1", now=2.0)
        r.record("d", "u1", now=3.0)
        s = r.stats()
        assert s.unique_users == 1

    def test_empty(self):
        s = DocPageviewRecorder().stats()
        assert s == RecorderStats(0, 0, 0, 0)


# ------------------------------------------------------------- ThreadSafety
class TestThreadSafety:
    def test_concurrent_record(self):
        r = DocPageviewRecorder()
        n_threads = 10
        per_thread = 50

        def worker(tid):
            for i in range(per_thread):
                r.record(f"d{tid}", f"u{tid}", now=float(i))

        threads = [threading.Thread(target=worker, args=(t,))
                   for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert r.stats().total_pageviews == n_threads * per_thread

    def test_concurrent_view_ids_unique(self):
        r = DocPageviewRecorder()

        def worker():
            for _ in range(20):
                r.record("d", now=1.0)

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # all view_ids unique
        ids = [v.view_id for v in r.views_for_doc("d")]
        assert len(ids) == len(set(ids))
        assert len(ids) == 8 * 20
