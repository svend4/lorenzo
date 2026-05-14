"""Tests for the E48 Workflow engine (step.py + engine.py).

Also preserves tests for the legacy DAG runner (dag.py).
"""
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.workflow.step import StepStatus, StepResult, WorkflowStep
from docstoolkit.workflow.engine import WorkflowConfig, WorkflowResult, WorkflowEngine


# ===========================================================================
# StepStatus
# ===========================================================================

def test_step_status_enum_members():
    assert StepStatus.PENDING.value == "pending"
    assert StepStatus.RUNNING.value == "running"
    assert StepStatus.SUCCESS.value == "success"
    assert StepStatus.FAILED.value == "failed"
    assert StepStatus.SKIPPED.value == "skipped"


def test_step_status_distinct():
    statuses = [
        StepStatus.PENDING, StepStatus.RUNNING, StepStatus.SUCCESS,
        StepStatus.FAILED, StepStatus.SKIPPED,
    ]
    assert len(set(statuses)) == 5


# ===========================================================================
# StepResult
# ===========================================================================

def test_step_result_is_success_true():
    r = StepResult(step_id="abc", status=StepStatus.SUCCESS, output={})
    assert r.is_success() is True


def test_step_result_is_success_false_failed():
    r = StepResult(step_id="abc", status=StepStatus.FAILED, output={}, error="boom")
    assert r.is_success() is False


def test_step_result_is_success_false_skipped():
    r = StepResult(step_id="abc", status=StepStatus.SKIPPED, output={})
    assert r.is_success() is False


def test_step_result_is_success_false_pending():
    r = StepResult(step_id="abc", status=StepStatus.PENDING, output={})
    assert r.is_success() is False


def test_step_result_is_success_false_running():
    r = StepResult(step_id="abc", status=StepStatus.RUNNING, output={})
    assert r.is_success() is False


def test_step_result_default_error_empty():
    r = StepResult(step_id="x", status=StepStatus.SUCCESS, output={})
    assert r.error == ""


def test_step_result_default_duration_zero():
    r = StepResult(step_id="x", status=StepStatus.SUCCESS, output={})
    assert r.duration_ms == 0.0


def test_step_result_stores_output():
    r = StepResult(step_id="x", status=StepStatus.SUCCESS, output={"key": "val"})
    assert r.output["key"] == "val"


def test_step_result_stores_error():
    r = StepResult(step_id="x", status=StepStatus.FAILED, output={}, error="oops")
    assert r.error == "oops"


def test_step_result_stores_duration():
    r = StepResult(step_id="x", status=StepStatus.SUCCESS, output={}, duration_ms=42.5)
    assert r.duration_ms == 42.5


# ===========================================================================
# WorkflowStep defaults and structure
# ===========================================================================

def test_workflow_step_auto_step_id():
    s = WorkflowStep(name="test", handler=lambda ctx: {})
    assert len(s.step_id) == 8
    assert s.step_id.isalnum()


def test_workflow_step_unique_step_ids():
    s1 = WorkflowStep(name="a", handler=lambda ctx: {})
    s2 = WorkflowStep(name="b", handler=lambda ctx: {})
    assert s1.step_id != s2.step_id


def test_workflow_step_default_retry_count():
    s = WorkflowStep(name="x", handler=lambda ctx: {})
    assert s.retry_count == 0


def test_workflow_step_default_skip_on_failure():
    s = WorkflowStep(name="x", handler=lambda ctx: {})
    assert s.skip_on_failure is False


def test_workflow_step_default_dependencies_empty():
    s = WorkflowStep(name="x", handler=lambda ctx: {})
    assert s.dependencies == []


def test_workflow_step_dependencies_not_shared():
    """Mutable default must be isolated per instance."""
    s1 = WorkflowStep(name="a", handler=lambda ctx: {})
    s2 = WorkflowStep(name="b", handler=lambda ctx: {})
    s1.dependencies.append("x")
    assert s2.dependencies == []


def test_workflow_step_custom_step_id():
    s = WorkflowStep(name="x", handler=lambda ctx: {}, step_id="myid1234")
    assert s.step_id == "myid1234"


# ===========================================================================
# WorkflowStep.execute — success path
# ===========================================================================

def test_execute_success_returns_success_status():
    s = WorkflowStep(name="x", handler=lambda ctx: {"v": 1})
    r = s.execute({})
    assert r.status == StepStatus.SUCCESS


