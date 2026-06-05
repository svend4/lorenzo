"""Tests for ask(self_rag=True) integration (Sprint 70 / I1)."""
from __future__ import annotations

import pytest

from docstoolkit.rag.pipeline import ask
from docstoolkit.rag.types import Passage


class _StubRetriever:
    def __init__(self, passages):
        self._p = passages
        self.calls: list[tuple[str, int]] = []

    def search(self, query, top_k):
        self.calls.append((query, top_k))
        return list(self._p[:top_k])


class _StubAnswerer:
    """Echos the query so reflect_on_answer can score overlap."""

    def __init__(self, fixed: str | None = None):
        self.fixed = fixed

    def answer(self, system, user, model=""):
        if self.fixed is not None:
            return self.fixed, 0, 0.0
        # Pull "Q:" line from user prompt to echo
        return user[-200:], 0, 0.0


@pytest.fixture
def patched_high(monkeypatch):
    """Stubs retriever + answerer; answer trivially matches passages."""
    import docstoolkit.rag.pipeline as mod
    passages = [
        Passage(text="Yodoca memory project agents",
                doc_id="docs/yodoca", title="Yodoca", score=0.9),
    ]
    retriever = _StubRetriever(passages)
    monkeypatch.setattr(mod, "Retriever", lambda **kw: retriever)
    monkeypatch.setattr(
        mod, "get_answerer",
        lambda name, **kw: _StubAnswerer("Yodoca memory project agents."),
    )
    return retriever


@pytest.fixture
def patched_low(monkeypatch):
    """Answer is unrelated to passages → reflect score should be low."""
    import docstoolkit.rag.pipeline as mod
    passages = [
        Passage(text="cars and bikes", doc_id="d/x", title="X", score=0.5),
    ]
    retriever = _StubRetriever(passages)
    monkeypatch.setattr(mod, "Retriever", lambda **kw: retriever)
    monkeypatch.setattr(
        mod, "get_answerer",
        lambda name, **kw: _StubAnswerer("zzz"),
    )
    return retriever


def test_self_rag_off_runs_one_iteration(patched_high):
    ask("Yodoca?", top_k=1)
    assert len(patched_high.calls) == 1


def test_self_rag_on_runs_multiple_iterations(patched_low):
    """Low-confidence answer → loop retries up to max_iters."""
    ask("rare topic", top_k=1, self_rag=True, self_rag_max_iters=3,
        self_rag_threshold=8.0)
    assert len(patched_low.calls) >= 2


def test_self_rag_stops_early_on_high_confidence(patched_high):
    """High confidence on first iteration → no second call."""
    ask("Yodoca", top_k=1, self_rag=True, self_rag_max_iters=4,
        self_rag_threshold=0.0)
    # threshold 0.0 means accept anything → 1 call only
    assert len(patched_high.calls) == 1


def test_self_rag_respects_max_iters(patched_low):
    ask("q", top_k=1, self_rag=True, self_rag_max_iters=2,
        self_rag_threshold=10.0)  # impossible — always retries
    assert len(patched_low.calls) <= 2


def test_self_rag_returns_answer_result(patched_high):
    result = ask("Yodoca?", top_k=1, self_rag=True)
    # Same shape as regular ask
    assert hasattr(result, "answer")
    assert hasattr(result, "retrieved_passages")
    assert hasattr(result, "duration_ms")


def test_self_rag_composes_with_facets(patched_high):
    result = ask("Yodoca?", top_k=1, self_rag=True, with_facets=True)
    # facets list should be present (potentially empty)
    assert isinstance(result.facets, list)
