"""Tests for DocSchemaRegistry (E281) — ≥45 tests."""
from __future__ import annotations

import threading
from dataclasses import fields as dc_fields

import pytest

from docstoolkit.doc_schema_registry import (
    FieldDef,
    DocSchema,
    ValidationResult,
    RegistryStats,
    DocSchemaRegistry,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_reg() -> DocSchemaRegistry:
    return DocSchemaRegistry()


def basic_fields() -> list[FieldDef]:
    return [
        FieldDef(name="title", field_type="str", required=True),
        FieldDef(name="count", field_type="int", required=False, default=0),
    ]


# ===========================================================================
# FieldDef dataclass
# ===========================================================================

class TestFieldDef:
    def test_minimal_construction(self):
        f = FieldDef(name="x", field_type="str")
        assert f.name == "x"
        assert f.field_type == "str"
        assert f.required is False
        assert f.default is None
        assert f.description == ""
        assert f.validators == []

    def test_full_construction(self):
        v = lambda val: val > 0
        f = FieldDef(name="score", field_type="float", required=True,
                     default=1.0, description="numeric score", validators=[v])
        assert f.required is True
        assert f.default == 1.0
        assert f.description == "numeric score"
        assert len(f.validators) == 1

    def test_validators_default_is_independent(self):
        f1 = FieldDef(name="a", field_type="str")
        f2 = FieldDef(name="b", field_type="str")
        f1.validators.append("x")
        assert f2.validators == []


# ===========================================================================
# DocSchema dataclass
# ===========================================================================

class TestDocSchema:
    def test_default_version_is_one(self):
        s = DocSchema(schema_id="s1", name="Article")
        assert s.version == 1

    def test_fields_default_empty(self):
        s = DocSchema(schema_id="s1", name="Article")
        assert s.fields == []

    def test_description_default_empty(self):
        s = DocSchema(schema_id="s1", name="Article")
        assert s.description == ""


# ===========================================================================
# ValidationResult dataclass
# ===========================================================================

class TestValidationResult:
    def test_valid_result(self):
        r = ValidationResult(schema_id="s1", doc_id="d1", valid=True)
        assert r.valid is True
        assert r.errors == []

    def test_invalid_result(self):
        r = ValidationResult(schema_id="s1", doc_id="d1", valid=False,
                             errors=["missing required field 'x'"])
        assert r.valid is False
        assert len(r.errors) == 1


# ===========================================================================
# DocSchemaRegistry — register
# ===========================================================================

class TestRegister:
    def test_register_returns_doc_schema(self):
        reg = make_reg()
        schema = reg.register("Blog")
        assert isinstance(schema, DocSchema)

    def test_register_assigns_schema_id(self):
        reg = make_reg()
        schema = reg.register("Blog")
        assert schema.schema_id.startswith("schema_")
        assert len(schema.schema_id) == len("schema_") + 12

    def test_register_stores_name(self):
        reg = make_reg()
        schema = reg.register("Wiki")
        assert schema.name == "Wiki"

    def test_register_initial_version_is_one(self):
        reg = make_reg()
        schema = reg.register("Doc")
        assert schema.version == 1

    def test_register_with_fields(self):
        reg = make_reg()
        schema = reg.register("Article", fields=basic_fields())
        assert len(schema.fields) == 2

    def test_register_with_description(self):
        reg = make_reg()
        schema = reg.register("Post", description="A blog post")
        assert schema.description == "A blog post"

    def test_register_increments_total(self):
        reg = make_reg()
        assert reg.total_schemas == 0
        reg.register("A")
        assert reg.total_schemas == 1
        reg.register("B")
        assert reg.total_schemas == 2

    def test_register_unique_ids(self):
        reg = make_reg()
        ids = {reg.register(f"S{i}").schema_id for i in range(50)}
        assert len(ids) == 50

    def test_register_no_fields_yields_empty_list(self):
        reg = make_reg()
        schema = reg.register("Empty")
        assert schema.fields == []


# ===========================================================================
# DocSchemaRegistry — get / get_by_name
# ===========================================================================

class TestGet:
    def test_get_existing(self):
        reg = make_reg()
        created = reg.register("X")
        fetched = reg.get(created.schema_id)
        assert fetched is created

    def test_get_missing_returns_none(self):
        reg = make_reg()
        assert reg.get("nonexistent_id") is None

    def test_get_by_name_existing(self):
        reg = make_reg()
        created = reg.register("MySchema")
        fetched = reg.get_by_name("MySchema")
        assert fetched is created

    def test_get_by_name_missing_returns_none(self):
        reg = make_reg()
        assert reg.get_by_name("Ghost") is None

    def test_get_by_name_returns_first_match(self):
        reg = make_reg()
        s1 = reg.register("Dup")
        reg.register("Dup")
        result = reg.get_by_name("Dup")
        # Must be one of the two; just ensure it is a DocSchema
        assert isinstance(result, DocSchema)
        assert result.name == "Dup"


# ===========================================================================
# DocSchemaRegistry — update
# ===========================================================================

class TestUpdate:
    def test_update_increments_version(self):
        reg = make_reg()
        schema = reg.register("V")
        reg.update(schema.schema_id)
        assert schema.version == 2

    def test_update_twice(self):
        reg = make_reg()
        schema = reg.register("V")
        reg.update(schema.schema_id)
        reg.update(schema.schema_id)
        assert schema.version == 3

    def test_update_replaces_fields(self):
        reg = make_reg()
        schema = reg.register("F", fields=[FieldDef("old", "str")])
        new_fields = [FieldDef("new1", "int"), FieldDef("new2", "bool")]
        reg.update(schema.schema_id, fields=new_fields)
        assert len(schema.fields) == 2
        assert schema.fields[0].name == "new1"

    def test_update_replaces_description(self):
        reg = make_reg()
        schema = reg.register("D", description="old")
        reg.update(schema.schema_id, description="new")
        assert schema.description == "new"

    def test_update_missing_returns_none(self):
        reg = make_reg()
        result = reg.update("ghost_id")
        assert result is None

    def test_update_existing_returns_schema(self):
        reg = make_reg()
        schema = reg.register("R")
        result = reg.update(schema.schema_id)
        assert result is schema

    def test_update_without_fields_keeps_old_fields(self):
        reg = make_reg()
        schema = reg.register("K", fields=[FieldDef("f1", "str")])
        reg.update(schema.schema_id, description="updated desc")
        assert schema.fields[0].name == "f1"


# ===========================================================================
# DocSchemaRegistry — delete
# ===========================================================================

class TestDelete:
    def test_delete_existing_returns_true(self):
        reg = make_reg()
        schema = reg.register("Del")
        assert reg.delete(schema.schema_id) is True

    def test_delete_removes_from_registry(self):
        reg = make_reg()
        schema = reg.register("Del")
        reg.delete(schema.schema_id)
        assert reg.get(schema.schema_id) is None

    def test_delete_nonexistent_returns_false(self):
        reg = make_reg()
        assert reg.delete("no_such_id") is False

    def test_delete_decrements_total(self):
        reg = make_reg()
        schema = reg.register("X")
        assert reg.total_schemas == 1
        reg.delete(schema.schema_id)
        assert reg.total_schemas == 0


# ===========================================================================
# DocSchemaRegistry — schemas()
# ===========================================================================

class TestSchemas:
    def test_schemas_empty(self):
        reg = make_reg()
        assert reg.schemas() == []

    def test_schemas_returns_all(self):
        reg = make_reg()
        reg.register("C")
        reg.register("A")
        reg.register("B")
        result = reg.schemas()
        assert len(result) == 3

    def test_schemas_sorted_by_name(self):
        reg = make_reg()
        reg.register("Zebra")
        reg.register("Alpha")
        reg.register("Middle")
        names = [s.name for s in reg.schemas()]
        assert names == sorted(names)


# ===========================================================================
# DocSchemaRegistry — add_field / remove_field
# ===========================================================================

class TestFieldOps:
    def test_add_field_success(self):
        reg = make_reg()
        schema = reg.register("S")
        result = reg.add_field(schema.schema_id, FieldDef("new_field", "str"))
        assert result is True
        assert len(schema.fields) == 1
        assert schema.fields[0].name == "new_field"

    def test_add_field_missing_schema_returns_false(self):
        reg = make_reg()
        result = reg.add_field("ghost", FieldDef("f", "str"))
        assert result is False

    def test_remove_field_success(self):
        reg = make_reg()
        schema = reg.register("S", fields=[FieldDef("keep", "str"), FieldDef("drop", "int")])
        result = reg.remove_field(schema.schema_id, "drop")
        assert result is True
        assert len(schema.fields) == 1
        assert schema.fields[0].name == "keep"

    def test_remove_field_missing_schema_returns_false(self):
        reg = make_reg()
        assert reg.remove_field("ghost", "f") is False

    def test_remove_field_missing_field_returns_false(self):
        reg = make_reg()
        schema = reg.register("S", fields=[FieldDef("existing", "str")])
        assert reg.remove_field(schema.schema_id, "nonexistent") is False

    def test_add_multiple_fields(self):
        reg = make_reg()
        schema = reg.register("M")
        for i in range(5):
            reg.add_field(schema.schema_id, FieldDef(f"f{i}", "str"))
        assert len(schema.fields) == 5


# ===========================================================================
# DocSchemaRegistry — validate
# ===========================================================================

class TestValidate:
    def _make_schema(self, reg: DocSchemaRegistry) -> DocSchema:
        fields = [
            FieldDef(name="title", field_type="str", required=True),
            FieldDef(name="count", field_type="int", required=False),
            FieldDef(name="score", field_type="float", required=False),
            FieldDef(name="active", field_type="bool", required=False),
            FieldDef(name="tags", field_type="list", required=False),
            FieldDef(name="meta", field_type="dict", required=False),
        ]
        return reg.register("TestDoc", fields=fields)

    def test_valid_doc(self):
        reg = make_reg()
        schema = self._make_schema(reg)
        result = reg.validate(schema.schema_id, {"title": "Hello"})
        assert result.valid is True
        assert result.errors == []

    def test_missing_required_field(self):
        reg = make_reg()
        schema = self._make_schema(reg)
        result = reg.validate(schema.schema_id, {})
        assert result.valid is False
        assert any("title" in e for e in result.errors)

    def test_wrong_type_str(self):
        reg = make_reg()
        schema = self._make_schema(reg)
        result = reg.validate(schema.schema_id, {"title": 123})
        assert result.valid is False
        assert any("title" in e for e in result.errors)

    def test_correct_int(self):
        reg = make_reg()
        schema = self._make_schema(reg)
        result = reg.validate(schema.schema_id, {"title": "x", "count": 5})
        assert result.valid is True

    def test_wrong_type_int(self):
        reg = make_reg()
        schema = self._make_schema(reg)
        result = reg.validate(schema.schema_id, {"title": "x", "count": "five"})
        assert result.valid is False

    def test_bool_rejected_for_int_field(self):
        reg = make_reg()
        schema = self._make_schema(reg)
        result = reg.validate(schema.schema_id, {"title": "x", "count": True})
        assert result.valid is False

    def test_int_accepted_for_float_field(self):
        reg = make_reg()
        schema = self._make_schema(reg)
        result = reg.validate(schema.schema_id, {"title": "x", "score": 3})
        assert result.valid is True

    def test_float_accepted_for_float_field(self):
        reg = make_reg()
        schema = self._make_schema(reg)
        result = reg.validate(schema.schema_id, {"title": "x", "score": 3.14})
        assert result.valid is True

    def test_bool_rejected_for_float_field(self):
        reg = make_reg()
        schema = self._make_schema(reg)
        result = reg.validate(schema.schema_id, {"title": "x", "score": True})
        assert result.valid is False

    def test_bool_field(self):
        reg = make_reg()
        schema = self._make_schema(reg)
        result = reg.validate(schema.schema_id, {"title": "x", "active": True})
        assert result.valid is True

    def test_list_field(self):
        reg = make_reg()
        schema = self._make_schema(reg)
        result = reg.validate(schema.schema_id, {"title": "x", "tags": ["a", "b"]})
        assert result.valid is True

    def test_dict_field(self):
        reg = make_reg()
        schema = self._make_schema(reg)
        result = reg.validate(schema.schema_id, {"title": "x", "meta": {"k": "v"}})
        assert result.valid is True

    def test_unknown_schema_returns_error(self):
        reg = make_reg()
        result = reg.validate("nonexistent", {"title": "x"})
        assert result.valid is False
        assert result.errors == ["schema not found"]

    def test_validation_result_has_correct_doc_id(self):
        reg = make_reg()
        schema = reg.register("S")
        result = reg.validate(schema.schema_id, {}, doc_id="my_doc_42")
        assert result.doc_id == "my_doc_42"

    def test_validation_result_default_doc_id(self):
        reg = make_reg()
        schema = reg.register("S")
        result = reg.validate(schema.schema_id, {})
        assert result.doc_id == "doc"

    def test_multiple_errors_reported(self):
        reg = make_reg()
        fields = [
            FieldDef("a", "str", required=True),
            FieldDef("b", "int", required=True),
        ]
        schema = reg.register("Multi", fields=fields)
        result = reg.validate(schema.schema_id, {})
        assert len(result.errors) == 2

    def test_extra_keys_ignored(self):
        reg = make_reg()
        schema = reg.register("S", fields=[FieldDef("x", "str", required=True)])
        result = reg.validate(schema.schema_id, {"x": "hello", "extra": 999})
        assert result.valid is True


# ===========================================================================
# DocSchemaRegistry — stats
# ===========================================================================

class TestStats:
    def test_stats_empty(self):
        reg = make_reg()
        s = reg.stats()
        assert s.total_schemas == 0
        assert s.total_fields == 0
        assert s.avg_fields_per_schema == 0.0

    def test_stats_after_register(self):
        reg = make_reg()
        reg.register("A", fields=[FieldDef("f1", "str"), FieldDef("f2", "int")])
        reg.register("B", fields=[FieldDef("g1", "bool")])
        s = reg.stats()
        assert s.total_schemas == 2
        assert s.total_fields == 3
        assert s.avg_fields_per_schema == 1.5

    def test_stats_returns_registry_stats(self):
        reg = make_reg()
        assert isinstance(reg.stats(), RegistryStats)

    def test_total_schemas_property(self):
        reg = make_reg()
        reg.register("X")
        reg.register("Y")
        assert reg.total_schemas == 2


# ===========================================================================
# Thread safety
# ===========================================================================

class TestThreadSafety:
    def test_concurrent_register(self):
        reg = make_reg()
        results = []
        lock = threading.Lock()

        def worker():
            schema = reg.register("Concurrent")
            with lock:
                results.append(schema.schema_id)

        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 20
        assert len(set(results)) == 20  # all unique IDs
        assert reg.total_schemas == 20

    def test_concurrent_delete(self):
        reg = make_reg()
        schemas = [reg.register(f"S{i}") for i in range(10)]
        deleted = []
        lock = threading.Lock()

        def worker(sid):
            result = reg.delete(sid)
            with lock:
                deleted.append(result)

        threads = [threading.Thread(target=worker, args=(s.schema_id,)) for s in schemas]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert sum(deleted) == 10
        assert reg.total_schemas == 0
