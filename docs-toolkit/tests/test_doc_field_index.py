"""Tests for the E364 DocFieldIndex module."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_field_index import DocFieldIndex, FieldRecord, IndexStats


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------
class TestFieldRecordDataclass:
    def test_construct_minimal(self):
        rec = FieldRecord(doc_id="d1")
        assert rec.doc_id == "d1"
        assert rec.field_values == {}

    def test_construct_with_values(self):
        rec = FieldRecord(doc_id="d2", field_values={"a": 1})
        assert rec.field_values == {"a": 1}

    def test_field_values_default_independent(self):
        a = FieldRecord(doc_id="a")
        b = FieldRecord(doc_id="b")
        a.field_values["x"] = 1
        assert "x" not in b.field_values

    def test_equality(self):
        a = FieldRecord(doc_id="d", field_values={"k": "v"})
        b = FieldRecord(doc_id="d", field_values={"k": "v"})
        assert a == b

    def test_inequality(self):
        a = FieldRecord(doc_id="d", field_values={"k": 1})
        b = FieldRecord(doc_id="d", field_values={"k": 2})
        assert a != b


class TestIndexStatsDataclass:
    def test_construct_minimal(self):
        s = IndexStats(total_records=0, indexed_fields=0)
        assert s.total_records == 0
        assert s.indexed_fields == 0
        assert s.unique_values_per_field == {}

    def test_construct_full(self):
        s = IndexStats(
            total_records=3,
            indexed_fields=2,
            unique_values_per_field={"a": 1, "b": 2},
        )
        assert s.unique_values_per_field == {"a": 1, "b": 2}

    def test_unique_values_default_independent(self):
        a = IndexStats(total_records=0, indexed_fields=0)
        b = IndexStats(total_records=0, indexed_fields=0)
        a.unique_values_per_field["x"] = 1
        assert "x" not in b.unique_values_per_field


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------
class TestConstruction:
    def test_empty_on_construct(self):
        idx = DocFieldIndex()
        assert idx.all_doc_ids() == []

    def test_stats_on_empty(self):
        idx = DocFieldIndex()
        s = idx.stats()
        assert s.total_records == 0
        assert s.indexed_fields == 0
        assert s.unique_values_per_field == {}

    def test_independent_instances(self):
        a = DocFieldIndex()
        b = DocFieldIndex()
        a.declare_field("x")
        a.index_record("d1", {"x": 1})
        assert b.all_doc_ids() == []


# ---------------------------------------------------------------------------
# declare_field
# ---------------------------------------------------------------------------
class TestDeclareField:
    def test_declare_single(self):
        idx = DocFieldIndex()
        idx.declare_field("status")
        assert idx.stats().indexed_fields == 1

    def test_declare_idempotent(self):
        idx = DocFieldIndex()
        idx.declare_field("status")
        idx.declare_field("status")
        assert idx.stats().indexed_fields == 1

    def test_declare_multiple(self):
        idx = DocFieldIndex()
        idx.declare_field("a")
        idx.declare_field("b")
        idx.declare_field("c")
        assert idx.stats().indexed_fields == 3

    def test_declare_backfills_existing_records(self):
        idx = DocFieldIndex()
        idx.index_record("d1", {"status": "ok"})
        idx.declare_field("status")
        assert idx.lookup_by_field("status", "ok") == ["d1"]


# ---------------------------------------------------------------------------
# index_record
# ---------------------------------------------------------------------------
class TestIndexRecord:
    def test_index_new(self):
        idx = DocFieldIndex()
        idx.declare_field("status")
        rec = idx.index_record("d1", {"status": "ok"})
        assert isinstance(rec, FieldRecord)
        assert rec.doc_id == "d1"
        assert rec.field_values == {"status": "ok"}

    def test_index_multiple_fields(self):
        idx = DocFieldIndex()
        idx.declare_field("status")
        idx.declare_field("score")
        idx.index_record("d1", {"status": "ok", "score": 5})
        assert idx.lookup_by_field("status", "ok") == ["d1"]
        assert idx.lookup_by_field("score", 5) == ["d1"]

    def test_reindex_removes_old(self):
        idx = DocFieldIndex()
        idx.declare_field("status")
        idx.index_record("d1", {"status": "old"})
        idx.index_record("d1", {"status": "new"})
        assert idx.lookup_by_field("status", "old") == []
        assert idx.lookup_by_field("status", "new") == ["d1"]

    def test_reindex_changes_count(self):
        idx = DocFieldIndex()
        idx.declare_field("status")
        idx.index_record("d1", {"status": "x"})
        idx.index_record("d1", {"status": "y"})
        assert idx.count_for_value("status", "x") == 0
        assert idx.count_for_value("status", "y") == 1

    def test_index_undeclared_field_ignored(self):
        idx = DocFieldIndex()
        idx.index_record("d1", {"status": "ok"})
        assert idx.lookup_by_field("status", "ok") == []

    def test_record_stored_even_for_undeclared(self):
        idx = DocFieldIndex()
        idx.index_record("d1", {"x": 1})
        assert idx.get_record("d1") is not None

    def test_field_values_are_copied(self):
        idx = DocFieldIndex()
        idx.declare_field("a")
        external = {"a": 1}
        idx.index_record("d1", external)
        external["a"] = 99
        assert idx.lookup_by_field("a", 1) == ["d1"]


# ---------------------------------------------------------------------------
# remove_record
# ---------------------------------------------------------------------------
class TestRemoveRecord:
    def test_remove_existing(self):
        idx = DocFieldIndex()
        idx.declare_field("status")
        idx.index_record("d1", {"status": "ok"})
        assert idx.remove_record("d1") is True

    def test_remove_clears_indexes(self):
        idx = DocFieldIndex()
        idx.declare_field("status")
        idx.index_record("d1", {"status": "ok"})
        idx.remove_record("d1")
        assert idx.lookup_by_field("status", "ok") == []

    def test_remove_missing(self):
        idx = DocFieldIndex()
        assert idx.remove_record("nope") is False

    def test_remove_only_target(self):
        idx = DocFieldIndex()
        idx.declare_field("s")
        idx.index_record("d1", {"s": "x"})
        idx.index_record("d2", {"s": "x"})
        idx.remove_record("d1")
        assert idx.lookup_by_field("s", "x") == ["d2"]


# ---------------------------------------------------------------------------
# get_record
# ---------------------------------------------------------------------------
class TestGetRecord:
    def test_get_existing(self):
        idx = DocFieldIndex()
        idx.index_record("d1", {"a": 1})
        rec = idx.get_record("d1")
        assert rec is not None and rec.doc_id == "d1"

    def test_get_missing(self):
        idx = DocFieldIndex()
        assert idx.get_record("nope") is None


# ---------------------------------------------------------------------------
# lookup_by_field
# ---------------------------------------------------------------------------
class TestLookupByField:
    def test_exact_match_single(self):
        idx = DocFieldIndex()
        idx.declare_field("s")
        idx.index_record("d1", {"s": "x"})
        assert idx.lookup_by_field("s", "x") == ["d1"]

    def test_exact_match_multiple_sorted(self):
        idx = DocFieldIndex()
        idx.declare_field("s")
        idx.index_record("d2", {"s": "x"})
        idx.index_record("d1", {"s": "x"})
        idx.index_record("d3", {"s": "x"})
        assert idx.lookup_by_field("s", "x") == ["d1", "d2", "d3"]

    def test_no_match(self):
        idx = DocFieldIndex()
        idx.declare_field("s")
        idx.index_record("d1", {"s": "x"})
        assert idx.lookup_by_field("s", "y") == []

    def test_empty_for_undeclared_field(self):
        idx = DocFieldIndex()
        idx.index_record("d1", {"s": "x"})
        assert idx.lookup_by_field("s", "x") == []


# ---------------------------------------------------------------------------
# lookup_by_range
# ---------------------------------------------------------------------------
class TestLookupByRange:
    def test_inclusive_bounds(self):
        idx = DocFieldIndex()
        idx.declare_field("score")
        idx.index_record("d1", {"score": 5})
        idx.index_record("d2", {"score": 10})
        idx.index_record("d3", {"score": 15})
        assert idx.lookup_by_range("score", 5, 15) == ["d1", "d2", "d3"]

    def test_exclusive_outside(self):
        idx = DocFieldIndex()
        idx.declare_field("score")
        idx.index_record("d1", {"score": 1})
        idx.index_record("d2", {"score": 5})
        idx.index_record("d3", {"score": 10})
        assert idx.lookup_by_range("score", 3, 7) == ["d2"]

    def test_sorted_output(self):
        idx = DocFieldIndex()
        idx.declare_field("score")
        idx.index_record("z", {"score": 1})
        idx.index_record("a", {"score": 2})
        idx.index_record("m", {"score": 3})
        assert idx.lookup_by_range("score", 0, 100) == ["a", "m", "z"]

    def test_empty_range(self):
        idx = DocFieldIndex()
        idx.declare_field("score")
        idx.index_record("d1", {"score": 10})
        assert idx.lookup_by_range("score", 100, 200) == []

    def test_undeclared_returns_empty(self):
        idx = DocFieldIndex()
        idx.index_record("d1", {"score": 5})
        assert idx.lookup_by_range("score", 0, 10) == []

    def test_string_range(self):
        idx = DocFieldIndex()
        idx.declare_field("name")
        idx.index_record("d1", {"name": "alpha"})
        idx.index_record("d2", {"name": "beta"})
        idx.index_record("d3", {"name": "zulu"})
        assert idx.lookup_by_range("name", "alpha", "beta") == ["d1", "d2"]


# ---------------------------------------------------------------------------
# values_for_field
# ---------------------------------------------------------------------------
class TestValuesForField:
    def test_sorted_unique(self):
        idx = DocFieldIndex()
        idx.declare_field("s")
        idx.index_record("d1", {"s": "b"})
        idx.index_record("d2", {"s": "a"})
        idx.index_record("d3", {"s": "a"})
        assert idx.values_for_field("s") == ["a", "b"]

    def test_empty_for_undeclared(self):
        idx = DocFieldIndex()
        assert idx.values_for_field("nope") == []

    def test_empty_after_clear(self):
        idx = DocFieldIndex()
        idx.declare_field("s")
        idx.index_record("d1", {"s": "x"})
        idx.clear()
        assert idx.values_for_field("s") == []


# ---------------------------------------------------------------------------
# count_for_value
# ---------------------------------------------------------------------------
class TestCountForValue:
    def test_count_basic(self):
        idx = DocFieldIndex()
        idx.declare_field("s")
        idx.index_record("d1", {"s": "x"})
        idx.index_record("d2", {"s": "x"})
        idx.index_record("d3", {"s": "y"})
        assert idx.count_for_value("s", "x") == 2
        assert idx.count_for_value("s", "y") == 1

    def test_count_unknown_value(self):
        idx = DocFieldIndex()
        idx.declare_field("s")
        assert idx.count_for_value("s", "nope") == 0

    def test_count_undeclared(self):
        idx = DocFieldIndex()
        assert idx.count_for_value("s", "x") == 0


# ---------------------------------------------------------------------------
# update_field
# ---------------------------------------------------------------------------
class TestUpdateField:
    def test_update_existing_returns_true(self):
        idx = DocFieldIndex()
        idx.declare_field("s")
        idx.index_record("d1", {"s": "x"})
        assert idx.update_field("d1", "s", "y") is True

    def test_update_missing_returns_false(self):
        idx = DocFieldIndex()
        assert idx.update_field("nope", "s", "y") is False

    def test_update_refreshes_indexes(self):
        idx = DocFieldIndex()
        idx.declare_field("s")
        idx.index_record("d1", {"s": "x"})
        idx.update_field("d1", "s", "y")
        assert idx.lookup_by_field("s", "x") == []
        assert idx.lookup_by_field("s", "y") == ["d1"]

    def test_update_adds_new_field(self):
        idx = DocFieldIndex()
        idx.declare_field("score")
        idx.index_record("d1", {"s": "x"})
        idx.update_field("d1", "score", 42)
        assert idx.lookup_by_field("score", 42) == ["d1"]

    def test_update_undeclared_field_stores_value(self):
        idx = DocFieldIndex()
        idx.index_record("d1", {"a": 1})
        assert idx.update_field("d1", "b", 2) is True
        rec = idx.get_record("d1")
        assert rec.field_values["b"] == 2


# ---------------------------------------------------------------------------
# all_doc_ids
# ---------------------------------------------------------------------------
class TestAllDocIds:
    def test_empty(self):
        idx = DocFieldIndex()
        assert idx.all_doc_ids() == []

    def test_sorted(self):
        idx = DocFieldIndex()
        idx.index_record("z", {})
        idx.index_record("a", {})
        idx.index_record("m", {})
        assert idx.all_doc_ids() == ["a", "m", "z"]

    def test_after_remove(self):
        idx = DocFieldIndex()
        idx.index_record("a", {})
        idx.index_record("b", {})
        idx.remove_record("a")
        assert idx.all_doc_ids() == ["b"]


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------
class TestClear:
    def test_clear_returns_count(self):
        idx = DocFieldIndex()
        idx.index_record("a", {})
        idx.index_record("b", {})
        assert idx.clear() == 2

    def test_clear_empty(self):
        idx = DocFieldIndex()
        assert idx.clear() == 0

    def test_clear_resets_records(self):
        idx = DocFieldIndex()
        idx.declare_field("s")
        idx.index_record("d1", {"s": "x"})
        idx.clear()
        assert idx.all_doc_ids() == []
        assert idx.lookup_by_field("s", "x") == []

    def test_clear_preserves_field_declarations(self):
        idx = DocFieldIndex()
        idx.declare_field("s")
        idx.index_record("d1", {"s": "x"})
        idx.clear()
        assert idx.stats().indexed_fields == 1


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------
class TestStats:
    def test_totals(self):
        idx = DocFieldIndex()
        idx.declare_field("s")
        idx.declare_field("score")
        idx.index_record("d1", {"s": "x", "score": 1})
        idx.index_record("d2", {"s": "y", "score": 2})
        s = idx.stats()
        assert s.total_records == 2
        assert s.indexed_fields == 2

    def test_unique_values_per_field(self):
        idx = DocFieldIndex()
        idx.declare_field("s")
        idx.index_record("d1", {"s": "x"})
        idx.index_record("d2", {"s": "y"})
        idx.index_record("d3", {"s": "y"})
        s = idx.stats()
        assert s.unique_values_per_field["s"] == 2

    def test_stats_updates_after_remove(self):
        idx = DocFieldIndex()
        idx.declare_field("s")
        idx.index_record("d1", {"s": "x"})
        idx.remove_record("d1")
        s = idx.stats()
        assert s.total_records == 0
        assert s.unique_values_per_field["s"] == 0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_index_record(self):
        idx = DocFieldIndex()
        idx.declare_field("group")
        n_threads = 8
        per_thread = 50

        def worker(start):
            for i in range(per_thread):
                idx.index_record(f"d{start}-{i}", {"group": start})

        threads = [
            threading.Thread(target=worker, args=(t,)) for t in range(n_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        s = idx.stats()
        assert s.total_records == n_threads * per_thread
        assert s.unique_values_per_field["group"] == n_threads

    def test_concurrent_index_and_remove(self):
        idx = DocFieldIndex()
        idx.declare_field("k")
        # Prime
        for i in range(200):
            idx.index_record(f"d{i}", {"k": i % 5})

        def remover():
            for i in range(200):
                idx.remove_record(f"d{i}")

        def adder():
            for i in range(200, 400):
                idx.index_record(f"d{i}", {"k": i % 5})

        threads = [threading.Thread(target=remover), threading.Thread(target=adder)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # All originals removed, all new ones present
        assert all(idx.get_record(f"d{i}") is None for i in range(200))
        assert all(idx.get_record(f"d{i}") is not None for i in range(200, 400))


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
