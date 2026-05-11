"""Tests for scripts/improve_search_repl.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_search_repl")


def test_tok_returns_list():
    result = mod._tok("agent memory retrieval")
    assert isinstance(result, list)


def test_tok_filters_stopwords():
    result = mod._tok("и в не на the a for agent")
    # stopwords should be filtered
    assert "и" not in result
    assert "the" not in result
    assert "agent" in result


def test_tok_filters_short_words():
    result = mod._tok("go to do it agent")
    # words < 3 chars should be filtered
    assert all(len(w) >= 3 for w in result)


def test_tok_lowercases():
    result = mod._tok("AGENT Memory")
    assert "agent" in result
    assert "memory" in result


def test_clean_removes_code_blocks():
    text = "before\n```python\ncode()\n```\nafter"
    result = mod._clean(text)
    assert "code()" not in result
    assert "before" in result
    assert "after" in result


def test_clean_removes_html_comments():
    text = "text <!-- comment --> more"
    result = mod._clean(text)
    assert "comment" not in result
    assert "text" in result


def test_clean_removes_urls():
    text = "See https://github.com/user/repo for details."
    result = mod._clean(text)
    assert "github.com" not in result
    assert "details" in result


def test_clean_returns_string():
    result = mod._clean("# Title\n\nContent.")
    assert isinstance(result, str)


def test_bm25_search_returns_list():
    passages = [
        {"file": "doc1.md", "text": "agent memory retrieval system", "tokens": ["agent", "memory", "retrieval", "system"]},
        {"file": "doc2.md", "text": "knowledge graph database", "tokens": ["knowledge", "graph", "database"]},
    ]
    bm25 = mod._build_bm25(passages)
    result = mod._bm25_search("agent", passages, bm25)
    assert isinstance(result, list)


def test_bm25_search_finds_relevant():
    passages = [
        {"file": "doc1.md", "text": "agent memory retrieval", "tokens": ["agent", "memory", "retrieval"]},
        {"file": "doc2.md", "text": "graph database knowledge", "tokens": ["graph", "database", "knowledge"]},
    ]
    bm25 = mod._build_bm25(passages)
    result = mod._bm25_search("agent memory", passages, bm25)
    assert len(result) >= 1
    assert result[0]["file"] == "doc1.md"


def test_bm25_search_empty_query():
    passages = [
        {"file": "doc1.md", "text": "agent memory", "tokens": ["agent", "memory"]},
    ]
    bm25 = mod._build_bm25(passages)
    result = mod._bm25_search("", passages, bm25)
    assert result == []


def test_bm25_search_respects_top():
    passages = [
        {"file": f"doc{i}.md", "text": "agent memory system", "tokens": ["agent", "memory", "system"]}
        for i in range(10)
    ]
    bm25 = mod._build_bm25(passages)
    result = mod._bm25_search("agent", passages, bm25, top=3)
    assert len(result) <= 3


def test_bm25_search_results_have_score():
    passages = [
        {"file": "doc1.md", "text": "agent memory", "tokens": ["agent", "memory"]},
    ]
    bm25 = mod._build_bm25(passages)
    result = mod._bm25_search("agent", passages, bm25)
    if result:
        assert "score" in result[0]
        assert isinstance(result[0]["score"], float)


def test_build_bm25_returns_dict():
    passages = [
        {"file": "doc1.md", "text": "agent memory", "tokens": ["agent", "memory"]},
    ]
    result = mod._build_bm25(passages)
    assert isinstance(result, dict)
    assert "idf" in result
    assert "inv" in result
    assert "avgdl" in result


def test_build_bm25_empty_passages():
    result = mod._build_bm25([])
    assert isinstance(result, dict)
    assert result["avgdl"] == 0


def test_fulltext_search_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("This has agent memory content.", encoding="utf-8")
    result = mod._fulltext_search("agent")
    assert isinstance(result, list)


def test_fulltext_search_finds_match(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("This has agent memory content.", encoding="utf-8")
    result = mod._fulltext_search("agent")
    assert len(result) >= 1


def test_fulltext_search_empty_query(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod._fulltext_search("")
    assert result == []


def test_stopwords_constant():
    assert hasattr(mod, "STOPWORDS")
    assert isinstance(mod.STOPWORDS, set)
    assert "и" in mod.STOPWORDS
    assert "the" in mod.STOPWORDS


def test_skip_files_constant():
    assert hasattr(mod, "SKIP_FILES")
    assert isinstance(mod.SKIP_FILES, set)
    assert "SUMMARIES.md" in mod.SKIP_FILES


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_query_bm25_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "PASSAGES_JSON", tmp_path / "passages.json")
    monkeypatch.setattr(mod, "SEARCH_INDEX", tmp_path / "search_index.json")
    (tmp_path / "doc.md").write_text("# AgentFS\n\nAgent memory system.", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["prog", "--query", "agent", "--mode", "bm25"])
    mod.main()


def test_main_query_full_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "PASSAGES_JSON", tmp_path / "passages.json")
    monkeypatch.setattr(mod, "SEARCH_INDEX", tmp_path / "search_index.json")
    (tmp_path / "doc.md").write_text("# Title\n\nContent.", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["prog", "--query", "title", "--mode", "full"])
    mod.main()


def test_main_index_rebuild_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "PASSAGES_JSON", tmp_path / "passages.json")
    monkeypatch.setattr(mod, "SEARCH_INDEX", tmp_path / "search_index.json")
    (tmp_path / "doc.md").write_text("# Title\n\nContent.", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["prog", "--index", "--query", "title"])
    mod.main()
