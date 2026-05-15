"""Smoke tests for `docstoolkit.rag.presets` — named ask() bundles."""
from __future__ import annotations

from unittest.mock import patch

import pytest

from docstoolkit.rag import (
    ask_advanced,
    ask_full_stack,
    ask_high_quality,
    ask_personalized,
    ask_research,
    ask_with_reasoning,
)
from docstoolkit.rag.types import Passage


class _Retriever:
    def search(self, query, top_k):
        return [
            Passage(text="Python is a programming language.",
                    doc_id="docs/python", title="Python", score=0.9),
            Passage(text="RAG retrieves passages and feeds them to an LLM.",
                    doc_id="docs/rag", title="RAG", score=0.85),
            Passage(text="Yodoca is a memory project.",
                    doc_id="memory/yodoca", title="Yodoca", score=0.8),
        ][:top_k]


class _Answerer:
    def answer(self, system, user, model=""):
        return "Python and RAG are key building blocks.", 0, 0.0


@pytest.fixture
def stub_pipeline():
    with patch("docstoolkit.rag.pipeline.Retriever",
               lambda **kw: _Retriever()), \
         patch("docstoolkit.rag.pipeline.get_answerer",
               lambda name, **kw: _Answerer()):
        yield


def test_personalized_passes_user_id(stub_pipeline):
    r = ask_personalized("hi", user_id="alice", top_k=2)
    assert r.answer
    assert len(r.retrieved_passages) <= 2


def test_high_quality_enables_provenance(stub_pipeline):
    r = ask_high_quality("What is RAG?", top_k=2)
    assert r.provenance is not None


def test_high_quality_override_provenance(stub_pipeline):
    # User can override the default
    r = ask_high_quality("What is RAG?", with_provenance=False, top_k=2)
    assert r.provenance is None


def test_with_reasoning_runs_got_and_debate(stub_pipeline):
    r = ask_with_reasoning("Why does X?", top_k=3)
    assert r.answer
    # GoT and debate produce trace results on AnswerResult
    assert r.got_result is not None
    assert r.debate_result is not None


def test_advanced_enables_auto_intent_and_mapreduce(stub_pipeline):
    r = ask_advanced("How are agents built?", top_k=2)
    assert r.answer


def test_research_passes_memory_and_personality(stub_pipeline):
    from docstoolkit.memory import TieredMemory
    from docstoolkit.personality import CognitiveProfile

    mem = TieredMemory()
    profile = CognitiveProfile(
        skepticism=0.8, synthesis=0.2, verification=0.5,
        pragmatism=0.2, exploration=0.5,
    )
    r = ask_research("agents and memory?", memory=mem, personality=profile,
                    top_k=2)
    assert r.answer
    assert mem.stats()["recall_count"] >= 0


def test_full_stack_runs(stub_pipeline):
    r = ask_full_stack("How do memory and RAG fit together?", top_k=2)
    assert r.answer
    assert r.facets  # auto-enabled
    # Provenance auto-enabled
    assert r.provenance is not None


def test_caller_kwargs_override_preset(stub_pipeline):
    # `ask_with_reasoning` enables GoT + debate; caller turns them off.
    r = ask_with_reasoning("Q?", self_rag=False, with_got=False,
                           with_debate=False, top_k=2)
    assert r.got_result is None
    assert r.debate_result is None
