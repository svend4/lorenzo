"""Tests for scripts/mcp_llm_server.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("mcp_llm_server")


# ── CACHE_PATH ────────────────────────────────────────────────────────────────

def test_cache_path_attribute():
    assert hasattr(mod, "CACHE_PATH")
    assert isinstance(mod.CACHE_PATH, Path)


def test_cache_path_is_jsonl():
    assert str(mod.CACHE_PATH).endswith(".jsonl")


# ── dispatch ──────────────────────────────────────────────────────────────────

def test_dispatch_llm_summary_no_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = mod.dispatch("llm_summary", {"file_path": "nonexistent.md"})
    assert isinstance(result, str)


def test_dispatch_llm_qa_no_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = mod.dispatch("llm_qa", {"question": "What is AgentFS?"})
    assert isinstance(result, str)


def test_dispatch_llm_enrich_dry_run(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = mod.dispatch("llm_enrich", {"section": "05-habr-projects", "dry_run": True})
    assert isinstance(result, str)


def test_dispatch_unknown_tool():
    result = mod.dispatch("unknown_xyz", {})
    assert "unknown_xyz" in result or "Неизвестный" in result


# ── TOOLS ─────────────────────────────────────────────────────────────────────

def test_tools_is_list():
    assert isinstance(mod.TOOLS, list)
    assert len(mod.TOOLS) > 0


def test_root_attribute():
    assert hasattr(mod, "ROOT")
    assert isinstance(mod.ROOT, Path)
