"""Tests for metabolism.proposals (Sprint 80 / N1)."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from docstoolkit.metabolism import (
    LifecycleState,
    RewriteProposal,
    propose_rewrite,
    rank_stale_documents,
)


def _iso_days_ago(days: float) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()


# ---- propose_rewrite ----

def test_propose_returns_proposal():
    p = propose_rewrite("doc/a", "Python content",
                        sources=[("src/b", "Python tutorial")])
    assert isinstance(p, RewriteProposal)
    assert p.target_doc_id == "doc/a"


def test_propose_absorbs_relevant_source():
    target = "Python and RAG and agents and memory and tokens are concepts."
    src = "Python is great and RAG retrieves passages and agents use memory."
    p = propose_rewrite("doc/a", target,
                        sources=[("src/b", src)],
                        min_relevance=0.1)
    assert p.has_changes
    assert p.fragments[0].source_doc_id == "src/b"


def test_propose_rejects_unrelated_source():
    p = propose_rewrite("doc/a", "Python content",
                        sources=[("src/b", "completely unrelated cooking recipe")],
                        min_relevance=0.5)
    assert not p.has_changes
    assert p.rejected
    assert p.rejected[0][0] == "src/b"


def test_propose_marks_stale_when_old():
    p = propose_rewrite(
        "old/doc", "small text",
        sources=[],
        last_modified_iso=_iso_days_ago(365),
    )
    assert p.target_state == LifecycleState.STALE


def test_propose_marks_aging_when_medium():
    p = propose_rewrite(
        "med/doc", "small text",
        sources=[],
        last_modified_iso=_iso_days_ago(120),
    )
    assert p.target_state == LifecycleState.AGING


def test_propose_no_age_keeps_state():
    p = propose_rewrite("fresh/doc", "small text", sources=[])
    # Without last_modified_iso, age=0 → state stays FRESH
    assert p.target_state == LifecycleState.FRESH


def test_propose_to_markdown_renders():
    p = propose_rewrite(
        "doc/a", "Python and Docker",
        sources=[("src/b", "Python Docker containers run apps.")],
        min_relevance=0.1,
    )
    md = p.to_markdown()
    assert "Rewrite proposal" in md
    assert "doc/a" in md


def test_propose_suggested_content_includes_fragments():
    target = "Python content here matters."
    src = "Python and content matter to readers."
    p = propose_rewrite("doc/a", target,
                        sources=[("src/b", src)],
                        min_relevance=0.1)
    assert "Updates" in p.suggested_content
    assert "absorbed from src/b" in p.suggested_content


def test_propose_empty_sources():
    p = propose_rewrite("doc/a", "content", sources=[])
    assert p.fragments == []
    assert p.rejected == []


def test_propose_multiple_sources():
    target = "Python RAG"
    p = propose_rewrite(
        "doc/a", target,
        sources=[
            ("good", "Python tutorial RAG"),
            ("bad", "totally different topic xyz"),
            ("alsogood", "RAG with Python guide"),
        ],
        min_relevance=0.1,
    )
    # At least one good source absorbed; bad rejected
    src_ids = {f.source_doc_id for f in p.fragments}
    rej_ids = {r[0] for r in p.rejected}
    assert "good" in src_ids or "alsogood" in src_ids
    assert "bad" in rej_ids


# ---- rank_stale_documents ----

def test_rank_filters_by_threshold():
    docs = [
        ("new", "fresh", _iso_days_ago(10)),
        ("old", "stale", _iso_days_ago(400)),
        ("med", "mid", _iso_days_ago(120)),
    ]
    ranked = rank_stale_documents(docs, threshold_days=180.0)
    ids = [d[0] for d in ranked]
    assert "old" in ids
    assert "new" not in ids
    assert "med" not in ids


def test_rank_orders_oldest_first():
    docs = [
        ("a", "x", _iso_days_ago(400)),
        ("b", "x", _iso_days_ago(600)),
        ("c", "x", _iso_days_ago(500)),
    ]
    ranked = rank_stale_documents(docs, threshold_days=100.0)
    ids = [d[0] for d in ranked]
    assert ids == ["b", "c", "a"]


def test_rank_empty_input():
    assert rank_stale_documents([], threshold_days=180.0) == []


def test_rank_no_stale_returns_empty():
    docs = [("a", "x", _iso_days_ago(10))]
    assert rank_stale_documents(docs, threshold_days=180.0) == []
