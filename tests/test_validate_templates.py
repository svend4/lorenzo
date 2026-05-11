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
