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


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_no_args_prints_usage(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "AUTO", False)
    monkeypatch.setattr(mod, "FILE_ARG", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "URL_ARG", None)
    mod.main()
    out = capsys.readouterr().out
    assert "Использование" in out or "improve_external_compare" in out


def test_main_auto_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "AUTO", True)
    monkeypatch.setattr(mod, "FILE_ARG", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "URL_ARG", None)
    monkeypatch.setattr(mod, "LIMIT", 0)
    mod.main()


def test_main_file_arg_missing_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "AUTO", False)
    monkeypatch.setattr(mod, "FILE_ARG", tmp_path / "nonexistent.md")
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "URL_ARG", "https://example.com")
    mod.main()


def test_tokens_returns_set():
    result = mod._tokens("Agent memory system works with knowledge.")
    assert isinstance(result, set)
    assert "agent" in result or "memory" in result


def test_tokens_filters_short():
    result = mod._tokens("I am in it at do")
    assert all(len(t) >= 4 for t in result)


def test_top_freq_returns_list():
    result = mod._top_freq("agent memory agent search knowledge")
    assert isinstance(result, list)
    assert len(result) > 0
    # agent should be most frequent
    assert result[0][0] == "agent"


def test_extract_urls_from_doc_finds_github():
    text = "See https://github.com/user/repo for details."
    result = mod._extract_urls_from_doc(text)
    assert any("github.com" in u for u in result)


def test_extract_urls_from_doc_no_urls():
    text = "No links here."
    result = mod._extract_urls_from_doc(text)
    assert result == []


def test_find_best_doc_returns_none_empty_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod._find_best_doc("agent memory")
    assert result is None


# ── compare_with_url ──────────────────────────────────────────────────────────

def test_compare_with_url_http_error(tmp_path, monkeypatch):
    """Test compare_with_url when URL fetch fails."""
    f = tmp_path / "doc.md"
    f.write_text("# AgentFS\n\nAgent memory knowledge retrieval system.", encoding="utf-8")
    monkeypatch.setattr(mod, "_fetch_url", lambda url: "HTTP 404: Not Found")
    result = mod.compare_with_url(f, "https://github.com/test/repo")
    assert "error" in result


def test_compare_with_url_network_error(tmp_path, monkeypatch):
    """Test compare_with_url when fetch returns error string."""
    f = tmp_path / "doc.md"
    f.write_text("# Test\n\nContent here.", encoding="utf-8")
    monkeypatch.setattr(mod, "_fetch_url", lambda url: "Error: Connection refused")
    result = mod.compare_with_url(f, "https://example.com")
    assert "error" in result


def test_compare_with_url_success(tmp_path, monkeypatch):
    """Test compare_with_url with successful fetch."""
    f = tmp_path / "doc.md"
    f.write_text("# AgentFS\n\nAgent memory knowledge retrieval system.", encoding="utf-8")
    fake_ext = "AgentFS is a file system for agents with memory and knowledge retrieval capabilities."
    monkeypatch.setattr(mod, "_fetch_url", lambda url: fake_ext)
    result = mod.compare_with_url(f, "https://github.com/test/repo")
    assert "error" not in result
    assert "jaccard" in result
    assert "common" in result
    assert "only_doc" in result
    assert "only_ext" in result
    assert isinstance(result["jaccard"], float)


def test_compare_with_url_file_not_readable(tmp_path, monkeypatch):
    """Test compare_with_url when file can't be read."""
    f = tmp_path / "nonexistent.md"
    monkeypatch.setattr(mod, "_fetch_url", lambda url: "Some content here")
    result = mod.compare_with_url(f, "https://example.com")
    assert "error" in result


# ── format_result ─────────────────────────────────────────────────────────────

def test_format_result_with_error():
    r = {"error": "HTTP 404: Not Found", "url": "https://example.com"}
    result = mod.format_result(r)
    assert isinstance(result, list)
    assert any("404" in s for s in result)


