"""
Тесты для scripts/improve_scripts_catalog.py.

Покрытие:
  - extract_docstring() — извлечение module-level docstring через AST
  - extract_flags()     — поиск --flag флагов в docstring
  - extract_summary()   — первая строка docstring без имени скрипта
  - extract_description() — описание без первой строки и блока запуска
  - load_groups()       — парсинг improve_run_all.py для группировки скриптов
"""

import importlib
import sys
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_scripts_catalog")

# ── extract_docstring ─────────────────────────────────────────────────────────

def test_extract_docstring_returns_string(tmp_path):
    f = tmp_path / "script.py"
    f.write_text('"""Module docstring."""\n\ndef main(): pass\n', encoding="utf-8")
    result = mod.extract_docstring(f)
    assert isinstance(result, str)


def test_extract_docstring_extracts_content(tmp_path):
    f = tmp_path / "script.py"
    f.write_text('"""Hello world module."""\n', encoding="utf-8")
    result = mod.extract_docstring(f)
    assert "Hello world module" in result


def test_extract_docstring_no_docstring(tmp_path):
    f = tmp_path / "script.py"
    f.write_text("x = 1\n", encoding="utf-8")
    result = mod.extract_docstring(f)
    assert result == ""


def test_extract_docstring_multiline(tmp_path):
    f = tmp_path / "script.py"
    f.write_text('"""\nLine one.\nLine two.\n"""\n', encoding="utf-8")
    result = mod.extract_docstring(f)
    assert "Line one" in result
    assert "Line two" in result


def test_extract_docstring_missing_file(tmp_path):
    result = mod.extract_docstring(tmp_path / "missing.py")
    assert result == ""


def test_extract_docstring_syntax_error(tmp_path):
    f = tmp_path / "bad.py"
    f.write_text("def (broken\n", encoding="utf-8")
    result = mod.extract_docstring(f)
    assert result == ""


# ── extract_flags ─────────────────────────────────────────────────────────────

def test_extract_flags_returns_list():
    result = mod.extract_flags("Use --dry-run and --apply flags.")
    assert isinstance(result, list)


def test_extract_flags_finds_flags():
    result = mod.extract_flags("Use --dry-run and --apply flags.")
    assert "--dry-run" in result
    assert "--apply" in result


def test_extract_flags_empty_string():
    assert mod.extract_flags("") == []


def test_extract_flags_no_flags():
    assert mod.extract_flags("No flags here at all.") == []


def test_extract_flags_sorted():
    result = mod.extract_flags("--zebra --alpha --middle")
    assert result == sorted(result)


def test_extract_flags_deduplicates():
    result = mod.extract_flags("--dry-run first, --dry-run second")
    assert result.count("--dry-run") == 1


def test_extract_flags_complex_flag():
    result = mod.extract_flags("Use --min-mentions and --output-file here.")
    assert "--min-mentions" in result
    assert "--output-file" in result


# ── extract_summary ───────────────────────────────────────────────────────────

def test_extract_summary_returns_string():
    assert isinstance(mod.extract_summary("improve_x.py — description here."), str)


def test_extract_summary_strips_script_name():
    result = mod.extract_summary("improve_validate.py — валидация структуры.")
    assert "improve_validate.py" not in result
    assert "валидация" in result


def test_extract_summary_empty_docstring():
    assert mod.extract_summary("") == ""


def test_extract_summary_uses_first_line():
    doc = "First line here.\n\nMore details on second line."
    result = mod.extract_summary(doc)
    assert "First line" in result
    assert "More details" not in result


def test_extract_summary_dash_separator():
    result = mod.extract_summary("improve_foo.py - generates reports.")
    assert "generate" in result.lower() or "reports" in result.lower()


# ── extract_description ───────────────────────────────────────────────────────

def test_extract_description_returns_string():
    doc = "First line.\n\nThis is the description.\n\nЗапуск:\n    python script.py"
    result = mod.extract_description(doc)
    assert isinstance(result, str)


def test_extract_description_skips_first_line():
    doc = "First line.\n\nThis is the description."
    result = mod.extract_description(doc)
    assert "First line" not in result
    assert "description" in result


def test_extract_description_stops_before_run_block():
    doc = "First.\n\nDescription here.\n\nЗапуск:\n    python improve_x.py"
    result = mod.extract_description(doc)
    assert "Запуск" not in result
    assert "improve_x.py" not in result


def test_extract_description_empty_docstring():
    assert mod.extract_description("") == ""


def test_extract_description_skips_python_lines():
    doc = "First line.\n\npython improve_x.py --flag\nActual description."
    result = mod.extract_description(doc)
    assert "python improve_x" not in result


# ── load_groups ───────────────────────────────────────────────────────────────

def test_load_groups_returns_dict():
    result = mod.load_groups()
    assert isinstance(result, dict)


def test_load_groups_values_are_strings():
    result = mod.load_groups()
    for v in result.values():
        assert isinstance(v, str)


def test_load_groups_keys_are_script_names():
    result = mod.load_groups()
    for k in result.keys():
        assert k.startswith("improve_")
        assert k.endswith(".py")


def test_load_groups_non_empty():
    # improve_run_all.py exists and has groups
    result = mod.load_groups()
    assert len(result) > 0


def test_load_groups_missing_runner(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "SCRIPTS_DIR", tmp_path)
    result = mod.load_groups()
    assert result == {}


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_catalog_md(tmp_path, monkeypatch):
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "improve_test.py").write_text('"""Test script."""\n\ndef main():\n    pass\n', encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SCRIPTS_DIR", scripts_dir)
    mod.main()
    assert (tmp_path / "SCRIPTS_CATALOG.md").exists()


def test_main_catalog_has_content(tmp_path, monkeypatch):
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "improve_test.py").write_text('"""Test script."""\n', encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SCRIPTS_DIR", scripts_dir)
    mod.main()
    text = (tmp_path / "SCRIPTS_CATALOG.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_scripts_dir(tmp_path, monkeypatch):
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SCRIPTS_DIR", scripts_dir)
    mod.main()
    assert (tmp_path / "SCRIPTS_CATALOG.md").exists()
