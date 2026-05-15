"""Tests for ask(with_got=True) integration (Sprint 75 / N3)."""
from __future__ import annotations

import pytest

from docstoolkit.rag.pipeline import ask
from docstoolkit.rag.types import Passage


class _StubRetriever:
    def __init__(self, passages):
        self._p = passages

    def search(self, query, top_k):
        return list(self._p[:top_k])


class _StubAnswerer:
    def answer(self, system, user, model=""):
        return "synthesized answer", 0, 0.0


@pytest.fixture
def patched(monkeypatch):
    import docstoolkit.rag.pipeline as mod
    passages = [
        Passage(text="Python is a programming language", doc_id="a",
                title="A", score=0.9),
        Passage(text="RAG combines retrieval and generation", doc_id="b",
                title="B", score=0.8),
        Passage(text="Docker is a container platform", doc_id="c",
                title="C", score=0.7),
    ]
    monkeypatch.setattr(mod, "Retriever",
                        lambda **kw: _StubRetriever(passages))
    monkeypatch.setattr(mod, "get_answerer",
                        lambda name, **kw: _StubAnswerer())


def test_got_off_returns_none(patched):
    result = ask("Python?", top_k=3)
    assert result.got_result is None


def test_got_on_returns_reasoning_result(patched):
    result = ask("Python and Docker?", top_k=3, with_got=True)
    assert result.got_result is not None
    assert hasattr(result.got_result, "graph")
    assert hasattr(result.got_result, "final_answer")


def test_got_respects_max_hypotheses(patched):
    result = ask("a and b and c and d and e?", top_k=3,
                 with_got=True, got_max_hypotheses=2)
    assert result.got_result is not None
    # Graph node count should be bounded
    assert result.got_result.graph.node_count() <= 10


def test_got_composes_with_facets(patched):
    result = ask("Python?", top_k=3, with_got=True, with_facets=True)
    assert result.got_result is not None
    assert isinstance(result.facets, list)
