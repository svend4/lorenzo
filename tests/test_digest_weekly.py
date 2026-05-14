"""
Тесты для scripts/improve_digest_weekly.py.

Покрытие нового API (после Iteration 14 rewrite):
  - _git()                — обёртка над subprocess.run
  - get_git_activity()    — git коммиты, added/modified, folders
  - get_card_stats()      — lifecycle статусы карточек
  - get_hot_cards()       — топ-K из .claude/hot_cards.json
  - get_query_analytics() — статистика запросов из query_log.jsonl
  - word_count()          — суммарный word-count docs/
  - build_report()        — сборка markdown отчёта
  - main()                — entry point
"""

import importlib
import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_digest_weekly")


# ── _git (helper) ─────────────────────────────────────────────────────────────

def _mock_run(stdout=""):
    result = MagicMock()
    result.stdout = stdout
    return result


def test_git_returns_string():
    with patch("subprocess.run", return_value=_mock_run("output")):
        result = mod._git("status")
    assert isinstance(result, str)


def test_git_strips_output():
    with patch("subprocess.run", return_value=_mock_run("  output  \n")):
        result = mod._git("status")
    assert result == "output"


def test_git_empty_output():
    with patch("subprocess.run", return_value=_mock_run("")):
        result = mod._git("log")
    assert result == ""


# ── get_git_activity ──────────────────────────────────────────────────────────

def test_get_git_activity_returns_dict():
    with patch.object(mod, "_git", return_value=""):
        result = mod.get_git_activity()
    assert isinstance(result, dict)


def test_get_git_activity_has_required_keys():
    with patch.object(mod, "_git", return_value=""):
        result = mod.get_git_activity()
    for key in ("commits", "added", "modified", "folders", "since", "days"):
        assert key in result


def test_get_git_activity_empty_commits():
    with patch.object(mod, "_git", return_value=""):
        result = mod.get_git_activity()
    assert result["commits"] == []
    assert result["added"] == []
    assert result["modified"] == []


def test_get_git_activity_parses_commits():
    def fake_git(*args):
        if "log" in args:
            return "abc1234 feat: add feature\nbcd5678 fix: fix bug"
        return ""

    with patch.object(mod, "_git", side_effect=fake_git):
        result = mod.get_git_activity()
    assert len(result["commits"]) == 2


def test_get_git_activity_parses_added_files():
    def fake_git(*args):
        if "log" in args:
            return "abc1234 feat: add"
        if "diff" in args:
            return "A\tdocs/new-file.md\nM\tdocs/existing.md"
        return ""

    with patch.object(mod, "_git", side_effect=fake_git):
        result = mod.get_git_activity()
    assert "docs/new-file.md" in result["added"]


def test_get_git_activity_parses_modified_files():
    def fake_git(*args):
        if "log" in args:
            return "abc1234 feat: add"
        if "diff" in args:
            return "M\tdocs/modified.md"
        return ""

    with patch.object(mod, "_git", side_effect=fake_git):
        result = mod.get_git_activity()
    assert "docs/modified.md" in result["modified"]


def test_get_git_activity_respects_days_param():
    with patch.object(mod, "_git", return_value="") as mock_git:
        mod.get_git_activity(days=14)
    called_args = [str(call) for call in mock_git.call_args_list]
    assert any("since" in str(c).lower() for c in called_args)


# ── word_count ────────────────────────────────────────────────────────────────

def test_word_count_returns_int(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    assert isinstance(mod.word_count(), int)


def test_word_count_counts_words(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "a.md").write_text("one two three", encoding="utf-8")
    (tmp_path / "b.md").write_text("four five", encoding="utf-8")
    assert mod.word_count() == 5


def test_word_count_zero_on_empty_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    assert mod.word_count() == 0


# ── get_card_stats ────────────────────────────────────────────────────────────

def test_get_card_stats_returns_required_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.get_card_stats()
    for key in ("total", "approved", "normalized", "raw", "promote_pct"):
        assert key in result


def test_get_card_stats_classifies_states(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "a.md").write_text("---\nstate: approved\n---\n# A", encoding="utf-8")
    (tmp_path / "b.md").write_text("---\nstate: normalized\n---\n# B", encoding="utf-8")
    (tmp_path / "c.md").write_text("# C without state", encoding="utf-8")
    s = mod.get_card_stats()
    assert s["approved"] == 1
    assert s["normalized"] == 1
    assert s["raw"] == 1
    assert s["total"] == 3


# ── get_hot_cards ─────────────────────────────────────────────────────────────

def test_get_hot_cards_returns_list_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    assert mod.get_hot_cards() == []


def test_get_hot_cards_reads_from_json(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    claude = tmp_path / ".claude"
    claude.mkdir()
    (claude / "hot_cards.json").write_text(
        json.dumps({"top": [{"title": "T1"}, {"title": "T2"}, {"title": "T3"}]}),
        encoding="utf-8",
    )
    result = mod.get_hot_cards(top_k=2)
    assert len(result) == 2
    assert result[0]["title"] == "T1"


# ── get_query_analytics ───────────────────────────────────────────────────────

def test_get_query_analytics_returns_zero_count_when_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    assert mod.get_query_analytics()["count"] == 0


# ── main ──────────────────────────────────────────────────────────────────────

def _dw_setup(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "get_git_activity", lambda days=7: {
        "commits": [],
        "added": [],
        "modified": [],
        "folders": {},
        "since": "2026-05-04",
        "days": days,
    })
    monkeypatch.setattr(mod, "get_card_stats", lambda: {
        "total": 1, "approved": 0, "normalized": 0, "raw": 1, "promote_pct": 0.0,
    })
    monkeypatch.setattr(mod, "get_hot_cards", lambda top_k=5: [])
    monkeypatch.setattr(mod, "get_query_analytics", lambda days=7, top_k=5: {"count": 0})
    monkeypatch.setattr(sys, "argv", ["improve_digest_weekly.py"])
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
