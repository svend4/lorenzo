"""Tests for scripts/improve_crosslink_all.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_crosslink_all")


def test_extract_md_links_returns_set(tmp_path):
    f = tmp_path / "source.md"
    target = tmp_path / "target.md"
    target.write_text("# Target", encoding="utf-8")
    result = mod._extract_md_links("[link](target.md)", f)
    assert isinstance(result, set)


def test_extract_md_links_finds_link(tmp_path):
    target = tmp_path / "target.md"
    target.write_text("# Target", encoding="utf-8")
    source = tmp_path / "source.md"
    result = mod._extract_md_links("[link](target.md)", source)
    assert target.resolve() in result


def test_extract_md_links_ignores_http():
    source = Path("/some/dir/source.md")
    result = mod._extract_md_links("[link](https://github.com/user/repo)", source)
    assert len(result) == 0


def test_extract_md_links_strips_anchor(tmp_path):
    target = tmp_path / "target.md"
    target.write_text("# Target", encoding="utf-8")
    source = tmp_path / "source.md"
    result = mod._extract_md_links("[link](target.md#section)", source)
    assert target.resolve() in result


def test_top_words_returns_set():
    result = mod._top_words("agent memory retrieval knowledge system data agent memory" * 3)
    assert isinstance(result, set)


def test_top_words_respects_n():
    result = mod._top_words("agent memory retrieval knowledge system data agent" * 3, n=3)
    assert len(result) <= 3


def test_top_words_filters_short():
    result = mod._top_words("the for and but agent memory")
    # Short words should be filtered (< 4 chars)
    assert all(len(w) >= 4 for w in result)


def test_title_returns_string(tmp_path):
    f = tmp_path / "test.md"
    result = mod._title(f, "# My Title\n\nContent.")
    assert isinstance(result, str)


def test_title_extracts_h1(tmp_path):
    f = tmp_path / "test.md"
    result = mod._title(f, "# My Document Title\n\nContent.")
    assert result == "My Document Title"


def test_title_fallback_to_stem(tmp_path):
    f = tmp_path / "my-document.md"
    result = mod._title(f, "No heading here.")
    assert "My Document" in result or "my-document" in result.lower()


def test_word_count_returns_int():
    result = mod._word_count("one two three")
    assert isinstance(result, int)
    assert result == 3


def test_update_or_append_appends_new():
    marker = "<!-- backlinks-auto -->"
    text = "# Title\n\nContent."
    new_block = f"\n{marker}\n## Links\n"
    result = mod._update_or_append(text, marker, new_block)
    assert marker in result


def test_update_or_append_updates_existing():
    marker = "<!-- backlinks-auto -->"
    # The pattern replaces from marker to (but not including) next ##
    # So put the old content after the marker, before the next ##
    text = f"# Title\n\nContent.\n{marker}\nOld content text here\n\n## Next Section\n"
    new_block = f"{marker}\nNew content here"
    result = mod._update_or_append(text, marker, new_block)
    assert "New content" in result
    assert marker in result


def test_build_backlink_block_returns_string(tmp_path):
    f = tmp_path / "source.md"
    backlinks = [(f, "Source Title")]
    result = mod._build_backlink_block(backlinks, tmp_path)
    assert isinstance(result, str)
    assert "Упоминается" in result


def test_build_related_block_returns_string(tmp_path):
    f = tmp_path / "related.md"
    related = [(f, "Related Title", 0.75)]
    result = mod._build_related_block(related, tmp_path)
    assert isinstance(result, str)
    assert "Связанные" in result


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    mod.main()  # dry-run → must not raise


def test_main_dry_run_with_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    (tmp_path / "a.md").write_text("# AgentFS\n\nMemory and agent systems.", encoding="utf-8")
    (tmp_path / "b.md").write_text("# Yodoca\n\nMemory consolidation agent.", encoding="utf-8")
    mod.main()  # must not raise


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    mod.main()  # must not raise


# ── module-level arg parsing (requires reload) ────────────────────────────────

def test_min_refs_arg_parsing():
    """Lines 40-42: --min-refs N sets MIN_REFS."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--min-refs", "3"]
        importlib.reload(mod)
        assert mod.MIN_REFS == 3
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_section_arg_parsing():
    """Lines 46-48: --section NAME sets SECTION_FILTER."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "01-svyazi"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER is not None
        assert "01-svyazi" in str(mod.SECTION_FILTER)
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


# ── _extract_md_links exception handler ──────────────────────────────────────

def test_extract_md_links_exception_handled(tmp_path, monkeypatch):
    """Lines 76-77: exception during path resolution → path silently skipped."""
    original_resolve = Path.resolve

    def mock_resolve(self, strict=False):
        if "badlink" in str(self):
            raise OSError("mocked resolve error")
        return original_resolve(self, strict=strict)

    monkeypatch.setattr(Path, "resolve", mock_resolve)
    source = tmp_path / "source.md"
    result = mod._extract_md_links("[Bad](badlink.md)", source)
    assert isinstance(result, set)
    assert len(result) == 0


# ── main with file-read exception ─────────────────────────────────────────────

def test_main_file_read_exception_handled(tmp_path, monkeypatch):
    """Lines 162-163: exception reading file → texts[f] = ''."""
    bad_file = tmp_path / "bad.md"
    bad_file.write_text("content here", encoding="utf-8")

    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "KEYWORDS", False)

    original_read = Path.read_text

    def mock_read(self, *args, **kwargs):
        if self == bad_file:
            raise OSError("mocked error")
        return original_read(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", mock_read)
    mod.main()  # should not crash


# ── main with actual backlinks (lines 176, 198-232, 240-244) ─────────────────

_LONG = "# Doc\n\n" + "word " * 25


def test_main_with_backlinked_files(tmp_path, monkeypatch):
    """Lines 176, 198-232: file B links to A → A gets backlink block."""
    file_a = tmp_path / "target.md"
    file_a.write_text(_LONG, encoding="utf-8")
    file_b = tmp_path / "source.md"
    file_b.write_text(_LONG + "\n\n[Target](target.md)", encoding="utf-8")

    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "KEYWORDS", False)
    monkeypatch.setattr(mod, "MIN_REFS", 1)
    mod.main()


def test_main_apply_writes_backlinks(tmp_path, monkeypatch):
    """Line 232: APPLY=True writes modified file to disk."""
    file_a = tmp_path / "target.md"
    file_a.write_text(_LONG, encoding="utf-8")
    file_b = tmp_path / "source.md"
    file_b.write_text(_LONG + "\n\n[Target](target.md)", encoding="utf-8")

    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", True)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "KEYWORDS", False)
    monkeypatch.setattr(mod, "MIN_REFS", 1)
    mod.main()
    content = file_a.read_text(encoding="utf-8")
    assert mod.BACKLINK_MARKER in content


def test_main_top_cited_stats(tmp_path, monkeypatch):
    """Lines 240-244: top-cited stats printed when backlinks exist."""
    target = tmp_path / "popular.md"
    target.write_text(_LONG, encoding="utf-8")
    for i in range(3):
        src = tmp_path / f"source{i}.md"
        src.write_text(_LONG + "\n\n[Popular](popular.md)", encoding="utf-8")

    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "KEYWORDS", False)
    monkeypatch.setattr(mod, "MIN_REFS", 1)
    mod.main()


# ── main KEYWORDS mode ────────────────────────────────────────────────────────

def test_main_keywords_mode(tmp_path, monkeypatch):
    """Lines 143, 181-184, 204-211: KEYWORDS=True runs keyword computation."""
    kw_text = "agent memory retrieval knowledge system architecture " * 5
    (tmp_path / "doc_a.md").write_text("# Doc A\n\n" + kw_text, encoding="utf-8")
    (tmp_path / "doc_b.md").write_text("# Doc B\n\n" + kw_text, encoding="utf-8")

    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "KEYWORDS", True)
    monkeypatch.setattr(mod, "MIN_REFS", 1)
    mod.main()


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 251: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "KEYWORDS", False)
    script_path = str(ROOT / "scripts" / "improve_crosslink_all.py")
    runpy.run_path(script_path, run_name="__main__")
