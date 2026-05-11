"""
Тесты для scripts/improve_graph.py.

Покрытие:
  - count_co_mentions() — подсчёт совместных упоминаний проектов
  - project_layer()     — слой архитектуры для проекта
  - make_mermaid()      — генерация диаграммы Mermaid
  - make_matrix()       — текстовая матрица совместных упоминаний
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_graph")

# ── count_co_mentions ─────────────────────────────────────────────────────────

def test_count_co_mentions_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.count_co_mentions()
    assert isinstance(result, dict)


def test_count_co_mentions_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.count_co_mentions()
    assert result == {}


def test_count_co_mentions_detects_pair(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("AgentFS and Yodoca work together in this project.", encoding="utf-8")
    result = mod.count_co_mentions()
    assert any("AgentFS" in str(k) and "Yodoca" in str(k) for k in result.keys())


def test_count_co_mentions_counts_multiple_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "file1.md").write_text("Svyazi and AgentFS work together.", encoding="utf-8")
    (tmp_path / "file2.md").write_text("Svyazi and AgentFS again together.", encoding="utf-8")
    result = mod.count_co_mentions()
    # Find the pair
    pair_count = 0
    for (p1, p2), count in result.items():
        if "Svyazi" in (p1, p2) and "AgentFS" in (p1, p2):
            pair_count = count
    assert pair_count == 2


# ── project_layer ─────────────────────────────────────────────────────────────

def test_project_layer_returns_string():
    result = mod.project_layer("AgentFS")
    assert isinstance(result, str)


def test_project_layer_known_project():
    result = mod.project_layer("AgentFS")
    assert result == "knowledge"


def test_project_layer_memory_project():
    result = mod.project_layer("Yodoca")
    assert result == "memory"


def test_project_layer_unknown_returns_other():
    result = mod.project_layer("NonExistentProject12345")
    assert result == "other"


def test_project_layer_ingestion():
    result = mod.project_layer("Svyazi")
    assert result == "ingestion"


def test_project_layer_security():
    result = mod.project_layer("SENTINEL")
    assert result == "security"


# ── make_mermaid ──────────────────────────────────────────────────────────────

def test_make_mermaid_returns_string():
    result = mod.make_mermaid({})
    assert isinstance(result, str)


def test_make_mermaid_starts_with_graph():
    result = mod.make_mermaid({})
    assert result.startswith("graph TD")


def test_make_mermaid_contains_subgraphs():
    result = mod.make_mermaid({})
    assert "subgraph" in result


def test_make_mermaid_includes_projects():
    result = mod.make_mermaid({})
    assert "AgentFS" in result


def test_make_mermaid_no_edges_below_threshold():
    co = {("AgentFS", "Yodoca"): 2}
    result = mod.make_mermaid(co, threshold=3)
    # Edge should NOT appear (count=2 < threshold=3)
    assert "-->" not in result or "AgentFS" not in result.split("-->")[0].split("\n")[-1]


def test_make_mermaid_includes_edge_above_threshold():
    co = {("AgentFS", "Yodoca"): 5}
    result = mod.make_mermaid(co, threshold=3)
    assert "-->" in result


def test_make_mermaid_empty_co():
    result = mod.make_mermaid({})
    assert "graph TD" in result
    # No edges
    assert "-->" not in result


# ── make_matrix ───────────────────────────────────────────────────────────────

def test_make_matrix_returns_list():
    co = {("AgentFS", "Yodoca"): 5, ("Svyazi", "Rufler"): 3}
    result = mod.make_matrix(co)
    assert isinstance(result, list)


def test_make_matrix_non_empty_for_co_mentions():
    co = {("AgentFS", "Yodoca"): 5}
    result = mod.make_matrix(co)
    assert len(result) > 0


def test_make_matrix_contains_header():
    co = {("AgentFS", "Yodoca"): 5}
    result = mod.make_matrix(co)
    text = "\n".join(result)
    assert "Топ" in text or "упоминан" in text


def test_make_matrix_contains_projects():
    co = {("AgentFS", "Yodoca"): 5}
    result = mod.make_matrix(co)
    text = "\n".join(result)
    assert "AgentFS" in text
    assert "Yodoca" in text


def test_make_matrix_empty_co():
    result = mod.make_matrix({})
    assert isinstance(result, list)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_graph_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "GRAPH.md").exists()


def test_main_graph_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nAgentFS and Yodoca work together.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "GRAPH.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "GRAPH.md").exists()


def test_main_graph_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "GRAPH.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
