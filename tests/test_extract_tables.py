"""
Тесты для scripts/improve_extract_tables.py.

Покрытие:
  - extract_tables()    — извлечение Markdown-таблиц из текста
  - get_table_context() — заголовок перед таблицей
  - count_cols()        — количество столбцов таблицы
  - rewrite_links()     — перезапись относительных ссылок
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_extract_tables")

# ── extract_tables ────────────────────────────────────────────────────────────

_SIMPLE_TABLE = "| Col1 | Col2 |\n|------|------|\n| A    | B    |"

def test_extract_tables_returns_list():
    result = mod.extract_tables(_SIMPLE_TABLE)
    assert isinstance(result, list)


def test_extract_tables_finds_one_table():
    result = mod.extract_tables(_SIMPLE_TABLE)
    assert len(result) == 1


def test_extract_tables_finds_multiple():
    text = (
        "# Section 1\n\n"
        "| A | B |\n|---|---|\n| 1 | 2 |\n\n"
        "Some text.\n\n"
        "| X | Y | Z |\n|---|---|---|\n| a | b | c |\n"
    )
    result = mod.extract_tables(text)
    assert len(result) == 2


def test_extract_tables_empty_text():
    assert mod.extract_tables("No tables here at all.") == []


def test_extract_tables_ignores_single_row():
    text = "| Header only |"
    result = mod.extract_tables(text)
    assert result == []


def test_extract_tables_preserves_content():
    result = mod.extract_tables(_SIMPLE_TABLE)
    assert "Col1" in result[0]
    assert "Col2" in result[0]


def test_extract_tables_table_starts_with_pipe():
    result = mod.extract_tables(_SIMPLE_TABLE)
    assert result[0].startswith("|")


def test_extract_tables_no_false_positives():
    text = "| header | only one row no separator |"
    result = mod.extract_tables(text)
    assert result == []

# ── get_table_context ─────────────────────────────────────────────────────────

def test_get_table_context_finds_preceding_heading():
    table = "| Col | Val |\n|-----|-----|\n| a   | b   |"
    text = "# Title\n\n## Section Header\n\nSome intro.\n\n" + table
    result = mod.get_table_context(text, table)
    assert "Section Header" in result


def test_get_table_context_returns_last_heading():
    table = "| C | V |\n|---|---|\n| 1 | 2 |"
    text = "# H1\n\n## H2\n\n### H3\n\n" + table
    result = mod.get_table_context(text, table)
    assert result == "H3"


def test_get_table_context_empty_when_no_heading():
    table = "| C | V |\n|---|---|\n| 1 | 2 |"
    text = "Just some text without headings.\n\n" + table
    result = mod.get_table_context(text, table)
    assert result == ""


def test_get_table_context_returns_string():
    result = mod.get_table_context("text", "table")
    assert isinstance(result, str)


def test_get_table_context_table_not_found():
    result = mod.get_table_context("text", "| x | y |\n|---|---|")
    assert result == ""

# ── count_cols ────────────────────────────────────────────────────────────────

def test_count_cols_two_columns():
    table = "| Col1 | Col2 |\n|------|------|\n| A | B |"
    assert mod.count_cols(table) == 2


def test_count_cols_three_columns():
    table = "| A | B | C |\n|---|---|---|\n| 1 | 2 | 3 |"
    assert mod.count_cols(table) == 3


def test_count_cols_five_columns():
    table = "| A | B | C | D | E |\n|---|---|---|---|---|\n| 1 | 2 | 3 | 4 | 5 |"
    assert mod.count_cols(table) == 5


def test_count_cols_returns_int():
    table = "| X | Y |\n|---|---|\n| 1 | 2 |"
    result = mod.count_cols(table)
    assert isinstance(result, int)

# ── rewrite_links ─────────────────────────────────────────────────────────────

def test_rewrite_links_preserves_http():
    table = "| [External](https://example.com) |"
    source = ROOT / "docs" / "file.md"
    result = mod.rewrite_links(table, source)
    assert "https://example.com" in result


def test_rewrite_links_preserves_anchors():
    table = "| [Anchor](#section) |"
    source = ROOT / "docs" / "file.md"
    result = mod.rewrite_links(table, source)
    assert "#section" in result


def test_rewrite_links_returns_string():
    table = "| text |"
    source = ROOT / "docs" / "file.md"
    result = mod.rewrite_links(table, source)
    assert isinstance(result, str)


def test_rewrite_links_no_links_unchanged():
    table = "| Col1 | Col2 |\n|------|------|\n| A    | B    |"
    source = ROOT / "docs" / "file.md"
    result = mod.rewrite_links(table, source)
    assert result == table


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_tables_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "TABLES.md").exists()


def test_main_tables_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text(
        "# Title\n\n| Col1 | Col2 |\n|------|------|\n| A | B |\n",
        encoding="utf-8"
    )
    mod.main()
    text = (tmp_path / "TABLES.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "TABLES.md").exists()


def test_main_tables_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "TABLES.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
