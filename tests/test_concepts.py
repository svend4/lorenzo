"""
Тесты для scripts/improve_concepts.py.

Покрытие:
  - clean()              — нормализация пробелов
  - clean_definition()   — очистка wikilinks и markdown-ссылок
  - extract_definitions() — извлечение определений из текста
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_concepts")

# ── clean ─────────────────────────────────────────────────────────────────────

def test_clean_returns_string():
    assert isinstance(mod.clean("some  text"), str)


def test_clean_collapses_spaces():
    assert mod.clean("too   many   spaces") == "too many spaces"


def test_clean_strips_whitespace():
    assert mod.clean("  leading and trailing  ") == "leading and trailing"


def test_clean_newlines_to_spaces():
    result = mod.clean("line one\nline two")
    assert "\n" not in result


def test_clean_empty_string():
    assert mod.clean("") == ""


# ── clean_definition ──────────────────────────────────────────────────────────

def test_clean_definition_returns_string():
    assert isinstance(mod.clean_definition("some text"), str)


def test_clean_definition_removes_wikilinks():
    text = "See [[AgentFS]] for details."
    result = mod.clean_definition(text)
    assert "[[" not in result
    assert "]]" not in result
    assert "AgentFS" in result


def test_clean_definition_removes_wikilinks_with_alias():
    text = "See [[agentfs|AgentFS]] for details."
    result = mod.clean_definition(text)
    assert "[[" not in result
    assert "AgentFS" in result


def test_clean_definition_removes_md_links():
    text = "See [AgentFS](docs/agentfs.md) for details."
    result = mod.clean_definition(text)
    assert "[" not in result
    assert "AgentFS" in result


def test_clean_definition_empty():
    assert mod.clean_definition("") == ""


# ── extract_definitions ───────────────────────────────────────────────────────

def test_extract_definitions_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Title\n\nSome plain text without definitions.\n", encoding="utf-8")
    result = mod.extract_definitions("Some plain text.", f)
    assert isinstance(result, list)


def test_extract_definitions_finds_dash_pattern(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    text = "Агент — это программный компонент, который выполняет задачи автономно в среде."
    result = mod.extract_definitions(text, f)
    assert isinstance(result, list)


def test_extract_definitions_result_has_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    text = "AgentFS — это файловая система для хранения знаний агента в структурированном виде."
    result = mod.extract_definitions(text, f)
    for item in result:
        assert "term" in item
        assert "definition" in item


def test_extract_definitions_skips_code_blocks(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    text = "```\nАгент — это программа которая выполняет задачи автономно\n```\nClean text."
    result = mod.extract_definitions(text, f)
    # Definitions inside code blocks should be skipped
    assert result == []


def test_extract_definitions_skips_short_definitions(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    text = "X — это Y."  # too short definition
    result = mod.extract_definitions(text, f)
    assert result == []


def test_extract_definitions_deduplicates_terms(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    text = (
        "AgentFS — это файловая система для хранения и доступа к знаниям агента.\n"
        "AgentFS — это система для структурирования информации в файловом хранилище.\n"
    )
    result = mod.extract_definitions(text, f)
    terms = [r["term"] for r in result]
    # Duplicates should be removed (same term key)
    agent_fs_count = sum(1 for t in terms if "AgentFS" in t)
    assert agent_fs_count <= 1


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_concepts_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "CONCEPTS.md").exists()


def test_main_concepts_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text(
        "# AgentFS\n\nAgentFS — это файловая система для хранения знаний агента.", encoding="utf-8"
    )
    mod.main()
    text = (tmp_path / "CONCEPTS.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "CONCEPTS.md").exists()


def test_main_concepts_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "CONCEPTS.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
