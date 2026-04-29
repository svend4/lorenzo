"""Тесты plan-and-execute mode."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.agent import (
    Subtask, SubtaskResult, Plan, PlanExecuteResult,
    heuristic_planner, execute_plan, plan_and_execute,
)


# ---- dataclasses ----

def test_subtask_defaults():
    s = Subtask(id=1, description="x")
    assert s.depends_on == []
    assert s.completed is False


def test_subtask_result_ok_property():
    sr = SubtaskResult(subtask_id=1, description="x", output="ok")
    assert sr.ok
    sr2 = SubtaskResult(subtask_id=2, description="x", error="boom")
    assert not sr2.ok


def test_plan_to_markdown():
    p = Plan(task="do stuff", subtasks=[
        Subtask(id=1, description="step one"),
        Subtask(id=2, description="step two", depends_on=[1]),
    ], rationale="why")
    md = p.to_markdown()
    assert "Plan: do stuff" in md
    assert "step one" in md
    assert "step two" in md
    assert "depends" in md


def test_plan_execute_result_ok():
    r = PlanExecuteResult(task="x", plan=Plan(task="x"))
    r.subtask_results = [SubtaskResult(subtask_id=1, description="a", output="ok")]
    assert r.ok


def test_plan_execute_result_not_ok_with_error():
    r = PlanExecuteResult(task="x", plan=Plan(task="x"))
    r.subtask_results = [SubtaskResult(subtask_id=1, description="a", error="!")]
    assert not r.ok


# ---- heuristic_planner ----

def test_heuristic_planner_numbered():
    p = heuristic_planner("1) первое 2) второе 3) третье")
    assert len(p.subtasks) == 3
    assert "первое" in p.subtasks[0].description
    assert "Numbered" in p.rationale


def test_heuristic_planner_connector_split():
    p = heuristic_planner("сначала А, потом Б")
    assert len(p.subtasks) == 2


def test_heuristic_planner_and_split():
    p = heuristic_planner("изучи A и сравни с B")
    assert len(p.subtasks) == 2
    # second depends on first (and-split)
    assert 1 in p.subtasks[1].depends_on


def test_heuristic_planner_single():
    p = heuristic_planner("что такое X?")
    assert len(p.subtasks) == 1
    assert "Single" in p.rationale


def test_heuristic_planner_short_text():
    p = heuristic_planner("hello")
    assert len(p.subtasks) == 1


# ---- execute_plan / plan_and_execute ----

def test_execute_plan_echo_executor():
    """Без agent — echo-executor возвращает описание."""
    plan = Plan(task="t", subtasks=[
        Subtask(id=1, description="step A"),
        Subtask(id=2, description="step B"),
    ])
    r = execute_plan(plan)
    assert r.ok
    assert len(r.subtask_results) == 2
    assert "step B" in r.final_answer
    assert r.halted_reason == "completed"


def test_execute_plan_with_failing_agent():
    class FailAgent:
        def run(self, task):
            raise RuntimeError("agent down")
    plan = Plan(task="t", subtasks=[Subtask(id=1, description="x")])
    r = execute_plan(plan, agent=FailAgent())
    assert not r.ok
    assert "subtask 1" in r.halted_reason
    assert "RuntimeError" in r.subtask_results[0].error


def test_execute_plan_dependencies_pass_prefix():
    """Subtask с depends_on должен получить контекст предыдущего."""
    seen_tasks = []
    class CapturingAgent:
        def run(self, task):
            seen_tasks.append(task)
            from docstoolkit.agent import AgentResult
            return AgentResult(task=task, answer=f"answered: {task[:30]}")
    plan = Plan(task="t", subtasks=[
        Subtask(id=1, description="step A"),
        Subtask(id=2, description="step B", depends_on=[1]),
    ])
    execute_plan(plan, agent=CapturingAgent())
    # second invocation has prefix from subtask 1
    assert "subtask 1" in seen_tasks[1]


def test_plan_and_execute_end_to_end():
    r = plan_and_execute("1) one 2) two")
    assert r.ok
    assert len(r.subtask_results) == 2


def test_execute_plan_on_subtask_callback():
    calls = []
    plan = Plan(task="t", subtasks=[
        Subtask(id=1, description="a"),
        Subtask(id=2, description="b"),
    ])
    execute_plan(plan, on_subtask=lambda st, sr: calls.append((st.id, sr.ok)))
    assert calls == [(1, True), (2, True)]


def test_plan_execute_result_to_markdown():
    plan = Plan(task="task", subtasks=[Subtask(id=1, description="a")])
    r = execute_plan(plan)
    md = r.to_markdown()
    assert "Plan-and-execute: task" in md
    assert "Execution trace" in md
    assert "Final answer" in md


def test_execute_plan_replan_on_failure():
    """При max_replans>0 и replanner — при failure вызывается replanner."""
    attempts = {"agent": 0, "replan": 0}

    class FlakyAgent:
        def run(self, task):
            attempts["agent"] += 1
            if attempts["agent"] == 1:
                raise RuntimeError("first call fails")
            from docstoolkit.agent import AgentResult
            return AgentResult(task=task, answer="recovered")

    def replanner(task):
        attempts["replan"] += 1
        return Plan(task=task, subtasks=[Subtask(id=1, description="alt")])

    plan = Plan(task="t", subtasks=[Subtask(id=1, description="orig")])
    r = execute_plan(plan, agent=FlakyAgent(),
                      max_replans=1, replanner=replanner)
    assert attempts["replan"] == 1
    assert r.replans == 1
