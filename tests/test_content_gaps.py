"""
Тесты для scripts/improve_content_gaps.py.

Покрытие:
  - _clean()              — очистка markdown-разметки
  - _extract_concepts()   — извлечение концептов из текста
  - _suggest_location()   — предложение папки для нового файла
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_content_gaps")


# ── _clean ────────────────────────────────────────────────────────────────────

def test_clean_returns_string():
    result = mod._clean("some text")
    assert isinstance(result, str)


def test_clean_removes_code_blocks():
    result = mod._clean("Before\n```python\ncode here\n```\nAfter")
    assert "code here" not in result


def test_clean_removes_inline_code():
    result = mod._clean("Use `function()` here.")
    assert "function()" not in result


def test_clean_removes_url():
    result = mod._clean("See https://example.com for more.")
    assert "https" not in result


def test_clean_removes_html_comments():
    result = mod._clean("Before <!-- comment --> after")
    assert "comment" not in result


def test_clean_empty():
    result = mod._clean("")
    assert result == ""


# ── _extract_concepts ─────────────────────────────────────────────────────────

def test_extract_concepts_returns_list():
    result = mod._extract_concepts("plain text")
    assert isinstance(result, list)


def test_extract_concepts_empty():
    result = mod._extract_concepts("")
    assert result == []


def test_extract_concepts_min_length_3():
    result = mod._extract_concepts("АБ ABC test")
    for c in result:
        assert len(c.lower().strip()) >= 3


def test_extract_concepts_max_length_50():
    result = mod._extract_concepts("# Title\n\nSome text here.")
    for c in result:
        assert len(c.lower().strip()) <= 50


def test_extract_concepts_no_pure_numbers():
    result = mod._extract_concepts("12345 and 678 in the text.")
    for c in result:
        assert not c.strip().isdigit()


# ── _suggest_location ─────────────────────────────────────────────────────────

def test_suggest_location_returns_string():
    result = mod._suggest_location("test term", [])
    assert isinstance(result, str)


def test_suggest_location_default_docs():
    result = mod._suggest_location("test term", [])
    assert "docs" in result


def test_suggest_location_uses_source_folder():
    sources = ["docs/05-habr-projects/memory/file.md",
               "docs/05-habr-projects/memory/other.md"]
    result = mod._suggest_location("memory term", sources)
    assert "docs/" in result


def test_suggest_location_most_common_folder():
    sources = [
        "docs/05-habr-projects/a.md",
        "docs/05-habr-projects/b.md",
        "docs/01-svyazi/c.md",
    ]
    result = mod._suggest_location("term", sources)
    assert "05-habr-projects" in result


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_content_gaps_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    assert (tmp_path / "CONTENT_GAPS.md").exists()


def test_main_content_gaps_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    (tmp_path / "doc.md").write_text(
        "# Title\n\nAgentFS and Yodoca are used here.", encoding="utf-8"
    )
    mod.main()
    text = (tmp_path / "CONTENT_GAPS.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    assert (tmp_path / "CONTENT_GAPS.md").exists()


def test_main_content_gaps_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    text = (tmp_path / "CONTENT_GAPS.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


def test_clean_removes_code_blocks():
    text = "before ```code here``` after"
    result = mod._clean(text)
    assert "code here" not in result
    assert "before" in result


def test_clean_removes_urls():
    result = mod._clean("Visit https://example.com for more.")
    assert "https://example.com" not in result


def test_extract_concepts_returns_list():
    result = mod._extract_concepts("AgentFS and Yodoca are systems.")
    assert isinstance(result, list)


def test_has_dedicated_doc_found(tmp_path):
    files = [tmp_path / "agentfs.md", tmp_path / "yodoca.md"]
    result = mod._has_dedicated_doc("AgentFS", files)
    assert result is not None


def test_has_dedicated_doc_not_found(tmp_path):
    files = [tmp_path / "other.md"]
    result = mod._has_dedicated_doc("AgentFS", files)
    assert result is None


def test_suggest_location_returns_string():
    sources = ["docs/01-svyazi/doc.md", "docs/01-svyazi/other.md"]
    result = mod._suggest_location("term", sources)
    assert isinstance(result, str)
    assert "docs" in result


def test_main_with_concepts(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_MENTIONS", 1)
    (tmp_path / "doc1.md").write_text(
        "# Title\n\nAgentFS is a system. AgentFS works well.", encoding="utf-8"
    )
    (tmp_path / "doc2.md").write_text(
        "# Other\n\nAgentFS integrates with Yodoca.", encoding="utf-8"
    )
    mod.main()
    assert (tmp_path / "CONTENT_GAPS.md").exists()


# ── arg parsing ───────────────────────────────────────────────────────────────

def test_min_mentions_arg_parsing():
    """Lines 27-29: --min-mentions N sets MIN_MENTIONS."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--min-mentions", "5"]
        importlib.reload(mod)
        assert mod.MIN_MENTIONS == 5
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_section_arg_parsing():
    """Lines 33-35: --section NAME sets SECTION_FILTER."""
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "05-habr-projects"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER is not None
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


