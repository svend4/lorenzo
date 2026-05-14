"""Tests for ``docstoolkit.attribute_store``."""
from __future__ import annotations

import os
import tempfile

import pytest

from docstoolkit.attribute_store import (
    AttributeChange,
    AttributeStore,
    AttributeValue,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def store() -> AttributeStore:
    s = AttributeStore()
    yield s
    s.close()


@pytest.fixture
def store_with_history() -> AttributeStore:
    s = AttributeStore(track_history=True)
    yield s
    s.close()


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestAttributeValue:
    def test_construct(self):
        av = AttributeValue("e1", "k", "v", "string", 1.0)
        assert av.entity_id == "e1"
        assert av.key == "k"
        assert av.value == "v"
        assert av.value_type == "string"
        assert av.updated_at == 1.0

    def test_equality(self):
        a = AttributeValue("e", "k", 1, "int", 0.0)
        b = AttributeValue("e", "k", 1, "int", 0.0)
        assert a == b

    def test_inequality(self):
        a = AttributeValue("e", "k", 1, "int", 0.0)
        b = AttributeValue("e", "k", 2, "int", 0.0)
        assert a != b


class TestAttributeChange:
    def test_construct(self):
        ch = AttributeChange("e1", "k", "old", "new", 5.0)
        assert ch.entity_id == "e1"
        assert ch.key == "k"
        assert ch.old_value == "old"
        assert ch.new_value == "new"
        assert ch.timestamp == 5.0

    def test_equality(self):
        a = AttributeChange("e", "k", 1, 2, 1.0)
        b = AttributeChange("e", "k", 1, 2, 1.0)
        assert a == b


# ---------------------------------------------------------------------------
# set
# ---------------------------------------------------------------------------


class TestSet:
    def test_set_string(self, store):
        result = store.set("e1", "title", "hello")
        assert isinstance(result, AttributeValue)
        assert result.value == "hello"
        assert result.value_type == "string"

    def test_set_returns_attribute_value(self, store):
        result = store.set("e1", "k", 42)
        assert isinstance(result, AttributeValue)

    def test_set_with_explicit_now(self, store):
        result = store.set("e1", "k", "v", now=123.456)
        assert result.updated_at == 123.456

    def test_set_uses_time_when_now_zero(self, store):
        result = store.set("e1", "k", "v")
        assert result.updated_at > 0

    def test_set_multiple_keys(self, store):
        store.set("e1", "k1", "v1")
        store.set("e1", "k2", "v2")
        assert store.get("e1", "k1") == "v1"
        assert store.get("e1", "k2") == "v2"

    def test_set_multiple_entities(self, store):
        store.set("e1", "k", "v1")
        store.set("e2", "k", "v2")
        assert store.get("e1", "k") == "v1"
        assert store.get("e2", "k") == "v2"


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


class TestGet:
    def test_get_existing(self, store):
        store.set("e", "k", "hello")
        assert store.get("e", "k") == "hello"

    def test_get_missing_returns_none(self, store):
        assert store.get("e", "missing") is None

    def test_get_missing_returns_default(self, store):
        assert store.get("e", "missing", default="x") == "x"

    def test_get_missing_entity(self, store):
        store.set("other", "k", "v")
        assert store.get("e", "k") is None

    def test_get_after_overwrite(self, store):
        store.set("e", "k", "old")
        store.set("e", "k", "new")
        assert store.get("e", "k") == "new"


# ---------------------------------------------------------------------------
# get_typed
# ---------------------------------------------------------------------------


class TestGetTyped:
    def test_returns_attribute_value(self, store):
        store.set("e", "k", "v", now=10.0)
        av = store.get_typed("e", "k")
        assert isinstance(av, AttributeValue)
        assert av.entity_id == "e"
        assert av.key == "k"
        assert av.value == "v"
        assert av.value_type == "string"
        assert av.updated_at == 10.0

    def test_missing_returns_none(self, store):
        assert store.get_typed("e", "missing") is None

    def test_typed_int(self, store):
        store.set("e", "k", 42)
        av = store.get_typed("e", "k")
        assert av.value == 42
        assert av.value_type == "int"

    def test_typed_bool(self, store):
        store.set("e", "k", True)
        av = store.get_typed("e", "k")
        assert av.value is True
        assert av.value_type == "bool"


# ---------------------------------------------------------------------------
# has
# ---------------------------------------------------------------------------


class TestHas:
    def test_has_existing(self, store):
        store.set("e", "k", "v")
        assert store.has("e", "k") is True

    def test_has_missing(self, store):
        assert store.has("e", "k") is False

    def test_has_after_delete(self, store):
        store.set("e", "k", "v")
        store.delete("e", "k")
        assert store.has("e", "k") is False

    def test_has_wrong_entity(self, store):
        store.set("e1", "k", "v")
        assert store.has("e2", "k") is False


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


class TestDelete:
    def test_delete_existing(self, store):
        store.set("e", "k", "v")
        assert store.delete("e", "k") is True
        assert not store.has("e", "k")

    def test_delete_missing(self, store):
        assert store.delete("e", "k") is False

    def test_delete_only_one_key(self, store):
        store.set("e", "k1", 1)
        store.set("e", "k2", 2)
        store.delete("e", "k1")
        assert not store.has("e", "k1")
        assert store.has("e", "k2")

    def test_delete_then_set(self, store):
        store.set("e", "k", "v1")
        store.delete("e", "k")
        store.set("e", "k", "v2")
        assert store.get("e", "k") == "v2"


# ---------------------------------------------------------------------------
# set_many
# ---------------------------------------------------------------------------


class TestSetMany:
    def test_set_many_basic(self, store):
        results = store.set_many("e", {"a": 1, "b": "two", "c": True})
        assert len(results) == 3
        assert all(isinstance(r, AttributeValue) for r in results)

    def test_set_many_get_back(self, store):
        store.set_many("e", {"a": 1, "b": "two"})
        assert store.get("e", "a") == 1
        assert store.get("e", "b") == "two"

    def test_set_many_empty(self, store):
        results = store.set_many("e", {})
        assert results == []
        assert store.count_attributes("e") == 0

    def test_set_many_overwrites(self, store):
        store.set("e", "a", "old")
        store.set_many("e", {"a": "new"})
        assert store.get("e", "a") == "new"

    def test_set_many_uses_now(self, store):
        results = store.set_many("e", {"a": 1, "b": 2}, now=99.0)
        assert all(r.updated_at == 99.0 for r in results)

    def test_set_many_mixed_types(self, store):
        store.set_many(
            "e",
            {"int": 1, "float": 2.5, "bool": True, "str": "x", "list": [1, 2]},
        )
        assert store.get("e", "int") == 1
        assert store.get("e", "float") == 2.5
        assert store.get("e", "bool") is True
        assert store.get("e", "str") == "x"
        assert store.get("e", "list") == [1, 2]


# ---------------------------------------------------------------------------
# get_all
# ---------------------------------------------------------------------------


class TestGetAll:
    def test_get_all_empty(self, store):
        assert store.get_all("e") == {}

    def test_get_all_basic(self, store):
        store.set("e", "a", 1)
        store.set("e", "b", "two")
        assert store.get_all("e") == {"a": 1, "b": "two"}

    def test_get_all_only_entity(self, store):
        store.set("e1", "a", 1)
        store.set("e2", "b", 2)
        assert store.get_all("e1") == {"a": 1}
        assert store.get_all("e2") == {"b": 2}

    def test_get_all_with_complex_types(self, store):
        store.set("e", "list", [1, 2, 3])
        store.set("e", "dict", {"k": "v"})
        out = store.get_all("e")
        assert out["list"] == [1, 2, 3]
        assert out["dict"] == {"k": "v"}


# ---------------------------------------------------------------------------
# delete_entity
# ---------------------------------------------------------------------------


class TestDeleteEntity:
    def test_delete_entity_count(self, store):
        store.set_many("e", {"a": 1, "b": 2, "c": 3})
        assert store.delete_entity("e") == 3

    def test_delete_entity_removes_attrs(self, store):
        store.set_many("e", {"a": 1, "b": 2})
        store.delete_entity("e")
        assert store.get_all("e") == {}

    def test_delete_entity_missing(self, store):
        assert store.delete_entity("missing") == 0

    def test_delete_entity_isolation(self, store):
        store.set("e1", "a", 1)
        store.set("e2", "a", 2)
        store.delete_entity("e1")
        assert store.get("e2", "a") == 2


# ---------------------------------------------------------------------------
# entities_with_key
# ---------------------------------------------------------------------------


class TestEntitiesWithKey:
    def test_empty(self, store):
        assert store.entities_with_key("k") == []

    def test_basic(self, store):
        store.set("e1", "k", 1)
        store.set("e2", "k", 2)
        store.set("e3", "other", 3)
        assert store.entities_with_key("k") == ["e1", "e2"]

    def test_distinct(self, store):
        store.set("e1", "k", 1)
        store.set("e1", "k", 2)  # overwrites
        assert store.entities_with_key("k") == ["e1"]

    def test_sorted(self, store):
        store.set("zebra", "k", 1)
        store.set("apple", "k", 1)
        result = store.entities_with_key("k")
        assert result == ["apple", "zebra"]


# ---------------------------------------------------------------------------
# entities_with_value
# ---------------------------------------------------------------------------


class TestEntitiesWithValue:
    def test_basic(self, store):
        store.set("e1", "status", "active")
        store.set("e2", "status", "inactive")
        store.set("e3", "status", "active")
        result = store.entities_with_value("status", "active")
        assert result == ["e1", "e3"]

    def test_no_matches(self, store):
        store.set("e1", "k", "v")
        assert store.entities_with_value("k", "other") == []

    def test_int_value(self, store):
        store.set("e1", "n", 42)
        store.set("e2", "n", 99)
        assert store.entities_with_value("n", 42) == ["e1"]

    def test_bool_value(self, store):
        store.set("e1", "active", True)
        store.set("e2", "active", False)
        assert store.entities_with_value("active", True) == ["e1"]

    def test_type_differentiation(self, store):
        # int 1 should not match bool True even though both encode to "1"
        store.set("e1", "k", 1)
        store.set("e2", "k", True)
        assert store.entities_with_value("k", 1) == ["e1"]
        assert store.entities_with_value("k", True) == ["e2"]


# ---------------------------------------------------------------------------
# count_entities
# ---------------------------------------------------------------------------


class TestCountEntities:
    def test_empty(self, store):
        assert store.count_entities() == 0

    def test_one(self, store):
        store.set("e1", "k", 1)
        assert store.count_entities() == 1

    def test_multiple(self, store):
        store.set("e1", "k", 1)
        store.set("e2", "k", 1)
        store.set("e3", "k", 1)
        assert store.count_entities() == 3

    def test_same_entity_multiple_keys(self, store):
        store.set("e1", "k1", 1)
        store.set("e1", "k2", 2)
        assert store.count_entities() == 1


# ---------------------------------------------------------------------------
# count_attributes
# ---------------------------------------------------------------------------


class TestCountAttributes:
    def test_total_empty(self, store):
        assert store.count_attributes() == 0

    def test_total(self, store):
        store.set("e1", "a", 1)
        store.set("e1", "b", 2)
        store.set("e2", "c", 3)
        assert store.count_attributes() == 3

    def test_per_entity(self, store):
        store.set("e1", "a", 1)
        store.set("e1", "b", 2)
        store.set("e2", "c", 3)
        assert store.count_attributes("e1") == 2
        assert store.count_attributes("e2") == 1

    def test_per_entity_empty(self, store):
        assert store.count_attributes("missing") == 0


# ---------------------------------------------------------------------------
# Types — int, float, bool, str
# ---------------------------------------------------------------------------


class TestTypes:
    def test_int_roundtrip(self, store):
        store.set("e", "k", 42)
        v = store.get("e", "k")
        assert v == 42
        assert isinstance(v, int)

    def test_negative_int(self, store):
        store.set("e", "k", -7)
        assert store.get("e", "k") == -7

    def test_zero_int(self, store):
        store.set("e", "k", 0)
        assert store.get("e", "k") == 0

    def test_float_roundtrip(self, store):
        store.set("e", "k", 3.14)
        v = store.get("e", "k")
        assert v == 3.14
        assert isinstance(v, float)

    def test_negative_float(self, store):
        store.set("e", "k", -0.5)
        assert store.get("e", "k") == -0.5

    def test_bool_true(self, store):
        store.set("e", "k", True)
        v = store.get("e", "k")
        assert v is True

    def test_bool_false(self, store):
        store.set("e", "k", False)
        v = store.get("e", "k")
        assert v is False

    def test_string_roundtrip(self, store):
        store.set("e", "k", "hello world")
        assert store.get("e", "k") == "hello world"

    def test_empty_string(self, store):
        store.set("e", "k", "")
        assert store.get("e", "k") == ""

    def test_unicode_string(self, store):
        store.set("e", "k", "привет 你好")
        assert store.get("e", "k") == "привет 你好"

    def test_value_type_field(self, store):
        store.set("e", "i", 1)
        store.set("e", "f", 1.5)
        store.set("e", "b", True)
        store.set("e", "s", "x")
        assert store.get_typed("e", "i").value_type == "int"
        assert store.get_typed("e", "f").value_type == "float"
        assert store.get_typed("e", "b").value_type == "bool"
        assert store.get_typed("e", "s").value_type == "string"

    def test_unsupported_type(self, store):
        with pytest.raises(TypeError):
            store.set("e", "k", object())


# ---------------------------------------------------------------------------
# JSON types — list, dict
# ---------------------------------------------------------------------------


class TestJsonTypes:
    def test_list_roundtrip(self, store):
        store.set("e", "k", [1, 2, 3])
        assert store.get("e", "k") == [1, 2, 3]

    def test_empty_list(self, store):
        store.set("e", "k", [])
        v = store.get("e", "k")
        assert v == []
        assert isinstance(v, list)

    def test_nested_list(self, store):
        store.set("e", "k", [[1, 2], [3, 4]])
        assert store.get("e", "k") == [[1, 2], [3, 4]]

    def test_dict_roundtrip(self, store):
        store.set("e", "k", {"a": 1, "b": "two"})
        assert store.get("e", "k") == {"a": 1, "b": "two"}

    def test_empty_dict(self, store):
        store.set("e", "k", {})
        v = store.get("e", "k")
        assert v == {}
        assert isinstance(v, dict)

    def test_nested_dict(self, store):
        store.set("e", "k", {"outer": {"inner": [1, 2]}})
        assert store.get("e", "k") == {"outer": {"inner": [1, 2]}}

    def test_mixed_list(self, store):
        store.set("e", "k", [1, "two", 3.0, True, None])
        assert store.get("e", "k") == [1, "two", 3.0, True, None]

    def test_json_value_type(self, store):
        store.set("e", "k", [1, 2])
        assert store.get_typed("e", "k").value_type == "json"


# ---------------------------------------------------------------------------
# Upsert behaviour
# ---------------------------------------------------------------------------


class TestUpsert:
    def test_overwrite_same_type(self, store):
        store.set("e", "k", 1)
        store.set("e", "k", 2)
        assert store.get("e", "k") == 2
        assert store.count_attributes("e") == 1

    def test_overwrite_different_type(self, store):
        store.set("e", "k", "string")
        store.set("e", "k", 42)
        av = store.get_typed("e", "k")
        assert av.value == 42
        assert av.value_type == "int"

    def test_updated_at_changes(self, store):
        store.set("e", "k", "a", now=1.0)
        store.set("e", "k", "b", now=2.0)
        assert store.get_typed("e", "k").updated_at == 2.0


# ---------------------------------------------------------------------------
# History
# ---------------------------------------------------------------------------


class TestHistory:
    def test_history_disabled_by_default(self, store):
        store.set("e", "k", "v")
        assert store.history("e") == []

    def test_history_records_insert(self, store_with_history):
        store_with_history.set("e", "k", "v1", now=1.0)
        h = store_with_history.history("e")
        assert len(h) == 1
        assert h[0].entity_id == "e"
        assert h[0].key == "k"
        assert h[0].old_value is None
        assert h[0].new_value == "v1"
        assert h[0].timestamp == 1.0

    def test_history_records_update(self, store_with_history):
        store_with_history.set("e", "k", "v1", now=1.0)
        store_with_history.set("e", "k", "v2", now=2.0)
        h = store_with_history.history("e")
        assert len(h) == 2
        assert h[1].old_value == "v1"
        assert h[1].new_value == "v2"

    def test_history_records_delete(self, store_with_history):
        store_with_history.set("e", "k", "v1")
        store_with_history.delete("e", "k")
        h = store_with_history.history("e")
        assert len(h) == 2
        assert h[1].old_value == "v1"
        assert h[1].new_value is None

    def test_history_filter_by_key(self, store_with_history):
        store_with_history.set("e", "a", 1)
        store_with_history.set("e", "b", 2)
        h = store_with_history.history("e", key="a")
        assert len(h) == 1
        assert h[0].key == "a"

    def test_history_other_entity(self, store_with_history):
        store_with_history.set("e1", "k", 1)
        store_with_history.set("e2", "k", 2)
        h = store_with_history.history("e1")
        assert len(h) == 1
        assert h[0].entity_id == "e1"

    def test_history_set_many(self, store_with_history):
        store_with_history.set_many("e", {"a": 1, "b": 2})
        h = store_with_history.history("e")
        assert len(h) == 2

    def test_history_delete_entity(self, store_with_history):
        store_with_history.set_many("e", {"a": 1, "b": 2})
        store_with_history.delete_entity("e")
        h = store_with_history.history("e")
        # 2 inserts + 2 deletes
        assert len(h) == 4

    def test_history_returns_attribute_changes(self, store_with_history):
        store_with_history.set("e", "k", 1)
        h = store_with_history.history("e")
        assert all(isinstance(c, AttributeChange) for c in h)


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


class TestPersistence:
    def test_file_db(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "attrs.db")
            s1 = AttributeStore(db_path=path)
            s1.set("e", "k", "hello")
            s1.set("e", "n", 42)
            s1.close()

            s2 = AttributeStore(db_path=path)
            assert s2.get("e", "k") == "hello"
            assert s2.get("e", "n") == 42
            s2.close()

    def test_file_db_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "attrs.db")
            s1 = AttributeStore(db_path=path, track_history=True)
            s1.set("e", "k", "v1", now=1.0)
            s1.set("e", "k", "v2", now=2.0)
            s1.close()

            s2 = AttributeStore(db_path=path, track_history=True)
            h = s2.history("e")
            assert len(h) == 2
            s2.close()

    def test_clear(self, store):
        store.set("e", "k", "v")
        store.set("e2", "k", "v")
        store.clear()
        assert store.count_entities() == 0
        assert store.count_attributes() == 0

    def test_close_idempotent(self):
        s = AttributeStore()
        s.close()
        # second close should not raise
        s.close()


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_string_value(self, store):
        store.set("e", "k", "")
        assert store.has("e", "k")
        assert store.get("e", "k") == ""

    def test_missing_entity_get_all(self, store):
        assert store.get_all("nope") == {}

    def test_missing_entity_count(self, store):
        assert store.count_attributes("nope") == 0

    def test_key_with_special_chars(self, store):
        store.set("e", "k/with-special.chars:1", "v")
        assert store.get("e", "k/with-special.chars:1") == "v"

    def test_entity_id_with_special_chars(self, store):
        store.set("e:1/2", "k", "v")
        assert store.get("e:1/2", "k") == "v"

    def test_large_value(self, store):
        big = "x" * 10000
        store.set("e", "k", big)
        assert store.get("e", "k") == big

    def test_many_entities(self, store):
        for i in range(100):
            store.set(f"e{i}", "k", i)
        assert store.count_entities() == 100
        assert store.get("e50", "k") == 50

    def test_default_is_returned_not_stored(self, store):
        assert store.get("e", "k", default="x") == "x"
        # subsequent get without default still returns None
        assert store.get("e", "k") is None

    def test_history_when_disabled_with_key(self, store):
        store.set("e", "k", "v")
        assert store.history("e", key="k") == []

    def test_set_zero_float(self, store):
        store.set("e", "k", 0.0)
        v = store.get("e", "k")
        assert v == 0.0
        assert isinstance(v, float)

    def test_bool_vs_int_preserved(self, store):
        # The store must distinguish bool from int on read.
        store.set("e", "b", True)
        store.set("e", "i", 1)
        b = store.get("e", "b")
        i = store.get("e", "i")
        assert b is True
        assert i == 1
        assert isinstance(b, bool)
        assert isinstance(i, int) and not isinstance(i, bool)
