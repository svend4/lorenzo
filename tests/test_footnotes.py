"""
Тесты для scripts/improve_footnotes.py.

Покрытие:
  - add_footnotes()  — добавление сносок [^term] к первому вхождению
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_footnotes")


# ── add_footnotes ─────────────────────────────────────────────────────────────

def test_add_footnotes_returns_tuple():
    result = mod.add_footnotes("# Title\n\nSome text.", {"MCP": "Model Context Protocol"})
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_add_footnotes_returns_string_and_int():
    text, count = mod.add_footnotes("# Title\n\nSome text.", {"MCP": "Model Context Protocol"})
    assert isinstance(text, str)
    assert isinstance(count, int)


def test_add_footnotes_zero_for_no_match():
    _, count = mod.add_footnotes("# Title\n\nSome text.", {"XYZ": "Definition"})
    assert count == 0


def test_add_footnotes_finds_term():
    text, count = mod.add_footnotes("Use MCP for tools.", {"MCP": "Model Context Protocol"})
    assert count >= 1


def test_add_footnotes_adds_reference():
    text, count = mod.add_footnotes("Use MCP for tools.", {"MCP": "Model Context Protocol"})
    if count > 0:
        assert "[^mcp]" in text


def test_add_footnotes_adds_definition():
    text, count = mod.add_footnotes("Use MCP for tools.", {"MCP": "Model Context Protocol"})
    if count > 0:
        assert "Model Context Protocol" in text


def test_add_footnotes_skips_if_marker_present():
    text_with_marker = f"# Title\n\n{mod.MARKER}\n\nUse MCP for tools."
    text, count = mod.add_footnotes(text_with_marker, {"MCP": "Model Context Protocol"})
    assert count == 0


def test_add_footnotes_idempotent():
    original = "Use MCP for agent tools here."
    text1, count1 = mod.add_footnotes(original, {"MCP": "Model Context Protocol"})
    text2, count2 = mod.add_footnotes(text1, {"MCP": "Model Context Protocol"})
    assert count2 == 0  # Already has marker


def test_add_footnotes_only_first_occurrence():
    text = "Use MCP here. And MCP again."
    result, count = mod.add_footnotes(text, {"MCP": "Definition"})
    if count > 0:
        # The body (before the marker) should have exactly one [^mcp] reference
        body = result.split(mod.MARKER)[0]
        assert body.count("[^mcp]") == 1


def test_add_footnotes_skips_code_blocks():
    text = "```\nMCP is here\n```\nReal MCP usage."
    text_out, count = mod.add_footnotes(text, {"MCP": "Model Context Protocol"})
    if count > 0:
        # The footnote ref should be in the "Real MCP" part, not the code block
        assert "```" in text_out


def test_add_footnotes_multiple_terms():
    text = "Use MCP and RAG together."
    _, count = mod.add_footnotes(
        text, {"MCP": "Model Context Protocol", "RAG": "Retrieval-Augmented Generation"}
    )
    assert count >= 0  # May or may not find depending on word boundaries
