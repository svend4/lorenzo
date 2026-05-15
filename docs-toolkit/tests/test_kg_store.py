"""Phase V.1 — SQLite-backed TripleStore tests.

Covers: schema creation, entity round-trip, triple insert + upsert,
indexed lookup by every filter, neighbors traversal.
"""
from __future__ import annotations

import pytest

from docstoolkit.knowledge_graph import (
    Entity, EntityType, Relation, RelationType,
    Triple, TripleStore,
)


@pytest.fixture
def store():
    s = TripleStore(":memory:")
    yield s
    s.close()


def _e(eid: str, name: str, typ: EntityType = EntityType.CONCEPT) -> Entity:
    return Entity(entity_id=eid, name=name, entity_type=typ)


def test_empty_store(store):
    assert store.entity_count() == 0
    assert store.triple_count() == 0


def test_add_get_entity_roundtrip(store):
    e = _e("py", "Python", EntityType.TECHNOLOGY)
    store.add_entity(e)
    got = store.get_entity("py")
    assert got is not None
    assert got.entity_id == "py"
    assert got.name == "Python"
    assert got.entity_type == EntityType.TECHNOLOGY


def test_get_missing_entity(store):
    assert store.get_entity("nope") is None


def test_find_entity_by_alias(store):
    e = Entity(entity_id="ml", name="Machine Learning",
               entity_type=EntityType.CONCEPT, aliases=("ML", "AI/ML"))
    store.add_entity(e)
    assert store.find_entity("ml") is not None       # exact name (case-fold)
    assert store.find_entity("AI/ML") is not None     # alias
    assert store.find_entity("unknown") is None


def test_add_triple(store):
    store.add_entity(_e("py", "Python"))
    store.add_entity(_e("rag", "RAG"))
    tid = store.add_triple(Triple(
        subject="py", predicate=RelationType.USES.value, object="rag",
        doc_id="docs/a.md", score=0.9,
    ))
    assert tid
    assert store.triple_count() == 1


def test_triple_upsert_keeps_max_score(store):
    store.add_entity(_e("py", "Python"))
    store.add_entity(_e("rag", "RAG"))
    store.add_triple(Triple(subject="py", predicate="uses",
                            object="rag", doc_id="d", score=0.4))
    store.add_triple(Triple(subject="py", predicate="uses",
                            object="rag", doc_id="d", score=0.8))
    # ON CONFLICT MAX(score) → 0.8
    triples = store.find_triples(subject="py")
    assert len(triples) == 1
    assert triples[0].score == pytest.approx(0.8)


def test_find_triples_by_each_filter(store):
    store.add_entity(_e("py", "Python"))
    store.add_entity(_e("rag", "RAG"))
    store.add_entity(_e("llm", "LLM"))
    store.add_triple(Triple(subject="py", predicate="uses",
                            object="rag", doc_id="d1"))
    store.add_triple(Triple(subject="py", predicate="uses",
                            object="llm", doc_id="d2"))
    store.add_triple(Triple(subject="rag", predicate="mentions",
                            object="llm", doc_id="d1"))

    # by subject
    res = store.find_triples(subject="py")
    assert len(res) == 2

    # by predicate
    res = store.find_triples(predicate="mentions")
    assert len(res) == 1
    assert res[0].subject == "rag"

    # by object
    res = store.find_triples(object="llm")
    assert len(res) == 2

    # by doc_id
    res = store.find_triples(doc_id="d1")
    assert len(res) == 2

    # combined
    res = store.find_triples(subject="py", object="llm")
    assert len(res) == 1


def test_find_triples_orders_by_score_desc(store):
    store.add_entity(_e("a", "A"))
    store.add_entity(_e("b", "B"))
    store.add_entity(_e("c", "C"))
    store.add_triple(Triple(subject="a", predicate="x", object="b", score=0.5))
    store.add_triple(Triple(subject="a", predicate="x", object="c", score=0.9))
    res = store.find_triples(subject="a")
    assert [t.object for t in res] == ["c", "b"]


def test_neighbors_both_directions(store):
    for eid, name in [("a", "A"), ("b", "B"), ("c", "C")]:
        store.add_entity(_e(eid, name))
    store.add_triple(Triple(subject="a", predicate="uses", object="b"))
    store.add_triple(Triple(subject="c", predicate="uses", object="a"))
    neighbors = store.neighbors("a")
    assert sorted(neighbors) == ["b", "c"]


def test_neighbors_with_predicate_filter(store):
    for eid, name in [("a", "A"), ("b", "B"), ("c", "C")]:
        store.add_entity(_e(eid, name))
    store.add_triple(Triple(subject="a", predicate="uses", object="b"))
    store.add_triple(Triple(subject="a", predicate="mentions", object="c"))
    assert store.neighbors("a", predicate="uses") == ["b"]
    assert store.neighbors("a", predicate="mentions") == ["c"]


def test_add_relation_convenience(store):
    store.add_entity(_e("a", "A"))
    store.add_entity(_e("b", "B"))
    rel = Relation(source_id="a", target_id="b",
                   relation_type=RelationType.USES)
    store.add_relation(rel, doc_id="d1", score=0.7)
    res = store.find_triples(subject="a")
    assert len(res) == 1
    assert res[0].predicate == "uses"
    assert res[0].score == pytest.approx(0.7)


def test_close_is_idempotent(store):
    store.close()
    store.close()  # second close must not raise


def test_persistence_via_file(tmp_path):
    p = tmp_path / "kg.sqlite"
    s1 = TripleStore(str(p))
    s1.add_entity(_e("py", "Python"))
    s1.add_triple(Triple(subject="py", predicate="x", object="py"))
    s1.close()
    # Re-open — content persists.
    s2 = TripleStore(str(p))
    try:
        assert s2.entity_count() == 1
        assert s2.triple_count() == 1
    finally:
        s2.close()
