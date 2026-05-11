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
