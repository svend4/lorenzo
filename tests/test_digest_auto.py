"""Tests for scripts/improve_digest_auto.py."""

import importlib
import sys
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_digest_auto")


def test_tokenize_diff_returns_tuple():
    diff = "+agent memory system\n-old data removed\n"
    result = mod._tokenize_diff(diff)
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_tokenize_diff_added_tokens():
    diff = "+agent memory knowledge system retrieval\n"
    added, removed = mod._tokenize_diff(diff)
    assert isinstance(added, Counter)
    assert len(added) > 0


def test_tokenize_diff_removed_tokens():
    diff = "-agent memory knowledge system\n"
    added, removed = mod._tokenize_diff(diff)
    assert isinstance(removed, Counter)
    assert len(removed) > 0


def test_tokenize_diff_skips_markers():
    diff = "--- old file\n+++ new file\n+actual content added\n"
    added, removed = mod._tokenize_diff(diff)
    assert "file" not in added
    assert "file" not in removed


def test_tokenize_diff_min_4_chars():
    diff = "+ab abc abcd abcde\n"
    added, removed = mod._tokenize_diff(diff)
    for token in added:
        assert len(token) >= 4


def test_section_of_docs_file():
    result = mod._section_of("docs/01-svyazi/file.md")
    assert result == "01-svyazi"


def test_section_of_scripts():
    result = mod._section_of("scripts/improve_test.py")
    assert result == "scripts"


def test_section_of_root():
    result = mod._section_of("README.md")
    assert result == "root"


def test_section_of_nested_docs():
    result = mod._section_of("docs/05-habr-projects/memory/yodoca.md")
    assert result == "05-habr-projects"


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_digest_auto_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent here.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "DIGEST_AUTO.md").exists()


def test_main_digest_auto_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent here.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "DIGEST_AUTO.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "DIGEST_AUTO.md").exists()


def test_main_digest_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "DIGEST_AUTO.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


def test_tokenize_diff_returns_counters():
    diff = "+added agent memory system\n-removed old text\n"
    added, removed = mod._tokenize_diff(diff)
    assert isinstance(added, __import__("collections").Counter)
    assert "agent" in added or "memory" in added or "system" in added


def test_tokenize_diff_empty():
    added, removed = mod._tokenize_diff("")
    assert len(added) == 0
    assert len(removed) == 0


def test_section_of_docs_path():
    result = mod._section_of("docs/01-svyazi/doc.md")
    assert result == "01-svyazi"


def test_section_of_scripts_path():
    result = mod._section_of("scripts/improve_test.py")
    assert result == "scripts"


def test_section_of_root():
    result = mod._section_of("README.md")
    assert result == "root"


def test_commit_stats_returns_dict():
    result = mod._commit_stats("2020-01-01")
    assert isinstance(result, dict)
    assert "total" in result
    assert "commits" in result


def test_file_stats_returns_dict():
    result = mod._file_stats_from_log("2020-01-01")
    assert isinstance(result, dict)
    assert "added" in result
    assert "modified" in result
