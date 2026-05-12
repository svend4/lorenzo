"""Tests for scripts/improve_run_all.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_run_all")


def test_groups_is_dict():
    assert hasattr(mod, "GROUPS")
    assert isinstance(mod.GROUPS, dict)


def test_groups_not_empty():
    assert len(mod.GROUPS) > 0


def test_group_order_is_list():
    assert hasattr(mod, "GROUP_ORDER")
    assert isinstance(mod.GROUP_ORDER, list)


def test_group_order_all_in_groups():
    for g in mod.GROUP_ORDER:
        assert g in mod.GROUPS, f"Group {g} in GROUP_ORDER but not in GROUPS"


def test_slow_scripts_is_set():
    assert hasattr(mod, "SLOW_SCRIPTS")
    assert isinstance(mod.SLOW_SCRIPTS, set)


def test_llm_scripts_is_set():
    assert hasattr(mod, "LLM_SCRIPTS")
    assert isinstance(mod.LLM_SCRIPTS, set)
    assert "improve_llm_enrich.py" in mod.LLM_SCRIPTS


def test_smart_conditions_is_dict():
    assert hasattr(mod, "SMART_CONDITIONS")
    assert isinstance(mod.SMART_CONDITIONS, dict)


def test_parse_score_finds_score():
    text = "## Средний балл: **75/100**"
    result = mod._parse_score(text)
    assert result == 75.0


def test_parse_score_percentage():
    text = "## Итог: **159/164** (96%)"
    result = mod._parse_score(text)
    assert result == 96.0


def test_parse_score_none_for_no_match():
    result = mod._parse_score("no score here")
    assert result is None


def test_parse_score_general_pattern():
    text = "Quality: 88/100 achieved"
    result = mod._parse_score(text)
    assert result == 88.0


def test_should_skip_smart_not_smart():
    skip, reason = mod.should_skip_smart("improve_health.py", smart=False)
    assert skip is False


def test_should_skip_smart_unknown_script():
    skip, reason = mod.should_skip_smart("improve_unknown_xyz.py", smart=True)
    assert skip is False


def test_should_skip_smart_no_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    skip, reason = mod.should_skip_smart("improve_health.py", smart=True)
    # File doesn't exist → don't skip
    assert skip is False


def test_should_skip_smart_below_threshold(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "HEALTH.md").write_text("## Средний балл: **70/100**", encoding="utf-8")
    skip, reason = mod.should_skip_smart("improve_health.py", smart=True)
    assert skip is False


def test_should_skip_smart_above_threshold(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    docs = tmp_path / "docs"
    docs.mkdir()
    # improve_health.py threshold is 90
    (docs / "HEALTH.md").write_text("## Средний балл: **95/100**", encoding="utf-8")
    skip, reason = mod.should_skip_smart("improve_health.py", smart=True)
    assert skip is True


def test_read_score_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod._read_score("MISSING.md")
    assert result is None


def test_read_score_existing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "METRICS.md").write_text("Средний балл: **82.5/100**", encoding="utf-8")
    result = mod._read_score("METRICS.md")
    assert result == 82.5


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--dry-run"])
    mod.main()
    out = capsys.readouterr().out
    assert "Lorenzo" in out or "DRY" in out


def test_main_group_filter_no_crash(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--group", "reports", "--dry-run"])
    mod.main()


def test_main_list_scripts_no_crash(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--dry-run", "--fast"])
    mod.main()


def test_parse_score_with_average():
    result = mod._parse_score("**Средний балл:** 65.7/100")
    assert abs(result - 65.7) < 0.01


def test_parse_score_with_general():
    result = mod._parse_score("Общий балл: **75/100**")
    assert abs(result - 75.0) < 0.01


def test_parse_score_fallback():
    result = mod._parse_score("Score: 55/100")
    assert abs(result - 55.0) < 0.01


def test_parse_score_no_match():
    result = mod._parse_score("No score here")
    assert result is None


def test_get_changed_groups_returns_list():
    result = mod._get_changed_groups()
    assert isinstance(result, list)


def test_should_skip_smart_not_in_conditions():
    skip, reason = mod.should_skip_smart("unknown_script.py", smart=True)
    assert skip is False


def test_main_smart_dry_run(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--smart", "--dry-run"])
    mod.main()


def test_main_changed_dry_run(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["prog", "--changed", "--dry-run"])
    mod.main()
