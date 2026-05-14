"""Tests for the schema_registry module (E43)."""
from __future__ import annotations

import time
import pytest

from docstoolkit.schema_registry import (
    SchemaVersion,
    FieldDef,
    Schema,
    SchemaValidationError,
    SchemaValidator,
    SchemaRegistry,
    VALID_FIELD_TYPES,
)


# ---------------------------------------------------------------------------
# SchemaVersion
# ---------------------------------------------------------------------------

class TestSchemaVersionStr:
    def test_str_basic(self):
        assert str(SchemaVersion(1, 2, 3)) == "1.2.3"

    def test_str_zeros(self):
        assert str(SchemaVersion(0, 0, 0)) == "0.0.0"

    def test_str_large(self):
        assert str(SchemaVersion(10, 20, 30)) == "10.20.30"


class TestSchemaVersionParse:
    def test_parse_basic(self):
        v = SchemaVersion.parse("1.2.3")
        assert v == SchemaVersion(1, 2, 3)

    def test_parse_roundtrip(self):
        v = SchemaVersion(3, 14, 159)
        assert SchemaVersion.parse(str(v)) == v

    def test_parse_zeros(self):
        v = SchemaVersion.parse("0.0.0")
        assert v == SchemaVersion(0, 0, 0)

    def test_parse_invalid_not_enough_parts(self):
        with pytest.raises(ValueError):
            SchemaVersion.parse("1.2")

    def test_parse_invalid_too_many_parts(self):
        with pytest.raises(ValueError):
            SchemaVersion.parse("1.2.3.4")

    def test_parse_invalid_non_numeric(self):
        with pytest.raises(ValueError):
            SchemaVersion.parse("a.b.c")

    def test_parse_strips_whitespace(self):
        v = SchemaVersion.parse("  2.0.1  ")
        assert v == SchemaVersion(2, 0, 1)


class TestSchemaVersionCompatibility:
    def test_same_major_compatible(self):
        assert SchemaVersion(1, 0, 0).is_compatible(SchemaVersion(1, 5, 3))

    def test_different_major_incompatible(self):
        assert not SchemaVersion(1, 0, 0).is_compatible(SchemaVersion(2, 0, 0))

    def test_same_version_compatible(self):
        v = SchemaVersion(2, 3, 4)
        assert v.is_compatible(v)

    def test_zero_major_compatible(self):
        assert SchemaVersion(0, 1, 0).is_compatible(SchemaVersion(0, 9, 9))


class TestSchemaVersionBump:
    def test_bump_patch(self):
        assert SchemaVersion(1, 2, 3).bump_patch() == SchemaVersion(1, 2, 4)

    def test_bump_minor_resets_patch(self):
        assert SchemaVersion(1, 2, 3).bump_minor() == SchemaVersion(1, 3, 0)

    def test_bump_major_resets_minor_patch(self):
        assert SchemaVersion(1, 2, 3).bump_major() == SchemaVersion(2, 0, 0)

    def test_bump_immutable(self):
        original = SchemaVersion(1, 2, 3)
        original.bump_patch()
        assert original == SchemaVersion(1, 2, 3)

    def test_bump_chain(self):
        v = SchemaVersion(0, 0, 0).bump_patch().bump_patch().bump_minor()
        assert v == SchemaVersion(0, 1, 0)

    def test_ordering(self):
        v1 = SchemaVersion(1, 0, 0)
        v2 = SchemaVersion(1, 0, 1)
        v3 = SchemaVersion(1, 1, 0)
        v4 = SchemaVersion(2, 0, 0)
        assert v1 < v2 < v3 < v4
        assert v4 > v3 > v2 > v1

    def test_equality(self):
        assert SchemaVersion(1, 2, 3) == SchemaVersion(1, 2, 3)
        assert SchemaVersion(1, 2, 3) != SchemaVersion(1, 2, 4)

    def test_hashable(self):
        s = {SchemaVersion(1, 0, 0), SchemaVersion(1, 0, 0), SchemaVersion(2, 0, 0)}
        assert len(s) == 2


# ---------------------------------------------------------------------------
# FieldDef
# ---------------------------------------------------------------------------

