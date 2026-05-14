"""Tests for docstoolkit.task_planner."""
from __future__ import annotations

import pytest

from docstoolkit.task_planner import Plan, Task, TaskPlanner, TaskStatus


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------


def _linear_planner() -> TaskPlanner:
    """A -> B -> C with durations 1, 2, 3."""
    p = TaskPlanner()
    p.add_task("a", "A", 1.0)
    p.add_task("b", "B", 2.0, ["a"])
    p.add_task("c", "C", 3.0, ["b"])
    return p


def _diamond_planner() -> TaskPlanner:
    """A -> B, A -> C, B -> D, C -> D (diamond)."""
    p = TaskPlanner()
    p.add_task("a", "A", 1.0)
    p.add_task("b", "B", 5.0, ["a"])
    p.add_task("c", "C", 2.0, ["a"])
    p.add_task("d", "D", 1.0, ["b", "c"])
    return p


# ----------------------------------------------------------------------
# TaskStatus
# ----------------------------------------------------------------------


class TestTaskStatus:
    def test_members(self):
        names = {s.name for s in TaskStatus}
        assert names == {"PENDING", "READY", "RUNNING", "DONE", "BLOCKED", "FAILED"}

    def test_pending_value(self):
        assert TaskStatus.PENDING.value == "pending"

    def test_failed_value(self):
        assert TaskStatus.FAILED.value == "failed"

    def test_done_value(self):
        assert TaskStatus.DONE.value == "done"


# ----------------------------------------------------------------------
# Task dataclass
# ----------------------------------------------------------------------


class TestTask:
    def test_defaults(self):
        t = Task(task_id="x", name="X", duration=1.0)
        assert t.dependencies == []
        assert t.status == TaskStatus.PENDING
        assert t.started_at == 0.0
        assert t.completed_at == 0.0

    def test_with_dependencies(self):
        t = Task(task_id="x", name="X", duration=1.0, dependencies=["a", "b"])
        assert t.dependencies == ["a", "b"]

    def test_status_assignment(self):
        t = Task(task_id="x", name="X", duration=1.0)
        t.status = TaskStatus.RUNNING
        assert t.status == TaskStatus.RUNNING


# ----------------------------------------------------------------------
# Plan dataclass
# ----------------------------------------------------------------------


class TestPlanDataclass:
    def test_construct(self):
        p = Plan(tasks=[], task_order=[], critical_path=[], total_duration=0.0)
        assert p.tasks == []
        assert p.task_order == []
        assert p.critical_path == []
        assert p.total_duration == 0.0


# ----------------------------------------------------------------------
# add_task
# ----------------------------------------------------------------------


class TestAddTask:
    def test_basic(self):
        p = TaskPlanner()
        task = p.add_task("a", "A", 1.5)
        assert task.task_id == "a"
        assert task.duration == 1.5
        assert p.task_count == 1

    def test_with_deps(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0)
        b = p.add_task("b", "B", 2.0, ["a"])
        assert b.dependencies == ["a"]

    def test_duplicate_raises(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0)
        with pytest.raises(ValueError):
            p.add_task("a", "A2", 2.0)

    def test_negative_duration_raises(self):
        p = TaskPlanner()
        with pytest.raises(ValueError):
            p.add_task("a", "A", -1.0)

    def test_zero_duration_allowed(self):
        p = TaskPlanner()
        p.add_task("a", "A", 0.0)
        assert p.task_count == 1


# ----------------------------------------------------------------------
# remove_task
# ----------------------------------------------------------------------


class TestRemoveTask:
    def test_remove_leaf(self):
        p = _linear_planner()
        assert p.remove_task("c") is True
        assert p.task_count == 2

    def test_remove_missing_returns_false(self):
        p = TaskPlanner()
        assert p.remove_task("nope") is False

    def test_remove_blocked_by_dependent(self):
        p = _linear_planner()
        # 'b' depends on 'a'; cannot drop 'a'.
        assert p.remove_task("a") is False
        assert p.task_count == 3

    def test_remove_after_dependent_dropped(self):
        p = _linear_planner()
        p.remove_task("c")
        p.remove_task("b")
        assert p.remove_task("a") is True
        assert p.task_count == 0


