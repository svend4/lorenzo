"""Tests for the schema_diff module (E102).

Covers:
- Empty dicts
- Single added/removed/changed/type-changed field
- Nested and deeply-nested diffs
- Multiple simultaneous changes
- DiffResult properties and summary()
- has_changes flag
- ignore_paths
- treat_list_as_scalar
- is_compatible
- patch()
- List comparison (default mode)
- None values
- Boolean vs integer type distinction
"""
from __future__ import annotations

import pytest

from docstoolkit.schema_diff import (
    ChangeType,
    FieldChange,
    DiffResult,
    SchemaDiffer,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _differ(**kwargs) -> SchemaDiffer:
    return SchemaDiffer(**kwargs)


def _paths(changes) -> list[str]:
    return [c.path for c in changes]


# ===========================================================================
# ChangeType
# ===========================================================================

class TestChangeType:
    def test_values_are_strings(self):
        assert ChangeType.ADDED == "added"
        assert ChangeType.REMOVED == "removed"
        assert ChangeType.CHANGED == "changed"
        assert ChangeType.TYPE_CHANGED == "type_changed"

    def test_is_str_subclass(self):
        assert isinstance(ChangeType.ADDED, str)


# ===========================================================================
# FieldChange
# ===========================================================================

class TestFieldChange:
    def test_defaults(self):
        fc = FieldChange(path="x", change_type=ChangeType.ADDED)
        assert fc.old_value is None
        assert fc.new_value is None
        assert fc.old_type == ""
        assert fc.new_type == ""

    def test_repr_contains_path(self):
        fc = FieldChange(path="a.b", change_type=ChangeType.CHANGED, old_value=1, new_value=2)
        assert "a.b" in repr(fc)
        assert "changed" in repr(fc)


# ===========================================================================
# DiffResult — properties
# ===========================================================================

class TestDiffResultProperties:
    def _make_result(self) -> DiffResult:
        return DiffResult(changes=[
            FieldChange("a", ChangeType.ADDED, new_value=1),
            FieldChange("b", ChangeType.REMOVED, old_value=2),
            FieldChange("c", ChangeType.CHANGED, old_value=3, new_value=4),
            FieldChange("d", ChangeType.TYPE_CHANGED, old_value=5, new_value="5",
                        old_type="int", new_type="str"),
        ])

    def test_has_changes_true(self):
        assert self._make_result().has_changes is True

    def test_has_changes_false(self):
        assert DiffResult().has_changes is False

    def test_added_filter(self):
        r = self._make_result()
        assert len(r.added) == 1
        assert r.added[0].path == "a"

    def test_removed_filter(self):
        r = self._make_result()
        assert len(r.removed) == 1
        assert r.removed[0].path == "b"

    def test_changed_filter(self):
        r = self._make_result()
        assert len(r.changed) == 1
        assert r.changed[0].path == "c"

    def test_type_changed_filter(self):
        r = self._make_result()
        assert len(r.type_changed) == 1
        assert r.type_changed[0].path == "d"

    def test_summary_counts(self):
        s = self._make_result().summary()
        assert s["added"] == 1
        assert s["removed"] == 1
        assert s["changed"] == 1
        assert s["type_changed"] == 1
        assert s["total"] == 4

    def test_summary_empty(self):
        s = DiffResult().summary()
        assert s == {"added": 0, "removed": 0, "changed": 0, "type_changed": 0, "total": 0}

    def test_summary_keys(self):
        s = DiffResult().summary()
        assert set(s.keys()) == {"added", "removed", "changed", "type_changed", "total"}


# ===========================================================================
# SchemaDiffer.diff — basic cases
# ===========================================================================

class TestDiffEmpty:
    def test_both_empty(self):
        d = _differ()
        result = d.diff({}, {})
        assert not result.has_changes
        assert result.changes == []

    def test_identical_flat(self):
        doc = {"a": 1, "b": "hello"}
        result = _differ().diff(doc, doc)
        assert not result.has_changes

    def test_identical_nested(self):
        doc = {"a": {"b": {"c": 42}}}
        result = _differ().diff(doc, doc)
        assert not result.has_changes


class TestDiffAdded:
    def test_single_added_field(self):
        result = _differ().diff({}, {"x": 10})
        assert len(result.changes) == 1
        fc = result.changes[0]
        assert fc.path == "x"
        assert fc.change_type == ChangeType.ADDED
        assert fc.old_value is None
        assert fc.new_value == 10

    def test_added_stores_new_value(self):
        result = _differ().diff({"a": 1}, {"a": 1, "b": [1, 2, 3]})
        assert len(result.added) == 1
        assert result.added[0].new_value == [1, 2, 3]

    def test_multiple_added(self):
        result = _differ().diff({}, {"x": 1, "y": 2, "z": 3})
        assert len(result.added) == 3
        assert set(_paths(result.added)) == {"x", "y", "z"}


class TestDiffRemoved:
    def test_single_removed_field(self):
        result = _differ().diff({"x": 10}, {})
        assert len(result.changes) == 1
        fc = result.changes[0]
        assert fc.path == "x"
        assert fc.change_type == ChangeType.REMOVED
        assert fc.old_value == 10
        assert fc.new_value is None

    def test_removed_stores_old_value(self):
        result = _differ().diff({"a": 1, "b": "gone"}, {"a": 1})
        assert len(result.removed) == 1
        assert result.removed[0].old_value == "gone"


class TestDiffChanged:
    def test_single_changed_field(self):
        result = _differ().diff({"x": 1}, {"x": 2})
        assert len(result.changes) == 1
        fc = result.changes[0]
        assert fc.path == "x"
        assert fc.change_type == ChangeType.CHANGED
        assert fc.old_value == 1
        assert fc.new_value == 2

    def test_string_changed(self):
        result = _differ().diff({"name": "Alice"}, {"name": "Bob"})
        assert len(result.changed) == 1
        assert result.changed[0].old_value == "Alice"
        assert result.changed[0].new_value == "Bob"

    def test_unchanged_value_not_reported(self):
        result = _differ().diff({"a": 42, "b": "same"}, {"a": 42, "b": "same"})
        assert not result.has_changes


class TestDiffTypeChanged:
    def test_int_to_str(self):
        result = _differ().diff({"x": 1}, {"x": "1"})
        assert len(result.type_changed) == 1
        fc = result.type_changed[0]
        assert fc.old_type == "int"
        assert fc.new_type == "str"
        assert fc.old_value == 1
        assert fc.new_value == "1"

    def test_str_to_list(self):
        result = _differ().diff({"x": "hi"}, {"x": [1, 2]})
        assert len(result.type_changed) == 1
        fc = result.type_changed[0]
        assert fc.old_type == "str"
        assert fc.new_type == "list"

    def test_type_changed_old_type_field(self):
        result = _differ().diff({"v": 3.14}, {"v": 3})
        fc = result.type_changed[0]
        assert fc.old_type == "float"
        assert fc.new_type == "int"


# ===========================================================================
# Nested and deep nesting
# ===========================================================================

class TestDiffNested:
    def test_nested_changed(self):
        old = {"user": {"address": {"city": "Moscow"}}}
        new = {"user": {"address": {"city": "Berlin"}}}
        result = _differ().diff(old, new)
        assert len(result.changes) == 1
        fc = result.changes[0]
        assert fc.path == "user.address.city"
        assert fc.change_type == ChangeType.CHANGED
        assert fc.old_value == "Moscow"
        assert fc.new_value == "Berlin"

    def test_nested_added(self):
        old = {"user": {"name": "Alice"}}
        new = {"user": {"name": "Alice", "age": 30}}
        result = _differ().diff(old, new)
        assert len(result.added) == 1
        assert result.added[0].path == "user.age"

    def test_nested_removed(self):
        old = {"user": {"name": "Alice", "age": 30}}
        new = {"user": {"name": "Alice"}}
        result = _differ().diff(old, new)
        assert len(result.removed) == 1
        assert result.removed[0].path == "user.age"

    def test_deeply_nested_added(self):
        old = {"a": {"b": {"c": {}}}}
        new = {"a": {"b": {"c": {"d": "value"}}}}
        result = _differ().diff(old, new)
        assert len(result.added) == 1
        assert result.added[0].path == "a.b.c.d"

    def test_deeply_nested_four_levels(self):
        old = {"x": {"y": {"z": {"w": 1}}}}
        new = {"x": {"y": {"z": {"w": 2}}}}
        result = _differ().diff(old, new)
        assert len(result.changed) == 1
        assert result.changed[0].path == "x.y.z.w"

    def test_mixed_add_remove_change(self):
        old = {"a": 1, "b": 2, "c": 3}
        new = {"a": 99, "c": 3, "d": 4}
        result = _differ().diff(old, new)
        assert len(result.added) == 1
        assert result.added[0].path == "d"
        assert len(result.removed) == 1
        assert result.removed[0].path == "b"
        assert len(result.changed) == 1
        assert result.changed[0].path == "a"

    def test_nested_dict_replaced_by_scalar(self):
        old = {"config": {"debug": True}}
        new = {"config": "disabled"}
        result = _differ().diff(old, new)
        assert len(result.type_changed) == 1
        assert result.type_changed[0].path == "config"

    def test_scalar_replaced_by_dict(self):
        old = {"config": "disabled"}
        new = {"config": {"debug": True}}
        result = _differ().diff(old, new)
        assert len(result.type_changed) == 1
        assert result.type_changed[0].path == "config"


# ===========================================================================
# ignore_paths
# ===========================================================================

class TestIgnorePaths:
    def test_ignore_top_level(self):
        result = _differ(ignore_paths={"secret"}).diff(
            {"secret": "old", "name": "Alice"},
            {"secret": "new", "name": "Alice"},
        )
        assert not result.has_changes

    def test_ignore_nested(self):
        old = {"user": {"name": "Alice", "token": "abc"}}
        new = {"user": {"name": "Alice", "token": "xyz"}}
        result = _differ(ignore_paths={"user.token"}).diff(old, new)
        assert not result.has_changes

    def test_ignore_does_not_affect_other_fields(self):
        old = {"a": 1, "b": 2}
        new = {"a": 99, "b": 2}
        result = _differ(ignore_paths={"b"}).diff(old, new)
        assert len(result.changed) == 1
        assert result.changed[0].path == "a"

    def test_ignore_added_field(self):
        result = _differ(ignore_paths={"new_field"}).diff(
            {"a": 1},
            {"a": 1, "new_field": "ignored"},
        )
        assert not result.has_changes

    def test_ignore_removed_field(self):
        result = _differ(ignore_paths={"gone"}).diff(
            {"a": 1, "gone": "bye"},
            {"a": 1},
        )
        assert not result.has_changes

    def test_ignore_multiple_paths(self):
        old = {"a": 1, "b": 2, "c": 3}
        new = {"a": 99, "b": 99, "c": 3}
        result = _differ(ignore_paths={"a", "b"}).diff(old, new)
        assert not result.has_changes

    def test_ignore_empty_set(self):
        result = _differ(ignore_paths=set()).diff({"a": 1}, {"a": 2})
        assert len(result.changed) == 1


# ===========================================================================
# treat_list_as_scalar
# ===========================================================================

class TestListComparison:
    def test_list_changed_default(self):
        result = _differ().diff({"tags": [1, 2]}, {"tags": [1, 2, 3]})
        assert len(result.changed) == 1
        assert result.changed[0].path == "tags"

    def test_list_unchanged_default(self):
        result = _differ().diff({"tags": [1, 2]}, {"tags": [1, 2]})
        assert not result.has_changes

    def test_list_treat_as_scalar_equal(self):
        result = _differ(treat_list_as_scalar=True).diff(
            {"tags": [1, 2]}, {"tags": [1, 2]}
        )
        assert not result.has_changes

    def test_list_treat_as_scalar_changed(self):
        result = _differ(treat_list_as_scalar=True).diff(
            {"tags": [1, 2]}, {"tags": [3, 4]}
        )
        assert len(result.changed) == 1
        assert result.changed[0].change_type == ChangeType.CHANGED

    def test_list_treat_as_scalar_different(self):
        # treat_list_as_scalar=False is default: lists compared by equality
        result = _differ(treat_list_as_scalar=False).diff(
            {"x": ["a"]}, {"x": ["b"]}
        )
        assert len(result.changed) == 1

    def test_list_type_change(self):
        # list → str is type changed
        result = _differ().diff({"x": [1, 2]}, {"x": "list"})
        assert len(result.type_changed) == 1
        assert result.type_changed[0].old_type == "list"
        assert result.type_changed[0].new_type == "str"


# ===========================================================================
# None values
# ===========================================================================

class TestNoneValues:
    def test_none_unchanged(self):
        result = _differ().diff({"x": None}, {"x": None})
        assert not result.has_changes

    def test_none_to_value(self):
        result = _differ().diff({"x": None}, {"x": 42})
        assert len(result.type_changed) == 1
        fc = result.type_changed[0]
        assert fc.old_type == "NoneType"
        assert fc.new_type == "int"

    def test_value_to_none(self):
        result = _differ().diff({"x": "hello"}, {"x": None})
        assert len(result.type_changed) == 1
        fc = result.type_changed[0]
        assert fc.old_type == "str"
        assert fc.new_type == "NoneType"

    def test_added_with_none_value(self):
        result = _differ().diff({}, {"key": None})
        assert len(result.added) == 1
        assert result.added[0].new_value is None

    def test_removed_with_none_value(self):
        result = _differ().diff({"key": None}, {})
        assert len(result.removed) == 1
        assert result.removed[0].old_value is None


# ===========================================================================
# Boolean vs integer type distinction
# ===========================================================================

class TestBoolVsInt:
    def test_bool_true_is_not_int_1(self):
        # Python: bool is subclass of int, but we want type distinction
        result = _differ().diff({"flag": True}, {"flag": 1})
        assert len(result.type_changed) == 1
        fc = result.type_changed[0]
        assert fc.old_type == "bool"
        assert fc.new_type == "int"

    def test_bool_false_is_not_int_0(self):
        result = _differ().diff({"flag": False}, {"flag": 0})
        assert len(result.type_changed) == 1
        fc = result.type_changed[0]
        assert fc.old_type == "bool"
        assert fc.new_type == "int"

    def test_bool_true_unchanged(self):
        result = _differ().diff({"flag": True}, {"flag": True})
        assert not result.has_changes

    def test_bool_changed(self):
        result = _differ().diff({"flag": True}, {"flag": False})
        assert len(result.changed) == 1
        fc = result.changed[0]
        assert fc.old_value is True
        assert fc.new_value is False

    def test_int_to_bool(self):
        result = _differ().diff({"v": 1}, {"v": True})
        assert len(result.type_changed) == 1
        assert result.type_changed[0].old_type == "int"
        assert result.type_changed[0].new_type == "bool"


# ===========================================================================
# is_compatible
# ===========================================================================

class TestIsCompatible:
    def test_identical_schemas_compatible(self):
        schema = {"a": 1, "b": "x"}
        assert _differ().is_compatible(schema, schema) is True

    def test_added_field_is_compatible(self):
        old = {"a": 1}
        new = {"a": 1, "b": 2}
        assert _differ().is_compatible(old, new) is True

    def test_changed_field_is_compatible(self):
        old = {"a": 1}
        new = {"a": 99}
        assert _differ().is_compatible(old, new) is True

    def test_removed_field_is_not_compatible(self):
        old = {"a": 1, "b": 2}
        new = {"a": 1}
        assert _differ().is_compatible(old, new) is False

    def test_type_changed_is_not_compatible(self):
        old = {"a": 1}
        new = {"a": "one"}
        assert _differ().is_compatible(old, new) is False

    def test_nested_removed_is_not_compatible(self):
        old = {"user": {"name": "Alice", "age": 30}}
        new = {"user": {"name": "Alice"}}
        assert _differ().is_compatible(old, new) is False

    def test_nested_added_is_compatible(self):
        old = {"user": {"name": "Alice"}}
        new = {"user": {"name": "Alice", "email": "a@b.com"}}
        assert _differ().is_compatible(old, new) is True

    def test_empty_old_is_compatible(self):
        assert _differ().is_compatible({}, {"a": 1, "b": 2}) is True

    def test_empty_new_is_not_compatible(self):
        assert _differ().is_compatible({"a": 1}, {}) is False


# ===========================================================================
# patch()
# ===========================================================================

class TestPatch:
    def test_patch_added(self):
        diff = DiffResult(changes=[
            FieldChange("b", ChangeType.ADDED, new_value=2),
        ])
        result = _differ().patch({"a": 1}, diff)
        assert result == {"a": 1, "b": 2}

    def test_patch_removed(self):
        diff = DiffResult(changes=[
            FieldChange("b", ChangeType.REMOVED, old_value=2),
        ])
        result = _differ().patch({"a": 1, "b": 2}, diff)
        assert result == {"a": 1}

    def test_patch_changed(self):
        diff = DiffResult(changes=[
            FieldChange("a", ChangeType.CHANGED, old_value=1, new_value=99),
        ])
        result = _differ().patch({"a": 1, "b": 2}, diff)
        assert result == {"a": 99, "b": 2}

    def test_patch_type_changed(self):
        diff = DiffResult(changes=[
            FieldChange("a", ChangeType.TYPE_CHANGED, old_value=1, new_value="one",
                        old_type="int", new_type="str"),
        ])
        result = _differ().patch({"a": 1}, diff)
        assert result == {"a": "one"}

    def test_patch_does_not_modify_base(self):
        base = {"a": 1, "b": 2}
        diff = DiffResult(changes=[
            FieldChange("b", ChangeType.CHANGED, old_value=2, new_value=99),
        ])
        _differ().patch(base, diff)
        assert base == {"a": 1, "b": 2}

    def test_patch_nested_added(self):
        diff = DiffResult(changes=[
            FieldChange("user.email", ChangeType.ADDED, new_value="a@b.com"),
        ])
        base = {"user": {"name": "Alice"}}
        result = _differ().patch(base, diff)
        assert result["user"]["email"] == "a@b.com"
        assert result["user"]["name"] == "Alice"

    def test_patch_nested_removed(self):
        diff = DiffResult(changes=[
            FieldChange("user.age", ChangeType.REMOVED, old_value=30),
        ])
        base = {"user": {"name": "Alice", "age": 30}}
        result = _differ().patch(base, diff)
        assert "age" not in result["user"]
        assert result["user"]["name"] == "Alice"

    def test_patch_nested_changed(self):
        diff = DiffResult(changes=[
            FieldChange("user.address.city", ChangeType.CHANGED,
                        old_value="Moscow", new_value="Berlin"),
        ])
        base = {"user": {"address": {"city": "Moscow", "zip": "101000"}}}
        result = _differ().patch(base, diff)
        assert result["user"]["address"]["city"] == "Berlin"
        assert result["user"]["address"]["zip"] == "101000"

    def test_patch_empty_changes(self):
        base = {"a": 1}
        result = _differ().patch(base, DiffResult())
        assert result == {"a": 1}

    def test_patch_roundtrip(self):
        """patch(old, diff(old, new)) should equal new for simple cases."""
        old = {"a": 1, "b": 2}
        new = {"a": 99, "c": 3}
        differ = _differ()
        diff = differ.diff(old, new)
        patched = differ.patch(old, diff)
        # "b" should be removed, "a" changed, "c" added
        assert patched == {"a": 99, "c": 3}

    def test_patch_deeply_nested_set(self):
        diff = DiffResult(changes=[
            FieldChange("a.b.c.d", ChangeType.ADDED, new_value="deep"),
        ])
        result = _differ().patch({}, diff)
        assert result["a"]["b"]["c"]["d"] == "deep"


# ===========================================================================
# Multiple changes at once
# ===========================================================================

class TestMultipleChanges:
    def test_add_remove_change_simultaneously(self):
        old = {"x": 1, "y": 2, "z": "hello"}
        new = {"x": 99, "z": "hello", "w": True}
        result = _differ().diff(old, new)

        assert len(result.added) == 1
        assert result.added[0].path == "w"
        assert len(result.removed) == 1
        assert result.removed[0].path == "y"
        assert len(result.changed) == 1
        assert result.changed[0].path == "x"
        assert result.summary()["total"] == 3

    def test_nested_and_flat_changes(self):
        old = {"top": 1, "nested": {"a": 1, "b": 2}}
        new = {"top": 2, "nested": {"a": 1, "b": 99}}
        result = _differ().diff(old, new)
        paths = _paths(result.changes)
        assert "top" in paths
        assert "nested.b" in paths
        assert len(result.changes) == 2


# ===========================================================================
# Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_empty_string_value(self):
        result = _differ().diff({"s": ""}, {"s": ""})
        assert not result.has_changes

    def test_empty_string_changed(self):
        result = _differ().diff({"s": "hi"}, {"s": ""})
        assert len(result.changed) == 1

    def test_zero_unchanged(self):
        result = _differ().diff({"n": 0}, {"n": 0})
        assert not result.has_changes

    def test_zero_vs_false_type_changed(self):
        result = _differ().diff({"n": 0}, {"n": False})
        assert len(result.type_changed) == 1

    def test_nested_empty_dict_unchanged(self):
        result = _differ().diff({"sub": {}}, {"sub": {}})
        assert not result.has_changes

    def test_dict_added_inside_existing_dict(self):
        old = {"meta": {}}
        new = {"meta": {"version": 2}}
        result = _differ().diff(old, new)
        assert len(result.added) == 1
        assert result.added[0].path == "meta.version"

    def test_deterministic_order(self):
        """Changes should be returned in sorted path order."""
        old = {"z": 1, "a": 2, "m": 3}
        new = {"z": 9, "a": 8, "m": 7}
        result = _differ().diff(old, new)
        paths = _paths(result.changes)
        assert paths == sorted(paths)
