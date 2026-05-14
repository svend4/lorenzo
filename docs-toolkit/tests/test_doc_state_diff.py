"""Tests for docstoolkit.doc_state_diff (E418)."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_state_diff import (
    DiffStats,
    DocStateDiff,
    FieldChange,
    StateDiffResult,
)


# ---------------------------------------------------------------------------
# FieldChange
# ---------------------------------------------------------------------------


class TestFieldChange:
    def test_create_added(self):
        fc = FieldChange("title", "added", None, "Hello")
        assert fc.field_name == "title"
        assert fc.change_type == "added"
        assert fc.old_value is None
        assert fc.new_value == "Hello"

    def test_create_removed(self):
        fc = FieldChange("tags", "removed", ["a"], None)
        assert fc.change_type == "removed"
        assert fc.old_value == ["a"]

    def test_create_modified(self):
        fc = FieldChange("count", "modified", 1, 2)
        assert fc.change_type == "modified"
        assert fc.old_value == 1
        assert fc.new_value == 2

    def test_default_values(self):
        fc = FieldChange("k", "added")
        assert fc.old_value is None
        assert fc.new_value is None


# ---------------------------------------------------------------------------
# StateDiffResult
# ---------------------------------------------------------------------------


class TestStateDiffResult:
    def test_create_empty(self):
        r = StateDiffResult(doc_id="d1", from_version="v1", to_version="v2")
        assert r.doc_id == "d1"
        assert r.from_version == "v1"
        assert r.to_version == "v2"
        assert r.changes == []
        assert r.added_count == 0
        assert r.removed_count == 0
        assert r.modified_count == 0

    def test_default_changes_isolated(self):
        a = StateDiffResult(doc_id="x", from_version="1", to_version="2")
        b = StateDiffResult(doc_id="y", from_version="1", to_version="2")
        a.changes.append(FieldChange("k", "added"))
        assert b.changes == []


# ---------------------------------------------------------------------------
# DiffStats
# ---------------------------------------------------------------------------


class TestDiffStats:
    def test_create(self):
        s = DiffStats(total_diffs=2, total_field_changes=5, unique_docs=3)
        assert s.total_diffs == 2
        assert s.total_field_changes == 5
        assert s.unique_docs == 3


# ---------------------------------------------------------------------------
# store_state / get_state / delete_state
# ---------------------------------------------------------------------------


class TestStoreGetDelete:
    def test_store_and_get(self):
        d = DocStateDiff()
        d.store_state("doc1", "v1", {"title": "T", "n": 1})
        st = d.get_state("doc1", "v1")
        assert st == {"title": "T", "n": 1}

    def test_get_missing_returns_none(self):
        d = DocStateDiff()
        assert d.get_state("nope", "v1") is None

    def test_store_copies_state(self):
        d = DocStateDiff()
        s = {"title": "T", "tags": ["a"]}
        d.store_state("doc1", "v1", s)
        s["title"] = "MUTATED"
        s["tags"].append("b")
        stored = d.get_state("doc1", "v1")
        assert stored == {"title": "T", "tags": ["a"]}

    def test_get_returns_copy(self):
        d = DocStateDiff()
        d.store_state("doc1", "v1", {"tags": ["a"]})
        st = d.get_state("doc1", "v1")
        st["tags"].append("b")
        again = d.get_state("doc1", "v1")
        assert again == {"tags": ["a"]}

    def test_delete_existing(self):
        d = DocStateDiff()
        d.store_state("doc1", "v1", {})
        assert d.delete_state("doc1", "v1") is True
        assert d.get_state("doc1", "v1") is None

    def test_delete_missing(self):
        d = DocStateDiff()
        assert d.delete_state("doc1", "v1") is False

    def test_overwrite_same_version(self):
        d = DocStateDiff()
        d.store_state("doc1", "v1", {"a": 1})
        d.store_state("doc1", "v1", {"a": 2})
        assert d.get_state("doc1", "v1") == {"a": 2}

    def test_multiple_versions(self):
        d = DocStateDiff()
        d.store_state("doc1", "v1", {"a": 1})
        d.store_state("doc1", "v2", {"a": 2})
        assert d.get_state("doc1", "v1") == {"a": 1}
        assert d.get_state("doc1", "v2") == {"a": 2}

    def test_multiple_docs(self):
        d = DocStateDiff()
        d.store_state("d1", "v1", {"x": 1})
        d.store_state("d2", "v1", {"x": 2})
        assert d.get_state("d1", "v1") == {"x": 1}
        assert d.get_state("d2", "v1") == {"x": 2}


# ---------------------------------------------------------------------------
# compute_diff
# ---------------------------------------------------------------------------


class TestComputeDiff:
    def test_diff_added(self):
        d = DocStateDiff()
        d.store_state("doc1", "v1", {"title": "T"})
        d.store_state("doc1", "v2", {"title": "T", "author": "A"})
        r = d.compute_diff("doc1", "v1", "v2")
        assert r is not None
        assert r.added_count == 1
        assert r.removed_count == 0
        assert r.modified_count == 0
        assert len(r.changes) == 1
        assert r.changes[0].field_name == "author"
        assert r.changes[0].change_type == "added"
        assert r.changes[0].new_value == "A"
        assert r.changes[0].old_value is None

    def test_diff_removed(self):
        d = DocStateDiff()
        d.store_state("doc1", "v1", {"title": "T", "author": "A"})
        d.store_state("doc1", "v2", {"title": "T"})
        r = d.compute_diff("doc1", "v1", "v2")
        assert r.removed_count == 1
        assert r.added_count == 0
        c = r.changes[0]
        assert c.field_name == "author"
        assert c.change_type == "removed"
        assert c.old_value == "A"
        assert c.new_value is None

    def test_diff_modified(self):
        d = DocStateDiff()
        d.store_state("doc1", "v1", {"title": "Old"})
        d.store_state("doc1", "v2", {"title": "New"})
        r = d.compute_diff("doc1", "v1", "v2")
        assert r.modified_count == 1
        c = r.changes[0]
        assert c.change_type == "modified"
        assert c.old_value == "Old"
        assert c.new_value == "New"

    def test_diff_mixed(self):
        d = DocStateDiff()
        d.store_state("doc1", "v1", {"a": 1, "b": 2, "c": 3})
        d.store_state("doc1", "v2", {"a": 1, "b": 20, "d": 4})
        r = d.compute_diff("doc1", "v1", "v2")
        assert r.added_count == 1  # d
        assert r.removed_count == 1  # c
        assert r.modified_count == 1  # b
        assert len(r.changes) == 3

    def test_diff_no_changes(self):
        d = DocStateDiff()
        d.store_state("doc1", "v1", {"a": 1, "b": 2})
        d.store_state("doc1", "v2", {"a": 1, "b": 2})
        r = d.compute_diff("doc1", "v1", "v2")
        assert r.added_count == 0
        assert r.removed_count == 0
        assert r.modified_count == 0
        assert r.changes == []

    def test_diff_sorted_by_field_name(self):
        d = DocStateDiff()
        d.store_state("doc1", "v1", {})
        d.store_state("doc1", "v2", {"z": 1, "a": 2, "m": 3})
        r = d.compute_diff("doc1", "v1", "v2")
        names = [c.field_name for c in r.changes]
        assert names == ["a", "m", "z"]

    def test_diff_from_missing(self):
        d = DocStateDiff()
        d.store_state("doc1", "v2", {})
        assert d.compute_diff("doc1", "v1", "v2") is None

    def test_diff_to_missing(self):
        d = DocStateDiff()
        d.store_state("doc1", "v1", {})
        assert d.compute_diff("doc1", "v1", "v2") is None

    def test_diff_both_missing(self):
        d = DocStateDiff()
        assert d.compute_diff("doc1", "v1", "v2") is None

    def test_diff_metadata_carries(self):
        d = DocStateDiff()
        d.store_state("doc7", "alpha", {})
        d.store_state("doc7", "beta", {})
        r = d.compute_diff("doc7", "alpha", "beta")
        assert r.doc_id == "doc7"
        assert r.from_version == "alpha"
        assert r.to_version == "beta"

    def test_diff_with_complex_values(self):
        d = DocStateDiff()
        d.store_state("d", "v1", {"list": [1, 2], "dict": {"x": 1}})
        d.store_state("d", "v2", {"list": [1, 2, 3], "dict": {"x": 1}})
        r = d.compute_diff("d", "v1", "v2")
        assert r.modified_count == 1
        assert r.changes[0].field_name == "list"

    def test_diff_caches_by_default(self):
        d = DocStateDiff()
        d.store_state("d", "v1", {"a": 1})
        d.store_state("d", "v2", {"a": 2})
        d.compute_diff("d", "v1", "v2")
        assert d.get_cached("d", "v1", "v2") is not None

    def test_diff_no_cache(self):
        d = DocStateDiff()
        d.store_state("d", "v1", {"a": 1})
        d.store_state("d", "v2", {"a": 2})
        d.compute_diff("d", "v1", "v2", cache=False)
        assert d.get_cached("d", "v1", "v2") is None

    def test_diff_value_is_deep_copied(self):
        d = DocStateDiff()
        d.store_state("d", "v1", {})
        d.store_state("d", "v2", {"lst": [1, 2]})
        r = d.compute_diff("d", "v1", "v2")
        r.changes[0].new_value.append(99)
        # Recompute and check original unchanged
        r2 = d.compute_diff("d", "v1", "v2", cache=False)
        assert r2.changes[0].new_value == [1, 2]


# ---------------------------------------------------------------------------
# get_cached / invalidate_cache
# ---------------------------------------------------------------------------


class TestCache:
    def test_get_cached_missing(self):
        d = DocStateDiff()
        assert d.get_cached("d", "v1", "v2") is None

    def test_get_cached_after_compute(self):
        d = DocStateDiff()
        d.store_state("d", "v1", {"a": 1})
        d.store_state("d", "v2", {"a": 2})
        r = d.compute_diff("d", "v1", "v2")
        cached = d.get_cached("d", "v1", "v2")
        assert cached is r

    def test_invalidate_all(self):
        d = DocStateDiff()
        d.store_state("d1", "v1", {})
        d.store_state("d1", "v2", {})
        d.store_state("d2", "v1", {})
        d.store_state("d2", "v2", {})
        d.compute_diff("d1", "v1", "v2")
        d.compute_diff("d2", "v1", "v2")
        n = d.invalidate_cache()
        assert n == 2
        assert d.get_cached("d1", "v1", "v2") is None
        assert d.get_cached("d2", "v1", "v2") is None

    def test_invalidate_one_doc(self):
        d = DocStateDiff()
        d.store_state("d1", "v1", {})
        d.store_state("d1", "v2", {})
        d.store_state("d2", "v1", {})
        d.store_state("d2", "v2", {})
        d.compute_diff("d1", "v1", "v2")
        d.compute_diff("d2", "v1", "v2")
        n = d.invalidate_cache("d1")
        assert n == 1
        assert d.get_cached("d1", "v1", "v2") is None
        assert d.get_cached("d2", "v1", "v2") is not None

    def test_invalidate_unknown_doc(self):
        d = DocStateDiff()
        assert d.invalidate_cache("unknown") == 0

    def test_invalidate_empty(self):
        d = DocStateDiff()
        assert d.invalidate_cache() == 0


# ---------------------------------------------------------------------------
# versions_for / all_doc_ids
# ---------------------------------------------------------------------------


class TestEnumeration:
    def test_versions_for_empty(self):
        d = DocStateDiff()
        assert d.versions_for("d1") == []

    def test_versions_for_sorted(self):
        d = DocStateDiff()
        d.store_state("d1", "v3", {})
        d.store_state("d1", "v1", {})
        d.store_state("d1", "v2", {})
        assert d.versions_for("d1") == ["v1", "v2", "v3"]

    def test_versions_for_isolates_doc(self):
        d = DocStateDiff()
        d.store_state("d1", "v1", {})
        d.store_state("d2", "v9", {})
        assert d.versions_for("d1") == ["v1"]

    def test_all_doc_ids_empty(self):
        assert DocStateDiff().all_doc_ids() == []

    def test_all_doc_ids_sorted_unique(self):
        d = DocStateDiff()
        d.store_state("zeta", "v1", {})
        d.store_state("alpha", "v1", {})
        d.store_state("alpha", "v2", {})
        d.store_state("mid", "v1", {})
        assert d.all_doc_ids() == ["alpha", "mid", "zeta"]


# ---------------------------------------------------------------------------
# apply_diff
# ---------------------------------------------------------------------------


class TestApplyDiff:
    def test_apply_added(self):
        d = DocStateDiff()
        d.store_state("d", "v1", {"a": 1})
        d.store_state("d", "v2", {"a": 1, "b": 2})
        diff = d.compute_diff("d", "v1", "v2")
        state = d.get_state("d", "v1")
        out = d.apply_diff(state, diff)
        assert out == {"a": 1, "b": 2}

    def test_apply_removed(self):
        d = DocStateDiff()
        d.store_state("d", "v1", {"a": 1, "b": 2})
        d.store_state("d", "v2", {"a": 1})
        diff = d.compute_diff("d", "v1", "v2")
        state = d.get_state("d", "v1")
        out = d.apply_diff(state, diff)
        assert out == {"a": 1}

    def test_apply_modified(self):
        d = DocStateDiff()
        d.store_state("d", "v1", {"a": 1})
        d.store_state("d", "v2", {"a": 99})
        diff = d.compute_diff("d", "v1", "v2")
        state = d.get_state("d", "v1")
        out = d.apply_diff(state, diff)
        assert out == {"a": 99}

    def test_apply_does_not_mutate_input(self):
        d = DocStateDiff()
        d.store_state("d", "v1", {"a": 1})
        d.store_state("d", "v2", {"a": 2})
        diff = d.compute_diff("d", "v1", "v2")
        state = {"a": 1, "extra": "stay"}
        out = d.apply_diff(state, diff)
        assert state == {"a": 1, "extra": "stay"}
        assert out == {"a": 2, "extra": "stay"}

    def test_apply_empty_diff(self):
        d = DocStateDiff()
        diff = StateDiffResult(doc_id="d", from_version="v1", to_version="v2")
        state = {"a": 1}
        out = d.apply_diff(state, diff)
        assert out == {"a": 1}
        assert out is not state

    def test_apply_remove_missing_field_is_safe(self):
        d = DocStateDiff()
        diff = StateDiffResult(
            doc_id="d",
            from_version="v1",
            to_version="v2",
            changes=[FieldChange("ghost", "removed", "x", None)],
            removed_count=1,
        )
        out = d.apply_diff({"a": 1}, diff)
        assert out == {"a": 1}

    def test_apply_mixed_changes(self):
        d = DocStateDiff()
        d.store_state("d", "v1", {"a": 1, "b": 2, "c": 3})
        d.store_state("d", "v2", {"a": 10, "c": 3, "z": 99})
        diff = d.compute_diff("d", "v1", "v2")
        state = d.get_state("d", "v1")
        out = d.apply_diff(state, diff)
        assert out == {"a": 10, "c": 3, "z": 99}


# ---------------------------------------------------------------------------
# merge_states
# ---------------------------------------------------------------------------


class TestMergeStates:
    def test_merge_disjoint(self):
        d = DocStateDiff()
        out = d.merge_states({"a": 1}, {"b": 2})
        assert out == {"a": 1, "b": 2}

    def test_merge_prefer_b_default(self):
        d = DocStateDiff()
        out = d.merge_states({"a": 1, "x": "from_a"}, {"x": "from_b", "b": 2})
        assert out == {"a": 1, "x": "from_b", "b": 2}

    def test_merge_prefer_a(self):
        d = DocStateDiff()
        out = d.merge_states(
            {"a": 1, "x": "from_a"},
            {"x": "from_b", "b": 2},
            prefer="a",
        )
        assert out == {"a": 1, "x": "from_a", "b": 2}

    def test_merge_invalid_prefer(self):
        d = DocStateDiff()
        with pytest.raises(ValueError):
            d.merge_states({}, {}, prefer="c")

    def test_merge_does_not_mutate_inputs(self):
        d = DocStateDiff()
        a = {"k": [1]}
        b = {"k": [2]}
        out = d.merge_states(a, b)
        out["k"].append(99)
        assert a == {"k": [1]}
        assert b == {"k": [2]}

    def test_merge_empty(self):
        d = DocStateDiff()
        assert d.merge_states({}, {}) == {}

    def test_merge_deep_copy_values(self):
        d = DocStateDiff()
        a = {"k": {"nested": 1}}
        b = {}
        out = d.merge_states(a, b)
        out["k"]["nested"] = 999
        assert a == {"k": {"nested": 1}}


# ---------------------------------------------------------------------------
# clear_all
# ---------------------------------------------------------------------------


class TestClearAll:
    def test_clear_empty(self):
        d = DocStateDiff()
        assert d.clear_all() == 0

    def test_clear_states_and_diffs(self):
        d = DocStateDiff()
        d.store_state("d", "v1", {"a": 1})
        d.store_state("d", "v2", {"a": 2})
        d.compute_diff("d", "v1", "v2")
        n = d.clear_all()
        assert n == 3  # 2 states + 1 diff
        assert d.all_doc_ids() == []
        assert d.get_cached("d", "v1", "v2") is None

    def test_clear_resets_state(self):
        d = DocStateDiff()
        d.store_state("d", "v1", {"a": 1})
        d.clear_all()
        assert d.get_state("d", "v1") is None


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_stats_empty(self):
        s = DocStateDiff().stats()
        assert s.total_diffs == 0
        assert s.total_field_changes == 0
        assert s.unique_docs == 0

    def test_stats_states_only(self):
        d = DocStateDiff()
        d.store_state("d1", "v1", {})
        d.store_state("d2", "v1", {})
        s = d.stats()
        assert s.unique_docs == 2
        assert s.total_diffs == 0
        assert s.total_field_changes == 0

    def test_stats_with_diffs(self):
        d = DocStateDiff()
        d.store_state("d1", "v1", {"a": 1, "b": 2})
        d.store_state("d1", "v2", {"a": 1, "b": 3, "c": 4})  # 1 mod + 1 add
        d.store_state("d2", "v1", {})
        d.store_state("d2", "v2", {"x": 1})  # 1 add
        d.compute_diff("d1", "v1", "v2")
        d.compute_diff("d2", "v1", "v2")
        s = d.stats()
        assert s.total_diffs == 2
        assert s.total_field_changes == 3
        assert s.unique_docs == 2

    def test_stats_after_invalidate(self):
        d = DocStateDiff()
        d.store_state("d1", "v1", {})
        d.store_state("d1", "v2", {"a": 1})
        d.compute_diff("d1", "v1", "v2")
        d.invalidate_cache()
        s = d.stats()
        assert s.total_diffs == 0
        assert s.total_field_changes == 0
        assert s.unique_docs == 1


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_stores(self):
        d = DocStateDiff()

        def worker(i: int) -> None:
            for j in range(20):
                d.store_state(f"doc-{i}", f"v{j}", {"i": i, "j": j})

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        ids = d.all_doc_ids()
        assert len(ids) == 8
        for i in range(8):
            assert f"doc-{i}" in ids
            assert d.versions_for(f"doc-{i}") == sorted(f"v{j}" for j in range(20))

    def test_concurrent_compute(self):
        d = DocStateDiff()
        for i in range(10):
            d.store_state("doc", f"v{i}", {"n": i})

        results: list = []
        lock = threading.Lock()

        def worker(start: int) -> None:
            for i in range(start, start + 3):
                r = d.compute_diff("doc", f"v{i}", f"v{i+1}")
                with lock:
                    results.append(r)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(0, 9, 3)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 9
        for r in results:
            assert r is not None
            assert r.modified_count == 1

    def test_concurrent_mixed_ops(self):
        d = DocStateDiff()

        def writer() -> None:
            for i in range(30):
                d.store_state("doc", f"v{i}", {"i": i})

        def reader() -> None:
            for _ in range(30):
                d.all_doc_ids()
                d.versions_for("doc")
                d.stats()

        ts = [threading.Thread(target=writer) for _ in range(2)] + [
            threading.Thread(target=reader) for _ in range(2)
        ]
        for t in ts:
            t.start()
        for t in ts:
            t.join()

        # Should not crash; final state has all versions
        assert len(d.versions_for("doc")) == 30

    def test_concurrent_clear(self):
        d = DocStateDiff()
        for i in range(20):
            d.store_state("doc", f"v{i}", {"i": i})

        def clearer() -> None:
            d.clear_all()

        def writer() -> None:
            for i in range(20):
                d.store_state("doc2", f"v{i}", {"i": i})

        t1 = threading.Thread(target=clearer)
        t2 = threading.Thread(target=writer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        # Just check no crash and final state is well-formed
        ids = d.all_doc_ids()
        assert isinstance(ids, list)


# ---------------------------------------------------------------------------
# Round-trip
# ---------------------------------------------------------------------------


class TestRoundTrip:
    def test_apply_diff_reconstructs_to_version(self):
        d = DocStateDiff()
        v1 = {"a": 1, "b": 2, "tags": ["x"]}
        v2 = {"a": 10, "c": 3, "tags": ["x", "y"]}
        d.store_state("doc", "v1", v1)
        d.store_state("doc", "v2", v2)
        diff = d.compute_diff("doc", "v1", "v2")
        rebuilt = d.apply_diff(d.get_state("doc", "v1"), diff)
        assert rebuilt == v2

    def test_apply_diff_to_unrelated_state(self):
        d = DocStateDiff()
        d.store_state("doc", "v1", {"a": 1})
        d.store_state("doc", "v2", {"a": 2, "b": 3})
        diff = d.compute_diff("doc", "v1", "v2")
        out = d.apply_diff({"a": 1, "extra": "z"}, diff)
        assert out == {"a": 2, "b": 3, "extra": "z"}