def test_execute_success_is_success():
    s = WorkflowStep(name="x", handler=lambda ctx: {"v": 1})
    r = s.execute({})
    assert r.is_success()


def test_execute_success_output_dict():
    s = WorkflowStep(name="x", handler=lambda ctx: {"answer": 42})
    r = s.execute({})
    assert r.output == {"answer": 42}


def test_execute_non_dict_output_wrapped():
    s = WorkflowStep(name="x", handler=lambda ctx: 99)
    r = s.execute({})
    assert r.output == {"result": 99}


def test_execute_none_output_wrapped():
    s = WorkflowStep(name="x", handler=lambda ctx: None)
    r = s.execute({})
    assert r.output == {"result": None}


def test_execute_passes_context_to_handler():
    captured = {}

    def handler(ctx):
        captured.update(ctx)
        return {}

    s = WorkflowStep(name="x", handler=handler)
    s.execute({"foo": "bar"})
    assert captured["foo"] == "bar"


def test_execute_returns_step_id():
    s = WorkflowStep(name="x", handler=lambda ctx: {}, step_id="deadbeef")
    r = s.execute({})
    assert r.step_id == "deadbeef"


def test_execute_success_error_empty():
    s = WorkflowStep(name="x", handler=lambda ctx: {})
    r = s.execute({})
    assert r.error == ""


def test_execute_tracks_duration():
    def slow(ctx):
        time.sleep(0.02)
        return {}

    s = WorkflowStep(name="x", handler=slow)
    r = s.execute({})
    assert r.duration_ms >= 15.0  # at least 15 ms


def test_execute_duration_is_float():
    s = WorkflowStep(name="x", handler=lambda ctx: {})
    r = s.execute({})
    assert isinstance(r.duration_ms, float)


# ===========================================================================
# WorkflowStep.execute — failure path
# ===========================================================================

def test_execute_exception_returns_failed_status():
    def boom(ctx):
        raise ValueError("bad")

    s = WorkflowStep(name="x", handler=boom)
    r = s.execute({})
    assert r.status == StepStatus.FAILED


def test_execute_exception_not_is_success():
    def boom(ctx):
        raise RuntimeError("oops")

    s = WorkflowStep(name="x", handler=boom)
    r = s.execute({})
    assert not r.is_success()


def test_execute_exception_error_contains_message():
    def boom(ctx):
        raise ValueError("specific error text")

    s = WorkflowStep(name="x", handler=boom)
    r = s.execute({})
    assert "specific error text" in r.error


def test_execute_exception_error_contains_type():
    def boom(ctx):
        raise TypeError("wrong type")

    s = WorkflowStep(name="x", handler=boom)
    r = s.execute({})
    assert "TypeError" in r.error


def test_execute_exception_output_empty_dict():
    def boom(ctx):
        raise Exception("x")

    s = WorkflowStep(name="x", handler=boom)
    r = s.execute({})
    assert r.output == {}


def test_execute_exception_tracks_duration():
    def slow_boom(ctx):
        time.sleep(0.01)
        raise RuntimeError("late failure")

    s = WorkflowStep(name="x", handler=slow_boom)
    r = s.execute({})
    assert r.duration_ms >= 5.0


# ===========================================================================
# WorkflowConfig defaults
# ===========================================================================

def test_workflow_config_defaults():
    c = WorkflowConfig()
    assert c.stop_on_failure is True
    assert c.max_retries == 0
    assert c.timeout_ms == 0


def test_workflow_config_custom():
    c = WorkflowConfig(stop_on_failure=False, max_retries=3, timeout_ms=500.0)
    assert c.stop_on_failure is False
    assert c.max_retries == 3
    assert c.timeout_ms == 500.0


# ===========================================================================
# WorkflowResult
# ===========================================================================

def test_workflow_result_failed_steps_empty_when_all_succeed():
    r = WorkflowResult(
        workflow_id="wf1",
        steps=[
            StepResult(step_id="a", status=StepStatus.SUCCESS, output={}),
            StepResult(step_id="b", status=StepStatus.SUCCESS, output={}),
        ],
        success=True,
    )
    assert r.failed_steps() == []


def test_workflow_result_failed_steps_returns_failed():
    r = WorkflowResult(
        workflow_id="wf1",
        steps=[
            StepResult(step_id="a", status=StepStatus.SUCCESS, output={}),
            StepResult(step_id="b", status=StepStatus.FAILED, output={}, error="x"),
        ],
        success=False,
    )
    assert len(r.failed_steps()) == 1
    assert r.failed_steps()[0].step_id == "b"


