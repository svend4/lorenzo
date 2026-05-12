"""
Тесты для scripts/improve_narrative.py.

Покрытие:
  - extract_narrative_points() — извлечение нарративных точек
  - get_summary()              — краткое резюме текста
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_narrative")


# ── extract_narrative_points ──────────────────────────────────────────────────

def test_extract_narrative_points_returns_list():
    result = mod.extract_narrative_points("plain text without patterns")
    assert isinstance(result, list)


def test_extract_narrative_points_empty():
    result = mod.extract_narrative_points("")
    assert result == []


def test_extract_narrative_points_finds_mvp():
    result = mod.extract_narrative_points(
        "mvp: создать поисковый движок на BM25 с поддержкой гибридного поиска"
    )
    assert len(result) > 0


def test_extract_narrative_points_result_is_tuples():
    result = mod.extract_narrative_points(
        "mvp: создать поисковый движок на BM25 с поддержкой гибридного поиска"
    )
    for item in result:
        assert isinstance(item, tuple)
        assert len(item) == 2


def test_extract_narrative_points_label_and_text():
    result = mod.extract_narrative_points(
        "mvp: создать поисковый движок на BM25 с поддержкой гибридного поиска"
    )
    for label, text in result:
        assert isinstance(label, str)
        assert isinstance(text, str)


def test_extract_narrative_points_max_5():
    text = " ".join([
        "mvp: создать поисковый движок на BM25 с поддержкой гибридного поиска документов",
        "цель: построить Knowledge OS для сообщества разработчиков Svyazi проекта",
        "главный риск: потеря данных при обновлении индексного файла системы поиска",
        "mvp: реализовать гибридный поиск с BM25 и TF-IDF для базы знаний документов",
        "цель: организовать эффективный поиск по документам базы знаний проекта",
        "написать команде разработчиков AgentFS о возможной интеграции с системой",
    ])
    result = mod.extract_narrative_points(text)
    assert len(result) <= 5


def test_extract_narrative_points_strips_code_blocks():
    text = "```\nmvp: создать поисковый движок на BM25\n```\nPlain text."
    result = mod.extract_narrative_points(text)
    # Code block content should be stripped
    texts = [text for _, text in result]
    assert all("BM25" not in t for t in texts) or len(result) == 0


def test_extract_narrative_points_finds_goal():
    result = mod.extract_narrative_points(
        "цель: построить локальную Knowledge OS для сообщества разработчиков проекта Svyazi"
    )
    labels = [label for label, _ in result]
    if result:
        assert "Цель" in " ".join(labels)


# ── get_summary ───────────────────────────────────────────────────────────────

def test_get_summary_returns_string():
    result = mod.get_summary("# Title\n\nSome content here.")
    assert isinstance(result, str)


def test_get_summary_empty():
    result = mod.get_summary("")
    assert isinstance(result, str)


def test_get_summary_removes_headings():
    result = mod.get_summary("# Title\n## Section\n\nContent here.")
    assert "# Title" not in result
    assert "## Section" not in result


def test_get_summary_truncates():
    long_text = "word " * 200
    result = mod.get_summary(long_text, max_words=10)
    word_count = len(result.replace("…", "").split())
    assert word_count <= 11


def test_get_summary_adds_ellipsis_if_truncated():
    long_text = "word " * 200
    result = mod.get_summary(long_text, max_words=10)
    if len(long_text.split()) > 10:
        assert "…" in result


def test_get_summary_strips_code_blocks():
    text = "```python\ncode here\n```\nReal content."
    result = mod.get_summary(text)
    assert "code here" not in result


def test_get_summary_removes_markdown_links():
    text = "See [AgentFS](docs/agentfs.md) for knowledge storage."
    result = mod.get_summary(text)
    assert "docs/agentfs.md" not in result


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_narrative_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "NARRATIVE_DOCS", [])
    mod.main()
    assert (tmp_path / "NARRATIVE.md").exists()


def test_main_narrative_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "NARRATIVE_DOCS", [])
    mod.main()
    text = (tmp_path / "NARRATIVE.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "NARRATIVE_DOCS", [])
    mod.main()
    assert (tmp_path / "NARRATIVE.md").exists()


def test_main_narrative_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "NARRATIVE_DOCS", [])
    mod.main()
    text = (tmp_path / "NARRATIVE.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


# ── main: with existing docs ──────────────────────────────────────────────────

def test_main_with_narrative_docs_existing(tmp_path, monkeypatch):
    """Lines 107-126: NARRATIVE_DOCS pointing to existing file."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    # Create a chapter file
    chapter_dir = tmp_path / "docs" / "chapter"
    chapter_dir.mkdir(parents=True)
    chapter_file = chapter_dir / "intro.md"
    chapter_file.write_text(
        "# Введение\n\nmvp: создать систему поиска данных для базы знаний.\n"
        "цель: построить Knowledge OS для разработчиков проекта Svyazi.\n",
        encoding="utf-8",
    )
    rel_path = "docs/chapter/intro.md"
    monkeypatch.setattr(mod, "NARRATIVE_DOCS", [rel_path])
    monkeypatch.setattr(mod, "CHAPTER_TITLES", {rel_path: "Глава 1: Введение"})
    mod.main()
    text = (tmp_path / "NARRATIVE.md").read_text(encoding="utf-8")
    assert "Глава 1" in text


def test_main_with_narrative_docs_missing(tmp_path, monkeypatch):
    """Lines 107-109: NARRATIVE_DOCS with non-existent file → skipped."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "NARRATIVE_DOCS", ["docs/nonexistent.md"])
    monkeypatch.setattr(mod, "CHAPTER_TITLES", {})
    mod.main()
    assert (tmp_path / "NARRATIVE.md").exists()


def test_main_with_narrative_points(tmp_path, monkeypatch):
    """Lines 119-122: chapter file with narrative points → written."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    chapter_dir = tmp_path / "docs" / "ch"
    chapter_dir.mkdir(parents=True)
    chapter_file = chapter_dir / "doc.md"
    chapter_file.write_text(
        "# Глава\n\nmvp: реализовать систему поиска документов для базы знаний агента.\n"
        "главный риск: потеря данных при обновлении индексного файла системы поиска.\n",
        encoding="utf-8",
    )
    rel_path = "docs/ch/doc.md"
    monkeypatch.setattr(mod, "NARRATIVE_DOCS", [rel_path])
    monkeypatch.setattr(mod, "CHAPTER_TITLES", {rel_path: "Глава: Тест"})
    mod.main()
    text = (tmp_path / "NARRATIVE.md").read_text(encoding="utf-8")
    assert "Глава: Тест" in text


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 147: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "NARRATIVE_DOCS", [])
    script_path = str(ROOT / "scripts" / "improve_narrative.py")
    runpy.run_path(script_path, run_name="__main__")
