"""Tests for rag.ask + reranker integration (Sprint 59 / M2)."""
from __future__ import annotations

import pytest

from docstoolkit.rag.pipeline import RAGPipeline
from docstoolkit.rag.types import RAGQuery, Passage
from docstoolkit.rerank.reranker import (
    NoOpReranker,
    TFIDFReranker,
    rerank,
)


class _StubRetriever:
    def __init__(self, passages):
        self._p = passages
        self.last_top_k = 0

    def search(self, query, top_k):
        self.last_top_k = top_k
        return list(self._p[:top_k])


class _StubAnswerer:
    def answer(self, system, user, model=""):
        return "stub answer", 0, 0.0


def _patch_pipeline(monkeypatch, retriever, answerer):
    """Replace Retriever and get_answerer used inside the pipeline."""
    import docstoolkit.rag.pipeline as mod

    monkeypatch.setattr(mod, "Retriever", lambda **kw: retriever)
    monkeypatch.setattr(mod, "get_answerer", lambda name, **kw: answerer)


def test_pipeline_overfetches_when_reranking(monkeypatch):
    """When a reranker is set, pipeline asks for top_k*3 candidates."""
    passages = [Passage(text=f"text {i}", doc_id=f"d{i}", score=0.5)
                for i in range(30)]
    retriever = _StubRetriever(passages)
    _patch_pipeline(monkeypatch, retriever, _StubAnswerer())

    query = RAGQuery(question="q", top_k=5, method="keyword",
                     answerer="echo")
    RAGPipeline(query, reranker=NoOpReranker()).run()
    assert retriever.last_top_k == 15


def test_pipeline_default_top_k_without_reranker(monkeypatch):
    passages = [Passage(text=f"t{i}", doc_id=f"d{i}", score=0.5)
                for i in range(20)]
    retriever = _StubRetriever(passages)
    _patch_pipeline(monkeypatch, retriever, _StubAnswerer())

    query = RAGQuery(question="q", top_k=4, method="keyword")
    RAGPipeline(query).run()
    assert retriever.last_top_k == 4


def test_pipeline_returns_top_k_after_rerank(monkeypatch):
    passages = [
        Passage(text="memory agents", doc_id="d0", score=0.1),
        Passage(text="cars and bikes", doc_id="d1", score=0.9),
        Passage(text="memory agents and bikes", doc_id="d2", score=0.5),
    ]
    retriever = _StubRetriever(passages * 5)
    _patch_pipeline(monkeypatch, retriever, _StubAnswerer())

    query = RAGQuery(question="memory agents", top_k=2,
                     method="keyword")
    result = RAGPipeline(query, reranker=TFIDFReranker()).run()
    # Re-ranked: highest token overlap should win
    assert len(result.retrieved_passages) == 2
    doc_ids = [p.doc_id for p in result.retrieved_passages]
    # d0 ("memory agents") matches strongest → first
    assert doc_ids[0] in ("d0", "d2")


def test_rerank_helper_no_passages_returns_empty():
    assert rerank("q", [], NoOpReranker()) == []


def test_rerank_helper_truncates_top_k():
    ps = [Passage(text=f"x{i}", doc_id=f"d{i}", score=float(i))
          for i in range(10)]
    out = rerank("q", ps, NoOpReranker(), top_k=3)
    assert len(out) == 3


def test_rerank_helper_sorts_descending():
    ps = [
        Passage(text="apple", doc_id="a", score=0.1),
        Passage(text="banana", doc_id="b", score=0.9),
        Passage(text="cherry", doc_id="c", score=0.5),
    ]
    out = rerank("q", ps, NoOpReranker())
    # NoOp preserves original scores; sort puts 0.9, 0.5, 0.1
    assert [p.doc_id for p in out] == ["b", "c", "a"]
