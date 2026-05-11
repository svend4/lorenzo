"""Tests for scripts/utils_chunker.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("utils_chunker")


def test_chunk_fixed_returns_list():
    result = mod.chunk_fixed("one two three four five six", words=3)
    assert isinstance(result, list)


def test_chunk_fixed_splits_by_word_count():
    text = " ".join(f"word{i}" for i in range(10))
    result = mod.chunk_fixed(text, words=3)
    assert len(result) >= 3


def test_chunk_fixed_last_chunk_smaller():
    text = " ".join(f"w{i}" for i in range(7))
    result = mod.chunk_fixed(text, words=3)
    assert len(result) == 3  # 3+3+1


def test_chunk_fixed_empty_text():
    result = mod.chunk_fixed("", words=100)
    assert result == []


def test_chunk_overlap_returns_list():
    result = mod.chunk_overlap("one two three four five six", words=4, overlap=2)
    assert isinstance(result, list)


def test_chunk_overlap_creates_overlap():
    words = [f"w{i}" for i in range(20)]
    text = " ".join(words)
    chunks = mod.chunk_overlap(text, words=10, overlap=5)
    # With overlap, consecutive chunks share words
    if len(chunks) >= 2:
        first_words = set(chunks[0].split())
        second_words = set(chunks[1].split())
        assert len(first_words & second_words) > 0


def test_chunk_overlap_empty_text():
    result = mod.chunk_overlap("", words=100, overlap=20)
    assert result == []


def test_chunk_by_headers_returns_list():
    text = "# Title\n\nContent.\n\n## Section\n\nMore."
    result = mod.chunk_by_headers(text)
    assert isinstance(result, list)


def test_chunk_by_headers_splits_on_headings():
    text = "# H1\n\nContent A.\n\n## H2\n\nContent B.\n\n### H3\n\nContent C."
    result = mod.chunk_by_headers(text, max_words=1000)
    assert len(result) >= 2


def test_chunk_by_headers_handles_long_section():
    long_section = "word " * 3000
    text = f"# Title\n\n{long_section}"
    result = mod.chunk_by_headers(text, max_words=100)
    assert len(result) > 1


def test_chunk_by_headers_empty():
    result = mod.chunk_by_headers("")
    assert result == []


def test_chunk_by_paragraphs_returns_list():
    text = "Para one.\n\nPara two.\n\nPara three."
    result = mod.chunk_by_paragraphs(text)
    assert isinstance(result, list)


def test_chunk_by_paragraphs_groups_short():
    short_paras = "\n\n".join([f"word{i}" for i in range(20)])
    result = mod.chunk_by_paragraphs(short_paras, max_words=5)
    for chunk in result:
        words = len(chunk.split())
        # Each chunk should not far exceed max_words (might exceed by 1 para)
        assert words <= 10


def test_chunk_by_paragraphs_empty():
    result = mod.chunk_by_paragraphs("")
    assert result == []


def test_word_count_returns_int():
    result = mod.word_count("one two three")
    assert isinstance(result, int)
    assert result == 3


def test_word_count_empty():
    assert mod.word_count("") == 0


def test_word_count_multiline():
    text = "line one\nline two\nline three"
    assert mod.word_count(text) == 6


def test_estimate_tokens_returns_int():
    result = mod.estimate_tokens("one two three four five")
    assert isinstance(result, int)


def test_estimate_tokens_approximately_1_3x_words():
    words = "word " * 100
    result = mod.estimate_tokens(words)
    assert 120 <= result <= 140  # ~1.3x


def test_fits_context_returns_bool():
    result = mod.fits_context("short text")
    assert isinstance(result, bool)


def test_fits_context_short_text():
    assert mod.fits_context("short text", max_tokens=1000) is True


def test_fits_context_too_long():
    long_text = "word " * 200_000
    assert mod.fits_context(long_text, max_tokens=100) is False


def test_iter_md_files_returns_iterator(tmp_path):
    (tmp_path / "docs").mkdir()
    f = tmp_path / "docs" / "doc.md"
    f.write_text("# Hello", encoding="utf-8")
    result = list(mod.iter_md_files(tmp_path))
    assert f in result


def test_iter_md_files_skips_readme(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    readme = docs / "README.md"
    readme.write_text("# README", encoding="utf-8")
    result = list(mod.iter_md_files(tmp_path))
    assert readme not in result


def test_iter_md_files_chunked_returns_tuples(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    f = docs / "doc.md"
    f.write_text("# Title\n\nContent here.\n\n## Section\n\nMore content.", encoding="utf-8")
    result = list(mod.iter_md_files_chunked(tmp_path))
    for item in result:
        assert isinstance(item, tuple)
        assert len(item) == 3
        path, idx, chunk = item
        assert isinstance(path, Path)
        assert isinstance(idx, int)
        assert isinstance(chunk, str)
