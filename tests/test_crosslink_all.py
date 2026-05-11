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
