"""Tests for scripts/improve_question_extractor.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_question_extractor")


def test_clean_returns_string():
    result = mod._clean("some text here")
    assert isinstance(result, str)


def test_clean_removes_code():
    result = mod._clean("Before\n```python\ncode\n```\nAfter")
    assert "code" not in result


def test_split_sentences_returns_list():
    text = "Как работает система поиска данных? Это хороший вопрос для анализа."
    result = mod._split_sentences(text)
    assert isinstance(result, list)


def test_split_sentences_filters_short():
    result = mod._split_sentences("Hi. OK.")
    assert all(len(s.split()) >= mod.MIN_WORDS for s in result)


def test_current_heading_returns_string():
    text = "# Title\n## Section\nsome content"
    result = mod._current_heading(text, len(text))
    assert isinstance(result, str)


def test_current_heading_finds_last_heading():
    text = "# Title\n## Section A\nfoo\n## Section B\nbar"
    result = mod._current_heading(text, len(text))
    assert "Section B" in result


def test_current_heading_empty():
    result = mod._current_heading("no headings here", 5)
    assert result == ""


def test_extract_from_file_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text(
        "# Title\n\nКак работает система поиска данных в проекте?\n"
        "Это хорошее решение для обработки запросов пользователей.\n",
        encoding="utf-8"
    )
    result = mod.extract_from_file(f)
    assert isinstance(result, list)


def test_extract_from_file_has_required_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text(
        "Как именно работает система поиска запросов данных?\n"
        "Это хорошее решение для анализа данных в системе.\n",
        encoding="utf-8"
    )
    result = mod.extract_from_file(f)
    for item in result:
        assert "types" in item
        assert "sentence" in item
        assert "source" in item


def test_extract_from_file_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "missing.md"
    result = mod.extract_from_file(f)
    assert result == []


def test_patterns_have_expected_types():
    assert "question" in mod.PATTERNS
    assert "hypothesis" in mod.PATTERNS
    assert "todo" in mod.PATTERNS
    assert "open" in mod.PATTERNS


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_questions_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    (tmp_path / "doc.md").write_text("# Title\n\nWhat is AgentFS?\n", encoding="utf-8")
    mod.main()
    assert (tmp_path / "QUESTIONS.md").exists()


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    assert (tmp_path / "QUESTIONS.md").exists()
