"""Tests for scripts/improve_workflow_v2.py."""

import importlib
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_workflow_v2")


def _make_runner(step: dict, depends_on=None) -> "mod.StepRunner":
    """Helper to create a StepRunner without execute_step side-effects."""
    s = dict(step)
    if depends_on is not None:
        s["depends_on"] = depends_on
    return mod.StepRunner(s, {}, dry_run=True)


def test_step_runner_auto_id_from_op():
    runner = _make_runner({"print": "hello world"})
    assert "print" in runner.id


def test_step_runner_auto_id_truncates():
    runner = _make_runner({"print": "a" * 100})
    assert len(runner.id) <= 50


def test_step_runner_explicit_id():
    runner = _make_runner({"id": "my-step", "print": "hello"})
    assert runner.id == "my-step"


def test_step_runner_default_retry():
    runner = _make_runner({"print": "hello"})
    assert runner.retry == 0


def test_step_runner_custom_retry():
    runner = _make_runner({"print": "hello", "retry": 3})
    assert runner.retry == 3


def test_step_runner_default_timeout():
    runner = _make_runner({"print": "hello"})
    assert runner.timeout == 60


def test_step_runner_custom_timeout():
    runner = _make_runner({"print": "hello", "timeout": 30})
    assert runner.timeout == 30


def test_step_runner_empty_depends_on():
    runner = _make_runner({"print": "hello"})
    assert runner.depends_on == []


def test_step_runner_depends_on():
    runner = _make_runner({"print": "hello", "depends_on": ["step-a", "step-b"]})
    assert runner.depends_on == ["step-a", "step-b"]


def test_is_purely_sequential_all_no_deps():
    runners = [
        _make_runner({"print": "hello"}),
        _make_runner({"print": "world"}),
    ]
    assert mod._is_purely_sequential(runners) is True


def test_is_purely_sequential_with_deps():
    runners = [
        _make_runner({"print": "hello"}),
        _make_runner({"print": "world", "depends_on": ["step-a"]}),
    ]
    assert mod._is_purely_sequential(runners) is False


def test_is_purely_sequential_empty():
    assert mod._is_purely_sequential([]) is True


def test_topological_order_returns_list():
    runners = [_make_runner({"print": "hello"})]
    result = mod._topological_order(runners)
    assert isinstance(result, list)


def test_topological_order_sequential():
    runners = [
        _make_runner({"id": "a", "print": "hello"}),
        _make_runner({"id": "b", "print": "world"}),
    ]
    groups = mod._topological_order(runners)
    # all steps without deps are in one group (ready to run in parallel)
    flat = [s.id for group in groups for s in group]
    assert set(flat) == {"a", "b"}


def test_topological_order_respects_deps():
    runners = [
        _make_runner({"id": "b", "print": "b", "depends_on": ["a"]}),
        _make_runner({"id": "a", "print": "a"}),
    ]
    groups = mod._topological_order(runners)
    # "a" should appear before "b"
    flat = [s.id for group in groups for s in group]
    assert flat.index("a") < flat.index("b")


def test_topological_order_cycle_fallback():
    """Cyclic deps should not infinite-loop — fallback takes first remaining."""
    runners = [
        _make_runner({"id": "a", "print": "a", "depends_on": ["b"]}),
        _make_runner({"id": "b", "print": "b", "depends_on": ["a"]}),
    ]
    groups = mod._topological_order(runners)
    # Should complete without hanging
    flat = [s.id for group in groups for s in group]
    assert set(flat) == {"a", "b"}


def test_topological_order_parallel_group():
    """Steps with no deps and same level should all be in one group."""
    runners = [
        _make_runner({"id": "a", "print": "a"}),
        _make_runner({"id": "b", "print": "b"}),
        _make_runner({"id": "c", "print": "c", "depends_on": ["a", "b"]}),
    ]
    groups = mod._topological_order(runners)
    # "a" and "b" have no deps, so they're in first group
    first_ids = {s.id for s in groups[0]}
    assert "a" in first_ids or "b" in first_ids


def test_runs_log_attribute():
    assert hasattr(mod, "RUNS_LOG")
    assert isinstance(mod.RUNS_LOG, Path)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_list_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "RUNS_LOG", tmp_path / "runs.json")
    monkeypatch.setattr("sys.argv", ["prog", "--list"])
    result = mod.main()
    assert result == 0


def test_main_no_task_returns_error(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "RUNS_LOG", tmp_path / "runs.json")
    monkeypatch.setattr("sys.argv", ["prog"])
    result = mod.main()
    assert result == 1


def test_main_history_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "RUNS_LOG", tmp_path / "runs.json")
    monkeypatch.setattr("sys.argv", ["prog", "--history"])
    result = mod.main()
    assert result == 0


def test_run_workflow_missing_task(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "RUNS_LOG", tmp_path / "runs.jsonl")
    monkeypatch.setattr(mod, "load_task", lambda t: None)
    with pytest.raises(FileNotFoundError):
        mod.run_workflow("nonexistent-task", {})