class TestFieldDefDefaults:
    def test_required_default_true(self):
        f = FieldDef(name="x", field_type="string")
        assert f.required is True

    def test_nullable_default_false(self):
        f = FieldDef(name="x", field_type="string")
        assert f.nullable is False

    def test_description_default_empty(self):
        f = FieldDef(name="x", field_type="string")
        assert f.description == ""

    def test_all_valid_types(self):
        for ft in VALID_FIELD_TYPES:
            f = FieldDef(name="x", field_type=ft)
            assert f.field_type == ft

    def test_invalid_type_raises(self):
        with pytest.raises(ValueError):
            FieldDef(name="x", field_type="unknown")

    def test_custom_values(self):
        f = FieldDef(
            name="score",
            field_type="float",
            required=False,
            nullable=True,
            description="A score value",
        )
        assert f.name == "score"
        assert f.field_type == "float"
        assert f.required is False
        assert f.nullable is True
        assert f.description == "A score value"


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

def make_schema(**kwargs) -> Schema:
    defaults = dict(
        name="TestSchema",
        version=SchemaVersion(1, 0, 0),
        fields=[
            FieldDef("id", "integer"),
            FieldDef("title", "string"),
            FieldDef("score", "float", required=False),
        ],
        description="A test schema",
    )
    defaults.update(kwargs)
    return Schema(**defaults)


class TestSchema:
    def test_schema_id_auto_generated(self):
        s = make_schema()
        assert s.schema_id is not None
        assert len(s.schema_id) == 8

    def test_schema_id_unique(self):
        s1 = make_schema()
        s2 = make_schema()
        assert s1.schema_id != s2.schema_id

    def test_created_ts_auto(self):
        before = time.time()
        s = make_schema()
        after = time.time()
        assert before <= s.created_ts <= after

    def test_field_names(self):
        s = make_schema()
        assert s.field_names() == ["id", "title", "score"]

    def test_required_fields(self):
        s = make_schema()
        req = s.required_fields()
        assert len(req) == 2
        assert req[0].name == "id"
        assert req[1].name == "title"

    def test_get_field_found(self):
        s = make_schema()
        f = s.get_field("title")
        assert f is not None
        assert f.name == "title"
        assert f.field_type == "string"

    def test_get_field_not_found(self):
        s = make_schema()
        assert s.get_field("nonexistent") is None

    def test_description_default(self):
        s = Schema(name="X", version=SchemaVersion(1, 0, 0), fields=[])
        assert s.description == ""


# ---------------------------------------------------------------------------
# SchemaValidator
# ---------------------------------------------------------------------------

def make_validator_schema() -> Schema:
    return Schema(
        name="Validator",
        version=SchemaVersion(1, 0, 0),
        fields=[
            FieldDef("name", "string"),
            FieldDef("age", "integer"),
            FieldDef("score", "float"),
            FieldDef("active", "boolean"),
            FieldDef("tags", "array"),
            FieldDef("meta", "object"),
            FieldDef("nickname", "string", required=False),
            FieldDef("bio", "string", required=True, nullable=True),
        ],
    )


