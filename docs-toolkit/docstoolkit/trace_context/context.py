"""TraceContext — thread-local current-span stack."""
from __future__ import annotations

import threading
from typing import Optional

from docstoolkit.trace_context.trace import Span


class TraceContext:
    """Thread-local stack of currently active spans.

    Each thread maintains its own independent stack — pushing a span in one
    thread does not affect any other thread's current span.
    """

    def __init__(self) -> None:
        self._current = threading.local()

    def _stack(self) -> list[Span]:
        """Return (creating if needed) this thread's span stack."""
        if not hasattr(self._current, "stack"):
            self._current.stack = []
        return self._current.stack

    def current_span(self) -> Optional[Span]:
        """Return the top of the current thread's stack, or None if empty."""
        stack = self._stack()
        return stack[-1] if stack else None

    def push(self, span: Span) -> None:
        """Push a span onto the current thread's stack."""
        self._stack().append(span)

    def pop(self) -> Optional[Span]:
        """Pop and return the top span, or None if the stack is empty."""
        stack = self._stack()
        if not stack:
            return None
        return stack.pop()

    def get_trace_id(self) -> str:
        """Return the trace_id of the current span, or '' if none."""
        span = self.current_span()
        return span.trace_id if span is not None else ""


# Single process-wide context. Thread-locality lives inside `_current`.
_GLOBAL_CONTEXT = TraceContext()


def get_current_span() -> Optional[Span]:
    """Return the current span from the global context (or None)."""
    return _GLOBAL_CONTEXT.current_span()


def set_current_span(span: Optional[Span]) -> None:
    """Convenience: push *span* if non-None, otherwise pop the top of the stack."""
    if span is None:
        _GLOBAL_CONTEXT.pop()
    else:
        _GLOBAL_CONTEXT.push(span)
