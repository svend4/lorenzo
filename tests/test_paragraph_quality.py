"""Tests for scripts/improve_paragraph_quality.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_paragraph_quality")


def test_paragraphs_returns_list():
    result = mod._paragraphs("Some text here.\n\nAnother paragraph.")
    assert isinstance(result, list)


def test_paragraphs_splits_on_blank_line():
    result = mod._paragraphs("First paragraph words.\n\nSecond paragraph words.")
    assert len(result) >= 2


def test_paragraphs_strips_code():
    result = mod._paragraphs("```python\ncode here\n```\n\nReal paragraph text.")
    texts = " ".join(result)
    assert "code here" not in texts


def test_paragraphs_strips_headings():
    result = mod._paragraphs("# Title\n\nReal content paragraph text here now.")
    texts = " ".join(result)
    assert "Title" not in texts


def test_tokens_returns_list():
    result = mod._tokens("hello world test")
    assert isinstance(result, list)


def test_tokens_min_3_chars():
    result = mod._tokens("ab abc abcd")
    for t in result:
        assert len(t) >= 3


def test_tokens_lowercased():
    result = mod._tokens("HELLO World")
    assert all(t == t.lower() for t in result)


def test_jaccard_returns_float():
    a = ["hello", "world"]
    b = ["world", "test"]
    result = mod._jaccard(a, b)
    assert isinstance(result, float)


def test_jaccard_identical():
    tokens = ["hello", "world"]
    result = mod._jaccard(tokens, tokens)
    assert result == 1.0


def test_jaccard_empty():
    result = mod._jaccard([], [])
    assert result == 0.0


def test_jaccard_no_overlap():
    result = mod._jaccard(["hello"], ["world"])
    assert result == 0.0


def test_water_ratio_returns_float():
    result = mod._water_ratio("this is a test")
    assert isinstance(result, float)


def test_water_ratio_stopword_heavy():
    result = mod._water_ratio("the and for or but in on at to for")
    assert result > 0.5


def test_water_ratio_no_stopwords():
    result = mod._water_ratio("agent memory system knowledge retrieval")
    assert result < 0.3


def test_is_truncated_no_punctuation():
    result = mod._is_truncated("This sentence has no ending")
    assert result is True


def test_is_truncated_with_period():
    result = mod._is_truncated("This sentence ends properly.")
    assert result is False


def test_is_truncated_with_question():
    result = mod._is_truncated("Does it end here?")
    assert result is False


def test_max_sentence_length_returns_int():
    result = mod._max_sentence_length("Hello world test.")
    assert isinstance(result, int)


def test_max_sentence_length_correct():
    result = mod._max_sentence_length("One word. Two words here.")
    assert result >= 3


def test_repeating_starts_returns_list():
    paras = ["one text", "one text again", "one more text"]
    result = mod._repeating_starts(paras)
    assert isinstance(result, list)


def test_repeating_starts_detects_three():
    paras = [
        "система анализирует данные запроса",
        "система обрабатывает входящий поток",
        "система отвечает на запросы пользователей",
    ]
    result = mod._repeating_starts(paras)
    assert len(result) == 3


def test_repeating_starts_no_repeat():
    paras = ["first text here", "second text here", "third text here"]
    result = mod._repeating_starts(paras)
    assert len(result) == 0


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_paragraph_quality_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    assert (tmp_path / "PARAGRAPH_QUALITY.md").exists()


def test_main_paragraph_quality_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    (tmp_path / "doc.md").write_text(
        "# Title\n\nContent about agent systems.", encoding="utf-8"
    )
    mod.main()
    text = (tmp_path / "PARAGRAPH_QUALITY.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    assert (tmp_path / "PARAGRAPH_QUALITY.md").exists()


def test_main_paragraph_quality_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    text = (tmp_path / "PARAGRAPH_QUALITY.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
