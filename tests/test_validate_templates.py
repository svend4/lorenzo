"""Тесты для improve_validate_templates.py."""
import json
import tempfile
from pathlib import Path

from improve_validate_templates import (
    extract_frontmatter, parse_yaml_simple, validate_value, validate_doc,
    load_schemas,
)

import importlib as _importlib
import sys as _sys
_sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent / "scripts"))
_mod = _importlib.import_module("improve_validate_templates")


def test_parse_yaml_simple_scalars():
    text = """
name: hello
count: 42
enabled: true
empty: null
"""
    result = parse_yaml_simple(text)
    assert result['name'] == 'hello'
    assert result['count'] == 42
    assert result['enabled'] is True
    assert result['empty'] is None


def test_parse_yaml_simple_list_inline():
    text = "tags: [a, b, c]"
    result = parse_yaml_simple(text)
    assert result['tags'] == ['a', 'b', 'c']


def test_parse_yaml_simple_quoted():
    text = 'name: "hello world"\nver: "1.0"'
    result = parse_yaml_simple(text)
    assert result['name'] == 'hello world'
    assert result['ver'] == '1.0'


def test_extract_frontmatter():
    text = """---
title: Test
---

# Body
content
"""
    fm, body = extract_frontmatter(text)
    assert fm == {'title': 'Test'}
    assert '# Body' in body


def test_validate_value_const():
    errs = validate_value('template', 'rfc', {'const': 'rfc'})
    assert errs == []
    errs = validate_value('template', 'wrong', {'const': 'rfc'})
    assert len(errs) == 1


def test_validate_value_enum():
    errs = validate_value('status', 'draft', {'enum': ['draft', 'published']})
    assert errs == []
    errs = validate_value('status', 'unknown', {'enum': ['draft', 'published']})
    assert len(errs) == 1


def test_validate_value_pattern():
    errs = validate_value('id', 'RFC-1234', {'type': 'string', 'pattern': r'^RFC-\d{4}$'})
    assert errs == []
    errs = validate_value('id', 'bad', {'type': 'string', 'pattern': r'^RFC-\d{4}$'})
    assert len(errs) == 1


def test_validate_doc_valid():
    """Полный цикл: создать документ, провалидировать."""
    schemas = load_schemas()
    if 'research-note' not in schemas:
        return  # Если схем нет — скип

    valid_doc = """---
template: research-note
version: "1.0"
title: "Test research"
created: 2026-04-29
tags: [test]
---

# Test

## Контекст

текст

## Ключевые находки

- 1
- 2

## Источники

- src

## Открытые вопросы

- ?

## Следующие шаги

- [ ] step
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(valid_doc)
        path = Path(f.name)

    errs = validate_doc(path, schemas)
    path.unlink()
    assert errs == [], f"Unexpected errors: {errs}"


def test_validate_doc_missing_section():
    schemas = load_schemas()
    if 'research-note' not in schemas:
        return

    invalid_doc = """---
template: research-note
version: "1.0"
title: "Test"
created: 2026-04-29
tags: [test]
---

# Test

## Контекст
текст
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(invalid_doc)
        path = Path(f.name)

    errs = validate_doc(path, schemas)
    path.unlink()
    # Должны быть errors про missing sections
    assert any('секция' in e for e in errs)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_no_schemas_returns_one(tmp_path, monkeypatch):
    monkeypatch.setattr(_mod, "SCHEMAS_DIR", tmp_path / "nonexistent-schemas")
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    result = _mod.main()
    assert result == 1


def test_main_with_schemas_no_crash(tmp_path, monkeypatch):
    schemas_dir = tmp_path / "_schemas"
    schemas_dir.mkdir(parents=True)
    (schemas_dir / "note.json").write_text(
        '{"template":"note","properties":{"title":{"type":"string"}},"required":["title"]}',
        encoding="utf-8"
    )
    monkeypatch.setattr(_mod, "SCHEMAS_DIR", schemas_dir)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    _mod.main()


def test_main_report_creates_validation_md(tmp_path, monkeypatch):
    schemas_dir = tmp_path / "_schemas"
    schemas_dir.mkdir(parents=True)
    (schemas_dir / "note.json").write_text(
        '{"template":"note","properties":{"title":{"type":"string"}},"required":["title"]}',
        encoding="utf-8"
    )
    monkeypatch.setattr(_mod, "SCHEMAS_DIR", schemas_dir)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--report"])
    _mod.main()
    assert (tmp_path / "VALIDATION.md").exists()


