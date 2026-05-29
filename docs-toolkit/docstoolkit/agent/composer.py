"""Tool composition for agentic workflows (Phase XIX).

Allows chaining tools in pipelines and parallel fan-out patterns so that
complex multi-step operations can be expressed declaratively rather than
wiring individual callables by hand.

Patterns supported:
* **Sequential** — output of each tool is passed as input to the next.
* **Parallel** — all tools run (in-process) and results are collected.
* **Conditional** — route to different tools based on a predicate.
* **Retry** — retry a tool on failure with configurable backoff.
* **Fallback** — try tools in order until one succeeds.

Pure stdlib — no external dependencies.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Sequence, Tuple


# ---------------------------------------------------------------------------
# Tool protocol
# ---------------------------------------------------------------------------

Tool = Callable[[Any], Any]   # (input) → output


# ---------------------------------------------------------------------------
# Composition building blocks
# ---------------------------------------------------------------------------

class SequentialPipeline:
    """Run tools one after another, piping output → input.

    Parameters
    ----------
    tools:
        Sequence of callables.  Each receives the previous tool's output
        (or the initial input for the first tool).
    name:
        Optional label used in trace output.
    """

    def __init__(self, tools: Sequence[Tool], name: str = "sequential") -> None:
        self.tools = list(tools)
        self.name = name

    def __call__(self, input: Any) -> Any:
        value = input
        for tool in self.tools:
            value = tool(value)
        return value

    def __repr__(self) -> str:
        return f"SequentialPipeline({[getattr(t, '__name__', repr(t)) for t in self.tools]})"


class ParallelFanOut:
    """Run all tools with the same input and collect results in a list.

    Parameters
    ----------
    tools:
        Sequence of callables, each invoked with the same input.
    name:
        Optional label.
    """

    def __init__(self, tools: Sequence[Tool], name: str = "parallel") -> None:
        self.tools = list(tools)
        self.name = name

    def __call__(self, input: Any) -> List[Any]:
        return [tool(input) for tool in self.tools]

    def __repr__(self) -> str:
        return f"ParallelFanOut({[getattr(t, '__name__', repr(t)) for t in self.tools]})"


class ConditionalRoute:
    """Route input to different tools based on a predicate.

    Parameters
    ----------
    predicate:
        ``(input) → bool`` — if True, *true_branch* is called; otherwise
        *false_branch* (if provided) is called or the input is returned as-is.
    true_branch:
        Tool called when predicate is truthy.
    false_branch:
        Tool called when predicate is falsy.  If None, input is passed through.
    """

    def __init__(
        self,
        predicate: Callable[[Any], bool],
        true_branch: Tool,
        false_branch: Optional[Tool] = None,
        name: str = "conditional",
    ) -> None:
        self.predicate = predicate
        self.true_branch = true_branch
        self.false_branch = false_branch
        self.name = name

    def __call__(self, input: Any) -> Any:
        if self.predicate(input):
            return self.true_branch(input)
        if self.false_branch is not None:
            return self.false_branch(input)
        return input   # pass-through


class RetryWrapper:
    """Retry *tool* on exception with configurable backoff.

    Parameters
    ----------
    tool:
        The callable to wrap.
    max_retries:
        Number of *additional* attempts after the first (0 = try once).
    initial_delay:
        Seconds to wait before the first retry.
    backoff_factor:
        Multiplier applied to the delay on each retry.
    exceptions:
        Tuple of exception types to catch.  Other exceptions propagate.
    """

    def __init__(
        self,
        tool: Tool,
        max_retries: int = 3,
        initial_delay: float = 0.5,
        backoff_factor: float = 2.0,
        exceptions: Tuple[type, ...] = (Exception,),
        name: str = "retry",
    ) -> None:
        self.tool = tool
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor
        self.exceptions = exceptions
        self.name = name

    def __call__(self, input: Any) -> Any:
        delay = self.initial_delay
        last_exc: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                return self.tool(input)
            except self.exceptions as exc:
                last_exc = exc
                if attempt < self.max_retries:
                    time.sleep(delay)
                    delay *= self.backoff_factor

        raise last_exc   # type: ignore[misc]


class FallbackChain:
    """Try tools in order and return the first successful result.

    Parameters
    ----------
    tools:
        Sequence of callables tried in order.
    exceptions:
        Exceptions that count as failure (trigger the next tool).
    """

    def __init__(
        self,
        tools: Sequence[Tool],
        exceptions: Tuple[type, ...] = (Exception,),
        name: str = "fallback",
    ) -> None:
        self.tools = list(tools)
        self.exceptions = exceptions
        self.name = name

    def __call__(self, input: Any) -> Any:
        last_exc: Optional[Exception] = None
        for tool in self.tools:
            try:
                return tool(input)
            except self.exceptions as exc:
                last_exc = exc
        raise last_exc or RuntimeError("All fallbacks failed")   # type: ignore[misc]


# ---------------------------------------------------------------------------
# Trace-aware wrapper
# ---------------------------------------------------------------------------

@dataclass
class ToolTrace:
    """Execution trace for a single tool call."""
    tool_name: str
    input: Any
    output: Any = None
    error: Optional[str] = None
    duration_ms: float = 0.0
    success: bool = True

    def to_dict(self) -> dict:
        return {
            "tool": self.tool_name,
            "duration_ms": self.duration_ms,
            "success": self.success,
            "error": self.error,
        }


class TracedTool:
    """Wraps any tool and records an execution trace."""

    def __init__(self, tool: Tool, name: Optional[str] = None) -> None:
        self.tool = tool
        self.name = name or getattr(tool, "__name__", repr(tool))
        self.traces: List[ToolTrace] = []

    def __call__(self, input: Any) -> Any:
        start = time.monotonic()
        trace = ToolTrace(tool_name=self.name, input=input)
        try:
            result = self.tool(input)
            trace.output = result
            return result
        except Exception as exc:
            trace.error = str(exc)
            trace.success = False
            raise
        finally:
            trace.duration_ms = (time.monotonic() - start) * 1000
            self.traces.append(trace)

    def last_trace(self) -> Optional[ToolTrace]:
        return self.traces[-1] if self.traces else None


# ---------------------------------------------------------------------------
# Declarative compose helper
# ---------------------------------------------------------------------------

def compose(*tools: Tool) -> SequentialPipeline:
    """Shorthand: compose(a, b, c) → SequentialPipeline([a, b, c])."""
    return SequentialPipeline(tools)


def parallel(*tools: Tool) -> ParallelFanOut:
    """Shorthand: parallel(a, b, c) → ParallelFanOut([a, b, c])."""
    return ParallelFanOut(tools)


def when(
    predicate: Callable[[Any], bool],
    then: Tool,
    otherwise: Optional[Tool] = None,
) -> ConditionalRoute:
    """Shorthand: when(pred, then_tool, else_tool)."""
    return ConditionalRoute(predicate, then, otherwise)


def retry(
    tool: Tool,
    times: int = 3,
    delay: float = 0.5,
    backoff: float = 2.0,
) -> RetryWrapper:
    """Shorthand: retry(tool, times=3)."""
    return RetryWrapper(tool, max_retries=times, initial_delay=delay, backoff_factor=backoff)


def fallback(*tools: Tool) -> FallbackChain:
    """Shorthand: fallback(primary, secondary, tertiary)."""
    return FallbackChain(tools)
