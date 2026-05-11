"""Tests for scripts/improve_keyword_index.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_keyword_index")


def test_clean_returns_string():
    result = mod._clean("some text here")
    assert isinstance(result, str)


def test_clean_removes_code():
    result = mod._clean("Before\n```python\ncode here\n```\nAfter")
    assert "code here" not in result


def test_tokens_returns_list():
    result = mod._tokens("agent memory knowledge system")
    assert isinstance(result, list)


def test_tokens_min_3_chars():
    result = mod._tokens("ab abc abcd")
    for t in result:
        assert len(t) >= 3


def test_tokens_removes_stopwords():
    result = mod._tokens("the and for or but")
    assert "the" not in result


def test_section_of_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    section = tmp_path / "01-svyazi"
    section.mkdir()
    f = section / "file.md"
    result = mod._section_of(f)
    assert isinstance(result, str)


def test_section_of_extracts_section(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    section = tmp_path / "01-svyazi"
    section.mkdir()
    f = section / "file.md"
    result = mod._section_of(f)
    assert result == "01-svyazi"


def test_build_index_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Agent Memory\n\n" + "agent memory system knowledge retrieval data " * 5, encoding="utf-8")
    result = mod.build_index([f])
    assert isinstance(result, dict)


def test_build_index_finds_terms(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Agent Memory\n\n" + "agent memory system knowledge retrieval data " * 5, encoding="utf-8")
    monkeypatch.setattr(mod, "MIN_DF", 1)
    result = mod.build_index([f])
    assert "agent" in result or "memory" in result


def test_build_index_entry_has_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "MIN_DF", 1)
    f = tmp_path / "test.md"
    f.write_text("agent memory system knowledge retrieval data " * 5, encoding="utf-8")
    result = mod.build_index([f])
    for word, entries in result.items():
        for entry in entries:
            assert "file" in entry
            assert "count" in entry
            assert "tf" in entry


def test_search_returns_list():
    index = {
        "agent": [{"file": "file1.md", "section": "root", "count": 5, "tf": 0.1}],
        "memory": [{"file": "file1.md", "section": "root", "count": 3, "tf": 0.06}],
    }
    result = mod.search(index, "agent memory")
    assert isinstance(result, list)


def test_search_finds_matching():
    index = {
        "agent": [{"file": "file1.md", "section": "root", "count": 5, "tf": 0.1}],
    }
    result = mod.search(index, "agent")
    assert len(result) >= 1
    assert result[0]["file"] == "file1.md"


def test_search_empty_query():
    index = {"agent": [{"file": "file1.md", "section": "root", "count": 5, "tf": 0.1}]}
    result = mod.search(index, "")
    assert result == []


def test_search_no_match():
    index = {"agent": [{"file": "file1.md", "section": "root", "count": 5, "tf": 0.1}]}
    result = mod.search(index, "xyznomatch")
    assert len(result) == 0
