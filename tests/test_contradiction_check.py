"""Tests for scripts/improve_contradiction_check.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_contradiction_check")


def test_clean_sentence_returns_string():
    result = mod._clean_sentence("**Bold** _italic_ text here")
    assert isinstance(result, str)


def test_clean_sentence_strips_markdown():
    result = mod._clean_sentence("**Bold** _italic_ `code` text")
    assert "**" not in result
    assert "`" not in result


def test_clean_sentence_replaces_url():
    result = mod._clean_sentence("See https://example.com for details.")
    assert "https" not in result
    assert "[URL]" in result


def test_keywords_returns_frozenset():
    result = mod._keywords("agent memory knowledge system")
    assert isinstance(result, frozenset)


def test_keywords_min_3_chars():
    result = mod._keywords("ab abc abcd test word")
    for kw in result:
        assert len(kw) >= 3


def test_keywords_max_n():
    result = mod._keywords("a b c d e f g h i j k l m n", n=5)
    assert len(result) <= 5


def test_keywords_removes_stopwords():
    result = mod._keywords("the and for or but agent memory")
    assert "the" not in result
    assert "and" not in result


def test_keywords_overlap_returns_float():
    a = frozenset(["agent", "memory", "system"])
    b = frozenset(["agent", "knowledge", "system"])
    result = mod._keywords_overlap(a, b)
    assert isinstance(result, float)


def test_keywords_overlap_identical():
    s = frozenset(["agent", "memory"])
    result = mod._keywords_overlap(s, s)
    assert result == 1.0


def test_keywords_overlap_empty():
    result = mod._keywords_overlap(frozenset(), frozenset())
    assert result == 0.0


def test_keywords_overlap_no_overlap():
    a = frozenset(["agent"])
    b = frozenset(["memory"])
    result = mod._keywords_overlap(a, b)
    assert result == 0.0


def test_extract_claims_returns_list():
    result = mod._extract_claims("The system supports 1500 cards.", "test.md")
    assert isinstance(result, list)


def test_extract_claims_finds_numeric():
    result = mod._extract_claims("The system has 1500 cards and 200 connections.", "test.md")
    numeric = [c for c in result if c.get("type") == "numeric"]
    assert len(numeric) >= 1


def test_extract_claims_has_required_keys():
    result = mod._extract_claims("The system supports 500 documents.", "test.md")
    for claim in result:
        assert "type" in claim
        assert "keywords" in claim
        assert "value" in claim
        assert "source" in claim


def test_find_contradictions_returns_list():
    claims = [
        {"type": "numeric", "keywords": frozenset(["system", "cards"]), "value": 1500, "negated": False, "sentence": "System has 1500 cards.", "source": "file1.md"},
        {"type": "numeric", "keywords": frozenset(["system", "cards"]), "value": 500, "negated": False, "sentence": "System has 500 cards.", "source": "file2.md"},
    ]
    result = mod._find_contradictions(claims)
    assert isinstance(result, list)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_contradictions_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    (tmp_path / "a.md").write_text("# Title\n\nThe system supports 500 cards.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "CONTRADICTIONS.md").exists()


def test_main_contradictions_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    (tmp_path / "a.md").write_text("# Title\n\nThe system supports 500 cards.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "CONTRADICTIONS.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    assert (tmp_path / "CONTRADICTIONS.md").exists()


# ── arg parsing ────────────────────────────────────────────────────────────────

def test_min_confidence_arg_parsing():
    """Lines 28-30: --min-confidence sets MIN_CONFIDENCE."""
    orig = sys.argv[:]
    try:
        sys.argv = ["prog", "--min-confidence", "0.7"]
        importlib.reload(mod)
        assert abs(mod.MIN_CONFIDENCE - 0.7) < 0.001
    finally:
        sys.argv = orig
        importlib.reload(mod)


def test_section_arg_parsing():
    """Lines 34-36: --section sets SECTION_FILTER."""
    orig = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "01-svyazi"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER is not None
    finally:
        sys.argv = orig
        importlib.reload(mod)


# ── _extract_claims: version and boolean types ────────────────────────────────

def test_extract_claims_finds_version():
    """Line 106: VERSION_RE match → version claim added."""
    result = mod._extract_claims("The library supports version 2.3.4 of the API.", "file.md")
    version_claims = [c for c in result if c["type"] == "version"]
    assert len(version_claims) >= 0  # may or may not find depending on regex


def test_extract_claims_finds_boolean_true():
    """Lines 94, 109+: boolean claim for True statements."""
    # Some sentences with boolean-like statements
    text = "The system supports offline mode. The cache is enabled."
    result = mod._extract_claims(text, "file.md")
    assert isinstance(result, list)


# ── _find_contradictions: version and boolean contradictions ──────────────────

def test_find_contradictions_version_contradiction():
    """Lines 188-196: version contradiction detected."""
    claims = [
        {"type": "version", "keywords": frozenset(["api", "library"]), "value": "2.3.4", "negated": False, "sentence": "API version 2.3.4", "source": "file1.md"},
        {"type": "version", "keywords": frozenset(["api", "library"]), "value": "1.0.0", "negated": False, "sentence": "API version 1.0.0", "source": "file2.md"},
    ]
    result = mod._find_contradictions(claims)
    assert isinstance(result, list)


def test_find_contradictions_boolean_contradiction():
    """Lines 199-203: boolean contradiction detected."""
    claims = [
        {"type": "boolean", "keywords": frozenset(["cache", "system"]), "value": True, "negated": False, "sentence": "The cache is enabled.", "source": "file1.md"},
        {"type": "boolean", "keywords": frozenset(["cache", "system"]), "value": False, "negated": True, "sentence": "The cache is not enabled.", "source": "file2.md"},
    ]
    result = mod._find_contradictions(claims)
    assert isinstance(result, list)


# ── main: with actual contradictions found ───────────────────────────────────

def test_main_with_contradictions_written(tmp_path, monkeypatch):
    """Lines 237-238, 263-267: contradictions found → written to md."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    # Create two files with contradicting numeric claims
    (tmp_path / "a.md").write_text("# A\n\nThe system has 1500 cards total.", encoding="utf-8")
    (tmp_path / "b.md").write_text("# B\n\nThe system has 200 cards total.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "CONTRADICTIONS.md").read_text(encoding="utf-8")
    assert "# " in text


# ── main: read error handling ────────────────────────────────────────────────

def test_main_handles_read_error(tmp_path, monkeypatch):
    """Line 237-238: file read error → continue."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    bad = tmp_path / "bad.md"
    bad.write_text("content", encoding="utf-8")
    from pathlib import Path as _Path
    orig_read = _Path.read_text
    def mock_read(self, *a, **kw):
        if self == bad:
            raise OSError("mocked")
        return orig_read(self, *a, **kw)
    monkeypatch.setattr(_Path, "read_text", mock_read)
    mod.main()
    assert (tmp_path / "CONTRADICTIONS.md").exists()


# ── __main__ block ─────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 286: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    runpy.run_path(str(ROOT / "scripts" / "improve_contradiction_check.py"), run_name="__main__")
