"""Tests for scripts/prototype_demo.py."""

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("prototype_demo")


def test_tokenize_returns_list():
    result = mod._tokenize("agent memory retrieval")
    assert isinstance(result, list)


def test_tokenize_filters_stopwords():
    result = mod._tokenize("the agent for memory retrieval")
    # "the" and "for" are in the stopwords set
    assert "the" not in result
    assert "for" not in result
    assert "agent" in result


def test_tokenize_lowercases():
    result = mod._tokenize("AGENT Memory")
    assert "agent" in result or "memory" in result


def test_doc_text_combines_fields():
    doc = {"content": "Content here.", "preview": "Preview.", "summary": "Summary."}
    result = mod._doc_text(doc)
    assert "Content here." in result
    assert "Preview." in result
    assert "Summary." in result


def test_doc_text_handles_empty():
    doc = {}
    result = mod._doc_text(doc)
    assert isinstance(result, str)


def test_doc_text_skips_none():
    doc = {"content": "Content.", "preview": None, "summary": ""}
    result = mod._doc_text(doc)
    assert "Content." in result


def test_tfidf_search_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    index = [
        {"title": "AgentFS", "content": "agent file system memory knowledge", "path": "doc1.md"},
        {"title": "Yodoca", "content": "memory consolidation decay agent", "path": "doc2.md"},
        {"title": "Other", "content": "unrelated topic different", "path": "doc3.md"},
    ]
    idx_file = tmp_path / "search_index.json"
    idx_file.write_text(json.dumps(index), encoding="utf-8")
    result = mod.tfidf_search("agent memory")
    assert isinstance(result, list)


def test_tfidf_search_finds_relevant(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    index = [
        {"title": "AgentFS", "content": "agent file system memory knowledge", "path": "doc1.md"},
        {"title": "Other", "content": "unrelated topic completely", "path": "doc2.md"},
    ]
    idx_file = tmp_path / "search_index.json"
    idx_file.write_text(json.dumps(index), encoding="utf-8")
    result = mod.tfidf_search("agent memory", top_k=5)
    assert len(result) >= 1
    titles = [r.get("title", "") for r in result]
    assert "AgentFS" in titles


def test_tfidf_search_empty_query(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    idx_file = tmp_path / "search_index.json"
    idx_file.write_text("[]", encoding="utf-8")
    result = mod.tfidf_search("")
    assert result == []


def test_tfidf_search_no_index(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.tfidf_search("agent")
    assert result == []


def test_bm25_search_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    passages = [
        {"text": "agent memory retrieval knowledge system", "file": "doc1.md"},
        {"text": "graph database relations edges nodes", "file": "doc2.md"},
    ]
    p = tmp_path / "passages.json"
    p.write_text(json.dumps(passages), encoding="utf-8")
    result = mod.bm25_search("agent")
    assert isinstance(result, list)


def test_bm25_search_empty_query(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    p = tmp_path / "passages.json"
    p.write_text("[]", encoding="utf-8")
    result = mod.bm25_search("")
    assert result == []


def test_bm25_search_no_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.bm25_search("agent")
    assert result == []


def test_success_criteria():
    assert hasattr(mod, "SUCCESS")
    assert isinstance(mod.SUCCESS, dict)
    assert "latency_s" in mod.SUCCESS
    assert "cards_min" in mod.SUCCESS


def test_benchmark_queries():
    assert hasattr(mod, "BENCHMARK_QUERIES")
    assert isinstance(mod.BENCHMARK_QUERIES, list)
    assert len(mod.BENCHMARK_QUERIES) > 0


def test_load_index_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    idx = [{"title": "Doc", "content": "content", "path": "doc.md"}]
    (tmp_path / "search_index.json").write_text(json.dumps(idx), encoding="utf-8")
    result = mod._load_index()
    assert isinstance(result, list)
    assert len(result) == 1


def test_load_index_empty_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._load_index()
    assert result == []


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_no_query_exits(monkeypatch):
    monkeypatch.setattr(mod, "QUERY", "")
    monkeypatch.setattr(mod, "FILE_ARG", None)
    monkeypatch.setattr(mod, "BENCHMARK", False)
    try:
        mod.main()
    except SystemExit:
        pass


def test_main_with_query_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", "agent memory")
    monkeypatch.setattr(mod, "FILE_ARG", None)
    monkeypatch.setattr(mod, "BENCHMARK", False)
    monkeypatch.setattr(mod, "JSON_OUT", False)
    monkeypatch.setattr(mod, "TOP", 3)
    mod.main()


def test_main_json_output_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "QUERY", "test")
    monkeypatch.setattr(mod, "FILE_ARG", None)
    monkeypatch.setattr(mod, "BENCHMARK", False)
    monkeypatch.setattr(mod, "JSON_OUT", True)
    monkeypatch.setattr(mod, "TOP", 3)
    mod.main()
