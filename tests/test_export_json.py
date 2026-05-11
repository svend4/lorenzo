"""
Тесты для scripts/improve_export_json.py.

Покрытие:
  - get_title()       — H1 из текста или fallback
  - get_summary()     — первый абзац без разметки, обрезка
  - get_tags()        — теги из HTML-комментария
  - get_h2_sections() — список H2 заголовков
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_export_json")

# ── get_title ─────────────────────────────────────────────────────────────────

def test_get_title_returns_string():
    result = mod.get_title("# My Title\n\nContent.", "fallback")
    assert isinstance(result, str)


def test_get_title_extracts_h1():
    result = mod.get_title("# My Title\n\nContent.", "fallback")
    assert result == "My Title"


def test_get_title_uses_fallback_when_no_h1():
    result = mod.get_title("## Section\n\nContent.", "default-name")
    assert result == "default-name"


def test_get_title_truncates_at_80():
    long_title = "A" * 100
    text = f"# {long_title}\n\nContent."
    result = mod.get_title(text, "fallback")
    assert len(result) <= 80


def test_get_title_strips_whitespace():
    result = mod.get_title("#   Title with spaces   \n\nContent.", "fallback")
    assert result == "Title with spaces"


def test_get_title_empty_text():
    result = mod.get_title("", "my-fallback")
    assert result == "my-fallback"


# ── get_summary ───────────────────────────────────────────────────────────────

def test_get_summary_returns_string():
    result = mod.get_summary("# Title\n\nSome content here.")
    assert isinstance(result, str)


def test_get_summary_from_comment():
    text = "<!-- summary -->Custom summary text.<!-- end -->"
    result = mod.get_summary(text)
    assert "Custom summary text" in result


def test_get_summary_max_200_chars():
    long_text = "word " * 200
    result = mod.get_summary(long_text)
    assert len(result) <= 200


def test_get_summary_removes_headings():
    text = "# Title\n\nActual content here."
    result = mod.get_summary(text)
    # Heading markers should be stripped
    assert "#" not in result


def test_get_summary_removes_markdown_formatting():
    text = "**Bold** and _italic_ and `code` text."
    result = mod.get_summary(text)
    assert "**" not in result


def test_get_summary_empty_text():
    result = mod.get_summary("")
    assert isinstance(result, str)


# ── get_tags ──────────────────────────────────────────────────────────────────

def test_get_tags_returns_list():
    result = mod.get_tags("Some text.")
    assert isinstance(result, list)


def test_get_tags_extracts_from_comment():
    text = "<!-- tags: memory, agent, mcp -->Content."
    result = mod.get_tags(text)
    assert "memory" in result
    assert "agent" in result
    assert "mcp" in result


def test_get_tags_empty_when_no_comment():
    result = mod.get_tags("# Title\n\nNo tags here.")
    assert result == []


def test_get_tags_strips_whitespace():
    text = "<!-- tags:  alpha , beta , gamma  -->Content."
    result = mod.get_tags(text)
    assert result == ["alpha", "beta", "gamma"]


def test_get_tags_single_tag():
    text = "<!-- tags: memory -->Content."
    result = mod.get_tags(text)
    assert result == ["memory"]


def test_get_tags_empty_text():
    result = mod.get_tags("")
    assert result == []


# ── get_h2_sections ───────────────────────────────────────────────────────────

def test_get_h2_sections_returns_list():
    result = mod.get_h2_sections("# Title\n\n## Section 1\n\nContent.")
    assert isinstance(result, list)


def test_get_h2_sections_finds_sections():
    text = "# Title\n\n## Alpha\n\n## Beta\n\n## Gamma\n"
    result = mod.get_h2_sections(text)
    assert "Alpha" in result
    assert "Beta" in result
    assert "Gamma" in result


def test_get_h2_sections_empty_when_no_h2():
    text = "# Title\n\n### H3 only\n\nContent."
    result = mod.get_h2_sections(text)
    assert result == []


def test_get_h2_sections_count():
    text = "## A\n## B\n## C\n"
    result = mod.get_h2_sections(text)
    assert len(result) == 3


def test_get_h2_sections_strips_content():
    result = mod.get_h2_sections("## My Section Title\n\nContent.")
    assert result == ["My Section Title"]


def test_get_h2_sections_empty_text():
    result = mod.get_h2_sections("")
    assert result == []
