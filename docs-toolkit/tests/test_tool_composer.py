"""Tests for docstoolkit.agent.composer — tool composition primitives."""
from __future__ import annotations

import pytest

from docstoolkit.agent import (
    SequentialPipeline, ParallelFanOut, ConditionalRoute,
    RetryWrapper, FallbackChain, TracedTool, ToolTrace,
    compose, parallel, when, retry, fallback,
)


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def double(x):
    return x * 2

def add_one(x):
    return x + 1

def stringify(x):
    return str(x)

def always_fail(x):
    raise ValueError("I always fail")

def always_succeed(x):
    return f"ok:{x}"

def negate(x):
    return -x


# ===========================================================================
# SequentialPipeline
# ===========================================================================

class TestSequentialPipeline:
    def test_single_tool(self):
        pipe = SequentialPipeline([double])
        assert pipe(5) == 10

    def test_two_tools_piped(self):
        pipe = SequentialPipeline([double, add_one])
        assert pipe(3) == 7   # 3*2 + 1

    def test_three_tools(self):
        pipe = SequentialPipeline([double, add_one, stringify])
        assert pipe(5) == "11"  # ((5*2)+1) → "11"

    def test_empty_pipeline_returns_input(self):
        pipe = SequentialPipeline([])
        assert pipe("hello") == "hello"

    def test_repr_contains_name(self):
        pipe = SequentialPipeline([double, add_one], name="my-pipe")
        assert "double" in repr(pipe) or "SequentialPipeline" in repr(pipe)


# ===========================================================================
# ParallelFanOut
# ===========================================================================

class TestParallelFanOut:
    def test_single_tool(self):
        fan = ParallelFanOut([double])
        assert fan(3) == [6]

    def test_multiple_tools(self):
        fan = ParallelFanOut([double, add_one, negate])
        results = fan(4)
        assert results == [8, 5, -4]

    def test_all_same_input(self):
        calls = []
        def record(x):
            calls.append(x)
            return x
        fan = ParallelFanOut([record, record, record])
        fan(42)
        assert calls == [42, 42, 42]

    def test_empty_returns_empty_list(self):
        fan = ParallelFanOut([])
        assert fan("x") == []


# ===========================================================================
# ConditionalRoute
# ===========================================================================

class TestConditionalRoute:
    def test_true_branch_taken(self):
        route = ConditionalRoute(lambda x: x > 0, double, negate)
        assert route(5) == 10

    def test_false_branch_taken(self):
        route = ConditionalRoute(lambda x: x > 0, double, negate)
        assert route(-3) == 3  # negate(-3) = 3

    def test_no_false_branch_passthrough(self):
        route = ConditionalRoute(lambda x: False, double)
        assert route(99) == 99  # passthrough

    def test_true_branch_on_edge(self):
        route = ConditionalRoute(lambda x: x == 0, double, add_one)
        assert route(0) == 0   # double(0)
        assert route(1) == 2   # add_one(1)


# ===========================================================================
# RetryWrapper
# ===========================================================================

class TestRetryWrapper:
    def test_succeeds_first_try(self):
        r = RetryWrapper(always_succeed, max_retries=3, initial_delay=0.0)
        assert r("x") == "ok:x"

    def test_fails_all_raises_last(self):
        r = RetryWrapper(always_fail, max_retries=2, initial_delay=0.0)
        with pytest.raises(ValueError, match="I always fail"):
            r("x")

    def test_retries_before_success(self):
        call_count = [0]

        def flaky(x):
            call_count[0] += 1
            if call_count[0] < 3:
                raise RuntimeError("not yet")
            return "success"

        r = RetryWrapper(flaky, max_retries=3, initial_delay=0.0)
        result = r("input")
        assert result == "success"
        assert call_count[0] == 3

    def test_specific_exception_type(self):
        def raises_type_error(x):
            raise TypeError("wrong type")

        # Only retries ValueError, not TypeError
        r = RetryWrapper(raises_type_error, max_retries=2, initial_delay=0.0,
                         exceptions=(ValueError,))
        with pytest.raises(TypeError):
            r("x")

    def test_zero_retries_no_extra_calls(self):
        calls = [0]

        def fail_once(x):
            calls[0] += 1
            raise RuntimeError("fail")

        r = RetryWrapper(fail_once, max_retries=0, initial_delay=0.0)
        with pytest.raises(RuntimeError):
            r("x")
        assert calls[0] == 1


