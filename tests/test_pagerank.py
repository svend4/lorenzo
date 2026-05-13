"""
Tests for scripts/improve_pagerank.py.

Coverage:
  - extract_links()     — link extraction from markdown text
  - build_graph()       — directed graph construction
  - compute_pagerank()  — PageRank iteration and convergence
  - normalise()         — score normalisation
"""
import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_pagerank")


# ── extract_links ─────────────────────────────────────────────────────────────

@pytest.fixture()
def fake_repo(tmp_path, monkeypatch):
    """A temporary directory that acts as the repo root, with a docs/ sub-dir."""
    docs = tmp_path / "docs"
    docs.mkdir()
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", docs)
    return tmp_path, docs


def test_extract_links_markdown_relative(fake_repo):
    root, docs = fake_repo
    (docs / "bar.md").write_text("x")
    text = "[foo](bar.md)"
    links = mod.extract_links(text, docs)
    assert any("bar.md" in l for l in links)


def test_extract_links_absolute_url_skipped(fake_repo):
    _, docs = fake_repo
    text = "[ext](https://example.com/page.md)"
    links = mod.extract_links(text, docs)
    assert links == []


def test_extract_links_wikilink(fake_repo):
    _, docs = fake_repo
    (docs / "TARGET.md").write_text("content")
    text = "[[TARGET]]"
    links = mod.extract_links(text, docs)
    assert any("TARGET.md" in l for l in links)


def test_extract_links_wikilink_with_alias(fake_repo):
    _, docs = fake_repo
    (docs / "FOO.md").write_text("x")
    text = "[[FOO|Display Name]]"
    links = mod.extract_links(text, docs)
    assert any("FOO.md" in l for l in links)


def test_extract_links_deduplication(fake_repo):
    _, docs = fake_repo
    (docs / "page.md").write_text("x")
    text = "[a](page.md) [b](page.md)"
    links = mod.extract_links(text, docs)
    assert len([l for l in links if "page.md" in l]) == 1


def test_extract_links_anchor_stripped(fake_repo):
    _, docs = fake_repo
    (docs / "doc.md").write_text("x")
    text = "[text](doc.md#section)"
    links = mod.extract_links(text, docs)
    assert any("doc.md" in l for l in links)
    assert not any("#" in l for l in links)


# ── build_graph ───────────────────────────────────────────────────────────────

def test_build_graph_returns_tuple(fake_repo):
    out_edges, nodes = mod.build_graph()
    assert isinstance(out_edges, dict)
    assert isinstance(nodes, set)


def test_build_graph_finds_edges(fake_repo):
    _, docs = fake_repo
    a = docs / "a.md"
    b = docs / "b.md"
    a.write_text("[link](b.md)")
    b.write_text("no links here")
    out_edges, nodes = mod.build_graph()
    assert len(nodes) >= 2
    edge_count = sum(len(v) for v in out_edges.values())
    assert edge_count >= 1


# ── compute_pagerank ──────────────────────────────────────────────────────────

def test_compute_pagerank_empty():
    result = mod.compute_pagerank({}, set())
    assert result == {}


def test_compute_pagerank_single_node():
    nodes = {"a.md"}
    result = mod.compute_pagerank({}, nodes)
    assert "a.md" in result
    assert result["a.md"] > 0


def test_compute_pagerank_sums_to_one():
    nodes = {"a.md", "b.md", "c.md"}
    out_edges = {"a.md": ["b.md"], "b.md": ["c.md"]}
    result = mod.compute_pagerank(out_edges, nodes)
    total = sum(result.values())
    assert abs(total - 1.0) < 0.01


def test_compute_pagerank_hub_gets_higher_score():
    # b.md is linked from two sources → should score highest
    nodes = {"a.md", "b.md", "c.md"}
    out_edges = {"a.md": ["b.md"], "c.md": ["b.md"]}
    result = mod.compute_pagerank(out_edges, nodes)
    assert result["b.md"] > result["a.md"]
    assert result["b.md"] > result["c.md"]


def test_compute_pagerank_no_inbound_gets_base():
    nodes = {"a.md", "b.md"}
    out_edges = {"a.md": ["b.md"]}
    result = mod.compute_pagerank(out_edges, nodes)
    # Both nodes should have positive score (dangling node distributes)
    assert result["a.md"] > 0
    assert result["b.md"] > 0


def test_compute_pagerank_converges(tmp_path):
    # Create a chain of 10 nodes; should converge well within default iterations
    nodes = {f"n{i}.md" for i in range(10)}
    out_edges = {f"n{i}.md": [f"n{i+1}.md"] for i in range(9)}
    result = mod.compute_pagerank(out_edges, nodes, max_iter=200)
    assert len(result) == 10
    assert all(v > 0 for v in result.values())


# ── normalise ─────────────────────────────────────────────────────────────────

def test_normalise_max_is_one():
    scores = {"a": 0.1, "b": 0.5, "c": 0.3}
    normed = mod.normalise(scores)
    assert abs(max(normed.values()) - 1.0) < 1e-9


def test_normalise_preserves_order():
    scores = {"a": 0.1, "b": 0.5, "c": 0.3}
    normed = mod.normalise(scores)
    assert normed["b"] > normed["c"] > normed["a"]


def test_normalise_empty():
    result = mod.normalise({})
    assert result == {}


# ── integration: gateway BM25 skip ───────────────────────────────────────────

def test_gateway_has_skip_prefixes():
    import importlib
    gw = importlib.import_module("gateway")
    assert hasattr(gw, "_SKIP_PREFIXES")
    assert "docs/obsidian/" in gw._SKIP_PREFIXES


def test_gateway_is_duplicate_obsidian():
    import importlib
    gw = importlib.import_module("gateway")
    assert gw._is_duplicate("docs/obsidian/CONTACTS.md") is True
    assert gw._is_duplicate("docs/CONTACTS.md") is False


def test_gateway_has_pagerank_loader():
    import importlib
    gw = importlib.import_module("gateway")
    assert callable(getattr(gw, "_load_pagerank", None))


def test_gateway_bm25_skip_excludes_tables():
    import importlib
    gw = importlib.import_module("gateway")
    assert "docs/TABLES.md" in gw._BM25_SKIP
    assert "docs/OUTLINE.md" in gw._BM25_SKIP
