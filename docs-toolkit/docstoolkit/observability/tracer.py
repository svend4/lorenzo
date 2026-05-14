"""Tracer: manages traces and spans for distributed tracing."""
import time
import uuid
from dataclasses import dataclass, field

from docstoolkit.observability.span import Span, SpanStatus


@dataclass
class Trace:
    """A collection of spans sharing the same trace_id."""

    trace_id: str
    spans: list[Span] = field(default_factory=list)
    created_ts: float = field(default_factory=time.time)

    def root_span(self) -> Span | None:
        """Return the span with no parent (root of the trace tree)."""
        for span in self.spans:
            if span.parent_id is None:
                return span
        return None

    def child_spans(self, parent_id: str) -> list[Span]:
        """Return all spans whose parent_id matches the given id."""
        return [s for s in self.spans if s.parent_id == parent_id]

    def total_duration_ms(self) -> float | None:
        """Return root span duration in milliseconds, or None if unavailable."""
        root = self.root_span()
        if root is None:
            return None
        return root.duration_ms()

    def has_errors(self) -> bool:
        """Return True if any span in the trace has ERROR or TIMEOUT status."""
        return any(
            s.status in (SpanStatus.ERROR, SpanStatus.TIMEOUT)
            for s in self.spans
        )

    def span_count(self) -> int:
        """Return the total number of spans in this trace."""
        return len(self.spans)


class Tracer:
    """Creates and manages distributed traces and their spans."""

    def __init__(self):
        self._traces: dict[str, Trace] = {}

    def start_trace(self, name: str = "") -> tuple[str, Span]:
        """Start a new trace and return (trace_id, root_span)."""
        trace_id = uuid.uuid4().hex
        root = Span(trace_id=trace_id, parent_id=None, name=name)
        trace = Trace(trace_id=trace_id, spans=[root])
        self._traces[trace_id] = trace
        return trace_id, root

    def start_span(self, trace_id: str, name: str, parent_id: str = None) -> Span:
        """Create and register a new child span within an existing trace."""
        span = Span(trace_id=trace_id, parent_id=parent_id, name=name)
        if trace_id in self._traces:
            self._traces[trace_id].spans.append(span)
        return span

    def finish_span(self, span: Span, status: SpanStatus = SpanStatus.OK, error: str = "") -> None:
        """Finish a span with the given status and optional error."""
        span.finish(status=status, error=error)

    def get_trace(self, trace_id: str) -> Trace | None:
        """Return the Trace for the given trace_id, or None if not found."""
        return self._traces.get(trace_id)

    def finish_trace(self, trace_id: str) -> Trace | None:
        """Finish all open spans in a trace and return it, or None if not found."""
        trace = self._traces.get(trace_id)
        if trace is None:
            return None
        for span in trace.spans:
            if not span.is_finished():
                span.finish()
        return trace

    def active_traces(self) -> int:
        """Return the number of traces that have at least one unfinished span."""
        count = 0
        for trace in self._traces.values():
            if any(not s.is_finished() for s in trace.spans):
                count += 1
        return count
