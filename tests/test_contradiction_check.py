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
