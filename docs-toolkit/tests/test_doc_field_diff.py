"""Tests for docstoolkit.doc_field_diff."""
from __future__ import annotations

import pytest

from docstoolkit.doc_field_diff import (
    ChangeKind,
    DiffSummary,
    DocFieldDiff,
    FieldChange,
)


# ---------------------------------------------------------------------------
# ChangeKind
# ---------------------------------------------------------------------------

class TestChangeKind:
    def test_added(self):
        assert ChangeKind.ADDED.value == "ADDED"

    def test_removed(self):
        assert ChangeKind.REMOVED.value == "REMOVED"

    def test_changed(self):
        assert ChangeKind.CHANGED.value == "CHANGED"

    def test_unchanged(self):
        assert ChangeKind.UNCHANGED.value == "UNCHANGED"

    def test_type_changed(self):
        assert ChangeKind.TYPE_CHANGED.value == "TYPE_CHANGED"


# ---------------------------------------------------------------------------
# FieldChange
# ---------------------------------------------------------------------------

class TestFieldChange:
    def test_basic_construction(self):
        c = FieldChange(path="a", kind=ChangeKind.ADDED, new_value=1)
        assert c.path == "a"
        assert c.kind == ChangeKind.ADDED
        assert c.new_value == 1
        assert c.old_value is None

    def test_changed_values(self):
        c = FieldChange(path="a", kind=ChangeKind.CHANGED, old_value=1, new_value=2)
        assert c.old_value == 1
        assert c.new_value == 2

    def test_defaults(self):
        c = FieldChange(path="x", kind=ChangeKind.UNCHANGED)
        assert c.old_value is None
        assert c.new_value is None


# ---------------------------------------------------------------------------
# DiffSummary
# ---------------------------------------------------------------------------

class TestDiffSummary:
    def test_defaults(self):
        s = DiffSummary()
        assert s.total_changes == 0
        assert s.added_count == 0
        assert s.removed_count == 0
        assert s.changed_count == 0
        assert s.type_changed_count == 0
        assert s.unchanged_count == 0
        assert s.affected_paths == set()

    def test_custom_values(self):
        s = DiffSummary(total_changes=5, added_count=2, removed_count=1)
        assert s.total_changes == 5
        assert s.added_count == 2
        assert s.removed_count == 1


# ---------------------------------------------------------------------------
# Diff basic
# ---------------------------------------------------------------------------

class TestDiffBasic:
    def test_identical(self):
        d = DocFieldDiff()
        assert d.diff({"a": 1}, {"a": 1}) == []

    def test_added_field(self):
        d = DocFieldDiff()
        changes = d.diff({"a": 1}, {"a": 1, "b": 2})
        assert len(changes) == 1
        assert changes[0].kind == ChangeKind.ADDED
        assert changes[0].path == "b"
        assert changes[0].new_value == 2

    def test_removed_field(self):
        d = DocFieldDiff()
        changes = d.diff({"a": 1, "b": 2}, {"a": 1})
        assert len(changes) == 1
        assert changes[0].kind == ChangeKind.REMOVED
        assert changes[0].path == "b"
        assert changes[0].old_value == 2

    def test_changed_field(self):
        d = DocFieldDiff()
        changes = d.diff({"a": 1}, {"a": 2})
        assert len(changes) == 1
        assert changes[0].kind == ChangeKind.CHANGED
        assert changes[0].old_value == 1
        assert changes[0].new_value == 2

    def test_multiple_changes(self):
        d = DocFieldDiff()
        changes = d.diff({"a": 1, "b": 2}, {"a": 1, "b": 3, "c": 4})
        kinds = {c.kind for c in changes}
        assert ChangeKind.CHANGED in kinds
        assert ChangeKind.ADDED in kinds

    def test_empty_to_empty(self):
        d = DocFieldDiff()
        assert d.diff({}, {}) == []

    def test_empty_to_nonempty(self):
        d = DocFieldDiff()
        changes = d.diff({}, {"a": 1})
        assert len(changes) == 1
        assert changes[0].kind == ChangeKind.ADDED


# ---------------------------------------------------------------------------
# Diff nested
# ---------------------------------------------------------------------------

