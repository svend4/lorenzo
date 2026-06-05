"""Tests for the E101 workflow_engine module.

Covers:
- StepStatus enum values and identity
- StepConfig / StepResult / WorkflowConfig dataclass construction
- WorkflowEngine.run — success paths (single step, multi-step)
- Context propagation between steps
- context["_results"] population
- Step failure stops workflow; remaining steps → SKIPPED
- max_retries > 0: success on retry
- max_retries > 0: all retries exhausted → FAILED
- skip_on_failure=True continues after failure
- WorkflowResult.success property
- WorkflowResult.step_results property
- WorkflowResult.get() lookup
- WorkflowEngine.validate() — all error conditions
- Edge cases: empty steps list, output accessible to later steps
- attempts count correctness
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.workflow_engine import (
    StepStatus,
    StepConfig,
    StepResult,
    WorkflowConfig,
    WorkflowResult,
    WorkflowEngine,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ok_step(name="step", value=None):
    """Return a StepConfig whose fn succeeds and returns *value*."""
    def fn(ctx):
        return value
    fn.__name__ = name
    return StepConfig(name=name, fn=fn)


def fail_step(name="fail", exc=None):
    """Return a StepConfig whose fn always raises."""
    err = exc or RuntimeError("boom")
    def fn(ctx):
        raise err
    fn.__name__ = name
    return StepConfig(name=name, fn=fn)


def make_engine():
    return WorkflowEngine()


# ---------------------------------------------------------------------------
# StepStatus
# ---------------------------------------------------------------------------

class TestStepStatus:
    def test_pending_value(self):
        assert StepStatus.PENDING == "pending"

    def test_running_value(self):
        assert StepStatus.RUNNING == "running"

    def test_done_value(self):
        assert StepStatus.DONE == "done"

    def test_failed_value(self):
        assert StepStatus.FAILED == "failed"

    def test_skipped_value(self):
        assert StepStatus.SKIPPED == "skipped"

    def test_retrying_value(self):
        assert StepStatus.RETRYING == "retrying"

    def test_all_members_distinct(self):
        all_members = list(StepStatus)
        assert len(set(all_members)) == len(all_members)

    def test_is_str_subclass(self):
        assert isinstance(StepStatus.DONE, str)


# ---------------------------------------------------------------------------
# StepConfig
# ---------------------------------------------------------------------------

class TestStepConfig:
    def test_defaults(self):
        cfg = StepConfig(name="s", fn=lambda ctx: None)
        assert cfg.max_retries == 0
        assert cfg.skip_on_failure is False

    def test_custom_values(self):
        fn = lambda ctx: 42
        cfg = StepConfig(name="x", fn=fn, max_retries=3, skip_on_failure=True)
        assert cfg.name == "x"
        assert cfg.fn is fn
        assert cfg.max_retries == 3
        assert cfg.skip_on_failure is True


# ---------------------------------------------------------------------------
# StepResult
# ---------------------------------------------------------------------------

class TestStepResult:
    def test_defaults(self):
        sr = StepResult(name="s", status=StepStatus.DONE)
        assert sr.output is None
        assert sr.error is None
        assert sr.attempts == 0

    def test_full_construction(self):
        exc = ValueError("oops")
        sr = StepResult(name="s", status=StepStatus.FAILED, output=None, error=exc, attempts=3)
        assert sr.name == "s"
        assert sr.status == StepStatus.FAILED
        assert sr.error is exc
        assert sr.attempts == 3


# ---------------------------------------------------------------------------
# WorkflowConfig
# ---------------------------------------------------------------------------

class TestWorkflowConfig:
    def test_empty_steps(self):
        cfg = WorkflowConfig(name="wf")
        assert cfg.steps == []

    def test_with_steps(self):
        steps = [ok_step("a"), ok_step("b")]
        cfg = WorkflowConfig(name="wf", steps=steps)
        assert len(cfg.steps) == 2


# ---------------------------------------------------------------------------
# WorkflowResult
# ---------------------------------------------------------------------------

class TestWorkflowResult:
    def _make(self, statuses):
        steps = [StepResult(name=f"s{i}", status=s) for i, s in enumerate(statuses)]
        return WorkflowResult(name="wf", steps=steps)

    def test_success_all_done(self):
        wr = self._make([StepStatus.DONE, StepStatus.DONE])
        assert wr.success is True

    def test_success_all_skipped(self):
        wr = self._make([StepStatus.SKIPPED, StepStatus.SKIPPED])
        assert wr.success is True

    def test_success_mixed_done_skipped(self):
        wr = self._make([StepStatus.DONE, StepStatus.SKIPPED])
        assert wr.success is True

    def test_success_false_when_failed(self):
        wr = self._make([StepStatus.DONE, StepStatus.FAILED])
        assert wr.success is False

    def test_success_empty_steps(self):
        wr = WorkflowResult(name="empty", steps=[])
        assert wr.success is True

    def test_step_results_returns_list(self):
        wr = self._make([StepStatus.DONE])
        assert isinstance(wr.step_results, list)
        assert len(wr.step_results) == 1

    def test_step_results_is_copy(self):
        wr = self._make([StepStatus.DONE])
        lst = wr.step_results
        lst.append("extra")
        assert len(wr.step_results) == 1  # original unchanged

    def test_get_existing(self):
        steps = [StepResult(name="alpha", status=StepStatus.DONE)]
        wr = WorkflowResult(name="wf", steps=steps)
        assert wr.get("alpha") is steps[0]

    def test_get_missing_returns_none(self):
        wr = WorkflowResult(name="wf", steps=[])
        assert wr.get("nope") is None

    def test_name_property(self):
        wr = WorkflowResult(name="my-workflow", steps=[])
        assert wr.name == "my-workflow"


# ---------------------------------------------------------------------------
# WorkflowEngine — single step success
# ---------------------------------------------------------------------------

class TestSingleStepSuccess:
    def test_result_success(self):
        engine = make_engine()
        cfg = WorkflowConfig(name="wf", steps=[ok_step("a", value=99)])
        result = engine.run(cfg)
        assert result.success is True

    def test_result_step_done(self):
        engine = make_engine()
        cfg = WorkflowConfig(name="wf", steps=[ok_step("a", value=99)])
        result = engine.run(cfg)
        sr = result.get("a")
        assert sr.status == StepStatus.DONE

    def test_result_output_stored(self):
        engine = make_engine()
        cfg = WorkflowConfig(name="wf", steps=[ok_step("a", value={"x": 1})])
        result = engine.run(cfg)
        assert result.get("a").output == {"x": 1}

    def test_attempts_is_one(self):
        engine = make_engine()
        cfg = WorkflowConfig(name="wf", steps=[ok_step("a")])
        result = engine.run(cfg)
        assert result.get("a").attempts == 1

    def test_error_is_none(self):
        engine = make_engine()
        cfg = WorkflowConfig(name="wf", steps=[ok_step("a")])
        result = engine.run(cfg)
        assert result.get("a").error is None


# ---------------------------------------------------------------------------
# WorkflowEngine — multi-step success and context propagation
# ---------------------------------------------------------------------------

class TestMultiStepSuccess:
    def test_all_done(self):
        def step_a(ctx):
            return 10

        def step_b(ctx):
            return 20

        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[
                StepConfig("a", fn=step_a),
                StepConfig("b", fn=step_b),
            ],
        )
        result = engine.run(cfg)
        assert result.success is True
        assert result.get("a").status == StepStatus.DONE
        assert result.get("b").status == StepStatus.DONE

    def test_context_results_populated(self):
        calls = []

        def step_a(ctx):
            calls.append("a")
            return 42

        def step_b(ctx):
            calls.append("b")
            assert ctx["_results"]["a"].output == 42
            return 84

        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[
                StepConfig("a", fn=step_a),
                StepConfig("b", fn=step_b),
            ],
        )
        result = engine.run(cfg)
        assert result.success is True
        assert calls == ["a", "b"]

    def test_output_accessible_in_later_steps(self):
        """Steps can read earlier outputs from context["_results"]."""
        def step_a(ctx):
            return [1, 2, 3]

        def step_b(ctx):
            items = ctx["_results"]["a"].output
            return sum(items)

        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig("a", fn=step_a), StepConfig("b", fn=step_b)],
        )
        result = engine.run(cfg)
        assert result.get("b").output == 6

    def test_step_results_order_preserved(self):
        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[ok_step("x"), ok_step("y"), ok_step("z")],
        )
        result = engine.run(cfg)
        names = [sr.name for sr in result.step_results]
        assert names == ["x", "y", "z"]

    def test_context_shared_mutation(self):
        """A step can mutate the raw context and the next step sees it."""
        def step_a(ctx):
            ctx["shared_key"] = "hello"
            return None

        def step_b(ctx):
            assert ctx["shared_key"] == "hello"
            return ctx["shared_key"] + " world"

        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig("a", fn=step_a), StepConfig("b", fn=step_b)],
        )
        result = engine.run(cfg)
        assert result.get("b").output == "hello world"


# ---------------------------------------------------------------------------
# WorkflowEngine — failure stops workflow, remaining steps SKIPPED
# ---------------------------------------------------------------------------

class TestFailureStopsWorkflow:
    def _run_with_middle_failure(self):
        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[
                ok_step("before"),
                fail_step("middle"),
                ok_step("after"),
            ],
        )
        return engine.run(cfg)

    def test_workflow_not_successful(self):
        result = self._run_with_middle_failure()
        assert result.success is False

    def test_before_step_done(self):
        result = self._run_with_middle_failure()
        assert result.get("before").status == StepStatus.DONE

    def test_failing_step_failed(self):
        result = self._run_with_middle_failure()
        assert result.get("middle").status == StepStatus.FAILED

    def test_after_step_skipped(self):
        result = self._run_with_middle_failure()
        assert result.get("after").status == StepStatus.SKIPPED

    def test_after_step_zero_attempts(self):
        result = self._run_with_middle_failure()
        assert result.get("after").attempts == 0

    def test_error_captured(self):
        exc = ValueError("test-error")
        engine = make_engine()
        cfg = WorkflowConfig(name="wf", steps=[fail_step("s", exc=exc)])
        result = engine.run(cfg)
        assert result.get("s").error is exc

    def test_multiple_trailing_steps_all_skipped(self):
        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[
                fail_step("step1"),
                ok_step("step2"),
                ok_step("step3"),
                ok_step("step4"),
            ],
        )
        result = engine.run(cfg)
        for name in ("step2", "step3", "step4"):
            assert result.get(name).status == StepStatus.SKIPPED


# ---------------------------------------------------------------------------
# WorkflowEngine — max_retries, success on retry
# ---------------------------------------------------------------------------

class TestMaxRetriesSuccessOnRetry:
    def test_succeeds_on_second_attempt(self):
        calls = []

        def flaky(ctx):
            calls.append(1)
            if len(calls) < 2:
                raise RuntimeError("not yet")
            return "ok"

        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig("s", fn=flaky, max_retries=1)],
        )
        result = engine.run(cfg)
        assert result.success is True
        assert result.get("s").status == StepStatus.DONE
        assert result.get("s").output == "ok"

    def test_attempts_count_is_correct(self):
        calls = []

        def flaky(ctx):
            calls.append(1)
            if len(calls) < 3:
                raise RuntimeError("not yet")
            return "done"

        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig("s", fn=flaky, max_retries=5)],
        )
        result = engine.run(cfg)
        assert result.get("s").attempts == 3  # failed twice, succeeded third

    def test_succeeds_on_last_allowed_attempt(self):
        calls = []

        def fn(ctx):
            calls.append(1)
            if len(calls) <= 3:
                raise RuntimeError("x")
            return "final"

        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig("s", fn=fn, max_retries=3)],
        )
        result = engine.run(cfg)
        assert result.success is True
        assert result.get("s").attempts == 4


# ---------------------------------------------------------------------------
# WorkflowEngine — max_retries exhausted → FAILED
# ---------------------------------------------------------------------------

class TestMaxRetriesExhausted:
    def test_failed_after_all_retries(self):
        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig("s", fn=lambda ctx: (_ for _ in ()).throw(RuntimeError("x")), max_retries=2)],
        )
        result = engine.run(cfg)
        assert result.get("s").status == StepStatus.FAILED

    def test_attempts_equals_one_plus_max_retries(self):
        calls = []

        def always_fail(ctx):
            calls.append(1)
            raise RuntimeError("always")

        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig("s", fn=always_fail, max_retries=4)],
        )
        result = engine.run(cfg)
        assert result.get("s").attempts == 5  # 1 initial + 4 retries
        assert len(calls) == 5

    def test_no_retries_attempts_is_one(self):
        def always_fail(ctx):
            raise RuntimeError("always")

        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig("s", fn=always_fail, max_retries=0)],
        )
        result = engine.run(cfg)
        assert result.get("s").attempts == 1

    def test_workflow_fails(self):
        def always_fail(ctx):
            raise RuntimeError("always")

        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig("s", fn=always_fail, max_retries=2)],
        )
        result = engine.run(cfg)
        assert result.success is False


# ---------------------------------------------------------------------------
# WorkflowEngine — skip_on_failure=True continues after failure
# ---------------------------------------------------------------------------

class TestSkipOnFailure:
    def test_continues_after_failure(self):
        ran = []

        def always_fail(ctx):
            raise RuntimeError("x")

        def after(ctx):
            ran.append("after")
            return "ran"

        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[
                StepConfig("fail_step", fn=always_fail, skip_on_failure=True),
                StepConfig("after_step", fn=after),
            ],
        )
        result = engine.run(cfg)
        assert ran == ["after"]

    def test_skipped_not_failed(self):
        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig("s", fn=lambda ctx: (_ for _ in ()).throw(RuntimeError()), skip_on_failure=True)],
        )
        result = engine.run(cfg)
        assert result.get("s").status == StepStatus.SKIPPED

    def test_workflow_still_successful(self):
        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig("s", fn=lambda ctx: (_ for _ in ()).throw(RuntimeError()), skip_on_failure=True)],
        )
        result = engine.run(cfg)
        assert result.success is True

    def test_error_captured_even_when_skipped(self):
        exc = TypeError("type-err")
        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig("s", fn=lambda ctx: (_ for _ in ()).throw(exc), skip_on_failure=True)],
        )
        result = engine.run(cfg)
        assert result.get("s").error is exc

    def test_later_steps_run_and_succeed(self):
        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[
                StepConfig("a", fn=lambda ctx: (_ for _ in ()).throw(RuntimeError()), skip_on_failure=True),
                StepConfig("b", fn=lambda ctx: "b-output"),
                StepConfig("c", fn=lambda ctx: "c-output"),
            ],
        )
        result = engine.run(cfg)
        assert result.get("b").status == StepStatus.DONE
        assert result.get("c").status == StepStatus.DONE
        assert result.success is True

    def test_skip_on_failure_with_retries_exhausted(self):
        """max_retries exhausted + skip_on_failure → SKIPPED, not FAILED."""
        calls = []

        def always_fail(ctx):
            calls.append(1)
            raise RuntimeError("x")

        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig("s", fn=always_fail, max_retries=2, skip_on_failure=True)],
        )
        result = engine.run(cfg)
        assert result.get("s").status == StepStatus.SKIPPED
        assert len(calls) == 3  # all attempts were made


# ---------------------------------------------------------------------------
# WorkflowEngine — context["_results"] correctness
# ---------------------------------------------------------------------------

class TestContextResults:
    def test_results_key_created(self):
        ctx = {}
        engine = make_engine()
        cfg = WorkflowConfig(name="wf", steps=[ok_step("a")])
        engine.run(cfg, context=ctx)
        assert "_results" in ctx

    def test_results_keyed_by_step_name(self):
        ctx = {}
        engine = make_engine()
        cfg = WorkflowConfig(name="wf", steps=[ok_step("alpha"), ok_step("beta")])
        engine.run(cfg, context=ctx)
        assert "alpha" in ctx["_results"]
        assert "beta" in ctx["_results"]

    def test_results_are_step_result_instances(self):
        ctx = {}
        engine = make_engine()
        cfg = WorkflowConfig(name="wf", steps=[ok_step("s")])
        engine.run(cfg, context=ctx)
        assert isinstance(ctx["_results"]["s"], StepResult)

    def test_skipped_steps_in_results(self):
        ctx = {}
        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[fail_step("f"), ok_step("after")],
        )
        engine.run(cfg, context=ctx)
        assert ctx["_results"]["after"].status == StepStatus.SKIPPED

    def test_initial_context_preserved(self):
        ctx = {"initial_key": "initial_value"}
        engine = make_engine()
        cfg = WorkflowConfig(name="wf", steps=[ok_step("a")])
        engine.run(cfg, context=ctx)
        assert ctx["initial_key"] == "initial_value"

    def test_none_context_creates_fresh_dict(self):
        engine = make_engine()
        cfg = WorkflowConfig(name="wf", steps=[ok_step("a")])
        result = engine.run(cfg, context=None)
        assert result.success is True  # no exception means ctx was created


# ---------------------------------------------------------------------------
# WorkflowEngine — empty steps list
# ---------------------------------------------------------------------------

class TestEmptyWorkflow:
    def test_empty_steps_success(self):
        engine = make_engine()
        cfg = WorkflowConfig(name="empty", steps=[])
        result = engine.run(cfg)
        assert result.success is True

    def test_empty_steps_no_step_results(self):
        engine = make_engine()
        cfg = WorkflowConfig(name="empty", steps=[])
        result = engine.run(cfg)
        assert result.step_results == []


# ---------------------------------------------------------------------------
# WorkflowEngine.validate()
# ---------------------------------------------------------------------------

class TestValidate:
    def test_valid_config_no_errors(self):
        engine = make_engine()
        cfg = WorkflowConfig(
            name="good",
            steps=[ok_step("a"), ok_step("b")],
        )
        assert engine.validate(cfg) == []

    def test_empty_workflow_name(self):
        engine = make_engine()
        cfg = WorkflowConfig(name="", steps=[])
        errors = engine.validate(cfg)
        assert any("name" in e.lower() for e in errors)

    def test_whitespace_only_name(self):
        engine = make_engine()
        cfg = WorkflowConfig(name="   ", steps=[])
        errors = engine.validate(cfg)
        assert any("name" in e.lower() for e in errors)

    def test_duplicate_step_names(self):
        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[ok_step("dup"), ok_step("dup")],
        )
        errors = engine.validate(cfg)
        assert any("dup" in e for e in errors)

    def test_duplicate_step_names_mentioned(self):
        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[ok_step("same"), ok_step("same")],
        )
        errors = engine.validate(cfg)
        assert len(errors) >= 1

    def test_non_callable_fn(self):
        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig(name="s", fn="not-a-function")],
        )
        errors = engine.validate(cfg)
        assert any("callable" in e.lower() for e in errors)

    def test_non_callable_fn_step_name_in_error(self):
        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig(name="broken", fn=42)],
        )
        errors = engine.validate(cfg)
        assert any("broken" in e for e in errors)

    def test_negative_max_retries(self):
        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig(name="s", fn=lambda ctx: None, max_retries=-1)],
        )
        errors = engine.validate(cfg)
        assert any("max_retries" in e.lower() for e in errors)

    def test_zero_max_retries_is_valid(self):
        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig(name="s", fn=lambda ctx: None, max_retries=0)],
        )
        assert engine.validate(cfg) == []

    def test_multiple_errors_returned(self):
        engine = make_engine()
        cfg = WorkflowConfig(
            name="",
            steps=[
                StepConfig(name="s", fn="bad", max_retries=-1),
                StepConfig(name="s", fn=lambda ctx: None),
            ],
        )
        errors = engine.validate(cfg)
        assert len(errors) >= 3  # empty name + non-callable + duplicate + neg retries

    def test_valid_empty_steps(self):
        engine = make_engine()
        cfg = WorkflowConfig(name="valid", steps=[])
        assert engine.validate(cfg) == []

    def test_lambda_is_callable(self):
        engine = make_engine()
        cfg = WorkflowConfig(
            name="wf",
            steps=[StepConfig(name="s", fn=lambda ctx: None)],
        )
        assert engine.validate(cfg) == []


# ---------------------------------------------------------------------------
# WorkflowEngine — engine is stateless / reusable
# ---------------------------------------------------------------------------

class TestEngineStateless:
    def test_reuse_engine_multiple_runs(self):
        engine = make_engine()
        cfg = WorkflowConfig(name="wf", steps=[ok_step("a", value=1)])
        r1 = engine.run(cfg)
        r2 = engine.run(cfg)
        assert r1.success is True
        assert r2.success is True

    def test_separate_contexts_per_run(self):
        results = []

        def record(ctx):
            results.append(id(ctx))
            return None

        engine = make_engine()
        cfg = WorkflowConfig(name="wf", steps=[StepConfig("s", fn=record)])
        engine.run(cfg)
        engine.run(cfg)
        # Each run created its own context (different id).
        assert len(results) == 2
        assert results[0] != results[1]
