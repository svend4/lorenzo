"""Tests for scripts/improve_external_compare.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_external_compare")


def test_stopwords_is_set():
    assert hasattr(mod, "STOPWORDS")
    assert isinstance(mod.STOPWORDS, set)
    assert "и" in mod.STOPWORDS
    assert "the" in mod.STOPWORDS


def test_tokens_returns_set():
    result = mod._tokens("agent memory retrieval system knowledge")
    assert isinstance(result, set)


def test_tokens_filters_stopwords():
    result = mod._tokens("the agent and memory for retrieval")
    assert "the" not in result
    assert "and" not in result
    assert "agent" in result


def test_tokens_filters_short_words():
    result = mod._tokens("the agent and go to memory")
    # words < 4 chars excluded by regex [а-яёa-z]{4,}
    assert all(len(w) >= 4 for w in result)


def test_tokens_respects_n():
    text = " ".join(["word"] + [f"unique{i}" for i in range(100)])
    result = mod._tokens(text, n=5)
    assert len(result) <= 5


def test_tokens_default_n():
    text = " ".join([f"word{i}word{i}" for i in range(100)])
    result = mod._tokens(text)
    assert len(result) <= 50


def test_top_freq_returns_list():
    result = mod._top_freq("agent memory agent retrieval memory agent")
    assert isinstance(result, list)


def test_top_freq_tuples_str_int():
    result = mod._top_freq("agent memory agent retrieval")
    for item in result:
        assert isinstance(item, tuple)
        assert isinstance(item[0], str)
        assert isinstance(item[1], int)


def test_top_freq_orders_by_frequency():
    result = mod._top_freq("agent agent agent memory memory knowledge")
    if len(result) >= 2:
        assert result[0][1] >= result[1][1]


def test_top_freq_respects_n():
    text = " ".join([f"unique{i}word" for i in range(50)])
    result = mod._top_freq(text, n=5)
    assert len(result) <= 5


def test_extract_urls_from_doc_returns_list():
    result = mod._extract_urls_from_doc("No URLs here.")
    assert isinstance(result, list)


def test_extract_urls_from_doc_finds_github():
    text = "See [project](https://github.com/user/repo) for details."
    result = mod._extract_urls_from_doc(text)
    assert any("github.com" in u for u in result)


def test_extract_urls_from_doc_finds_habr():
    text = "Published on https://habr.com/ru/articles/12345/"
    result = mod._extract_urls_from_doc(text)
    assert any("habr.com" in u for u in result)


def test_extract_urls_from_doc_ignores_others():
    text = "See https://example.com/page for reference."
    result = mod._extract_urls_from_doc(text)
    assert len(result) == 0


def test_extract_urls_strips_trailing_punctuation():
    text = "See https://github.com/user/repo."
    result = mod._extract_urls_from_doc(text)
    if result:
        assert not result[0].endswith(".")


def test_find_best_doc_returns_path_or_none(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "agentfs.md"
    f.write_text("# AgentFS\n\nAgent filesystem project.", encoding="utf-8")
    result = mod._find_best_doc("agentfs")
    assert result is None or isinstance(result, Path)


def test_find_best_doc_finds_matching(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "agentfs.md"
    f.write_text("# AgentFS\n\nAgent filesystem project.", encoding="utf-8")
    result = mod._find_best_doc("agentfs")
    assert result == f


def test_find_best_doc_no_match(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "unrelated.md"
    f.write_text("# Unrelated\n\nSomething else.", encoding="utf-8")
    result = mod._find_best_doc("completely_nonexistent_xyz")
    # Either returns None or the least-relevant file
    assert result is None or isinstance(result, Path)


def test_today_attribute():
    assert hasattr(mod, "TODAY")
    assert isinstance(mod.TODAY, str)
    assert len(mod.TODAY) == 10


def test_timeout_constant():
    assert hasattr(mod, "TIMEOUT")
    assert isinstance(mod.TIMEOUT, int)
    assert mod.TIMEOUT > 0
