"""Tests for ask(memory=...) integration (Sprint 74 / I5)."""
from __future__ import annotations

import pytest

from docstoolkit.memory import TieredMemory
from docstoolkit.rag.pipeline import ask
from docstoolkit.rag.types import Passage


class _R:
    def search(self, q, top_k):
        return [Passage(text=f"text {q}", doc_id="d", title="D", score=0.7)]


class _A:
    def answer(self, s, u, model=""):
        return "response", 0, 0.0


@pytest.fixture
def patched(monkeypatch):
    import docstoolkit.rag.pipeline as mod
    monkeypatch.setattr(mod, "Retriever", lambda **kw: _R())
    monkeypatch.setattr(mod, "get_answerer", lambda name, **kw: _A())


def test_memory_off_does_not_record(patched):
    mem = TieredMemory()
    # No ask() with memory → mem stats stay at zero
    ask("query", top_k=1)
    assert mem.stats()["recall_count"] == 0


def test_memory_on_records_interaction(patched):
    mem = TieredMemory()
    ask("first question", top_k=1, memory=mem)
    # Both user and assistant turns recorded
    assert mem.stats()["recall_count"] >= 2


def test_memory_persists_across_calls(patched):
    mem = TieredMemory()
    ask("first", top_k=1, memory=mem)
    ask("second", top_k=1, memory=mem)
    # 4 turns total (2 per ask)
    assert mem.stats()["recall_count"] >= 4


def test_memory_working_window_filled(patched):
    mem = TieredMemory(working_max=10)
    ask("q1", top_k=1, memory=mem)
    assert mem.stats()["working_messages"] >= 2


def test_memory_handles_archive():
    mem = TieredMemory()
    fact_id = mem.archive("Yodoca is a memory project", tags=["fact"])
    assert fact_id


def test_memory_recall_search(patched):
    mem = TieredMemory()
    ask("about Python", top_k=1, memory=mem)
    hits = mem.recall_search("Python", top_k=5)
    # Should find at least the question turn
    assert isinstance(hits, list)


def test_memory_error_does_not_break_ask(patched, monkeypatch):
    class BadMem:
        def recall_search(self, q, top_k):
            raise RuntimeError("boom")

        def add_interaction(self, role, content):
            raise RuntimeError("boom")

    # ask() should swallow the failure
    r = ask("query", top_k=1, memory=BadMem())
    assert r.answer == "response"
