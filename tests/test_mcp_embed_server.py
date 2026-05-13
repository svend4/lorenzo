"""Tests for scripts/mcp_embed_server.py."""

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("mcp_embed_server")


# ── tool_keyword_search ───────────────────────────────────────────────────────

def test_tool_keyword_search_empty_query():
    result = mod.tool_keyword_search("")
    assert isinstance(result, str)
    assert "query" in result.lower() or "укаж" in result.lower()


def test_tool_keyword_search_returns_string(monkeypatch):
    import mcp_common
    monkeypatch.setattr(mcp_common, "load_search_index", lambda: [
        {"title": "AgentFS", "content": "agent file system", "path": "agentfs.md", "tags": []},
    ])
    result = mod.tool_keyword_search("agent")
    assert isinstance(result, str)


def test_tool_keyword_search_no_results(monkeypatch):
    import mcp_common
    monkeypatch.setattr(mcp_common, "load_search_index", lambda: [])
    result = mod.tool_keyword_search("xyz_unique_query")
    assert isinstance(result, str)


# ── tool_list_providers ───────────────────────────────────────────────────────

def test_tool_list_providers_returns_string():
    result = mod.tool_list_providers()
    assert isinstance(result, str)


def test_tool_list_providers_mentions_providers():
    result = mod.tool_list_providers()
    assert "tfidf" in result.lower() or "keyword" in result.lower() or "провайдер" in result.lower()


# ── tool_hybrid_search ────────────────────────────────────────────────────────

def test_tool_hybrid_search_empty_query():
    result = mod.tool_hybrid_search("")
    assert isinstance(result, str)


def test_tool_hybrid_search_returns_string(monkeypatch):
    import mcp_common
    monkeypatch.setattr(mcp_common, "load_search_index", lambda: [
        {"title": "AgentFS", "content": "agent file system", "path": "agentfs.md", "tags": []},
    ])
    result = mod.tool_hybrid_search("agent")
    assert isinstance(result, str)


# ── dispatch ──────────────────────────────────────────────────────────────────

def test_dispatch_keyword_search():
    result = mod.dispatch("keyword_search", {"query": ""})
    assert isinstance(result, str)


def test_dispatch_list_providers():
    result = mod.dispatch("list_providers", {})
    assert isinstance(result, str)


def test_dispatch_unknown_tool():
    result = mod.dispatch("unknown_xyz", {})
    assert "unknown_xyz" in result or "Неизвестный" in result


# ── TOOLS ─────────────────────────────────────────────────────────────────────

def test_tools_is_list():
    assert isinstance(mod.TOOLS, list)
    assert len(mod.TOOLS) > 0
