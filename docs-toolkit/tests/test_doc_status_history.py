"""Tests for E399 DocStatusHistory."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_status_history import (
    DocStatusHistory,
    StatusChange,
    StatusStats,
)


# ---------------------------------------------------------------------------
# Dataclass shapes
# ---------------------------------------------------------------------------


class TestStatusChangeDataclass:
    def test_construct_minimal(self):
        c = StatusChange(
            change_id=1,
            doc_id="doc-1",
            old_status=None,
            new_status="draft",
        )
        assert c.change_id == 1
        assert c.doc_id == "doc-1"
        assert c.old_status is None
        assert c.new_status == "draft"

    def test_default_fields(self):
        c = StatusChange(change_id=1, doc_id="d", old_status=None, new_status="x")
        assert c.changed_at == 0.0
        assert c.changed_by == ""
        assert c.note == ""

    def test_explicit_fields(self):
        c = StatusChange(
            change_id=7,
            doc_id="d",
            old_status="a",
            new_status="b",
            changed_at=123.5,
            changed_by="alice",
            note="hello",
        )
        assert c.changed_at == 123.5
        assert c.changed_by == "alice"
        assert c.note == "hello"

    def test_equality(self):
        a = StatusChange(change_id=1, doc_id="d", old_status=None, new_status="x")
        b = StatusChange(change_id=1, doc_id="d", old_status=None, new_status="x")
        assert a == b


class TestStatusStatsDataclass:
    def test_construct(self):
        s = StatusStats(total_changes=5, unique_docs=2)
        assert s.total_changes == 5
        assert s.unique_docs == 2
        assert s.current_status_counts == {}

    def test_default_factory_independent(self):
        a = StatusStats(total_changes=0, unique_docs=0)
        b = StatusStats(total_changes=0, unique_docs=0)
        a.current_status_counts["x"] = 1
        assert b.current_status_counts == {}

    def test_explicit_counts(self):
        s = StatusStats(
            total_changes=3,
            unique_docs=2,
            current_status_counts={"a": 1, "b": 1},
        )
        assert s.current_status_counts == {"a": 1, "b": 1}


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_construct_default(self):
        h = DocStatusHistory()
        assert h.all_doc_ids() == []

    def test_initial_stats(self):
        h = DocStatusHistory()
        s = h.stats()
        assert s.total_changes == 0
        assert s.unique_docs == 0
        assert s.current_status_counts == {}

    def test_initial_distribution(self):
        h = DocStatusHistory()
        assert h.status_distribution() == {}

    def test_independent_instances(self):
        a = DocStatusHistory()
        b = DocStatusHistory()
        a.record_change("d", "draft")
        assert b.all_doc_ids() == []


# ---------------------------------------------------------------------------
# record_change
# ---------------------------------------------------------------------------


class TestRecordChange:
    def test_returns_status_change(self):
        h = DocStatusHistory()
        c = h.record_change("d1", "draft")
        assert isinstance(c, StatusChange)

    def test_first_change_old_status_none(self):
        h = DocStatusHistory()
        c = h.record_change("d1", "draft")
        assert c.old_status is None
        assert c.new_status == "draft"

    def test_old_status_auto_detected(self):
        h = DocStatusHistory()
        h.record_change("d1", "draft", now=1.0)
        c = h.record_change("d1", "review", now=2.0)
        assert c.old_status == "draft"
        assert c.new_status == "review"

    def test_id_increments_from_one(self):
        h = DocStatusHistory()
        c1 = h.record_change("d1", "draft")
        c2 = h.record_change("d2", "draft")
        c3 = h.record_change("d1", "review")
        assert (c1.change_id, c2.change_id, c3.change_id) == (1, 2, 3)

    def test_uses_now_when_passed(self):
        h = DocStatusHistory()
        c = h.record_change("d", "x", now=42.0)
        assert c.changed_at == 42.0

    def test_default_changed_by_and_note(self):
        h = DocStatusHistory()
        c = h.record_change("d", "x")
        assert c.changed_by == ""
        assert c.note == ""

    def test_changed_by_and_note_propagated(self):
        h = DocStatusHistory()
        c = h.record_change("d", "x", changed_by="alice", note="kickoff")
        assert c.changed_by == "alice"
        assert c.note == "kickoff"

    def test_current_status_updated(self):
        h = DocStatusHistory()
        h.record_change("d", "draft")
        h.record_change("d", "published")
        assert h.current_status("d") == "published"


# ---------------------------------------------------------------------------
# current_status
# ---------------------------------------------------------------------------


class TestCurrentStatus:
    def test_unknown_doc_returns_none(self):
        h = DocStatusHistory()
        assert h.current_status("missing") is None

    def test_returns_latest(self):
        h = DocStatusHistory()
        h.record_change("d", "a", now=1.0)
        h.record_change("d", "b", now=2.0)
        h.record_change("d", "c", now=3.0)
        assert h.current_status("d") == "c"

    def test_per_doc_independent(self):
        h = DocStatusHistory()
        h.record_change("d1", "draft")
        h.record_change("d2", "review")
        assert h.current_status("d1") == "draft"
        assert h.current_status("d2") == "review"


# ---------------------------------------------------------------------------
# history_for
# ---------------------------------------------------------------------------


class TestHistoryFor:
    def test_empty_doc_returns_empty(self):
        h = DocStatusHistory()
        assert h.history_for("nope") == []

    def test_most_recent_first(self):
        h = DocStatusHistory()
        h.record_change("d", "a", now=1.0)
        h.record_change("d", "b", now=2.0)
        h.record_change("d", "c", now=3.0)
        hist = h.history_for("d")
        assert [x.new_status for x in hist] == ["c", "b", "a"]

    def test_limit_truncates(self):
        h = DocStatusHistory()
        for i, s in enumerate(["a", "b", "c", "d"]):
            h.record_change("doc", s, now=float(i))
        hist = h.history_for("doc", limit=2)
        assert [x.new_status for x in hist] == ["d", "c"]

    def test_limit_none_returns_all(self):
        h = DocStatusHistory()
        for i, s in enumerate(["a", "b", "c"]):
            h.record_change("doc", s, now=float(i))
        assert len(h.history_for("doc", limit=None)) == 3

    def test_does_not_include_other_docs(self):
        h = DocStatusHistory()
        h.record_change("d1", "x")
        h.record_change("d2", "y")
        assert [c.doc_id for c in h.history_for("d1")] == ["d1"]


# ---------------------------------------------------------------------------
# latest_change_for
# ---------------------------------------------------------------------------


class TestLatestChangeFor:
    def test_unknown_returns_none(self):
        h = DocStatusHistory()
        assert h.latest_change_for("nope") is None

    def test_returns_latest_change(self):
        h = DocStatusHistory()
        h.record_change("d", "a", now=1.0)
        c = h.record_change("d", "b", now=2.0)
        assert h.latest_change_for("d") == c

    def test_single_change(self):
        h = DocStatusHistory()
        c = h.record_change("d", "a")
        assert h.latest_change_for("d") == c


# ---------------------------------------------------------------------------
# time_in_current_status
# ---------------------------------------------------------------------------


class TestTimeInCurrentStatus:
    def test_unknown_returns_none(self):
        h = DocStatusHistory()
        assert h.time_in_current_status("nope") is None

    def test_computes_seconds(self):
        h = DocStatusHistory()
        h.record_change("d", "x", now=100.0)
        assert h.time_in_current_status("d", now=150.0) == 50.0

    def test_uses_latest_change(self):
        h = DocStatusHistory()
        h.record_change("d", "a", now=1.0)
        h.record_change("d", "b", now=10.0)
        assert h.time_in_current_status("d", now=20.0) == 10.0

    def test_zero_when_now_equals_changed_at(self):
        h = DocStatusHistory()
        h.record_change("d", "x", now=42.0)
        assert h.time_in_current_status("d", now=42.0) == 0.0


# ---------------------------------------------------------------------------
# transitions
# ---------------------------------------------------------------------------


class TestTransitions:
    def test_empty(self):
        h = DocStatusHistory()
        assert h.transitions("a", "b") == []

    def test_filters_old_and_new(self):
        h = DocStatusHistory()
        h.record_change("d1", "draft", now=1.0)
        h.record_change("d1", "review", now=2.0)
        h.record_change("d2", "draft", now=3.0)
        h.record_change("d2", "review", now=4.0)
        h.record_change("d1", "published", now=5.0)
        ts = h.transitions("draft", "review")
        assert len(ts) == 2
        assert all(c.old_status == "draft" and c.new_status == "review" for c in ts)

    def test_sorted_by_changed_at(self):
        h = DocStatusHistory()
        h.record_change("d2", "draft", now=10.0)
        h.record_change("d2", "review", now=20.0)
        h.record_change("d1", "draft", now=1.0)
        h.record_change("d1", "review", now=2.0)
        ts = h.transitions("draft", "review")
        assert [c.changed_at for c in ts] == [2.0, 20.0]

    def test_no_match_returns_empty(self):
        h = DocStatusHistory()
        h.record_change("d", "draft")
        h.record_change("d", "review")
        # No "review" -> "draft" transition recorded
        assert h.transitions("review", "draft") == []


# ---------------------------------------------------------------------------
# docs_in_status
# ---------------------------------------------------------------------------


class TestDocsInStatus:
    def test_empty(self):
        h = DocStatusHistory()
        assert h.docs_in_status("draft") == []

    def test_returns_sorted(self):
        h = DocStatusHistory()
        h.record_change("zeta", "draft")
        h.record_change("alpha", "draft")
        h.record_change("mu", "draft")
        assert h.docs_in_status("draft") == ["alpha", "mu", "zeta"]

    def test_only_current_status(self):
        h = DocStatusHistory()
        h.record_change("d1", "draft")
        h.record_change("d1", "published")
        h.record_change("d2", "draft")
        assert h.docs_in_status("draft") == ["d2"]
        assert h.docs_in_status("published") == ["d1"]

    def test_unknown_status(self):
        h = DocStatusHistory()
        h.record_change("d", "draft")
        assert h.docs_in_status("archived") == []


# ---------------------------------------------------------------------------
# status_distribution
# ---------------------------------------------------------------------------


class TestStatusDistribution:
    def test_empty(self):
        h = DocStatusHistory()
        assert h.status_distribution() == {}

    def test_counts(self):
        h = DocStatusHistory()
        h.record_change("d1", "draft")
        h.record_change("d2", "draft")
        h.record_change("d3", "published")
        assert h.status_distribution() == {"draft": 2, "published": 1}

    def test_uses_current_status_only(self):
        h = DocStatusHistory()
        h.record_change("d", "draft")
        h.record_change("d", "review")
        h.record_change("d", "published")
        assert h.status_distribution() == {"published": 1}

    def test_returns_copy(self):
        h = DocStatusHistory()
        h.record_change("d", "draft")
        d = h.status_distribution()
        d["draft"] = 999
        assert h.status_distribution() == {"draft": 1}


# ---------------------------------------------------------------------------
# changes_in_range
# ---------------------------------------------------------------------------


class TestChangesInRange:
    def test_empty(self):
        h = DocStatusHistory()
        assert h.changes_in_range(0.0, 100.0) == []

    def test_inclusive_bounds(self):
        h = DocStatusHistory()
        h.record_change("d", "a", now=10.0)
        h.record_change("d", "b", now=20.0)
        h.record_change("d", "c", now=30.0)
        res = h.changes_in_range(10.0, 30.0)
        assert [c.new_status for c in res] == ["a", "b", "c"]

    def test_excludes_outside(self):
        h = DocStatusHistory()
        h.record_change("d", "a", now=5.0)
        h.record_change("d", "b", now=15.0)
        h.record_change("d", "c", now=25.0)
        res = h.changes_in_range(10.0, 20.0)
        assert [c.new_status for c in res] == ["b"]

    def test_doc_filter(self):
        h = DocStatusHistory()
        h.record_change("d1", "a", now=1.0)
        h.record_change("d2", "b", now=2.0)
        h.record_change("d1", "c", now=3.0)
        res = h.changes_in_range(0.0, 10.0, doc_id="d1")
        assert [c.new_status for c in res] == ["a", "c"]

    def test_sorted_ascending(self):
        h = DocStatusHistory()
        h.record_change("d", "a", now=30.0)
        h.record_change("d", "b", now=10.0)
        h.record_change("d", "c", now=20.0)
        # Note: record_change appends in call order; we test order by changed_at
        res = h.changes_in_range(0.0, 100.0)
        assert [c.changed_at for c in res] == [10.0, 20.0, 30.0]


# ---------------------------------------------------------------------------
# clear_doc
# ---------------------------------------------------------------------------


class TestClearDoc:
    def test_unknown_returns_zero(self):
        h = DocStatusHistory()
        assert h.clear_doc("nope") == 0

    def test_returns_count(self):
        h = DocStatusHistory()
        h.record_change("d", "a")
        h.record_change("d", "b")
        h.record_change("d", "c")
        assert h.clear_doc("d") == 3

    def test_history_removed(self):
        h = DocStatusHistory()
        h.record_change("d", "a")
        h.record_change("d", "b")
        h.clear_doc("d")
        assert h.history_for("d") == []

    def test_current_status_removed(self):
        h = DocStatusHistory()
        h.record_change("d", "a")
        h.clear_doc("d")
        assert h.current_status("d") is None

    def test_does_not_affect_other_docs(self):
        h = DocStatusHistory()
        h.record_change("d1", "a")
        h.record_change("d2", "b")
        h.clear_doc("d1")
        assert h.current_status("d2") == "b"
        assert h.history_for("d2") != []

    def test_changes_in_range_excludes_cleared(self):
        h = DocStatusHistory()
        h.record_change("d1", "a", now=1.0)
        h.record_change("d2", "b", now=2.0)
        h.clear_doc("d1")
        res = h.changes_in_range(0.0, 10.0)
        assert [c.doc_id for c in res] == ["d2"]


# ---------------------------------------------------------------------------
# all_doc_ids
# ---------------------------------------------------------------------------


class TestAllDocIds:
    def test_empty(self):
        h = DocStatusHistory()
        assert h.all_doc_ids() == []

    def test_sorted(self):
        h = DocStatusHistory()
        h.record_change("zeta", "x")
        h.record_change("alpha", "x")
        h.record_change("mu", "x")
        assert h.all_doc_ids() == ["alpha", "mu", "zeta"]

    def test_deduplicated(self):
        h = DocStatusHistory()
        h.record_change("d", "a")
        h.record_change("d", "b")
        h.record_change("d", "c")
        assert h.all_doc_ids() == ["d"]


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self):
        s = DocStatusHistory().stats()
        assert s.total_changes == 0
        assert s.unique_docs == 0
        assert s.current_status_counts == {}

    def test_total_changes(self):
        h = DocStatusHistory()
        h.record_change("d1", "a")
        h.record_change("d2", "b")
        h.record_change("d1", "c")
        assert h.stats().total_changes == 3

    def test_unique_docs(self):
        h = DocStatusHistory()
        h.record_change("d1", "a")
        h.record_change("d2", "b")
        h.record_change("d1", "c")
        assert h.stats().unique_docs == 2

    def test_current_status_counts(self):
        h = DocStatusHistory()
        h.record_change("d1", "draft")
        h.record_change("d2", "draft")
        h.record_change("d3", "published")
        s = h.stats()
        assert s.current_status_counts == {"draft": 2, "published": 1}

    def test_stats_after_clear(self):
        h = DocStatusHistory()
        h.record_change("d1", "a")
        h.record_change("d2", "b")
        h.clear_doc("d1")
        s = h.stats()
        assert s.unique_docs == 1
        assert s.total_changes == 1
        assert s.current_status_counts == {"b": 1}


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_record_change(self):
        h = DocStatusHistory()
        n_threads = 8
        per_thread = 50

        def worker(tid: int):
            for i in range(per_thread):
                h.record_change(f"doc-{tid}", f"s-{i}")

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = h.stats()
        assert s.total_changes == n_threads * per_thread
        assert s.unique_docs == n_threads
        # All change_ids should be unique and form 1..N
        all_ids = [c.change_id for c in h.changes_in_range(0.0, 1e18)]
        assert sorted(all_ids) == list(range(1, n_threads * per_thread + 1))

    def test_concurrent_shared_doc(self):
        h = DocStatusHistory()
        n_threads = 10
        per_thread = 100

        def worker(tid: int):
            for i in range(per_thread):
                h.record_change("shared", f"t{tid}-s{i}")

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert h.stats().total_changes == n_threads * per_thread
        assert h.all_doc_ids() == ["shared"]
        # History length matches
        assert len(h.history_for("shared")) == n_threads * per_thread


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-q"])
