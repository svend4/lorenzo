"""Tests for scripts/improve_subtopic_fill.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_subtopic_fill")


def test_word_count_returns_int():
    result = mod._word_count("hello world test")
    assert isinstance(result, int)


def test_word_count_counts():
    result = mod._word_count("one two three")
    assert result == 3


def test_word_count_empty():
    result = mod._word_count("")
    assert result == 0


def test_clean_returns_string():
    result = mod._clean("some text here")
    assert isinstance(result, str)


def test_clean_removes_code():
    result = mod._clean("Before\n```python\ncode here\n```\nAfter")
    assert "code here" not in result


def test_top_words_returns_set():
    result = mod._top_words("agent memory knowledge system retrieval data " * 5)
    assert isinstance(result, set)


def test_top_words_respects_n():
    result = mod._top_words("agent memory knowledge system retrieval data " * 5, n=3)
    assert len(result) <= 3


def test_relevance_returns_float():
    stub_words = {"agent", "memory", "system"}
    source = "agent memory retrieval system data knowledge"
    result = mod._relevance(stub_words, source)
    assert isinstance(result, float)
    assert 0 <= result <= 1


def test_relevance_zero_for_empty():
    result = mod._relevance(set(), "some text here")
    assert result == 0.0


def test_relevance_high_for_similar():
    stub_words = {"agent", "memory", "knowledge", "system"}
    source = "agent memory knowledge system retrieval data " * 5
    result = mod._relevance(stub_words, source)
    assert result > 0.0


def test_extract_best_paragraph_returns_string():
    text = "# Title\n\nFirst paragraph about agent memory.\n\nSecond paragraph about knowledge graphs."
    query_words = {"agent", "memory"}
    result = mod._extract_best_paragraph(text, query_words)
    assert isinstance(result, str)


def test_extract_best_paragraph_finds_relevant():
    para = "Agent memory system retrieval data processing knowledge graph architecture pipeline."
    # Ensure it's > 80 chars (the minimum for the function)
    assert len(para) > 80
    text = f"Some intro text unrelated to the main topic.\n\n{para}\n\nCompletely unrelated stuff about other topics."
    query_words = {"agent", "memory", "system"}
    result = mod._extract_best_paragraph(text, query_words)
    assert len(result) > 0


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    mod.main()  # no stubs → returns early, must not raise


def test_main_with_stub_file_dry_run(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    (tmp_path / "stub.md").write_text("# Short stub\n\nBrief.", encoding="utf-8")
    (tmp_path / "full.md").write_text(
        "# Full Doc\n\n" + "Content about agent memory systems. " * 50, encoding="utf-8"
    )
    mod.main()  # must not raise


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    mod.main()  # must not raise
