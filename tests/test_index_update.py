"""
Тесты для scripts/improve_index_update.py.

Покрытие:
  - _clean_md()             — очистка markdown-разметки
  - _extract_summary_block() — извлечение <!-- summary --> блока
  - _extract_body()         — извлечение основного текста
  - _extract_content()      — формирование индексируемого контента
  - build_entry()           — построение записи индекса из файла
"""

import importlib
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_index_update")

# ── _clean_md ─────────────────────────────────────────────────────────────────

def test_clean_md_removes_code_blocks():
    text = "before\n```python\ncode here\n```\nafter"
    result = mod._clean_md(text)
    assert "code here" not in result
    assert "before" in result
    assert "after" in result


def test_clean_md_removes_html_comments():
    text = "text <!-- this is a comment --> more text"
    result = mod._clean_md(text)
    assert "this is a comment" not in result
    assert "text" in result


def test_clean_md_removes_toc_links():
    text = "## Title\n- [Section](#section-anchor)\n- [Other](#other)\nreal text"
    result = mod._clean_md(text)
    assert "#section-anchor" not in result
    assert "real text" in result


def test_clean_md_removes_markdown_chars():
    text = "**bold** _italic_ `code` [link](url) | table |"
    result = mod._clean_md(text)
    assert "**" not in result
    assert "_italic_" not in result
    assert "`code`" not in result


def test_clean_md_normalizes_whitespace():
    text = "word1    \n\n\n    word2\t\tword3"
    result = mod._clean_md(text)
    assert "  " not in result   # no double spaces
    assert "word1" in result
    assert "word3" in result


def test_clean_md_empty_string():
    assert mod._clean_md("") == ""

# ── _extract_summary_block ────────────────────────────────────────────────────

def test_extract_summary_block_finds_content():
    text = "# Title\n\n<!-- summary -->\n> Key summary content here.\n\n<!-- tags: foo -->"
    result = mod._extract_summary_block(text)
    assert "Key summary content here" in result


def test_extract_summary_block_empty_when_absent():
    text = "# Title\n\nNo summary block here at all."
    result = mod._extract_summary_block(text)
    assert result == ""


def test_extract_summary_block_strips_markdown():
    text = "<!-- summary -->\n> **Bold text** and _italic_.\n\n<!-- end -->"
    result = mod._extract_summary_block(text)
    assert "**" not in result
    assert "Bold text" in result


def test_extract_summary_block_stops_at_next_comment():
    text = "<!-- summary -->\nSummary here.\n<!-- tags: foo -->\nNot summary."
    result = mod._extract_summary_block(text)
    assert "Summary here" in result
    assert "Not summary" not in result

# ── _extract_body ─────────────────────────────────────────────────────────────

def test_extract_body_removes_autofill_blocks():
    text = "<!-- autofill-status -->\nautofill content\n## Real Section\nReal content"
    result = mod._extract_body(text)
    assert "autofill content" not in result


def test_extract_body_removes_summary_block():
    text = "<!-- summary -->\nSummary text.\n<!-- end -->\n## Content\nReal body here."
    result = mod._extract_body(text)
    assert "Summary text" not in result


def test_extract_body_keeps_real_content():
    text = "# Doc Title\n\n## Section\nThis is real content about agents.\n"
    result = mod._extract_body(text)
    assert "real content about agents" in result


def test_extract_body_removes_toc_links():
    text = "- [Introduction](#introduction)\n- [Details](#details)\n\nReal paragraph here."
    result = mod._extract_body(text)
    assert "#introduction" not in result
    assert "Real paragraph here" in result

# ── _extract_content ──────────────────────────────────────────────────────────

def test_extract_content_returns_string():
    text = "# Title\n\nSome content here about agents and memory."
    result = mod._extract_content(text)
    assert isinstance(result, str)


def test_extract_content_respects_max_chars():
    long_text = "word " * 1000
    result = mod._extract_content(long_text, max_chars=100)
    assert len(result) <= 100


def test_extract_content_prefers_summary_block():
    text = (
        "# Title\n\n"
        "<!-- summary -->\n> KEY TERM from summary block.\n\n<!-- tags: x -->\n\n"
        "## Section\nGeneric body text that is less relevant.\n"
    )
    result = mod._extract_content(text)
    assert "KEY TERM" in result


def test_extract_content_falls_back_to_body():
    text = "# Title\n\n## Section\nBody content about knowledge graphs and RAG."
    result = mod._extract_content(text)
    assert "knowledge graphs" in result or "Body content" in result

# ── build_entry ───────────────────────────────────────────────────────────────

@pytest.fixture
def tmp_doc(tmp_path):
    """Создаёт временный .md файл для тестирования build_entry."""
    doc = tmp_path / "docs" / "05-habr-projects" / "memory" / "test-project.md"
    doc.parent.mkdir(parents=True)
    doc.write_text(
        "---\ntitle: Test Project\nmaturity: beta\n---\n\n"
        "# Test Project\n\n"
        "<!-- summary -->\n> A test project for memory agents.\n\n<!-- tags: memory, test -->\n\n"
        "## Что это\n\nThis is a test memory project with consolidation.\n",
        encoding="utf-8",
    )
    # Temporarily patch ROOT in the module
    original_root = mod.ROOT
    mod.ROOT = tmp_path
    yield doc
    mod.ROOT = original_root


def test_build_entry_returns_dict(tmp_doc):
    entry = mod.build_entry(tmp_doc)
    assert isinstance(entry, dict)


def test_build_entry_has_required_keys(tmp_doc):
    entry = mod.build_entry(tmp_doc)
    for key in ("path", "title", "section", "tags", "summary", "words", "content", "updated"):
        assert key in entry, f"missing key: {key}"


def test_build_entry_extracts_h1_title(tmp_doc):
    entry = mod.build_entry(tmp_doc)
    assert entry["title"] == "Test Project"


def test_build_entry_detects_section(tmp_doc):
    entry = mod.build_entry(tmp_doc)
    assert entry["section"] == "05-habr-projects"


def test_build_entry_content_has_summary(tmp_doc):
    entry = mod.build_entry(tmp_doc)
    assert "memory agents" in entry["content"]


def test_build_entry_words_positive(tmp_doc):
    entry = mod.build_entry(tmp_doc)
    assert entry["words"] > 0


def test_build_entry_real_doc():
    """Тест на реальном файле из корпуса."""
    yodoca = ROOT / "docs" / "05-habr-projects" / "memory" / "yodoca.md"
    if not yodoca.exists():
        pytest.skip("yodoca.md not found")
    entry = mod.build_entry(yodoca)
    assert entry["title"]
    assert len(entry["content"]) > 50
    assert entry["section"] == "05-habr-projects"
    assert entry["words"] > 10
