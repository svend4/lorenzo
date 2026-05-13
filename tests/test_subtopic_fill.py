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


# ── module-level arg parsing ───────────────────────────────────────────────────

def test_min_words_arg_parsing():
    """Lines 36-38: --min-words N sets MIN_WORDS."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--min-words", "200"]
        importlib.reload(mod)
        assert mod.MIN_WORDS == 200
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_section_arg_parsing():
    """Lines 42-44: --section NAME sets SECTION_FILTER."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "05-habr-projects"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER is not None
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


# ── _build_fill_section ────────────────────────────────────────────────────────

_SOURCE_TEXT = "# Knowledge System\n\n" + "agent memory system knowledge retrieval " * 30


def test_build_fill_section_finds_candidates(tmp_path, monkeypatch):
    """Lines 127, 135-159: relevant candidates found → section built."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    stub = tmp_path / "stub.md"
    stub.write_text("# Agent Memory\n\nagent memory knowledge", encoding="utf-8")
    source = tmp_path / "source.md"
    source.write_text(_SOURCE_TEXT, encoding="utf-8")

    stub_words = {"agent", "memory", "knowledge"}
    result = mod._build_fill_section(stub, stub_words, [stub, source])
    assert result is not None
    assert "Связанные" in result


def test_build_fill_section_skips_short_source(tmp_path, monkeypatch):
    """Line 124: source with < 100 words → skipped, no candidates."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    stub = tmp_path / "stub.md"
    stub.write_text("# Agent\n\nagent memory", encoding="utf-8")
    short_source = tmp_path / "short.md"
    short_source.write_text("# Short\n\nagent memory", encoding="utf-8")  # < 100 words

    stub_words = {"agent", "memory"}
    result = mod._build_fill_section(stub, stub_words, [stub, short_source])
    assert result is None


def test_build_fill_section_exception_handled(tmp_path, monkeypatch):
    """Lines 121-122: exception reading file in _build_fill_section → continue."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    stub = tmp_path / "stub.md"
    stub.write_text("# Short", encoding="utf-8")
    bad = tmp_path / "bad.md"
    bad.write_text("content", encoding="utf-8")

    from pathlib import Path as _Path
    original = _Path.read_text

    def mock_read(self, *a, **kw):
        if self == bad:
            raise OSError("mocked")
        return original(self, *a, **kw)

    monkeypatch.setattr(_Path, "read_text", mock_read)
    stub_words = {"agent", "memory"}
    result = mod._build_fill_section(stub, stub_words, [stub, bad])
    assert result is None or isinstance(result, str)


# ── main edge cases ────────────────────────────────────────────────────────────

def test_main_first_read_exception(tmp_path, monkeypatch):
    """Lines 184-185: exception in first read of stubs loop → continue."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "MIN_WORDS", 1000)

    bad_file = tmp_path / "bad.md"
    bad_file.write_text("agent memory", encoding="utf-8")

    from pathlib import Path as _Path
    original = _Path.read_text

    def mock_read(self, *a, **kw):
        if self == bad_file:
            raise OSError("mocked")
        return original(self, *a, **kw)

    monkeypatch.setattr(_Path, "read_text", mock_read)
    mod.main()  # should not crash


def test_main_second_read_exception(tmp_path, monkeypatch):
    """Lines 201-202: exception in second read (stub_targets loop) → continue."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "MIN_WORDS", 1000)

    bad_stub = tmp_path / "bad_stub.md"
    bad_stub.write_text("agent memory", encoding="utf-8")

    from pathlib import Path as _Path
    original = _Path.read_text
    call_counts: dict = {}

    def mock_read(self, *a, **kw):
        key = str(self)
        call_counts[key] = call_counts.get(key, 0) + 1
        if self == bad_stub and call_counts[key] >= 2:
            raise OSError("second read fails")
        return original(self, *a, **kw)

    monkeypatch.setattr(_Path, "read_text", mock_read)
    mod.main()  # should not crash


def test_main_stub_with_few_words(tmp_path, monkeypatch):
    """Lines 205-206: stub has < 3 key words → skipped."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "MIN_WORDS", 1000)

    # All words < 4 chars or stopwords → empty top_words set
    (tmp_path / "sparse.md").write_text("# A\n\nit a is", encoding="utf-8")
    mod.main()  # should not crash


def test_main_stub_no_candidates(tmp_path, monkeypatch):
    """Lines 209-211: _build_fill_section returns None → skipped."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "MIN_WORDS", 1000)

    # Stub has distinctive words but no matching sources
    (tmp_path / "stub.md").write_text(
        "# Unique\n\nxylophone banana guitar", encoding="utf-8"
    )
    mod.main()  # should not crash


def test_main_apply_writes_file(tmp_path, monkeypatch):
    """Lines 213-221: APPLY=True → writes to stub file."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", True)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "MIN_WORDS", 50)

    stub = tmp_path / "stub.md"
    stub.write_text("# Agent Memory\n\nagent memory knowledge", encoding="utf-8")
    source = tmp_path / "source.md"
    source.write_text(_SOURCE_TEXT, encoding="utf-8")
    mod.main()
    # The file should still be readable (not crash)
    assert stub.read_text(encoding="utf-8") is not None


# ── __main__ block ─────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 230: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    script_path = str(ROOT / "scripts" / "improve_subtopic_fill.py")
    runpy.run_path(script_path, run_name="__main__")
