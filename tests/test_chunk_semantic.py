"""Tests for scripts/improve_chunk_semantic.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_chunk_semantic")


def test_clean_text_returns_string():
    result = mod._clean_text("some text here")
    assert isinstance(result, str)


def test_clean_text_removes_code():
    result = mod._clean_text("Before\n```python\ncode here\n```\nAfter")
    assert "code here" not in result
    assert "CODE BLOCK" in result


def test_clean_text_removes_markdown():
    result = mod._clean_text("**bold** _italic_ text")
    assert "**" not in result
    assert "_" not in result


def test_clean_text_replaces_url():
    result = mod._clean_text("See https://example.com for details.")
    assert "[URL]" in result


def test_word_count_returns_int():
    result = mod._word_count("hello world test")
    assert isinstance(result, int)


def test_word_count_correct():
    result = mod._word_count("one two three four five")
    assert result == 5


def test_chunk_id_returns_string():
    result = mod._chunk_id("docs/test.md", "Introduction", 0)
    assert isinstance(result, str)


def test_chunk_id_length_12():
    result = mod._chunk_id("docs/test.md", "Introduction", 0)
    assert len(result) == 12


def test_chunk_id_deterministic():
    r1 = mod._chunk_id("docs/test.md", "Introduction", 0)
    r2 = mod._chunk_id("docs/test.md", "Introduction", 0)
    assert r1 == r2


def test_chunk_id_different_for_different_input():
    r1 = mod._chunk_id("docs/test.md", "Introduction", 0)
    r2 = mod._chunk_id("docs/test.md", "Introduction", 1)
    assert r1 != r2


def test_split_by_headings_returns_list():
    text = "# Title\n\nContent here.\n\n## Section\n\nMore content.\n"
    result = mod._split_by_headings(text)
    assert isinstance(result, list)


def test_split_by_headings_each_is_tuple():
    text = "# Title\n\nContent.\n## Section\n\nContent.\n"
    result = mod._split_by_headings(text)
    for item in result:
        assert isinstance(item, tuple)
        assert len(item) == 3


def test_split_by_headings_tracks_parent():
    text = "# Parent\n\nIntro.\n## Child\n\nChild content.\n"
    result = mod._split_by_headings(text)
    children = [(p, h, t) for p, h, t in result if h == "Child"]
    assert len(children) >= 1
    assert children[0][0] == "Parent"


def test_split_by_headings_no_headings():
    text = "Just plain text without any headings here."
    result = mod._split_by_headings(text)
    assert len(result) == 1
    assert result[0] == ("", "", text)


def test_split_by_paragraphs_returns_list():
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
    result = mod._split_by_paragraphs(text, max_words=100)
    assert isinstance(result, list)


def test_split_by_paragraphs_respects_max():
    text = "word " * 200 + "\n\n" + "word " * 200
    result = mod._split_by_paragraphs(text, max_words=150)
    assert len(result) >= 2


def test_chunk_file_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    f.write_text(
        "# Title\n\n" + "word " * 100 + "\n\n## Section\n\n" + "content " * 100,
        encoding="utf-8"
    )
    result = mod.chunk_file(f)
    assert isinstance(result, list)


def test_chunk_file_entries_have_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    f.write_text(
        "# Title\n\n" + "word " * 100 + "\n\n## Section\n\n" + "content " * 100,
        encoding="utf-8"
    )
    result = mod.chunk_file(f)
    for chunk in result:
        assert "id" in chunk
        assert "source" in chunk
        assert "text" in chunk
        assert "word_count" in chunk


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_chunks_dir(tmp_path, monkeypatch):
    chunks_dir = tmp_path / "chunks"
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "OUTPUT_DIR", chunks_dir)
    mod.main()
    assert chunks_dir.exists()


def test_main_creates_all_chunks_jsonl(tmp_path, monkeypatch):
    chunks_dir = tmp_path / "chunks"
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "OUTPUT_DIR", chunks_dir)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent about memory.", encoding="utf-8")
    mod.main()
    assert (chunks_dir / "all_chunks.jsonl").exists()


def test_main_empty_docs(tmp_path, monkeypatch):
    chunks_dir = tmp_path / "chunks"
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "OUTPUT_DIR", chunks_dir)
    mod.main()  # no files → creates empty all_chunks.jsonl
    assert (chunks_dir / "all_chunks.jsonl").exists()
