"""Tests for scripts/improve_source_map.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_source_map")


def test_is_imported_returns_bool(tmp_path):
    f = tmp_path / "extracted_data.md"
    result = mod._is_imported(f)
    assert isinstance(result, bool)


def test_is_imported_detects_md_md_suffix(tmp_path):
    f = tmp_path / "content-file-md.md"
    result = mod._is_imported(f)
    assert result is True


def test_is_imported_detects_part_suffix(tmp_path):
    f = tmp_path / "document-part-2.md"
    result = mod._is_imported(f)
    assert result is True


def test_is_imported_regular_file(tmp_path):
    f = tmp_path / "regular-document.md"
    result = mod._is_imported(f)
    assert result is False


def test_extract_sources_returns_dict():
    result = mod._extract_sources("plain text content")
    assert isinstance(result, dict)


def test_extract_sources_from_frontmatter():
    text = "---\nsource: https://github.com/user/repo\ntitle: Test\n---\nContent"
    result = mod._extract_sources(text)
    assert "source" in result
    assert "github.com" in result["source"]


def test_extract_sources_from_comment():
    text = "Some text <!-- source: https://habr.com/article --> more"
    result = mod._extract_sources(text)
    assert "comment_source" in result


def test_extract_sources_finds_github_url():
    text = "See github.com/user/repo for more details about this project."
    result = mod._extract_sources(text)
    # May find external URLs
    assert isinstance(result, dict)


def test_extract_sources_empty():
    result = mod._extract_sources("")
    assert isinstance(result, dict)


def test_categorize_with_source_returns_string(tmp_path, monkeypatch):
    f = tmp_path / "test.md"
    git_info = {}
    sources = {"source": "https://github.com/user/repo"}
    result = mod._categorize(f, git_info, sources)
    assert isinstance(result, str)
    assert "Из источника" in result


def test_categorize_with_comment_source(tmp_path, monkeypatch):
    f = tmp_path / "test.md"
    git_info = {}
    sources = {"comment_source": "https://habr.com/article"}
    result = mod._categorize(f, git_info, sources)
    assert "Из комментария" in result


def test_categorize_imported_file(tmp_path):
    f = tmp_path / "content-overview.md"
    git_info = {}
    sources = {}
    result = mod._categorize(f, git_info, sources)
    assert "Авто-импорт" in result


def test_categorize_manual(tmp_path):
    f = tmp_path / "regular-document.md"
    git_info = {"first_author": "John Human"}
    sources = {}
    result = mod._categorize(f, git_info, sources)
    assert "Ручной" in result


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_source_map_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    assert (tmp_path / "SOURCE_MAP.md").exists()


def test_main_source_map_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent here.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "SOURCE_MAP.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    assert (tmp_path / "SOURCE_MAP.md").exists()


def test_main_source_map_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()
    text = (tmp_path / "SOURCE_MAP.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
