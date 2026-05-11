"""
Тесты для scripts/improve_changelog_auto.py.

Покрытие:
  - parse_commits()     — парсинг git-лога в список коммитов
  - group_by_month()    — группировка коммитов по месяцу
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_changelog_auto")


# ── parse_commits ─────────────────────────────────────────────────────────────

def test_parse_commits_returns_list():
    log = "abc1234|||2025-01-15|||feat: add search feature"
    result = mod.parse_commits(log)
    assert isinstance(result, list)


def test_parse_commits_empty_log():
    result = mod.parse_commits("")
    assert result == []


def test_parse_commits_single_commit():
    log = "abc1234|||2025-01-15|||feat: add search feature"
    result = mod.parse_commits(log)
    assert len(result) == 1


def test_parse_commits_multiple_commits():
    log = (
        "abc1234|||2025-01-15|||feat: add search\n"
        "def5678|||2025-01-16|||fix: resolve issue\n"
        "ghi9012|||2025-01-17|||docs: update readme"
    )
    result = mod.parse_commits(log)
    assert len(result) == 3


def test_parse_commits_has_required_keys():
    log = "abc1234|||2025-01-15|||feat: add feature"
    result = mod.parse_commits(log)
    for key in ("sha", "date", "type", "scope", "msg"):
        assert key in result[0], f"Missing key: {key}"


def test_parse_commits_truncates_sha():
    log = "abcdef1234567890|||2025-01-15|||feat: add feature"
    result = mod.parse_commits(log)
    assert len(result[0]["sha"]) == 8


def test_parse_commits_feat_type():
    log = "abc1234|||2025-01-15|||feat: add new feature"
    result = mod.parse_commits(log)
    assert result[0]["type"] == "feat"


def test_parse_commits_fix_type():
    log = "abc1234|||2025-01-15|||fix: resolve bug"
    result = mod.parse_commits(log)
    assert result[0]["type"] == "fix"


def test_parse_commits_docs_type():
    log = "abc1234|||2025-01-15|||docs: update readme"
    result = mod.parse_commits(log)
    assert result[0]["type"] == "docs"


def test_parse_commits_chore_type():
    log = "abc1234|||2025-01-15|||chore: update deps"
    result = mod.parse_commits(log)
    assert result[0]["type"] == "chore"


def test_parse_commits_refactor_type():
    log = "abc1234|||2025-01-15|||refactor: clean up code"
    result = mod.parse_commits(log)
    assert result[0]["type"] == "refactor"


def test_parse_commits_test_type():
    log = "abc1234|||2025-01-15|||test: add unit tests"
    result = mod.parse_commits(log)
    assert result[0]["type"] == "test"


def test_parse_commits_unknown_type_becomes_other():
    log = "abc1234|||2025-01-15|||unknown: something odd"
    result = mod.parse_commits(log)
    assert result[0]["type"] == "other"


def test_parse_commits_no_type_becomes_other():
    log = "abc1234|||2025-01-15|||plain commit message"
    result = mod.parse_commits(log)
    assert result[0]["type"] == "other"


def test_parse_commits_extracts_scope():
    log = "abc1234|||2025-01-15|||feat(search): add BM25 search"
    result = mod.parse_commits(log)
    assert result[0]["scope"] == "search"


def test_parse_commits_no_scope_empty_string():
    log = "abc1234|||2025-01-15|||feat: add feature"
    result = mod.parse_commits(log)
    assert result[0]["scope"] == ""


def test_parse_commits_extracts_message():
    log = "abc1234|||2025-01-15|||feat: add BM25 search"
    result = mod.parse_commits(log)
    assert "BM25 search" in result[0]["msg"]


def test_parse_commits_truncates_message():
    long_msg = "a" * 200
    log = f"abc1234|||2025-01-15|||feat: {long_msg}"
    result = mod.parse_commits(log)
    assert len(result[0]["msg"]) <= 120


def test_parse_commits_date_truncated_to_10():
    log = "abc1234|||2025-01-15T14:30:00|||feat: add feature"
    result = mod.parse_commits(log)
    assert result[0]["date"] == "2025-01-15"


def test_parse_commits_skips_malformed_lines():
    log = "bad line without separators"
    result = mod.parse_commits(log)
    assert result == []


def test_parse_commits_skips_empty_lines():
    log = "abc1234|||2025-01-15|||feat: add\n\ndef5678|||2025-01-16|||fix: bug"
    result = mod.parse_commits(log)
    assert len(result) == 2


def test_parse_commits_case_insensitive_type():
    log = "abc1234|||2025-01-15|||FEAT: add feature"
    result = mod.parse_commits(log)
    assert result[0]["type"] == "feat"


# ── group_by_month ────────────────────────────────────────────────────────────

def test_group_by_month_returns_dict():
    commits = [{"sha": "abc", "date": "2025-01-15", "type": "feat", "scope": "", "msg": "test"}]
    result = mod.group_by_month(commits)
    assert isinstance(result, dict)


def test_group_by_month_empty():
    result = mod.group_by_month([])
    assert result == {}


def test_group_by_month_groups_same_month():
    commits = [
        {"sha": "abc", "date": "2025-01-15", "type": "feat", "scope": "", "msg": "a"},
        {"sha": "def", "date": "2025-01-20", "type": "fix", "scope": "", "msg": "b"},
    ]
    result = mod.group_by_month(commits)
    assert "2025-01" in result
    assert len(result["2025-01"]) == 2


def test_group_by_month_separates_months():
    commits = [
        {"sha": "abc", "date": "2025-01-15", "type": "feat", "scope": "", "msg": "a"},
        {"sha": "def", "date": "2025-02-10", "type": "fix", "scope": "", "msg": "b"},
    ]
    result = mod.group_by_month(commits)
    assert "2025-01" in result
    assert "2025-02" in result
    assert len(result) == 2


def test_group_by_month_sorted_descending():
    commits = [
        {"sha": "abc", "date": "2025-01-15", "type": "feat", "scope": "", "msg": "a"},
        {"sha": "def", "date": "2025-03-10", "type": "fix", "scope": "", "msg": "b"},
        {"sha": "ghi", "date": "2025-02-05", "type": "docs", "scope": "", "msg": "c"},
    ]
    result = mod.group_by_month(commits)
    keys = list(result.keys())
    assert keys == sorted(keys, reverse=True)


def test_group_by_month_key_format():
    commits = [{"sha": "abc", "date": "2025-06-15", "type": "feat", "scope": "", "msg": "a"}]
    result = mod.group_by_month(commits)
    assert "2025-06" in result
