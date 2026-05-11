"""
Тесты для scripts/improve_concept_graph.py.

Покрытие:
  - build_graph()  — граф совместных упоминаний
  - to_mermaid()   — Mermaid-диаграмма из графа
  - to_dot()       — Graphviz DOT из графа
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_concept_graph")

# ── build_graph ───────────────────────────────────────────────────────────────

def test_build_graph_returns_tuple(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod.build_graph([])
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_build_graph_empty_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    nodes, edges = mod.build_graph([])
    assert nodes == {}
    assert edges == {}


def test_build_graph_extracts_nodes(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "TOP_CONCEPTS", 5)
    monkeypatch.setattr(mod, "MIN_WEIGHT", 1)
    f = tmp_path / "doc.md"
    f.write_text("агент память консолидация архитектура знания слой модуль поиск", encoding="utf-8")
    nodes, edges = mod.build_graph([f])
    assert len(nodes) > 0


def test_build_graph_nodes_have_count(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "TOP_CONCEPTS", 5)
    monkeypatch.setattr(mod, "MIN_WEIGHT", 1)
    f = tmp_path / "doc.md"
    f.write_text("агент агент агент память знания слой модуль поиск база данны", encoding="utf-8")
    nodes, edges = mod.build_graph([f])
    for node_data in nodes.values():
        assert "count" in node_data
        assert "category" in node_data


def test_build_graph_edges_have_weight(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "TOP_CONCEPTS", 10)
    monkeypatch.setattr(mod, "MIN_WEIGHT", 1)
    f1 = tmp_path / "a.md"
    f1.write_text("агент память знания архитектура поиск слой модуль база данны текст файл", encoding="utf-8")
    f2 = tmp_path / "b.md"
    f2.write_text("агент память знания архитектура поиск слой модуль база данны текст файл", encoding="utf-8")
    nodes, edges = mod.build_graph([f1, f2])
    for weight in edges.values():
        assert isinstance(weight, int)
        assert weight >= 1


# ── to_mermaid ────────────────────────────────────────────────────────────────

def test_to_mermaid_returns_string():
    nodes = {"агент": {"count": 5, "files": 2, "category": "agent"}}
    edges = {}
    result = mod.to_mermaid(nodes, edges)
    assert isinstance(result, str)


def test_to_mermaid_starts_with_graph_td():
    nodes = {"агент": {"count": 5, "files": 2, "category": "agent"}}
    result = mod.to_mermaid(nodes, {})
    assert result.startswith("graph TD")


def test_to_mermaid_includes_nodes():
    nodes = {
        "агент": {"count": 5, "files": 2, "category": "agent"},
        "память": {"count": 3, "files": 1, "category": "memory"},
    }
    result = mod.to_mermaid(nodes, {})
    assert "агент" in result
    assert "память" in result


def test_to_mermaid_includes_edges():
    nodes = {
        "агент": {"count": 5, "files": 2, "category": "agent"},
        "память": {"count": 3, "files": 1, "category": "memory"},
    }
    edges = {("агент", "память"): 3}
    result = mod.to_mermaid(nodes, edges)
    assert "-->" in result


def test_to_mermaid_empty_graph():
    result = mod.to_mermaid({}, {})
    assert "graph TD" in result


# ── to_dot ────────────────────────────────────────────────────────────────────

def test_to_dot_returns_string():
    nodes = {"агент": {"count": 5, "files": 2, "category": "agent"}}
    edges = {}
    result = mod.to_dot(nodes, edges)
    assert isinstance(result, str)


def test_to_dot_valid_digraph():
    nodes = {"агент": {"count": 5, "files": 2, "category": "agent"}}
    result = mod.to_dot(nodes, {})
    assert "digraph" in result
    assert "{" in result
    assert "}" in result


def test_to_dot_includes_nodes():
    nodes = {"агент": {"count": 5, "files": 2, "category": "agent"}}
    result = mod.to_dot(nodes, {})
    assert "агент" in result


def test_to_dot_includes_edges():
    nodes = {
        "агент": {"count": 5, "files": 2, "category": "agent"},
        "память": {"count": 3, "files": 1, "category": "memory"},
    }
    edges = {("агент", "память"): 3}
    result = mod.to_dot(nodes, edges)
    assert "->" in result


def test_to_dot_empty_graph():
    result = mod.to_dot({}, {})
    assert "digraph" in result
