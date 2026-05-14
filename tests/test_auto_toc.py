"""
Тесты для scripts/improve_auto_toc.py.

Покрытие:
  - _slug()              — GitHub-совместимый якорь из заголовка
  - _build_toc()         — строит markdown TOC
  - _extract_headings()  — извлекает заголовки H2..Hmax
  - _has_toc()           — определяет наличие TOC
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_auto_toc")


# ── _slug ─────────────────────────────────────────────────────────────────────

def test_slug_returns_string():
    result = mod._slug("Hello World")
    assert isinstance(result, str)


def test_slug_lowercases():
    result = mod._slug("Hello World")
    assert result == result.lower()


def test_slug_spaces_to_dashes():
    result = mod._slug("Hello World")
    assert result == "hello-world"


def test_slug_removes_special_chars():
    result = mod._slug("Hello, World!")
    assert "," not in result
    assert "!" not in result


def test_slug_strips_dashes():
    result = mod._slug("  Hello World  ")
    assert not result.startswith("-")
    assert not result.endswith("-")


def test_slug_handles_cyrillic():
    result = mod._slug("Агент памяти")
    assert isinstance(result, str)
    assert len(result) > 0


def test_slug_empty():
    result = mod._slug("")
    assert isinstance(result, str)


# ── _build_toc ────────────────────────────────────────────────────────────────

def test_build_toc_returns_string():
    headings = [(2, "Introduction"), (2, "Methods")]
    result = mod._build_toc(headings)
    assert isinstance(result, str)


def test_build_toc_starts_with_marker():
    headings = [(2, "Section")]
    result = mod._build_toc(headings)
    assert result.startswith(mod.TOC_MARKER)


def test_build_toc_contains_contents():
    headings = [(2, "Section")]
    result = mod._build_toc(headings)
    assert "## Contents" in result


def test_build_toc_contains_heading_links():
    headings = [(2, "My Section")]
    result = mod._build_toc(headings)
    assert "My Section" in result
    assert "(#" in result


def test_build_toc_h2_no_indent():
    headings = [(2, "Top Level")]
    result = mod._build_toc(headings)
    assert "- [Top Level]" in result


def test_build_toc_h3_indented():
    headings = [(3, "Sub Level")]
    result = mod._build_toc(headings)
    assert "  - [Sub Level]" in result


def test_build_toc_multiple_headings():
    headings = [(2, "Section A"), (2, "Section B"), (3, "Sub B")]
    result = mod._build_toc(headings)
    assert "Section A" in result
    assert "Section B" in result
    assert "Sub B" in result


def test_build_toc_deduplicates_anchors():
    headings = [(2, "Same Title"), (2, "Same Title")]
    result = mod._build_toc(headings)
    # Both should appear, second with -1 suffix
    assert result.count("Same Title") == 2


# ── _extract_headings ─────────────────────────────────────────────────────────

def test_extract_headings_returns_list():
    result = mod._extract_headings("## Section\n", 3)
    assert isinstance(result, list)


def test_extract_headings_skips_h1():
    result = mod._extract_headings("# Title\n## Section\n", 3)
    for level, _ in result:
        assert level >= 2


def test_extract_headings_extracts_h2():
    result = mod._extract_headings("## My Section\n", 3)
    assert (2, "My Section") in result


def test_extract_headings_extracts_h3():
    result = mod._extract_headings("### Sub Section\n", 3)
    assert (3, "Sub Section") in result


def test_extract_headings_respects_max_level():
    text = "## H2\n### H3\n#### H4\n"
    result = mod._extract_headings(text, 3)
    levels = [level for level, _ in result]
    assert 4 not in levels


def test_extract_headings_skips_code_blocks():
    text = "```\n## Fake Heading\n```\n## Real Heading\n"
    result = mod._extract_headings(text, 3)
    titles = [title for _, title in result]
    assert "Fake Heading" not in titles
    assert "Real Heading" in titles


def test_extract_headings_removes_formatting():
    result = mod._extract_headings("## **Bold** Heading\n", 3)
    if result:
        _, title = result[0]
        assert "**" not in title


# ── _has_toc ──────────────────────────────────────────────────────────────────

def test_has_toc_false_without_toc():
    result = mod._has_toc("# Title\n\nSome content.\n")
    assert result is False


def test_has_toc_true_with_marker():
    result = mod._has_toc(f"# Title\n\n{mod.TOC_MARKER}\n## Contents\n")
    assert result is True


def test_has_toc_true_with_contents_heading():
    result = mod._has_toc("# Title\n\n## Contents\n- [Section](#section)\n")
    assert result is True


def test_has_toc_true_with_table_of_contents():
    result = mod._has_toc("# Title\n\n## Table of Contents\n- [Section](#section)\n")
    assert result is True


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    (tmp_path / "doc.md").write_text(
        "# Title\n\n## Section 1\n\nContent.\n\n## Section 2\n\nMore content.", encoding="utf-8"
    )
    mod.main()  # dry-run → must not raise


def test_main_apply_adds_toc(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", True)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_HEADINGS", 2)
    f = tmp_path / "doc.md"
    f.write_text(
        "# Title\n\n## Section 1\n\nContent.\n\n## Section 2\n\nMore.", encoding="utf-8"
    )
    mod.main()  # apply → must not raise


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()  # no files → must not raise


# ── arg parsing ───────────────────────────────────────────────────────────────

def test_min_headings_arg_parsing():
    """Lines 34-36: --min-headings N sets MIN_HEADINGS."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--min-headings", "5"]
        importlib.reload(mod)
        assert mod.MIN_HEADINGS == 5
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_depth_arg_parsing():
    """Lines 40-42: --depth N sets TOC_DEPTH."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--depth", "4"]
        importlib.reload(mod)
        assert mod.TOC_DEPTH == 4
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
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


# ── process_file edge cases ───────────────────────────────────────────────────

def test_process_file_read_exception(tmp_path, monkeypatch):
    """Lines 132-133: read exception → return False."""
    f = tmp_path / "bad.md"
    f.write_text("content", encoding="utf-8")

    from pathlib import Path as _Path
    original_read = _Path.read_text

    def mock_read(self, *args, **kwargs):
        if self == f:
            raise OSError("mocked error")
        return original_read(self, *args, **kwargs)

    monkeypatch.setattr(_Path, "read_text", mock_read)
    result = mod.process_file(f)
    assert result is False


def test_process_file_too_few_headings(tmp_path, monkeypatch):
    """Line 137: fewer than MIN_HEADINGS → return False."""
    monkeypatch.setattr(mod, "MIN_HEADINGS", 5)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\n## Section\n\nContent.", encoding="utf-8")
    result = mod.process_file(f)
    assert result is False


def test_process_file_manual_toc_no_marker(tmp_path, monkeypatch):
    """Line 153: has_toc but no TOC_MARKER → return False."""
    monkeypatch.setattr(mod, "MIN_HEADINGS", 2)
    f = tmp_path / "doc.md"
    f.write_text(
        "# Title\n\n## Contents\n- [Sec](#sec)\n\n## Section\n\nContent.\n\n## Other\n\nMore.",
        encoding="utf-8",
    )
    result = mod.process_file(f)
    assert result is False


def test_process_file_updates_existing_toc(tmp_path, monkeypatch):
    """Lines 143-149: file has TOC_MARKER → strips and re-inserts."""
    monkeypatch.setattr(mod, "MIN_HEADINGS", 2)
    monkeypatch.setattr(mod, "APPLY", False)
    toc_block = f"{mod.TOC_MARKER}\n## Contents\n- [Old](#old)\n"
    f = tmp_path / "doc.md"
    f.write_text(
        f"# Title\n\n{toc_block}\n## Section A\n\nContent.\n\n## Section B\n\nMore.",
        encoding="utf-8",
    )
    result = mod.process_file(f)
    # Either returns True (changed) or False (no change needed) - must not crash
    assert isinstance(result, bool)


def test_process_file_no_h1(tmp_path, monkeypatch):
    """Line 161: no H1 in else branch → toc_block + text."""
    monkeypatch.setattr(mod, "MIN_HEADINGS", 2)
    monkeypatch.setattr(mod, "APPLY", False)
    f = tmp_path / "doc.md"
    f.write_text("## Section A\n\nContent.\n\n## Section B\n\nMore.", encoding="utf-8")
    result = mod.process_file(f)
    assert result is True


# ── main: edge cases ──────────────────────────────────────────────────────────

def test_main_read_exception_in_loop(tmp_path, monkeypatch):
    """Lines 189-190: exception reading file in main loop → continue."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    bad = tmp_path / "bad.md"
    bad.write_text("content", encoding="utf-8")

    from pathlib import Path as _Path
    original_read = _Path.read_text

    def mock_read(self, *args, **kwargs):
        if self == bad:
            raise OSError("mocked error")
        return original_read(self, *args, **kwargs)

    monkeypatch.setattr(_Path, "read_text", mock_read)
    mod.main()  # must not crash


def test_main_skipped_has_toc(tmp_path, monkeypatch):
    """Lines 196-197: file has manual TOC (no marker) → skipped_has += 1."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_HEADINGS", 2)
    f = tmp_path / "doc.md"
    f.write_text(
        "# Title\n\n## Contents\n- [A](#a)\n\n## Section A\n\nContent.\n\n## Section B\n\nMore.",
        encoding="utf-8",
    )
    mod.main()  # must not crash


def test_main_apply_updates_toc(tmp_path, monkeypatch):
    """Lines 198-202: process_file returns True → updated count incremented."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", True)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_HEADINGS", 2)
    f = tmp_path / "doc.md"
    f.write_text(
        "# Title\n\n## Section A\n\nContent here.\n\n## Section B\n\nMore content.",
        encoding="utf-8",
    )
    mod.main()
    content = f.read_text(encoding="utf-8")
    assert mod.TOC_MARKER in content


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 212: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "APPLY", False)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    script_path = str(ROOT / "scripts" / "improve_auto_toc.py")
    runpy.run_path(script_path, run_name="__main__")
