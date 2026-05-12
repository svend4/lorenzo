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


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_no_schemas_returns_one(tmp_path, monkeypatch):
    import importlib as _il
    import sys as _sys
    vt = _il.import_module("improve_validate_templates")
    monkeypatch.setattr(vt, "SCHEMAS_DIR", tmp_path / "nonexistent-schemas")
    monkeypatch.setattr(vt, "DOCS", tmp_path)
    monkeypatch.setattr(vt, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--all", "--dry-run"])
    result = mod.main()
    assert result == 1


def test_main_no_template_arg_returns_one(tmp_path, monkeypatch):
    import importlib as _il
    vt = _il.import_module("improve_validate_templates")
    schemas_dir = tmp_path / "_schemas"
    schemas_dir.mkdir(parents=True)
    (schemas_dir / "note.json").write_text(
        '{"template":"note","properties":{"title":{"type":"string"}},"required":["title"]}',
        encoding="utf-8"
    )
    monkeypatch.setattr(vt, "SCHEMAS_DIR", schemas_dir)
    monkeypatch.setattr(vt, "DOCS", tmp_path)
    monkeypatch.setattr(vt, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--dry-run"])
    result = mod.main()
    assert result == 1


def test_default_for_type_string():
    result = mod.default_for_type({"type": "string"})
    assert result == ""


def test_default_for_type_integer():
    result = mod.default_for_type({"type": "integer"})
    assert isinstance(result, int)


def test_default_for_type_array():
    result = mod.default_for_type({"type": "array"})
    assert result == []


def test_default_for_type_boolean():
    result = mod.default_for_type({"type": "boolean"})
    assert result is False


def test_default_for_type_enum():
    result = mod.default_for_type({"enum": ["draft", "published"]})
    assert result == "draft"


def test_default_for_type_date():
    result = mod.default_for_type({"type": "string", "format": "date"})
    assert isinstance(result, str)
    assert len(result) == 10  # YYYY-MM-DD


def test_suggest_migrations_missing_required(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("---\ntitle: Test\n---\n\nContent.", encoding="utf-8")
    schema = {
        "properties": {"title": {"type": "string"}, "status": {"type": "string"}},
        "required": ["title", "status"],
    }
    result = mod.suggest_migrations(f, schema)
    add_ops = [s for s in result if s["type"] == "add" and s["field"] == "status"]
    assert len(add_ops) == 1


def test_suggest_migrations_no_frontmatter(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nNo frontmatter.", encoding="utf-8")
    result = mod.suggest_migrations(f, {})
    assert result == []


# ── find_docs_with_template ────────────────────────────────────────────────────

def test_find_docs_with_template_finds_match(tmp_path, monkeypatch):
    """Lines 29-39: finds docs with matching template frontmatter."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    doc = tmp_path / "doc.md"
    doc.write_text("---\ntemplate: contact-outreach\ntitle: Test\n---\n\nContent.", encoding="utf-8")
    result = mod.find_docs_with_template("contact-outreach")
    assert len(result) >= 1


def test_find_docs_with_template_skips_no_match(tmp_path, monkeypatch):
    """Lines 37-38: docs without matching template are skipped."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    doc = tmp_path / "doc.md"
    doc.write_text("---\ntemplate: other-template\n---\n\nContent.", encoding="utf-8")
    result = mod.find_docs_with_template("contact-outreach")
    assert result == []


def test_find_docs_with_template_skips_schemas_dir(tmp_path, monkeypatch):
    """Lines 32-34: docs in _schemas dir are skipped."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    schemas_dir = tmp_path / "_schemas"
    schemas_dir.mkdir()
    doc = schemas_dir / "doc.md"
    doc.write_text("---\ntemplate: contact-outreach\n---\n\nContent.", encoding="utf-8")
    result = mod.find_docs_with_template("contact-outreach")
    assert doc not in result


# ── apply_migrations ───────────────────────────────────────────────────────────

def test_apply_migrations_add_field(tmp_path):
    """Lines 116-136: apply_migrations adds missing field."""
    f = tmp_path / "doc.md"
    f.write_text("---\ntitle: My Doc\n---\n\nContent.", encoding="utf-8")
    suggestions = [{"type": "add", "field": "status", "value": "draft"}]
    result = mod.apply_migrations(f, suggestions)
    assert "status: draft" in result


def test_apply_migrations_remove_field(tmp_path):
    """Lines 127-128: apply_migrations removes extra field."""
    f = tmp_path / "doc.md"
    f.write_text("---\ntitle: My Doc\nlegacy_field: old_value\n---\n\nContent.", encoding="utf-8")
    suggestions = [{"type": "remove", "field": "legacy_field"}]
    result = mod.apply_migrations(f, suggestions)
    assert "legacy_field" not in result


def test_apply_migrations_fix_enum(tmp_path):
    """Lines 128-134: apply_migrations fixes invalid enum value."""
    f = tmp_path / "doc.md"
    f.write_text("---\nstatus: unknown_val\n---\n\nContent.", encoding="utf-8")
    suggestions = [{"type": "fix_enum", "field": "status",
                    "value": "unknown_val", "allowed": ["draft", "published"]}]
    result = mod.apply_migrations(f, suggestions)
    assert "status: draft" in result


def test_apply_migrations_no_frontmatter(tmp_path):
    """Line 119: no frontmatter → return unchanged text."""
    f = tmp_path / "doc.md"
    original = "# Title\n\nNo frontmatter."
    f.write_text(original, encoding="utf-8")
    result = mod.apply_migrations(f, [{"type": "add", "field": "status", "value": "draft"}])
    assert result == original


def test_to_yaml_value_numeric_string():
    """Line 149-151: string matching '-?\\d+' pattern → quoted."""
    result = mod._to_yaml_value("-123")
    assert result == '"-123"'


# ── main: --template with schemas ─────────────────────────────────────────────

def _make_schemas(schemas_dir: Path, template_name: str = "note") -> None:
    schemas_dir.mkdir(parents=True, exist_ok=True)
    (schemas_dir / f"{template_name}.json").write_text(
        f'{{"template":"{template_name}","properties":{{"title":{{"type":"string"}},'
        f'"status":{{"enum":["draft","published"]}}}},"required":["title","status"]}}',
        encoding="utf-8"
    )


def test_main_template_no_matching_docs(tmp_path, monkeypatch):
    """Lines 162-165, 187: template found but no docs → prints and continues."""
    import importlib as _il
    vt = _il.import_module("improve_validate_templates")
    schemas_dir = tmp_path / "_schemas"
    _make_schemas(schemas_dir)
    monkeypatch.setattr(vt, "SCHEMAS_DIR", schemas_dir)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--template", "note", "--dry-run"])
    result = mod.main()
    assert result == 0


def test_main_template_with_docs_needing_migration(tmp_path, monkeypatch):
    """Lines 188-207: template with docs that need migration → print suggestions."""
    import importlib as _il
    vt = _il.import_module("improve_validate_templates")
    schemas_dir = tmp_path / "_schemas"
    _make_schemas(schemas_dir)
    monkeypatch.setattr(vt, "SCHEMAS_DIR", schemas_dir)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    doc = tmp_path / "doc.md"
    doc.write_text("---\ntemplate: note\ntitle: Test\n---\n\nContent.", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["prog", "--template", "note", "--dry-run"])
    result = mod.main()
    assert result == 0


def test_main_template_apply(tmp_path, monkeypatch, capsys):
    """Lines 205-207: --apply writes changes to file."""
    import importlib as _il
    vt = _il.import_module("improve_validate_templates")
    schemas_dir = tmp_path / "_schemas"
    _make_schemas(schemas_dir)
    monkeypatch.setattr(vt, "SCHEMAS_DIR", schemas_dir)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    doc = tmp_path / "doc.md"
    doc.write_text("---\ntemplate: note\ntitle: Test\n---\n\nContent.", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["prog", "--template", "note", "--apply"])
    result = mod.main()
    assert result == 0
    content = doc.read_text(encoding="utf-8")
    assert "status:" in content


def test_main_unknown_schema_warns(tmp_path, monkeypatch, capsys):
    """Lines 180-183: template not in schemas → warning."""
    import importlib as _il
    vt = _il.import_module("improve_validate_templates")
    schemas_dir = tmp_path / "_schemas"
    _make_schemas(schemas_dir)
    monkeypatch.setattr(vt, "SCHEMAS_DIR", schemas_dir)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--template", "nonexistent_xyz", "--dry-run"])
    mod.main()
    out = capsys.readouterr().out
    assert "не найдена" in out or "nonexistent_xyz" in out


def test_main_all_flag(tmp_path, monkeypatch):
    """Lines 172: do_all=True processes all schemas."""
    import importlib as _il
    vt = _il.import_module("improve_validate_templates")
    schemas_dir = tmp_path / "_schemas"
    _make_schemas(schemas_dir)
    monkeypatch.setattr(vt, "SCHEMAS_DIR", schemas_dir)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--all", "--dry-run"])
    result = mod.main()
    assert result == 0


# ── __main__ block ─────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Lines 216, 219: __main__ block."""
    import runpy, importlib as _il
    vt = _il.import_module("improve_validate_templates")
    schemas_dir = tmp_path / "_schemas"
    _make_schemas(schemas_dir)
    monkeypatch.setattr(vt, "SCHEMAS_DIR", schemas_dir)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--all", "--dry-run"])
    script_path = str(ROOT / "scripts" / "improve_template_migrate.py")
    with pytest.raises(SystemExit):
        runpy.run_path(script_path, run_name="__main__")
