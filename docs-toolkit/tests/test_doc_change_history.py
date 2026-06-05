"""Tests for docstoolkit.doc_change_history (E332)."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_change_history import (
    ChangeEntry,
    ChangeHistoryStats,
    DocChangeHistory,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _hist() -> DocChangeHistory:
    return DocChangeHistory()


def _record(
    h: DocChangeHistory,
    doc_id: str = "d1",
    field: str = "title",
    old_value: str = "old",
    new_value: str = "new",
    changed_by: str = "alice",
    comment: str = "",
    now: float | None = None,
) -> ChangeEntry:
    return h.record(
        doc_id=doc_id,
        field=field,
        old_value=old_value,
        new_value=new_value,
        changed_by=changed_by,
        comment=comment,
        now=now,
    )


# ---------------------------------------------------------------------------
# ChangeEntry dataclass
# ---------------------------------------------------------------------------


class TestChangeEntryDataclass:
    def test_construct_with_required_only(self):
        e = ChangeEntry(
            change_id=1,
            doc_id="d1",
            field="title",
            old_value="a",
            new_value="b",
        )
        assert e.change_id == 1
        assert e.doc_id == "d1"
        assert e.field == "title"
        assert e.old_value == "a"
        assert e.new_value == "b"

    def test_default_changed_at_zero(self):
        e = ChangeEntry(change_id=1, doc_id="d", field="f", old_value="", new_value="")
        assert e.changed_at == 0.0

    def test_default_changed_by_empty(self):
        e = ChangeEntry(change_id=1, doc_id="d", field="f", old_value="", new_value="")
        assert e.changed_by == ""

    def test_default_comment_empty(self):
        e = ChangeEntry(change_id=1, doc_id="d", field="f", old_value="", new_value="")
        assert e.comment == ""

    def test_all_fields_assignable(self):
        e = ChangeEntry(
            change_id=7,
            doc_id="d7",
            field="content",
            old_value="x",
            new_value="y",
            changed_at=123.5,
            changed_by="bob",
            comment="typo fix",
        )
        assert e.changed_at == 123.5
        assert e.changed_by == "bob"
        assert e.comment == "typo fix"

    def test_equality(self):
        e1 = ChangeEntry(change_id=1, doc_id="d", field="f", old_value="o", new_value="n")
        e2 = ChangeEntry(change_id=1, doc_id="d", field="f", old_value="o", new_value="n")
        assert e1 == e2


# ---------------------------------------------------------------------------
# ChangeHistoryStats dataclass
# ---------------------------------------------------------------------------


class TestChangeHistoryStatsDataclass:
    def test_fields_assignable(self):
        s = ChangeHistoryStats(
            total_changes=10, unique_docs=3, unique_users=2, unique_fields=4
        )
        assert s.total_changes == 10
        assert s.unique_docs == 3
        assert s.unique_users == 2
        assert s.unique_fields == 4

    def test_equality(self):
        a = ChangeHistoryStats(1, 1, 1, 1)
        b = ChangeHistoryStats(1, 1, 1, 1)
        assert a == b

    def test_zero_stats(self):
        s = ChangeHistoryStats(0, 0, 0, 0)
        assert s.total_changes == 0


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_history(self):
        h = _hist()
        assert h.stats().total_changes == 0

    def test_no_docs_initially(self):
        assert _hist().all_doc_ids() == []

    def test_get_missing_returns_none(self):
        assert _hist().get_change(1) is None

    def test_changes_for_unknown_doc_empty(self):
        assert _hist().changes_for_doc("nope") == []


# ---------------------------------------------------------------------------
# record
# ---------------------------------------------------------------------------


class TestRecord:
    def test_record_returns_entry(self):
        h = _hist()
        e = _record(h)
        assert isinstance(e, ChangeEntry)

    def test_first_id_is_one(self):
        h = _hist()
        e = _record(h)
        assert e.change_id == 1

    def test_ids_increment(self):
        h = _hist()
        ids = [_record(h).change_id for _ in range(5)]
        assert ids == [1, 2, 3, 4, 5]

    def test_timestamp_set_when_now_none(self):
        h = _hist()
        e = _record(h, now=None)
        assert e.changed_at > 0

    def test_timestamp_uses_now_when_given(self):
        h = _hist()
        e = _record(h, now=42.5)
        assert e.changed_at == 42.5

    def test_all_fields_stored(self):
        h = _hist()
        e = _record(
            h,
            doc_id="dX",
            field="content",
            old_value="aa",
            new_value="bb",
            changed_by="carol",
            comment="ok",
            now=99.0,
        )
        assert e.doc_id == "dX"
        assert e.field == "content"
        assert e.old_value == "aa"
        assert e.new_value == "bb"
        assert e.changed_by == "carol"
        assert e.comment == "ok"
        assert e.changed_at == 99.0

    def test_default_changed_by_empty(self):
        h = _hist()
        e = h.record("d", "title", "a", "b")
        assert e.changed_by == ""

    def test_default_comment_empty(self):
        h = _hist()
        e = h.record("d", "title", "a", "b")
        assert e.comment == ""

    def test_recorded_indexed_by_doc(self):
        h = _hist()
        _record(h, doc_id="dA")
        assert h.changes_for_doc("dA")

    def test_empty_user_not_indexed(self):
        h = _hist()
        h.record("d", "title", "a", "b", changed_by="")
        # No user index entry is created for empty user.
        assert h.changes_by_user("") == []


# ---------------------------------------------------------------------------
# get_change
# ---------------------------------------------------------------------------


class TestGetChange:
    def test_get_found(self):
        h = _hist()
        e = _record(h)
        assert h.get_change(e.change_id) == e

    def test_get_missing(self):
        h = _hist()
        _record(h)
        assert h.get_change(999) is None

    def test_get_zero_id(self):
        h = _hist()
        _record(h)
        assert h.get_change(0) is None

    def test_get_negative(self):
        assert _hist().get_change(-1) is None


# ---------------------------------------------------------------------------
# changes_for_doc
# ---------------------------------------------------------------------------


class TestChangesForDoc:
    def test_returns_only_doc_entries(self):
        h = _hist()
        _record(h, doc_id="a")
        _record(h, doc_id="b")
        _record(h, doc_id="a")
        out = h.changes_for_doc("a")
        assert len(out) == 2
        assert all(e.doc_id == "a" for e in out)

    def test_sorted_by_changed_at(self):
        h = _hist()
        _record(h, doc_id="x", now=30.0)
        _record(h, doc_id="x", now=10.0)
        _record(h, doc_id="x", now=20.0)
        out = h.changes_for_doc("x")
        ts = [e.changed_at for e in out]
        assert ts == [10.0, 20.0, 30.0]

    def test_field_filter(self):
        h = _hist()
        _record(h, doc_id="x", field="title")
        _record(h, doc_id="x", field="content")
        _record(h, doc_id="x", field="title")
        out = h.changes_for_doc("x", field="title")
        assert len(out) == 2
        assert all(e.field == "title" for e in out)

    def test_field_filter_empty(self):
        h = _hist()
        _record(h, doc_id="x", field="title")
        assert h.changes_for_doc("x", field="content") == []

    def test_limit(self):
        h = _hist()
        for i in range(5):
            _record(h, doc_id="x", now=float(i))
        assert len(h.changes_for_doc("x", limit=3)) == 3

    def test_limit_zero(self):
        h = _hist()
        _record(h, doc_id="x")
        assert h.changes_for_doc("x", limit=0) == []

    def test_limit_larger_than_available(self):
        h = _hist()
        _record(h, doc_id="x")
        assert len(h.changes_for_doc("x", limit=100)) == 1

    def test_unknown_doc(self):
        assert _hist().changes_for_doc("missing") == []


# ---------------------------------------------------------------------------
# changes_by_user
# ---------------------------------------------------------------------------


class TestChangesByUser:
    def test_returns_only_user_entries(self):
        h = _hist()
        _record(h, changed_by="alice")
        _record(h, changed_by="bob")
        _record(h, changed_by="alice")
        out = h.changes_by_user("alice")
        assert len(out) == 2
        assert all(e.changed_by == "alice" for e in out)

    def test_sorted_by_changed_at(self):
        h = _hist()
        _record(h, changed_by="alice", now=5.0)
        _record(h, changed_by="alice", now=1.0)
        _record(h, changed_by="alice", now=3.0)
        out = h.changes_by_user("alice")
        assert [e.changed_at for e in out] == [1.0, 3.0, 5.0]

    def test_cross_doc(self):
        h = _hist()
        _record(h, doc_id="a", changed_by="alice")
        _record(h, doc_id="b", changed_by="alice")
        out = h.changes_by_user("alice")
        assert {e.doc_id for e in out} == {"a", "b"}

    def test_limit(self):
        h = _hist()
        for i in range(4):
            _record(h, changed_by="alice", now=float(i))
        assert len(h.changes_by_user("alice", limit=2)) == 2

    def test_unknown_user(self):
        assert _hist().changes_by_user("nobody") == []


# ---------------------------------------------------------------------------
# changes_in_range
# ---------------------------------------------------------------------------


class TestChangesInRange:
    def test_inclusive_bounds(self):
        h = _hist()
        _record(h, now=1.0)
        _record(h, now=2.0)
        _record(h, now=3.0)
        out = h.changes_in_range(1.0, 3.0)
        assert len(out) == 3

    def test_excludes_outside(self):
        h = _hist()
        _record(h, now=0.5)
        _record(h, now=2.0)
        _record(h, now=5.0)
        out = h.changes_in_range(1.0, 3.0)
        assert [e.changed_at for e in out] == [2.0]

    def test_doc_filter(self):
        h = _hist()
        _record(h, doc_id="a", now=1.0)
        _record(h, doc_id="b", now=2.0)
        _record(h, doc_id="a", now=3.0)
        out = h.changes_in_range(0.0, 10.0, doc_id="a")
        assert len(out) == 2
        assert all(e.doc_id == "a" for e in out)

    def test_sorted(self):
        h = _hist()
        _record(h, now=5.0)
        _record(h, now=1.0)
        _record(h, now=3.0)
        out = h.changes_in_range(0.0, 10.0)
        assert [e.changed_at for e in out] == [1.0, 3.0, 5.0]

    def test_empty_range(self):
        h = _hist()
        _record(h, now=10.0)
        assert h.changes_in_range(0.0, 5.0) == []

    def test_unknown_doc_filter(self):
        h = _hist()
        _record(h, doc_id="a", now=1.0)
        assert h.changes_in_range(0.0, 10.0, doc_id="missing") == []


# ---------------------------------------------------------------------------
# latest_for
# ---------------------------------------------------------------------------


class TestLatestFor:
    def test_returns_most_recent(self):
        h = _hist()
        _record(h, doc_id="x", field="title", new_value="v1", now=1.0)
        _record(h, doc_id="x", field="title", new_value="v2", now=3.0)
        _record(h, doc_id="x", field="title", new_value="v3", now=2.0)
        out = h.latest_for("x", "title")
        assert out is not None
        assert out.new_value == "v2"

    def test_none_when_no_changes(self):
        h = _hist()
        assert h.latest_for("x", "title") is None

    def test_none_for_other_field(self):
        h = _hist()
        _record(h, doc_id="x", field="title")
        assert h.latest_for("x", "content") is None

    def test_separate_per_field(self):
        h = _hist()
        _record(h, doc_id="x", field="title", new_value="t1", now=1.0)
        _record(h, doc_id="x", field="content", new_value="c1", now=2.0)
        latest_title = h.latest_for("x", "title")
        latest_content = h.latest_for("x", "content")
        assert latest_title.new_value == "t1"
        assert latest_content.new_value == "c1"


# ---------------------------------------------------------------------------
# revert_value
# ---------------------------------------------------------------------------


class TestRevertValue:
    def test_returns_old_value(self):
        h = _hist()
        _record(h, doc_id="x", field="title", old_value="orig", new_value="new")
        assert h.revert_value("x", "title") == "orig"

    def test_none_when_no_changes(self):
        assert _hist().revert_value("x", "title") is None

    def test_uses_most_recent_old_value(self):
        h = _hist()
        _record(h, doc_id="x", field="title", old_value="v0", new_value="v1", now=1.0)
        _record(h, doc_id="x", field="title", old_value="v1", new_value="v2", now=2.0)
        assert h.revert_value("x", "title") == "v1"

    def test_returns_empty_string_if_old_was_empty(self):
        h = _hist()
        _record(h, doc_id="x", field="title", old_value="", new_value="new")
        assert h.revert_value("x", "title") == ""

    def test_unknown_field(self):
        h = _hist()
        _record(h, doc_id="x", field="title")
        assert h.revert_value("x", "content") is None


# ---------------------------------------------------------------------------
# count_changes_for
# ---------------------------------------------------------------------------


class TestCountChangesFor:
    def test_total_for_doc(self):
        h = _hist()
        _record(h, doc_id="x")
        _record(h, doc_id="x")
        _record(h, doc_id="y")
        assert h.count_changes_for("x") == 2

    def test_field_scoped(self):
        h = _hist()
        _record(h, doc_id="x", field="title")
        _record(h, doc_id="x", field="content")
        _record(h, doc_id="x", field="title")
        assert h.count_changes_for("x", field="title") == 2

    def test_field_no_match(self):
        h = _hist()
        _record(h, doc_id="x", field="title")
        assert h.count_changes_for("x", field="content") == 0

    def test_unknown_doc(self):
        assert _hist().count_changes_for("missing") == 0

    def test_zero_when_empty(self):
        assert _hist().count_changes_for("x") == 0


# ---------------------------------------------------------------------------
# purge_doc
# ---------------------------------------------------------------------------


class TestPurgeDoc:
    def test_returns_count(self):
        h = _hist()
        _record(h, doc_id="x")
        _record(h, doc_id="x")
        _record(h, doc_id="y")
        assert h.purge_doc("x") == 2

    def test_gone_from_index(self):
        h = _hist()
        _record(h, doc_id="x")
        h.purge_doc("x")
        assert h.changes_for_doc("x") == []

    def test_doc_id_removed_from_all_doc_ids(self):
        h = _hist()
        _record(h, doc_id="x")
        _record(h, doc_id="y")
        h.purge_doc("x")
        assert "x" not in h.all_doc_ids()

    def test_other_docs_intact(self):
        h = _hist()
        _record(h, doc_id="x")
        _record(h, doc_id="y")
        h.purge_doc("x")
        assert len(h.changes_for_doc("y")) == 1

    def test_user_index_cleaned(self):
        h = _hist()
        _record(h, doc_id="x", changed_by="alice")
        h.purge_doc("x")
        assert h.changes_by_user("alice") == []

    def test_user_index_partial_cleanup(self):
        h = _hist()
        _record(h, doc_id="x", changed_by="alice")
        _record(h, doc_id="y", changed_by="alice")
        h.purge_doc("x")
        remaining = h.changes_by_user("alice")
        assert len(remaining) == 1
        assert remaining[0].doc_id == "y"

    def test_purge_unknown_doc(self):
        assert _hist().purge_doc("missing") == 0

    def test_global_list_preserved(self):
        h = _hist()
        _record(h, doc_id="x")
        _record(h, doc_id="x")
        h.purge_doc("x")
        # Global stats still count all changes ever recorded.
        assert h.stats().total_changes == 2


# ---------------------------------------------------------------------------
# all_doc_ids
# ---------------------------------------------------------------------------


class TestAllDocIds:
    def test_sorted(self):
        h = _hist()
        _record(h, doc_id="zzz")
        _record(h, doc_id="aaa")
        _record(h, doc_id="mmm")
        assert h.all_doc_ids() == ["aaa", "mmm", "zzz"]

    def test_unique(self):
        h = _hist()
        _record(h, doc_id="x")
        _record(h, doc_id="x")
        _record(h, doc_id="x")
        assert h.all_doc_ids() == ["x"]

    def test_empty(self):
        assert _hist().all_doc_ids() == []


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_totals(self):
        h = _hist()
        _record(h, doc_id="a", field="title", changed_by="alice")
        _record(h, doc_id="b", field="content", changed_by="bob")
        _record(h, doc_id="a", field="tags", changed_by="alice")
        s = h.stats()
        assert s.total_changes == 3
        assert s.unique_docs == 2
        assert s.unique_users == 2
        assert s.unique_fields == 3

    def test_empty_stats(self):
        s = _hist().stats()
        assert s == ChangeHistoryStats(0, 0, 0, 0)

    def test_unique_fields_dedup(self):
        h = _hist()
        _record(h, field="title")
        _record(h, field="title")
        _record(h, field="content")
        assert h.stats().unique_fields == 2

    def test_unique_users_skips_empty(self):
        h = _hist()
        h.record("d", "title", "a", "b", changed_by="")
        h.record("d", "title", "b", "c", changed_by="")
        # Empty changed_by is never indexed in _by_user.
        assert h.stats().unique_users == 0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_record(self):
        h = _hist()
        N = 20
        per_thread = 25

        def worker(uid: int):
            for i in range(per_thread):
                h.record(
                    doc_id=f"d{uid % 3}",
                    field="content",
                    old_value=str(i),
                    new_value=str(i + 1),
                    changed_by=f"u{uid}",
                )

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = h.stats()
        assert s.total_changes == N * per_thread

    def test_concurrent_record_unique_ids(self):
        h = _hist()
        ids: list[int] = []
        ids_lock = threading.Lock()

        def worker():
            for _ in range(50):
                e = h.record("d", "f", "a", "b", changed_by="u")
                with ids_lock:
                    ids.append(e.change_id)

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(ids) == len(set(ids))
        assert min(ids) == 1
        assert max(ids) == len(ids)


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-q"])
