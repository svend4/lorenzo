"""Tests for docstoolkit.citations — extract_links, pagerank, orphans, authorities."""
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.citations import (
    extract_links,
    build_citation_graph,
    pagerank,
    detect_orphans,
    detect_authorities,
    build_pagerank_report,
)


# ---------------------------------------------------------------------------
# extract_links
# ---------------------------------------------------------------------------

def test_extract_standard_markdown_links():
    md = "[Read more](docs/intro.md) and [advanced](advanced.md)"
    links = extract_links(md, "index")
    assert "docs/intro" in links
    assert "advanced" in links


def test_extract_wikilinks():
    md = "See [[overview]] and [[api/reference]]."
    links = extract_links(md, "index")
    assert "overview" in links
    assert "api/reference" in links


def test_extract_wikilinks_with_alias():
    md = "See [[overview|Overview Page]]."
    links = extract_links(md, "index")
    assert "overview" in links


def test_filter_external_urls_markdown():
    md = "[External](https://example.com) and [Internal](local.md)"
    links = extract_links(md, "index")
    assert "https://example.com" not in links
    assert not any(l.startswith("http") for l in links)
    assert "local" in links


def test_filter_external_urls_wikilinks():
    # Wikilinks should not normally be URLs but let's be defensive
    md = "[text](http://bad.com)"
    links = extract_links(md, "index")
    assert not any(l.startswith("http") for l in links)


def test_filter_self_links():
    md = "[self](self.md)"
    links = extract_links(md, "self")
    assert "self" not in links


def test_normalize_leading_dotslash():
    md = "[page](./subdir/page.md)"
    links = extract_links(md, "index")
    assert "subdir/page" in links
    assert not any(l.startswith("./") for l in links)


def test_normalize_md_extension_stripped():
    md = "[page](docs/page.md)"
    links = extract_links(md, "index")
    assert "docs/page" in links
    assert not any(l.endswith(".md") for l in links)


def test_strip_fragment_anchors():
    md = "[heading](docs/page.md#section-1)"
    links = extract_links(md, "index")
    assert "docs/page" in links
    assert not any("#" in l for l in links)


def test_empty_text_returns_empty():
    assert extract_links("", "index") == []


def test_no_links_returns_empty():
    assert extract_links("Just plain text, no links here.", "index") == []


def test_multiple_links_deduplication_not_applied():
    # extract_links returns all occurrences (dedup is caller's concern)
    md = "[a](doc.md) [b](doc.md)"
    links = extract_links(md, "index")
    # At least 2 entries since both point to "doc"
    assert links.count("doc") == 2


# ---------------------------------------------------------------------------
# build_citation_graph
# ---------------------------------------------------------------------------

def test_build_citation_graph_basic(tmp_path):
    (tmp_path / "a.md").write_text("# A\nSee [B](b.md).")
    (tmp_path / "b.md").write_text("# B\nSee [C](c.md).")
    (tmp_path / "c.md").write_text("# C\nNo links.")

    graph = build_citation_graph(tmp_path)
    assert "a" in graph
    assert "b" in graph["a"]
    assert "c" in graph["b"]
    assert graph["c"] == []


def test_build_citation_graph_empty_dir(tmp_path):
    graph = build_citation_graph(tmp_path)
    assert graph == {}


def test_build_citation_graph_ignores_external(tmp_path):
    (tmp_path / "doc.md").write_text("See [Google](https://google.com).")
    graph = build_citation_graph(tmp_path)
    assert graph["doc"] == []


# ---------------------------------------------------------------------------
# pagerank
# ---------------------------------------------------------------------------

def test_pagerank_empty_graph():
    assert pagerank({}) == {}


def test_pagerank_single_node():
    graph = {"a": []}
    pr = pagerank(graph)
    assert "a" in pr
    assert abs(pr["a"] - 1.0) < 1e-6


def test_pagerank_two_nodes_mutual():
    graph = {"a": ["b"], "b": ["a"]}
    pr = pagerank(graph)
    # Symmetric → equal scores
    assert abs(pr["a"] - pr["b"]) < 1e-4


