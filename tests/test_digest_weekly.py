"""
Тесты для scripts/improve_digest_weekly.py.

Покрытие:
  - git()                 — обёртка над subprocess.run для git команд
  - get_weekly_changes()  — парсинг изменений из git
  - word_count_delta()    — подсчёт слов в docs/
"""

import importlib
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_digest_weekly")

# ── git (helper function) ─────────────────────────────────────────────────────

def _mock_run(stdout=""):
    result = MagicMock()
    result.stdout = stdout
    return result


def test_git_returns_string():
    with patch("subprocess.run", return_value=_mock_run("output")):
        result = mod.git("status")
    assert isinstance(result, str)


def test_git_strips_output():
    with patch("subprocess.run", return_value=_mock_run("  output  \n")):
        result = mod.git("status")
    assert result == "output"


def test_git_empty_output():
    with patch("subprocess.run", return_value=_mock_run("")):
        result = mod.git("log")
    assert result == ""


# ── get_weekly_changes ────────────────────────────────────────────────────────

def test_get_weekly_changes_returns_dict():
    with patch.object(mod, "git", return_value=""):
        result = mod.get_weekly_changes()
    assert isinstance(result, dict)


def test_get_weekly_changes_has_required_keys():
    with patch.object(mod, "git", return_value=""):
        result = mod.get_weekly_changes()
    assert "commits" in result
    assert "added" in result
    assert "modified" in result
    assert "folders" in result
    assert "since" in result
    assert "days" in result


def test_get_weekly_changes_empty_commits():
    with patch.object(mod, "git", return_value=""):
        result = mod.get_weekly_changes()
    assert result["commits"] == []
    assert result["added"] == []
    assert result["modified"] == []


def test_get_weekly_changes_parses_commits():
    log_output = "abc1234 feat: add feature\nbcd5678 fix: fix bug"

    def fake_git(*args):
        if "log" in args:
            return log_output
        return ""

    with patch.object(mod, "git", side_effect=fake_git):
        result = mod.get_weekly_changes()
    assert len(result["commits"]) == 2


def test_get_weekly_changes_parses_added_files():
    def fake_git(*args):
        if "log" in args:
            return "abc1234 feat: add"
        if "diff" in args:
            return "A\tdocs/new-file.md\nM\tdocs/existing.md"
        return ""

    with patch.object(mod, "git", side_effect=fake_git):
        result = mod.get_weekly_changes()
    assert "docs/new-file.md" in result["added"]


def test_get_weekly_changes_parses_modified_files():
    def fake_git(*args):
        if "log" in args:
            return "abc1234 feat: add"
        if "diff" in args:
            return "M\tdocs/modified.md"
        return ""

    with patch.object(mod, "git", side_effect=fake_git):
        result = mod.get_weekly_changes()
    assert "docs/modified.md" in result["modified"]


def test_get_weekly_changes_respects_days_param():
    with patch.object(mod, "git", return_value="") as mock_git:
        mod.get_weekly_changes(days=14)
    # git should have been called with --since
    called_args = [str(call) for call in mock_git.call_args_list]
    assert any("since" in str(c).lower() for c in called_args)


# ── word_count_delta ──────────────────────────────────────────────────────────

def test_word_count_delta_returns_tuple(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.word_count_delta()
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_word_count_delta_returns_ints(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    current, delta = mod.word_count_delta()
    assert isinstance(current, int)
    assert isinstance(delta, int)


def test_word_count_delta_counts_words(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "a.md").write_text("one two three", encoding="utf-8")
    (tmp_path / "b.md").write_text("four five", encoding="utf-8")
    current, _ = mod.word_count_delta()
    assert current == 5


def test_word_count_delta_second_is_zero(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    _, delta = mod.word_count_delta()
    assert delta == 0


# ── main ──────────────────────────────────────────────────────────────────────

def _dw_setup(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "get_weekly_changes", lambda days=7: {
        "commits": [],
        "added": [],
        "modified": [],
        "folders": {},
        "since": "2026-05-04",
        "days": days,
    })
    monkeypatch.setattr(mod, "word_count_delta", lambda: (100, 5))
    (tmp_path / "sample.md").write_text("# Test\n\nContent.", encoding="utf-8")


def test_main_creates_digest_weekly_md(tmp_path, monkeypatch):
    _dw_setup(tmp_path, monkeypatch)
    mod.main()
    assert (tmp_path / "DIGEST_WEEKLY.md").exists()


def test_main_digest_weekly_has_content(tmp_path, monkeypatch):
    _dw_setup(tmp_path, monkeypatch)
    mod.main()
    text = (tmp_path / "DIGEST_WEEKLY.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_digest_weekly_no_crash(tmp_path, monkeypatch):
    _dw_setup(tmp_path, monkeypatch)
    mod.main()
