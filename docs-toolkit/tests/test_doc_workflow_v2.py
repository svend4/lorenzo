"""Tests for docstoolkit.doc_workflow_v2 (E265)."""
from __future__ import annotations

import pytest

from docstoolkit.doc_workflow_v2 import (
    DocWorkflowV2,
    StepDef,
    StepInstance,
    StepStatus,
    WorkflowDefinitionV2,
    WorkflowInstance,
    WorkflowStatus,
)


def _linear_def(name: str = "linear") -> WorkflowDefinitionV2:
    d = WorkflowDefinitionV2(name)
    d.add_step("a", "A")
    d.add_step("b", "B")
    d.add_step("c", "C")
    d.add_transition("a", "b")
    d.add_transition("b", "c")
    return d


def _parallel_def() -> WorkflowDefinitionV2:
    d = WorkflowDefinitionV2("parallel")
    d.add_step("start", "Start")
    d.add_step("review_a", "Review A")
    d.add_step("review_b", "Review B", parallel_with=["review_a"])
    d.add_step("finish", "Finish")
    d.add_transition("start", "review_a")
    d.add_transition("start", "review_b")
    d.add_transition("review_a", "finish")
    d.add_transition("review_b", "finish")
    return d


class TestStepStatus:
    def test_pending_member(self):
        assert StepStatus.PENDING.value == "pending"

    def test_active_member(self):
        assert StepStatus.ACTIVE.value == "active"

    def test_completed_member(self):
        assert StepStatus.COMPLETED.value == "completed"

    def test_skipped_member(self):
        assert StepStatus.SKIPPED.value == "skipped"

    def test_failed_member(self):
        assert StepStatus.FAILED.value == "failed"

    def test_timed_out_member(self):
        assert StepStatus.TIMED_OUT.value == "timed_out"

    def test_six_members(self):
        assert len(list(StepStatus)) == 6


class TestWorkflowStatus:
    def test_active(self):
        assert WorkflowStatus.ACTIVE.value == "active"

    def test_completed(self):
        assert WorkflowStatus.COMPLETED.value == "completed"

    def test_failed(self):
        assert WorkflowStatus.FAILED.value == "failed"

    def test_cancelled(self):
        assert WorkflowStatus.CANCELLED.value == "cancelled"

    def test_four_members(self):
        assert len(list(WorkflowStatus)) == 4


class TestStepDef:
    def test_basic(self):
        s = StepDef(step_id="a", name="A")
        assert s.step_id == "a"
        assert s.name == "A"
        assert s.condition is None
        assert s.timeout_seconds is None
        assert s.parallel_with == []

    def test_with_condition(self):
        cond = lambda ctx: True
        s = StepDef(step_id="a", name="A", condition=cond)
        assert s.condition is cond

    def test_with_timeout(self):
        s = StepDef(step_id="a", name="A", timeout_seconds=30.0)
        assert s.timeout_seconds == 30.0


class TestStepInstance:
    def test_defaults(self):
        s = StepInstance(step_id="a", status=StepStatus.PENDING)
        assert s.started_at is None
        assert s.completed_at is None
        assert s.result is None
        assert s.error is None

    def test_with_values(self):
        s = StepInstance(
            step_id="a",
            status=StepStatus.COMPLETED,
            started_at=1.0,
            completed_at=2.0,
            result={"x": 1},
        )
        assert s.result == {"x": 1}


class TestWorkflowInstance:
    def test_defaults(self):
        w = WorkflowInstance(
            instance_id="i", doc_id="d", status=WorkflowStatus.ACTIVE
        )
        assert w.context == {}
        assert w.steps == {}
        assert w.started_at == 0.0
        assert w.completed_at is None

    def test_with_context(self):
        w = WorkflowInstance(
            instance_id="i",
            doc_id="d",
            status=WorkflowStatus.ACTIVE,
            context={"k": "v"},
        )
        assert w.context["k"] == "v"


