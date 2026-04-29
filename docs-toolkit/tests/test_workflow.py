"""Тесты workflow DAG runner."""
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.workflow import Workflow, Step, run, run_async
from docstoolkit.workflow.dag import (
    StepResult, WorkflowResult, _topo_sort, _level_sort,
    _resolve_inputs, _step_deps,
)


# ---- dataclass / props ----

def test_step_defaults():
    s = Step(name="x", fn=lambda: 1)
    assert s.on_error == "fail"
    assert s.max_retries == 0


def test_step_result_ok_property():
    sr = StepResult(name="x", output=1)
    assert sr.ok
    sr2 = StepResult(name="x", error="boom")
    assert not sr2.ok
    sr3 = StepResult(name="x", skipped=True)
    assert not sr3.ok


def test_workflow_result_ok_property():
    r = WorkflowResult(workflow="x")
    assert r.ok
    r.failed.append("step1")
    assert not r.ok


def test_workflow_result_step_lookup():
    r = WorkflowResult(workflow="x", steps=[
        StepResult(name="a", output=1),
        StepResult(name="b", output=2),
    ])
    assert r.step("a").output == 1
    assert r.step("b").output == 2
    assert r.step("missing") is None


# ---- topo / level sort ----

def test_topo_sort_linear():
    s = [
        Step(name="a", fn=lambda: 1),
        Step(name="b", fn=lambda x: x, inputs={"x": "$.a.output"}),
        Step(name="c", fn=lambda x: x, inputs={"x": "$.b.output"}),
    ]
    order = _topo_sort(s)
    assert [x.name for x in order] == ["a", "b", "c"]


def test_topo_sort_cycle_returns_none():
    s = [
        Step(name="a", fn=lambda x: x, inputs={"x": "$.b.output"}),
        Step(name="b", fn=lambda x: x, inputs={"x": "$.a.output"}),
    ]
    assert _topo_sort(s) is None


def test_level_sort_groups_independent():
    s = [
        Step(name="a", fn=lambda: 1),
        Step(name="b", fn=lambda: 2),
        Step(name="c", fn=lambda x, y: x + y,
             inputs={"x": "$.a.output", "y": "$.b.output"}),
    ]
    levels = _level_sort(s)
    assert len(levels) == 2
    names_l0 = {x.name for x in levels[0]}
    assert names_l0 == {"a", "b"}
    assert [x.name for x in levels[1]] == ["c"]


def test_level_sort_cycle_returns_none():
    s = [
        Step(name="a", fn=lambda x: x, inputs={"x": "$.b.output"}),
        Step(name="b", fn=lambda x: x, inputs={"x": "$.a.output"}),
    ]
    assert _level_sort(s) is None


# ---- input resolution ----

def test_resolve_inputs_context():
    out = _resolve_inputs({"q": "$.question"}, {"question": "x"}, {})
    assert out["q"] == "x"


def test_resolve_inputs_step_output():
    out = _resolve_inputs({"p": "$.fetch.output"}, {}, {"fetch": [1, 2]})
    assert out["p"] == [1, 2]


def test_resolve_inputs_constant():
    out = _resolve_inputs({"k": 42, "name": "literal"}, {}, {})
    assert out["k"] == 42
    assert out["name"] == "literal"


def test_step_deps_empty():
    s = Step(name="x", fn=lambda: 1)
    assert _step_deps(s) == set()


def test_step_deps_collects_step_refs():
    s = Step(name="x", fn=lambda: 1, inputs={"a": "$.s1.output", "b": "$.s2.output", "c": "$.ctx"})
    deps = _step_deps(s)
    assert deps == {"s1", "s2"}


# ---- run sync ----

def test_run_simple_pipeline():
    wf = Workflow(name="t", steps=[
        Step("a", fn=lambda: 10),
        Step("b", fn=lambda x: x + 1, inputs={"x": "$.a.output"}),
    ])
    r = run(wf, {})
    assert r.ok
    assert r.outputs["b"] == 11


def test_run_uses_context():
    wf = Workflow(name="t", steps=[
        Step("greet", fn=lambda name: f"hi {name}", inputs={"name": "$.who"}),
    ])
    r = run(wf, {"who": "Alice"})
    assert r.outputs["greet"] == "hi Alice"


def test_run_fail_on_error_aborts():
    wf = Workflow(name="t", steps=[
        Step("good", fn=lambda: 1),
        Step("bad", fn=lambda: (_ for _ in ()).throw(ValueError("boom"))),
        Step("never", fn=lambda: "x"),
    ])
    r = run(wf, {})
    assert "bad" in r.failed
    # never должен быть skipped
    skipped = [s for s in r.steps if s.skipped]
    assert any(s.name == "never" for s in skipped)


def test_run_skip_on_error_continues():
    wf = Workflow(name="t", steps=[
        Step("bad", fn=lambda: (_ for _ in ()).throw(RuntimeError("x")),
             on_error="skip"),
        Step("good", fn=lambda: 1),
    ])
    r = run(wf, {})
    assert "bad" in r.failed
    assert r.outputs.get("good") == 1


def test_run_cycle_detected():
    wf = Workflow(name="cyc", steps=[
        Step("x", fn=lambda y: y, inputs={"y": "$.y.output"}),
        Step("y", fn=lambda x: x, inputs={"x": "$.x.output"}),
    ])
    r = run(wf, {})
    assert "__cycle__" in r.failed


# ---- run_async ----

def test_run_async_parallel_independent_steps():
    """Три независимых шага по 30мс — должны идти параллельно."""
    def slow(): time.sleep(0.03); return "x"
    wf = Workflow(name="par", steps=[
        Step("a", fn=slow),
        Step("b", fn=slow),
        Step("c", fn=slow),
    ])
    t0 = time.time()
    r = run_async(wf, {}, max_workers=4)
    elapsed_ms = (time.time() - t0) * 1000
    assert r.ok
    assert elapsed_ms < 90  # вместо 90 sync
    assert all(r.outputs.get(n) == "x" for n in ("a", "b", "c"))


def test_run_async_respects_dependencies():
    wf = Workflow(name="dep", steps=[
        Step("a", fn=lambda: 1),
        Step("b", fn=lambda x: x + 10, inputs={"x": "$.a.output"}),
    ])
    r = run_async(wf, {})
    assert r.outputs["b"] == 11


def test_run_async_fail_aborts_downstream():
    wf = Workflow(name="x", steps=[
        Step("bad", fn=lambda: (_ for _ in ()).throw(ValueError("boom"))),
        Step("after", fn=lambda x: x, inputs={"x": "$.bad.output"}),
    ])
    r = run_async(wf, {})
    assert "bad" in r.failed
    after_sr = r.step("after")
    assert after_sr is not None
    assert after_sr.skipped


# ---- report ----

def test_workflow_result_report_markdown():
    wf = Workflow(name="rpt", steps=[
        Step("a", fn=lambda: "ok"),
    ])
    r = run(wf, {})
    md = r.report()
    assert "Workflow: rpt" in md
    assert "`a`" in md
    assert "ok" in md or "str" in md
