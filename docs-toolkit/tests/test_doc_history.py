"""Tests for docstoolkit.doc_history."""
import threading

import pytest

from docstoolkit.doc_history import (
    DocHistory,
    DocSnapshot,
    Edit,
    EditType,
    HistoryStats,
)


# --------------------------------------------------------------------- helpers
def _rec(h, doc="d1", t=EditType.INSERT, before="", after="x", now=0.0,
         author=None, desc=None):
    return h.record(doc, t, before, after, author=author, description=desc, now=now)


# --------------------------------------------------------------------- EditType
class TestEditType:
    def test_insert(self):
        assert EditType.INSERT.value == "insert"

    def test_delete(self):
        assert EditType.DELETE.value == "delete"

    def test_replace(self):
        assert EditType.REPLACE.value == "replace"

    def test_format(self):
        assert EditType.FORMAT.value == "format"

    def test_rename(self):
        assert EditType.RENAME.value == "rename"

    def test_distinct(self):
        assert len({t.value for t in EditType}) == 5


# --------------------------------------------------------------------- Edit
class TestEdit:
    def test_basic_fields(self):
        e = Edit(
            edit_id=1, doc_id="a", edit_type=EditType.INSERT,
            before="", after="hi", timestamp=1.0,
        )
        assert e.edit_id == 1
        assert e.doc_id == "a"
        assert e.edit_type == EditType.INSERT
        assert e.before == ""
        assert e.after == "hi"
        assert e.timestamp == 1.0
        assert e.author is None
        assert e.description is None

    def test_optional_fields(self):
        e = Edit(
            edit_id=2, doc_id="b", edit_type=EditType.REPLACE,
            before="a", after="b", timestamp=2.0,
            author="alice", description="fix typo",
        )
        assert e.author == "alice"
        assert e.description == "fix typo"


# --------------------------------------------------------------------- DocSnapshot
class TestDocSnapshot:
    def test_basic_fields(self):
        s = DocSnapshot(snapshot_id=1, doc_id="d", content="text", timestamp=0.5)
        assert s.snapshot_id == 1
        assert s.doc_id == "d"
        assert s.content == "text"
        assert s.timestamp == 0.5
        assert s.label is None

    def test_label(self):
        s = DocSnapshot(
            snapshot_id=2, doc_id="d", content="t", timestamp=0.0, label="v1",
        )
        assert s.label == "v1"


# --------------------------------------------------------------------- HistoryStats
class TestHistoryStats:
    def test_basic(self):
        s = HistoryStats(total_edits=0, total_snapshots=0)
        assert s.total_edits == 0
        assert s.total_snapshots == 0
        assert s.edits_per_doc == {}
        assert s.can_undo_count == 0

    def test_with_data(self):
        s = HistoryStats(
            total_edits=3, total_snapshots=1,
            edits_per_doc={"a": 2, "b": 1}, can_undo_count=2,
        )
        assert s.total_edits == 3
        assert s.edits_per_doc["a"] == 2
        assert s.can_undo_count == 2


# --------------------------------------------------------------------- Record
class TestRecord:
    def test_record_returns_edit(self):
        h = DocHistory()
        e = _rec(h)
        assert isinstance(e, Edit)
        assert e.edit_id == 1
        assert e.doc_id == "d1"
        assert e.edit_type == EditType.INSERT

    def test_record_sequential_ids(self):
        h = DocHistory()
        e1 = _rec(h)
        e2 = _rec(h)
        e3 = _rec(h, doc="d2")
        assert e1.edit_id == 1
        assert e2.edit_id == 2
        assert e3.edit_id == 3

    def test_record_stores_in_applied(self):
        h = DocHistory()
        _rec(h)
        assert h.can_undo("d1") is True
        assert h.can_redo("d1") is False

    def test_record_with_author_and_desc(self):
        h = DocHistory()
        e = _rec(h, author="bob", desc="initial")
        assert e.author == "bob"
        assert e.description == "initial"

    def test_record_separate_docs(self):
        h = DocHistory()
        _rec(h, doc="a")
        _rec(h, doc="b")
        assert h.can_undo("a")
        assert h.can_undo("b")


# --------------------------------------------------------------------- Undo
class TestUndo:
    def test_undo_returns_edit(self):
        h = DocHistory()
        _rec(h, after="x")
        e = h.undo("d1")
        assert e is not None
        assert e.after == "x"

    def test_undo_no_history(self):
        h = DocHistory()
        assert h.undo("missing") is None

    def test_undo_empty_after_pop(self):
        h = DocHistory()
        _rec(h)
        h.undo("d1")
        assert h.undo("d1") is None

    def test_undo_moves_to_redo(self):
        h = DocHistory()
        _rec(h)
        h.undo("d1")
        assert h.can_redo("d1")
        assert not h.can_undo("d1")


