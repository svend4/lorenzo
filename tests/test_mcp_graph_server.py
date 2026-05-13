"""Tests for scripts/mcp_graph_server.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("mcp_graph_server")


# ── tool_health ───────────────────────────────────────────────────────────────

def test_tool_health_no_docs(monkeypatch):
    monkeypatch.setattr(mod, "read_doc", lambda filename: "")
    result = mod.tool_health()
    assert isinstance(result, str)
    assert "запустите" in result.lower() or "health" in result.lower()


def test_tool_health_with_content(monkeypatch):
    monkeypatch.setattr(mod, "read_doc", lambda filename: f"# {filename}\n\nScore: 87/100")
    result = mod.tool_health()
    assert isinstance(result, str)
    assert "HEALTH.md" in result or "87" in result


# ── tool_decisions ────────────────────────────────────────────────────────────

def test_tool_decisions_no_doc(monkeypatch):
    monkeypatch.setattr(mod, "read_doc", lambda filename: "")
    result = mod.tool_decisions("memory")
    assert isinstance(result, str)
    assert "DECISIONS.md" in result or "не найден" in result.lower()


def test_tool_decisions_finds_topic(monkeypatch):
    monkeypatch.setattr(mod, "read_doc",
                        lambda filename: "## Memory decisions\n\nUse BM25 for retrieval.")
    result = mod.tool_decisions("memory")
    assert isinstance(result, str)


def test_tool_decisions_not_found(monkeypatch):
    monkeypatch.setattr(mod, "read_doc",
                        lambda filename: "## Unrelated topic\n\nSome decision.")
    result = mod.tool_decisions("xyz_nonexistent")
    assert isinstance(result, str)
    assert "не найден" in result.lower() or "xyz_nonexistent" in result


# ── tool_concept_graph ────────────────────────────────────────────────────────

def test_tool_concept_graph_no_doc(monkeypatch):
    monkeypatch.setattr(mod, "read_doc", lambda filename: "")
    result = mod.tool_concept_graph()
    assert isinstance(result, str)
    assert "CONCEPT_GRAPH" in result or "не найден" in result.lower()


def test_tool_concept_graph_with_content(monkeypatch):
    monkeypatch.setattr(mod, "read_doc",
                        lambda filename: "## Concepts\n\n- memory → retrieval\n- agent → tool")
    result = mod.tool_concept_graph(top_n=5)
    assert isinstance(result, str)


# ── tool_kpi_history ──────────────────────────────────────────────────────────

def test_tool_kpi_history_no_doc(monkeypatch):
    monkeypatch.setattr(mod, "read_doc", lambda filename: "")
    result = mod.tool_kpi_history()
    assert isinstance(result, str)
    assert "KPI_HISTORY" in result or "не найден" in result.lower()


def test_tool_kpi_history_with_name(monkeypatch):
    monkeypatch.setattr(mod, "read_doc",
                        lambda filename: "## health_score\n\n| date | value |\n| 2025 | 87 |")
    result = mod.tool_kpi_history("health_score")
    assert isinstance(result, str)


def test_tool_kpi_history_name_not_found(monkeypatch):
    monkeypatch.setattr(mod, "read_doc",
                        lambda filename: "## other_metric\n\ndata.")
    result = mod.tool_kpi_history("nonexistent_xyz")
    assert isinstance(result, str)
    assert "не найдена" in result.lower() or "nonexistent_xyz" in result


# ── dispatch ──────────────────────────────────────────────────────────────────

def test_dispatch_get_health(monkeypatch):
    monkeypatch.setattr(mod, "read_doc", lambda filename: "")
    result = mod.dispatch("get_health", {})
    assert isinstance(result, str)


def test_dispatch_get_decisions(monkeypatch):
    monkeypatch.setattr(mod, "read_doc", lambda filename: "")
    result = mod.dispatch("get_decisions", {"topic": "memory"})
    assert isinstance(result, str)


def test_dispatch_get_concept_graph(monkeypatch):
    monkeypatch.setattr(mod, "read_doc", lambda filename: "")
    result = mod.dispatch("get_concept_graph", {"top_n": 10})
    assert isinstance(result, str)


def test_dispatch_unknown_tool():
    result = mod.dispatch("unknown_xyz", {})
    assert "unknown_xyz" in result or "Неизвестный" in result


# ── TOOLS ─────────────────────────────────────────────────────────────────────

def test_tools_is_list():
    assert isinstance(mod.TOOLS, list)
    assert len(mod.TOOLS) > 0
