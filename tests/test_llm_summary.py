"""Tests for scripts/improve_llm_summary.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_llm_summary")


def test_map_prompt_constant():
    assert hasattr(mod, "MAP_PROMPT")
    assert isinstance(mod.MAP_PROMPT, str)
    assert "{chunk}" in mod.MAP_PROMPT


def test_reduce_prompt_constant():
    assert hasattr(mod, "REDUCE_PROMPT")
    assert isinstance(mod.REDUCE_PROMPT, str)
    assert "{title}" in mod.REDUCE_PROMPT
    assert "{summaries}" in mod.REDUCE_PROMPT


def test_min_words_constant():
    assert hasattr(mod, "MIN_WORDS")
    assert isinstance(mod.MIN_WORDS, int)
    assert mod.MIN_WORDS > 0


def test_dry_run_attribute():
    assert hasattr(mod, "DRY_RUN")
    assert isinstance(mod.DRY_RUN, bool)


def test_today_attribute():
    assert hasattr(mod, "TODAY")
    assert isinstance(mod.TODAY, str)
    assert len(mod.TODAY) == 10


def test_model_attribute():
    assert hasattr(mod, "MODEL")
    assert isinstance(mod.MODEL, str)
    assert "claude" in mod.MODEL.lower()


def test_docs_path_attribute():
    assert hasattr(mod, "DOCS")
    assert isinstance(mod.DOCS, Path)


def test_map_prompt_has_instructions():
    # Should instruct about summarization
    assert "суммари" in mod.MAP_PROMPT.lower() or "summary" in mod.MAP_PROMPT.lower() or "кратко" in mod.MAP_PROMPT.lower()


def test_reduce_prompt_has_format():
    # Should have format instructions
    assert "Markdown" in mod.REDUCE_PROMPT or "markdown" in mod.REDUCE_PROMPT.lower()


def test_min_words_reasonable():
    # Should be between 100 and 1000
    assert 100 <= mod.MIN_WORDS <= 1000


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "DIGEST_PATH", tmp_path / "DIGEST.md")
    mod.main()


def test_main_dry_run_with_file(tmp_path, monkeypatch):
    doc = tmp_path / "doc.md"
    doc.write_text("# AgentFS\n\n" + "Content. " * 30, encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "DIGEST_PATH", tmp_path / "DIGEST.md")
    mod.main()


def test_collect_targets_empty_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    result = mod.collect_targets()
    assert isinstance(result, list)


def test_collect_targets_with_file_filter(tmp_path, monkeypatch):
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\n" + "word " * 300, encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "FILE_FILTER", f)
    result = mod.collect_targets()
    assert f in result


def test_collect_targets_file_filter_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "FILE_FILTER", tmp_path / "nonexistent.md")
    result = mod.collect_targets()
    assert result == []


def test_load_digest_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DIGEST_PATH", tmp_path / "nonexistent.md")
    result = mod.load_digest()
    assert result == {}


def test_load_digest_with_existing(tmp_path, monkeypatch):
    digest = tmp_path / "DIGEST.md"
    digest.write_text(
        "## Title\n_Файл: [doc.md](doc.md)_\n\nContent.\n",
        encoding="utf-8"
    )
    monkeypatch.setattr(mod, "DIGEST_PATH", digest)
    result = mod.load_digest()
    assert "doc.md" in result


def test_append_to_digest_creates_file(tmp_path, monkeypatch):
    digest = tmp_path / "DIGEST.md"
    monkeypatch.setattr(mod, "DIGEST_PATH", digest)
    mod.append_to_digest("## New Section\n\nContent.\n")
    assert digest.exists()
    assert "New Section" in digest.read_text(encoding="utf-8")


# ── arg parsing ───────────────────────────────────────────────────────────────

def test_section_arg_parsing():
    """Lines 37-39: --section NAME sets SECTION_FILTER."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "05-habr-projects"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER is not None
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_file_arg_parsing():
    """Lines 43-45: --file PATH sets FILE_FILTER."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--file", "docs/test.md"]
        importlib.reload(mod)
        assert mod.FILE_FILTER is not None
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


# ── summarize_chunks ──────────────────────────────────────────────────────────

def test_summarize_chunks_single_chunk():
    """Lines 89-96: single chunk → direct summarize."""
    class MockContent:
        text = "Summary of the document chunk content."
    class MockResp:
        content = [MockContent()]
    class MockMessages:
        def create(self, **kwargs):
            return MockResp()
    class MockClient:
        messages = MockMessages()

    result = mod.summarize_chunks(["chunk text content here"], MockClient(), "Test Title")
    assert isinstance(result, str)
    assert result == "Summary of the document chunk content."


def test_summarize_chunks_multiple_chunks():
    """Lines 99-117: multiple chunks → map-reduce."""
    class MockContent:
        text = "Mini summary."
    class MockResp:
        content = [MockContent()]
    call_count = [0]
    class MockMessages:
        def create(self, **kwargs):
            call_count[0] += 1
            return MockResp()
    class MockClient:
        messages = MockMessages()

    result = mod.summarize_chunks(["chunk1 content", "chunk2 content"], MockClient(), "Test Title")
    assert isinstance(result, str)
    assert call_count[0] == 3  # 2 map + 1 reduce


# ── main: dry-run with targets ────────────────────────────────────────────────

def test_main_dry_run_with_many_targets(tmp_path, monkeypatch):
    """Lines 209-213: dry-run with new_targets → prints file info."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 1)
    monkeypatch.setattr(mod, "DIGEST_PATH", tmp_path / "DIGEST.md")
    for i in range(3):
        (tmp_path / f"doc{i}.md").write_text(f"# Doc {i}\n\n" + "word " * 5, encoding="utf-8")
    mod.main()


