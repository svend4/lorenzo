"""Tests for scripts/improve_reclassify.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_reclassify")


def test_clean_returns_string():
    result = mod._clean("some text here")
    assert isinstance(result, str)


def test_clean_removes_code():
    result = mod._clean("Before\n```python\ncode here\n```\nAfter")
    assert "code here" not in result


def test_tokenize_returns_list():
    result = mod._tokenize("agent memory knowledge system")
    assert isinstance(result, list)


def test_tokenize_removes_stopwords():
    result = mod._tokenize("the and for or but in on")
    assert "the" not in result


def test_tfidf_returns_dict():
    docs = {
        "doc1": ["agent", "memory", "agent", "system"],
        "doc2": ["graph", "knowledge", "agent", "system"],
        "doc3": ["retrieval", "memory", "system", "agent"],
    }
    result = mod._tfidf(docs)
    assert isinstance(result, dict)


def test_tfidf_all_docs_present():
    docs = {
        "doc1": ["agent", "memory", "agent", "system", "data"],
        "doc2": ["graph", "knowledge", "agent", "system", "data"],
    }
    result = mod._tfidf(docs)
    for doc_id in docs:
        assert doc_id in result


def test_top_words_returns_list():
    scores = {"agent": 0.8, "memory": 0.5, "graph": 0.3}
    result = mod._top_words(scores, n=2)
    assert isinstance(result, list)
    assert len(result) == 2


def test_top_words_sorted():
    scores = {"agent": 0.8, "memory": 0.5, "graph": 0.3}
    result = mod._top_words(scores, n=3)
    assert result[0] == "agent"


def test_kmeans_returns_dict():
    tfidf = {
        "f1": {"agent": 0.8, "memory": 0.5},
        "f2": {"graph": 0.9, "knowledge": 0.4},
        "f3": {"agent": 0.7, "system": 0.6},
    }
    result = mod._kmeans(tfidf, k=2)
    assert isinstance(result, dict)


def test_name_cluster_returns_string():
    tfidf = {
        "f1": {"agent": 0.8, "memory": 0.5},
        "f2": {"agent": 0.7, "knowledge": 0.6},
    }
    result = mod._name_cluster(["f1", "f2"], tfidf)
    assert isinstance(result, str)


def test_safe_folder_name_returns_string():
    result = mod._safe_folder_name("Agent Memory System")
    assert isinstance(result, str)


def test_safe_folder_name_no_special_chars():
    result = mod._safe_folder_name("Agent & Memory: System!")
    assert ":" not in result
    assert "!" not in result
    assert "&" not in result


def test_safe_folder_name_max_40():
    result = mod._safe_folder_name("very long cluster name that exceeds forty characters here")
    assert len(result) <= 40


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    mod.main()


def test_main_few_files_message(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    (tmp_path / "doc.md").write_text("# Title\n\nContent.", encoding="utf-8")
    mod.main()
    out = capsys.readouterr().out
    assert "мало" in out or "Файлов" in out


def test_main_with_content_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    for i in range(5):
        (tmp_path / f"doc{i}.md").write_text(
            f"# Title {i}\n\n" + f"Content word{i} text {i}. " * 20,
            encoding="utf-8"
        )
    mod.main()
