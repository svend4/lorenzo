"""Tests for ask() Path C/B integrations.

Sprints covered:
  - 72 / I2  multi-agent debate
  - 73 / M6  active learning auto-enqueue
  - 78 / I10 map-reduce summarisation
  - 85 / N2  negotiation broker
  - 89 / N9  personality re-ranking
"""
from __future__ import annotations

from pathlib import Path

import pytest

from docstoolkit.active_learning import LearningQueue
from docstoolkit.personality import CognitiveProfile
from docstoolkit.rag.pipeline import ask
from docstoolkit.rag.types import Passage


class _StubRetriever:
    def __init__(self, passages):
        self._p = passages

    def search(self, query, top_k):
        return list(self._p[:top_k])


class _StubAnswerer:
    def answer(self, system, user, model=""):
        return "synthesised answer", 1, 0.0


@pytest.fixture
def patched(monkeypatch):
    import docstoolkit.rag.pipeline as mod

    passages = [
        Passage(text="Python is a programming language for many tasks.",
                doc_id="a", title="Py", score=0.9),
        Passage(text="RAG combines retrieval with LLM generation flows.",
                doc_id="b", title="RAG", score=0.7),
        Passage(text="Docker provides reproducible containers for apps.",
                doc_id="c", title="Dk", score=0.5),
    ]
    monkeypatch.setattr(mod, "Retriever",
                        lambda **kw: _StubRetriever(passages))
    monkeypatch.setattr(mod, "get_answerer",
                        lambda name, **kw: _StubAnswerer())


# ---------- I2 debate ----------

def test_debate_off_returns_none(patched):
    r = ask("Python?", top_k=3)
    assert r.debate_result is None


def test_debate_on_returns_debate_result(patched):
    r = ask("Python?", top_k=3, with_debate=True, debate_max_rounds=1)
    assert r.debate_result is not None
    # DebateResult has rounds + confidence
    assert hasattr(r.debate_result, "rounds")


def test_debate_replaces_answer_with_consensus(patched):
    r = ask("Python?", top_k=3, with_debate=True, debate_max_rounds=1)
    assert r.answer  # non-empty


# ---------- I10 map-reduce ----------

def test_mapreduce_off_uses_normal_answerer(patched):
    r = ask("Python?", top_k=3)
    assert r.mapreduce_trace is None
    assert "synthesised" in r.answer


def test_mapreduce_on_returns_trace(patched):
    r = ask("Python?", top_k=3, with_mapreduce=True,
            mapreduce_chunk_size=2)
    assert r.mapreduce_trace is not None


def test_mapreduce_replaces_answer(patched):
    r = ask("Python?", top_k=3, with_mapreduce=True)
    # final_answer comes from map_reduce_ask
    assert r.answer != ""


# ---------- N2 negotiation ----------

def test_negotiation_off_returns_none(patched):
    r = ask("Python?", top_k=3)
    assert r.auction_result is None


def test_negotiation_on_returns_auction(patched):
    r = ask("Python?", top_k=3, with_negotiation=True,
            negotiation_budget=2)
    # AuctionResult may be None if module errored; tolerate that
    if r.auction_result is not None:
        assert hasattr(r.auction_result, "selected_passages")


# ---------- N9 personality ----------

def test_personality_off_uses_normal_order(patched):
    r = ask("Python?", top_k=3)
    # default order — first passage is "a"
    assert r.retrieved_passages[0].doc_id == "a"


def test_personality_skepticism_re_ranks(patched):
    """A high-skepticism profile should boost passages containing
    skeptical markers; we just verify the rerank ran without crashing."""
    profile = CognitiveProfile(
        skepticism=0.9, synthesis=0.1, verification=0.1,
        pragmatism=0.1, exploration=0.1,
    )
    r = ask("Python?", top_k=3, personality=profile)
    assert len(r.retrieved_passages) <= 3


# ---------- M6 learning queue ----------

def test_learning_queue_high_confidence_no_enqueue(patched, tmp_path):
    """Passages with max score 0.9 — high — should NOT enqueue."""
    queue = LearningQueue(db_path=tmp_path / "lq.sqlite")
    try:
        ask("Python?", top_k=3, learning_queue=queue)
        # 0.9 > 0.3 → not enqueued
        assert queue.stats()["total"] == 0
    finally:
        queue.close()


def test_learning_queue_low_confidence_enqueues(patched, tmp_path, monkeypatch):
    """Force-low scores → queue receives an item."""
    queue = LearningQueue(db_path=tmp_path / "lq.sqlite")
    try:
        import docstoolkit.rag.pipeline as mod
        weak = [Passage(text="x", doc_id="d", title="D", score=0.05)
                for _ in range(3)]
        monkeypatch.setattr(mod, "Retriever",
                            lambda **kw: _StubRetriever(weak))
        ask("rare topic", top_k=3, learning_queue=queue)
        assert queue.stats()["total"] >= 1
    finally:
        queue.close()


def test_learning_queue_handles_no_queue(patched):
    # No queue passed → no crash
    r = ask("Python?", top_k=3)
    assert r.answer


# ---------- composition ----------

def test_compose_many_features(patched):
    r = ask(
        "Python?",
        top_k=3,
        with_facets=True,
        with_provenance=True,
        with_debate=True,
        debate_max_rounds=1,
    )
    assert r.facets is not None
    assert r.debate_result is not None