# ----------------------------------------------------------------------
# update_status
# ----------------------------------------------------------------------


class TestUpdateStatus:
    def test_set_running_records_started_at(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0)
        p.update_status("a", TaskStatus.RUNNING, now=10.0)
        assert p.get_task("a").status == TaskStatus.RUNNING
        assert p.get_task("a").started_at == 10.0

    def test_set_done_records_completed_at(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0)
        p.update_status("a", TaskStatus.DONE, now=42.0)
        assert p.get_task("a").completed_at == 42.0

    def test_set_failed_records_completed_at(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0)
        p.update_status("a", TaskStatus.FAILED, now=5.0)
        assert p.get_task("a").completed_at == 5.0

    def test_unknown_returns_false(self):
        p = TaskPlanner()
        assert p.update_status("nope", TaskStatus.DONE) is False

    def test_running_then_done(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0)
        p.update_status("a", TaskStatus.RUNNING, now=1.0)
        p.update_status("a", TaskStatus.DONE, now=4.0)
        t = p.get_task("a")
        assert t.started_at == 1.0
        assert t.completed_at == 4.0


# ----------------------------------------------------------------------
# get_task
# ----------------------------------------------------------------------


class TestGetTask:
    def test_existing(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0)
        assert p.get_task("a").name == "A"

    def test_missing_returns_none(self):
        p = TaskPlanner()
        assert p.get_task("nope") is None


# ----------------------------------------------------------------------
# ready_tasks
# ----------------------------------------------------------------------


class TestReadyTasks:
    def test_no_deps_all_ready(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0)
        p.add_task("b", "B", 1.0)
        ready = {t.task_id for t in p.ready_tasks()}
        assert ready == {"a", "b"}

    def test_with_pending_dep_not_ready(self):
        p = _linear_planner()
        ready = {t.task_id for t in p.ready_tasks()}
        assert ready == {"a"}

    def test_after_dep_done(self):
        p = _linear_planner()
        p.mark_done("a")
        ready = {t.task_id for t in p.ready_tasks()}
        assert ready == {"b"}

    def test_done_task_not_in_ready(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0)
        p.mark_done("a")
        assert p.ready_tasks() == []

    def test_diamond_progress(self):
        p = _diamond_planner()
        p.mark_done("a")
        ready = {t.task_id for t in p.ready_tasks()}
        assert ready == {"b", "c"}
        p.mark_done("b")
        p.mark_done("c")
        ready = {t.task_id for t in p.ready_tasks()}
        assert ready == {"d"}


# ----------------------------------------------------------------------
# blocked_tasks
# ----------------------------------------------------------------------


class TestBlockedTasks:
    def test_no_failures(self):
        p = _linear_planner()
        assert p.blocked_tasks() == []

    def test_failed_dep_blocks_successor(self):
        p = _linear_planner()
        p.update_status("a", TaskStatus.FAILED)
        blocked = {t.task_id for t in p.blocked_tasks()}
        assert "b" in blocked

    def test_diamond_one_failure(self):
        p = _diamond_planner()
        p.update_status("b", TaskStatus.FAILED)
        blocked = {t.task_id for t in p.blocked_tasks()}
        assert blocked == {"d"}


# ----------------------------------------------------------------------
# topological_order
# ----------------------------------------------------------------------