def test_run_workflow_empty_pipeline(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "RUNS_LOG", tmp_path / "runs.jsonl")
    monkeypatch.setattr(mod, "load_task", lambda t: {"pipeline": []})
    result = mod.run_workflow("empty-task", {})
    assert result["status"] == "empty"


def test_run_workflow_dry_run(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "RUNS_LOG", tmp_path / "runs.jsonl")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    task = {"pipeline": [{"print": "hello world"}]}
    monkeypatch.setattr(mod, "load_task", lambda t: task)
    result = mod.run_workflow("test-task", {}, dry_run=True)
    assert isinstance(result, dict)
    assert "steps" in result
    assert len(result["steps"]) >= 1


def test_print_result_ok(capsys):
    r = {"id": "step1", "op": "print", "status": "ok", "duration_ms": 100, "attempts": []}
    mod._print_result(r)
    out = capsys.readouterr().out
    assert "step1" in out


def test_print_result_fail_with_error(capsys):
    r = {
        "id": "step1", "op": "run", "status": "fail", "duration_ms": 50,
        "attempts": [{"attempt": 1, "status": "fail", "duration_ms": 50,
                      "output_preview": "", "error": "Command failed here"}]
    }
    mod._print_result(r)
    out = capsys.readouterr().out
    assert "step1" in out


def test_print_result_dry_run(capsys):
    r = {"id": "step1", "op": "print", "status": "dry-run", "duration_ms": 0, "attempts": []}
    mod._print_result(r)
    out = capsys.readouterr().out
    assert "step1" in out


def test_summary_all_ok():
    results = [{"status": "ok"}, {"status": "ok"}]
    result = mod._summary(results)
    assert isinstance(result, dict)
    assert result["ok"] == 2
    assert result["fail"] == 0


def test_summary_with_fail():
    results = [{"status": "ok"}, {"status": "fail"}]
    result = mod._summary(results)
    assert result["ok"] == 1
    assert result["fail"] == 1


def test_save_and_load_runs(tmp_path, monkeypatch):
    runs_log = tmp_path / "runs.jsonl"
    monkeypatch.setattr(mod, "RUNS_LOG", runs_log)
    record = {
        "run_id": "abc123", "task_id": "test", "started": "2026-01-01",
        "finished": "2026-01-01", "duration_ms": 100, "inputs": {},
        "parallel": 1, "dry_run": False, "summary": {"ok": 1},
        "steps": []
    }
    mod._save_run(record)
    results = mod._load_runs()
    assert len(results) >= 1
    assert results[-1]["run_id"] == "abc123"


def test_load_runs_empty_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "RUNS_LOG", tmp_path / "nonexistent.jsonl")
    result = mod._load_runs()
    assert result == []


def test_load_runs_filter_by_task(tmp_path, monkeypatch):
    runs_log = tmp_path / "runs.jsonl"
    monkeypatch.setattr(mod, "RUNS_LOG", runs_log)
    mod._save_run({"run_id": "1", "task_id": "task-a", "started": "2026-01-01",
                   "finished": "2026-01-01", "duration_ms": 0, "inputs": {},
                   "parallel": 1, "dry_run": False, "summary": {}, "steps": []})
    mod._save_run({"run_id": "2", "task_id": "task-b", "started": "2026-01-01",
                   "finished": "2026-01-01", "duration_ms": 0, "inputs": {},
                   "parallel": 1, "dry_run": False, "summary": {}, "steps": []})
    results = mod._load_runs(task_id="task-a")
    assert all(r["task_id"] == "task-a" for r in results)


def test_cmd_history_empty(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "RUNS_LOG", tmp_path / "nonexistent.jsonl")
    result = mod.cmd_history()
    assert result == 0
    out = capsys.readouterr().out
    assert "Нет" in out or "no" in out.lower()


def test_cmd_history_with_runs(tmp_path, monkeypatch, capsys):
    runs_log = tmp_path / "runs.jsonl"
    monkeypatch.setattr(mod, "RUNS_LOG", runs_log)
    mod._save_run({"run_id": "test123", "task_id": "test-task", "started": "2026-01-01T10:00:00",
                   "finished": "2026-01-01T10:00:01", "duration_ms": 100, "inputs": {},
                   "parallel": 1, "dry_run": False, "summary": {"ok": 1}, "steps": []})
    result = mod.cmd_history()
    assert result == 0
    out = capsys.readouterr().out
    assert "test123" in out


def test_main_with_task_dry_run(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "RUNS_LOG", tmp_path / "runs.jsonl")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "load_task", lambda t: {"pipeline": [{"print": "hello"}]})
    monkeypatch.setattr("sys.argv", ["prog", "--task", "test-task", "--dry-run"])
    result = mod.main()
    assert result == 0


def test_run_workflow_parallel(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "RUNS_LOG", tmp_path / "runs.jsonl")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    task = {
        "pipeline": [
            {"id": "a", "print": "step a"},
            {"id": "b", "print": "step b"},
        ]
    }
    monkeypatch.setattr(mod, "load_task", lambda t: task)
    result = mod.run_workflow("test-task", {}, dry_run=True, parallel=2)
    assert len(result["steps"]) == 2
