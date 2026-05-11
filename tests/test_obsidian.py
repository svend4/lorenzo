"""Tests for scripts/improve_obsidian.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_obsidian")


def test_extract_title_returns_string(tmp_path):
    f = tmp_path / "test.md"
    result = mod._extract_title("# My Title\nContent here.", f)
    assert isinstance(result, str)


def test_extract_title_finds_h1(tmp_path):
    f = tmp_path / "test.md"
    result = mod._extract_title("# My Title\nContent here.", f)
    assert result == "My Title"


def test_extract_title_fallback_to_stem(tmp_path):
    f = tmp_path / "my-test-file.md"
    result = mod._extract_title("No heading here.", f)
    assert "My" in result or "my" in result.lower()


def test_extract_tags_returns_list():
    result = mod._extract_tags("<!-- tags: memory, agent, knowledge -->")
    assert isinstance(result, list)


def test_extract_tags_parses_tags():
    result = mod._extract_tags("<!-- tags: memory, agent, knowledge -->")
    assert "memory" in result
    assert "agent" in result
    assert "knowledge" in result


def test_extract_tags_empty_text():
    result = mod._extract_tags("no tags here")
    assert result == []


def test_make_frontmatter_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    result = mod._make_frontmatter("My Title", ["memory"], f)
    assert isinstance(result, str)


def test_make_frontmatter_has_title(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    result = mod._make_frontmatter("My Title", [], f)
    assert "My Title" in result


def test_make_frontmatter_has_tags(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    result = mod._make_frontmatter("Title", ["memory", "agent"], f)
    assert "memory" in result
    assert "agent" in result


def test_make_frontmatter_starts_with_dashes(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    result = mod._make_frontmatter("Title", [], f)
    assert result.startswith("---")


def test_convert_links_returns_string(tmp_path):
    f = tmp_path / "source.md"
    result = mod._convert_links("Some text here.", f)
    assert isinstance(result, str)


def test_convert_links_converts_md_links(tmp_path):
    target = tmp_path / "target.md"
    target.write_text("content")
    source = tmp_path / "source.md"
    result = mod._convert_links("[target](target.md)", source)
    assert "[[target]]" in result


def test_convert_links_leaves_non_md_links(tmp_path):
    f = tmp_path / "source.md"
    original = "[link](https://example.com)"
    result = mod._convert_links(original, f)
    assert original in result


def test_convert_links_with_label(tmp_path):
    target = tmp_path / "target.md"
    target.write_text("content")
    source = tmp_path / "source.md"
    result = mod._convert_links("[My Label](target.md)", source)
    assert "[[target|My Label]]" in result or "[[target]]" in result


def test_section_tag_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    section = tmp_path / "01-svyazi"
    section.mkdir()
    f = section / "file.md"
    result = mod._section_tag(f)
    assert isinstance(result, str)


def test_section_tag_strips_number_prefix(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    section = tmp_path / "01-svyazi"
    section.mkdir()
    f = section / "file.md"
    result = mod._section_tag(f)
    assert not result[0].isdigit()