class TestTopologicalOrder:
    def test_linear(self):
        p = _linear_planner()
        assert p.topological_order() == ["a", "b", "c"]

    def test_diamond_a_first_d_last(self):
        order = _diamond_planner().topological_order()
        assert order[0] == "a"
        assert order[-1] == "d"
        # b and c after a.
        assert order.index("b") > order.index("a")
        assert order.index("c") > order.index("a")
        # d after b and c.
        assert order.index("d") > order.index("b")
        assert order.index("d") > order.index("c")

    def test_independent_tasks(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0)
        p.add_task("b", "B", 1.0)
        p.add_task("c", "C", 1.0)
        order = p.topological_order()
        assert set(order) == {"a", "b", "c"}

    def test_missing_dep_raises(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0, ["ghost"])
        with pytest.raises(ValueError):
            p.topological_order()


# ----------------------------------------------------------------------
# Cycles
# ----------------------------------------------------------------------


class TestTopoOrderCyclic:
    def test_two_cycle(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0, ["b"])
        p.add_task("b", "B", 1.0, ["a"])
        with pytest.raises(ValueError):
            p.topological_order()

    def test_three_cycle(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0, ["c"])
        p.add_task("b", "B", 1.0, ["a"])
        p.add_task("c", "C", 1.0, ["b"])
        with pytest.raises(ValueError):
            p.topological_order()


class TestHasCycle:
    def test_acyclic(self):
        assert _diamond_planner().has_cycle() is False

    def test_cyclic(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0, ["b"])
        p.add_task("b", "B", 1.0, ["a"])
        assert p.has_cycle() is True

    def test_self_loop(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0, ["a"])
        assert p.has_cycle() is True

    def test_empty(self):
        assert TaskPlanner().has_cycle() is False


# ----------------------------------------------------------------------
# critical_path
# ----------------------------------------------------------------------


class TestCriticalPath:
    def test_linear(self):
        assert _linear_planner().critical_path() == ["a", "b", "c"]

    def test_diamond(self):
        # a(1)->b(5)->d(1) = 7, a(1)->c(2)->d(1) = 4
        cp = _diamond_planner().critical_path()
        assert cp == ["a", "b", "d"]

    def test_empty(self):
        assert TaskPlanner().critical_path() == []

    def test_single_task(self):
        p = TaskPlanner()
        p.add_task("a", "A", 5.0)
        assert p.critical_path() == ["a"]

    def test_parallel_branches_pick_longer(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0)
        p.add_task("b", "B", 10.0)
        p.add_task("c", "C", 2.0)
        cp = p.critical_path()
        assert cp == ["b"]


# ----------------------------------------------------------------------
# total_duration
# ----------------------------------------------------------------------


class TestTotalDuration:
    def test_linear(self):
        assert _linear_planner().total_duration() == pytest.approx(6.0)

    def test_diamond(self):
        # a(1) + b(5) + d(1) = 7
        assert _diamond_planner().total_duration() == pytest.approx(7.0)

    def test_empty(self):
        assert TaskPlanner().total_duration() == 0.0

    def test_independent(self):
        p = TaskPlanner()
        p.add_task("a", "A", 3.0)
        p.add_task("b", "B", 7.0)
        # Longest single-task path is b.
        assert p.total_duration() == pytest.approx(7.0)


# ----------------------------------------------------------------------
# plan
# ----------------------------------------------------------------------


class TestPlan:
    def test_returns_plan_obj(self):
        p = _diamond_planner()
        plan = p.plan()
        assert isinstance(plan, Plan)
        assert plan.total_duration == pytest.approx(7.0)
        assert plan.critical_path == ["a", "b", "d"]
        assert plan.task_order[0] == "a"
        assert plan.task_order[-1] == "d"
        assert len(plan.tasks) == 4

    def test_plan_empty(self):
        plan = TaskPlanner().plan()
        assert plan.tasks == []
        assert plan.task_order == []
        assert plan.critical_path == []
        assert plan.total_duration == 0.0


# ----------------------------------------------------------------------
# validate
# ----------------------------------------------------------------------