class TestDiffNestedDict:
    def test_nested_added(self):
        d = DocFieldDiff()
        changes = d.diff(
            {"meta": {"a": 1}},
            {"meta": {"a": 1, "b": 2}},
        )
        assert len(changes) == 1
        assert changes[0].path == "meta.b"
        assert changes[0].kind == ChangeKind.ADDED

    def test_nested_changed(self):
        d = DocFieldDiff()
        changes = d.diff(
            {"meta": {"author": "x"}},
            {"meta": {"author": "y"}},
        )
        assert len(changes) == 1
        assert changes[0].path == "meta.author"
        assert changes[0].kind == ChangeKind.CHANGED

    def test_nested_removed(self):
        d = DocFieldDiff()
        changes = d.diff(
            {"meta": {"a": 1, "b": 2}},
            {"meta": {"a": 1}},
        )
        assert len(changes) == 1
        assert changes[0].path == "meta.b"
        assert changes[0].kind == ChangeKind.REMOVED

    def test_deeply_nested(self):
        d = DocFieldDiff()
        changes = d.diff(
            {"a": {"b": {"c": 1}}},
            {"a": {"b": {"c": 2}}},
        )
        assert len(changes) == 1
        assert changes[0].path == "a.b.c"

    def test_mix_of_changes(self):
        d = DocFieldDiff()
        changes = d.diff(
            {"meta": {"a": 1, "b": 2}},
            {"meta": {"a": 5, "c": 3}},
        )
        # b removed, a changed, c added
        assert len(changes) == 3
        kinds = {c.kind for c in changes}
        assert ChangeKind.ADDED in kinds
        assert ChangeKind.REMOVED in kinds
        assert ChangeKind.CHANGED in kinds


# ---------------------------------------------------------------------------
# Diff lists
# ---------------------------------------------------------------------------

class TestDiffLists:
    def test_identical_lists(self):
        d = DocFieldDiff()
        assert d.diff({"x": [1, 2, 3]}, {"x": [1, 2, 3]}) == []

    def test_list_value_changed(self):
        d = DocFieldDiff()
        changes = d.diff({"x": [1, 2, 3]}, {"x": [1, 9, 3]})
        assert len(changes) == 1
        assert changes[0].path == "x[1]"
        assert changes[0].kind == ChangeKind.CHANGED

    def test_list_extended(self):
        d = DocFieldDiff()
        changes = d.diff({"x": [1, 2]}, {"x": [1, 2, 3]})
        assert len(changes) == 1
        assert changes[0].path == "x[2]"
        assert changes[0].kind == ChangeKind.ADDED
        assert changes[0].new_value == 3

    def test_list_shortened(self):
        d = DocFieldDiff()
        changes = d.diff({"x": [1, 2, 3]}, {"x": [1, 2]})
        assert len(changes) == 1
        assert changes[0].path == "x[2]"
        assert changes[0].kind == ChangeKind.REMOVED
        assert changes[0].old_value == 3

    def test_list_of_dicts(self):
        d = DocFieldDiff()
        changes = d.diff(
            {"items": [{"id": 1}, {"id": 2}]},
            {"items": [{"id": 1}, {"id": 3}]},
        )
        assert len(changes) == 1
        assert changes[0].path == "items[1].id"
        assert changes[0].kind == ChangeKind.CHANGED


# ---------------------------------------------------------------------------
# Type change
# ---------------------------------------------------------------------------

class TestDiffTypeChange:
    def test_int_to_string(self):
        d = DocFieldDiff()
        changes = d.diff({"a": 1}, {"a": "1"})
        assert len(changes) == 1
        assert changes[0].kind == ChangeKind.TYPE_CHANGED

    def test_dict_to_list(self):
        d = DocFieldDiff()
        changes = d.diff({"a": {"x": 1}}, {"a": [1, 2]})
        assert len(changes) == 1
        assert changes[0].kind == ChangeKind.TYPE_CHANGED

    def test_string_to_none(self):
        d = DocFieldDiff()
        changes = d.diff({"a": "x"}, {"a": None})
        assert len(changes) == 1
        assert changes[0].kind == ChangeKind.TYPE_CHANGED

    def test_bool_to_int_is_type_change(self):
        d = DocFieldDiff()
        # bool is a subclass of int but type() differs
        changes = d.diff({"a": True}, {"a": 1})
        assert len(changes) == 1
        assert changes[0].kind == ChangeKind.TYPE_CHANGED


# ---------------------------------------------------------------------------
# Include unchanged
# ---------------------------------------------------------------------------

