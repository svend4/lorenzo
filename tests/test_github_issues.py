"""Tests for scripts/improve_github_issues.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_github_issues")


def test_todo_patterns_is_list():
    assert hasattr(mod, "TODO_PATTERNS")
    assert isinstance(mod.TODO_PATTERNS, list)
    assert len(mod.TODO_PATTERNS) > 0


def test_priority_files_is_list():
    assert hasattr(mod, "PRIORITY_FILES")
    assert isinstance(mod.PRIORITY_FILES, list)


def test_extract_issues_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Plan\n\n- [ ] Fix the memory system\n- [ ] Add better indexing\n", encoding="utf-8")
    result = mod._extract_issues(f)
    assert isinstance(result, list)


def test_extract_issues_finds_checkbox_todos(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Plan\n\n- [ ] Fix the memory system module\n", encoding="utf-8")
    result = mod._extract_issues(f)
    assert len(result) >= 1
    titles = [r["title"] for r in result]
    assert any("memory system" in t for t in titles)


def test_extract_issues_finds_todo_keyword(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Plan\n\nTODO: Implement better retrieval system here\n", encoding="utf-8")
    result = mod._extract_issues(f)
    assert len(result) >= 1


def test_extract_issues_finds_fixme_keyword(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Plan\n\nFIXME: broken link in documentation system\n", encoding="utf-8")
    result = mod._extract_issues(f)
    assert len(result) >= 1


def test_extract_issues_deduplicates(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text(
        "# Plan\n\n- [ ] Fix the memory system module\n- [ ] Fix the memory system module\n",
        encoding="utf-8"
    )
    result = mod._extract_issues(f)
    titles = [r["title"] for r in result]
    assert len(titles) == len(set(titles))


def test_extract_issues_has_required_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Plan\n\n- [ ] Fix the memory system module\n", encoding="utf-8")
    result = mod._extract_issues(f)
    for item in result:
        assert "title" in item
        assert "source" in item
        assert "labels" in item


def test_extract_issues_empty_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "empty.md"
    f.write_text("# Title\n\nThis file has no tasks or action items.\n", encoding="utf-8")
    result = mod._extract_issues(f)
    assert result == []


def test_extract_issues_missing_file(tmp_path):
    result = mod._extract_issues(tmp_path / "missing.md")
    assert result == []


def test_extract_issues_skips_short_titles(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Plan\n\n- [ ] Too short\n", encoding="utf-8")
    result = mod._extract_issues(f)
    titles = [r["title"] for r in result]
    assert not any(t == "Too short" for t in titles)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_github_issues_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "CREATE", False)
    mod.main()
    assert (tmp_path / "GITHUB_ISSUES.md").exists()


def test_main_github_issues_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "CREATE", False)
    (tmp_path / "doc.md").write_text(
        "# Title\n\n- [ ] Implement BM25 search for the knowledge base\n",
        encoding="utf-8"
    )
    mod.main()
    text = (tmp_path / "GITHUB_ISSUES.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "CREATE", False)
    mod.main()
    assert (tmp_path / "GITHUB_ISSUES.md").exists()


def test_main_github_issues_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "CREATE", False)
    mod.main()
    text = (tmp_path / "GITHUB_ISSUES.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