class TestSchemaValidator:
    def setup_method(self):
        self.validator = SchemaValidator()
        self.schema = make_validator_schema()

    def _valid_data(self):
        return {
            "name": "Alice",
            "age": 30,
            "score": 9.5,
            "active": True,
            "tags": ["a", "b"],
            "meta": {"key": "val"},
            "bio": None,  # nullable
        }

    def test_valid_data_no_errors(self):
        errors = self.validator.validate(self._valid_data(), self.schema)
        assert errors == []

    def test_missing_required_field(self):
        data = self._valid_data()
        del data["name"]
        errors = self.validator.validate(data, self.schema)
        assert any(e.field == "name" for e in errors)

    def test_missing_optional_field_ok(self):
        data = self._valid_data()
        # nickname is optional, not present
        errors = self.validator.validate(data, self.schema)
        assert not any(e.field == "nickname" for e in errors)

    def test_nullable_field_none_ok(self):
        data = self._valid_data()
        data["bio"] = None
        errors = self.validator.validate(data, self.schema)
        assert not any(e.field == "bio" for e in errors)

    def test_non_nullable_field_none_error(self):
        data = self._valid_data()
        data["name"] = None
        errors = self.validator.validate(data, self.schema)
        assert any(e.field == "name" for e in errors)

    def test_wrong_type_string(self):
        data = self._valid_data()
        data["name"] = 123
        errors = self.validator.validate(data, self.schema)
        assert any(e.field == "name" for e in errors)

    def test_wrong_type_integer(self):
        data = self._valid_data()
        data["age"] = "thirty"
        errors = self.validator.validate(data, self.schema)
        assert any(e.field == "age" for e in errors)

    def test_bool_not_accepted_as_integer(self):
        data = self._valid_data()
        data["age"] = True
        errors = self.validator.validate(data, self.schema)
        assert any(e.field == "age" for e in errors)

    def test_float_accepts_int(self):
        data = self._valid_data()
        data["score"] = 9  # int accepted for float
        errors = self.validator.validate(data, self.schema)
        assert not any(e.field == "score" for e in errors)

    def test_float_rejects_bool(self):
        data = self._valid_data()
        data["score"] = True
        errors = self.validator.validate(data, self.schema)
        assert any(e.field == "score" for e in errors)

    def test_wrong_type_boolean(self):
        data = self._valid_data()
        data["active"] = 1  # int, not bool
        errors = self.validator.validate(data, self.schema)
        assert any(e.field == "active" for e in errors)

    def test_wrong_type_array(self):
        data = self._valid_data()
        data["tags"] = {"a": 1}
        errors = self.validator.validate(data, self.schema)
        assert any(e.field == "tags" for e in errors)

    def test_wrong_type_object(self):
        data = self._valid_data()
        data["meta"] = [1, 2]
        errors = self.validator.validate(data, self.schema)
        assert any(e.field == "meta" for e in errors)

    def test_multiple_errors(self):
        data = {"bio": None}  # missing all required: name, age, score, active, tags, meta
        errors = self.validator.validate(data, self.schema)
        missing = [e.field for e in errors]
        for required_field in ("name", "age", "score", "active", "tags", "meta"):
            assert required_field in missing

    def test_error_has_value(self):
        data = self._valid_data()
        data["name"] = 999
        errors = self.validator.validate(data, self.schema)
        err = next(e for e in errors if e.field == "name")
        assert err.value == 999

    def test_empty_schema_no_errors(self):
        schema = Schema(name="Empty", version=SchemaVersion(1, 0, 0), fields=[])
        errors = self.validator.validate({"anything": "goes"}, schema)
        assert errors == []


# ---------------------------------------------------------------------------
# SchemaRegistry
# ---------------------------------------------------------------------------

def make_reg() -> SchemaRegistry:
    return SchemaRegistry()  # :memory:


def make_simple_schema(name: str = "MySchema", version: str = "1.0.0") -> Schema:
    return Schema(
        name=name,
        version=SchemaVersion.parse(version),
        fields=[FieldDef("id", "integer"), FieldDef("label", "string")],
        description=f"Schema {name} v{version}",
    )


class TestSchemaRegistryBasic:
    def setup_method(self):
        self.reg = make_reg()

    def test_register_and_get(self):
        s = make_simple_schema()
        self.reg.register(s)
        retrieved = self.reg.get(s.schema_id)
        assert retrieved is not None
        assert retrieved.schema_id == s.schema_id

    def test_get_nonexistent_returns_none(self):
        assert self.reg.get("doesnotexist") is None

    def test_register_preserves_fields(self):
        s = make_simple_schema()
        self.reg.register(s)
        retrieved = self.reg.get(s.schema_id)
        assert retrieved.field_names() == ["id", "label"]

    def test_register_preserves_version(self):
        s = make_simple_schema(version="2.3.4")
        self.reg.register(s)
        retrieved = self.reg.get(s.schema_id)
        assert retrieved.version == SchemaVersion(2, 3, 4)

    def test_register_preserves_description(self):
        s = make_simple_schema()
        self.reg.register(s)
        retrieved = self.reg.get(s.schema_id)
        assert retrieved.description == s.description

    def test_register_preserves_created_ts(self):
        s = make_simple_schema()
        self.reg.register(s)
        retrieved = self.reg.get(s.schema_id)
        assert abs(retrieved.created_ts - s.created_ts) < 0.001


