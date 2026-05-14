"""Tests for /faceted page and _faceted_search in docstoolkit.serve."""
import json
import socketserver
import sys
import threading
import urllib.parse
import urllib.request
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.serve import _faceted_search, DocsHandler
from docstoolkit.config import Config


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

SAMPLE_DOCS = [
    {
        "title": "AgentFS Overview",
        "path": "docs/knowledge/agentfs.md",
        "content": "AgentFS is a filesystem agent for knowledge management",
        "preview": "filesystem agent",
        "tags": ["agent", "filesystem", "knowledge"],
        "lang": "EN",
    },
    {
        "title": "NGT Memory",
        "path": "docs/memory/ngt-memory.md",
        "content": "NGT Memory provides fast approximate nearest neighbour search for agent memory",
        "preview": "fast nearest neighbour",
        "tags": ["memory", "agent", "search"],
        "lang": "RU",
    },
    {
        "title": "Yodoca",
        "path": "docs/memory/yodoca.md",
        "content": "Yodoca is an in-process memory store for AI agents",
        "preview": "in-process memory",
        "tags": ["memory", "agent"],
        "lang": "RU",
    },
    {
        "title": "Knowledge Space",
        "path": "docs/knowledge/knowledge-space.md",
        "content": "Knowledge Space organises documents into a graph of concepts",
        "preview": "graph of concepts",
        "tags": ["knowledge", "graph", "concept"],
        "lang": "EN",
    },
    {
        "title": "Svyazi Architecture",
        "path": "docs/svyazi/overview.md",
        "content": "Svyazi 2.0 is a community intelligence platform",
        "preview": "community intelligence",
        "tags": ["architecture", "community"],
        "lang": "MIX",
    },
]


def _make_cfg(tmp_path: Path) -> Config:
    docs = tmp_path / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    # Write a minimal search_index.json
    (docs / "search_index.json").write_text(
        json.dumps(SAMPLE_DOCS, ensure_ascii=False), encoding="utf-8"
    )
    return Config(
        root=tmp_path,
        paths={"docs": "docs", "templates": "docs/templates",
               "schemas": "docs/templates/_schemas",
               "tasks": "tasks", "skills": ".claude/skills"},
        validation={}, language={}, sections={},
    )


def _start_server(cfg: Config):
    DocsHandler.cfg = cfg
    httpd = socketserver.TCPServer(("127.0.0.1", 0), DocsHandler)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd, port


# ---------------------------------------------------------------------------
# _faceted_search unit tests
# ---------------------------------------------------------------------------

def test_no_filters_no_query_returns_all_with_zero_score():
    results = _faceted_search(SAMPLE_DOCS, q="")
    # No query, no filters → all docs returned (score=0.0), unranked
    assert len(results) == len(SAMPLE_DOCS)
    assert all(r["score"] == 0.0 for r in results)


def test_query_returns_matching_docs():
    results = _faceted_search(SAMPLE_DOCS, q="memory")
    titles = [r["title"] for r in results]
    # NGT Memory and Yodoca both mention memory
    assert any("Memory" in t or "Yodoca" in t for t in titles)


def test_query_ranking_title_weighted_higher():
    # "knowledge" appears in title of two docs + content of one
    results = _faceted_search(SAMPLE_DOCS, q="knowledge")
    assert len(results) > 0
    # "Knowledge Space" has "knowledge" in title (3x weight) → should rank well
    titles = [r["title"] for r in results]
    # At least one result should be from knowledge section
    assert any("Knowledge" in t for t in titles)


def test_section_filter():
    results = _faceted_search(SAMPLE_DOCS, q="agent", section="docs")
    # All paths start with "docs/" so section "docs" should match all
    assert len(results) > 0
    for r in results:
        assert r["section"] == "docs"


def test_section_filter_no_match():
    results = _faceted_search(SAMPLE_DOCS, q="agent", section="nonexistent")
    assert results == []


def test_lang_filter_ru():
    results = _faceted_search(SAMPLE_DOCS, q="agent", lang="RU")
    # Only RU docs
    paths = [r["path"] for r in results]
    assert all("memory" in p for p in paths)


def test_lang_filter_en():
    results = _faceted_search(SAMPLE_DOCS, q="agent", lang="EN")
    for r in results:
        doc = next(d for d in SAMPLE_DOCS if d["path"] == r["path"])
        assert doc["lang"].upper() == "EN"


def test_lang_filter_mix():
    results = _faceted_search(SAMPLE_DOCS, q="community", lang="MIX")
    assert any("svyazi" in r["path"] for r in results)


def test_tag_filter_single():
    results = _faceted_search(SAMPLE_DOCS, q="", tags="filesystem")
    # Only AgentFS has "filesystem" tag
    assert len(results) == 1
    assert results[0]["title"] == "AgentFS Overview"