class TestDiffIncludeUnchanged:
    def test_default_excludes_unchanged(self):
        d = DocFieldDiff()
        changes = d.diff({"a": 1, "b": 2}, {"a": 1, "b": 99})
        assert all(c.kind != ChangeKind.UNCHANGED for c in changes)

    def test_with_unchanged(self):
        d = DocFieldDiff()
        changes = d.diff({"a": 1, "b": 2}, {"a": 1, "b": 99}, include_unchanged=True)
        unchanged = [c for c in changes if c.kind == ChangeKind.UNCHANGED]
        assert len(unchanged) == 1
        assert unchanged[0].path == "a"


# ---------------------------------------------------------------------------
# diff_value
# ---------------------------------------------------------------------------

class TestDiffValue:
    def test_two_primitives_equal(self):
        d = DocFieldDiff()
        changes = d.diff_value(1, 1, "x")
        assert len(changes) == 1
        assert changes[0].kind == ChangeKind.UNCHANGED

    def test_two_primitives_different(self):
        d = DocFieldDiff()
        changes = d.diff_value(1, 2, "x")
        assert len(changes) == 1
        assert changes[0].kind == ChangeKind.CHANGED

    def test_two_lists(self):
        d = DocFieldDiff()
        changes = d.diff_value([1, 2], [1, 3], "lst")
        # one unchanged + one changed
        assert any(c.path == "lst[1]" and c.kind == ChangeKind.CHANGED for c in changes)

    def test_empty_path(self):
        d = DocFieldDiff()
        changes = d.diff_value({"a": 1}, {"a": 2}, "")
        assert changes[0].path == "a"


# ---------------------------------------------------------------------------
# is_equal
# ---------------------------------------------------------------------------

class TestIsEqual:
    def test_equal_dicts(self):
        d = DocFieldDiff()
        assert d.is_equal({"a": 1}, {"a": 1}) is True

    def test_not_equal(self):
        d = DocFieldDiff()
        assert d.is_equal({"a": 1}, {"a": 2}) is False

    def test_shallow_equal(self):
        d = DocFieldDiff()
        assert d.is_equal({"a": 1}, {"a": 1}, deep=False) is True

    def test_shallow_not_equal(self):
        d = DocFieldDiff()
        assert d.is_equal({"a": 1}, {"a": 2}, deep=False) is False

    def test_deep_nested_equal(self):
        d = DocFieldDiff()
        assert d.is_equal({"a": {"b": [1, 2]}}, {"a": {"b": [1, 2]}}) is True

    def test_deep_nested_not_equal(self):
        d = DocFieldDiff()
        assert d.is_equal({"a": {"b": [1, 2]}}, {"a": {"b": [1, 3]}}) is False


# ---------------------------------------------------------------------------
# summary
# ---------------------------------------------------------------------------

class TestSummary:
    def test_empty_summary(self):
        d = DocFieldDiff()
        s = d.summary({"a": 1}, {"a": 1})
        assert s.total_changes == 0
        assert s.unchanged_count == 1

    def test_added(self):
        d = DocFieldDiff()
        s = d.summary({}, {"a": 1})
        assert s.added_count == 1
        assert s.total_changes == 1
        assert "a" in s.affected_paths

    def test_removed(self):
        d = DocFieldDiff()
        s = d.summary({"a": 1}, {})
        assert s.removed_count == 1

    def test_changed(self):
        d = DocFieldDiff()
        s = d.summary({"a": 1}, {"a": 2})
        assert s.changed_count == 1

    def test_type_changed(self):
        d = DocFieldDiff()
        s = d.summary({"a": 1}, {"a": "1"})
        assert s.type_changed_count == 1

    def test_combined(self):
        d = DocFieldDiff()
        s = d.summary(
            {"a": 1, "b": 2, "c": 3},
            {"a": 1, "b": 99, "d": 4},
        )
        assert s.changed_count == 1  # b
        assert s.added_count == 1  # d
        assert s.removed_count == 1  # c
        assert s.unchanged_count == 1  # a
        assert s.total_changes == 3


# ---------------------------------------------------------------------------
# added_fields
# ---------------------------------------------------------------------------

class TestAddedFields:
    def test_none_added(self):
        d = DocFieldDiff()
        assert d.added_fields({"a": 1}, {"a": 2}) == []

    def test_one_added(self):
        d = DocFieldDiff()
        assert d.added_fields({}, {"a": 1}) == ["a"]

    def test_nested_added(self):
        d = DocFieldDiff()
        assert d.added_fields({"m": {}}, {"m": {"x": 1}}) == ["m.x"]


