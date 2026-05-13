"""Fast unit tests for core search functions and /api/collabs endpoint."""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import gateway  # noqa: E402 — must come after sys.path update

client = TestClient(gateway.app)

# ---------------------------------------------------------------------------
# hybrid_search unit tests
# ---------------------------------------------------------------------------

def test_hybrid_search_returns_list():
    results = gateway.hybrid_search("агент память", top_k=5)
    assert isinstance(results, list)


def test_hybrid_search_nonempty_for_known_query():
    results = gateway.hybrid_search("AgentFS obsidian", top_k=5)
    assert len(results) > 0


def test_hybrid_search_result_has_path_or_file():
    results = gateway.hybrid_search("граф знаний", top_k=3)
    for r in results:
        assert r.get("path") or r.get("file"), f"No path/file in result: {r}"


def test_hybrid_search_top_k_respected():
    for k in (1, 3, 10):
        results = gateway.hybrid_search("консолидация памяти", top_k=k)
        assert len(results) <= k


def test_hybrid_search_returns_project_for_known_term():
    results = gateway.hybrid_search("Yodoca консолидация", top_k=10)
    paths = [r.get("path", r.get("file", "")) for r in results]
    assert any("yodoca" in p.lower() for p in paths), (
        f"yodoca not in top-10 for 'Yodoca консолидация': {paths}"
    )


def test_hybrid_search_empty_query_returns_list():
    results = gateway.hybrid_search("", top_k=5)
    assert isinstance(results, list)


# ---------------------------------------------------------------------------
# find_collabs unit tests
# ---------------------------------------------------------------------------

def test_find_collabs_returns_list():
    results = gateway.find_collabs("агент память", top_k=5)
    assert isinstance(results, list)


def test_find_collabs_returns_project_files():
    results = gateway.find_collabs("граф знаний типизированные отношения", top_k=5)
    assert len(results) > 0
    for r in results:
        assert "file" in r or "path" in r
        assert "score" in r


def test_find_collabs_score_in_valid_range():
    results = gateway.find_collabs("YAML оркестрация декларативный", top_k=5)
    for r in results:
        assert 0.0 <= r["score"] <= 1.0, f"score out of range: {r['score']}"


def test_find_collabs_top_k_respected():
    for k in (1, 3, 9):
        results = gateway.find_collabs("memory graph", top_k=k)
        assert len(results) <= k


def test_find_collabs_known_project_in_top3():
    """Rufler should appear for YAML orchestration query."""
    results = gateway.find_collabs("yaml декларативный оркестрация агентов", top_k=5)
    files = [r.get("file", r.get("path", "")) for r in results]
    assert any("rufler" in f.lower() for f in files), (
        f"rufler not in top-5 collabs: {files}"
    )


# ---------------------------------------------------------------------------
# /api/collabs endpoint tests
# ---------------------------------------------------------------------------

def test_collabs_endpoint_status_ok():
    r = client.post("/api/collabs", json={"query": "агент память"})
    assert r.status_code == 200


def test_collabs_endpoint_has_required_fields():
    r = client.post("/api/collabs", json={"query": "граф знаний"})
    body = r.json()
    assert "query" in body
    assert "results" in body
    assert "count" in body
    assert "latency_s" in body


def test_collabs_endpoint_count_matches_results():
    r = client.post("/api/collabs", json={"query": "RAG retrieval", "top_k": 3})
    body = r.json()
    assert body["count"] == len(body["results"])


def test_collabs_endpoint_top_k_respected():
    r = client.post("/api/collabs", json={"query": "memory graph", "top_k": 2})
    body = r.json()
    assert body["count"] <= 2


def test_collabs_endpoint_latency_is_fast():
    r = client.post("/api/collabs", json={"query": "yaml оркестрация"})
    body = r.json()
    assert body["latency_s"] < 5.0