# ── parse_yaml_simple extended ────────────────────────────────────────────────

def test_parse_yaml_simple_block_list():
    """Lines 52-54: block list items under a key."""
    text = "tags:\n- item1\n- item2"
    result = _mod.parse_yaml_simple(text)
    assert result['tags'] == ['item1', 'item2']


def test_parse_yaml_simple_empty_value():
    """Line 66-70: key with empty value sets up a list accumulator."""
    text = "key: \n- a\n- b"
    result = _mod.parse_yaml_simple(text)
    assert result['key'] == ['a', 'b']


def test_parse_yaml_simple_empty_array_literal():
    """Line 64/66: `key: []` → empty list."""
    text = "tags: []"
    result = _mod.parse_yaml_simple(text)
    assert result['tags'] == []


def test_parse_yaml_simple_inline_empty_brackets():
    """Line 71-75: inline array with only whitespace inside brackets."""
    text = "tags: [ ]"
    result = _mod.parse_yaml_simple(text)
    assert result['tags'] == []


def test_parse_yaml_simple_orphan_list_item():
    """Line 59: list item line when current_list is None is skipped."""
    text = "  - orphan\nname: hello"
    result = _mod.parse_yaml_simple(text)
    assert 'name' in result
    assert result['name'] == 'hello'
    # The orphan item is not stored
    assert len(result) == 1


# ── _coerce_scalar extended ───────────────────────────────────────────────────

def test_coerce_scalar_false():
    """Line 91: 'false' string → False bool."""
    result = _mod._coerce_scalar('false')
    assert result is False


def test_coerce_scalar_float():
    """Line 100: float string → float."""
    result = _mod._coerce_scalar('3.14')
    assert result == 3.14
    assert isinstance(result, float)


# ── extract_frontmatter extended ──────────────────────────────────────────────

def test_extract_frontmatter_no_frontmatter():
    """Line 107: file with no frontmatter returns (None, text)."""
    text = "# Just a heading\n\nSome content."
    fm, body = _mod.extract_frontmatter(text)
    assert fm is None
    assert body == text


def test_extract_frontmatter_parse_exception(monkeypatch):
    """Lines 110-111: if parse_yaml_simple raises, return (None, text)."""
    def raise_error(text):
        raise ValueError("parse error")
    monkeypatch.setattr(_mod, "parse_yaml_simple", raise_error)
    text = "---\nkey: value\n---\nbody"
    fm, body = _mod.extract_frontmatter(text)
    assert fm is None
    assert body == text


# ── load_schemas extended ─────────────────────────────────────────────────────

def test_load_schemas_invalid_json(tmp_path, monkeypatch):
    """Lines 128-129: schema file with invalid JSON triggers exception path."""
    schemas_dir = tmp_path / "_schemas"
    schemas_dir.mkdir(parents=True)
    (schemas_dir / "bad.json").write_text("this is not json", encoding="utf-8")
    monkeypatch.setattr(_mod, "SCHEMAS_DIR", schemas_dir)
    schemas = _mod.load_schemas()
    # Bad schema is skipped, result is empty
    assert schemas == {}


# ── validate_value extended ───────────────────────────────────────────────────

def test_validate_value_null_type_ok():
    """Lines 148-149: null type with None value → ok."""
    errs = _mod.validate_value('x', None, {'type': 'null'})
    assert errs == []


def test_validate_value_integer_type_ok():
    """Lines 154-155: integer type with int value → ok."""
    errs = _mod.validate_value('x', 42, {'type': 'integer'})
    assert errs == []


def test_validate_value_number_type_ok():
    """Lines 157-158: number type with float value → ok."""
    errs = _mod.validate_value('x', 3.14, {'type': 'number'})
    assert errs == []


def test_validate_value_boolean_type_ok():
    """Lines 160-161: boolean type with bool value → ok."""
    errs = _mod.validate_value('x', True, {'type': 'boolean'})
    assert errs == []


