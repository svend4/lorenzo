"""Tests for ask() + facets/filters/provenance integration.

Covers Sprint 55 / S2 (facets, filters) and Sprint 61 / I3 (provenance).
"""
from __future__ import annotations

import pytest

from docstoolkit.rag.pipeline import RAGPipeline, ask
from docstoolkit.rag.types import Passage, RAGQuery


class _StubRetriever:
    def __init__(self, passages):
        self._p = passages
        self.last_top_k = 0

    def search(self, query, top_k):
        self.last_top_k = top_k
        return list(self._p[:top_k])


class _StubAnswerer:
    def answer(self, system, user, model=""):
        return "Yodoca is a memory project. AgentFS uses RAG.", 0, 0.0


@pytest.fixture
def patched(monkeypatch):
    import docstoolkit.rag.pipeline as mod

    passages = [
        Passage(text="Yodoca is a memory project for agents.",
                doc_id="docs/yodoca", title="Yodoca", score=0.9),
        Passage(text="AgentFS uses RAG and memory.",
                doc_id="docs/agentfs", title="AgentFS", score=0.8),
        Passage(text="tests skipped",
                doc_id="tests/skip", title="Skip", score=0.7),
        Passage(text="tag:rag intro material",
                doc_id="docs/intro", title="Intro", score=0.6),
    ]
    retriever = _StubRetriever(passages)
    monkeypatch.setattr(mod, "Retriever", lambda **kw: retriever)
    monkeypatch.setattr(mod, "get_answerer", lambda name, **kw: _StubAnswerer())
    return retriever


# ---------------- facets ----------------

def test_ask_with_facets_returns_aggregations(patched):
    result = ask("query", top_k=4, with_facets=True)
    assert result.facets
    sec = next(a for a in result.facets if a.field_name == "section")
    assert dict(sec.values).get("docs") == 3


def test_ask_without_facets_empty_by_default(patched):
    result = ask("query", top_k=4)
    assert result.facets == []


def test_ask_custom_facet_fields(patched):
    result = ask("query", top_k=4, with_facets=True,
                 facet_fields=("section",))
    assert len(result.facets) == 1
    assert result.facets[0].field_name == "section"


# ---------------- filters ----------------

def test_ask_filter_section_only(patched):
    result = ask("query", top_k=3, filters={"section": "docs"})
    doc_ids = [p.doc_id for p in result.retrieved_passages]
    assert all(d.startswith("docs/") for d in doc_ids)


def test_ask_filter_overfetches(patched):
    """When filtering, pipeline must overfetch so the filter has candidates."""
    ask("query", top_k=2, filters={"section": "docs"})
    assert patched.last_top_k >= 2 * 4


def test_ask_filter_limits_to_top_k(patched):
    result = ask("query", top_k=2, filters={"section": "docs"})
    assert len(result.retrieved_passages) <= 2


def test_ask_filter_unknown_section_returns_empty(patched):
    result = ask("query", top_k=3, filters={"section": "ghosts"})
    # No passages match
    assert result.retrieved_passages == [] or \
        all(p.doc_id.startswith("ghosts/") for p in result.retrieved_passages)


def test_ask_filter_combines_with_facets(patched):
    result = ask("query", top_k=3,
                 filters={"section": "docs"},
                 with_facets=True)
    if result.facets:
        sec = next((a for a in result.facets if a.field_name == "section"),
                   None)
        # After filtering, only `docs` should show in facets
        if sec and sec.values:
            assert all(v == "docs" for v, _ in sec.values)


# ---------------- provenance ----------------

def test_ask_with_provenance_returns_provenance(patched):
    result = ask("Yodoca?", top_k=3, with_provenance=True)
    assert result.provenance is not None
    # ProvenancedAnswer dataclass: must have text + claims
    assert hasattr(result.provenance, "text")
    assert hasattr(result.provenance, "claims")


def test_ask_without_provenance_none_default(patched):
    result = ask("Yodoca?", top_k=3)
    assert result.provenance is None


def test_provenance_overall_confidence_is_float(patched):
    result = ask("Yodoca?", top_k=3, with_provenance=True)
    if result.provenance is not None:
        oc = result.provenance.overall_confidence
        assert 0.0 <= oc <= 1.0


# ---------------- composition ----------------

def test_ask_compose_filters_facets_provenance(patched):
    result = ask(
        "Yodoca?",
        top_k=2,
        filters={"section": "docs"},
        with_facets=True,
        with_provenance=True,
    )
    # All three layers active
    assert result.provenance is not None
    assert result.facets
    assert all(p.doc_id.startswith("docs/")
               for p in result.retrieved_passages)
