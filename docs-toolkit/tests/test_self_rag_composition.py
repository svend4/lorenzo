"""Phase II.1 — `self_rag=True` must compose with the reasoning flags.

Before II.1 `_self_rag_run` had its own short pipeline that dropped
`with_got` / `with_debate` / `with_negotiation` / `memory` / `personality`.
These contract tests pin the new behaviour: every reasoning trace appears
on the final `AnswerResult` even when self-RAG is on.
"""
from __future__ import annotations

from unittest.mock import patch

import pytest

from docstoolkit.rag import ask, ask_with_reasoning, ask_full_stack
from docstoolkit.rag.types import Passage


class _Retriever:
    def search(self, query, top_k=5):
        return [
            Passage(text="Python is used for RAG.",
                    doc_id="d1", title="Python", score=0.92),
            Passage(text="Memory helps long-running agents.",
                    doc_id="d2", title="Memory", score=0.85),
            Passage(text="Docker enables reproducible deploys.",
                    doc_id="d3", title="Docker", score=0.7),
            Passage(text="RAG combines retrieval with generation.",
                    doc_id="d4", title="RAG", score=0.65),
        ][:top_k]


class _Answerer:
    def answer(self, system, user, model=""):
        return "RAG and memory together enable robust agents.", 0, 0.0


@pytest.fixture
def stub():
    with patch("docstoolkit.rag.pipeline.Retriever",
               lambda **kw: _Retriever()), \
         patch("docstoolkit.rag.pipeline.get_answerer",
               lambda name, **kw: _Answerer()):
        yield


def test_self_rag_composes_with_got(stub):
    r = ask("Why do agents need memory?",
            self_rag=True, self_rag_max_iters=2,
            with_got=True, got_max_hypotheses=3, top_k=3)
    assert r.answer
    assert r.got_result is not None, (
        "Phase II.1: self_rag must not silently drop with_got"
    )


def test_self_rag_composes_with_debate(stub):
    r = ask("Why do agents need memory?",
            self_rag=True, self_rag_max_iters=2,
            with_debate=True, debate_max_rounds=1, top_k=3)
    assert r.answer
    assert r.debate_result is not None, (
        "Phase II.1: self_rag must not silently drop with_debate"
    )


def test_self_rag_composes_with_negotiation(stub):
    r = ask("Why do agents need memory?",
            self_rag=True, self_rag_max_iters=2,
            with_negotiation=True, negotiation_budget=3, top_k=3)
    assert r.answer
    assert r.auction_result is not None, (
        "Phase II.1: self_rag must not silently drop with_negotiation"
    )


def test_self_rag_composes_all_three(stub):
    r = ask("Why do agents need memory?",
            self_rag=True, self_rag_max_iters=2,
            with_got=True, got_max_hypotheses=3,
            with_debate=True, debate_max_rounds=1,
            with_negotiation=True, negotiation_budget=3,
            top_k=3)
    assert r.answer
    assert r.got_result is not None
    assert r.debate_result is not None
    assert r.auction_result is not None


def test_ask_with_reasoning_preset_enables_self_rag(stub):
    """Phase II.2 — the preset now includes self_rag again."""
    r = ask_with_reasoning("Why do agents need memory?", top_k=3)
    assert r.answer
    assert r.got_result is not None
    assert r.debate_result is not None


def test_ask_full_stack_preset_enables_self_rag(stub):
    """Phase II.2 — full-stack preset also includes self_rag again."""
    r = ask_full_stack("Why do agents need memory?", top_k=3)
    assert r.answer
    assert r.got_result is not None
    assert r.debate_result is not None
    assert r.auction_result is not None


def test_self_rag_alone_unchanged(stub):
    """Regression guard: bare self_rag without reasoning flags still works."""
    r = ask("Why do agents need memory?",
            self_rag=True, self_rag_max_iters=2, top_k=3)
    assert r.answer
    # No reasoning flags → these stay None
    assert r.got_result is None
    assert r.debate_result is None
    assert r.auction_result is None