class TestValidate:
    def test_valid(self):
        ok, errors = _diamond_planner().validate()
        assert ok is True
        assert errors == []

    def test_missing_dep(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0, ["ghost"])
        ok, errors = p.validate()
        assert ok is False
        assert any("ghost" in e for e in errors)

    def test_cycle(self):
        p = TaskPlanner()
        p.add_task("a", "A", 1.0, ["b"])
        p.add_task("b", "B", 1.0, ["a"])
        ok, errors = p.validate()
        assert ok is False
        assert any("ycle" in e for e in errors)

    def test_empty_is_valid(self):
        ok, errors = TaskPlanner().validate()
        assert ok is True
        assert errors == []


# ----------------------------------------------------------------------
# task_count
# ----------------------------------------------------------------------


class TestTaskCount:
    def test_zero(self):
        assert TaskPlanner().task_count == 0

    def test_after_adds(self):
        p = _diamond_planner()
        assert p.task_count == 4


# ----------------------------------------------------------------------
# clear
# ----------------------------------------------------------------------


class TestClear:
    def test_clear_empties(self):
        p = _diamond_planner()
        p.clear()
        assert p.task_count == 0
        assert p.ready_tasks() == []


# ----------------------------------------------------------------------
# mark_done
# ----------------------------------------------------------------------


class TestMarkDone:
    def test_marks_done(self):
        p = _linear_planner()
        assert p.mark_done("a", now=2.0) is True
        t = p.get_task("a")
        assert t.status == TaskStatus.DONE
        assert t.completed_at == 2.0

    def test_unknown_returns_false(self):
        assert TaskPlanner().mark_done("nope") is False


# ----------------------------------------------------------------------
# progress / complete_count
# ----------------------------------------------------------------------


class TestProgress:
    def test_zero_for_empty(self):
        assert TaskPlanner().progress == 0.0
        assert TaskPlanner().complete_count == 0

    def test_zero_when_none_done(self):
        p = _linear_planner()
        assert p.progress == 0.0
        assert p.complete_count == 0

    def test_partial(self):
        p = _linear_planner()
        p.mark_done("a")
        assert p.complete_count == 1
        assert p.progress == pytest.approx(1.0 / 3.0)

    def test_full(self):
        p = _linear_planner()
        p.mark_done("a")
        p.mark_done("b")
        p.mark_done("c")
        assert p.complete_count == 3
        assert p.progress == 1.0


# ----------------------------------------------------------------------
# Edge cases
# ----------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_plan_methods(self):
        p = TaskPlanner()
        assert p.topological_order() == []
        assert p.critical_path() == []
        assert p.total_duration() == 0.0
        assert p.ready_tasks() == []
        assert p.blocked_tasks() == []

    def test_single_task(self):
        p = TaskPlanner()
        p.add_task("solo", "Solo", 4.5)
        assert p.topological_order() == ["solo"]
        assert p.critical_path() == ["solo"]
        assert p.total_duration() == pytest.approx(4.5)
        assert [t.task_id for t in p.ready_tasks()] == ["solo"]

    def test_parallel_branches(self):
        # Fan-out: a -> b, a -> c, a -> d ; all leaves
        p = TaskPlanner()
        p.add_task("a", "A", 1.0)
        p.add_task("b", "B", 2.0, ["a"])
        p.add_task("c", "C", 5.0, ["a"])
        p.add_task("d", "D", 3.0, ["a"])
        assert p.critical_path() == ["a", "c"]
        assert p.total_duration() == pytest.approx(6.0)

    def test_zero_duration_critical_path(self):
        p = TaskPlanner()
        p.add_task("a", "A", 0.0)
        p.add_task("b", "B", 0.0, ["a"])
        assert p.critical_path() == ["a", "b"]
        assert p.total_duration() == 0.0

    def test_mark_done_then_progress(self):
        p = _diamond_planner()
        p.mark_done("a")
        p.mark_done("b")
        assert p.progress == 0.5