def test_validate_value_object_type_ok():
    """Lines 165-167: object type with dict value → ok."""
    errs = _mod.validate_value('x', {}, {'type': 'object'})
    assert errs == []


def test_validate_value_type_mismatch():
    """Lines 169-170: type mismatch → error returned."""
    errs = _mod.validate_value('x', 'str', {'type': 'integer'})
    assert len(errs) == 1
    assert 'str' in errs[0] or 'integer' in errs[0]


def test_validate_value_min_length_violation():
    """Line 173: minLength violation."""
    errs = _mod.validate_value('x', 'ab', {'type': 'string', 'minLength': 5})
    assert len(errs) == 1
    assert 'minLength' in errs[0]


def test_validate_value_format_date_violation():
    """Line 177: format=date violation."""
    errs = _mod.validate_value('x', 'not-a-date', {'type': 'string', 'format': 'date'})
    assert len(errs) == 1
    assert 'YYYY-MM-DD' in errs[0]


def test_validate_value_minimum_violation():
    """Lines 179-180: minimum violation."""
    errs = _mod.validate_value('x', 3, {'type': 'integer', 'minimum': 5})
    assert len(errs) == 1
    assert 'minimum' in errs[0]


def test_validate_value_maximum_violation():
    """Lines 181-182: maximum violation."""
    errs = _mod.validate_value('x', 10, {'type': 'integer', 'maximum': 5})
    assert len(errs) == 1
    assert 'maximum' in errs[0]


def test_validate_value_min_items_violation():
    """Line 185: minItems violation."""
    errs = _mod.validate_value('x', [], {'type': 'array', 'minItems': 1})
    assert len(errs) == 1
    assert 'minItems' in errs[0]


def test_validate_value_items_validation():
    """Lines 186-188: items validation — wrong type in array."""
    errs = _mod.validate_value('x', ['a'], {'type': 'array', 'items': {'type': 'integer'}})
    assert len(errs) == 1
    assert 'x[0]' in errs[0]


# ── validate_doc extended ─────────────────────────────────────────────────────

def _make_schema(tmp_path, name="note", required=None, properties=None, required_sections=None):
    schemas_dir = tmp_path / "_schemas"
    schemas_dir.mkdir(parents=True, exist_ok=True)
    schema = {"template": name}
    if required is not None:
        schema["required"] = required
    if properties is not None:
        schema["properties"] = properties
    if required_sections is not None:
        schema["required_sections"] = required_sections
    (schemas_dir / f"{name}.json").write_text(json.dumps(schema), encoding="utf-8")
    return {name: schema}


def test_validate_doc_no_frontmatter(tmp_path):
    """Line 196: file without frontmatter → empty errors list."""
    md = tmp_path / "plain.md"
    md.write_text("# No frontmatter here\n\ncontent", encoding="utf-8")
    schemas = _make_schema(tmp_path)
    errs = _mod.validate_doc(md, schemas)
    assert errs == []


def test_validate_doc_no_template_field(tmp_path):
    """Line 200: frontmatter without 'template' field → error."""
    md = tmp_path / "no_tmpl.md"
    md.write_text("---\ntitle: hello\n---\nbody", encoding="utf-8")
    schemas = _make_schema(tmp_path)
    errs = _mod.validate_doc(md, schemas)
    assert len(errs) == 1
    assert 'template' in errs[0]


def test_validate_doc_unknown_template(tmp_path):
    """Line 202: frontmatter with unknown template → error."""
    md = tmp_path / "unknown.md"
    md.write_text("---\ntemplate: ghost\n---\nbody", encoding="utf-8")
    schemas = _make_schema(tmp_path)
    errs = _mod.validate_doc(md, schemas)
    assert len(errs) == 1
    assert 'ghost' in errs[0]


def test_validate_doc_missing_required_field(tmp_path):
    """Line 210: missing required field → error."""
    schemas = _make_schema(tmp_path, required=["title"], properties={"title": {"type": "string"}})
    md = tmp_path / "missing.md"
    md.write_text("---\ntemplate: note\n---\nbody", encoding="utf-8")
    errs = _mod.validate_doc(md, schemas)
    assert any('title' in e for e in errs)


