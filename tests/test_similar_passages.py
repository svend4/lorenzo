"""Tests for scripts/improve_similar_passages.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_similar_passages")


def test_clean_returns_string():
    result = mod._clean("some text here")
    assert isinstance(result, str)


def test_clean_removes_code():
    result = mod._clean("Before\n```python\ncode\n```\nAfter")
    assert "code" not in result


def test_tokenize_returns_list():
    result = mod._tokenize("agent memory knowledge system")
    assert isinstance(result, list)


def test_tokenize_removes_stopwords():
    result = mod._tokenize("the and for or but")
    assert "the" not in result


def test_cosine_returns_float():
    a = {"agent": 0.5, "memory": 0.3}
    b = {"agent": 0.4, "knowledge": 0.6}
    result = mod._cosine(a, b)
    assert isinstance(result, float)


def test_cosine_identical():
    a = {"agent": 0.5, "memory": 0.3}
    result = mod._cosine(a, a)
    assert abs(result - 1.0) < 0.01


def test_cosine_no_overlap():
    a = {"agent": 0.5}
    b = {"memory": 0.3}
    result = mod._cosine(a, b)
    assert result == 0.0


def test_cosine_empty():
    result = mod._cosine({}, {})
    assert result == 0.0


def test_tfidf_vectors_returns_list():
    passages = [
        {"tokens": ["agent", "memory", "agent", "system"]},
        {"tokens": ["graph", "knowledge", "agent", "system"]},
    ]
    result = mod._tfidf_vectors(passages)
    assert isinstance(result, list)


def test_tfidf_vectors_adds_vec():
    passages = [
        {"tokens": ["agent", "memory", "system", "knowledge"]},
        {"tokens": ["graph", "data", "retrieval", "system"]},
    ]
    result = mod._tfidf_vectors(passages)
    for p in result:
        assert "vec" in p
        assert isinstance(p["vec"], dict)


def test_find_similar_returns_list():
    passages = [
        {"source": "file1.md", "text": "Agent memory system.", "tokens": ["agent", "memory"], "vec": {"agent": 0.8, "memory": 0.6}},
        {"source": "file2.md", "text": "Agent memory retrieval.", "tokens": ["agent", "memory"], "vec": {"agent": 0.7, "memory": 0.5}},
    ]
    result = mod.find_similar(passages)
    assert isinstance(result, list)


def test_find_similar_skips_same_source():
    passages = [
        {"source": "file1.md", "text": "Same source text.", "tokens": ["agent"], "vec": {"agent": 0.8}},
        {"source": "file1.md", "text": "Same source other.", "tokens": ["agent"], "vec": {"agent": 0.7}},
    ]
    result = mod.find_similar(passages)
    assert len(result) == 0


def test_find_similar_has_required_keys():
    passages = [
        {"source": "file1.md", "text": "Agent memory system.", "tokens": ["agent", "memory"], "vec": {"agent": 0.8, "memory": 0.6}},
        {"source": "file2.md", "text": "Agent memory retrieval.", "tokens": ["agent", "memory"], "vec": {"agent": 0.7, "memory": 0.5}},
    ]
    result = mod.find_similar(passages)
    for pair in result:
        assert "sim" in pair
        assert "source_a" in pair
        assert "source_b" in pair
        assert "text_a" in pair
        assert "text_b" in pair