# ---------------------------------------------------------------------------
# removed_fields
# ---------------------------------------------------------------------------

class TestRemovedFields:
    def test_none_removed(self):
        d = DocFieldDiff()
        assert d.removed_fields({"a": 1}, {"a": 1}) == []

    def test_one_removed(self):
        d = DocFieldDiff()
        assert d.removed_fields({"a": 1}, {}) == ["a"]

    def test_nested_removed(self):
        d = DocFieldDiff()
        assert d.removed_fields({"m": {"x": 1}}, {"m": {}}) == ["m.x"]


# ---------------------------------------------------------------------------
# changed_fields
# ---------------------------------------------------------------------------

class TestChangedFields:
    def test_none_changed(self):
        d = DocFieldDiff()
        assert d.changed_fields({"a": 1}, {"a": 1}) == []

    def test_one_changed(self):
        d = DocFieldDiff()
        assert d.changed_fields({"a": 1}, {"a": 2}) == ["a"]

    def test_type_change_included(self):
        d = DocFieldDiff()
        # TYPE_CHANGED counts as a change in changed_fields
        result = d.changed_fields({"a": 1}, {"a": "1"})
        assert result == ["a"]


# ---------------------------------------------------------------------------
# unchanged_fields
# ---------------------------------------------------------------------------

class TestUnchangedFields:
    def test_all_unchanged(self):
        d = DocFieldDiff()
        assert d.unchanged_fields({"a": 1, "b": 2}, {"a": 1, "b": 2}) == ["a", "b"]

    def test_none_unchanged(self):
        d = DocFieldDiff()
        assert d.unchanged_fields({"a": 1}, {"a": 2}) == []


# ---------------------------------------------------------------------------
# get_value
# ---------------------------------------------------------------------------

class TestGetValue:
    def test_top_level(self):
        d = DocFieldDiff()
        assert d.get_value({"a": 1}, "a") == 1

    def test_nested(self):
        d = DocFieldDiff()
        assert d.get_value({"a": {"b": 2}}, "a.b") == 2

    def test_default_missing(self):
        d = DocFieldDiff()
        assert d.get_value({"a": 1}, "b", default="x") == "x"

    def test_list_index(self):
        d = DocFieldDiff()
        assert d.get_value({"a": [10, 20]}, "a[1]") == 20

    def test_nested_list_dict(self):
        d = DocFieldDiff()
        assert d.get_value({"a": [{"x": 1}]}, "a[0].x") == 1

    def test_missing_default_none(self):
        d = DocFieldDiff()
        assert d.get_value({"a": 1}, "missing") is None


# ---------------------------------------------------------------------------
# set_value
# ---------------------------------------------------------------------------

class TestSetValue:
    def test_top_level(self):
        d = DocFieldDiff()
        data = {}
        assert d.set_value(data, "a", 1) is True
        assert data["a"] == 1

    def test_nested_creates_intermediate(self):
        d = DocFieldDiff()
        data = {}
        d.set_value(data, "a.b.c", 42)
        assert data == {"a": {"b": {"c": 42}}}

    def test_list_index(self):
        d = DocFieldDiff()
        data = {"x": [1, 2]}
        d.set_value(data, "x[0]", 99)
        assert data["x"][0] == 99

    def test_extend_list(self):
        d = DocFieldDiff()
        data = {"x": [1]}
        d.set_value(data, "x[3]", 9)
        assert data["x"][3] == 9


# ---------------------------------------------------------------------------
# apply_patch
# ---------------------------------------------------------------------------

