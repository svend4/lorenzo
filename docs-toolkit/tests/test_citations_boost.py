"""Tests for PageRank-boosted retrieval (Sprint 56 / S4)."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from docstoolkit.citations.boost import (
    PageRankBoostedRetriever,
    boost_scores,
    build_pr_lookup,
)
from docstoolkit.rag.types import Passage


def _p(doc_id: str, score: float = 0.5) -> Passage:
    return Passage(text=f"text of {doc_id}", doc_id=doc_id,
                   title=doc_id, score=score)


class MockRetriever:
    def __init__(self, passages: list[Passage]):
        self._p = passages

    def search(self, query: str, top_k: int = 5) -> list[Passage]:
        return list(self._p[:top_k])


# ---------- boost_scores ----------

def test_boost_scores_empty_pr_returns_as_is():
    ps = [_p("a", 0.5), _p("b", 0.6)]
    out = boost_scores(ps, {})
    assert [x.score for x in out] == [0.5, 0.6]


def test_boost_scores_zero_max_pr_returns_as_is():
    ps = [_p("a", 0.5)]
    out = boost_scores(ps, {"a": 0.0})
    assert out[0].score == 0.5


def test_boost_scores_uses_alpha():
    ps = [_p("a", 1.0), _p("b", 1.0)]
    # pr=max for `a`, 0 for `b`; alpha=0.5, cap=1.0
    out = boost_scores(ps, {"a": 1.0, "b": 0.0}, alpha=0.5, cap=1.0)
    assert out[0].score == pytest.approx(1.5)
    assert out[1].score == pytest.approx(1.0)


def test_boost_scores_respects_cap():
    ps = [_p("a", 1.0)]
    # cap should limit the boost
    out = boost_scores(ps, {"a": 1.0}, alpha=1.0, cap=0.4)
    # max boost = 1 + 1.0 * 0.4 = 1.4
    assert out[0].score == pytest.approx(1.4)


def test_boost_scores_returns_new_passages():
    src = _p("a", 0.5)
    out = boost_scores([src], {"a": 1.0}, alpha=0.5, cap=1.0)
    assert out[0] is not src
    assert src.score == 0.5  # original untouched


def test_boost_scores_unknown_doc_no_boost():
    ps = [_p("a", 0.7), _p("unknown", 0.7)]
    out = boost_scores(ps, {"a": 1.0}, alpha=0.5, cap=1.0)
    # `unknown` has no PR → boost factor 1.0
    assert out[1].score == pytest.approx(0.7)


# ---------- PageRankBoostedRetriever ----------

def test_pr_boosted_retriever_promotes_authoritative_doc():
    ps = [_p("low_authority", 0.7), _p("high_authority", 0.6),
          _p("filler1", 0.4), _p("filler2", 0.3)]
    base = MockRetriever(ps)
    boosted = PageRankBoostedRetriever(
        base=base,
        pr_scores={"high_authority": 1.0, "low_authority": 0.0},
        alpha=1.0, cap=1.0,
    )
    out = boosted.search("q", top_k=2)
    # high_authority should rank first thanks to boost (0.6 * 2.0 = 1.2 > 0.7)
    assert out[0].doc_id == "high_authority"
    assert out[0].score > out[1].score


def test_pr_boosted_retriever_no_scores_passes_through():
    ps = [_p("a", 0.7), _p("b", 0.6), _p("c", 0.5), _p("d", 0.4)]
    base = MockRetriever(ps)
    boosted = PageRankBoostedRetriever(base=base, pr_scores={})
    out = boosted.search("q", top_k=2)
    assert [x.doc_id for x in out] == ["a", "b"]


def test_pr_boosted_retriever_top_k_truncates():
    ps = [_p(f"d{i}", 0.5) for i in range(10)]
    base = MockRetriever(ps)
    boosted = PageRankBoostedRetriever(base=base, pr_scores={})
    out = boosted.search("q", top_k=3)
    assert len(out) == 3


def test_pr_boosted_retriever_uses_2x_window():
    """Base retriever should be asked for top_k*2 candidates."""
    captured = {}

    class Recorder:
        def search(self, query, top_k):
            captured["top_k"] = top_k
            return [_p(f"d{i}", 0.5) for i in range(top_k)]

    boosted = PageRankBoostedRetriever(base=Recorder(), pr_scores={})
    boosted.search("q", top_k=4)
    assert captured["top_k"] == 8


# ---------- build_pr_lookup integration ----------

def test_build_pr_lookup_from_corpus(tmp_path):
    (tmp_path / "a.md").write_text("link to [b](b.md)", encoding="utf-8")
    (tmp_path / "b.md").write_text("link to [c](c.md)", encoding="utf-8")
    (tmp_path / "c.md").write_text("just text", encoding="utf-8")
    pr = build_pr_lookup(tmp_path)
    assert "a" in pr and "b" in pr and "c" in pr
    # c has more incoming → should not be smallest
    assert pr["c"] > 0


def test_pr_boosted_retriever_lazy_loads_from_corpus(tmp_path):
    (tmp_path / "x.md").write_text("see [y](y.md)", encoding="utf-8")
    (tmp_path / "y.md").write_text("end", encoding="utf-8")
    base = MockRetriever([_p("x", 0.5), _p("y", 0.5),
                          _p("pad1", 0.4), _p("pad2", 0.3)])
    boosted = PageRankBoostedRetriever(base=base, corpus_dir=tmp_path,
                                       alpha=0.5, cap=1.0)
    out = boosted.search("q", top_k=2)
    # y has one incoming link → should rank above x
    by_id = {p.doc_id: p.score for p in out}
    assert by_id["y"] >= by_id["x"]