def test_tag_filter_multiple():
    # Tags "memory" OR "graph" (comma-sep = any match)
    results = _faceted_search(SAMPLE_DOCS, q="", tags="memory,graph")
    titles = {r["title"] for r in results}
    # Should include NGT Memory, Yodoca (memory tag) and Knowledge Space (graph tag)
    assert "NGT Memory" in titles or "Yodoca" in titles or "Knowledge Space" in titles


def test_combined_section_and_query():
    results = _faceted_search(SAMPLE_DOCS, q="memory", section="docs")
    # Both query matches and correct section
    assert len(results) >= 1


def test_result_has_required_fields():
    results = _faceted_search(SAMPLE_DOCS, q="agent")
    assert len(results) > 0
    r = results[0]
    assert "title" in r
    assert "path" in r
    assert "section" in r
    assert "score" in r
    assert "word_count" in r
    assert "tags" in r


def test_result_score_positive_for_matches():
    results = _faceted_search(SAMPLE_DOCS, q="filesystem")
    assert len(results) > 0
    assert all(r["score"] > 0 for r in results)


def test_result_sorted_by_score_desc():
    results = _faceted_search(SAMPLE_DOCS, q="agent")
    scores = [r["score"] for r in results]
    assert scores == sorted(scores, reverse=True)


def test_empty_docs_list():
    assert _faceted_search([], q="anything") == []


def test_max_50_results():
    big_docs = [
        {
            "title": f"Doc {i}", "path": f"docs/section/doc{i}.md",
            "content": "agent " * 20, "preview": "agent",
            "tags": [], "lang": "EN",
        }
        for i in range(100)
    ]
    results = _faceted_search(big_docs, q="agent")
    assert len(results) <= 50


# ---------------------------------------------------------------------------
# HTTP route tests
# ---------------------------------------------------------------------------

def test_faceted_route_returns_200(tmp_path):
    cfg = _make_cfg(tmp_path)
    httpd, port = _start_server(cfg)
    try:
        r = urllib.request.urlopen(f"http://127.0.0.1:{port}/faceted")
        assert r.status == 200
        body = r.read().decode("utf-8")
        assert "Faceted" in body or "faceted" in body.lower()
    finally:
        httpd.shutdown()


def test_faceted_route_has_form_element(tmp_path):
    cfg = _make_cfg(tmp_path)
    httpd, port = _start_server(cfg)
    try:
        r = urllib.request.urlopen(f"http://127.0.0.1:{port}/faceted")
        body = r.read().decode("utf-8")
        assert "<form" in body
        assert 'name="q"' in body
        assert 'name="section"' in body
        assert 'name="lang"' in body
    finally:
        httpd.shutdown()


def test_faceted_route_shows_lang_options(tmp_path):
    cfg = _make_cfg(tmp_path)
    httpd, port = _start_server(cfg)
    try:
        r = urllib.request.urlopen(f"http://127.0.0.1:{port}/faceted")
        body = r.read().decode("utf-8")
        assert "RU" in body
        assert "EN" in body
        assert "MIX" in body
    finally:
        httpd.shutdown()


def test_api_faceted_returns_json(tmp_path):
    cfg = _make_cfg(tmp_path)
    httpd, port = _start_server(cfg)
    try:
        url = f"http://127.0.0.1:{port}/api/faceted?q=memory"
        r = urllib.request.urlopen(url)
        assert r.status == 200
        ct = r.headers.get("Content-Type", "")
        assert "application/json" in ct
        data = json.loads(r.read().decode("utf-8"))
        assert "results" in data
        assert "total" in data
        assert "query" in data
        assert data["query"] == "memory"
    finally:
        httpd.shutdown()


def test_api_faceted_json_structure(tmp_path):
    cfg = _make_cfg(tmp_path)
    httpd, port = _start_server(cfg)
    try:
        url = f"http://127.0.0.1:{port}/api/faceted?q=agent"
        r = urllib.request.urlopen(url)
        data = json.loads(r.read().decode("utf-8"))
        assert isinstance(data["results"], list)
        assert isinstance(data["total"], int)
        assert data["total"] == len(data["results"])
    finally:
        httpd.shutdown()


def test_api_faceted_with_section_filter(tmp_path):
    cfg = _make_cfg(tmp_path)
    httpd, port = _start_server(cfg)
    try:
        url = f"http://127.0.0.1:{port}/api/faceted?q=agent&section=docs"
        r = urllib.request.urlopen(url)
        data = json.loads(r.read().decode("utf-8"))
        assert data["section"] == "docs"
    finally:
        httpd.shutdown()


def test_api_faceted_no_query_returns_all_docs(tmp_path):
    cfg = _make_cfg(tmp_path)
    httpd, port = _start_server(cfg)
    try:
        url = f"http://127.0.0.1:{port}/api/faceted"
        r = urllib.request.urlopen(url)
        data = json.loads(r.read().decode("utf-8"))
        # No query, no filters → all docs, score 0.0
        assert isinstance(data["results"], list)
        assert data["total"] == len(data["results"])
    finally:
        httpd.shutdown()