class TestApplyPatch:
    def test_added(self):
        d = DocFieldDiff()
        changes = [FieldChange(path="b", kind=ChangeKind.ADDED, new_value=2)]
        result = d.apply_patch({"a": 1}, changes)
        assert result == {"a": 1, "b": 2}

    def test_removed(self):
        d = DocFieldDiff()
        changes = [FieldChange(path="b", kind=ChangeKind.REMOVED, old_value=2)]
        result = d.apply_patch({"a": 1, "b": 2}, changes)
        assert result == {"a": 1}

    def test_changed(self):
        d = DocFieldDiff()
        changes = [FieldChange(path="a", kind=ChangeKind.CHANGED, old_value=1, new_value=99)]
        result = d.apply_patch({"a": 1}, changes)
        assert result == {"a": 99}

    def test_apply_diff_roundtrip(self):
        d = DocFieldDiff()
        old = {"a": 1, "b": [1, 2], "c": {"x": 10}}
        new = {"a": 2, "b": [1, 2, 3], "c": {"x": 11}}
        changes = d.diff(old, new)
        result = d.apply_patch(old, changes)
        assert result == new

    def test_apply_does_not_mutate(self):
        d = DocFieldDiff()
        old = {"a": 1}
        changes = [FieldChange(path="a", kind=ChangeKind.CHANGED, old_value=1, new_value=2)]
        d.apply_patch(old, changes)
        assert old == {"a": 1}

    def test_unchanged_skipped(self):
        d = DocFieldDiff()
        changes = [FieldChange(path="a", kind=ChangeKind.UNCHANGED, old_value=1, new_value=1)]
        result = d.apply_patch({"a": 1}, changes)
        assert result == {"a": 1}


# ---------------------------------------------------------------------------
# extract_paths
# ---------------------------------------------------------------------------

class TestExtractPaths:
    def test_flat(self):
        d = DocFieldDiff()
        paths = d.extract_paths({"a": 1, "b": 2})
        assert set(paths) == {"a", "b"}

    def test_nested(self):
        d = DocFieldDiff()
        paths = d.extract_paths({"a": {"b": 1}})
        assert paths == ["a.b"]

    def test_with_list(self):
        d = DocFieldDiff()
        paths = d.extract_paths({"x": [1, 2]})
        assert set(paths) == {"x[0]", "x[1]"}

    def test_complex(self):
        d = DocFieldDiff()
        paths = d.extract_paths({"a": {"b": [{"c": 1}]}})
        assert paths == ["a.b[0].c"]

    def test_empty(self):
        d = DocFieldDiff()
        assert d.extract_paths({}) == []


# ---------------------------------------------------------------------------
# compact
# ---------------------------------------------------------------------------

class TestCompact:
    def test_removes_unchanged(self):
        d = DocFieldDiff()
        changes = [
            FieldChange(path="a", kind=ChangeKind.UNCHANGED),
            FieldChange(path="b", kind=ChangeKind.ADDED, new_value=1),
        ]
        result = d.compact(changes)
        assert len(result) == 1
        assert result[0].path == "b"

    def test_no_unchanged(self):
        d = DocFieldDiff()
        changes = [
            FieldChange(path="a", kind=ChangeKind.ADDED),
            FieldChange(path="b", kind=ChangeKind.REMOVED),
        ]
        result = d.compact(changes)
        assert len(result) == 2

    def test_empty(self):
        d = DocFieldDiff()
        assert d.compact([]) == []


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_none_to_none(self):
        d = DocFieldDiff()
        changes = d.diff({"a": None}, {"a": None})
        assert changes == []

    def test_value_to_none_is_type_change(self):
        d = DocFieldDiff()
        changes = d.diff({"a": 1}, {"a": None})
        assert len(changes) == 1
        assert changes[0].kind == ChangeKind.TYPE_CHANGED

    def test_none_to_value_is_type_change(self):
        d = DocFieldDiff()
        changes = d.diff({"a": None}, {"a": 1})
        assert changes[0].kind == ChangeKind.TYPE_CHANGED

    def test_empty_dict_value_unchanged(self):
        d = DocFieldDiff()
        changes = d.diff({"a": {}}, {"a": {}})
        assert changes == []

    def test_empty_list_unchanged(self):
        d = DocFieldDiff()
        changes = d.diff({"a": []}, {"a": []})
        assert changes == []

    def test_nested_full_replace_same_type(self):
        d = DocFieldDiff()
        changes = d.diff(
            {"a": {"x": 1, "y": 2}},
            {"a": {"z": 99}},
        )
        kinds = {c.kind for c in changes}
        assert ChangeKind.REMOVED in kinds
        assert ChangeKind.ADDED in kinds

    def test_get_value_empty_path_returns_data(self):
        d = DocFieldDiff()
        assert d.get_value({"a": 1}, "") == {"a": 1}

    def test_set_value_empty_path_returns_false(self):
        d = DocFieldDiff()
        assert d.set_value({}, "", 1) is False
