"""
Тесты для scripts/improve_clusters.py.

Покрытие:
  - tokenize()       — токенизация, стопслова, минимальная длина
  - build_tfidf()    — TF-IDF матрица, ненулевые веса
  - cosine()         — косинусное сходство двух векторов
  - greedy_cluster() — жадная кластеризация по порогу
  - top_words()      — топ слов кластера по суммарному TF-IDF
"""

import importlib
import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_clusters")

# ── tokenize ──────────────────────────────────────────────────────────────────

def test_tokenize_returns_list():
    assert isinstance(mod.tokenize("some text"), list)


def test_tokenize_lowercases():
    result = mod.tokenize("AgentFS Memory")
    assert all(t == t.lower() for t in result)


def test_tokenize_removes_stopwords():
    result = mod.tokenize("и в на что как это для или но the a an")
    assert result == []


def test_tokenize_keeps_content_words():
    result = mod.tokenize("агент память консолидация yodoca agentfs")
    assert "агент" in result
    assert "память" in result
    assert "yodoca" in result


def test_tokenize_min_length_3():
    # Pattern: [а-яёa-z][а-яёa-z\-]{2,} → min 3 chars total
    result = mod.tokenize("ab abc abcd")
    assert "ab" not in result
    assert "abc" in result


def test_tokenize_empty_text():
    assert mod.tokenize("") == []

# ── build_tfidf ───────────────────────────────────────────────────────────────

def _sample_docs():
    return {
        "memory.md": ["память", "консолидация", "агент", "decay", "граф"],
        "yaml.md":   ["yaml", "оркестрация", "декларативный", "агент", "rufler"],
        "graph.md":  ["граф", "узел", "ребро", "связь", "память"],
    }


def test_build_tfidf_returns_dict():
    result = mod.build_tfidf(_sample_docs())
    assert isinstance(result, dict)


def test_build_tfidf_has_all_docs():
    docs = _sample_docs()
    result = mod.build_tfidf(docs)
    assert set(result.keys()) == set(docs.keys())


def test_build_tfidf_weights_positive():
    result = mod.build_tfidf(_sample_docs())
    for vec in result.values():
        for score in vec.values():
            assert score > 0


def test_build_tfidf_rare_word_higher_idf():
    docs = {
        "a": ["уникальное", "агент"],
        "b": ["агент"],
        "c": ["агент"],
    }
    result = mod.build_tfidf(docs)
    vec_a = result["a"]
    # "уникальное" appears in 1 doc, "агент" in 3 — unique should have higher IDF
    if "уникальное" in vec_a and "агент" in vec_a:
        assert vec_a["уникальное"] > vec_a["агент"]


def test_build_tfidf_empty_docs():
    result = mod.build_tfidf({})
    assert result == {}

# ── cosine ────────────────────────────────────────────────────────────────────

def test_cosine_identical_vectors():
    v = {"a": 0.5, "b": 0.3, "c": 0.2}
    result = mod.cosine(v, v)
    assert abs(result - 1.0) < 1e-9


def test_cosine_orthogonal_vectors():
    v1 = {"a": 1.0}
    v2 = {"b": 1.0}
    assert mod.cosine(v1, v2) == 0.0


def test_cosine_returns_float():
    v1 = {"a": 1.0, "b": 0.5}
    v2 = {"a": 0.5, "c": 1.0}
    result = mod.cosine(v1, v2)
    assert isinstance(result, float)


def test_cosine_range_0_to_1():
    v1 = {"a": 1.0, "b": 2.0}
    v2 = {"a": 0.5, "b": 1.0, "c": 3.0}
    result = mod.cosine(v1, v2)
    assert 0.0 <= result <= 1.0


def test_cosine_empty_vectors():
    assert mod.cosine({}, {}) == 0.0


def test_cosine_one_empty():
    assert mod.cosine({"a": 1.0}, {}) == 0.0


def test_cosine_symmetric():
    v1 = {"a": 1.0, "b": 0.5}
    v2 = {"a": 0.8, "b": 0.3}
    assert abs(mod.cosine(v1, v2) - mod.cosine(v2, v1)) < 1e-9

# ── greedy_cluster ────────────────────────────────────────────────────────────

def _build_test_tfidf():
    docs = {
        "memory1.md": ["память", "консолидация", "decay", "агент", "граф"],
        "memory2.md": ["память", "консолидация", "decay", "агент", "store"],
        "yaml1.md":   ["yaml", "оркестрация", "декларативный", "rufler"],
        "yaml2.md":   ["yaml", "декларативный", "конфигурация", "rufler"],
    }
    return mod.build_tfidf(docs)


def test_greedy_cluster_returns_list():
    tfidf = _build_test_tfidf()
    result = mod.greedy_cluster(tfidf, threshold=0.1)
    assert isinstance(result, list)


def test_greedy_cluster_covers_all_docs():
    tfidf = _build_test_tfidf()
    result = mod.greedy_cluster(tfidf, threshold=0.1)
    all_in_clusters = [p for cluster in result for p in cluster]
    assert set(all_in_clusters) == set(tfidf.keys())


def test_greedy_cluster_no_duplicates():
    tfidf = _build_test_tfidf()
    result = mod.greedy_cluster(tfidf, threshold=0.1)
    all_paths = [p for cluster in result for p in cluster]
    assert len(all_paths) == len(set(all_paths))


def test_greedy_cluster_similar_docs_grouped():
    tfidf = _build_test_tfidf()
    # Low threshold — similar docs should cluster together
    result = mod.greedy_cluster(tfidf, threshold=0.1)
    # memory docs and yaml docs should tend to be in same clusters
    for cluster in result:
        if "memory1.md" in cluster:
            assert "memory2.md" in cluster
            break


def test_greedy_cluster_high_threshold_singletons():
    tfidf = _build_test_tfidf()
    # Very high threshold — almost nothing merges
    result = mod.greedy_cluster(tfidf, threshold=0.999)
    assert len(result) >= len(tfidf) - 1


def test_greedy_cluster_sorted_by_size():
    tfidf = _build_test_tfidf()
    result = mod.greedy_cluster(tfidf, threshold=0.1)
    sizes = [len(c) for c in result]
    assert sizes == sorted(sizes, reverse=True)

# ── top_words ─────────────────────────────────────────────────────────────────

def test_top_words_returns_list():
    tfidf = _build_test_tfidf()
    result = mod.top_words(["memory1.md"], tfidf, n=3)
    assert isinstance(result, list)


def test_top_words_respects_n():
    tfidf = _build_test_tfidf()
    result = mod.top_words(list(tfidf.keys()), tfidf, n=4)
    assert len(result) <= 4


def test_top_words_non_empty_for_valid_paths():
    tfidf = _build_test_tfidf()
    result = mod.top_words(["memory1.md", "memory2.md"], tfidf, n=5)
    assert len(result) > 0


def test_top_words_memory_cluster_has_memory_words():
    tfidf = _build_test_tfidf()
    result = mod.top_words(["memory1.md", "memory2.md"], tfidf, n=6)
    # "память" or "консолидация" should appear in memory cluster top words
    assert any(w in result for w in ["память", "консолидация", "decay"])


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_clusters_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "CLUSTERS.md").exists()


def test_main_clusters_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "a.md").write_text("# AgentFS\n\nMemory agent system.", encoding="utf-8")
    (tmp_path / "b.md").write_text("# Yodoca\n\nMemory consolidation.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "CLUSTERS.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "CLUSTERS.md").exists()


def test_main_clusters_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "CLUSTERS.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
