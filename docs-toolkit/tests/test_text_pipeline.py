"""Tests for docstoolkit.text_pipeline — target: >= 85 tests."""
from __future__ import annotations

import pytest

from docstoolkit.text_pipeline import (
    PipelineResult,
    PipelineStep,
    StepOutput,
    TextPipeline,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def _upper(text: str) -> str:
    return text.upper()


def _lower(text: str) -> str:
    return text.lower()


def _strip(text: str) -> str:
    return text.strip()


def _double(text: str) -> str:
    return text * 2


def _add_bang(text: str) -> str:
    return text + "!"


def _replace_a(text: str) -> str:
    return text.replace("a", "X")


def _exploding(text: str) -> str:
    raise ValueError("boom")


# ===========================================================================
# PipelineStep dataclass
# ===========================================================================

class TestPipelineStep:
    def test_name_stored(self):
        step = PipelineStep(name="s", fn=_upper)
        assert step.name == "s"

    def test_fn_stored(self):
        step = PipelineStep(name="s", fn=_upper)
        assert step.fn is _upper

    def test_enabled_default_true(self):
        step = PipelineStep(name="s", fn=_upper)
        assert step.enabled is True

    def test_enabled_can_be_false(self):
        step = PipelineStep(name="s", fn=_upper, enabled=False)
        assert step.enabled is False

    def test_condition_default_none(self):
        step = PipelineStep(name="s", fn=_upper)
        assert step.condition is None

    def test_condition_stored(self):
        cond = lambda t: len(t) > 0
        step = PipelineStep(name="s", fn=_upper, condition=cond)
        assert step.condition is cond


# ===========================================================================
# StepOutput dataclass
# ===========================================================================

class TestStepOutput:
    def test_fields_stored(self):
        so = StepOutput(step_name="s", input="a", output="A")
        assert so.step_name == "s"
        assert so.input == "a"
        assert so.output == "A"

    def test_skipped_default_false(self):
        so = StepOutput(step_name="s", input="a", output="a")
        assert so.skipped is False

    def test_skipped_can_be_true(self):
        so = StepOutput(step_name="s", input="a", output="a", skipped=True)
        assert so.skipped is True


# ===========================================================================
# Empty pipeline
# ===========================================================================

class TestEmptyPipeline:
    def test_empty_pipeline_returns_original(self):
        pipeline = TextPipeline()
        result = pipeline.run("hello")
        assert result.final == "hello"

    def test_empty_pipeline_empty_string(self):
        pipeline = TextPipeline()
        result = pipeline.run("")
        assert result.final == ""

    def test_empty_pipeline_steps_list_empty(self):
        pipeline = TextPipeline()
        result = pipeline.run("hello")
        assert result.steps == []

    def test_empty_pipeline_was_modified_false(self):
        pipeline = TextPipeline()
        result = pipeline.run("hello")
        assert result.was_modified is False

    def test_empty_pipeline_step_count(self):
        pipeline = TextPipeline()
        assert pipeline.step_count() == 0

    def test_empty_pipeline_step_names(self):
        pipeline = TextPipeline()
        assert pipeline.step_names() == []


# ===========================================================================
# Single step
# ===========================================================================

class TestSingleStep:
    def test_single_step_transforms_text(self):
        pipeline = TextPipeline([PipelineStep("upper", _upper)])
        result = pipeline.run("hello")
        assert result.final == "HELLO"

    def test_single_step_step_output_recorded(self):
        pipeline = TextPipeline([PipelineStep("upper", _upper)])
        result = pipeline.run("hello")
        assert len(result.steps) == 1
        assert result.steps[0].step_name == "upper"

    def test_single_step_input_in_output(self):
        pipeline = TextPipeline([PipelineStep("upper", _upper)])
        result = pipeline.run("hello")
        assert result.steps[0].input == "hello"

    def test_single_step_output_in_step_output(self):
        pipeline = TextPipeline([PipelineStep("upper", _upper)])
        result = pipeline.run("hello")
        assert result.steps[0].output == "HELLO"

    def test_single_step_not_skipped(self):
        pipeline = TextPipeline([PipelineStep("upper", _upper)])
        result = pipeline.run("hello")
        assert result.steps[0].skipped is False

    def test_single_step_was_modified_true(self):
        pipeline = TextPipeline([PipelineStep("upper", _upper)])
        result = pipeline.run("hello")
        assert result.was_modified is True

    def test_single_step_no_modification_was_modified_false(self):
        pipeline = TextPipeline([PipelineStep("noop", lambda t: t)])
        result = pipeline.run("hello")
        assert result.was_modified is False


# ===========================================================================
# Multi-step pipeline: chaining
# ===========================================================================

class TestMultiStep:
    def test_two_steps_chained(self):
        pipeline = TextPipeline([
            PipelineStep("strip", _strip),
            PipelineStep("upper", _upper),
        ])
        result = pipeline.run("  hello  ")
        assert result.final == "HELLO"

    def test_each_step_receives_previous_output(self):
        pipeline = TextPipeline([
            PipelineStep("strip", _strip),
            PipelineStep("upper", _upper),
        ])
        result = pipeline.run("  hello  ")
        assert result.steps[0].output == "hello"
        assert result.steps[1].input == "hello"

    def test_three_steps_order_matters(self):
        pipeline = TextPipeline([
            PipelineStep("lower", _lower),
            PipelineStep("replace_a", _replace_a),
            PipelineStep("bang", _add_bang),
        ])
        result = pipeline.run("ABC")
        # lower → "abc", replace_a → "Xbc", bang → "Xbc!"
        assert result.final == "Xbc!"

    def test_multi_step_records_count(self):
        pipeline = TextPipeline([
            PipelineStep("a", _upper),
            PipelineStep("b", _lower),
            PipelineStep("c", _strip),
        ])
        result = pipeline.run("hello")
        assert len(result.steps) == 3

    def test_multi_step_intermediate_inputs_recorded(self):
        pipeline = TextPipeline([
            PipelineStep("strip", _strip),
            PipelineStep("lower", _lower),
        ])
        result = pipeline.run("  HELLO  ")
        assert result.steps[0].input == "  HELLO  "
        assert result.steps[1].input == "HELLO"

    def test_real_strip_lower_replace(self):
        pipeline = TextPipeline([
            PipelineStep("strip", str.strip),
            PipelineStep("lower", str.lower),
            PipelineStep("replace", lambda t: t.replace(" ", "_")),
        ])
        result = pipeline.run("  Hello World  ")
        assert result.final == "hello_world"


# ===========================================================================
# Disabled steps
# ===========================================================================

class TestDisabledStep:
    def test_disabled_step_skipped(self):
        pipeline = TextPipeline([PipelineStep("upper", _upper, enabled=False)])
        result = pipeline.run("hello")
        assert result.steps[0].skipped is True

    def test_disabled_step_text_passes_through(self):
        pipeline = TextPipeline([PipelineStep("upper", _upper, enabled=False)])
        result = pipeline.run("hello")
        assert result.final == "hello"

    def test_disabled_step_output_equals_input(self):
        pipeline = TextPipeline([PipelineStep("upper", _upper, enabled=False)])
        result = pipeline.run("hello")
        assert result.steps[0].output == result.steps[0].input

    def test_disabled_middle_step_others_still_run(self):
        pipeline = TextPipeline([
            PipelineStep("lower", _lower),
            PipelineStep("upper", _upper, enabled=False),
            PipelineStep("bang", _add_bang),
        ])
        result = pipeline.run("Hello")
        assert result.final == "hello!"

    def test_all_disabled_returns_original(self):
        pipeline = TextPipeline([
            PipelineStep("a", _upper, enabled=False),
            PipelineStep("b", _lower, enabled=False),
        ])
        result = pipeline.run("Hello")
        assert result.final == "Hello"
        assert result.was_modified is False


# ===========================================================================
# Conditional steps
# ===========================================================================

class TestConditionalStep:
    def test_condition_true_step_runs(self):
        step = PipelineStep("upper", _upper, condition=lambda t: len(t) > 0)
        pipeline = TextPipeline([step])
        result = pipeline.run("hello")
        assert result.final == "HELLO"
        assert result.steps[0].skipped is False

    def test_condition_false_step_skipped(self):
        step = PipelineStep("upper", _upper, condition=lambda t: len(t) > 10)
        pipeline = TextPipeline([step])
        result = pipeline.run("hello")
        assert result.steps[0].skipped is True
        assert result.final == "hello"

    def test_condition_false_output_equals_input(self):
        step = PipelineStep("upper", _upper, condition=lambda t: False)
        pipeline = TextPipeline([step])
        result = pipeline.run("hello")
        assert result.steps[0].output == "hello"

    def test_condition_receives_current_input(self):
        """Condition is evaluated on the text *entering* that step."""
        seen: list[str] = []

        def cond(t: str) -> bool:
            seen.append(t)
            return True

        pipeline = TextPipeline([
            PipelineStep("lower", _lower),
            PipelineStep("upper", _upper, condition=cond),
        ])
        pipeline.run("  Hello  ")
        assert seen == ["  hello  "]

    def test_disabled_overrides_condition(self):
        """enabled=False means the step is always skipped, condition not checked."""
        called: list[bool] = []

        def cond(t: str) -> bool:
            called.append(True)
            return True

        step = PipelineStep("s", _upper, enabled=False, condition=cond)
        pipeline = TextPipeline([step])
        result = pipeline.run("hi")
        assert result.steps[0].skipped is True
        assert called == []  # condition never evaluated


# ===========================================================================
# PipelineResult properties
# ===========================================================================

class TestPipelineResult:
    def test_final_field(self):
        result = PipelineResult(final="done")
        assert result.final == "done"

    def test_steps_default_empty(self):
        result = PipelineResult(final="x")
        assert result.steps == []

    def test_was_modified_true(self):
        steps = [StepOutput(step_name="s", input="a", output="b")]
        result = PipelineResult(final="b", steps=steps)
        assert result.was_modified is True

    def test_was_modified_false_no_change(self):
        steps = [StepOutput(step_name="s", input="a", output="a")]
        result = PipelineResult(final="a", steps=steps)
        assert result.was_modified is False

    def test_was_modified_false_empty_steps(self):
        result = PipelineResult(final="a")
        assert result.was_modified is False

    def test_get_step_found(self):
        steps = [
            StepOutput(step_name="alpha", input="a", output="A"),
            StepOutput(step_name="beta", input="A", output="A!"),
        ]
        result = PipelineResult(final="A!", steps=steps)
        assert result.get_step("beta") is steps[1]

    def test_get_step_not_found(self):
        result = PipelineResult(final="x")
        assert result.get_step("missing") is None

    def test_get_step_returns_first_match_when_duplicate_names(self):
        steps = [
            StepOutput(step_name="dup", input="a", output="b"),
            StepOutput(step_name="dup", input="b", output="c"),
        ]
        result = PipelineResult(final="c", steps=steps)
        assert result.get_step("dup") is steps[0]

    def test_step_names_result(self):
        steps = [
            StepOutput(step_name="one", input="a", output="A"),
            StepOutput(step_name="two", input="A", output="A!"),
        ]
        result = PipelineResult(final="A!", steps=steps)
        assert result.step_names() == ["one", "two"]

    def test_step_names_empty_result(self):
        result = PipelineResult(final="x")
        assert result.step_names() == []


# ===========================================================================
# add_step — chaining
# ===========================================================================

class TestAddStep:
    def test_add_step_returns_self(self):
        pipeline = TextPipeline()
        step = PipelineStep("s", _upper)
        returned = pipeline.add_step(step)
        assert returned is pipeline

    def test_add_step_chainable(self):
        pipeline = (
            TextPipeline()
            .add_step(PipelineStep("strip", _strip))
            .add_step(PipelineStep("upper", _upper))
        )
        result = pipeline.run("  hello  ")
        assert result.final == "HELLO"

    def test_add_step_increments_count(self):
        pipeline = TextPipeline()
        pipeline.add_step(PipelineStep("s", _upper))
        assert pipeline.step_count() == 1

    def test_add_step_appended_at_end(self):
        pipeline = TextPipeline([PipelineStep("first", _upper)])
        pipeline.add_step(PipelineStep("second", _lower))
        assert pipeline.step_names() == ["first", "second"]


# ===========================================================================
# run_steps (subset execution)
# ===========================================================================

class TestRunSteps:
    def test_run_steps_single_name(self):
        pipeline = TextPipeline([
            PipelineStep("strip", _strip),
            PipelineStep("upper", _upper),
            PipelineStep("bang", _add_bang),
        ])
        result = pipeline.run_steps("  hello  ", ["upper"])
        assert result.final == "  HELLO  "

    def test_run_steps_subset_in_definition_order(self):
        pipeline = TextPipeline([
            PipelineStep("strip", _strip),
            PipelineStep("upper", _upper),
            PipelineStep("bang", _add_bang),
        ])
        result = pipeline.run_steps("  hello  ", ["strip", "bang"])
        # strip runs first → "hello", bang → "hello!"
        assert result.final == "hello!"

    def test_run_steps_empty_names_returns_original(self):
        pipeline = TextPipeline([PipelineStep("upper", _upper)])
        result = pipeline.run_steps("hello", [])
        assert result.final == "hello"
        assert result.steps == []

    def test_run_steps_records_only_selected(self):
        pipeline = TextPipeline([
            PipelineStep("a", _upper),
            PipelineStep("b", _lower),
            PipelineStep("c", _strip),
        ])
        result = pipeline.run_steps("hello", ["a", "c"])
        assert result.step_names() == ["a", "c"]

    def test_run_steps_name_not_in_pipeline_ignored(self):
        pipeline = TextPipeline([PipelineStep("real", _upper)])
        result = pipeline.run_steps("hello", ["real", "nonexistent"])
        assert result.final == "HELLO"
        assert len(result.steps) == 1


# ===========================================================================
# remove_step
# ===========================================================================

class TestRemoveStep:
    def test_remove_existing_returns_true(self):
        pipeline = TextPipeline([PipelineStep("s", _upper)])
        assert pipeline.remove_step("s") is True

    def test_remove_nonexistent_returns_false(self):
        pipeline = TextPipeline()
        assert pipeline.remove_step("missing") is False

    def test_remove_step_decrements_count(self):
        pipeline = TextPipeline([PipelineStep("s", _upper)])
        pipeline.remove_step("s")
        assert pipeline.step_count() == 0

    def test_remove_first_match_only(self):
        """When two steps share a name, only the first is removed."""
        pipeline = TextPipeline([
            PipelineStep("dup", _upper),
            PipelineStep("dup", _lower),
        ])
        pipeline.remove_step("dup")
        assert pipeline.step_count() == 1
        assert pipeline.step_names() == ["dup"]

    def test_remove_step_from_middle(self):
        pipeline = TextPipeline([
            PipelineStep("a", _upper),
            PipelineStep("b", _lower),
            PipelineStep("c", _strip),
        ])
        pipeline.remove_step("b")
        assert pipeline.step_names() == ["a", "c"]


# ===========================================================================
# step_count and step_names (pipeline-level)
# ===========================================================================

class TestStepCountAndNames:
    def test_step_count_zero(self):
        assert TextPipeline().step_count() == 0

    def test_step_count_multiple(self):
        pipeline = TextPipeline([
            PipelineStep("a", _upper),
            PipelineStep("b", _lower),
        ])
        assert pipeline.step_count() == 2

    def test_step_names_order(self):
        pipeline = TextPipeline([
            PipelineStep("first", _upper),
            PipelineStep("second", _lower),
            PipelineStep("third", _strip),
        ])
        assert pipeline.step_names() == ["first", "second", "third"]

    def test_step_names_with_duplicates(self):
        pipeline = TextPipeline([
            PipelineStep("dup", _upper),
            PipelineStep("dup", _lower),
        ])
        assert pipeline.step_names() == ["dup", "dup"]


# ===========================================================================
# clone
# ===========================================================================

class TestClone:
    def test_clone_produces_new_pipeline(self):
        original = TextPipeline([PipelineStep("s", _upper)])
        cloned = original.clone()
        assert cloned is not original

    def test_clone_same_step_count(self):
        original = TextPipeline([PipelineStep("s", _upper)])
        cloned = original.clone()
        assert cloned.step_count() == original.step_count()

    def test_clone_same_results(self):
        original = TextPipeline([PipelineStep("lower", _lower)])
        cloned = original.clone()
        assert cloned.run("HELLO").final == original.run("HELLO").final

    def test_clone_is_independent_add(self):
        original = TextPipeline([PipelineStep("a", _upper)])
        cloned = original.clone()
        cloned.add_step(PipelineStep("b", _lower))
        assert original.step_count() == 1
        assert cloned.step_count() == 2

    def test_clone_is_independent_remove(self):
        original = TextPipeline([
            PipelineStep("a", _upper),
            PipelineStep("b", _lower),
        ])
        cloned = original.clone()
        cloned.remove_step("a")
        assert original.step_count() == 2
        assert cloned.step_count() == 1

    def test_original_unaffected_by_clone_add(self):
        original = TextPipeline([PipelineStep("lower", _lower)])
        cloned = original.clone()
        cloned.add_step(PipelineStep("bang", _add_bang))
        result = original.run("HELLO")
        assert result.final == "hello"


# ===========================================================================
# Exception propagation
# ===========================================================================

class TestExceptionPropagation:
    def test_exception_in_step_propagates(self):
        pipeline = TextPipeline([PipelineStep("boom", _exploding)])
        with pytest.raises(ValueError, match="boom"):
            pipeline.run("hello")

    def test_exception_in_middle_step_propagates(self):
        pipeline = TextPipeline([
            PipelineStep("lower", _lower),
            PipelineStep("boom", _exploding),
            PipelineStep("upper", _upper),
        ])
        with pytest.raises(ValueError):
            pipeline.run("hello")

    def test_exception_type_preserved(self):
        def _type_error(t: str) -> str:
            raise TypeError("type problem")

        pipeline = TextPipeline([PipelineStep("te", _type_error)])
        with pytest.raises(TypeError, match="type problem"):
            pipeline.run("hello")


# ===========================================================================
# All steps skipped
# ===========================================================================

class TestAllStepsSkipped:
    def test_all_disabled_final_is_original(self):
        pipeline = TextPipeline([
            PipelineStep("a", _upper, enabled=False),
            PipelineStep("b", _lower, enabled=False),
            PipelineStep("c", _strip, enabled=False),
        ])
        result = pipeline.run("  Hello  ")
        assert result.final == "  Hello  "

    def test_all_condition_false_final_is_original(self):
        always_false = lambda t: False
        pipeline = TextPipeline([
            PipelineStep("a", _upper, condition=always_false),
            PipelineStep("b", _lower, condition=always_false),
        ])
        result = pipeline.run("Hello")
        assert result.final == "Hello"

    def test_all_skipped_was_modified_false(self):
        pipeline = TextPipeline([
            PipelineStep("s", _upper, enabled=False),
        ])
        result = pipeline.run("hello")
        assert result.was_modified is False

    def test_all_skipped_each_output_equals_input(self):
        pipeline = TextPipeline([
            PipelineStep("a", _upper, enabled=False),
            PipelineStep("b", _lower, enabled=False),
        ])
        result = pipeline.run("Hello")
        for so in result.steps:
            assert so.output == so.input


# ===========================================================================
# Steps with the same name (both run)
# ===========================================================================

class TestDuplicateStepNames:
    def test_two_steps_same_name_both_run(self):
        pipeline = TextPipeline([
            PipelineStep("transform", _upper),
            PipelineStep("transform", _add_bang),
        ])
        result = pipeline.run("hello")
        # upper → "HELLO", bang → "HELLO!"
        assert result.final == "HELLO!"

    def test_two_steps_same_name_records_both(self):
        pipeline = TextPipeline([
            PipelineStep("dup", _upper),
            PipelineStep("dup", _lower),
        ])
        result = pipeline.run("hello")
        assert len(result.steps) == 2

    def test_get_step_with_duplicates_returns_first(self):
        pipeline = TextPipeline([
            PipelineStep("dup", _upper),
            PipelineStep("dup", _lower),
        ])
        result = pipeline.run("hello")
        # first step uppercased → "HELLO"
        assert result.get_step("dup").output == "HELLO"


# ===========================================================================
# Real-world text transformations
# ===========================================================================

class TestRealTextTransformations:
    def test_strip_then_lower(self):
        pipeline = TextPipeline([
            PipelineStep("strip", str.strip),
            PipelineStep("lower", str.lower),
        ])
        result = pipeline.run("   HELLO WORLD   ")
        assert result.final == "hello world"

    def test_lower_then_replace_spaces(self):
        pipeline = TextPipeline([
            PipelineStep("lower", str.lower),
            PipelineStep("spaces", lambda t: t.replace(" ", "-")),
        ])
        result = pipeline.run("Hello World")
        assert result.final == "hello-world"

    def test_strip_lower_replace_combined(self):
        pipeline = TextPipeline([
            PipelineStep("strip", str.strip),
            PipelineStep("lower", str.lower),
            PipelineStep("replace", lambda t: t.replace(" ", "_")),
        ])
        result = pipeline.run("  FOO BAR  ")
        assert result.final == "foo_bar"

    def test_conditional_only_non_empty(self):
        pipeline = TextPipeline([
            PipelineStep("upper", _upper, condition=lambda t: bool(t.strip())),
        ])
        non_empty = pipeline.run("hello")
        empty = pipeline.run("")
        assert non_empty.final == "HELLO"
        assert empty.final == ""
        assert empty.steps[0].skipped is True

    def test_pipeline_init_with_steps_list(self):
        steps = [
            PipelineStep("a", _strip),
            PipelineStep("b", _lower),
        ]
        pipeline = TextPipeline(steps)
        result = pipeline.run("  HELLO  ")
        assert result.final == "hello"

    def test_pipeline_init_with_none_acts_as_empty(self):
        pipeline = TextPipeline(None)
        result = pipeline.run("hello")
        assert result.final == "hello"
        assert pipeline.step_count() == 0
