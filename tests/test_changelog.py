"""
Тесты для scripts/improve_changelog.py.

Покрытие:
  - get_git_log()        — парсинг git log в список dict
  - parse_commit_type()  — тип коммита и описание из conventional commits
  - group_by_date()      — группировка коммитов по дате
  - format_stats()       — статистика по типам коммитов
"""

import importlib
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_changelog")

# ── get_git_log ───────────────────────────────────────────────────────────────

def _mock_run(stdout):
    result = MagicMock()
    result.stdout = stdout
    result.returncode = 0
    return result


def test_get_git_log_returns_list():
    with patch("subprocess.run", return_value=_mock_run("")):
        result = mod.get_git_log()
    assert isinstance(result, list)


def test_get_git_log_parses_commit():
    output = "abc12345|2025-05-01T10:00:00 +0000|feat: add feature|body text"
    with patch("subprocess.run", return_value=_mock_run(output)):
        result = mod.get_git_log()
    assert len(result) == 1
    assert result[0]["sha"] == "abc12345"
    assert result[0]["date"] == "2025-05-01"
    assert "add feature" in result[0]["subject"]


def test_get_git_log_truncates_sha():
    output = "abcdef1234567890|2025-05-01T00:00:00 +0000|fix: something|"
    with patch("subprocess.run", return_value=_mock_run(output)):
        result = mod.get_git_log()
    assert len(result[0]["sha"]) == 8


def test_get_git_log_empty_output():
    with patch("subprocess.run", return_value=_mock_run("")):
        result = mod.get_git_log()
    assert result == []


def test_get_git_log_multiple_commits():
    output = (
        "aaa11111|2025-05-01T00:00:00 +0000|feat: alpha|\n"
        "bbb22222|2025-05-02T00:00:00 +0000|fix: beta|"
    )
    with patch("subprocess.run", return_value=_mock_run(output)):
        result = mod.get_git_log()
    assert len(result) == 2


def test_get_git_log_handles_exception():
    with patch("subprocess.run", side_effect=Exception("git error")):
        result = mod.get_git_log()
    assert result == []


# ── parse_commit_type ─────────────────────────────────────────────────────────

def test_parse_commit_type_returns_tuple():
    result = mod.parse_commit_type("feat: add feature")
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_parse_commit_type_feat():
    t, desc = mod.parse_commit_type("feat: add new feature")
    assert t == "feat"
    assert "new feature" in desc


def test_parse_commit_type_fix():
    t, desc = mod.parse_commit_type("fix: correct bug")
    assert t == "fix"
    assert "correct bug" in desc


def test_parse_commit_type_improve():
    t, desc = mod.parse_commit_type("improve: better search")
    assert t == "improve"


def test_parse_commit_type_with_scope():
    t, desc = mod.parse_commit_type("feat(search): add BM25")
    assert t == "feat"
    assert "BM25" in desc


def test_parse_commit_type_unknown_defaults_to_chore():
    t, desc = mod.parse_commit_type("update: something unclear")
    assert t == "chore"
    assert "something unclear" in desc


def test_parse_commit_type_case_insensitive():
    t, _ = mod.parse_commit_type("Feat: add feature")
    assert t == "feat"


def test_parse_commit_type_docs():
    t, _ = mod.parse_commit_type("docs: update README")
    assert t == "docs"


def test_parse_commit_type_test():
    t, _ = mod.parse_commit_type("test: add unit tests")
    assert t == "test"


def test_parse_commit_type_chore():
    t, _ = mod.parse_commit_type("chore: update dependencies")
    assert t == "chore"


# ── group_by_date ─────────────────────────────────────────────────────────────

def test_group_by_date_returns_dict():
    commits = [{"sha": "abc", "date": "2025-05-01", "subject": "feat: x", "body": ""}]
    result = mod.group_by_date(commits)
    assert isinstance(result, dict)


def test_group_by_date_groups_same_date():
    commits = [
        {"sha": "a", "date": "2025-05-01", "subject": "feat: a", "body": ""},
        {"sha": "b", "date": "2025-05-01", "subject": "fix: b", "body": ""},
        {"sha": "c", "date": "2025-05-02", "subject": "chore: c", "body": ""},
    ]
    result = mod.group_by_date(commits)
    assert len(result["2025-05-01"]) == 2
    assert len(result["2025-05-02"]) == 1


def test_group_by_date_empty_list():
    result = mod.group_by_date([])
    assert result == {}


def test_group_by_date_keys_are_dates():
    commits = [{"sha": "x", "date": "2025-05-03", "subject": "feat: x", "body": ""}]
    result = mod.group_by_date(commits)
    assert "2025-05-03" in result


# ── format_stats ──────────────────────────────────────────────────────────────

def test_format_stats_returns_string():
    commits = [{"sha": "a", "date": "2025-05-01", "subject": "feat: alpha", "body": ""}]
    result = mod.format_stats(commits)
    assert isinstance(result, str)


def test_format_stats_contains_commit_type():
    commits = [{"sha": "a", "date": "2025-05-01", "subject": "feat: alpha", "body": ""}]
    result = mod.format_stats(commits)
    assert "feat" in result


def test_format_stats_empty_list():
    result = mod.format_stats([])
    assert isinstance(result, str)


def test_format_stats_counts_correctly():
    commits = [
        {"sha": "a", "subject": "feat: alpha", "date": "2025-05-01", "body": ""},
        {"sha": "b", "subject": "feat: beta",  "date": "2025-05-01", "body": ""},
        {"sha": "c", "subject": "fix: gamma",  "date": "2025-05-02", "body": ""},
    ]
    result = mod.format_stats(commits)
    assert "feat: 2" in result
    assert "fix: 1" in result


def test_format_stats_multiple_types():
    commits = [
        {"sha": "a", "subject": "feat: x", "date": "2025-05-01", "body": ""},
        {"sha": "b", "subject": "fix: y",  "date": "2025-05-01", "body": ""},
        {"sha": "c", "subject": "docs: z", "date": "2025-05-01", "body": ""},
    ]
    result = mod.format_stats(commits)
    assert "|" in result  # separator between entries
