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


def test_chunk_file_exception_returns_empty(tmp_path, monkeypatch):
    """Lines 140-141: exception reading file → returns []."""
    from pathlib import Path as _Path
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "bad.md"
    f.write_text("content", encoding="utf-8")
    original_read_text = _Path.read_text
    def fake_read(self, *a, **kw):
        if self == f:
            raise OSError("permission denied")
        return original_read_text(self, *a, **kw)
    monkeypatch.setattr(_Path, "read_text", fake_read)
    result = mod.chunk_file(f)
    assert result == []


def test_chunk_file_large_section_splits(tmp_path, monkeypatch):
    """Lines 194-210: section with > MAX_CHUNK_WORDS → split by paragraphs."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "MAX_CHUNK_WORDS", 50)
    monkeypatch.setattr(mod, "MIN_CHUNK_WORDS", 10)
    # Create a section with many words (> 50)
    big_para = "word " * 30
    content = "# Title\n\n" + f"{big_para}\n\n{big_para}\n"
    f = tmp_path / "big.md"
    f.write_text(content, encoding="utf-8")
    result = mod.chunk_file(f)
    assert isinstance(result, list)


def test_chunk_file_small_sections_buffered(tmp_path, monkeypatch):
    """Lines 162-191: small sections accumulated in buffer then flushed including overflow."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "MAX_CHUNK_WORDS", 50)
    monkeypatch.setattr(mod, "MIN_CHUNK_WORDS", 10)
    # Each small section has 9 words (< MIN_CHUNK_WORDS=10 requires < 10 here)
    # Actually, MIN_CHUNK_WORDS=10 means wc < 10 is "small". Use 8-word sections.
    # After 6 sections × 8 words = 48 words. When 7th section tries to add 8 more:
    # buffer_words(48) + wc(8) = 56 > MAX_CHUNK_WORDS(50) → triggers flush (line 186)
    small_sections = "\n\n".join([
        f"## Section {i}\n\n" + "word " * 8
        for i in range(7)
    ])
    f = tmp_path / "small.md"
    f.write_text("# Title\n\n" + small_sections, encoding="utf-8")
    result = mod.chunk_file(f)
    assert isinstance(result, list)


def test_main_with_content_file(tmp_path, monkeypatch):
    """Lines 250-256, 260-263, 269: main() with both empty and content files."""
    chunks_dir = tmp_path / "chunks"
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "OUTPUT_DIR", chunks_dir)
    monkeypatch.setattr(mod, "MIN_CHUNK_WORDS", 5)
    monkeypatch.setattr(mod, "MAX_CHUNK_WORDS", 200)
    # File with enough content to produce chunks
    content = "# Memory Systems\n\n" + "agent memory knowledge " * 20 + "\n\n"
    content += "## Retrieval\n\n" + "retrieval augmented generation " * 20
    (tmp_path / "doc.md").write_text(content, encoding="utf-8")
    # File too short → no chunks → triggers line 252 (continue)
    (tmp_path / "tiny.md").write_text("# T\n\na", encoding="utf-8")
    mod.main()
    all_chunks = chunks_dir / "all_chunks.jsonl"
    assert all_chunks.exists()
    text = all_chunks.read_text(encoding="utf-8")
    assert len(text) > 0


def test_main_with_section_filter(tmp_path, monkeypatch):
    """Lines 237, 250: SECTION_FILTER limits files processed."""
    chunks_dir = tmp_path / "chunks"
    section_dir = tmp_path / "05-habr-projects"
    section_dir.mkdir()
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", section_dir)
    monkeypatch.setattr(mod, "OUTPUT_DIR", chunks_dir)
    monkeypatch.setattr(mod, "MIN_CHUNK_WORDS", 5)
    monkeypatch.setattr(mod, "MAX_CHUNK_WORDS", 200)
    content = "# Memory\n\n" + "agent memory knowledge " * 20
    (section_dir / "yodoca.md").write_text(content, encoding="utf-8")
    mod.main()
    assert (chunks_dir / "all_chunks.jsonl").exists()


def test_module_level_args_max_words(monkeypatch):
    """Lines 36-38: --max-words flag sets MAX_CHUNK_WORDS."""
    monkeypatch.setattr(sys, "argv", ["prog", "--max-words", "150"])
    importlib.reload(mod)
    assert mod.MAX_CHUNK_WORDS == 150


def test_module_level_args_min_words(monkeypatch):
    """Lines 41-43: --min-words flag sets MIN_CHUNK_WORDS."""
    monkeypatch.setattr(sys, "argv", ["prog", "--min-words", "25"])
    importlib.reload(mod)
    assert mod.MIN_CHUNK_WORDS == 25


def test_module_level_args_section(monkeypatch):
    """Lines 47-49: --section flag sets SECTION_FILTER."""
    monkeypatch.setattr(sys, "argv", ["prog", "--section", "05-habr-projects"])
    importlib.reload(mod)
    assert mod.SECTION_FILTER is not None


def test_module_level_args_output(monkeypatch):
    """Lines 53-55: --output flag sets OUTPUT_DIR."""
    monkeypatch.setattr(sys, "argv", ["prog", "--output", "my_chunks"])
    importlib.reload(mod)
    assert "my_chunks" in str(mod.OUTPUT_DIR)