class TestAddStep:
    def test_returns_step(self):
        d = WorkflowDefinitionV2("x")
        s = d.add_step("a", "A")
        assert isinstance(s, StepDef)
        assert s.step_id == "a"

    def test_with_parallel(self):
        d = WorkflowDefinitionV2("x")
        d.add_step("a", "A")
        s = d.add_step("b", "B", parallel_with=["a"])
        assert s.parallel_with == ["a"]

    def test_duplicate_overwrites(self):
        d = WorkflowDefinitionV2("x")
        d.add_step("a", "A")
        d.add_step("a", "A2")
        steps = d.steps()
        assert len(steps) == 1
        assert steps[0].name == "A2"


class TestAddTransition:
    def test_returns_true(self):
        d = WorkflowDefinitionV2("x")
        d.add_step("a", "A")
        d.add_step("b", "B")
        assert d.add_transition("a", "b") is True

    def test_unknown_from(self):
        d = WorkflowDefinitionV2("x")
        d.add_step("a", "A")
        assert d.add_transition("missing", "a") is False

    def test_unknown_to(self):
        d = WorkflowDefinitionV2("x")
        d.add_step("a", "A")
        assert d.add_transition("a", "missing") is False

    def test_duplicate(self):
        d = WorkflowDefinitionV2("x")
        d.add_step("a", "A")
        d.add_step("b", "B")
        d.add_transition("a", "b")
        assert d.add_transition("a", "b") is False


class TestSteps:
    def test_empty(self):
        d = WorkflowDefinitionV2("x")
        assert d.steps() == []

    def test_order(self):
        d = WorkflowDefinitionV2("x")
        d.add_step("a", "A")
        d.add_step("b", "B")
        d.add_step("c", "C")
        ids = [s.step_id for s in d.steps()]
        assert ids == ["a", "b", "c"]


class TestNextSteps:
    def test_no_next(self):
        d = _linear_def()
        assert d.next_steps("c") == []

    def test_one_next(self):
        d = _linear_def()
        assert d.next_steps("a") == ["b"]

    def test_multiple_next(self):
        d = _parallel_def()
        nxt = d.next_steps("start")
        assert set(nxt) == {"review_a", "review_b"}

    def test_unknown(self):
        d = _linear_def()
        assert d.next_steps("missing") == []


class TestParallelGroups:
    def test_none(self):
        d = _linear_def()
        assert d.parallel_groups() == []

    def test_one_pair(self):
        d = _parallel_def()
        groups = d.parallel_groups()
        assert len(groups) == 1
        assert groups[0] == {"review_a", "review_b"}

    def test_transitive(self):
        d = WorkflowDefinitionV2("x")
        d.add_step("a", "A")
        d.add_step("b", "B", parallel_with=["a"])
        d.add_step("c", "C", parallel_with=["b"])
        groups = d.parallel_groups()
        assert len(groups) == 1
        assert groups[0] == {"a", "b", "c"}


