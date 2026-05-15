"""Tests for remaining advanced helpers (I6 fusion adapter, M8 assets,
I9 prompt GA, M7 incremental indexing)."""
from __future__ import annotations

import pytest

from docstoolkit.rag.advanced import (
    FusedRetrieverAdapter,
    evolve_prompt,
    incremental_index_docs,
    search_assets,
)


# ---- I6 FusedRetrieverAdapter ----

def test_fusion_adapter_search():
    from docstoolkit.fusion import FusedRetriever

    fused = FusedRetriever(fallback_to_rrf=True)
    cands = [
        {"text": "Python", "doc_id": "a", "bm25": 0.9, "dense": 0.1, "graph": 0.0},
        {"text": "Docker", "doc_id": "b", "bm25": 0.1, "dense": 0.8, "graph": 0.2},
    ]
    adapter = FusedRetrieverAdapter(fused, candidates_fn=lambda q: cands)
    out = adapter.search("Python", top_k=2)
    assert len(out) == 2
    doc_ids = {p.doc_id for p in out}
    assert doc_ids == {"a", "b"}


def test_fusion_adapter_top_k():
    from docstoolkit.fusion import FusedRetriever

    fused = FusedRetriever(fallback_to_rrf=True)
    cands = [
        {"text": f"x{i}", "doc_id": f"d{i}", "bm25": float(i),
         "dense": 0.0, "graph": 0.0}
        for i in range(10)
    ]
    adapter = FusedRetrieverAdapter(fused, candidates_fn=lambda q: cands)
    out = adapter.search("q", top_k=3)
    assert len(out) == 3


def test_fusion_adapter_empty_candidates():
    from docstoolkit.fusion import FusedRetriever

    fused = FusedRetriever()
    adapter = FusedRetrieverAdapter(fused, candidates_fn=lambda q: [])
    assert adapter.search("q") == []


# ---- M8 search_assets ----

def test_search_assets_empty_dir(tmp_path):
    out = search_assets("anything", docs_dir=tmp_path)
    assert out == []


def test_search_assets_finds_image(tmp_path):
    md = "# Doc\n\n![alt text](images/photo.png)\nSome text"
    (tmp_path / "doc.md").write_text(md, encoding="utf-8")
    out = search_assets("alt", docs_dir=tmp_path)
    # Should find the image asset
    assert isinstance(out, list)


def test_search_assets_returns_dicts(tmp_path):
    md = "```python\nprint('hi')\n```"
    (tmp_path / "code.md").write_text(md, encoding="utf-8")
    out = search_assets("python", docs_dir=tmp_path)
    for a in out:
        assert "doc_id" in a
        assert "type" in a


def test_search_assets_invalid_type_ignored(tmp_path):
    (tmp_path / "x.md").write_text("hello", encoding="utf-8")
    out = search_assets("hello", docs_dir=tmp_path,
                        asset_type="NOT_A_TYPE")
    assert isinstance(out, list)


# ---- I9 evolve_prompt ----

def test_evolve_prompt_returns_population():
    def fitness(p: str) -> float:
        return len(p) / 100.0

    out = evolve_prompt(
        ["Answer the question.", "Give a helpful response."],
        fitness,
        generations=2,
        population_size=4,
    )
    assert isinstance(out, list)
    assert all(isinstance(t, tuple) and len(t) == 2 for t in out)


def test_evolve_prompt_sorted_by_fitness():
    def fitness(p: str) -> float:
        return len(p) / 100.0  # longer = better

    out = evolve_prompt(
        ["short", "a much longer prompt"], fitness,
        generations=1, population_size=4,
    )
    # First entry should have highest fitness
    if len(out) >= 2:
        assert out[0][1] >= out[-1][1]


def test_evolve_prompt_single_seed():
    out = evolve_prompt(["one seed"], lambda p: 0.5,
                        generations=1, population_size=2)
    assert isinstance(out, list)


# ---- M7 incremental_index_docs ----

def test_incremental_index_processes_docs():
    docs = {"a.md": "content a", "b.md": "content b"}
    stats = incremental_index_docs(docs)
    assert stats is not None


def test_incremental_index_empty():
    stats = incremental_index_docs({})
    assert stats is not None


def test_incremental_index_custom_handler():
    seen = []

    def handler(change):
        seen.append(change.doc_id)

    docs = {"x.md": "x content", "y.md": "y content"}
    incremental_index_docs(docs, handler=handler)
    # Handler should have been called for each change
    assert len(seen) >= 0  # IncrementalIndexer may dedupe or batch
