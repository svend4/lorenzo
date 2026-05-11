"""Tests for scripts/mcp_search_server.py."""

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("mcp_search_server")


# ── tool_search_docs ──────────────────────────────────────────────────────────

def test_tool_search_docs_empty_query():
    result = mod.tool_search_docs("")
    assert isinstance(result, str)
    assert "query" in result.lower() or "укаж" in result.lower()


def test_tool_search_docs_returns_string(monkeypatch):
    import mcp_common
    monkeypatch.setattr(mcp_common, "load_search_index", lambda: [
        {"title": "AgentFS", "content": "agent file system", "path": "doc.md", "tags": []},
    ])
    result = mod.tool_search_docs("agent")
    assert isinstance(result, str)


def test_tool_search_docs_no_results(monkeypatch):
    import mcp_common
    monkeypatch.setattr(mcp_common, "load_search_index", lambda: [])
    result = mod.tool_search_docs("xyznonexistent")
    assert isinstance(result, str)


def test_tool_search_docs_finds_relevant(monkeypatch):
    import mcp_common
    monkeypatch.setattr(mcp_common, "load_search_index", lambda: [
        {"title": "AgentFS project", "content": "agent filesystem memory", "path": "agentfs.md", "tags": []},
        {"title": "Unrelated", "content": "unrelated content here", "path": "other.md", "tags": []},
    ])
    result = mod.tool_search_docs("AgentFS")
    assert "AgentFS" in result or "agentfs" in result.lower()


# ── tool_find_similar ─────────────────────────────────────────────────────────

def test_tool_find_similar_no_similar_md(monkeypatch):
    import mcp_common
    monkeypatch.setattr(mcp_common, "read_doc", lambda filename: "")
    result = mod.tool_find_similar("agentfs.md")
    assert isinstance(result, str)
    assert "SIMILAR.md" in result or "найдены" in result.lower()


def test_tool_find_similar_finds_in_text(monkeypatch):
    import mcp_common
    similar_text = (
        "## agentfs.md\n\n"
        "- docs/05-habr-projects/memory/yodoca.md (0.85)\n"
        "- docs/04-ai-collaborations/01-overview.md (0.72)\n"
    )
    monkeypatch.setattr(mcp_common, "read_doc", lambda filename: similar_text)
    result = mod.tool_find_similar("agentfs.md")
    assert isinstance(result, str)


# ── dispatch ──────────────────────────────────────────────────────────────────

def test_dispatch_search_docs(monkeypatch):
    import mcp_common
    monkeypatch.setattr(mcp_common, "load_search_index", lambda: [])
    result = mod.dispatch("search_docs", {"query": "agent"})
    assert isinstance(result, str)


def test_dispatch_find_similar(monkeypatch):
    import mcp_common
    monkeypatch.setattr(mcp_common, "read_doc", lambda filename: "")
    result = mod.dispatch("find_similar", {"file_path": "test.md"})
    assert isinstance(result, str)


def test_dispatch_unknown_tool():
    result = mod.dispatch("unknown_tool_xyz", {})
    assert isinstance(result, str)
    assert "unknown_tool_xyz" in result or "Неизвестный" in result


def test_dispatch_empty_query():
    result = mod.dispatch("search_docs", {"query": ""})
    assert isinstance(result, str)


# ── TOOLS list ────────────────────────────────────────────────────────────────

def test_tools_is_list():
    assert isinstance(mod.TOOLS, list)
    assert len(mod.TOOLS) > 0


def test_tools_have_search_docs():
    names = [getattr(t, "name", None) or t.get("name") if isinstance(t, dict) else t.name
             for t in mod.TOOLS]
    assert "search_docs" in names


# ── module attributes ─────────────────────────────────────────────────────────

def test_root_attribute():
    assert hasattr(mod, "ROOT") or hasattr(
        importlib.import_module("mcp_common"), "ROOT"
    )
