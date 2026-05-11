"""Tests for scripts/improve_duplicate_across.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_duplicate_across")


def test_tokens_returns_list():
    result = mod._tokens("agent memory knowledge system")
    assert isinstance(result, list)


def test_tokens_removes_stopwords():
    result = mod._tokens("the and for or but in on at")
    assert "the" not in result
    assert "and" not in result


def test_tokens_min_3_chars():
    result = mod._tokens("ab abc abcd")
    for t in result:
        assert len(t) >= 3


def test_shingles_returns_set():
    tokens = ["agent", "memory", "system", "knowledge", "data"]
    result = mod._shingles(tokens, n=2)
    assert isinstance(result, set)


def test_shingles_correct_size():
    tokens = ["a", "b", "c", "d"]
    result = mod._shingles(tokens, n=2)
    assert len(result) == 3  # ab, bc, cd


def test_shingles_empty_when_too_short():
    tokens = ["a", "b"]
    result = mod._shingles(tokens, n=4)
    assert result == set()


def test_jaccard_shingle_returns_float():
    s_a = {"a b", "b c", "c d"}
    s_b = {"a b", "b c", "x y"}
    result = mod._jaccard_shingle(s_a, s_b)
    assert isinstance(result, float)


def test_jaccard_shingle_identical():
    s = {"a b", "b c", "c d"}
    result = mod._jaccard_shingle(s, s)
    assert result == 1.0


def test_jaccard_shingle_empty():
    result = mod._jaccard_shingle(set(), set())
    assert result == 0.0


def test_jaccard_shingle_no_overlap():
    s_a = {"a b"}
    s_b = {"c d"}
    result = mod._jaccard_shingle(s_a, s_b)
    assert result == 0.0


def test_word_overlap_returns_float():
    tok_a = ["agent", "memory", "system"]
    tok_b = ["agent", "knowledge", "system"]
    result = mod._word_overlap(tok_a, tok_b)
    assert isinstance(result, float)


def test_word_overlap_identical():
    tokens = ["agent", "memory", "system"]
    result = mod._word_overlap(tokens, tokens)
    assert result == 1.0


def test_word_overlap_no_overlap():
    tok_a = ["agent"]
    tok_b = ["memory"]
    result = mod._word_overlap(tok_a, tok_b)
    assert result == 0.0


def test_verdict_returns_string():
    result = mod._verdict(0.7)
    assert isinstance(result, str)


def test_verdict_high_similarity():
    result = mod._verdict(0.8)
    assert "Вероятный" in result


def test_verdict_medium_similarity():
    result = mod._verdict(0.5)
    assert "Значительное" in result


def test_verdict_low_similarity():
    result = mod._verdict(0.2)
    assert "Умеренное" in result


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_duplicate_across_md_internal(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "INTERNAL", True)
    monkeypatch.setattr(mod, "OTHER_DIR", None)
    monkeypatch.setattr(mod, "OTHER_REPO", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    sec_a = tmp_path / "sec-a"
    sec_b = tmp_path / "sec-b"
    sec_a.mkdir()
    sec_b.mkdir()
    (sec_a / "doc1.md").write_text("# AgentFS\n\nAgent memory architecture.", encoding="utf-8")
    (sec_b / "doc2.md").write_text("# Yodoca\n\nMemory consolidation agent.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "DUPLICATE_ACROSS.md").exists()


def test_main_creates_duplicate_across_md_other_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "INTERNAL", False)
    monkeypatch.setattr(mod, "OTHER_DIR", tmp_path)
    monkeypatch.setattr(mod, "OTHER_REPO", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    (tmp_path / "doc1.md").write_text("# AgentFS\n\nContent.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "DUPLICATE_ACROSS.md").exists()


def test_main_duplicate_across_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "INTERNAL", True)
    monkeypatch.setattr(mod, "OTHER_DIR", None)
    monkeypatch.setattr(mod, "OTHER_REPO", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    sec = tmp_path / "sec-x"
    sec.mkdir()
    (sec / "doc.md").write_text("# AgentFS\n\nContent.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "DUPLICATE_ACROSS.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_no_flags_prints_usage(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "INTERNAL", False)
    monkeypatch.setattr(mod, "OTHER_DIR", None)
    monkeypatch.setattr(mod, "OTHER_REPO", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    captured = capsys.readouterr()
    assert "Использование" in captured.out or "--internal" in captured.out
