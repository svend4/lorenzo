"""Tests for E357 DocBreadcrumbStore."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_breadcrumb_store import (
    Breadcrumb,
    BreadcrumbStats,
    DocBreadcrumbStore,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestBreadcrumbDataclass:
    def test_required_fields(self):
        c = Breadcrumb(entry_id=1, user_id="u", doc_id="d")
        assert c.entry_id == 1
        assert c.user_id == "u"
        assert c.doc_id == "d"

    def test_default_title(self):
        c = Breadcrumb(entry_id=1, user_id="u", doc_id="d")
        assert c.title == ""

    def test_default_visited_at(self):
        c = Breadcrumb(entry_id=1, user_id="u", doc_id="d")
        assert c.visited_at == 0.0

    def test_explicit_title_and_time(self):
        c = Breadcrumb(
            entry_id=2,
            user_id="u",
            doc_id="d",
            title="hello",
            visited_at=42.5,
        )
        assert c.title == "hello"
        assert c.visited_at == 42.5

    def test_equality(self):
        a = Breadcrumb(entry_id=1, user_id="u", doc_id="d")
        b = Breadcrumb(entry_id=1, user_id="u", doc_id="d")
        assert a == b


class TestBreadcrumbStatsDataclass:
    def test_fields(self):
        s = BreadcrumbStats(total_entries=3, unique_users=2, unique_docs=2)
        assert s.total_entries == 3
        assert s.unique_users == 2
        assert s.unique_docs == 2

    def test_equality(self):
        a = BreadcrumbStats(total_entries=1, unique_users=1, unique_docs=1)
        b = BreadcrumbStats(total_entries=1, unique_users=1, unique_docs=1)
        assert a == b

    def test_inequality(self):
        a = BreadcrumbStats(total_entries=1, unique_users=1, unique_docs=1)
        b = BreadcrumbStats(total_entries=2, unique_users=1, unique_docs=1)
        assert a != b


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_default_max(self):
        s = DocBreadcrumbStore()
        assert s._max_per_user == 50

    def test_custom_max(self):
        s = DocBreadcrumbStore(max_per_user=10)
        assert s._max_per_user == 10

    def test_empty_on_init(self):
        s = DocBreadcrumbStore()
        assert s.stats().total_entries == 0
        assert s.users_with_history() == []

    def test_invalid_max(self):
        with pytest.raises(ValueError):
            DocBreadcrumbStore(max_per_user=0)

    def test_invalid_negative_max(self):
        with pytest.raises(ValueError):
            DocBreadcrumbStore(max_per_user=-3)


# ---------------------------------------------------------------------------
# visit()
# ---------------------------------------------------------------------------


class TestVisit:
    def test_returns_breadcrumb(self):
        s = DocBreadcrumbStore()
        c = s.visit("u1", "d1")
        assert isinstance(c, Breadcrumb)

    def test_id_starts_at_one(self):
        s = DocBreadcrumbStore()
        c = s.visit("u1", "d1")
        assert c.entry_id == 1

    def test_id_increments(self):
        s = DocBreadcrumbStore()
        a = s.visit("u1", "d1")
        b = s.visit("u1", "d2")
        c = s.visit("u2", "d3")
        assert a.entry_id == 1
        assert b.entry_id == 2
        assert c.entry_id == 3

    def test_title_recorded(self):
        s = DocBreadcrumbStore()
        c = s.visit("u1", "d1", title="My Doc")
        assert c.title == "My Doc"

    def test_explicit_now(self):
        s = DocBreadcrumbStore()
        c = s.visit("u1", "d1", now=123.0)
        assert c.visited_at == 123.0

    def test_default_now(self):
        s = DocBreadcrumbStore()
        c = s.visit("u1", "d1")
        assert c.visited_at > 0

    def test_visit_stored(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        assert s.stats().total_entries == 1

    def test_trim_drops_oldest(self):
        s = DocBreadcrumbStore(max_per_user=3)
        for i in range(5):
            s.visit("u1", f"d{i}")
        trail = s.trail_for("u1")
        doc_ids = [c.doc_id for c in trail]
        # most recent first; oldest two dropped
        assert doc_ids == ["d4", "d3", "d2"]

    def test_trim_removes_entry_from_entries(self):
        s = DocBreadcrumbStore(max_per_user=2)
        a = s.visit("u1", "d1")
        s.visit("u1", "d2")
        s.visit("u1", "d3")
        # entry a should be gone
        assert a.entry_id not in s._entries
        assert s.stats().total_entries == 2


# ---------------------------------------------------------------------------
# trail_for()
# ---------------------------------------------------------------------------


class TestTrailFor:
    def test_empty_user(self):
        s = DocBreadcrumbStore()
        assert s.trail_for("nobody") == []

    def test_most_recent_first(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        s.visit("u1", "d2")
        s.visit("u1", "d3")
        trail = s.trail_for("u1")
        assert [c.doc_id for c in trail] == ["d3", "d2", "d1"]

    def test_default_limit_is_max_per_user(self):
        s = DocBreadcrumbStore(max_per_user=4)
        for i in range(4):
            s.visit("u1", f"d{i}")
        assert len(s.trail_for("u1")) == 4

    def test_explicit_limit_overrides(self):
        s = DocBreadcrumbStore()
        for i in range(10):
            s.visit("u1", f"d{i}")
        trail = s.trail_for("u1", limit=3)
        assert len(trail) == 3
        assert [c.doc_id for c in trail] == ["d9", "d8", "d7"]

    def test_explicit_limit_zero(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        assert s.trail_for("u1", limit=0) == []

    def test_isolation_between_users(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        s.visit("u2", "d2")
        assert [c.doc_id for c in s.trail_for("u1")] == ["d1"]
        assert [c.doc_id for c in s.trail_for("u2")] == ["d2"]

    def test_limit_larger_than_trail(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        s.visit("u1", "d2")
        trail = s.trail_for("u1", limit=100)
        assert len(trail) == 2


# ---------------------------------------------------------------------------
# recent_doc()
# ---------------------------------------------------------------------------


class TestRecentDoc:
    def test_none_for_empty(self):
        s = DocBreadcrumbStore()
        assert s.recent_doc("u1") is None

    def test_single(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        c = s.recent_doc("u1")
        assert c is not None
        assert c.doc_id == "d1"

    def test_most_recent(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        s.visit("u1", "d2")
        s.visit("u1", "d3")
        c = s.recent_doc("u1")
        assert c.doc_id == "d3"


# ---------------------------------------------------------------------------
# previous_doc()
# ---------------------------------------------------------------------------


class TestPreviousDoc:
    def test_none_for_empty(self):
        s = DocBreadcrumbStore()
        assert s.previous_doc("u1") is None

    def test_none_for_single(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        assert s.previous_doc("u1") is None

    def test_second_most_recent(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        s.visit("u1", "d2")
        c = s.previous_doc("u1")
        assert c is not None
        assert c.doc_id == "d1"

    def test_after_many_visits(self):
        s = DocBreadcrumbStore()
        for i in range(5):
            s.visit("u1", f"d{i}")
        c = s.previous_doc("u1")
        assert c.doc_id == "d3"


# ---------------------------------------------------------------------------
# clear_user()
# ---------------------------------------------------------------------------


class TestClearUser:
    def test_unknown_user_returns_zero(self):
        s = DocBreadcrumbStore()
        assert s.clear_user("nobody") == 0

    def test_clear_returns_count(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        s.visit("u1", "d2")
        assert s.clear_user("u1") == 2

    def test_clear_isolates_user(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        s.visit("u2", "d2")
        s.clear_user("u1")
        assert s.trail_for("u1") == []
        assert len(s.trail_for("u2")) == 1

    def test_entries_removed(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        s.visit("u1", "d2")
        s.clear_user("u1")
        assert s.stats().total_entries == 0


# ---------------------------------------------------------------------------
# clear_all()
# ---------------------------------------------------------------------------


class TestClearAll:
    def test_empty_returns_zero(self):
        s = DocBreadcrumbStore()
        assert s.clear_all() == 0

    def test_clear_all_returns_count(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        s.visit("u2", "d2")
        s.visit("u3", "d3")
        assert s.clear_all() == 3

    def test_clear_all_resets(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        s.visit("u2", "d2")
        s.clear_all()
        assert s.users_with_history() == []
        assert s.stats().total_entries == 0


# ---------------------------------------------------------------------------
# users_with_history()
# ---------------------------------------------------------------------------


class TestUsersWithHistory:
    def test_empty(self):
        s = DocBreadcrumbStore()
        assert s.users_with_history() == []

    def test_sorted(self):
        s = DocBreadcrumbStore()
        s.visit("charlie", "d1")
        s.visit("alice", "d2")
        s.visit("bob", "d3")
        assert s.users_with_history() == ["alice", "bob", "charlie"]

    def test_deduplicated(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        s.visit("u1", "d2")
        assert s.users_with_history() == ["u1"]

    def test_excludes_cleared(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        s.visit("u2", "d2")
        s.clear_user("u1")
        assert s.users_with_history() == ["u2"]


# ---------------------------------------------------------------------------
# unique_docs_visited()
# ---------------------------------------------------------------------------


class TestUniqueDocsVisited:
    def test_empty_user(self):
        s = DocBreadcrumbStore()
        assert s.unique_docs_visited("u1") == []

    def test_sorted(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "zeta")
        s.visit("u1", "alpha")
        s.visit("u1", "beta")
        assert s.unique_docs_visited("u1") == ["alpha", "beta", "zeta"]

    def test_unique(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        s.visit("u1", "d1")
        s.visit("u1", "d2")
        assert s.unique_docs_visited("u1") == ["d1", "d2"]


# ---------------------------------------------------------------------------
# frequency_for_doc()
# ---------------------------------------------------------------------------


class TestFrequencyForDoc:
    def test_no_visits(self):
        s = DocBreadcrumbStore()
        assert s.frequency_for_doc("u1", "d1") == 0

    def test_single_visit(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        assert s.frequency_for_doc("u1", "d1") == 1

    def test_multiple_visits(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        s.visit("u1", "d1")
        s.visit("u1", "d2")
        s.visit("u1", "d1")
        assert s.frequency_for_doc("u1", "d1") == 3
        assert s.frequency_for_doc("u1", "d2") == 1

    def test_isolated_per_user(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        assert s.frequency_for_doc("u2", "d1") == 0


# ---------------------------------------------------------------------------
# most_visited_docs()
# ---------------------------------------------------------------------------


class TestMostVisitedDocs:
    def test_empty(self):
        s = DocBreadcrumbStore()
        assert s.most_visited_docs("u1") == []

    def test_sorted_by_count_desc(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "a")
        s.visit("u1", "b")
        s.visit("u1", "b")
        s.visit("u1", "c")
        s.visit("u1", "c")
        s.visit("u1", "c")
        result = s.most_visited_docs("u1")
        assert result == [("c", 3), ("b", 2), ("a", 1)]

    def test_tiebreak_by_doc_asc(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "zeta")
        s.visit("u1", "alpha")
        result = s.most_visited_docs("u1")
        assert result == [("alpha", 1), ("zeta", 1)]

    def test_limit_applied(self):
        s = DocBreadcrumbStore()
        for d in "abcdef":
            s.visit("u1", d)
        result = s.most_visited_docs("u1", limit=3)
        assert len(result) == 3

    def test_default_limit_five(self):
        s = DocBreadcrumbStore()
        for d in "abcdefgh":
            s.visit("u1", d)
        result = s.most_visited_docs("u1")
        assert len(result) == 5


# ---------------------------------------------------------------------------
# Trim
# ---------------------------------------------------------------------------


class TestTrim:
    def test_max_one(self):
        s = DocBreadcrumbStore(max_per_user=1)
        s.visit("u1", "d1")
        s.visit("u1", "d2")
        trail = s.trail_for("u1")
        assert len(trail) == 1
        assert trail[0].doc_id == "d2"

    def test_keeps_within_max(self):
        s = DocBreadcrumbStore(max_per_user=3)
        for i in range(10):
            s.visit("u1", f"d{i}")
        assert len(s.trail_for("u1")) == 3

    def test_per_user_independent(self):
        s = DocBreadcrumbStore(max_per_user=2)
        s.visit("u1", "d1")
        s.visit("u1", "d2")
        s.visit("u1", "d3")
        s.visit("u2", "x1")
        assert len(s.trail_for("u1")) == 2
        assert len(s.trail_for("u2")) == 1

    def test_trim_clears_old_entries_from_total(self):
        s = DocBreadcrumbStore(max_per_user=2)
        for i in range(5):
            s.visit("u1", f"d{i}")
        # only the last two should remain
        assert s.stats().total_entries == 2


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self):
        s = DocBreadcrumbStore()
        st = s.stats()
        assert st.total_entries == 0
        assert st.unique_users == 0
        assert st.unique_docs == 0

    def test_simple(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        s.visit("u1", "d2")
        s.visit("u2", "d1")
        st = s.stats()
        assert st.total_entries == 3
        assert st.unique_users == 2
        assert st.unique_docs == 2

    def test_after_clear(self):
        s = DocBreadcrumbStore()
        s.visit("u1", "d1")
        s.clear_all()
        st = s.stats()
        assert st.total_entries == 0
        assert st.unique_users == 0
        assert st.unique_docs == 0

    def test_after_trim(self):
        s = DocBreadcrumbStore(max_per_user=2)
        s.visit("u1", "d1")
        s.visit("u1", "d2")
        s.visit("u1", "d3")
        st = s.stats()
        assert st.total_entries == 2
        assert st.unique_users == 1
        assert st.unique_docs == 2


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_visits_same_user(self):
        s = DocBreadcrumbStore(max_per_user=10_000)
        n_threads = 8
        per_thread = 50

        def worker(tid):
            for i in range(per_thread):
                s.visit("u1", f"d{tid}-{i}")

        threads = [
            threading.Thread(target=worker, args=(t,))
            for t in range(n_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert s.stats().total_entries == n_threads * per_thread

    def test_concurrent_visits_distinct_users(self):
        s = DocBreadcrumbStore(max_per_user=1000)
        n_threads = 6
        per_thread = 40

        def worker(tid):
            for i in range(per_thread):
                s.visit(f"u{tid}", f"d{i}")

        threads = [
            threading.Thread(target=worker, args=(t,))
            for t in range(n_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert s.stats().total_entries == n_threads * per_thread
        assert len(s.users_with_history()) == n_threads

    def test_concurrent_unique_ids(self):
        s = DocBreadcrumbStore(max_per_user=10_000)
        n_threads = 8
        per_thread = 25
        ids: list[int] = []
        ids_lock = threading.Lock()

        def worker():
            local = []
            for _ in range(per_thread):
                local.append(s.visit("u1", "d").entry_id)
            with ids_lock:
                ids.extend(local)

        threads = [threading.Thread(target=worker) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(ids) == len(set(ids))