class TestSchemaRegistryFind:
    def setup_method(self):
        self.reg = make_reg()

    def test_find_by_name(self):
        s = make_simple_schema(name="Alpha")
        self.reg.register(s)
        found = self.reg.find("Alpha")
        assert found is not None
        assert found.name == "Alpha"

    def test_find_by_name_and_version(self):
        s = make_simple_schema(name="Beta", version="2.0.0")
        self.reg.register(s)
        found = self.reg.find("Beta", "2.0.0")
        assert found is not None
        assert found.version == SchemaVersion(2, 0, 0)

    def test_find_wrong_version_returns_none(self):
        s = make_simple_schema(name="Gamma", version="1.0.0")
        self.reg.register(s)
        assert self.reg.find("Gamma", "9.9.9") is None

    def test_find_nonexistent_name_returns_none(self):
        assert self.reg.find("NoSuchSchema") is None


class TestSchemaRegistryList:
    def setup_method(self):
        self.reg = make_reg()

    def test_list_empty(self):
        assert self.reg.list_schemas() == []

    def test_list_all(self):
        s1 = make_simple_schema("A", "1.0.0")
        s2 = make_simple_schema("B", "2.0.0")
        self.reg.register(s1)
        self.reg.register(s2)
        schemas = self.reg.list_schemas()
        assert len(schemas) == 2

    def test_list_versions_empty(self):
        assert self.reg.list_versions("NoSuchSchema") == []

    def test_list_versions_multiple(self):
        for v in ("1.0.0", "1.1.0", "2.0.0"):
            self.reg.register(make_simple_schema("Versioned", v))
        versions = self.reg.list_versions("Versioned")
        assert len(versions) == 3
        assert SchemaVersion(1, 0, 0) in versions
        assert SchemaVersion(1, 1, 0) in versions
        assert SchemaVersion(2, 0, 0) in versions

    def test_list_versions_sorted(self):
        for v in ("2.0.0", "1.0.0", "1.1.0"):
            self.reg.register(make_simple_schema("SortTest", v))
        versions = self.reg.list_versions("SortTest")
        assert versions == sorted(versions)


class TestSchemaRegistryDelete:
    def setup_method(self):
        self.reg = make_reg()

    def test_delete_existing(self):
        s = make_simple_schema()
        self.reg.register(s)
        result = self.reg.delete(s.schema_id)
        assert result is True
        assert self.reg.get(s.schema_id) is None

    def test_delete_nonexistent_returns_false(self):
        assert self.reg.delete("ghost") is False

    def test_delete_reduces_list(self):
        s1 = make_simple_schema("X", "1.0.0")
        s2 = make_simple_schema("Y", "1.0.0")
        self.reg.register(s1)
        self.reg.register(s2)
        self.reg.delete(s1.schema_id)
        schemas = self.reg.list_schemas()
        assert len(schemas) == 1
        assert schemas[0].name == "Y"


class TestSchemaRegistryLatest:
    def setup_method(self):
        self.reg = make_reg()

    def test_latest_single_version(self):
        s = make_simple_schema("Single", "1.0.0")
        self.reg.register(s)
        latest = self.reg.latest("Single")
        assert latest is not None
        assert latest.version == SchemaVersion(1, 0, 0)

    def test_latest_multiple_versions(self):
        for v in ("1.0.0", "1.5.0", "2.0.0", "1.9.9"):
            self.reg.register(make_simple_schema("Multi", v))
        latest = self.reg.latest("Multi")
        assert latest is not None
        assert latest.version == SchemaVersion(2, 0, 0)

    def test_latest_nonexistent_returns_none(self):
        assert self.reg.latest("GhostSchema") is None

    def test_latest_after_delete(self):
        s1 = make_simple_schema("Del", "1.0.0")
        s2 = make_simple_schema("Del", "2.0.0")
        self.reg.register(s1)
        self.reg.register(s2)
        self.reg.delete(s2.schema_id)
        latest = self.reg.latest("Del")
        assert latest is not None
        assert latest.version == SchemaVersion(1, 0, 0)

    def test_register_replace(self):
        s = make_simple_schema("Replace", "1.0.0")
        self.reg.register(s)
        # Register again with same ID (replace)
        self.reg.register(s)
        schemas = self.reg.list_schemas()
        assert len(schemas) == 1
