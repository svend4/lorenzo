"""Tests for scripts/improve_text_segmenter.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_text_segmenter")


def test_word_count_returns_int():
    result = mod._word_count("hello world test")
    assert isinstance(result, int)


def test_word_count_counts_words():
    result = mod._word_count("one two three four five")
    assert result == 5


def test_word_count_empty():
    result = mod._word_count("")
    assert result == 0


def test_extract_title_returns_string(tmp_path):
    f = tmp_path / "test.md"
    result = mod._extract_title("# My Title\nContent here.", f)
    assert isinstance(result, str)


def test_extract_title_finds_h1(tmp_path):
    f = tmp_path / "test.md"
    result = mod._extract_title("# My Title\nContent here.", f)
    assert result == "My Title"


def test_extract_title_fallback(tmp_path):
    f = tmp_path / "my-test-file.md"
    result = mod._extract_title("no heading", f)
    assert len(result) > 0


def test_split_into_segments_returns_list():
    text = "# Title\n\nContent here.\n\n## Section\n\nMore content.\n"
    result = mod._split_into_segments(text, target_size=100)
    assert isinstance(result, list)


def test_split_into_segments_has_content():
    text = "# Title\n\nSome content here.\n\n## Section A\n\nSection A content.\n\n## Section B\n\nSection B content.\n"
    result = mod._split_into_segments(text, target_size=50)
    assert len(result) >= 1


def test_split_into_segments_entry_keys():
    text = "## Section\n\nSome content goes here for testing purposes.\n"
    result = mod._split_into_segments(text, target_size=100)
    for seg in result:
        assert "heading" in seg
        assert "content" in seg
        assert "word_count" in seg


def test_split_into_segments_word_counts():
    text = "## Section\n\nSome content goes here for testing purposes.\n"
    result = mod._split_into_segments(text, target_size=100)
    for seg in result:
        assert isinstance(seg["word_count"], int)
        assert seg["word_count"] >= 0


def test_split_into_segments_no_headings():
    text = "First paragraph of content here.\n\n\nSecond paragraph of content here.\n"
    result = mod._split_into_segments(text, target_size=100)
    assert len(result) >= 1


def test_split_into_segments_respects_target():
    # With small target_size, should split into multiple segments
    text = "## Section\n\n" + ("word " * 100) + "\n\n## Other\n\n" + ("word " * 100)
    result = mod._split_into_segments(text, target_size=20)
    assert len(result) >= 2


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    mod.main()


def test_main_no_large_files_message(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    (tmp_path / "doc.md").write_text("# Title\n\nShort content.", encoding="utf-8")
    mod.main()
    out = capsys.readouterr().out
    assert "Нет файлов" in out or "Файлов" in out


def test_main_large_file_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "MAX_WORDS", 10)
    (tmp_path / "big.md").write_text(
        "# Title\n\n## Section\n\n" + "word " * 50 + "\n\n## Other\n\n" + "word " * 50,
        encoding="utf-8"
    )
    mod.main()


# ── module-level arg parsing ───────────────────────────────────────────────────

def test_max_words_arg_parsing():
    """Lines 37-39: --max-words N sets MAX_WORDS."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--max-words", "800"]
        importlib.reload(mod)
        assert mod.MAX_WORDS == 800
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_part_size_arg_parsing():
    """Lines 42-44: --part-size N sets PART_SIZE."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--part-size", "300"]
        importlib.reload(mod)
        assert mod.PART_SIZE == 300
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_section_arg_parsing():
    """Lines 48-50: --section NAME sets SECTION_FILTER."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "01-svyazi"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER is not None
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


# ── _split_into_segments edge cases ───────────────────────────────────────────

def test_split_no_headings_paragraph_split():
    """Lines 78-103: text with < 2 headings → split by paragraphs."""
    # No headings at all — splits by paragraphs
    text = ("word " * 20 + "\n\n\n") * 5  # 5 paragraphs, 20 words each
    result = mod._split_into_segments(text, target_size=30)
    assert isinstance(result, list)
    assert len(result) >= 1


def test_split_no_headings_single_large_para():
    """Lines 84-95: paragraph overflow → flush buffer."""
    # Make one large paragraph to trigger the flush
    text = ("word " * 50 + "\n\n\n") + ("word " * 50 + "\n\n\n")
    result = mod._split_into_segments(text, target_size=30)
    assert len(result) >= 2


