"""Tests for ask(at_commit=...) time-travel (Sprint 79 / I8)."""
from __future__ import annotations

import pytest

from docstoolkit.rag.pipeline import ask
from docstoolkit.rag.types import Passage


def test_at_commit_invokes_temporal_query(monkeypatch):
    """When at_commit set, ask() uses query_at_time() and skips normal pipeline."""
    captured = {}

    from docstoolkit.temporal import TemporalAnswer

    def fake_qat(query, commit_or_ts, **kw):
        captured["query"] = query
        captured["commit"] = commit_or_ts
        return TemporalAnswer(
            answer="historical answer",
            passages=[Passage(text="old text", doc_id="d", title="D",
                              score=0.5)],
            timestamp="2024-01-01",
            commit="abc1234",
            doc_count=1,
        )

    monkeypatch.setattr("docstoolkit.temporal.query_at_time", fake_qat)
    r = ask("query", at_commit="abc1234", top_k=3)
    assert r.answer == "historical answer"
    assert r.at_commit == "abc1234"
    assert captured["commit"] == "abc1234"


def test_at_commit_empty_passes_through(monkeypatch):
    """Without at_commit, normal pipeline runs."""
    import docstoolkit.rag.pipeline as mod

    class _R:
        def search(self, q, top_k):
            return [Passage(text="t", doc_id="d", title="D", score=0.5)]

    class _A:
        def answer(self, s, u, model=""):
            return "fresh answer", 0, 0.0

    monkeypatch.setattr(mod, "Retriever", lambda **kw: _R())
    monkeypatch.setattr(mod, "get_answerer", lambda name, **kw: _A())
    r = ask("query", top_k=3)
    assert r.at_commit == ""
    assert r.answer == "fresh answer"


def test_at_commit_fallback_on_error(monkeypatch):
    """If temporal raises, ask() falls back to normal retrieval."""
    import docstoolkit.rag.pipeline as mod

    class _R:
        def search(self, q, top_k):
            return [Passage(text="t", doc_id="d", title="D", score=0.5)]

    class _A:
        def answer(self, s, u, model=""):
            return "live answer", 0, 0.0

    monkeypatch.setattr(mod, "Retriever", lambda **kw: _R())
    monkeypatch.setattr(mod, "get_answerer", lambda name, **kw: _A())

    def boom(*a, **kw):
        raise RuntimeError("git not available")

    monkeypatch.setattr("docstoolkit.temporal.query_at_time", boom)
    r = ask("query", at_commit="abc1234", top_k=3)
    # Should fall back to normal pipeline → "live answer"
    assert r.answer == "live answer"