class TestStart:
    def test_returns_instance(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("doc-1", now=0.0)
        assert isinstance(inst, WorkflowInstance)
        assert inst.doc_id == "doc-1"

    def test_status_active(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("doc-1", now=0.0)
        assert inst.status == WorkflowStatus.ACTIVE

    def test_first_step_active(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("doc-1", now=0.0)
        assert inst.steps["a"].status == StepStatus.ACTIVE
        assert inst.steps["b"].status == StepStatus.PENDING
        assert inst.steps["c"].status == StepStatus.PENDING

    def test_context_copied(self):
        wf = DocWorkflowV2(_linear_def())
        ctx = {"k": 1}
        inst = wf.start("d", context=ctx, now=0.0)
        ctx["k"] = 999
        assert inst.context["k"] == 1

    def test_started_at(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=42.0)
        assert inst.started_at == 42.0

    def test_unique_ids(self):
        wf = DocWorkflowV2(_linear_def())
        a = wf.start("d", now=0.0)
        b = wf.start("d", now=0.0)
        assert a.instance_id != b.instance_id


class TestCompleteStep:
    def test_unknown_instance(self):
        wf = DocWorkflowV2(_linear_def())
        assert wf.complete_step("missing", "a") is False

    def test_unknown_step(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        assert wf.complete_step(inst.instance_id, "z") is False

    def test_inactive_step(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        assert wf.complete_step(inst.instance_id, "b") is False  # pending

    def test_success(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        assert wf.complete_step(inst.instance_id, "a", result={"x": 1}, now=1.0)
        st = wf.get_instance(inst.instance_id).steps["a"]
        assert st.status == StepStatus.COMPLETED
        assert st.completed_at == 1.0
        assert st.result == {"x": 1}


class TestCompleteStepAdvances:
    def test_next_active(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        wf.complete_step(inst.instance_id, "a", now=1.0)
        inst2 = wf.get_instance(inst.instance_id)
        assert inst2.steps["b"].status == StepStatus.ACTIVE

    def test_terminal_completes_workflow(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        wf.complete_step(inst.instance_id, "a", now=1.0)
        wf.complete_step(inst.instance_id, "b", now=2.0)
        wf.complete_step(inst.instance_id, "c", now=3.0)
        inst2 = wf.get_instance(inst.instance_id)
        assert inst2.status == WorkflowStatus.COMPLETED
        assert inst2.completed_at == 3.0


class TestFailStep:
    def test_unknown_instance(self):
        wf = DocWorkflowV2(_linear_def())
        assert wf.fail_step("missing", "a") is False

    def test_inactive_step(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        assert wf.fail_step(inst.instance_id, "b") is False

    def test_success(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        assert wf.fail_step(inst.instance_id, "a", error="boom", now=1.0)
        inst2 = wf.get_instance(inst.instance_id)
        assert inst2.steps["a"].status == StepStatus.FAILED
        assert inst2.steps["a"].error == "boom"
        assert inst2.status == WorkflowStatus.FAILED


class TestSkipStep:
    def test_skip_active(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        assert wf.skip_step(inst.instance_id, "a", now=1.0)
        inst2 = wf.get_instance(inst.instance_id)
        assert inst2.steps["a"].status == StepStatus.SKIPPED
        assert inst2.steps["b"].status == StepStatus.ACTIVE

    def test_skip_pending(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        # b is pending; skip should still work and advance
        assert wf.skip_step(inst.instance_id, "b", now=1.0) is True

    def test_unknown(self):
        wf = DocWorkflowV2(_linear_def())
        assert wf.skip_step("missing", "a") is False


class TestCancel:
    def test_cancel_active(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        assert wf.cancel(inst.instance_id, now=5.0) is True
        inst2 = wf.get_instance(inst.instance_id)
        assert inst2.status == WorkflowStatus.CANCELLED
        assert inst2.completed_at == 5.0

    def test_cancel_already_completed(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        wf.complete_step(inst.instance_id, "a", now=1.0)
        wf.complete_step(inst.instance_id, "b", now=2.0)
        wf.complete_step(inst.instance_id, "c", now=3.0)
        assert wf.cancel(inst.instance_id) is False

    def test_cancel_unknown(self):
        wf = DocWorkflowV2(_linear_def())
        assert wf.cancel("missing") is False


class TestActiveSteps:
    def test_initial(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        actives = wf.active_steps(inst.instance_id)
        assert [s.step_id for s in actives] == ["a"]

    def test_unknown(self):
        wf = DocWorkflowV2(_linear_def())
        assert wf.active_steps("missing") == []

    def test_after_complete(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        wf.complete_step(inst.instance_id, "a", now=1.0)
        actives = wf.active_steps(inst.instance_id)
        assert [s.step_id for s in actives] == ["b"]


class TestPendingSteps:
    def test_initial(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        pending = wf.pending_steps(inst.instance_id)
        assert {s.step_id for s in pending} == {"b", "c"}

    def test_unknown(self):
        wf = DocWorkflowV2(_linear_def())
        assert wf.pending_steps("missing") == []


class TestCheckTimeouts:
    def test_no_timeouts(self):
        wf = DocWorkflowV2(_linear_def())
        wf.start("d", now=0.0)
        assert wf.check_timeouts(now=1000.0) == 0

    def test_one_timeout(self):
        d = WorkflowDefinitionV2("x")
        d.add_step("a", "A", timeout_seconds=10.0)
        d.add_step("b", "B")
        d.add_transition("a", "b")
        wf = DocWorkflowV2(d)
        inst = wf.start("d", now=0.0)
        n = wf.check_timeouts(now=100.0)
        assert n == 1
        inst2 = wf.get_instance(inst.instance_id)
        assert inst2.steps["a"].status == StepStatus.TIMED_OUT
        assert inst2.status == WorkflowStatus.FAILED

    def test_within_deadline(self):
        d = WorkflowDefinitionV2("x")
        d.add_step("a", "A", timeout_seconds=10.0)
        wf = DocWorkflowV2(d)
        wf.start("d", now=0.0)
        assert wf.check_timeouts(now=5.0) == 0

    def test_no_timeout_config(self):
        wf = DocWorkflowV2(_linear_def())
        wf.start("d", now=0.0)
        assert wf.check_timeouts(now=1e9) == 0


class TestGetInstance:
    def test_known(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        assert wf.get_instance(inst.instance_id) is inst

    def test_unknown(self):
        wf = DocWorkflowV2(_linear_def())
        assert wf.get_instance("missing") is None


class TestInstancesForDoc:
    def test_empty(self):
        wf = DocWorkflowV2(_linear_def())
        assert wf.instances_for_doc("d") == []

    def test_multiple(self):
        wf = DocWorkflowV2(_linear_def())
        wf.start("d1", now=0.0)
        wf.start("d1", now=1.0)
        wf.start("d2", now=2.0)
        assert len(wf.instances_for_doc("d1")) == 2
        assert len(wf.instances_for_doc("d2")) == 1


class TestActiveInstances:
    def test_all_active(self):
        wf = DocWorkflowV2(_linear_def())
        wf.start("d1", now=0.0)
        wf.start("d2", now=0.0)
        assert len(wf.active_instances()) == 2

    def test_after_cancel(self):
        wf = DocWorkflowV2(_linear_def())
        a = wf.start("d1", now=0.0)
        wf.start("d2", now=0.0)
        wf.cancel(a.instance_id)
        assert len(wf.active_instances()) == 1


class TestProgress:
    def test_initial(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        assert wf.progress(inst.instance_id) == 0.0

    def test_partial(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        wf.complete_step(inst.instance_id, "a", now=1.0)
        assert wf.progress(inst.instance_id) == pytest.approx(1 / 3)

    def test_full(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        wf.complete_step(inst.instance_id, "a", now=1.0)
        wf.complete_step(inst.instance_id, "b", now=2.0)
        wf.complete_step(inst.instance_id, "c", now=3.0)
        assert wf.progress(inst.instance_id) == 1.0

    def test_unknown(self):
        wf = DocWorkflowV2(_linear_def())
        assert wf.progress("missing") == 0.0


class TestParallel:
    def test_both_activated(self):
        wf = DocWorkflowV2(_parallel_def())
        inst = wf.start("d", now=0.0)
        wf.complete_step(inst.instance_id, "start", now=1.0)
        inst2 = wf.get_instance(inst.instance_id)
        assert inst2.steps["review_a"].status == StepStatus.ACTIVE
        assert inst2.steps["review_b"].status == StepStatus.ACTIVE

    def test_finish_when_both_done(self):
        wf = DocWorkflowV2(_parallel_def())
        inst = wf.start("d", now=0.0)
        wf.complete_step(inst.instance_id, "start", now=1.0)
        wf.complete_step(inst.instance_id, "review_a", now=2.0)
        wf.complete_step(inst.instance_id, "review_b", now=3.0)
        inst2 = wf.get_instance(inst.instance_id)
        assert inst2.steps["finish"].status == StepStatus.ACTIVE

    def test_completion(self):
        wf = DocWorkflowV2(_parallel_def())
        inst = wf.start("d", now=0.0)
        wf.complete_step(inst.instance_id, "start", now=1.0)
        wf.complete_step(inst.instance_id, "review_a", now=2.0)
        wf.complete_step(inst.instance_id, "review_b", now=3.0)
        wf.complete_step(inst.instance_id, "finish", now=4.0)
        inst2 = wf.get_instance(inst.instance_id)
        assert inst2.status == WorkflowStatus.COMPLETED


class TestConditional:
    def test_condition_true(self):
        d = WorkflowDefinitionV2("x")
        d.add_step("a", "A")
        d.add_step("b", "B", condition=lambda ctx: ctx.get("ok") is True)
        d.add_transition("a", "b")
        wf = DocWorkflowV2(d)
        inst = wf.start("d", context={"ok": True}, now=0.0)
        wf.complete_step(inst.instance_id, "a", now=1.0)
        inst2 = wf.get_instance(inst.instance_id)
        assert inst2.steps["b"].status == StepStatus.ACTIVE

    def test_condition_false_skips(self):
        d = WorkflowDefinitionV2("x")
        d.add_step("a", "A")
        d.add_step("b", "B", condition=lambda ctx: ctx.get("ok") is True)
        d.add_step("c", "C")
        d.add_transition("a", "b")
        d.add_transition("b", "c")
        wf = DocWorkflowV2(d)
        inst = wf.start("d", context={"ok": False}, now=0.0)
        wf.complete_step(inst.instance_id, "a", now=1.0)
        inst2 = wf.get_instance(inst.instance_id)
        assert inst2.steps["b"].status == StepStatus.SKIPPED
        assert inst2.steps["c"].status == StepStatus.ACTIVE

    def test_condition_exception_skips(self):
        def boom(ctx):
            raise RuntimeError("bad")

        d = WorkflowDefinitionV2("x")
        d.add_step("a", "A")
        d.add_step("b", "B", condition=boom)
        d.add_transition("a", "b")
        wf = DocWorkflowV2(d)
        inst = wf.start("d", now=0.0)
        wf.complete_step(inst.instance_id, "a", now=1.0)
        inst2 = wf.get_instance(inst.instance_id)
        assert inst2.steps["b"].status == StepStatus.SKIPPED


class TestTotalInstances:
    def test_zero(self):
        wf = DocWorkflowV2(_linear_def())
        assert wf.total_instances == 0

    def test_growth(self):
        wf = DocWorkflowV2(_linear_def())
        wf.start("d1", now=0.0)
        wf.start("d2", now=0.0)
        assert wf.total_instances == 2


class TestClear:
    def test_clears_all(self):
        wf = DocWorkflowV2(_linear_def())
        wf.start("d1", now=0.0)
        wf.start("d2", now=0.0)
        wf.clear()
        assert wf.total_instances == 0

    def test_clear_empty_ok(self):
        wf = DocWorkflowV2(_linear_def())
        wf.clear()
        assert wf.total_instances == 0


class TestEdgeCases:
    def test_single_step_workflow_completes(self):
        d = WorkflowDefinitionV2("x")
        d.add_step("only", "Only")
        wf = DocWorkflowV2(d)
        inst = wf.start("d", now=0.0)
        wf.complete_step(inst.instance_id, "only", now=1.0)
        assert wf.get_instance(inst.instance_id).status == WorkflowStatus.COMPLETED

    def test_no_steps_finalizes_immediately(self):
        d = WorkflowDefinitionV2("empty")
        wf = DocWorkflowV2(d)
        inst = wf.start("d", now=0.0)
        assert inst.status == WorkflowStatus.COMPLETED

    def test_complete_after_fail_blocked(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        wf.fail_step(inst.instance_id, "a", error="x", now=1.0)
        # Workflow is FAILED; further actions blocked
        assert wf.complete_step(inst.instance_id, "a", now=2.0) is False

    def test_complete_after_cancel_blocked(self):
        wf = DocWorkflowV2(_linear_def())
        inst = wf.start("d", now=0.0)
        wf.cancel(inst.instance_id, now=1.0)
        assert wf.complete_step(inst.instance_id, "a", now=2.0) is False