# --------------------------------------------------------------------- Redo
class TestRedo:
    def test_redo_after_undo(self):
        h = DocHistory()
        _rec(h, after="x")
        h.undo("d1")
        e = h.redo("d1")
        assert e is not None
        assert e.after == "x"

    def test_redo_no_history(self):
        h = DocHistory()
        assert h.redo("missing") is None

    def test_redo_without_undo(self):
        h = DocHistory()
        _rec(h)
        assert h.redo("d1") is None

    def test_redo_restores_to_applied(self):
        h = DocHistory()
        _rec(h)
        h.undo("d1")
        h.redo("d1")
        assert h.can_undo("d1")
        assert not h.can_redo("d1")


# --------------------------------------------------------------------- Sequence
class TestUndoRedoSequence:
    def test_record_undo_redo_cycle(self):
        h = DocHistory()
        _rec(h, after="a")
        _rec(h, before="a", after="ab")
        _rec(h, before="ab", after="abc")
        assert h.current_content("d1") == "abc"
        h.undo("d1")
        assert h.current_content("d1") == "ab"
        h.undo("d1")
        assert h.current_content("d1") == "a"
        h.redo("d1")
        assert h.current_content("d1") == "ab"

    def test_multiple_undos_redos(self):
        h = DocHistory()
        for i in range(5):
            _rec(h, before=str(i), after=str(i + 1))
        for _ in range(3):
            h.undo("d1")
        for _ in range(2):
            h.redo("d1")
        # 5 - 3 + 2 = 4 applied
        assert len(h.history("d1")) == 4


# --------------------------------------------------------------------- can_undo / can_redo
class TestCanUndoRedo:
    def test_initial_state(self):
        h = DocHistory()
        assert not h.can_undo("any")
        assert not h.can_redo("any")

    def test_after_record(self):
        h = DocHistory()
        _rec(h)
        assert h.can_undo("d1")
        assert not h.can_redo("d1")

    def test_after_undo(self):
        h = DocHistory()
        _rec(h)
        h.undo("d1")
        assert not h.can_undo("d1")
        assert h.can_redo("d1")

    def test_after_redo(self):
        h = DocHistory()
        _rec(h)
        h.undo("d1")
        h.redo("d1")
        assert h.can_undo("d1")
        assert not h.can_redo("d1")


# --------------------------------------------------------------------- history()
class TestHistory:
    def test_history_empty(self):
        h = DocHistory()
        assert h.history("missing") == []

    def test_history_newest_first(self):
        h = DocHistory()
        e1 = _rec(h, after="a")
        e2 = _rec(h, after="b")
        e3 = _rec(h, after="c")
        result = h.history("d1")
        assert [e.edit_id for e in result] == [e3.edit_id, e2.edit_id, e1.edit_id]

    def test_history_with_limit(self):
        h = DocHistory()
        for _ in range(5):
            _rec(h)
        result = h.history("d1", limit=2)
        assert len(result) == 2

    def test_history_excludes_undone(self):
        h = DocHistory()
        _rec(h, after="a")
        _rec(h, after="b")
        h.undo("d1")
        assert len(h.history("d1")) == 1


# --------------------------------------------------------------------- current_content
class TestCurrentContent:
    def test_none_for_unknown_doc(self):
        h = DocHistory()
        assert h.current_content("none") is None

    def test_after_single_edit(self):
        h = DocHistory()
        _rec(h, after="hello")
        assert h.current_content("d1") == "hello"

    def test_reflects_latest_edit(self):
        h = DocHistory()
        _rec(h, after="one")
        _rec(h, after="two")
        assert h.current_content("d1") == "two"

    def test_after_undo(self):
        h = DocHistory()
        _rec(h, before="", after="one")
        _rec(h, before="one", after="two")
        h.undo("d1")
        assert h.current_content("d1") == "one"

    def test_after_undo_to_empty(self):
        h = DocHistory()
        _rec(h, before="start", after="x")
        h.undo("d1")
        # Falls back to 'before' of the undone edit
        assert h.current_content("d1") == "start"


# --------------------------------------------------------------------- redo clear
class TestNewEditClearsRedo:
    def test_record_clears_redo(self):
        h = DocHistory()
        _rec(h, after="a")
        _rec(h, after="b")
        h.undo("d1")
        assert h.can_redo("d1")
        _rec(h, after="c")
        assert not h.can_redo("d1")

    def test_other_doc_redo_preserved(self):
        h = DocHistory()
        _rec(h, doc="x", after="x1")
        h.undo("x")
        _rec(h, doc="y", after="y1")
        assert h.can_redo("x")


