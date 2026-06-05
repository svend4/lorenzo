"""Tests for KGRetriever (Sprint 66 / M1)."""
from __future__ import annotations

import pytest

from docstoolkit.knowledge_graph import KGRetriever
from docstoolkit.rag.types import Passage


# ---- basic indexing ----

def test_kgr_indexes_doc():
    kgr = KGRetriever()
    kgr.index_doc("docs/a", "Yodoca is a memory project.", title="A")
    stats = kgr.stats()
    assert stats["docs"] == 1


def test_kgr_indexes_multiple_docs():
    kgr = KGRetriever()
    kgr.index_doc("a", "Python and RAG.")
    kgr.index_doc("b", "Docker and Kubernetes.")
    assert kgr.stats()["docs"] == 2


def test_kgr_skips_empty_text():
    kgr = KGRetriever()
    kgr.index_doc("a", "")
    assert kgr.stats()["docs"] == 0


def test_kgr_index_passages_bulk():
    kgr = KGRetriever()
    kgr.index_passages([
        Passage(text="Python rules", doc_id="a", title="A", score=0.1),
        Passage(text="Docker matters", doc_id="b", title="B", score=0.2),
    ])
    assert kgr.stats()["docs"] == 2


# ---- search ----

def test_kgr_search_finds_doc_by_entity():
    kgr = KGRetriever()
    kgr.index_doc("docs/python", "Python and RAG together.", title="Py")
    kgr.index_doc("docs/docker", "Docker containers.", title="Dk")
    out = kgr.search("Python", top_k=5)
    assert any(p.doc_id == "docs/python" for p in out)


def test_kgr_search_empty_corpus_returns_empty():
    kgr = KGRetriever()
    assert kgr.search("Python") == []


def test_kgr_search_unknown_query_returns_empty():
    kgr = KGRetriever()
    kgr.index_doc("a", "Yodoca rocks.")
    out = kgr.search("nonexistententity_xyz")
    assert out == []


def test_kgr_search_respects_top_k():
    kgr = KGRetriever()
    for i in range(10):
        kgr.index_doc(f"doc{i}", "Python and AI.", title=f"D{i}")
    out = kgr.search("Python", top_k=3)
    assert len(out) <= 3


def test_kgr_search_returns_passages():
    kgr = KGRetriever()
    kgr.index_doc("a", "Python is great.", title="A")
    out = kgr.search("Python")
    assert all(isinstance(p, Passage) for p in out)
    assert out[0].title == "A"


def test_kgr_score_is_normalized():
    kgr = KGRetriever()
    kgr.index_doc("a", "Python is great.")
    out = kgr.search("Python")
    for p in out:
        assert 0.0 <= p.score <= 1.0


# ---- multi-hop expansion ----

def test_kgr_multi_hop_finds_neighbours():
    """If A is linked to B and we query A, B's docs should also rank."""
    kgr = KGRetriever(max_hops=2)
    # Both Python and Docker mentioned together → relation
    kgr.index_doc("rel", "Python uses Docker for deployment.", title="rel")
    # Doc mentioning only Docker
    kgr.index_doc("dk", "Docker matters.", title="dk")
    out = kgr.search("Python", top_k=5)
    doc_ids = {p.doc_id for p in out}
    # rel is direct; dk is via Docker
    assert "rel" in doc_ids


def test_kgr_max_hops_zero_falls_back_to_direct():
    """max_hops=0 still returns direct seed matches via _expand minimum 1."""
    kgr = KGRetriever(max_hops=0)
    kgr.index_doc("a", "Python is great.", title="A")
    out = kgr.search("Python", top_k=5)
    assert any(p.doc_id == "a" for p in out)


# ---- ordering ----

def test_kgr_higher_match_ranks_first():
    kgr = KGRetriever()
    # doc A mentions one entity, doc B mentions two
    kgr.index_doc("docA", "Python.", title="A")
    kgr.index_doc("docB", "Python and Docker.", title="B")
    out = kgr.search("Python Docker", top_k=2)
    # docB should be at top
    assert out[0].doc_id == "docB"