def test_main_dry_run_more_than_20_targets(tmp_path, monkeypatch):
    """Lines 186, 215: dry-run with > 20 new_targets → truncation message."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 1)
    monkeypatch.setattr(mod, "DIGEST_PATH", tmp_path / "DIGEST.md")
    for i in range(22):
        (tmp_path / f"doc{i:02d}.md").write_text(f"# Doc {i}\n\nword\n", encoding="utf-8")
    mod.main()  # prints "... и ещё N файлов"


# ── main: non-dry-run with mock anthropic ─────────────────────────────────────

def test_main_apply_with_mock_anthropic(tmp_path, monkeypatch):
    """Lines 220-256: non-dry-run uses mock anthropic."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 1)
    monkeypatch.setattr(mod, "DIGEST_PATH", tmp_path / "DIGEST.md")
    (tmp_path / "doc.md").write_text("# Test Doc\n\nContent here.\n", encoding="utf-8")

    class MockContent:
        text = "Summary text."
    class MockResp:
        content = [MockContent()]
    class MockMessages:
        def create(self, **kwargs):
            return MockResp()
    class MockAnthropicInstance:
        messages = MockMessages()
    class MockAnthropicModule:
        def Anthropic(self):
            return MockAnthropicInstance()

    monkeypatch.setitem(sys.modules, "anthropic", MockAnthropicModule())
    mod.main()  # should not crash


def test_main_apply_anthropic_not_installed(tmp_path, monkeypatch):
    """Lines 222-224: anthropic not importable → sys.exit(1)."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 1)
    monkeypatch.setattr(mod, "DIGEST_PATH", tmp_path / "DIGEST.md")
    (tmp_path / "doc.md").write_text("# Test\n\nword\n", encoding="utf-8")
    saved = sys.modules.pop("anthropic", None)
    try:
        with pytest.raises(SystemExit):
            mod.main()
    finally:
        if saved is not None:
            sys.modules["anthropic"] = saved


def test_main_apply_summarize_exception_handled(tmp_path, monkeypatch):
    """Lines 253-254: summarize_chunks raises → exception caught."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "MIN_WORDS", 1)
    monkeypatch.setattr(mod, "DIGEST_PATH", tmp_path / "DIGEST.md")
    (tmp_path / "doc.md").write_text("# Test\n\nword\n", encoding="utf-8")

    class MockMessages:
        def create(self, **kwargs):
            raise RuntimeError("API error")
    class MockAnthropicInstance:
        messages = MockMessages()
    class MockAnthropicModule:
        def Anthropic(self):
            return MockAnthropicInstance()

    monkeypatch.setitem(sys.modules, "anthropic", MockAnthropicModule())
    mod.main()  # exception caught, should not crash


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 260: __main__ block."""
    import runpy
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--dry-run"]
        script_path = str(ROOT / "scripts" / "improve_llm_summary.py")
        runpy.run_path(script_path, run_name="__main__")
    finally:
        sys.argv = orig_argv
