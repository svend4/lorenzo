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


# ── run_script ────────────────────────────────────────────────────────────────

def test_run_script_not_found(tmp_path, monkeypatch):
    """Lines 410-411: script file not found → returns (False, 0.0)."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    ok, elapsed = mod.run_script("nonexistent_xyz_script.py", dry_run=False)
    assert ok is False
    assert elapsed == 0.0


def test_run_script_success(tmp_path, monkeypatch):
    """Lines 417-430: subprocess succeeds → returns (True, elapsed)."""
    import subprocess as sp
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "fake.py").write_text("print('done')", encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", tmp_path)

    def mock_run(cmd, **kwargs):
        return sp.CompletedProcess(cmd, 0, stdout="Success line\n", stderr="")

    monkeypatch.setattr(sp, "run", mock_run)
    ok, elapsed = mod.run_script("fake.py", dry_run=False)
    assert ok is True


def test_run_script_failure(tmp_path, monkeypatch):
    """Lines 431-434: subprocess fails → returns (False, elapsed)."""
    import subprocess as sp
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "fake.py").write_text("exit(1)", encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", tmp_path)

    def mock_run(cmd, **kwargs):
        return sp.CompletedProcess(cmd, 1, stdout="", stderr="fatal error occurred\n")

    monkeypatch.setattr(sp, "run", mock_run)
    ok, elapsed = mod.run_script("fake.py", dry_run=False)
    assert ok is False


# ── _get_changed_groups (lines 381, 384, 388) ─────────────────────────────────

def test_get_changed_groups_with_docs_and_scripts(monkeypatch):
    """Lines 381, 384, 388: docs + scripts changes → groups populated."""
    import subprocess as sp
    call_count = [0]

    def mock_run(cmd, **kwargs):
        call_count[0] += 1
        if call_count[0] == 1:
            return sp.CompletedProcess(cmd, 0, stdout="docs/01-svyazi/file.md\n", stderr="")
        return sp.CompletedProcess(cmd, 0, stdout="scripts/test.py\n", stderr="")

    monkeypatch.setattr(sp, "run", mock_run)
    result = mod._get_changed_groups()
    assert isinstance(result, list)
    assert len(result) > 0


# ── main: --parallel flag ──────────────────────────────────────────────────────

def test_main_parallel_valid_flag(monkeypatch, capsys):
    """Lines 449-452: --parallel N sets parallel=N."""
    monkeypatch.setattr("sys.argv", ["prog", "--parallel", "2", "--dry-run", "--group", "mcp"])
    mod.main()


def test_main_parallel_invalid_value(monkeypatch, capsys):
    """Lines 453-454: --parallel notanint → parallel=4 (ValueError branch)."""
    monkeypatch.setattr("sys.argv", ["prog", "--parallel", "notanint", "--dry-run", "--group", "mcp"])
    mod.main()


# ── main: --only flag ─────────────────────────────────────────────────────────

def test_main_only_with_extension(monkeypatch, capsys):
    """Lines 462-469: --only improve_health.py --dry-run → only_scripts branch."""
    monkeypatch.setattr("sys.argv", ["prog", "--only", "improve_health.py", "--dry-run"])
    mod.main()
    out = capsys.readouterr().out
    assert "improve_health.py" in out


def test_main_only_without_extension(monkeypatch, capsys):
    """Line 467-468: name without .py → .py appended."""
    monkeypatch.setattr("sys.argv", ["prog", "--only", "improve_health,improve_metrics", "--dry-run"])
    mod.main()


def test_main_only_with_llm_script(monkeypatch, capsys):
    """Lines 494-497, 539-541: LLM script in --only → skipped with message."""
    monkeypatch.setattr("sys.argv", ["prog", "--only", "improve_llm_enrich.py", "--dry-run"])
    mod.main()
    out = capsys.readouterr().out
    assert "ANTHROPIC_API_KEY" in out


def test_main_only_with_error_exits(monkeypatch, capsys):
    """Lines 509-510, 585: total_err > 0 → sys.exit(1)."""
    monkeypatch.setattr("sys.argv", ["prog", "--only", "improve_health.py"])

    def mock_run_script(script, dry_run=False):
        return False, 0.5

    monkeypatch.setattr(mod, "run_script", mock_run_script)
    with pytest.raises(SystemExit):
        mod.main()


# ── main: --changed with non-empty groups ─────────────────────────────────────

def test_main_changed_with_groups_found(monkeypatch, capsys):
    """Line 520: --changed with groups found → prints groups."""
    import subprocess as sp
    call_count = [0]

    def mock_run(cmd, **kwargs):
        call_count[0] += 1
        if call_count[0] <= 2 and "diff" in cmd and "--name-only" in cmd:
            return sp.CompletedProcess(cmd, 0, stdout="docs/01-svyazi/file.md\n", stderr="")
        return sp.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(sp, "run", mock_run)
    monkeypatch.setattr("sys.argv", ["prog", "--changed", "--dry-run"])
    mod.main()
    out = capsys.readouterr().out
    assert "Группы" in out or "structure" in out or "index" in out


# ── main: unknown group ───────────────────────────────────────────────────────

def test_main_unknown_group_warns(monkeypatch, capsys):
    """Lines 528-529: unknown group → warning printed."""
    monkeypatch.setattr("sys.argv", ["prog", "--group", "nonexistent_xyz_group", "--dry-run"])
    mod.main()
    out = capsys.readouterr().out
    assert "не найдена" in out


# ── _run_group: LLM skip and error path ──────────────────────────────────────

def test_run_group_skips_llm_scripts(monkeypatch, capsys):
    """Lines 539-541: LLM script in group → skipped with LLM message."""
    monkeypatch.setattr(mod, "GROUPS", {
        "test_llm_group": ["improve_llm_enrich.py", "improve_health.py"]
    })
    monkeypatch.setattr("sys.argv", ["prog", "--group", "test_llm_group", "--dry-run"])
    mod.main()
    out = capsys.readouterr().out
    assert "ANTHROPIC_API_KEY" in out


def test_run_group_counts_errors(monkeypatch, capsys):
    """Line 555, 585: run_script returns False → g_err incremented → sys.exit(1)."""
    monkeypatch.setattr(mod, "GROUPS", {"test_err_group": ["improve_health.py"]})
    monkeypatch.setattr("sys.argv", ["prog", "--group", "test_err_group"])

    def mock_run_script(script, dry_run=False):
        return False, 0.5

    monkeypatch.setattr(mod, "run_script", mock_run_script)
    with pytest.raises(SystemExit):
        mod.main()


# ── parallel execution ─────────────────────────────────────────────────────────

def test_main_parallel_execution(monkeypatch, capsys):
    """Lines 560-565: parallel > 1 and not dry_run → ThreadPoolExecutor used."""
    monkeypatch.setattr(mod, "GROUPS", {"test_par_group": ["improve_health.py"]})
    monkeypatch.setattr("sys.argv", ["prog", "--parallel", "2", "--group", "test_par_group"])

    def mock_run_script(script, dry_run=False):
        return True, 0.0

    monkeypatch.setattr(mod, "run_script", mock_run_script)
    mod.main()


# ── --report flag ─────────────────────────────────────────────────────────────

def test_main_report_flag(monkeypatch, capsys):
    """Lines 577-582: --report shows git diff --stat output."""
    import subprocess as sp
    monkeypatch.setattr(mod, "GROUPS", {"test_rep_group": ["improve_health.py"]})
    monkeypatch.setattr("sys.argv", ["prog", "--report", "--group", "test_rep_group"])

    def mock_run_script(script, dry_run=False):
        return True, 0.0

    monkeypatch.setattr(mod, "run_script", mock_run_script)

    def mock_sp_run(cmd, **kwargs):
        if isinstance(cmd, list) and "git" in cmd:
            return sp.CompletedProcess(cmd, 0, stdout=" 2 files changed\n", stderr="")
        return sp.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(sp, "run", mock_sp_run)
    mod.main()
    out = capsys.readouterr().out
    assert "Изменения" in out or "files changed" in out


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(monkeypatch):
    """Line 589: __main__ block."""
    import runpy
    monkeypatch.setattr("sys.argv", ["prog", "--dry-run", "--group", "mcp"])
    script_path = str(ROOT / "scripts" / "improve_run_all.py")
    runpy.run_path(script_path, run_name="__main__")