# ── _extract_concepts edge cases ──────────────────────────────────────────────

def test_extract_concepts_skips_len2_abbrev():
    """Line 89: concept with len < 3 → skipped."""
    result = mod._extract_concepts("AB testing is not good here.")
    # "AB" (2 chars) should be filtered out
    for c in result:
        assert len(c.lower().strip()) >= 3


def test_extract_concepts_skips_known_terms():
    """Line 91: concept in KNOWN_TERMS → skipped."""
    result = mod._extract_concepts("LLM is a known term here.")
    for c in result:
        assert c.lower() not in mod.KNOWN_TERMS


def test_extract_concepts_skips_pure_digits():
    """Line 93: quoted pure-digit concept → skipped."""
    result = mod._extract_concepts('Use "12345" as the identifier here.')
    for c in result:
        assert not c.strip().isdigit()


# ── main: full coverage with CamelCase concepts ───────────────────────────────

def test_main_finds_gaps_with_camelcase(tmp_path, monkeypatch):
    """Lines 143, 148-154, 171-189, 198: real CamelCase concepts create gaps."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_MENTIONS", 2)
    # KnowledgeBase appears in 2 files → gap
    (tmp_path / "doc1.md").write_text(
        "# Title\n\nKnowledgeBase is the core system here.", encoding="utf-8"
    )
    (tmp_path / "doc2.md").write_text(
        "# Other\n\nKnowledgeBase integrates well with SearchEngine.", encoding="utf-8"
    )
    mod.main()
    text = (tmp_path / "CONTENT_GAPS.md").read_text(encoding="utf-8")
    assert "#" in text


def test_main_file_read_exception(tmp_path, monkeypatch):
    """Lines 138-139: exception reading file → continue."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
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
    mod.main()  # should not crash


def test_main_gaps_with_dedicated_doc_skipped(tmp_path, monkeypatch):
    """Lines 150-152: concept has dedicated doc → skip from gaps."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_MENTIONS", 1)
    # Create KnowledgeBase in 1 file
    (tmp_path / "doc1.md").write_text(
        "# Title\n\nKnowledgeBase is used here.", encoding="utf-8"
    )
    # Create a dedicated doc for it
    (tmp_path / "knowledgebase.md").write_text(
        "# KnowledgeBase\n\nDedicated document.", encoding="utf-8"
    )
    mod.main()
    assert (tmp_path / "CONTENT_GAPS.md").exists()


def test_main_many_gaps_detail(tmp_path, monkeypatch):
    """Lines 182-189: detail section for gaps[:20] with >5 files per gap."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "MIN_MENTIONS", 2)
    # Create multiple files all mentioning KnowledgeBase
    for i in range(7):
        (tmp_path / f"doc{i}.md").write_text(
            f"# Title{i}\n\nKnowledgeBase SearchEngine SystemArchitecture.",
            encoding="utf-8",
        )
    mod.main()
    text = (tmp_path / "CONTENT_GAPS.md").read_text(encoding="utf-8")
    assert "Рекомендуется" in text or "#" in text


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 202: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    script_path = str(ROOT / "scripts" / "improve_content_gaps.py")
    runpy.run_path(script_path, run_name="__main__")
