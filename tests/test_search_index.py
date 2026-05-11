"""Tests for scripts/improve_search_index.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_search_index")


def test_extract_meta_returns_dict():
    result = mod.extract_meta("# Title\n\nSome content here.")
    assert isinstance(result, dict)


def test_extract_meta_has_required_keys():
    result = mod.extract_meta("# Title\n\nContent here.")
    assert "title" in result
    assert "summary" in result
    assert "tags" in result
    assert "projects" in result
    assert "words" in result
    assert "text_length" in result


def test_extract_meta_extracts_title():
    result = mod.extract_meta("# My Document Title\n\nContent here.")
    assert result["title"] == "My Document Title"


def test_extract_meta_no_title():
    result = mod.extract_meta("No heading here.\n\nJust content.")
    assert result["title"] == ""


def test_extract_meta_extracts_tags():
    text = "<!-- tags: python, memory, agent -->\n# Title"
    result = mod.extract_meta(text)
    assert "python" in result["tags"]
    assert "memory" in result["tags"]
    assert "agent" in result["tags"]


def test_extract_meta_no_tags():
    result = mod.extract_meta("# Title\n\nContent without tags.")
    assert result["tags"] == []


def test_extract_meta_extracts_summary():
    text = "# Title\n<!-- summary -->\n> This is the summary text\n\nContent."
    result = mod.extract_meta(text)
    assert "This is the summary text" in result["summary"]


def test_extract_meta_counts_words():
    text = "# Title\n\none two three four five"
    result = mod.extract_meta(text)
    assert result["words"] > 0


def test_extract_meta_extracts_projects():
    text = "**Проекты:** AgentFS, NGT Memory, Yodoca\n\nContent here."
    result = mod.extract_meta(text)
    assert "AgentFS" in result["projects"]


def test_build_index_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# Test Document\n\nThis is test content with enough words.", encoding="utf-8")
    result = mod.build_index()
    assert isinstance(result, list)


def test_build_index_skips_short_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "short.md").write_text("tiny", encoding="utf-8")
    result = mod.build_index()
    assert len(result) == 0


def test_build_index_includes_long_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    content = "# Test\n\n" + "This is a reasonably long document with lots of content. " * 5
    (tmp_path / "doc.md").write_text(content, encoding="utf-8")
    result = mod.build_index()
    assert len(result) == 1


def test_build_index_entry_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    content = "# Test\n\n" + "Content word " * 30
    (tmp_path / "doc.md").write_text(content, encoding="utf-8")
    result = mod.build_index()
    assert len(result) == 1
    assert "content" in result[0]
    assert "preview" in result[0]
    assert "path" in result[0]


def test_build_index_content_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    long_content = "# Title\n\n" + "word " * 2000
    (tmp_path / "doc.md").write_text(long_content, encoding="utf-8")
    result = mod.build_index()
    assert len(result[0]["content"]) <= 3000


def test_build_index_multiple_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    for i in range(3):
        (tmp_path / f"doc{i}.md").write_text(f"# Doc {i}\n\n" + "content word " * 20, encoding="utf-8")
    result = mod.build_index()
    assert len(result) == 3


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_search_index_json(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# Title\n\n" + "word " * 20, encoding="utf-8")
    mod.main()
    assert (tmp_path / "search_index.json").exists()


def test_main_creates_search_index_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# Title\n\n" + "word " * 20, encoding="utf-8")
    mod.main()
    assert (tmp_path / "SEARCH.md").exists()


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "search_index.json").exists()