def test_workflow_result_succeeded_steps_returns_successes():
    r = WorkflowResult(
        workflow_id="wf1",
        steps=[
            StepResult(step_id="a", status=StepStatus.SUCCESS, output={}),
            StepResult(step_id="b", status=StepStatus.FAILED, output={}, error="x"),
            StepResult(step_id="c", status=StepStatus.SUCCESS, output={}),
        ],
        success=False,
    )
    ids = [s.step_id for s in r.succeeded_steps()]
    assert ids == ["a", "c"]


def test_workflow_result_succeeded_does_not_include_skipped():
    r = WorkflowResult(
        workflow_id="wf1",
        steps=[
            StepResult(step_id="a", status=StepStatus.SUCCESS, output={}),
            StepResult(step_id="b", status=StepStatus.SKIPPED, output={}),
        ],
        success=True,
    )
    ids = [s.step_id for s in r.succeeded_steps()]
    assert ids == ["a"]


def test_workflow_result_total_duration_ms_sum():
    r = WorkflowResult(
        workflow_id="wf1",
        steps=[
            StepResult(step_id="a", status=StepStatus.SUCCESS, output={}, duration_ms=10.0),
            StepResult(step_id="b", status=StepStatus.SUCCESS, output={}, duration_ms=20.5),
            StepResult(step_id="c", status=StepStatus.FAILED, output={}, duration_ms=5.0),
        ],
        success=False,
    )
    assert r.total_duration_ms() == pytest.approx(35.5)


def test_workflow_result_total_duration_zero_when_no_steps():
    r = WorkflowResult(workflow_id="wf1", steps=[], success=True)
    assert r.total_duration_ms() == 0.0


# ===========================================================================
# WorkflowEngine basics
# ===========================================================================

def test_engine_step_count_zero_initially():
    e = WorkflowEngine()
    assert e.step_count() == 0


def test_engine_step_count_after_add():
    e = WorkflowEngine()
    e.add_step(WorkflowStep(name="a", handler=lambda ctx: {}))
    assert e.step_count() == 1


def test_engine_step_count_multiple():
    e = WorkflowEngine()
    for i in range(5):
        e.add_step(WorkflowStep(name=f"s{i}", handler=lambda ctx: {}))
    assert e.step_count() == 5


def test_engine_run_returns_workflow_result():
    e = WorkflowEngine()
    r = e.run()
    assert isinstance(r, WorkflowResult)


def test_engine_run_success_no_steps():
    e = WorkflowEngine()
    r = e.run()
    assert r.success is True


def test_engine_run_single_step_success():
    e = WorkflowEngine()
    e.add_step(WorkflowStep(name="a", handler=lambda ctx: {"x": 1}))
    r = e.run()
    assert r.success is True
    assert len(r.steps) == 1
    assert r.steps[0].is_success()


def test_engine_run_workflow_id_assigned():
    e = WorkflowEngine()
    r = e.run()
    assert r.workflow_id != ""
    assert len(r.workflow_id) > 0


def test_engine_run_sequential_order():
    order = []

    def make_handler(name):
        def h(ctx):
            order.append(name)
            return {}
        return h

    e = WorkflowEngine()
    e.add_step(WorkflowStep(name="first", handler=make_handler("first")))
    e.add_step(WorkflowStep(name="second", handler=make_handler("second")))
    e.add_step(WorkflowStep(name="third", handler=make_handler("third")))
    e.run()
    assert order == ["first", "second", "third"]


# ===========================================================================
# WorkflowEngine: context passing and merging
# ===========================================================================

def test_engine_passes_initial_context():
    received = {}

    def handler(ctx):
        received.update(ctx)
        return {}

    e = WorkflowEngine()
    e.add_step(WorkflowStep(name="a", handler=handler))
    e.run({"key": "value"})
    assert received["key"] == "value"


def test_engine_merges_step_output_into_context():
    received = {}

    def step_b(ctx):
        received.update(ctx)
        return {}

    e = WorkflowEngine()
    e.add_step(WorkflowStep(name="a", handler=lambda ctx: {"from_a": 42}))
    e.add_step(WorkflowStep(name="b", handler=step_b))
    e.run()
    assert received.get("from_a") == 42