# ===========================================================================
# FallbackChain
# ===========================================================================

class TestFallbackChain:
    def test_first_tool_succeeds(self):
        chain = FallbackChain([always_succeed, double])
        assert chain("x") == "ok:x"

    def test_falls_through_to_second(self):
        chain = FallbackChain([always_fail, always_succeed])
        assert chain("y") == "ok:y"

    def test_all_fail_raises(self):
        chain = FallbackChain([always_fail, always_fail])
        with pytest.raises(ValueError):
            chain("z")

    def test_only_specified_exceptions_caught(self):
        def raises_runtime(x):
            raise RuntimeError("runtime")

        chain = FallbackChain([raises_runtime, always_succeed],
                               exceptions=(ValueError,))
        # RuntimeError is not caught, should propagate
        with pytest.raises(RuntimeError):
            chain("x")

    def test_empty_raises_runtime(self):
        chain = FallbackChain([])
        with pytest.raises(RuntimeError):
            chain("x")


# ===========================================================================
# TracedTool
# ===========================================================================

class TestTracedTool:
    def test_wraps_callable(self):
        traced = TracedTool(double, name="double")
        assert traced(5) == 10

    def test_records_trace_on_success(self):
        traced = TracedTool(double)
        traced(3)
        trace = traced.last_trace()
        assert trace is not None
        assert trace.success is True
        assert trace.error is None
        assert trace.duration_ms >= 0

    def test_records_trace_on_failure(self):
        traced = TracedTool(always_fail)
        with pytest.raises(ValueError):
            traced("x")
        trace = traced.last_trace()
        assert trace.success is False
        assert trace.error == "I always fail"

    def test_multiple_calls_accumulate_traces(self):
        traced = TracedTool(double)
        traced(1)
        traced(2)
        traced(3)
        assert len(traced.traces) == 3

    def test_trace_to_dict(self):
        traced = TracedTool(add_one, name="add_one")
        traced(10)
        d = traced.last_trace().to_dict()
        assert d["tool"] == "add_one"
        assert d["success"] is True

    def test_no_trace_initially(self):
        traced = TracedTool(double)
        assert traced.last_trace() is None

    def test_name_from_function(self):
        traced = TracedTool(double)
        assert "double" in traced.name


# ===========================================================================
# Shorthand functions
# ===========================================================================

class TestShorthands:
    def test_compose(self):
        pipe = compose(double, add_one)
        assert isinstance(pipe, SequentialPipeline)
        assert pipe(3) == 7

    def test_parallel(self):
        fan = parallel(double, add_one)
        assert isinstance(fan, ParallelFanOut)
        assert fan(2) == [4, 3]

    def test_when(self):
        route = when(lambda x: x > 0, double, negate)
        assert isinstance(route, ConditionalRoute)
        assert route(5) == 10

    def test_retry(self):
        r = retry(always_succeed, times=3)
        assert isinstance(r, RetryWrapper)
        assert r("a") == "ok:a"

    def test_fallback(self):
        chain = fallback(always_fail, always_succeed)
        assert isinstance(chain, FallbackChain)
        assert chain("x") == "ok:x"


# ===========================================================================
# Composition of compositions
# ===========================================================================

class TestNestedComposition:
    def test_sequential_of_parallel(self):
        fan = parallel(double, add_one)    # [2x, x+1]
        pipe = compose(fan, lambda lst: sum(lst))
        assert pipe(3) == 10   # sum([6, 4])

    def test_fallback_with_retry(self):
        call_count = [0]

        def sometimes_fail(x):
            call_count[0] += 1
            if call_count[0] < 3:
                raise ValueError("try again")
            return "finally"

        chain = fallback(
            retry(sometimes_fail, times=5, delay=0.0),
            always_succeed,
        )
        result = chain("x")
        assert result == "finally"

    def test_traced_in_pipeline(self):
        traced_double = TracedTool(double, name="double")
        pipe = compose(traced_double, add_one)
        assert pipe(4) == 9   # 4*2 + 1
        assert traced_double.last_trace().success is True

    def test_conditional_with_sequential(self):
        positive_pipe = compose(double, add_one)   # 2x+1 for positive
        route = when(lambda x: x > 0, positive_pipe, negate)
        assert route(3) == 7   # 3*2+1
        assert route(-2) == 2  # negate(-2)
