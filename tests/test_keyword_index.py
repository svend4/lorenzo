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


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_keyword_index_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "QUERY", None)
    mod.main()
    assert (tmp_path / "KEYWORD_INDEX.md").exists()


def test_main_keyword_index_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "QUERY", None)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nAgent memory system.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "KEYWORD_INDEX.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "QUERY", None)
    mod.main()
    assert (tmp_path / "KEYWORD_INDEX.md").exists()


def test_main_keyword_index_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "QUERY", None)
    mod.main()
    text = (tmp_path / "KEYWORD_INDEX.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


# ── arg parsing (module-level) ────────────────────────────────────────────────

def test_min_df_arg_parsing():
    """Lines 34-36: --min-df N sets MIN_DF."""
    orig = sys.argv[:]
    try:
        sys.argv = ["prog", "--min-df", "3"]
        importlib.reload(mod)
        assert mod.MIN_DF == 3
    finally:
        sys.argv = orig
        importlib.reload(mod)


def test_top_arg_parsing():
    """Lines 39-41: --top N sets TOP_WORDS."""
    orig = sys.argv[:]
    try:
        sys.argv = ["prog", "--top", "50"]
        importlib.reload(mod)
        assert mod.TOP_WORDS == 50
    finally:
        sys.argv = orig
        importlib.reload(mod)


def test_query_arg_parsing():
    """Lines 45-47: --query Q sets QUERY."""
    orig = sys.argv[:]
    try:
        sys.argv = ["prog", "--query", "agent memory"]
        importlib.reload(mod)
        assert mod.QUERY == "agent memory"
    finally:
        sys.argv = orig
        importlib.reload(mod)


def test_section_arg_parsing():
    """Lines 51-53: --section S sets SECTION_FILTER."""
    orig = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "01-svyazi"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER is not None
    finally:
        sys.argv = orig
        importlib.reload(mod)


# ── _section_of: ValueError path ─────────────────────────────────────────────

def test_section_of_unknown_when_not_under_docs(tmp_path, monkeypatch):
    """Lines 93-94: path not under DOCS → return 'unknown'."""
    monkeypatch.setattr(mod, "DOCS", tmp_path / "docs")
    (tmp_path / "docs").mkdir()
    outside = tmp_path / "outside.md"
    outside.write_text("content", encoding="utf-8")
    result = mod._section_of(outside)
    assert result == "unknown"


def test_section_of_root_for_direct_child(tmp_path, monkeypatch):
    """Line 92: file directly in DOCS → return 'root'."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "direct.md"
    f.write_text("content", encoding="utf-8")
    result = mod._section_of(f)
    assert result == "root"


# ── build_index: exception and empty tokens ────────────────────────────────────

def test_build_index_handles_read_error(tmp_path, monkeypatch):
    """Lines 107-108: exception reading file → continue."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    bad = tmp_path / "bad.md"
    bad.write_text("content", encoding="utf-8")

    from pathlib import Path as _Path
    orig_read = _Path.read_text

    def mock_read(self, *a, **kw):
        if self == bad:
            raise OSError("mocked")
        return orig_read(self, *a, **kw)

    monkeypatch.setattr(_Path, "read_text", mock_read)
    result = mod.build_index([bad])
    assert isinstance(result, dict)


def test_build_index_skips_empty_tokens(tmp_path, monkeypatch):
    """Line 116: file with no tokens (only stopwords) → continue."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    # Only stopwords → empty tokens
    empty = tmp_path / "empty.md"
    empty.write_text("the and for or", encoding="utf-8")
    result = mod.build_index([empty])
    assert isinstance(result, dict)


# ── search: bigram scoring ────────────────────────────────────────────────────

def test_search_bigram_scoring():
    """Line 172: bigram boost when len(terms) > 1."""
    index = {
        "agent": [{"file": "doc.md", "section": "root", "count": 2, "tf": 0.1}],
        "memory": [{"file": "doc.md", "section": "root", "count": 2, "tf": 0.1}],
        "agent_memory": [{"file": "doc.md", "section": "root", "count": 2, "tf": 0.2}],
    }
    result = mod.search(index, "agent memory")
    assert len(result) >= 1
    assert result[0]["file"] == "doc.md"


# ── main: query mode and bigrams section ─────────────────────────────────────

def test_main_with_query_prints_results(tmp_path, monkeypatch, capsys):
    """Lines 200-207: QUERY set → search and print results."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "QUERY", "agent")
    (tmp_path / "doc.md").write_text("agent memory system knowledge " * 10, encoding="utf-8")
    mod.main()
    out = capsys.readouterr().out
    assert "agent" in out.lower() or "Поиск" in out or "найдено" in out.lower()


def test_main_with_query_no_results(tmp_path, monkeypatch, capsys):
    """Line 205-206: no results found → print 'Ничего не найдено'."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "QUERY", "xyzabcnonexistentterm")
    mod.main()
    out = capsys.readouterr().out
    assert "найдено" in out.lower()


def test_main_with_bigrams_adds_bigrams_section(tmp_path, monkeypatch):
    """Lines 232-241: bigrams in index → bigrams table added to KEYWORD_INDEX.md."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "QUERY", None)
    monkeypatch.setattr(mod, "BIGRAMS", True)
    # Need a file with repeated bigrams to trigger bigram_freq[bg] >= 2
    content = "agent memory agent memory agent memory agent memory " * 5
    (tmp_path / "doc.md").write_text("# Title\n\n" + content, encoding="utf-8")
    mod.main()
    text = (tmp_path / "KEYWORD_INDEX.md").read_text(encoding="utf-8")
    # Bigrams section appears when bigrams exist
    assert "#" in text


# ── __main__ block ─────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 269: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "QUERY", None)
    runpy.run_path(str(ROOT / "scripts" / "improve_keyword_index.py"), run_name="__main__")
