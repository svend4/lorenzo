"""Tests for docstoolkit.doc_index_builder (E313 — composite document index).

Coverage target: >= 55 tests.
"""
from __future__ import annotations

import sys
import threading
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.doc_index_builder import (
    DocIndexBuilder,
    IndexEntry,
    IndexField,
    IndexStats,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_builder() -> DocIndexBuilder:
    return DocIndexBuilder()


def builder_with_fields(*names: str, indexed: bool = True) -> DocIndexBuilder:
    b = make_builder()
    for name in names:
        b.define_field(IndexField(name=name, indexed=indexed))
    return b


# ===========================================================================
# 1. IndexField dataclass
# ===========================================================================

class TestIndexFieldDataclass:
    def test_required_name(self):
        f = IndexField(name="title")
        assert f.name == "title"

    def test_default_field_type(self):
        f = IndexField(name="x")
        assert f.field_type == "str"

    def test_default_indexed_true(self):
        f = IndexField(name="x")
        assert f.indexed is True

    def test_default_sortable_false(self):
        f = IndexField(name="x")
        assert f.sortable is False

    def test_explicit_int_type(self):
        f = IndexField(name="count", field_type="int")
        assert f.field_type == "int"

    def test_explicit_not_indexed(self):
        f = IndexField(name="body", indexed=False)
        assert f.indexed is False

    def test_explicit_sortable(self):
        f = IndexField(name="score", sortable=True)
        assert f.sortable is True

    def test_all_fields_settable(self):
        f = IndexField(name="n", field_type="float", indexed=False, sortable=True)
        assert f.name == "n"
        assert f.field_type == "float"
        assert f.indexed is False
        assert f.sortable is True


# ===========================================================================
# 2. IndexEntry dataclass
# ===========================================================================

class TestIndexEntryDataclass:
    def test_basic_construction(self):
        e = IndexEntry(doc_id="d1")
        assert e.doc_id == "d1"
        assert e.fields == {}

    def test_fields_default_factory_is_independent(self):
        a = IndexEntry(doc_id="a")
        b = IndexEntry(doc_id="b")
        a.fields["k"] = 1
        assert b.fields == {}

    def test_fields_can_be_supplied(self):
        e = IndexEntry(doc_id="x", fields={"title": "hello"})
        assert e.fields == {"title": "hello"}

    def test_doc_id_type(self):
        e = IndexEntry(doc_id="abc")
        assert isinstance(e.doc_id, str)


# ===========================================================================
# 3. IndexStats dataclass
# ===========================================================================

class TestIndexStatsDataclass:
    def test_construction(self):
        s = IndexStats(total_docs=5, total_fields=3, indexed_fields=2)
        assert s.total_docs == 5
        assert s.total_fields == 3
        assert s.indexed_fields == 2

    def test_zero_defaults(self):
        s = IndexStats(total_docs=0, total_fields=0, indexed_fields=0)
        assert s.total_docs == 0


# ===========================================================================
# 4. Construction
# ===========================================================================

class TestConstruction:
    def test_empty_builder(self):
        b = make_builder()
        assert b.all_doc_ids() == []
        assert b.list_fields() == []

    def test_stats_on_empty(self):
        s = make_builder().stats()
        assert s.total_docs == 0
        assert s.total_fields == 0
        assert s.indexed_fields == 0


# ===========================================================================
# 5. define_field
# ===========================================================================

class TestDefineField:
    def test_register_new_field(self):
        b = make_builder()
        b.define_field(IndexField(name="title"))
        assert b.get_field("title") is not None

    def test_replace_existing_field(self):
        b = make_builder()
        b.define_field(IndexField(name="score", field_type="str"))
        b.define_field(IndexField(name="score", field_type="int"))
        assert b.get_field("score").field_type == "int"

    def test_default_values_preserved(self):
        b = make_builder()
        b.define_field(IndexField(name="x"))
        f = b.get_field("x")
        assert f.field_type == "str"
        assert f.indexed is True
        assert f.sortable is False

    def test_not_indexed_field_has_no_inverted_bucket(self):
        b = make_builder()
        b.define_field(IndexField(name="body", indexed=False))
        # lookup should return empty (no bucket)
        assert b.lookup("body", "anything") == []


# ===========================================================================
# 6. remove_field
# ===========================================================================

class TestRemoveField:
    def test_remove_existing_returns_true(self):
        b = builder_with_fields("title")
        assert b.remove_field("title") is True

    def test_remove_missing_returns_false(self):
        b = make_builder()
        assert b.remove_field("nonexistent") is False

    def test_removes_from_list_fields(self):
        b = builder_with_fields("title", "body")
        b.remove_field("title")
        names = [f.name for f in b.list_fields()]
        assert "title" not in names
        assert "body" in names

    def test_removes_inverted_index_data(self):
        b = builder_with_fields("tag")
        b.index_doc("d1", {"tag": "python"})
        b.remove_field("tag")
        # After field removal the inverted bucket is gone, lookup must be empty
        assert b.lookup("tag", "python") == []

    def test_double_remove_returns_false(self):
        b = builder_with_fields("x")
        b.remove_field("x")
        assert b.remove_field("x") is False


# ===========================================================================
# 7. get_field
# ===========================================================================

class TestGetField:
    def test_found(self):
        b = make_builder()
        b.define_field(IndexField(name="f1", field_type="bool"))
        f = b.get_field("f1")
        assert f is not None
        assert f.name == "f1"

    def test_not_found(self):
        b = make_builder()
        assert b.get_field("missing") is None


# ===========================================================================
# 8. list_fields
# ===========================================================================

class TestListFields:
    def test_sorted_alphabetically(self):
        b = make_builder()
        for name in ["zebra", "alpha", "monkey"]:
            b.define_field(IndexField(name=name))
        names = [f.name for f in b.list_fields()]
        assert names == ["alpha", "monkey", "zebra"]

    def test_empty_when_no_fields(self):
        assert make_builder().list_fields() == []


# ===========================================================================
# 9. index_doc
# ===========================================================================

class TestIndexDoc:
    def test_stores_entry(self):
        b = builder_with_fields("title")
        b.index_doc("d1", {"title": "hello"})
        entry = b.get_entry("d1")
        assert entry is not None
        assert entry.doc_id == "d1"
        assert entry.fields["title"] == "hello"

    def test_builds_inverted_index(self):
        b = builder_with_fields("tag")
        b.index_doc("d1", {"tag": "python"})
        assert "d1" in b.lookup("tag", "python")

    def test_returns_index_entry(self):
        b = builder_with_fields("title")
        result = b.index_doc("d1", {"title": "t"})
        assert isinstance(result, IndexEntry)
        assert result.doc_id == "d1"

    def test_reindex_removes_old_values(self):
        b = builder_with_fields("status")
        b.index_doc("d1", {"status": "draft"})
        b.index_doc("d1", {"status": "published"})
        assert b.lookup("status", "draft") == []
        assert "d1" in b.lookup("status", "published")

    def test_multiple_docs_same_value(self):
        b = builder_with_fields("lang")
        b.index_doc("d1", {"lang": "python"})
        b.index_doc("d2", {"lang": "python"})
        result = b.lookup("lang", "python")
        assert sorted(result) == ["d1", "d2"]

    def test_fields_not_in_definition_still_stored(self):
        b = make_builder()
        b.index_doc("d1", {"unknown_field": "value"})
        entry = b.get_entry("d1")
        assert entry.fields["unknown_field"] == "value"


# ===========================================================================
# 10. remove_doc
# ===========================================================================

class TestRemoveDoc:
    def test_remove_existing_returns_true(self):
        b = builder_with_fields("title")
        b.index_doc("d1", {"title": "x"})
        assert b.remove_doc("d1") is True

    def test_remove_missing_returns_false(self):
        b = make_builder()
        assert b.remove_doc("ghost") is False

    def test_removes_from_entries(self):
        b = builder_with_fields("title")
        b.index_doc("d1", {"title": "t"})
        b.remove_doc("d1")
        assert b.get_entry("d1") is None

    def test_removes_from_inverted_index(self):
        b = builder_with_fields("category")
        b.index_doc("d1", {"category": "news"})
        b.remove_doc("d1")
        assert b.lookup("category", "news") == []

    def test_does_not_affect_other_docs(self):
        b = builder_with_fields("category")
        b.index_doc("d1", {"category": "news"})
        b.index_doc("d2", {"category": "news"})
        b.remove_doc("d1")
        assert b.lookup("category", "news") == ["d2"]


# ===========================================================================
# 11. get_entry
# ===========================================================================

class TestGetEntry:
    def test_found(self):
        b = make_builder()
        b.index_doc("d1", {"x": 1})
        assert b.get_entry("d1") is not None

    def test_not_found(self):
        b = make_builder()
        assert b.get_entry("missing") is None


# ===========================================================================
# 12. lookup
# ===========================================================================

class TestLookup:
    def test_exact_match(self):
        b = builder_with_fields("color")
        b.index_doc("d1", {"color": "red"})
        assert b.lookup("color", "red") == ["d1"]

    def test_no_match_returns_empty(self):
        b = builder_with_fields("color")
        b.index_doc("d1", {"color": "red"})
        assert b.lookup("color", "blue") == []

    def test_unindexed_field_returns_empty(self):
        b = make_builder()
        b.define_field(IndexField(name="body", indexed=False))
        b.index_doc("d1", {"body": "hello"})
        assert b.lookup("body", "hello") == []

    def test_unknown_field_returns_empty(self):
        b = make_builder()
        assert b.lookup("no_such_field", "value") == []

    def test_result_is_sorted(self):
        b = builder_with_fields("type")
        for doc_id in ["z1", "a1", "m1"]:
            b.index_doc(doc_id, {"type": "article"})
        result = b.lookup("type", "article")
        assert result == sorted(result)


# ===========================================================================
# 13. query
# ===========================================================================

class TestQuery:
    def test_single_filter(self):
        b = builder_with_fields("lang")
        b.index_doc("d1", {"lang": "python"})
        b.index_doc("d2", {"lang": "go"})
        assert b.query({"lang": "python"}) == ["d1"]

    def test_and_of_two_filters(self):
        b = builder_with_fields("lang", "status")
        b.index_doc("d1", {"lang": "python", "status": "active"})
        b.index_doc("d2", {"lang": "python", "status": "inactive"})
        b.index_doc("d3", {"lang": "go", "status": "active"})
        result = b.query({"lang": "python", "status": "active"})
        assert result == ["d1"]

    def test_no_match_returns_empty(self):
        b = builder_with_fields("x")
        b.index_doc("d1", {"x": "a"})
        assert b.query({"x": "z"}) == []

    def test_empty_filters_returns_empty(self):
        b = builder_with_fields("x")
        b.index_doc("d1", {"x": "a"})
        assert b.query({}) == []

    def test_result_is_sorted(self):
        b = builder_with_fields("tag")
        for doc_id in ["c", "a", "b"]:
            b.index_doc(doc_id, {"tag": "shared"})
        result = b.query({"tag": "shared"})
        assert result == ["a", "b", "c"]

    def test_unknown_field_in_filter_returns_empty(self):
        b = builder_with_fields("x")
        b.index_doc("d1", {"x": "a"})
        assert b.query({"no_such_field": "a"}) == []


# ===========================================================================
# 14. sort_by
# ===========================================================================

class TestSortBy:
    def test_ascending(self):
        b = builder_with_fields("score")
        b.index_doc("d1", {"score": 3})
        b.index_doc("d2", {"score": 1})
        b.index_doc("d3", {"score": 2})
        result = b.sort_by("score")
        assert result == ["d2", "d3", "d1"]

    def test_descending(self):
        b = builder_with_fields("score")
        b.index_doc("d1", {"score": 3})
        b.index_doc("d2", {"score": 1})
        b.index_doc("d3", {"score": 2})
        result = b.sort_by("score", reverse=True)
        assert result == ["d1", "d3", "d2"]

    def test_missing_field_sorts_last(self):
        b = builder_with_fields("priority")
        b.index_doc("d1", {"priority": 1})
        b.index_doc("d2", {})  # no priority
        b.index_doc("d3", {"priority": 2})
        result = b.sort_by("priority")
        # d1 (1) < d3 (2) come first; d2 (missing) comes last
        assert result.index("d2") == 2

    def test_missing_field_sorts_last_reverse(self):
        b = builder_with_fields("priority")
        b.index_doc("d1", {"priority": 1})
        b.index_doc("d2", {})
        result = b.sort_by("priority", reverse=True)
        assert result[-1] == "d2"

    def test_string_values_sorted_lexicographically(self):
        b = builder_with_fields("name")
        b.index_doc("x", {"name": "charlie"})
        b.index_doc("y", {"name": "alice"})
        b.index_doc("z", {"name": "bob"})
        result = b.sort_by("name")
        assert result == ["y", "z", "x"]


# ===========================================================================
# 15. all_doc_ids
# ===========================================================================

class TestAllDocIds:
    def test_sorted(self):
        b = make_builder()
        for doc_id in ["z", "a", "m"]:
            b.index_doc(doc_id, {})
        assert b.all_doc_ids() == ["a", "m", "z"]

    def test_empty(self):
        assert make_builder().all_doc_ids() == []

    def test_after_removal(self):
        b = make_builder()
        b.index_doc("d1", {})
        b.index_doc("d2", {})
        b.remove_doc("d1")
        assert b.all_doc_ids() == ["d2"]


# ===========================================================================
# 16. stats
# ===========================================================================

class TestStats:
    def test_total_docs(self):
        b = make_builder()
        b.index_doc("d1", {})
        b.index_doc("d2", {})
        assert b.stats().total_docs == 2

    def test_total_fields(self):
        b = builder_with_fields("a", "b", "c")
        assert b.stats().total_fields == 3

    def test_indexed_fields(self):
        b = make_builder()
        b.define_field(IndexField(name="f1", indexed=True))
        b.define_field(IndexField(name="f2", indexed=False))
        b.define_field(IndexField(name="f3", indexed=True))
        s = b.stats()
        assert s.indexed_fields == 2
        assert s.total_fields == 3

    def test_stats_after_remove_field(self):
        b = builder_with_fields("a", "b")
        b.remove_field("a")
        s = b.stats()
        assert s.total_fields == 1
        assert s.indexed_fields == 1

    def test_stats_after_remove_doc(self):
        b = make_builder()
        b.index_doc("d1", {})
        b.remove_doc("d1")
        assert b.stats().total_docs == 0


# ===========================================================================
# 17. Thread safety
# ===========================================================================

class TestThreadSafety:
    def test_concurrent_index_doc(self):
        """Many threads writing distinct doc_ids must all succeed."""
        b = builder_with_fields("val")
        errors: list[Exception] = []

        def worker(doc_id: str) -> None:
            try:
                b.index_doc(doc_id, {"val": doc_id})
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(f"d{i}",)) for i in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert b.stats().total_docs == 50
        ids = b.all_doc_ids()
        assert ids == sorted(ids)

    def test_concurrent_mixed_operations(self):
        """Interleaved index_doc and remove_doc must not raise."""
        b = builder_with_fields("x")
        errors: list[Exception] = []

        def index_worker(i: int) -> None:
            try:
                b.index_doc(f"ins{i}", {"x": str(i)})
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        def remove_worker(i: int) -> None:
            try:
                # Removal of a non-existent doc should just return False, not raise.
                b.remove_doc(f"ins{i}")
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = []
        for i in range(25):
            threads.append(threading.Thread(target=index_worker, args=(i,)))
            threads.append(threading.Thread(target=remove_worker, args=(i,)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
