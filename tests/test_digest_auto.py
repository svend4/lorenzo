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


# ── _get_changed_files ────────────────────────────────────────────────────────

def test_get_changed_files_returns_dict():
    """Lines 100-116: _get_changed_files() returns a dict."""
    result = mod._get_changed_files("2020-01-01")
    assert isinstance(result, dict)


def test_get_changed_files_with_mock_output(monkeypatch):
    """Lines 103, 109: fallback log call + empty/commit lines skipped (continue)."""
    def mock_git(cmd):
        if cmd[0] == "diff":
            return ""  # first diff call returns empty → triggers fallback (line 103)
        # fallback log call returns output with empty + commit + real file lines
        return "A\tdocs/new-file.md\n\ncommit abc123\nM\tscripts/test.py\n"
    monkeypatch.setattr(mod, "_git", mock_git)
    result = mod._get_changed_files("2020-01-01")
    assert isinstance(result, dict)
    all_files = [f for files in result.values() for f in files]
    assert any(f.endswith(".md") or f.endswith(".py") for f in all_files)


# ── _get_diff_text fallback ───────────────────────────────────────────────────

def test_get_diff_text_returns_string():
    """Lines 120-128: _get_diff_text() returns string (may use fallback)."""
    result = mod._get_diff_text("2020-01-01")
    assert isinstance(result, str)


def test_get_diff_text_fallback_with_commits(monkeypatch):
    """Lines 126-127: fallback branch when diff is empty but 2+ commits exist."""
    def mock_git(cmd):
        if cmd[0] == "diff" and "HEAD@" in cmd[1]:
            return ""  # first call returns empty
        if cmd[0] == "log" and "--format=%H" in cmd[2]:
            return "abc123|a@b.com|subject|2026-01-01\ndef456|a@b.com|subject2|2026-01-02"
        if cmd[0] == "diff" and "abc123^" in cmd[1]:
            return "+added content here\n"
        return ""
    monkeypatch.setattr(mod, "_git", mock_git)
    result = mod._get_diff_text("2020-01-01")
    assert isinstance(result, str)


# ── _git exception handler ────────────────────────────────────────────────────

def test_git_exception_returns_empty(monkeypatch):
    """Lines 79-80: subprocess.run raises exception → empty string returned."""
    import subprocess
    def mock_run(*args, **kwargs):
        raise OSError("No git")
    monkeypatch.setattr(subprocess, "run", mock_run)
    result = mod._git(["log", "--oneline"])
    assert result == ""


# ── main with mocked data (covers sections 250-306) ──────────────────────────

def test_main_with_rich_mock_data(tmp_path, monkeypatch):
    """Lines 250-306: all main() sections rendered when data is available."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "FORMAT", "md")

    def mock_commit_stats(since):
        return {
            "total": 5,
            "commits": [{"date": "2026-01-01", "hash": "abc12345", "subject": "add agent memory"}],
            "authors": [("user@example.com", 5)],
            "by_date": {"2026-01-01": 5},
        }

    def mock_file_stats(since):
        return {
            "added": ["docs/01-svyazi/new-file.md"],
            "modified": ["docs/05-habr-projects/memory/yodoca.md"],
            "by_section": [("01-svyazi", 3), ("05-habr-projects", 2)],
            "total_changed": 2,
        }

    # Diff with tokens appearing 3+ times for new_concepts
    mock_diff = "+agent agent agent memory knowledge system\n-removed old system\n"
    monkeypatch.setattr(mod, "_commit_stats", mock_commit_stats)
    monkeypatch.setattr(mod, "_file_stats_from_log", mock_file_stats)
    monkeypatch.setattr(mod, "_get_diff_text", lambda since: mock_diff)

    mod.main()
    text = (tmp_path / "DIGEST_AUTO.md").read_text(encoding="utf-8")
    assert "Активность по секциям" in text
    assert "Последние коммиты" in text
    assert "Новые файлы" in text
    assert "Изменённые файлы" in text


def test_main_format_text(tmp_path, monkeypatch, capsys):
    """Lines 224-232: FORMAT=='text' → prints to stdout and returns early."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "FORMAT", "text")

    def mock_commit_stats(since):
        return {
            "total": 2,
            "commits": [{"date": "2026-01-01", "hash": "abc123", "subject": "test commit"}],
            "authors": [],
            "by_date": {},
        }

    def mock_file_stats(since):
        return {
            "added": ["docs/file.md"],
            "modified": [],
            "by_section": [],
            "total_changed": 1,
        }

    monkeypatch.setattr(mod, "_commit_stats", mock_commit_stats)
    monkeypatch.setattr(mod, "_file_stats_from_log", mock_file_stats)
    monkeypatch.setattr(mod, "_get_diff_text", lambda since: "+added content\n")

    mod.main()
    captured = capsys.readouterr()
    assert "Дайджест" in captured.out
    # No DIGEST_AUTO.md written (early return)
    assert not (tmp_path / "DIGEST_AUTO.md").exists()


# ── module-level arg parsing (requires reload) ────────────────────────────────

def test_days_arg_parsing():
    """Lines 33-35: --days N sets DAYS."""
    import sys, importlib
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--days", "14"]
        importlib.reload(mod)
        assert mod.DAYS == 14
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_since_arg_parsing():
    """Lines 38-40: --since DATE sets SINCE."""
    import sys, importlib
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--since", "2026-01-01"]
        importlib.reload(mod)
        assert mod.SINCE == "2026-01-01"
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


def test_format_arg_parsing():
    """Lines 43-45: --format text sets FORMAT."""
    import sys, importlib
    orig_argv = sys.argv[:]
    try:
        sys.argv = ["prog", "--format", "text"]
        importlib.reload(mod)
        assert mod.FORMAT == "text"
    finally:
        sys.argv = orig_argv
        importlib.reload(mod)


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 310: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "FORMAT", "md")
    script_path = str(ROOT / "scripts" / "improve_digest_auto.py")
    runpy.run_path(script_path, run_name="__main__")
