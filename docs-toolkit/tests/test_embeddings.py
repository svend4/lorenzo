"""Тесты embeddings."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.embeddings import (
    TFIDFProvider, HybridSearcher, get_provider, list_providers,
    SearchResult,
)
from docstoolkit.embeddings.tfidf import _tokenize, _cosine_sparse


def test_tokenize_filters_stopwords():
    tokens = _tokenize("the quick brown fox и в на")
    assert "quick" in tokens
    assert "brown" in tokens
    assert "the" not in tokens
    assert "и" not in tokens


def test_tokenize_handles_russian():
    tokens = _tokenize("Память агентов поддерживает быстрый поиск")
    assert "память" in tokens
    assert "агентов" in tokens
    assert "быстрый" in tokens


def test_cosine_sparse_identical():
    a = {"x": 1.0, "y": 0.5}
    assert _cosine_sparse(a, a) == pytest.approx(1.0)


def test_cosine_sparse_orthogonal():
    a = {"x": 1.0}
    b = {"y": 1.0}
    assert _cosine_sparse(a, b) == 0.0


def test_cosine_sparse_empty():
    assert _cosine_sparse({}, {"x": 1}) == 0.0


def test_tfidf_search_relevance():
    docs = [
        {"id": "d1", "title": "Yodoca", "content": "memory hot path"},
        {"id": "d2", "title": "Other", "content": "unrelated rag"},
        {"id": "d3", "title": "Memory", "content": "agent memory storage"},
    ]
    prov = TFIDFProvider()
    prov.fit([d["content"] + " " + d["title"] for d in docs])
    results = prov.search("memory", docs, top_k=3)
    assert len(results) >= 1
    # Memory-relевант должен быть в топе
    top_ids = [r.doc_id for r in results[:2]]
    assert "d1" in top_ids or "d3" in top_ids
    assert "d2" not in top_ids[:1]  # не должно быть #1


def test_tfidf_empty_corpus():
    prov = TFIDFProvider()
    prov.fit([])
    results = prov.search("test", [], top_k=5)
    assert results == []


def test_hybrid_searcher_keyword_only():
    docs = [
        {"id": "a", "title": "memory", "content": "x"},
        {"id": "b", "title": "rag", "content": "y"},
    ]
    keyword = TFIDFProvider()
    keyword.fit([d["content"] + " " + d["title"] for d in docs])
    searcher = HybridSearcher(keyword=keyword)
    results = searcher.search("memory", docs, top_k=2)
    assert len(results) >= 1
    assert results[0].doc_id == "a"


def test_hybrid_rrf_combines_rankings():
    """RRF: документ топ-1 у обоих провайдеров → топ результат у hybrid."""
    docs = [
        {"id": "a", "title": "memory", "content": "memory storage agent"},
        {"id": "b", "title": "other", "content": "irrelevant text"},
        {"id": "c", "title": "extra", "content": "different content"},
    ]
    keyword = TFIDFProvider()
    keyword.fit([d["content"] for d in docs])
    # Используем тот же провайдер дважды (для теста структуры)
    semantic = TFIDFProvider()
    semantic.fit([d["content"] for d in docs])
    searcher = HybridSearcher(keyword=keyword, semantic=semantic)
    results = searcher.search("memory storage", docs, top_k=3)
    assert results[0].doc_id == "a"


def test_get_provider_fallback():
    """Запрос несуществующего провайдера → tfidf fallback."""
    prov = get_provider("nonexistent")
    assert prov.name == "tfidf"


def test_list_providers_returns_tfidf():
    providers = list_providers()
    assert "tfidf" in providers


def test_search_result_sortable():
    a = SearchResult(doc_id="a", score=0.5)
    b = SearchResult(doc_id="b", score=0.8)
    sorted_results = sorted([a, b])
    assert sorted_results[0] == a  # меньше score первый при ascending