def test_split_large_section_split_by_paragraphs():
    """Lines 131-161: heading path: section > target_size*1.5 → flush buffer then split."""
    # Need 2+ headings to enter heading path
    # Small section fills the buffer, then huge section triggers lines 131-161
    big_para = "word " * 50
    text = ("## Small\n\n" + "word " * 10 + "\n\n"
            "## Huge\n\n" + (big_para + "\n\n") * 4)
    result = mod._split_into_segments(text, target_size=40)
    # Buffer flushed for small, then huge split into multiple parts
    assert len(result) >= 2


def test_split_buffer_overflow_creates_new_segment():
    """Lines 163-172: buffer_words + sec word_count > target_size → flush."""
    # Two sections, each < target but combined > target
    text = ("## Section A\n\n" + "word " * 40 + "\n\n"
            "## Section B\n\n" + "word " * 40 + "\n\n"
            "## Section C\n\n" + "word " * 40)
    result = mod._split_into_segments(text, target_size=50)
    assert len(result) >= 2


# ── _write_parts ───────────────────────────────────────────────────────────────

def test_write_parts_creates_parts_dir(tmp_path):
    """Lines 191-229: _write_parts creates parts dir with index.md."""
    f = tmp_path / "doc.md"
    f.write_text("# Document\n\nContent here.", encoding="utf-8")
    segments = [
        {"heading": "Part One", "level": 2, "content": "Content one.", "word_count": 2},
        {"heading": "Part Two", "level": 2, "content": "Content two.", "word_count": 2},
    ]
    parts_dir = mod._write_parts(f, "Document", segments)
    assert parts_dir.exists()
    assert (parts_dir / "index.md").exists()
    assert (parts_dir / "part-01.md").exists()
    assert (parts_dir / "part-02.md").exists()


def test_write_parts_index_has_title(tmp_path):
    """_write_parts index.md contains title."""
    f = tmp_path / "doc.md"
    f.write_text("# Document\n\nContent.", encoding="utf-8")
    segments = [
        {"heading": "Section", "level": 2, "content": "Content.", "word_count": 1},
    ]
    parts_dir = mod._write_parts(f, "My Title", segments)
    index_text = (parts_dir / "index.md").read_text(encoding="utf-8")
    assert "My Title" in index_text


def test_write_parts_navigation_links(tmp_path):
    """Lines 218-221: navigation links added to parts."""
    f = tmp_path / "doc.md"
    f.write_text("# Doc\n\nContent.", encoding="utf-8")
    segments = [
        {"heading": "A", "level": 2, "content": "Content A.", "word_count": 2},
        {"heading": "B", "level": 2, "content": "Content B.", "word_count": 2},
        {"heading": "C", "level": 2, "content": "Content C.", "word_count": 2},
    ]
    parts_dir = mod._write_parts(f, "Doc", segments)
    p2 = (parts_dir / "part-02.md").read_text(encoding="utf-8")
    assert "part-03" in p2 or "part-01" in p2


# ── main: APPLY mode ───────────────────────────────────────────────────────────

def test_main_apply_creates_parts(tmp_path, monkeypatch):
    """Lines 274-276, 280: APPLY=True writes parts for large files."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", True)
    monkeypatch.setattr(mod, "MAX_WORDS", 10)
    monkeypatch.setattr(mod, "PART_SIZE", 20)
    (tmp_path / "big.md").write_text(
        "# Title\n\n## Section A\n\n" + "word " * 30 + "\n\n## Section B\n\n" + "word " * 30,
        encoding="utf-8"
    )
    mod.main()
    parts_dir = tmp_path / "big-parts"
    assert parts_dir.exists()


def test_main_read_exception_handled(tmp_path, monkeypatch):
    """Lines 248-249: exception reading file → continue."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "MAX_WORDS", 5)
    bad_file = tmp_path / "bad.md"
    bad_file.write_text("content", encoding="utf-8")

    from pathlib import Path as _Path
    original_read = _Path.read_text

    def mock_read(self, *args, **kwargs):
        if self == bad_file:
            raise OSError("mocked error")
        return original_read(self, *args, **kwargs)

    monkeypatch.setattr(_Path, "read_text", mock_read)
    mod.main()  # should not crash


# ── __main__ block ─────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 286: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    script_path = str(ROOT / "scripts" / "improve_text_segmenter.py")
    runpy.run_path(script_path, run_name="__main__")
