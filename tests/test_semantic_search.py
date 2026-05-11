"""
Тесты для scripts/improve_semantic_search.py.

Покрытие:
  - tokenize()          — токенизация строк
  - search_bm25()       — BM25-поиск
  - search_fulltext()   — полнотекстовый поиск
  - search_hybrid()     — гибридный поиск (основной режим)
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_semantic_search")

# ── tokenize ──────────────────────────────────────────────────────────────────

def test_tokenize_returns_list():
    assert isinstance(mod.tokenize("агент память консолидация"), list)


def test_tokenize_removes_short_tokens():
    tokens = mod.tokenize("я к в агент", min_len=3)
    assert all(len(t) >= 3 for t in tokens)


def test_tokenize_lowercases():
    tokens = mod.tokenize("AgentFS YODOCA")
    assert all(t == t.lower() for t in tokens)


def test_tokenize_empty_string():
    assert mod.tokenize("") == []

# ── search_bm25 ───────────────────────────────────────────────────────────────

def test_search_bm25_returns_list():
    results = mod.search_bm25("агент память", top=5)
    assert isinstance(results, list)


def test_search_bm25_top_k_respected():
    for k in (1, 3, 5):
        results = mod.search_bm25("граф знаний", top=k)
        assert len(results) <= k


def test_search_bm25_results_have_path_or_file():
    results = mod.search_bm25("Yodoca консолидация", top=5)
    if results:
        assert "path" in results[0] or "file" in results[0]


def test_search_bm25_results_have_score():
    results = mod.search_bm25("RAG retrieval", top=5)
    if results:
        assert "score" in results[0]
        assert results[0]["score"] >= 0


def test_search_bm25_empty_query():
    results = mod.search_bm25("", top=5)
    assert isinstance(results, list)   # не должен падать


def test_search_bm25_yodoca_in_top10():
    results = mod.search_bm25("Yodoca decay консолидация", top=10)
    locs = [r.get("path", "") or r.get("file", "") for r in results]
    assert any("yodoca" in p for p in locs), f"yodoca not found in: {locs}"

# ── search_fulltext ───────────────────────────────────────────────────────────

def test_search_fulltext_returns_list():
    results = mod.search_fulltext("агент память", top=5)
    assert isinstance(results, list)


def test_search_fulltext_top_k_respected():
    results = mod.search_fulltext("RAG", top=3)
    assert len(results) <= 3


def test_search_fulltext_results_have_path_or_file():
    results = mod.search_fulltext("Rufler YAML", top=5)
    if results:
        assert "path" in results[0] or "file" in results[0]

# ── search_hybrid ─────────────────────────────────────────────────────────────

def test_search_hybrid_returns_list():
    results = mod.search_hybrid("агент память консолидация", top=5)
    assert isinstance(results, list)


def test_search_hybrid_nonempty_for_known_query():
    results = mod.search_hybrid("Yodoca decay память", top=5)
    assert len(results) > 0


def test_search_hybrid_top_k_respected():
    for k in (1, 3, 5):
        results = mod.search_hybrid("граф знаний", top=k)
        assert len(results) <= k


def test_search_hybrid_results_have_path_and_score():
    results = mod.search_hybrid("RAG retrieval evidence", top=5)
    if results:
        assert "path" in results[0]
        assert "score" in results[0]


def test_search_hybrid_scores_descending():
    results = mod.search_hybrid("AgentFS knowledge filesystem", top=10)
    scores = [r["score"] for r in results]
    assert scores == sorted(scores, reverse=True)


def test_search_hybrid_section_filter():
    results = mod.search_hybrid("агент", top=20, section="05-habr-projects")
    for r in results:
        assert "05-habr-projects" in r.get("path", ""), \
            f"section filter violated: {r.get('path')}"


def test_search_hybrid_agentfs_in_top5():
    results = mod.search_hybrid("AgentFS Obsidian vault filesystem агент", top=5)
    paths = [r.get("path", "") for r in results]
    assert any("agentfs" in p for p in paths), f"agentfs not in top-5: {paths}"
