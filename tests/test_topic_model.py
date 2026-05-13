"""Tests for scripts/improve_topic_model.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_topic_model")


def test_clean_returns_string():
    result = mod._clean("some text here")
    assert isinstance(result, str)


def test_clean_removes_code():
    result = mod._clean("Before\n```python\ncode here\n```\nAfter")
    assert "code" not in result


def test_clean_removes_urls():
    result = mod._clean("See https://example.com for more.")
    assert "https" not in result


def test_clean_lowercases():
    result = mod._clean("HELLO WORLD")
    assert result == result.lower()


def test_tokenize_returns_list():
    result = mod._tokenize("agent memory knowledge system")
    assert isinstance(result, list)


def test_tokenize_min_length():
    result = mod._tokenize("abc abcd abcde")
    for t in result:
        assert len(t) >= mod.MIN_WORD_LEN


def test_tokenize_removes_stopwords():
    result = mod._tokenize("the and for or but")
    assert "the" not in result
    assert "and" not in result


def test_compute_tfidf_returns_dict():
    docs = {
        "doc1": ["agent", "memory", "agent", "system"],
        "doc2": ["knowledge", "graph", "agent", "system"],
        "doc3": ["memory", "retrieval", "system", "agent"],
    }
    result = mod._compute_tfidf(docs)
    assert isinstance(result, dict)


def test_compute_tfidf_all_docs_present():
    docs = {
        "doc1": ["agent", "memory", "agent", "system"],
        "doc2": ["knowledge", "graph", "agent", "system"],
    }
    result = mod._compute_tfidf(docs)
    for doc_id in docs:
        assert doc_id in result


def test_compute_tfidf_scores_are_floats():
    docs = {
        "doc1": ["agent", "memory", "agent", "knowledge"],
        "doc2": ["knowledge", "graph", "memory", "system"],
    }
    result = mod._compute_tfidf(docs)
    for doc_id, scores in result.items():
        for word, score in scores.items():
            assert isinstance(score, float)


def test_top_words_returns_list():
    scores = {"agent": 0.8, "memory": 0.5, "graph": 0.3}
    result = mod._top_words(scores, n=2)
    assert isinstance(result, list)
    assert len(result) == 2


def test_top_words_sorted_by_score():
    scores = {"agent": 0.8, "memory": 0.5, "graph": 0.3}
    result = mod._top_words(scores, n=3)
    assert result[0] == "agent"


def test_top_words_respects_n():
    scores = {"a": 0.9, "b": 0.7, "c": 0.5, "d": 0.3}
    result = mod._top_words(scores, n=2)
    assert len(result) == 2


def test_cluster_files_returns_dict():
    tfidf = {
        "f1": {"agent": 0.8, "memory": 0.5},
        "f2": {"graph": 0.9, "knowledge": 0.4},
        "f3": {"agent": 0.7, "memory": 0.6},
    }
    result = mod._cluster_files(tfidf, n_clusters=2)
    assert isinstance(result, dict)


def test_cluster_files_empty():
    result = mod._cluster_files({}, n_clusters=3)
    assert result == {}


def test_name_cluster_returns_string():
    tfidf = {
        "f1": {"agent": 0.8, "memory": 0.5},
        "f2": {"agent": 0.7, "knowledge": 0.6},
    }
    result = mod._name_cluster(["f1", "f2"], tfidf)
    assert isinstance(result, str)


def test_name_cluster_contains_top_word():
    tfidf = {
        "f1": {"agent": 0.9, "memory": 0.3},
    }
    result = mod._name_cluster(["f1"], tfidf)
    assert "agent" in result


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_topic_model_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    (tmp_path / "doc.md").write_text("# Title\n\nContent.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "TOPIC_MODEL.md").exists()


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    assert (tmp_path / "TOPIC_MODEL.md").exists()
