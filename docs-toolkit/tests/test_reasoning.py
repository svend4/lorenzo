"""Tests for graph reasoning: TripletStore and GraphReasoner."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.graph.builder import ConceptGraph
from docstoolkit.graph.reasoning import TripletStore, GraphReasoner


# ---- TripletStore ----

@pytest.fixture
def store(tmp_path):
    s = TripletStore(db_path=tmp_path / "tri.sqlite")
    yield s
    s.close()


def test_tripletstore_add_returns_id(store):
    row_id = store.add("AgentFS", "использует", "SQLite")
    assert isinstance(row_id, int)
    assert row_id > 0


def test_tripletstore_find_by_subject(store):
    store.add("AgentFS", "использует", "SQLite", doc_id="doc1")
    store.add("AgentFS", "основан на", "Python", doc_id="doc1")
    store.add("Yodoca", "использует", "Redis", doc_id="doc2")

    results = store.find(subject="AgentFS")
    assert len(results) == 2
    predicates = {r[2] for r in results}
    assert "использует" in predicates
    assert "основан на" in predicates


def test_tripletstore_find_by_predicate(store):
    store.add("AgentFS", "использует", "SQLite")
    store.add("Yodoca", "использует", "Redis")
    store.add("NgtMemory", "является", "хранилищем")

    results = store.find(predicate="использует")
    assert len(results) == 2
    subjects = {r[1] for r in results}
    assert "AgentFS" in subjects
    assert "Yodoca" in subjects


def test_tripletstore_find_by_object(store):
    store.add("AgentFS", "использует", "SQLite")
    store.add("Yodoca", "использует", "SQLite")
    store.add("NgtMemory", "использует", "Redis")

    results = store.find(object="SQLite")
    assert len(results) == 2


def test_tripletstore_find_combined(store):
    store.add("AgentFS", "использует", "SQLite")
    store.add("Yodoca", "использует", "SQLite")
    store.add("AgentFS", "основан на", "Python")

    results = store.find(subject="AgentFS", predicate="использует")
    assert len(results) == 1
    assert results[0][3] == "SQLite"


def test_tripletstore_find_no_filter_returns_all(store):
    store.add("A", "p1", "B")
    store.add("C", "p2", "D")
    results = store.find()
    assert len(results) == 2


def test_tripletstore_confidence_stored(store):
    store.add("A", "uses", "B", confidence=0.75)
    results = store.find(subject="A")
    assert len(results) == 1
    # tuple: (id, subject, predicate, object, doc_id, confidence)
    assert abs(results[0][5] - 0.75) < 1e-6


def test_tripletstore_extract_from_text_ru(store):
    text = "AgentFS использует SQLite для хранения данных. " * 5
    count = store.extract_from_text(text, doc_id="doc_ru")
    assert count >= 1
    results = store.find(predicate="использует")
    subjects = {r[1] for r in results}
    assert "AgentFS" in subjects


def test_tripletstore_extract_from_text_en(store):
    text = "NgtMemory uses Redis for caching results. " * 5
    count = store.extract_from_text(text, doc_id="doc_en")
    assert count >= 1
    results = store.find(predicate="uses")
    subjects = {r[1] for r in results}
    assert "NgtMemory" in subjects


def test_tripletstore_stats(store):
    store.add("A", "p", "B", doc_id="d1")
    store.add("C", "p", "D", doc_id="d2")
    store.add("A", "q", "E", doc_id="d1")
    s = store.stats()
    assert s["total"] == 3
    assert s["subjects"] == 2
    assert s["predicates"] == 2
    assert s["docs"] == 2


# ---- GraphReasoner ----

def _make_graph() -> ConceptGraph:
    """Build a simple 4-node graph: A-B-C-D chain with A-D direct link."""
    g = ConceptGraph()
    g.add_node("A", "project")
    g.add_node("B", "project")
    g.add_node("C", "project")
    g.add_node("D", "project")
    g.add_edge("A", "B", 5)
    g.add_edge("B", "C", 3)
    g.add_edge("C", "D", 2)
    g.add_edge("A", "D", 1)
    return g


def test_find_connected_1_hop():
    g = _make_graph()
    r = GraphReasoner(g)
    connected = r.find_connected("A", hops=1)
    # A is directly connected to B and D
    assert "B" in connected
    assert "D" in connected
    assert "C" not in connected  # C is 2 hops away from A via B


def test_find_connected_2_hops():
    g = _make_graph()
    r = GraphReasoner(g)
    connected = r.find_connected("A", hops=2)
    assert "B" in connected
    assert "C" in connected
    assert "D" in connected


def test_find_connected_unknown_node():
    g = _make_graph()
    r = GraphReasoner(g)
    assert r.find_connected("UNKNOWN", hops=2) == []


def test_find_connected_excludes_start():
    g = _make_graph()
    r = GraphReasoner(g)
    connected = r.find_connected("A", hops=2)
    assert "A" not in connected


def test_explain_path_direct():
    g = _make_graph()
    r = GraphReasoner(g)
    path = r.explain_path("A", "B")
    assert path == ["A", "B"]


def test_explain_path_indirect():
    g = ConceptGraph()
    g.add_node("X", "project")
    g.add_node("Y", "project")
    g.add_node("Z", "project")
    g.add_edge("X", "Y", 1)
    g.add_edge("Y", "Z", 1)
    r = GraphReasoner(g)
    path = r.explain_path("X", "Z")
    assert path[0] == "X"
    assert path[-1] == "Z"
    assert len(path) == 3


def test_explain_path_same_node():
    g = _make_graph()
    r = GraphReasoner(g)
    assert r.explain_path("A", "A") == ["A"]


def test_explain_path_unreachable():
    g = ConceptGraph()
    g.add_node("X", "project")
    g.add_node("Y", "project")
    # No edges between X and Y
    r = GraphReasoner(g)
    assert r.explain_path("X", "Y") == []


def test_explain_path_unknown_node():
    g = _make_graph()
    r = GraphReasoner(g)
    assert r.explain_path("A", "MISSING") == []


def test_multi_hop_query(tmp_path):
    g = _make_graph()
    store = TripletStore(db_path=tmp_path / "mhq.sqlite")
    store.add("AgentFS", "использует", "RAG")
    store.add("AgentFS", "упоминает", "memory")
    store.add("Yodoca", "использует", "RAG")
    store.add("NgtMemory", "упоминает", "memory")

    r = GraphReasoner(g, store=store)
    results = r.multi_hop_query([
        ("использует", "RAG"),
        ("упоминает", "memory"),
    ])
    # Only AgentFS satisfies both conditions
    assert "AgentFS" in results
    assert "Yodoca" not in results
    assert "NgtMemory" not in results
    store.close()


def test_multi_hop_query_empty_conditions(tmp_path):
    g = _make_graph()
    store = TripletStore(db_path=tmp_path / "mhq2.sqlite")
    r = GraphReasoner(g, store=store)
    assert r.multi_hop_query([]) == []
    store.close()


def test_multi_hop_query_no_store():
    g = _make_graph()
    r = GraphReasoner(g, store=None)
    assert r.multi_hop_query([("p", "o")]) == []


def test_answer_graph_query_known_entity():
    g = _make_graph()
    r = GraphReasoner(g)
    answer = r.answer_graph_query("Tell me about A and B")
    assert "A" in answer or "B" in answer


def test_answer_graph_query_unknown_entity():
    g = _make_graph()
    r = GraphReasoner(g)
    answer = r.answer_graph_query("something completely unknown xyz123")
    assert "No known entities" in answer
