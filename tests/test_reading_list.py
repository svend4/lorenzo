"""Tests for scripts/improve_reading_list.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_reading_list")


def test_tokenize_returns_list():
    result = mod._tokenize("agent memory knowledge system")
    assert isinstance(result, list)


def test_tokenize_removes_stopwords():
    result = mod._tokenize("the and for or but in on")
    assert "the" not in result


def test_tokenize_min_3_chars():
    result = mod._tokenize("ab abc abcd")
    for t in result:
        assert len(t) >= 3


def test_clean_returns_string():
    result = mod._clean("some text")
    assert isinstance(result, str)


def test_clean_removes_code():
    result = mod._clean("Before\n```python\ncode\n```\nAfter")
    assert "code" not in result


def test_ru_ratio_returns_float():
    tokens = ["агент", "память", "agent", "memory"]
    result = mod._ru_ratio(tokens)
    assert isinstance(result, float)
    assert 0 <= result <= 1


def test_ru_ratio_pure_russian():
    tokens = ["агент", "память", "знания", "система"]
    result = mod._ru_ratio(tokens)
    assert result == 1.0


def test_ru_ratio_pure_english():
    tokens = ["agent", "memory", "knowledge", "system"]
    result = mod._ru_ratio(tokens)
    assert result == 0.0


def test_ru_ratio_empty():
    result = mod._ru_ratio([])
    assert result == 0.5


def test_read_time_returns_int():
    result = mod._read_time(1000, 0.8)
    assert isinstance(result, int)


def test_read_time_minimum_1():
    result = mod._read_time(0, 0.8)
    assert result >= 1


def test_read_time_proportional():
    short = mod._read_time(200, 0.8)
    long_ = mod._read_time(2000, 0.8)
    assert long_ > short


def test_extract_title_returns_string(tmp_path):
    f = tmp_path / "test.md"
    result = mod._extract_title("# My Title\nContent here.", f)
    assert isinstance(result, str)


def test_extract_title_finds_h1(tmp_path):
    f = tmp_path / "test.md"
    result = mod._extract_title("# My Title\nContent here.", f)
    assert result == "My Title"


def test_extract_title_fallback(tmp_path):
    f = tmp_path / "my-test-file.md"
    result = mod._extract_title("no heading", f)
    assert "my" in result.lower() or "test" in result.lower()


def test_search_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f1 = tmp_path / "file1.md"
    f2 = tmp_path / "file2.md"
    f1.write_text("# Agent Memory\n" + "agent memory system knowledge retrieval data " * 10, encoding="utf-8")
    f2.write_text("# Graph Knowledge\n" + "graph knowledge query system retrieval agent " * 10, encoding="utf-8")
    docs, bm25 = mod.build_bm25([f1, f2])
    result = mod.search("agent memory", docs, bm25, top=5)
    assert isinstance(result, list)


def test_search_returns_scored_results(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f1 = tmp_path / "file1.md"
    f2 = tmp_path / "file2.md"
    f1.write_text("# Agent Memory\n" + "agent memory system knowledge retrieval data " * 10, encoding="utf-8")
    f2.write_text("# Knowledge Graph\n" + "graph knowledge system retrieval data storage " * 10, encoding="utf-8")
    docs, bm25 = mod.build_bm25([f1, f2])
    result = mod.search("agent memory", docs, bm25, top=5)
    for r in result:
        assert "score" in r
        assert "read_min" in r
