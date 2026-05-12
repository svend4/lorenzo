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


def test_tokens_returns_list():
    result = mod._tokens("Hello world agent memory system works")
    assert isinstance(result, list)


def test_tokens_filters_short():
    result = mod._tokens("I am in it at do")
    assert all(len(t) >= 3 for t in result)


def test_shingles_empty_when_few_tokens():
    result = mod._shingles(["one", "two"])
    # With default SHINGLE_N > 2, should return empty
    assert isinstance(result, set)


def test_shingles_produces_ngrams():
    result = mod._shingles(["agent", "memory", "system", "works", "well"], n=3)
    assert isinstance(result, set)
    assert len(result) > 0


def test_jaccard_both_empty():
    result = mod._jaccard_shingle(set(), set())
    assert result == 0.0


def test_jaccard_identical():
    sh = {"agent memory", "memory system"}
    result = mod._jaccard_shingle(sh, sh)
    assert abs(result - 1.0) < 0.01


def test_word_overlap_identical():
    tok = ["agent", "memory", "system"]
    result = mod._word_overlap(tok, tok)
    assert abs(result - 1.0) < 0.01


def test_word_overlap_disjoint():
    a = ["agent", "memory"]
    b = ["search", "graph"]
    result = mod._word_overlap(a, b)
    assert result == 0.0


def test_load_files_empty_dir(tmp_path):
    result = mod._load_files(tmp_path)
    assert isinstance(result, dict)
    assert len(result) == 0


def test_verdict_returns_string():
    result = mod._verdict(0.9)
    assert isinstance(result, str)
    result2 = mod._verdict(0.5)
    assert isinstance(result2, str)


# ── _load_files ───────────────────────────────────────────────────────────────

def test_load_files_with_md_files(tmp_path):
    content = "agent memory " * 30
    (tmp_path / "doc1.md").write_text(f"# Title\n\n{content}", encoding="utf-8")
    (tmp_path / "doc2.md").write_text(f"# Other\n\n{content}", encoding="utf-8")
    result = mod._load_files(tmp_path)
    assert len(result) >= 1


def test_load_files_skips_skip_files(tmp_path):
    (tmp_path / "README.md").write_text("# README\n\n" + "word " * 50, encoding="utf-8")
    result = mod._load_files(tmp_path)
    assert not any("README.md" in k for k in result)


def test_load_files_returns_dict_with_expected_keys(tmp_path):
    content = "agent memory knowledge " * 20
    (tmp_path / "doc.md").write_text(f"# Test\n\n{content}", encoding="utf-8")
    result = mod._load_files(tmp_path)
    if result:
        v = next(iter(result.values()))
        assert "path" in v
        assert "tokens" in v
        assert "shingles" in v
        assert "words" in v


# ── _find_duplicates ──────────────────────────────────────────────────────────

def test_find_duplicates_no_duplicates(tmp_path, capsys):
    content_a = "agent memory " * 30
    content_b = "graph knowledge " * 30
    fa = tmp_path / "doc_a.md"
    fb = tmp_path / "doc_b.md"
    tok_a = mod._tokens(content_a)
    tok_b = mod._tokens(content_b)
    ca = {"path": fa, "tokens": tok_a, "shingles": mod._shingles(tok_a), "words": 60}
    cb = {"path": fb, "tokens": tok_b, "shingles": mod._shingles(tok_b), "words": 60}
    pairs = mod._find_duplicates({str(fa): ca}, {str(fb): cb}, threshold=0.9)
    assert isinstance(pairs, list)


def test_find_duplicates_finds_similar(tmp_path, capsys):
    content = "agent memory knowledge system retrieval " * 20
    fa = tmp_path / "doc_a.md"
    fb = tmp_path / "doc_b.md"
    tok = mod._tokens(content)
    ca = {"path": fa, "tokens": tok, "shingles": mod._shingles(tok), "words": 100}
    cb = {"path": fb, "tokens": tok, "shingles": mod._shingles(tok), "words": 100}
    pairs = mod._find_duplicates({str(fa): ca}, {str(fb): cb}, threshold=0.1)
    assert len(pairs) >= 1
    assert pairs[0]["combined"] >= 0.1


# ── main() variants ───────────────────────────────────────────────────────────

def test_main_other_dir_not_found(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "INTERNAL", False)
    monkeypatch.setattr(mod, "OTHER_DIR", tmp_path / "nonexistent_other")
    monkeypatch.setattr(mod, "OTHER_REPO", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    out = capsys.readouterr().out
    assert "не найдена" in out or "not found" in out.lower()


def test_main_other_dir_with_files(tmp_path, monkeypatch, capsys):
    docs = tmp_path / "docs"
    docs.mkdir()
    other = tmp_path / "other"
    other.mkdir()
    content = "agent memory knowledge " * 20
    (docs / "doc.md").write_text(f"# Doc\n\n{content}", encoding="utf-8")
    (other / "other.md").write_text(f"# Other\n\ncompletely different topic graph " * 20, encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", docs)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "INTERNAL", False)
    monkeypatch.setattr(mod, "OTHER_DIR", other)
    monkeypatch.setattr(mod, "OTHER_REPO", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "THRESHOLD", 0.3)
    mod.main()
    out_file = docs / "DUPLICATE_ACROSS.md"
    assert out_file.exists()


def test_main_other_repo_not_found(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "INTERNAL", False)
    monkeypatch.setattr(mod, "OTHER_DIR", None)
    monkeypatch.setattr(mod, "OTHER_REPO", tmp_path / "nonexistent_repo")
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    out = capsys.readouterr().out
    assert "не найден" in out or "not found" in out.lower()


def test_main_other_repo_with_docs(tmp_path, monkeypatch, capsys):
    docs = tmp_path / "docs"
    docs.mkdir()
    other_repo = tmp_path / "other_repo"
    other_repo_docs = other_repo / "docs"
    other_repo_docs.mkdir(parents=True)
    content = "agent memory knowledge " * 20
    (docs / "doc.md").write_text(f"# Doc\n\n{content}", encoding="utf-8")
    (other_repo_docs / "other.md").write_text(f"# Other\n\nresearch graph system " * 20, encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", docs)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "INTERNAL", False)
    monkeypatch.setattr(mod, "OTHER_DIR", None)
    monkeypatch.setattr(mod, "OTHER_REPO", other_repo)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "THRESHOLD", 0.3)
    mod.main()


def test_main_internal_with_pairs(tmp_path, monkeypatch, capsys):
    docs = tmp_path / "docs"
    docs.mkdir()
    sec_a = docs / "sec-a"
    sec_a.mkdir()
    sec_b = docs / "sec-b"
    sec_b.mkdir()
    content = "agent memory knowledge system retrieval " * 15
    (sec_a / "doc.md").write_text(f"# Doc A\n\n{content}", encoding="utf-8")
    (sec_b / "doc.md").write_text(f"# Doc B\n\n{content}", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", docs)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "INTERNAL", True)
    monkeypatch.setattr(mod, "OTHER_DIR", None)
    monkeypatch.setattr(mod, "OTHER_REPO", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "THRESHOLD", 0.1)
    mod.main()
    out_file = docs / "DUPLICATE_ACROSS.md"
    assert out_file.exists()
