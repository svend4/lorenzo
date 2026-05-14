"""Tests for docstoolkit.doc_render_pipeline."""
from __future__ import annotations

import pytest

from docstoolkit.doc_render_pipeline import (
    DocRenderPipeline,
    RenderContext,
    RenderResult,
    RenderStage,
    RenderStep,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def identity(text: str, ctx: RenderContext) -> tuple[str, RenderContext]:
    return text, ctx


def upper(text: str, ctx: RenderContext) -> tuple[str, RenderContext]:
    return text.upper(), ctx


def lower(text: str, ctx: RenderContext) -> tuple[str, RenderContext]:
    return text.lower(), ctx


def append_a(text: str, ctx: RenderContext) -> tuple[str, RenderContext]:
    return text + "A", ctx


def append_b(text: str, ctx: RenderContext) -> tuple[str, RenderContext]:
    return text + "B", ctx


def boom(text: str, ctx: RenderContext) -> tuple[str, RenderContext]:
    raise RuntimeError("boom")


# ---------------------------------------------------------------------------
# RenderStage
# ---------------------------------------------------------------------------


class TestRenderStage:
    def test_has_parse(self):
        assert RenderStage.PARSE.value == "parse"

    def test_has_transform(self):
        assert RenderStage.TRANSFORM.value == "transform"

    def test_has_render(self):
        assert RenderStage.RENDER.value == "render"

    def test_has_post_process(self):
        assert RenderStage.POST_PROCESS.value == "post_process"

    def test_distinct_members(self):
        assert len({RenderStage.PARSE, RenderStage.TRANSFORM,
                    RenderStage.RENDER, RenderStage.POST_PROCESS}) == 4


# ---------------------------------------------------------------------------
# RenderStep
# ---------------------------------------------------------------------------


class TestRenderStep:
    def test_defaults(self):
        s = RenderStep(name="x", func=identity)
        assert s.name == "x"
        assert s.stage == RenderStage.TRANSFORM
        assert s.priority == 0
        assert s.enabled is True

    def test_custom_stage(self):
        s = RenderStep(name="x", func=identity, stage=RenderStage.RENDER)
        assert s.stage == RenderStage.RENDER

    def test_custom_priority(self):
        s = RenderStep(name="x", func=identity, priority=42)
        assert s.priority == 42

    def test_disabled(self):
        s = RenderStep(name="x", func=identity, enabled=False)
        assert s.enabled is False


# ---------------------------------------------------------------------------
# RenderContext
# ---------------------------------------------------------------------------


class TestRenderContext:
    def test_basic(self):
        ctx = RenderContext(doc_id="d1")
        assert ctx.doc_id == "d1"
        assert ctx.variables == {}
        assert ctx.errors == []
        assert ctx.applied_steps == []

    def test_independent_variables(self):
        a = RenderContext(doc_id="a")
        b = RenderContext(doc_id="b")
        a.variables["k"] = 1
        assert "k" not in b.variables

    def test_independent_errors(self):
        a = RenderContext(doc_id="a")
        b = RenderContext(doc_id="b")
        a.errors.append("oops")
        assert b.errors == []

    def test_custom_variables(self):
        ctx = RenderContext(doc_id="d", variables={"title": "Hello"})
        assert ctx.variables["title"] == "Hello"


# ---------------------------------------------------------------------------
# RenderResult
# ---------------------------------------------------------------------------


class TestRenderResult:
    def test_basic(self):
        ctx = RenderContext(doc_id="d")
        r = RenderResult(output="x", context=ctx, success=True)
        assert r.output == "x"
        assert r.context is ctx
        assert r.success is True
        assert r.duration_ms == 0.0

    def test_duration(self):
        ctx = RenderContext(doc_id="d")
        r = RenderResult(output="x", context=ctx, success=True, duration_ms=12.5)
        assert r.duration_ms == 12.5


# ---------------------------------------------------------------------------
# add_step
# ---------------------------------------------------------------------------


class TestAddStep:
    def test_add_one(self):
        p = DocRenderPipeline()
        s = p.add_step("a", identity)
        assert isinstance(s, RenderStep)
        assert s.name == "a"
        assert p.step_count == 1

    def test_add_multiple(self):
        p = DocRenderPipeline()
        p.add_step("a", identity)
        p.add_step("b", identity)
        p.add_step("c", identity)
        assert p.step_count == 3

    def test_default_stage(self):
        p = DocRenderPipeline()
        s = p.add_step("a", identity)
        assert s.stage == RenderStage.TRANSFORM

    def test_custom_stage(self):
        p = DocRenderPipeline()
        s = p.add_step("a", identity, stage=RenderStage.RENDER)
        assert s.stage == RenderStage.RENDER

    def test_priority(self):
        p = DocRenderPipeline()
        s = p.add_step("a", identity, priority=10)
        assert s.priority == 10

    def test_duplicate_name_raises(self):
        p = DocRenderPipeline()
        p.add_step("a", identity)
        with pytest.raises(ValueError):
            p.add_step("a", identity)


# ---------------------------------------------------------------------------
# remove_step
# ---------------------------------------------------------------------------


class TestRemoveStep:
    def test_remove_existing(self):
        p = DocRenderPipeline()
        p.add_step("a", identity)
        assert p.remove_step("a") is True
        assert p.step_count == 0

    def test_remove_missing(self):
        p = DocRenderPipeline()
        assert p.remove_step("nope") is False

    def test_remove_one_keeps_others(self):
        p = DocRenderPipeline()
        p.add_step("a", identity)
        p.add_step("b", identity)
        p.remove_step("a")
        assert p.step_count == 1
        assert p.list_steps()[0].name == "b"


# ---------------------------------------------------------------------------
# enable / disable
# ---------------------------------------------------------------------------


class TestEnableDisable:
    def test_disable_existing(self):
        p = DocRenderPipeline()
        p.add_step("a", identity)
        assert p.disable_step("a") is True
        assert p.list_steps()[0].enabled is False

    def test_enable_existing(self):
        p = DocRenderPipeline()
        p.add_step("a", identity)
        p.disable_step("a")
        assert p.enable_step("a") is True
        assert p.list_steps()[0].enabled is True

    def test_disable_missing(self):
        p = DocRenderPipeline()
        assert p.disable_step("nope") is False

    def test_enable_missing(self):
        p = DocRenderPipeline()
        assert p.enable_step("nope") is False

    def test_disabled_step_skipped_in_render(self):
        p = DocRenderPipeline()
        p.add_step("u", upper)
        p.disable_step("u")
        r = p.render("hi", doc_id="d")
        assert r.output == "hi"
        assert "u" not in r.context.applied_steps


# ---------------------------------------------------------------------------
# render — basic
# ---------------------------------------------------------------------------


class TestRenderBasic:
    def test_no_steps_returns_input(self):
        p = DocRenderPipeline()
        r = p.render("hello")
        assert r.output == "hello"
        assert r.success is True

    def test_returns_result(self):
        p = DocRenderPipeline()
        r = p.render("hi")
        assert isinstance(r, RenderResult)

    def test_doc_id_propagated(self):
        p = DocRenderPipeline()
        r = p.render("hi", doc_id="abc")
        assert r.context.doc_id == "abc"

    def test_default_doc_id(self):
        p = DocRenderPipeline()
        r = p.render("hi")
        assert r.context.doc_id == "doc"

    def test_variables_propagated(self):
        p = DocRenderPipeline()
        r = p.render("hi", variables={"k": 1})
        assert r.context.variables["k"] == 1

    def test_duration_recorded(self):
        p = DocRenderPipeline()
        p.add_step("u", upper)
        r = p.render("hi")
        assert r.duration_ms >= 0.0


# ---------------------------------------------------------------------------
# render — transformations
# ---------------------------------------------------------------------------


class TestRenderTransform:
    def test_single_transform(self):
        p = DocRenderPipeline()
        p.add_step("u", upper)
        r = p.render("hi")
        assert r.output == "HI"

    def test_chained_transforms(self):
        p = DocRenderPipeline()
        p.add_step("u", upper, priority=0)
        p.add_step("l", lower, priority=1)
        r = p.render("Hi")
        assert r.output == "hi"

    def test_applied_steps_recorded(self):
        p = DocRenderPipeline()
        p.add_step("u", upper)
        r = p.render("hi")
        assert r.context.applied_steps == ["u"]

    def test_step_can_mutate_context(self):
        def annotate(text, ctx):
            ctx.variables["n"] = ctx.variables.get("n", 0) + 1
            return text, ctx

        p = DocRenderPipeline()
        p.add_step("a", annotate)
        r = p.render("hi")
        assert r.context.variables["n"] == 1


# ---------------------------------------------------------------------------
# render — stage order
# ---------------------------------------------------------------------------


class TestRenderStageOrder:
    def test_stages_execute_in_order(self):
        order: list[str] = []

        def make(name):
            def fn(text, ctx):
                order.append(name)
                return text, ctx
            return fn

        p = DocRenderPipeline()
        # add in reverse order
        p.add_step("pp", make("pp"), stage=RenderStage.POST_PROCESS)
        p.add_step("r", make("r"), stage=RenderStage.RENDER)
        p.add_step("t", make("t"), stage=RenderStage.TRANSFORM)
        p.add_step("p", make("p"), stage=RenderStage.PARSE)
        p.render("hi")
        assert order == ["p", "t", "r", "pp"]

    def test_text_flows_across_stages(self):
        p = DocRenderPipeline()
        p.add_step("p", append_a, stage=RenderStage.PARSE)
        p.add_step("t", append_b, stage=RenderStage.TRANSFORM)
        p.add_step("r", append_a, stage=RenderStage.RENDER)
        p.add_step("pp", append_b, stage=RenderStage.POST_PROCESS)
        r = p.render("")
        assert r.output == "ABAB"

    def test_only_one_stage(self):
        p = DocRenderPipeline()
        p.add_step("x", upper, stage=RenderStage.POST_PROCESS)
        r = p.render("hi")
        assert r.output == "HI"


# ---------------------------------------------------------------------------
# render — priority within stage
# ---------------------------------------------------------------------------


class TestRenderPriority:
    def test_priority_within_stage(self):
        p = DocRenderPipeline()
        p.add_step("b", append_b, stage=RenderStage.TRANSFORM, priority=10)
        p.add_step("a", append_a, stage=RenderStage.TRANSFORM, priority=1)
        r = p.render("")
        assert r.output == "AB"

    def test_negative_priority(self):
        p = DocRenderPipeline()
        p.add_step("a", append_a, stage=RenderStage.TRANSFORM, priority=0)
        p.add_step("b", append_b, stage=RenderStage.TRANSFORM, priority=-5)
        r = p.render("")
        assert r.output == "BA"

    def test_priority_isolated_per_stage(self):
        order: list[str] = []

        def make(name):
            def fn(text, ctx):
                order.append(name)
                return text, ctx
            return fn

        p = DocRenderPipeline()
        # high-priority post_process still runs after low-priority transform
        p.add_step("pp", make("pp"), stage=RenderStage.POST_PROCESS, priority=-99)
        p.add_step("t", make("t"), stage=RenderStage.TRANSFORM, priority=99)
        p.render("hi")
        assert order == ["t", "pp"]


# ---------------------------------------------------------------------------
# render — errors
# ---------------------------------------------------------------------------


class TestRenderError:
    def test_error_captured(self):
        p = DocRenderPipeline()
        p.add_step("oops", boom)
        r = p.render("hi")
        assert r.success is False
        assert len(r.context.errors) == 1
        assert "boom" in r.context.errors[0]

    def test_pipeline_continues_after_error(self):
        p = DocRenderPipeline()
        p.add_step("oops", boom, priority=0)
        p.add_step("u", upper, priority=1)
        r = p.render("hi")
        assert r.output == "HI"
        assert r.success is False

    def test_error_includes_step_name(self):
        p = DocRenderPipeline()
        p.add_step("badstep", boom)
        r = p.render("hi")
        assert "badstep" in r.context.errors[0]

    def test_failed_step_not_in_applied(self):
        p = DocRenderPipeline()
        p.add_step("oops", boom)
        r = p.render("hi")
        assert "oops" not in r.context.applied_steps


# ---------------------------------------------------------------------------
# render — empty pipeline
# ---------------------------------------------------------------------------


class TestRenderEmpty:
    def test_empty_success(self):
        p = DocRenderPipeline()
        r = p.render("hello")
        assert r.success is True
        assert r.output == "hello"

    def test_empty_applied(self):
        p = DocRenderPipeline()
        r = p.render("hello")
        assert r.context.applied_steps == []

    def test_empty_no_errors(self):
        p = DocRenderPipeline()
        r = p.render("hello")
        assert r.context.errors == []


# ---------------------------------------------------------------------------
# render_batch
# ---------------------------------------------------------------------------


class TestRenderBatch:
    def test_batch_basic(self):
        p = DocRenderPipeline()
        p.add_step("u", upper)
        results = p.render_batch([("hi", "d1"), ("bye", "d2")])
        assert len(results) == 2
        assert results[0].output == "HI"
        assert results[1].output == "BYE"

    def test_batch_doc_ids(self):
        p = DocRenderPipeline()
        results = p.render_batch([("a", "x"), ("b", "y")])
        assert results[0].context.doc_id == "x"
        assert results[1].context.doc_id == "y"

    def test_batch_empty(self):
        p = DocRenderPipeline()
        results = p.render_batch([])
        assert results == []

    def test_batch_isolated_contexts(self):
        def stash(text, ctx):
            ctx.variables["v"] = ctx.doc_id
            return text, ctx

        p = DocRenderPipeline()
        p.add_step("s", stash)
        results = p.render_batch([("a", "x"), ("b", "y")])
        assert results[0].context.variables["v"] == "x"
        assert results[1].context.variables["v"] == "y"


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------


class TestValidate:
    def test_empty_valid(self):
        p = DocRenderPipeline()
        ok, errs = p.validate()
        assert ok is True
        assert errs == []

    def test_normal_valid(self):
        p = DocRenderPipeline()
        p.add_step("a", identity)
        p.add_step("b", upper)
        ok, errs = p.validate()
        assert ok is True
        assert errs == []

    def test_returns_tuple(self):
        p = DocRenderPipeline()
        result = p.validate()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_invalid_func(self):
        p = DocRenderPipeline()
        p.add_step("bad", identity)
        # corrupt the step after the fact
        p._steps["bad"].func = "not-callable"  # type: ignore[assignment]
        ok, errs = p.validate()
        assert ok is False
        assert any("bad" in e for e in errs)


# ---------------------------------------------------------------------------
# list_steps
# ---------------------------------------------------------------------------


class TestListSteps:
    def test_empty(self):
        p = DocRenderPipeline()
        assert p.list_steps() == []

    def test_returns_all(self):
        p = DocRenderPipeline()
        p.add_step("a", identity)
        p.add_step("b", identity)
        assert len(p.list_steps()) == 2

    def test_filter_by_stage(self):
        p = DocRenderPipeline()
        p.add_step("a", identity, stage=RenderStage.PARSE)
        p.add_step("b", identity, stage=RenderStage.RENDER)
        result = p.list_steps(stage=RenderStage.PARSE)
        assert len(result) == 1
        assert result[0].name == "a"

    def test_enabled_only(self):
        p = DocRenderPipeline()
        p.add_step("a", identity)
        p.add_step("b", identity)
        p.disable_step("a")
        result = p.list_steps(enabled_only=True)
        assert len(result) == 1
        assert result[0].name == "b"

    def test_order_by_stage_then_priority(self):
        p = DocRenderPipeline()
        p.add_step("late", identity, stage=RenderStage.POST_PROCESS)
        p.add_step("early", identity, stage=RenderStage.PARSE)
        p.add_step("mid_high", identity, stage=RenderStage.TRANSFORM, priority=10)
        p.add_step("mid_low", identity, stage=RenderStage.TRANSFORM, priority=1)
        names = [s.name for s in p.list_steps()]
        assert names == ["early", "mid_low", "mid_high", "late"]


# ---------------------------------------------------------------------------
# steps_in_stage
# ---------------------------------------------------------------------------


class TestStepsInStage:
    def test_empty(self):
        p = DocRenderPipeline()
        assert p.steps_in_stage(RenderStage.PARSE) == []

    def test_single_stage(self):
        p = DocRenderPipeline()
        p.add_step("a", identity, stage=RenderStage.PARSE)
        p.add_step("b", identity, stage=RenderStage.RENDER)
        result = p.steps_in_stage(RenderStage.PARSE)
        assert [s.name for s in result] == ["a"]

    def test_priority_order_inside_stage(self):
        p = DocRenderPipeline()
        p.add_step("hi", identity, stage=RenderStage.TRANSFORM, priority=10)
        p.add_step("lo", identity, stage=RenderStage.TRANSFORM, priority=1)
        result = p.steps_in_stage(RenderStage.TRANSFORM)
        assert [s.name for s in result] == ["lo", "hi"]


# ---------------------------------------------------------------------------
# step_count
# ---------------------------------------------------------------------------


class TestStepCount:
    def test_empty(self):
        p = DocRenderPipeline()
        assert p.step_count == 0

    def test_after_add(self):
        p = DocRenderPipeline()
        p.add_step("a", identity)
        assert p.step_count == 1

    def test_after_remove(self):
        p = DocRenderPipeline()
        p.add_step("a", identity)
        p.add_step("b", identity)
        p.remove_step("a")
        assert p.step_count == 1


# ---------------------------------------------------------------------------
# move_step
# ---------------------------------------------------------------------------


class TestMoveStep:
    def test_move_existing(self):
        p = DocRenderPipeline()
        p.add_step("a", identity, stage=RenderStage.PARSE)
        assert p.move_step("a", RenderStage.RENDER) is True
        assert p.list_steps()[0].stage == RenderStage.RENDER

    def test_move_missing(self):
        p = DocRenderPipeline()
        assert p.move_step("nope", RenderStage.RENDER) is False

    def test_move_affects_execution_order(self):
        p = DocRenderPipeline()
        p.add_step("a", append_a, stage=RenderStage.PARSE)
        p.add_step("b", append_b, stage=RenderStage.POST_PROCESS)
        # baseline: A then B
        assert p.render("").output == "AB"
        # swap: move b to PARSE with lower priority
        p.move_step("b", RenderStage.PARSE)
        p.set_priority("b", -1)
        assert p.render("").output == "BA"


# ---------------------------------------------------------------------------
# set_priority
# ---------------------------------------------------------------------------


class TestSetPriority:
    def test_set_existing(self):
        p = DocRenderPipeline()
        p.add_step("a", identity)
        assert p.set_priority("a", 42) is True
        assert p.list_steps()[0].priority == 42

    def test_set_missing(self):
        p = DocRenderPipeline()
        assert p.set_priority("nope", 1) is False

    def test_priority_changes_order(self):
        p = DocRenderPipeline()
        p.add_step("a", append_a, priority=0)
        p.add_step("b", append_b, priority=1)
        assert p.render("").output == "AB"
        p.set_priority("a", 10)
        assert p.render("").output == "BA"


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_clear_empty(self):
        p = DocRenderPipeline()
        p.clear()
        assert p.step_count == 0

    def test_clear_populated(self):
        p = DocRenderPipeline()
        p.add_step("a", identity)
        p.add_step("b", identity)
        p.clear()
        assert p.step_count == 0

    def test_clear_returns_none(self):
        p = DocRenderPipeline()
        assert p.clear() is None


# ---------------------------------------------------------------------------
# edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_all_disabled(self):
        p = DocRenderPipeline()
        p.add_step("a", upper)
        p.add_step("b", append_a)
        p.disable_step("a")
        p.disable_step("b")
        r = p.render("hi")
        assert r.output == "hi"
        assert r.context.applied_steps == []
        assert r.success is True

    def test_remove_nonexistent_then_add(self):
        p = DocRenderPipeline()
        assert p.remove_step("missing") is False
        p.add_step("missing", identity)
        assert p.step_count == 1

    def test_enable_idempotent(self):
        p = DocRenderPipeline()
        p.add_step("a", identity)
        p.enable_step("a")
        p.enable_step("a")
        assert p.list_steps()[0].enabled is True

    def test_disable_idempotent(self):
        p = DocRenderPipeline()
        p.add_step("a", identity)
        p.disable_step("a")
        p.disable_step("a")
        assert p.list_steps()[0].enabled is False

    def test_render_empty_string(self):
        p = DocRenderPipeline()
        p.add_step("u", upper)
        r = p.render("")
        assert r.output == ""
        assert r.success is True

    def test_step_ignores_non_context_return(self):
        # If the step returns a non-RenderContext as second element, the
        # pipeline should not crash — the original ctx is kept.
        def weird(text, ctx):
            return text + "!", "not-a-context"  # type: ignore[return-value]

        p = DocRenderPipeline()
        p.add_step("w", weird)
        r = p.render("hi")
        assert r.output == "hi!"
        assert isinstance(r.context, RenderContext)

    def test_variables_independent_per_render(self):
        def stash(text, ctx):
            ctx.variables["count"] = ctx.variables.get("count", 0) + 1
            return text, ctx

        p = DocRenderPipeline()
        p.add_step("s", stash)
        r1 = p.render("a")
        r2 = p.render("b")
        assert r1.context.variables["count"] == 1
        assert r2.context.variables["count"] == 1

    def test_full_lifecycle_pipeline(self):
        # md -> html -> wrap -> minify style pipeline
        def parse(text, ctx):
            ctx.variables["raw"] = text
            return text, ctx

        def to_html(text, ctx):
            return f"<p>{text}</p>", ctx

        def wrap(text, ctx):
            return f"<html><body>{text}</body></html>", ctx

        def minify(text, ctx):
            return text.replace(" ", ""), ctx

        p = DocRenderPipeline()
        p.add_step("parse", parse, stage=RenderStage.PARSE)
        p.add_step("html", to_html, stage=RenderStage.TRANSFORM)
        p.add_step("wrap", wrap, stage=RenderStage.RENDER)
        p.add_step("minify", minify, stage=RenderStage.POST_PROCESS)
        r = p.render("hello world", doc_id="page1")
        assert r.success is True
        assert "<html>" in r.output
        assert " " not in r.output
        assert r.context.variables["raw"] == "hello world"
        assert r.context.applied_steps == ["parse", "html", "wrap", "minify"]
