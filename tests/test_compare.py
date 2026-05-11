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