def test_format_result_success(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("# Test", encoding="utf-8")
    r = {
        "doc_path": f,
        "url": "https://github.com/test/repo",
        "jaccard": 0.45,
        "common": ["agent", "memory"],
        "only_doc": ["unique"],
        "only_ext": ["external"],
        "missing_topics": ["missing"],
        "ext_len": 100,
        "doc_len": 200,
    }
    result = mod.format_result(r)
    assert isinstance(result, list)
    assert any("doc.md" in s for s in result)


def test_format_result_no_common(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("# Test", encoding="utf-8")
    r = {
        "doc_path": f,
        "url": "https://github.com/test/repo",
        "jaccard": 0.0,
        "common": [],
        "only_doc": [],
        "only_ext": [],
        "missing_topics": [],
        "ext_len": 50,
        "doc_len": 100,
    }
    result = mod.format_result(r)
    assert isinstance(result, list)


# ── _fetch_url ────────────────────────────────────────────────────────────────

def test_fetch_url_http_error(monkeypatch):
    """Test _fetch_url with HTTP error."""
    import urllib.error
    def fake_urlopen(req, timeout=None):
        raise urllib.error.HTTPError("url", 404, "Not Found", {}, None)
    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    result = mod._fetch_url("https://example.com/test")
    assert "HTTP 404" in result


def test_fetch_url_generic_error(monkeypatch):
    """Test _fetch_url with generic exception."""
    def fake_urlopen(req, timeout=None):
        raise OSError("Connection refused")
    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    result = mod._fetch_url("https://example.com/test")
    assert "Error" in result


def test_fetch_url_strips_html_tags(monkeypatch):
    """Test _fetch_url returns plain text."""
    from unittest.mock import MagicMock
    fake_resp = MagicMock()
    fake_resp.__enter__ = lambda s: s
    fake_resp.__exit__ = MagicMock(return_value=False)
    fake_resp.read.return_value = b"<html><body><p>Hello world agent</p></body></html>"
    monkeypatch.setattr("urllib.request.urlopen", lambda req, timeout=None: fake_resp)
    result = mod._fetch_url("https://example.com")
    assert "<html>" not in result
    assert "Hello" in result


# ── main with compare ─────────────────────────────────────────────────────────

def test_main_file_with_url_http_error(tmp_path, monkeypatch, capsys):
    f = tmp_path / "doc.md"
    f.write_text("# Test\n\nContent about agent memory.", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "AUTO", False)
    monkeypatch.setattr(mod, "FILE_ARG", f)
    monkeypatch.setattr(mod, "URL_ARG", "https://example.com/test")
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "_fetch_url", lambda url: "Error: Connection refused")
    mod.main()


def test_main_file_with_url_success(tmp_path, monkeypatch, capsys):
    f = tmp_path / "doc.md"
    f.write_text("# Agent Memory\n\nAgent memory knowledge retrieval.", encoding="utf-8")
    fake_ext = "Agent memory knowledge retrieval system capabilities."
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "AUTO", False)
    monkeypatch.setattr(mod, "FILE_ARG", f)
    monkeypatch.setattr(mod, "URL_ARG", "https://github.com/test/repo")
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "_fetch_url", lambda url: fake_ext)
    mod.main()
    out = capsys.readouterr().out
    assert "wrote" in out or "сравнений" in out


def test_main_query_with_url(tmp_path, monkeypatch, capsys):
    f = tmp_path / "agentfs.md"
    f.write_text("# AgentFS\n\nAgent file system memory knowledge.", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "AUTO", False)
    monkeypatch.setattr(mod, "FILE_ARG", None)
    monkeypatch.setattr(mod, "URL_ARG", "https://github.com/test/repo")
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "QUERY", "agentfs")
    monkeypatch.setattr(mod, "_fetch_url", lambda url: "AgentFS agent file system memory.")
    mod.main()


def test_main_query_no_doc_found(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "AUTO", False)
    monkeypatch.setattr(mod, "FILE_ARG", None)
    monkeypatch.setattr(mod, "URL_ARG", "https://github.com/test/repo")
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "QUERY", "nonexistent_xyz_query")
    mod.main()
    out = capsys.readouterr().out
    assert "не найден" in out or "not found" in out.lower()


def test_main_auto_with_url_in_doc(tmp_path, monkeypatch, capsys):
    f = tmp_path / "doc.md"
    f.write_text(
        "# Test Doc\n\nAgent memory knowledge system. See https://github.com/user/repo for details.",
        encoding="utf-8"
    )
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "AUTO", True)
    monkeypatch.setattr(mod, "FILE_ARG", None)
    monkeypatch.setattr(mod, "URL_ARG", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "LIMIT", 1)
    monkeypatch.setattr(mod, "_fetch_url", lambda url: "Agent file system memory.")
    mod.main()