def test_pagerank_cycle_equal_scores():
    # A → B → C → A: all equal rank
    graph = {"a": ["b"], "b": ["c"], "c": ["a"]}
    pr = pagerank(graph)
    scores = list(pr.values())
    assert max(scores) - min(scores) < 1e-4


def test_pagerank_star_center_highest():
    # Hub B ← {A, C, D, E}: B should have highest rank
    graph = {
        "a": ["b"], "c": ["b"], "d": ["b"], "e": ["b"],
        "b": [],
    }
    pr = pagerank(graph)
    assert pr["b"] == max(pr.values())


def test_pagerank_all_nodes_included():
    # Node "z" appears only as target, not as key
    graph = {"a": ["z"], "b": ["z"]}
    pr = pagerank(graph)
    assert "z" in pr
    assert "a" in pr
    assert "b" in pr


def test_pagerank_scores_sum_to_one():
    graph = {"a": ["b", "c"], "b": ["a"], "c": ["a", "b"]}
    pr = pagerank(graph)
    total = sum(pr.values())
    assert abs(total - 1.0) < 1e-5


def test_pagerank_converges_within_max_iter():
    # 100-node random graph: should converge in ≤ 50 iterations
    random.seed(42)
    n = 100
    nodes = [f"n{i}" for i in range(n)]
    graph = {node: random.sample(nodes, k=3) for node in nodes}
    pr = pagerank(graph, max_iter=50)
    assert len(pr) == n
    total = sum(pr.values())
    assert abs(total - 1.0) < 1e-4


def test_pagerank_dangling_node():
    # "sink" has no outlinks → dangling; rank should still distribute
    graph = {"a": ["sink"], "sink": []}
    pr = pagerank(graph)
    assert "sink" in pr
    assert pr["sink"] > 0


# ---------------------------------------------------------------------------
# detect_orphans
# ---------------------------------------------------------------------------

def test_detect_orphans_basic():
    # "a" has no inlinks → orphan
    graph = {"a": ["b"], "b": ["c"]}
    orphans = detect_orphans(graph)
    assert "a" in orphans
    assert "b" not in orphans
    assert "c" not in orphans


def test_detect_orphans_empty():
    assert detect_orphans({}) == []


def test_detect_orphans_all_connected():
    graph = {"a": ["b"], "b": ["a"]}
    # Both have inlinks from each other → no orphans
    orphans = detect_orphans(graph)
    assert orphans == []


def test_detect_orphans_sorted():
    graph = {"z": ["b"], "a": ["b"], "b": []}
    orphans = detect_orphans(graph)
    assert orphans == sorted(orphans)


# ---------------------------------------------------------------------------
# detect_authorities
# ---------------------------------------------------------------------------

def test_detect_authorities_top_k():
    pr = {"a": 0.5, "b": 0.3, "c": 0.1, "d": 0.05, "e": 0.05}
    top = detect_authorities(pr, top_k=2)
    assert len(top) == 2
    assert top[0][0] == "a"
    assert top[1][0] == "b"


def test_detect_authorities_all():
    pr = {"a": 0.5, "b": 0.3}
    top = detect_authorities(pr, top_k=10)
    assert len(top) == 2


def test_detect_authorities_sorted_descending():
    pr = {"a": 0.1, "b": 0.9, "c": 0.4}
    top = detect_authorities(pr, top_k=3)
    scores = [s for _, s in top]
    assert scores == sorted(scores, reverse=True)


# ---------------------------------------------------------------------------
# build_pagerank_report
# ---------------------------------------------------------------------------

def test_build_pagerank_report_returns_markdown(tmp_path):
    (tmp_path / "a.md").write_text("[b](b.md)")
    (tmp_path / "b.md").write_text("[a](a.md)")
    report = build_pagerank_report(tmp_path)
    assert "# Citation Graph" in report
    assert "PageRank" in report
    assert "|" in report  # table


def test_build_pagerank_report_empty_dir(tmp_path):
    report = build_pagerank_report(tmp_path)
    assert "0" in report  # zero docs/edges
    assert "Orphan" in report
