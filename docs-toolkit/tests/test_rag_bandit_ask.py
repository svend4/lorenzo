"""Tests for ask_with_bandit (Sprint 76 / I7)."""
from __future__ import annotations

import pytest

from docstoolkit.bandit import BanditExperiment
from docstoolkit.rag.bandit_ask import ask_with_bandit, evaluate_record
from docstoolkit.rag.types import Passage


class _R:
    def __init__(self):
        self.last_method: str | None = None

    def search(self, q, top_k):
        return [Passage(text="t", doc_id="d", title="D", score=0.7)]


class _A:
    def answer(self, s, u, model=""):
        return "answer", 0, 0.0


@pytest.fixture
def patched(monkeypatch):
    import docstoolkit.rag.pipeline as mod
    captured = {"method": None}

    def fake_retriever(method="hybrid", model=""):
        captured["method"] = method
        return _R()

    monkeypatch.setattr(mod, "Retriever", fake_retriever)
    monkeypatch.setattr(mod, "get_answerer", lambda name, **kw: _A())
    return captured


def test_picks_a_variant(patched):
    exp = BanditExperiment("t", ["bm25", "hybrid"])
    result, picked = ask_with_bandit(
        "q", exp, {"bm25": {"method": "bm25"},
                   "hybrid": {"method": "hybrid"}},
    )
    assert picked in ("bm25", "hybrid")
    assert patched["method"] == picked


def test_empty_variants_raises(patched):
    exp = BanditExperiment("t", ["x"])
    with pytest.raises(ValueError):
        ask_with_bandit("q", exp, {})


def test_evaluate_record_success(patched):
    exp = BanditExperiment("t", ["bm25"])
    result, picked = ask_with_bandit("q", exp, {"bm25": {"method": "bm25"}})
    succ = evaluate_record(exp, picked, result, success_threshold=0.5)
    assert succ is True


def test_evaluate_record_failure_on_error(patched):
    from docstoolkit.rag.types import AnswerResult
    exp = BanditExperiment("t", ["bm25"])
    fake = AnswerResult(answer="err", error="boom")
    succ = evaluate_record(exp, "bm25", fake)
    assert succ is False


def test_evaluate_record_failure_on_low_score(patched):
    from docstoolkit.rag.types import AnswerResult
    weak = Passage(text="x", doc_id="d", title="D", score=0.05)
    fake = AnswerResult(answer="a", retrieved_passages=[weak])
    exp = BanditExperiment("t", ["bm25"])
    succ = evaluate_record(exp, "bm25", fake, success_threshold=0.3)
    assert succ is False
