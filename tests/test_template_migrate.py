"""Tests for scripts/improve_template_migrate.py."""

import importlib
import sys
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_template_migrate")


def test_to_yaml_value_none():
    assert mod._to_yaml_value(None) == "null"


def test_to_yaml_value_bool_true():
    assert mod._to_yaml_value(True) == "true"


def test_to_yaml_value_bool_false():
    assert mod._to_yaml_value(False) == "false"


def test_to_yaml_value_int():
    assert mod._to_yaml_value(42) == "42"


def test_to_yaml_value_float():
    assert mod._to_yaml_value(3.14) == "3.14"


def test_to_yaml_value_empty_string():
    result = mod._to_yaml_value("")
    assert result == '""'


def test_to_yaml_value_simple_string():
    result = mod._to_yaml_value("hello")
    assert result == "hello"


def test_to_yaml_value_string_with_colon():
    result = mod._to_yaml_value("key: value")
    assert result.startswith('"')


def test_to_yaml_value_reserved_word():
    result = mod._to_yaml_value("null")
    assert result == '"null"'


def test_to_yaml_value_list():
    result = mod._to_yaml_value([1, 2])
    assert result == "[1, 2]"


def test_to_yaml_value_empty_list():
    result = mod._to_yaml_value([])
    assert result == "[]"


def test_default_for_type_enum():
    schema = {"enum": ["draft", "review", "published"]}
    result = mod.default_for_type(schema)
    assert result == "draft"


def test_default_for_type_const():
    schema = {"const": "project-component"}
    result = mod.default_for_type(schema)
    assert result == "project-component"


def test_default_for_type_string():
    schema = {"type": "string"}
    result = mod.default_for_type(schema)
    assert result == ""


def test_default_for_type_date_string():
    schema = {"type": "string", "format": "date"}
    result = mod.default_for_type(schema)
    assert result == date.today().isoformat()


def test_default_for_type_integer():
    schema = {"type": "integer"}
    result = mod.default_for_type(schema)
    assert result == 0


def test_default_for_type_integer_with_minimum():
    schema = {"type": "integer", "minimum": 5}
    result = mod.default_for_type(schema)
    assert result == 5


def test_default_for_type_array():
    schema = {"type": "array"}
    result = mod.default_for_type(schema)
    assert result == []


def test_default_for_type_object():
    schema = {"type": "object"}
    result = mod.default_for_type(schema)
    assert result == {}


def test_default_for_type_boolean():
    schema = {"type": "boolean"}
    result = mod.default_for_type(schema)
    assert result is False


def test_default_for_type_null():
    schema = {"type": "null"}
    result = mod.default_for_type(schema)
    assert result is None


def test_default_for_type_unknown():
    schema = {}
    result = mod.default_for_type(schema)
    assert result is None


def test_suggest_migrations_empty_frontmatter(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nNo frontmatter.", encoding="utf-8")
    schema = {"properties": {"title": {"type": "string"}}, "required": ["title"]}
    result = mod.suggest_migrations(f, schema)
    assert result == []


def test_suggest_migrations_missing_required(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("---\ntitle: My Doc\n---\n\nContent.", encoding="utf-8")
    schema = {
        "properties": {
            "title": {"type": "string"},
            "status": {"enum": ["draft", "published"]},
        },
        "required": ["title", "status"],
    }
    result = mod.suggest_migrations(f, schema)
    types = [s["type"] for s in result]
    assert "add" in types
    added = [s for s in result if s["type"] == "add"]
    assert any(s["field"] == "status" for s in added)


def test_suggest_migrations_unknown_field(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("---\ntitle: My Doc\nlegacy_field: value\n---\n\nContent.", encoding="utf-8")
    schema = {
        "properties": {"title": {"type": "string"}},
        "required": [],
    }
    result = mod.suggest_migrations(f, schema)
    removes = [s for s in result if s["type"] == "remove"]
    assert any(s["field"] == "legacy_field" for s in removes)


def test_suggest_migrations_invalid_enum(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("---\nstatus: unknown_value\n---\n\nContent.", encoding="utf-8")
    schema = {
        "properties": {"status": {"enum": ["draft", "published"]}},
        "required": [],
    }
    result = mod.suggest_migrations(f, schema)
    enum_fixes = [s for s in result if s["type"] == "fix_enum"]
    assert len(enum_fixes) == 1
    assert enum_fixes[0]["field"] == "status"
    assert enum_fixes[0]["allowed"] == ["draft", "published"]


def test_suggest_migrations_valid_doc(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("---\ntitle: My Doc\nstatus: draft\n---\n\nContent.", encoding="utf-8")
    schema = {
        "properties": {
            "title": {"type": "string"},
            "status": {"enum": ["draft", "published"]},
        },
        "required": ["title", "status"],
    }
    result = mod.suggest_migrations(f, schema)
    assert result == []
