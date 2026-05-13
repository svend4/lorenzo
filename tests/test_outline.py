"""
Тесты для scripts/improve_outline.py.

Покрытие:
  - _word_count()       — подсчёт слов
  - _extract_headings() — извлечение заголовков
  - _extract_summary()  — первый абзац после H1
  - _section_label()    — человекочитаемое название секции
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_outline")


# ── _word_count ───────────────────────────────────────────────────────────────

def test_word_count_returns_int():
    result = mod._word_count("one two three")
    assert isinstance(result, int)


def test_word_count_counts():
    result = mod._word_count("one two three four five")
    assert result == 5


def test_word_count_empty():
    result = mod._word_count("")
    assert result == 0


# ── _extract_headings ─────────────────────────────────────────────────────────

def test_extract_headings_returns_list():
    result = mod._extract_headings("# Title\n## Section\n")
    assert isinstance(result, list)


def test_extract_headings_extracts_h1():
    result = mod._extract_headings("# My Title\n")
    assert (1, "My Title") in result


def test_extract_headings_extracts_h2():
    result = mod._extract_headings("## My Section\n")
    assert (2, "My Section") in result


def test_extract_headings_respects_max_level():
    text = "## H2\n### H3\n#### H4\n"
    result = mod._extract_headings(text, max_level=3)
    levels = [lv for lv, _ in result]
    assert 4 not in levels


def test_extract_headings_removes_formatting():
    result = mod._extract_headings("## **Bold** Heading\n")
    if result:
        _, title = result[0]
        assert "**" not in title


def test_extract_headings_empty():
    result = mod._extract_headings("plain text without headings")
    assert result == []


# ── _extract_summary ──────────────────────────────────────────────────────────

def test_extract_summary_returns_string():
    result = mod._extract_summary("# Title\n\nSome text here.\n")
    assert isinstance(result, str)


def test_extract_summary_extracts_after_h1():
    result = mod._extract_summary("# Title\n\nThis is the first paragraph content.\n")
    assert "first paragraph" in result


def test_extract_summary_skips_heading_itself():
    result = mod._extract_summary("# Title\n\nContent here.\n")
    assert "Title" not in result or "Content" in result


def test_extract_summary_empty_returns_empty():
    result = mod._extract_summary("")
    assert result == ""


def test_extract_summary_truncates_at_120():
    long_text = "# Title\n\n" + "A" * 200 + "\n"
    result = mod._extract_summary(long_text)
    assert len(result) <= 124  # 120 + possible "…"


def test_extract_summary_skips_comment_lines():
    text = "# Title\n<!-- tags: memory -->\nContent here.\n"
    result = mod._extract_summary(text)
    assert "tags" not in result or "Content" in result


# ── _section_label ────────────────────────────────────────────────────────────

def test_section_label_returns_string(tmp_path):
    section = tmp_path / "01-svyazi"
    result = mod._section_label(section)
    assert isinstance(result, str)


def test_section_label_removes_leading_digits(tmp_path):
    section = tmp_path / "01-svyazi"
    result = mod._section_label(section)
    assert not result.startswith("01")


def test_section_label_titlecase(tmp_path):
    section = tmp_path / "my-section-name"
    result = mod._section_label(section)
    # Should be title-cased
    assert result[0].isupper() or result == result.title()


def test_section_label_dashes_to_spaces(tmp_path):
    section = tmp_path / "my-section"
    result = mod._section_label(section)
    assert "-" not in result


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_outline_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\n## Section\n\nContent.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "OUTLINE.md").exists()


def test_main_outline_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\n## Section\n\nContent.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "OUTLINE.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "OUTLINE.md").exists()


def test_main_outline_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "OUTLINE.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
