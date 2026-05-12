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


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_concept_graph_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FORMAT", "mermaid")
    mod.main()
    assert (tmp_path / "CONCEPT_GRAPH.md").exists()


def test_main_concept_graph_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FORMAT", "mermaid")
    (tmp_path / "doc.md").write_text("# AgentFS\n\nAgent memory system.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "CONCEPT_GRAPH.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FORMAT", "mermaid")
    mod.main()
    assert (tmp_path / "CONCEPT_GRAPH.md").exists()


# ── arg parsing ────────────────────────────────────────────────────────────────

def test_min_weight_arg_parsing():
    """Lines 33-35: --min-weight N sets MIN_WEIGHT."""
    orig = sys.argv[:]
    try:
        sys.argv = ["prog", "--min-weight", "5"]
        importlib.reload(mod)
        assert mod.MIN_WEIGHT == 5
    finally:
        sys.argv = orig
        importlib.reload(mod)


def test_top_concepts_arg_parsing():
    """Lines 38-40: --top-concepts N sets TOP_CONCEPTS."""
    orig = sys.argv[:]
    try:
        sys.argv = ["prog", "--top-concepts", "20"]
        importlib.reload(mod)
        assert mod.TOP_CONCEPTS == 20
    finally:
        sys.argv = orig
        importlib.reload(mod)


def test_format_arg_parsing():
    """Lines 44-46: --format dot sets FORMAT."""
    orig = sys.argv[:]
    try:
        sys.argv = ["prog", "--format", "dot"]
        importlib.reload(mod)
        assert mod.FORMAT == "dot"
    finally:
        sys.argv = orig
        importlib.reload(mod)


def test_section_arg_parsing():
    """Lines 50-52: --section sets SECTION_FILTER."""
    orig = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "01-svyazi"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER is not None
    finally:
        sys.argv = orig
        importlib.reload(mod)


# ── build_graph: exception reading file ───────────────────────────────────────

def test_build_graph_handles_read_error(tmp_path, monkeypatch):
    """Lines 116-117: exception reading file → continue."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    bad = tmp_path / "bad.md"
    bad.write_text("content", encoding="utf-8")
    from pathlib import Path as _Path
    orig_read = _Path.read_text
    def mock_read(self, *a, **kw):
        if self == bad:
            raise OSError("mocked")
        return orig_read(self, *a, **kw)
    monkeypatch.setattr(_Path, "read_text", mock_read)
    nodes, edges = mod.build_graph([bad])
    assert isinstance(nodes, dict)


# ── main: DOT format ────────────────────────────────────────────────────────

def test_main_dot_format(tmp_path, monkeypatch):
    """Lines 243-248, 253-257: FORMAT=dot → concept_graph.dot written."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FORMAT", "dot")
    content = "agent memory knowledge system retrieval " * 10
    (tmp_path / "doc.md").write_text("# Title\n\n" + content, encoding="utf-8")
    mod.main()
    assert (tmp_path / "CONCEPT_GRAPH.md").exists()
    assert (tmp_path / "concept_graph.dot").exists()


# ── __main__ block ─────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 282: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FORMAT", "mermaid")
    runpy.run_path(str(ROOT / "scripts" / "improve_concept_graph.py"), run_name="__main__")
