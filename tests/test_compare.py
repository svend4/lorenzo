"""Tests for scripts/improve_compare.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_compare")


def test_word_count_returns_int():
    result = mod.word_count("one two three")
    assert isinstance(result, int)


def test_word_count_counts():
    result = mod.word_count("one two three four five")
    assert result == 5


def test_word_count_empty():
    result = mod.word_count("")
    assert result == 0


def test_word_count_multiline():
    result = mod.word_count("one two\nthree four")
    assert result == 4


def test_git_log_files_returns_dict():
    # git_log_files uses subprocess, handles exceptions gracefully
    result = mod.git_log_files(1)
    assert isinstance(result, dict)


def test_git_log_files_handles_error():
    # Should not raise even if git fails
    try:
        result = mod.git_log_files(9999)
        assert isinstance(result, dict)
    except Exception:
        pytest.fail("git_log_files should not raise exceptions")


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_compare_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent here.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "COMPARE.md").exists()


def test_main_compare_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent here.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "COMPARE.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "COMPARE.md").exists()


def test_main_compare_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "COMPARE.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


# ── main: changed files and removed files ─────────────────────────────────────

def test_main_with_changed_files(tmp_path, monkeypatch):
    """Lines 55-58: changed files → entries in changed list."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nNew content.", encoding="utf-8")
    # Fake old_files with different content for same path
    fake_old = {"docs/doc.md": "# AgentFS\n\nOld content here."}
    monkeypatch.setattr(mod, "git_log_files", lambda n: fake_old)
    mod.main()
    text = (tmp_path / "COMPARE.md").read_text(encoding="utf-8")
    assert "doc.md" in text


def test_main_with_removed_files(tmp_path, monkeypatch):
    """Line 81: removed files → listed in output."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    # No docs in tmp_path, but old_files has a file
    fake_old = {"docs/old_file.md": "# Old\n\nWas here."}
    monkeypatch.setattr(mod, "git_log_files", lambda n: fake_old)
    mod.main()
    text = (tmp_path / "COMPARE.md").read_text(encoding="utf-8")
    assert "old_file.md" in text


def test_main_many_added_files_truncated(tmp_path, monkeypatch):
    """Line 77: > 40 added files → truncation note appended."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    # Create 45 new docs files
    for i in range(45):
        (tmp_path / f"doc{i:03d}.md").write_text(f"# Title {i}\n\nContent.", encoding="utf-8")
    # No old files
    monkeypatch.setattr(mod, "git_log_files", lambda n: {})
    mod.main()
    text = (tmp_path / "COMPARE.md").read_text(encoding="utf-8")
    assert "и ещё" in text


# ── git_log_files: subprocess inner path ─────────────────────────────────────

def test_git_log_files_with_real_repo():
    """Lines 27-31: real git repo → inner git show runs, result[line] set."""
    result = mod.git_log_files(1)
    assert isinstance(result, dict)
    # If HEAD~1 exists with docs/*.md, result will have entries
    # Just verify it doesn't crash and returns valid dict


def test_git_log_files_exception_path(monkeypatch):
    """Lines 32-33: subprocess.run raises → caught by except, returns {}."""
    import subprocess
    def mock_run(*args, **kwargs):
        raise OSError("mock error")
    monkeypatch.setattr(subprocess, "run", mock_run)
    result = mod.git_log_files(1)
    assert result == {}


# ── __main__ block ─────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 98: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    runpy.run_path(str(ROOT / "scripts" / "improve_compare.py"), run_name="__main__")