# --------------------------------------------------------------------- max history
class TestMaxHistory:
    def test_oldest_dropped(self):
        h = DocHistory(max_history=3)
        e1 = _rec(h, after="1")
        e2 = _rec(h, after="2")
        e3 = _rec(h, after="3")
        e4 = _rec(h, after="4")
        ids = [e.edit_id for e in h.history("d1")]
        assert e1.edit_id not in ids
        assert e4.edit_id in ids
        assert len(ids) == 3

    def test_default_max_history(self):
        h = DocHistory()
        assert h.max_history == 100

    def test_invalid_max_history(self):
        with pytest.raises(ValueError):
            DocHistory(max_history=0)
        with pytest.raises(ValueError):
            DocHistory(max_history=-1)

    def test_max_one(self):
        h = DocHistory(max_history=1)
        _rec(h, after="a")
        _rec(h, after="b")
        hist = h.history("d1")
        assert len(hist) == 1
        assert hist[0].after == "b"


# --------------------------------------------------------------------- snapshot
class TestTakeSnapshot:
    def test_returns_snapshot(self):
        h = DocHistory()
        s = h.take_snapshot("d1", "content", label="v1", now=10.0)
        assert isinstance(s, DocSnapshot)
        assert s.snapshot_id == 1
        assert s.doc_id == "d1"
        assert s.content == "content"
        assert s.label == "v1"
        assert s.timestamp == 10.0

    def test_sequential_ids(self):
        h = DocHistory()
        s1 = h.take_snapshot("d1", "a")
        s2 = h.take_snapshot("d2", "b")
        assert s2.snapshot_id == s1.snapshot_id + 1

    def test_no_label(self):
        h = DocHistory()
        s = h.take_snapshot("d1", "x")
        assert s.label is None


# --------------------------------------------------------------------- restore
class TestRestoreSnapshot:
    def test_returns_content(self):
        h = DocHistory()
        s = h.take_snapshot("d1", "original")
        assert h.restore_snapshot(s.snapshot_id) == "original"

    def test_unknown_returns_none(self):
        h = DocHistory()
        assert h.restore_snapshot(999) is None

    def test_clears_redo(self):
        h = DocHistory()
        _rec(h, after="x")
        h.undo("d1")
        assert h.can_redo("d1")
        s = h.take_snapshot("d1", "snap")
        h.restore_snapshot(s.snapshot_id)
        assert not h.can_redo("d1")


# --------------------------------------------------------------------- list snapshots
class TestListSnapshots:
    def test_empty(self):
        h = DocHistory()
        assert h.list_snapshots("any") == []

    def test_lists_for_doc(self):
        h = DocHistory()
        h.take_snapshot("a", "1")
        h.take_snapshot("b", "2")
        h.take_snapshot("a", "3")
        a_list = h.list_snapshots("a")
        assert len(a_list) == 2
        assert all(s.doc_id == "a" for s in a_list)

    def test_other_doc_excluded(self):
        h = DocHistory()
        h.take_snapshot("a", "x")
        assert h.list_snapshots("b") == []


# --------------------------------------------------------------------- delete snapshot
class TestDeleteSnapshot:
    def test_delete_existing(self):
        h = DocHistory()
        s = h.take_snapshot("d1", "x")
        assert h.delete_snapshot(s.snapshot_id) is True
        assert h.restore_snapshot(s.snapshot_id) is None

    def test_delete_missing(self):
        h = DocHistory()
        assert h.delete_snapshot(999) is False

    def test_delete_twice(self):
        h = DocHistory()
        s = h.take_snapshot("d1", "x")
        h.delete_snapshot(s.snapshot_id)
        assert h.delete_snapshot(s.snapshot_id) is False