def test_engine_context_accumulates_across_steps():
    e = WorkflowEngine()
    e.add_step(WorkflowStep(name="s1", handler=lambda ctx: {"s1_val": 1}))
    e.add_step(WorkflowStep(name="s2", handler=lambda ctx: {"s2_val": ctx.get("s1_val", 0) + 10}))
    e.add_step(WorkflowStep(name="s3", handler=lambda ctx: {"total": ctx.get("s2_val", 0) + ctx.get("s1_val", 0)}))
    r = e.run()
    assert r.context.get("total") == 12


def test_engine_result_context_reflects_final_state():
    e = WorkflowEngine()
    e.add_step(WorkflowStep(name="a", handler=lambda ctx: {"answer": 99}))
    r = e.run({"seed": 0})
    assert r.context["answer"] == 99
    assert r.context["seed"] == 0


# ===========================================================================
# WorkflowEngine: stop_on_failure
# ===========================================================================

def test_engine_stop_on_failure_true_stops_after_failure():
    executed = []

    def make_handler(name):
        def h(ctx):
            executed.append(name)
            return {}
        return h

    e = WorkflowEngine(WorkflowConfig(stop_on_failure=True))
    e.add_step(WorkflowStep(name="ok", handler=make_handler("ok")))
    e.add_step(WorkflowStep(name="fail", handler=lambda ctx: (_ for _ in ()).throw(RuntimeError("boom"))))
    e.add_step(WorkflowStep(name="never", handler=make_handler("never")))
    r = e.run()
    assert r.success is False
    assert "never" not in executed


def test_engine_stop_on_failure_true_skips_remaining():
    e = WorkflowEngine(WorkflowConfig(stop_on_failure=True))
    e.add_step(WorkflowStep(name="bad", handler=lambda ctx: (_ for _ in ()).throw(ValueError("x"))))
    e.add_step(WorkflowStep(name="skip_me", handler=lambda ctx: {}))
    r = e.run()
    skipped = [s for s in r.steps if s.status == StepStatus.SKIPPED]
    assert len(skipped) >= 1


def test_engine_stop_on_failure_false_continues():
    executed = []

    def fail(ctx):
        raise RuntimeError("hard fail")

    def after(ctx):
        executed.append("after")
        return {}

    e = WorkflowEngine(WorkflowConfig(stop_on_failure=False))
    e.add_step(WorkflowStep(name="bad", handler=fail))
    e.add_step(WorkflowStep(name="after", handler=after))
    r = e.run()
    assert "after" in executed


def test_engine_stop_on_failure_false_success_false_on_any_failure():
    e = WorkflowEngine(WorkflowConfig(stop_on_failure=False))
    e.add_step(WorkflowStep(name="bad", handler=lambda ctx: (_ for _ in ()).throw(RuntimeError("x"))))
    e.add_step(WorkflowStep(name="ok", handler=lambda ctx: {}))
    r = e.run()
    assert r.success is False


# ===========================================================================
# WorkflowEngine: skip_on_failure
# ===========================================================================

def test_skip_on_failure_does_not_stop_engine():
    executed = []

    e = WorkflowEngine(WorkflowConfig(stop_on_failure=True))
    e.add_step(WorkflowStep(
        name="soft_fail",
        handler=lambda ctx: (_ for _ in ()).throw(ValueError("meh")),
        skip_on_failure=True,
    ))
    e.add_step(WorkflowStep(
        name="continues",
        handler=lambda ctx: (executed.append("continues"), {})[1],
    ))
    r = e.run()
    assert "continues" in executed


def test_skip_on_failure_step_marked_skipped():
    e = WorkflowEngine()
    e.add_step(WorkflowStep(
        name="soft",
        handler=lambda ctx: (_ for _ in ()).throw(ValueError("x")),
        skip_on_failure=True,
    ))
    r = e.run()
    assert r.steps[0].status == StepStatus.SKIPPED


def test_skip_on_failure_result_success_unchanged_by_skipped():
    """A skip_on_failure step should not mark result.success=False."""
    e = WorkflowEngine()
    e.add_step(WorkflowStep(
        name="soft",
        handler=lambda ctx: (_ for _ in ()).throw(ValueError("x")),
        skip_on_failure=True,
    ))
    r = e.run()
    # No hard failure → result.success remains True
    assert r.success is True


# ===========================================================================
# WorkflowEngine: retry
# ===========================================================================

