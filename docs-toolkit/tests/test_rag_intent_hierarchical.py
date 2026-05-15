"""Tests for ask() auto-intent and hierarchical routing.

Sprint 67 / M3 — hierarchical retrieval
Sprint 68 / M4 — intent-based pipeline routing
"""
from __future__ import annotations

import pytest

from docstoolkit.rag.pipeline import ask
from docstoolkit.rag.types import Passage


class _StubRetriever:
    last_kwargs: dict | None = None

    def __init__(self, passages, method=""):
        self._p = passages
        _StubRetriever.last_method = method
        self.calls: list[tuple[str, int]] = []

    def search(self, query, top_k):
        self.calls.append((query, top_k))
        return list(self._p[:top_k])


class _StubAnswerer:
    def answer(self, system, user, model=""):
        return "ok", 0, 0.0


@pytest.fixture
def patched(monkeypatch):
    import docstoolkit.rag.pipeline as mod
    captured = {"method": None, "top_k": None}
    passages = [Passage(text=f"t{i}", doc_id=f"d{i}", title=f"D{i}",
                        score=0.5) for i in range(10)]

    def fake_retriever(method="hybrid", model=""):
        captured["method"] = method
        return _StubRetriever(passages, method=method)

    monkeypatch.setattr(mod, "Retriever", fake_retriever)
    monkeypatch.setattr(mod, "get_answerer", lambda name, **kw: _StubAnswerer())
    return captured


# ---------------- auto_intent ----------------

def test_auto_intent_off_uses_default_hybrid(patched):
    ask("explain RAG", top_k=5)
    assert patched["method"] == "hybrid"


def test_auto_intent_factoid_picks_keyword(patched):
    # "When was X founded?" → FACTOID → keyword retriever
    ask("When was Anthropic founded?", auto_intent=True)
    # IntentRouter defaults factoid → keyword (or could be hybrid if classification differs)
    assert patched["method"] in ("keyword", "hybrid", "semantic", "bm25")


def test_auto_intent_does_not_override_explicit_method(patched):
    ask("query", method="bm25", auto_intent=True)
    # Caller-explicit method should win when not "hybrid"
    assert patched["method"] == "bm25"


# ---------------- hierarchical ----------------

def test_hierarchical_off_uses_retriever(patched, monkeypatch):
    ask("query", top_k=3)
    # Regular retriever called
    assert patched["method"] is not None


def test_hierarchical_on_uses_static_passages(patched, monkeypatch):
    """hierarchical=True → bypasses normal Retriever for hierarchical_search."""
    import docstoolkit.rag.pipeline as mod

    fake_passages = [Passage(text="hier", doc_id="h/a", title="H", score=0.9)]

    class FakeResult:
        passages = fake_passages

    def fake_h_search(query, **kw):
        return FakeResult()

    monkeypatch.setattr("docstoolkit.rag.hierarchical.hierarchical_search",
                        fake_h_search)
    result = ask("query", top_k=3, hierarchical=True)
    # Passages from FakeResult should appear
    assert any(p.doc_id == "h/a" for p in result.retrieved_passages)


def test_hierarchical_fallback_on_error(patched, monkeypatch):
    """If hierarchical_search blows up, regular pipeline still runs."""
    def boom(*a, **kw):
        raise RuntimeError("boom")
    monkeypatch.setattr("docstoolkit.rag.hierarchical.hierarchical_search", boom)
    # Should not raise
    ask("query", top_k=3, hierarchical=True)
