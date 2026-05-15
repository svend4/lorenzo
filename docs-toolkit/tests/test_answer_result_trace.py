"""Phase III.1 + III.2 — AnswerResult.trace + to_trace_markdown().

Pin the contract: every pipeline branch emits an ordered trace and each
event has a non-negative t_ms and a payload dict.
"""
from __future__ import annotations

from unittest.mock import patch

import pytest

from docstoolkit.rag import ask, TraceEvent
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
        ][:top_k]


class _Answerer:
    def answer(self, system, user, model=""):
        return "answer", 0, 0.0


@pytest.fixture
def stub():
    with patch("docstoolkit.rag.pipeline.Retriever",
               lambda **kw: _Retriever()), \
         patch("docstoolkit.rag.pipeline.get_answerer",
               lambda name, **kw: _Answerer()):
        yield


def test_baseline_trace_has_retrieve_and_answer(stub):
    r = ask("q?", top_k=2)
    stages = [ev.stage for ev in r.trace]
    assert "retrieve" in stages
    assert "answer" in stages
    assert "assemble" in stages


def test_trace_events_are_traceevent_instances(stub):
    r = ask("q?", top_k=2)
    assert r.trace
    for ev in r.trace:
        assert isinstance(ev, TraceEvent)
        assert ev.t_ms >= 0.0
        assert isinstance(ev.payload, dict)


def test_trace_with_rerank(stub):
    from docstoolkit.rerank.reranker import TFIDFReranker
    r = ask("q?", top_k=2, reranker=TFIDFReranker())
    stages = [ev.stage for ev in r.trace]
    assert "rerank" in stages


def test_trace_with_facets_provenance_got(stub):
    r = ask("q?", top_k=2, with_facets=True, with_provenance=True,
            with_got=True, got_max_hypotheses=2)
    stages = [ev.stage for ev in r.trace]
    assert "facets" in stages
    assert "provenance" in stages
    assert "got" in stages


def test_trace_with_self_rag_emits_iter_events(stub):
    r = ask("q?", top_k=2, self_rag=True, self_rag_max_iters=2)
    stages = [ev.stage for ev in r.trace]
    # self_rag_iter should appear at the start (prepended by _self_rag_run)
    assert stages[0] == "self_rag_iter"
    # And the inner pipeline stages should still be there
    assert "retrieve" in stages
    assert "answer" in stages


def test_to_trace_markdown_renders_table(stub):
    r = ask("q?", top_k=2, with_facets=True)
    md = r.to_trace_markdown()
    assert md
    assert "## Trace" in md
    assert "| Stage |" in md
    assert "`retrieve`" in md
    assert "`facets`" in md


def test_to_trace_markdown_empty_when_no_trace():
    from docstoolkit.rag.types import AnswerResult
    r = AnswerResult(answer="x")
    assert r.to_trace_markdown() == ""


def test_trace_sum_close_to_duration_ms(stub):
    r = ask("q?", top_k=2, with_facets=True, with_provenance=True)
    trace_sum = sum(ev.t_ms for ev in r.trace)
    # duration_ms is wall-clock int, trace_sum is float; allow generous slack
    # because pipeline does some work outside instrumented blocks.
    assert trace_sum <= r.duration_ms + 100, (
        f"Trace sum {trace_sum:.2f} ms > duration {r.duration_ms} ms + 100"
    )