def test_engine_retries_on_failure_and_succeeds():
    call_count = [0]

    def flaky(ctx):
        call_count[0] += 1
        if call_count[0] < 3:
            raise RuntimeError("not yet")
        return {"done": True}

    e = WorkflowEngine(WorkflowConfig(max_retries=3))
    e.add_step(WorkflowStep(name="flaky", handler=flaky))
    r = e.run()
    assert r.success is True
    assert call_count[0] == 3


def test_engine_retries_exhausted_marks_failed():
    call_count = [0]

    def always_fail(ctx):
        call_count[0] += 1
        raise RuntimeError("always")

    e = WorkflowEngine(WorkflowConfig(max_retries=2))
    e.add_step(WorkflowStep(name="bad", handler=always_fail))
    r = e.run()
    assert r.success is False
    assert call_count[0] == 3  # 1 original + 2 retries


def test_step_retry_count_overrides_config():
    call_count = [0]

    def flaky(ctx):
        call_count[0] += 1
        if call_count[0] < 2:
            raise RuntimeError("retry me")
        return {}

    e = WorkflowEngine(WorkflowConfig(max_retries=0))
    e.add_step(WorkflowStep(name="flaky", handler=flaky, retry_count=2))
    r = e.run()
    assert r.success is True
    assert call_count[0] == 2


# ===========================================================================
# WorkflowEngine: dependencies
# ===========================================================================

def test_dependencies_step_waits_for_predecessor():
    order = []

    def make_handler(name):
        def h(ctx):
            order.append(name)
            return {}
        return h

    e = WorkflowEngine()
    # Add b before a but declare dependency on a
    e.add_step(WorkflowStep(name="b", handler=make_handler("b"), dependencies=["a"]))
    e.add_step(WorkflowStep(name="a", handler=make_handler("a")))
    e.run()
    assert order.index("a") < order.index("b")


def test_dependencies_skipped_when_dep_fails():
    e = WorkflowEngine(WorkflowConfig(stop_on_failure=False))
    e.add_step(WorkflowStep(name="a", handler=lambda ctx: (_ for _ in ()).throw(RuntimeError("x"))))
    e.add_step(WorkflowStep(name="b", handler=lambda ctx: {}, dependencies=["a"]))
    r = e.run()
    b_result = next((s for s in r.steps if s.step_id == e._steps[1].step_id), None)
    assert b_result is not None
    assert b_result.status == StepStatus.SKIPPED


def test_dependencies_satisfied_step_runs():
    e = WorkflowEngine()
    e.add_step(WorkflowStep(name="a", handler=lambda ctx: {"a_done": True}))
    e.add_step(WorkflowStep(name="b", handler=lambda ctx: {"b_done": True}, dependencies=["a"]))
    r = e.run()
    assert r.success is True
    assert len(r.succeeded_steps()) == 2


# ===========================================================================
# WorkflowEngine: integration / end-to-end
# ===========================================================================

def test_full_pipeline_three_steps():
    e = WorkflowEngine()
    e.add_step(WorkflowStep(name="fetch", handler=lambda ctx: {"data": [1, 2, 3]}))
    e.add_step(WorkflowStep(name="process", handler=lambda ctx: {"total": sum(ctx["data"])}))
    e.add_step(WorkflowStep(name="report", handler=lambda ctx: {"message": f"sum={ctx['total']}"}))
    r = e.run()
    assert r.success is True
    assert r.context["message"] == "sum=6"


def test_initial_context_available_throughout():
    e = WorkflowEngine()
    e.add_step(WorkflowStep(name="a", handler=lambda ctx: {"doubled": ctx["seed"] * 2}))
    e.add_step(WorkflowStep(name="b", handler=lambda ctx: {"quadrupled": ctx["doubled"] * 2}))
    r = e.run({"seed": 5})
    assert r.context["quadrupled"] == 20


def test_multiple_failures_with_stop_on_failure_false():
    e = WorkflowEngine(WorkflowConfig(stop_on_failure=False))
    e.add_step(WorkflowStep(name="f1", handler=lambda ctx: (_ for _ in ()).throw(ValueError("1"))))
    e.add_step(WorkflowStep(name="f2", handler=lambda ctx: (_ for _ in ()).throw(ValueError("2"))))
    r = e.run()
    assert r.success is False
    assert len(r.failed_steps()) == 2


def test_engine_no_steps_empty_result():
    e = WorkflowEngine()
    r = e.run({"x": 1})
    assert r.steps == []
    assert r.success is True
    assert r.total_duration_ms() == 0.0