def test_validate_doc_additional_field_no_schema(tmp_path):
    """Line 216: field present in frontmatter but not in properties is skipped."""
    schemas = _make_schema(tmp_path, properties={"title": {"type": "string"}})
    md = tmp_path / "extra.md"
    md.write_text("---\ntemplate: note\ntitle: hello\nextra_field: value\n---\nbody", encoding="utf-8")
    errs = _mod.validate_doc(md, schemas)
    assert errs == []


# ── main() extended ───────────────────────────────────────────────────────────

def _setup_schemas_dir(tmp_path, name="note", required=None, properties=None, required_sections=None):
    schemas_dir = tmp_path / "_schemas"
    schemas_dir.mkdir(parents=True, exist_ok=True)
    schema = {"template": name}
    if required is not None:
        schema["required"] = required
    if properties is not None:
        schema["properties"] = properties
    if required_sections is not None:
        schema["required_sections"] = required_sections
    (schemas_dir / f"{name}.json").write_text(json.dumps(schema), encoding="utf-8")
    return schemas_dir


def test_main_section_flag(tmp_path, monkeypatch):
    """Lines 236-238: --section flag parses and uses subdirectory."""
    schemas_dir = _setup_schemas_dir(tmp_path)
    sub = tmp_path / "mysection"
    sub.mkdir()
    (sub / "doc.md").write_text("---\ntemplate: note\n---\nbody", encoding="utf-8")
    monkeypatch.setattr(_mod, "SCHEMAS_DIR", schemas_dir)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--section", str(sub)])
    result = _mod.main()
    assert result == 0


def test_main_file_flag(tmp_path, monkeypatch):
    """Lines 240-242, 251: --file flag processes single file."""
    schemas_dir = _setup_schemas_dir(tmp_path)
    md = tmp_path / "single.md"
    md.write_text("---\ntemplate: note\n---\nbody", encoding="utf-8")
    monkeypatch.setattr(_mod, "SCHEMAS_DIR", schemas_dir)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--file", str(md)])
    result = _mod.main()
    assert result == 0


def test_main_processes_files_with_template(tmp_path, monkeypatch):
    """Lines 262-277: files with template frontmatter increment total counter."""
    schemas_dir = _setup_schemas_dir(tmp_path, required=["title"], properties={"title": {"type": "string"}})
    md = tmp_path / "valid.md"
    md.write_text("---\ntemplate: note\ntitle: Hello\n---\nbody", encoding="utf-8")
    monkeypatch.setattr(_mod, "SCHEMAS_DIR", schemas_dir)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    result = _mod.main()
    assert result == 0


def test_main_files_with_errors_printed(tmp_path, monkeypatch, capsys):
    """Lines 283-286: files with errors are printed."""
    schemas_dir = _setup_schemas_dir(tmp_path, required=["title"], properties={"title": {"type": "string"}})
    md = tmp_path / "broken.md"
    # Missing required title field
    md.write_text("---\ntemplate: note\n---\nbody", encoding="utf-8")
    monkeypatch.setattr(_mod, "SCHEMAS_DIR", schemas_dir)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    result = _mod.main()
    out = capsys.readouterr().out
    assert 'title' in out
    assert result == 0  # no --strict


def test_main_report_with_errors(tmp_path, monkeypatch):
    """Lines 296-301: report includes errors section when there are errors."""
    schemas_dir = _setup_schemas_dir(tmp_path, required=["title"], properties={"title": {"type": "string"}})
    md = tmp_path / "broken.md"
    md.write_text("---\ntemplate: note\n---\nbody", encoding="utf-8")
    monkeypatch.setattr(_mod, "SCHEMAS_DIR", schemas_dir)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--report"])
    _mod.main()
    report_text = (tmp_path / "VALIDATION.md").read_text(encoding="utf-8")
    assert "Ошибки по файлам" in report_text


def test_main_strict_with_errors_returns_one(tmp_path, monkeypatch):
    """Line 312: --strict with errors → return 1."""
    schemas_dir = _setup_schemas_dir(tmp_path, required=["title"], properties={"title": {"type": "string"}})
    md = tmp_path / "broken.md"
    md.write_text("---\ntemplate: note\n---\nbody", encoding="utf-8")
    monkeypatch.setattr(_mod, "SCHEMAS_DIR", schemas_dir)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--strict"])
    result = _mod.main()
    assert result == 1
