"""Тесты EmbeddingCache."""
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.embeddings.cache import EmbeddingCache, hash_content
from docstoolkit.embeddings.tfidf import TFIDFProvider


def test_hash_content_deterministic():
    assert hash_content("hello") == hash_content("hello")
    assert hash_content("hello") != hash_content("world")


def test_cache_save_load_idf(tmp_path):
    cache = EmbeddingCache(tmp_path / "test.sqlite")
    cache.save_idf("tfidf", {"a": 1.5, "b": 2.0}, n_docs=100)
    loaded, n = cache.load_idf("tfidf")
    assert loaded == {"a": 1.5, "b": 2.0}
    assert n == 100
    cache.close()


def test_cache_load_idf_missing(tmp_path):
    cache = EmbeddingCache(tmp_path / "test.sqlite")
    assert cache.load_idf("nonexistent") is None
    cache.close()


def test_cache_save_load_vector(tmp_path):
    cache = EmbeddingCache(tmp_path / "test.sqlite")
    cache.save_vector("tfidf", "doc1", "content", {"a": 0.5, "b": 0.3})
    loaded = cache.load_vector("tfidf", "doc1", "content")
    assert loaded == {"a": 0.5, "b": 0.3}
    cache.close()


def test_cache_invalidates_on_content_change(tmp_path):
    cache = EmbeddingCache(tmp_path / "test.sqlite")
    cache.save_vector("tfidf", "doc1", "original", [0.1, 0.2])
    # Тот же content — найдено
    assert cache.load_vector("tfidf", "doc1", "original") == [0.1, 0.2]
    # Другой content — не найдено (invalidated)
    assert cache.load_vector("tfidf", "doc1", "changed") is None
    cache.close()


def test_cache_invalidate_provider(tmp_path):
    cache = EmbeddingCache(tmp_path / "test.sqlite")
    cache.save_vector("tfidf", "doc1", "x", [1])
    cache.save_vector("tfidf", "doc2", "y", [2])
    cache.save_vector("st", "doc1", "x", [1, 2, 3])
    cache.invalidate("tfidf")
    assert cache.load_vector("tfidf", "doc1") is None
    assert cache.load_vector("tfidf", "doc2") is None
    # Другой провайдер не тронут
    assert cache.load_vector("st", "doc1") == [1, 2, 3]
    cache.close()


def test_cache_stats(tmp_path):
    cache = EmbeddingCache(tmp_path / "test.sqlite")
    cache.save_idf("tfidf", {"x": 1.0}, n_docs=10)
    cache.save_vector("tfidf", "doc1", "c", [0.1])
    cache.save_vector("tfidf", "doc2", "c", [0.2])
    cache.save_vector("st", "doc1", "c", [0.3, 0.4])
    stats = cache.stats()
    assert stats["total_vectors"] == 3
    assert "tfidf" in stats["per_provider"]
    assert stats["per_provider"]["tfidf"] == 2
    assert "tfidf" in stats["idf_providers"]
    cache.close()


def test_tfidf_with_cache_loads_idf(tmp_path):
    """TF-IDF с cache: первый fit сохраняет, второй init читает."""
    cache = EmbeddingCache(tmp_path / "test.sqlite")

    p1 = TFIDFProvider(cache=cache)
    p1.fit(["hello world", "foo bar baz"])
    assert p1._fitted
    assert "hello" in p1._idf or "world" in p1._idf

    p2 = TFIDFProvider(cache=cache)
    # Должен быть fitted из кэша без вызова fit()
    assert p2._fitted
    assert p2._idf == p1._idf

    cache.close()


def test_tfidf_cache_invalidation_via_force(tmp_path):
    """force=True перезаписывает кэш."""
    cache = EmbeddingCache(tmp_path / "test.sqlite")
    p = TFIDFProvider(cache=cache)
    p.fit(["text1"])
    old_idf = dict(p._idf)
    # Перезапись с другим корпусом
    p.fit(["completely different vocabulary here"], force=True)
    assert p._idf != old_idf
    cache.close()
