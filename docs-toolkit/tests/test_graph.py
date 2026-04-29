"""Тесты knowledge graph."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.graph.ner import extract_entities, EntityKinds
from docstoolkit.graph.builder import build_graph, ConceptGraph
from docstoolkit.graph.export import export_dot, export_mermaid, export_json, export_markdown


def test_ner_extracts_persons():
    text = ("John Smith works on the project. " * 50)  # длинный для min_text_len
    ents = extract_entities(text)
    persons = [e.text for e in ents[EntityKinds.PERSON]]
    assert "John Smith" in persons


def test_ner_extracts_handles():
    text = "Contact @kksudo and @vladspace for details. " * 30
    ents = extract_entities(text)
    persons = [e.text for e in ents[EntityKinds.PERSON]]
    assert "@kksudo" in persons
    assert "@vladspace" in persons


def test_ner_extracts_camelcase():
    text = "Use AgentFS or NgtMemory for storage. " * 30
    ents = extract_entities(text)
    projects = [e.text for e in ents[EntityKinds.PROJECT]]
    assert "AgentFS" in projects
    assert "NgtMemory" in projects


def test_ner_extracts_kebab():
    text = "Run knowledge-space and habr-projects pipelines. " * 30
    ents = extract_entities(text)
    projects = [e.text for e in ents[EntityKinds.PROJECT]]
    assert "knowledge-space" in projects


def test_ner_extracts_dates():
    text = "On 2026-04-29 we shipped. Launched 15.04.2024 and июль 2025 too. " * 20
    ents = extract_entities(text)
    dates = [e.text for e in ents[EntityKinds.DATE]]
    assert "2026-04-29" in dates
    assert "15.04.2024" in dates


def test_ner_too_short_returns_empty():
    """Короткий текст — игнор для шума."""
    ents = extract_entities("Short")
    assert ents[EntityKinds.PERSON] == []
    assert ents[EntityKinds.PROJECT] == []


def test_build_graph_basic():
    docs = [
        {"path": "d1", "content": "AgentFS works with Yodoca extensively. " * 30},
        {"path": "d2", "content": "AgentFS pairs with NgtMemory perfectly. " * 30},
    ]
    g = build_graph(docs)
    assert "AgentFS" in g.nodes
    assert g.nodes["AgentFS"]["count"] >= 2
    assert g.nodes["AgentFS"]["kind"] == "project"
    assert "d1" in g.nodes["AgentFS"]["docs"]


def test_build_graph_cooccurrence():
    """Сущности встречающиеся вместе → edge."""
    text = "AgentFS and NgtMemory work together. " * 30
    docs = [{"path": "d1", "content": text}]
    g = build_graph(docs)
    pairs = g.top_pairs()
    pair_names = {(a, b) for (a, b), _ in pairs}
    # Канонический порядок (sorted)
    expected = tuple(sorted(["AgentFS", "NgtMemory"]))
    assert expected in pair_names


def test_top_concepts_filter_by_kind():
    docs = [
        {"path": "d1", "content": "@kksudo uses AgentFS daily. " * 30},
    ]
    g = build_graph(docs)
    persons = g.top_concepts(10, kind="person")
    projects = g.top_concepts(10, kind="project")
    assert any(p[0] == "@kksudo" for p in persons)
    assert any(p[0] == "AgentFS" for p in projects)


def test_neighbors():
    docs = [{"path": "d1", "content": "AgentFS uses NgtMemory and Yodoca. " * 30}]
    g = build_graph(docs)
    nbrs = g.neighbors("AgentFS")
    nbr_names = [n for n, _ in nbrs]
    assert "NgtMemory" in nbr_names or "Yodoca" in nbr_names


def test_export_dot():
    g = ConceptGraph()
    g.add_node("A", "project")
    g.add_node("B", "concept")
    g.add_edge("A", "B", weight=5)
    dot = export_dot(g)
    assert "graph ConceptGraph" in dot
    assert '"A"' in dot
    assert '"B"' in dot


def test_export_json():
    g = ConceptGraph()
    g.add_node("X", "person")
    g.add_edge("X", "Y", 3)
    g.add_node("Y", "project")
    out = export_json(g)
    import json as _json
    data = _json.loads(out)
    assert "nodes" in data
    assert "edges" in data
    assert data["stats"]["nodes"] == 2


def test_export_mermaid():
    g = ConceptGraph()
    g.add_node("Foo", "project")
    g.add_node("Bar", "concept")
    g.add_edge("Foo", "Bar", 3)
    out = export_mermaid(g)
    assert "graph LR" in out
    assert "Foo" in out
    assert "Bar" in out


def test_export_markdown():
    g = ConceptGraph()
    g.add_node("Project1", "project")
    g.add_node("Project1", "project")  # увеличиваем счёт
    md = export_markdown(g)
    assert "Concept Graph" in md
    assert "Project1" in md