# --------------------------------------------------------------------- diff
class TestDiffEdits:
    def test_diff_basic(self):
        h = DocHistory()
        e1 = h.record("d1", EditType.REPLACE, "hello world", "hello brave world")
        e2 = h.record("d1", EditType.REPLACE, "hello brave world", "hello brave new world")
        diff = h.diff_edits("d1", e1.edit_id, e2.edit_id)
        assert "hello world" in diff or "hello brave new world" in diff
        assert diff != ""

    def test_diff_unknown_doc(self):
        h = DocHistory()
        assert h.diff_edits("missing", 1, 2) == ""

    def test_diff_unknown_edit(self):
        h = DocHistory()
        _rec(h)
        assert h.diff_edits("d1", 1, 999) == ""

    def test_diff_includes_unified_markers(self):
        h = DocHistory()
        e1 = h.record("d1", EditType.REPLACE, "line a\n", "line b\n")
        e2 = h.record("d1", EditType.REPLACE, "line b\n", "line c\n")
        diff = h.diff_edits("d1", e1.edit_id, e2.edit_id)
        assert "edit-" in diff

    def test_diff_finds_undone_edit(self):
        h = DocHistory()
        e1 = h.record("d1", EditType.REPLACE, "a", "b")
        e2 = h.record("d1", EditType.REPLACE, "b", "c")
        h.undo("d1")
        # e2 is now in undone; diff_edits should still find it
        diff = h.diff_edits("d1", e1.edit_id, e2.edit_id)
        assert diff != ""


# --------------------------------------------------------------------- stats
class TestStats:
    def test_empty(self):
        h = DocHistory()
        s = h.stats()
        assert s.total_edits == 0
        assert s.total_snapshots == 0
        assert s.edits_per_doc == {}
        assert s.can_undo_count == 0

    def test_with_edits(self):
        h = DocHistory()
        _rec(h, doc="a")
        _rec(h, doc="a")
        _rec(h, doc="b")
        s = h.stats()
        assert s.total_edits == 3
        assert s.edits_per_doc["a"] == 2
        assert s.edits_per_doc["b"] == 1
        assert s.can_undo_count == 3

    def test_with_snapshots(self):
        h = DocHistory()
        h.take_snapshot("a", "x")
        h.take_snapshot("b", "y")
        s = h.stats()
        assert s.total_snapshots == 2

    def test_undo_reduces_can_undo_count(self):
        h = DocHistory()
        _rec(h)
        _rec(h)
        h.undo("d1")
        s = h.stats()
        assert s.can_undo_count == 1
        assert s.total_edits == 2  # both still tracked


# --------------------------------------------------------------------- clear
class TestClear:
    def test_clear_all(self):
        h = DocHistory()
        _rec(h, doc="a")
        _rec(h, doc="b")
        removed = h.clear()
        assert removed == 2
        assert not h.can_undo("a")
        assert not h.can_undo("b")

    def test_clear_single_doc(self):
        h = DocHistory()
        _rec(h, doc="a")
        _rec(h, doc="b")
        removed = h.clear("a")
        assert removed == 1
        assert not h.can_undo("a")
        assert h.can_undo("b")

    def test_clear_missing(self):
        h = DocHistory()
        assert h.clear("missing") == 0

    def test_clear_empty(self):
        h = DocHistory()
        assert h.clear() == 0

    def test_clear_includes_undone(self):
        h = DocHistory()
        _rec(h)
        _rec(h)
        h.undo("d1")
        # 1 applied + 1 undone = 2 removed
        assert h.clear("d1") == 2


# --------------------------------------------------------------------- edge cases
class TestEdgeCases:
    def test_total_edits_property(self):
        h = DocHistory()
        assert h.total_edits == 0
        _rec(h)
        assert h.total_edits == 1
        _rec(h)
        assert h.total_edits == 2

    def test_total_edits_includes_undone(self):
        h = DocHistory()
        _rec(h)
        h.undo("d1")
        assert h.total_edits == 1

    def test_record_with_now(self):
        h = DocHistory()
        e = _rec(h, now=42.5)
        assert e.timestamp == 42.5

    def test_independent_doc_stacks(self):
        h = DocHistory()
        _rec(h, doc="a", after="a1")
        _rec(h, doc="b", after="b1")
        h.undo("a")
        assert h.can_redo("a")
        assert not h.can_redo("b")
        assert h.current_content("b") == "b1"

    def test_thread_safety(self):
        h = DocHistory()
        errors = []

        def worker(doc):
            try:
                for i in range(50):
                    h.record(doc, EditType.INSERT, "", str(i))
            except Exception as exc:  # noqa
                errors.append(exc)

        threads = [
            threading.Thread(target=worker, args=(f"d{i}",))
            for i in range(4)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert errors == []
        stats = h.stats()
        # 4 docs × 50 = 200
        assert stats.total_edits == 200

    def test_history_limit_zero(self):
        h = DocHistory()
        _rec(h)
        assert h.history("d1", limit=0) == []

    def test_snapshot_creates_doc_bucket(self):
        h = DocHistory()
        s = h.take_snapshot("new", "content")
        # restoring should not crash on missing doc
        result = h.restore_snapshot(s.snapshot_id)
        assert result == "content"
