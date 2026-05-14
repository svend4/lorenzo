"""Tracer — creates spans, manages parent/child linking, exports results."""
from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Iterator, Optional

from docstoolkit.trace_context.context import _GLOBAL_CONTEXT
from docstoolkit.trace_context.trace import Span, SpanKind, SpanStatus


class Tracer:
    """Lightweight tracer with an in-memory completed-span buffer."""

    def __init__(self, service_name: str = "default") -> None:
        self.service_name = service_name
        self._spans: list[Span] = []

    # ------------------------------------------------------------------ core
    def start_span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        parent: Optional[Span] = None,
        attributes: Optional[dict] = None,
    ) -> Span:
        """Create a new span, mark it as started, and push it as current.

        If *parent* is None we use the current span from the global context,
        inheriting its trace_id and span_id so the spans form a tree.
        """
        span = Span(name=name, kind=kind)

        effective_parent = parent if parent is not None else _GLOBAL_CONTEXT.current_span()
        if effective_parent is not None:
            span.trace_id = effective_parent.trace_id
            span.parent_span_id = effective_parent.span_id

        if attributes:
            span.attributes.update(attributes)

        span.start_time = time.time()
        _GLOBAL_CONTEXT.push(span)
        return span

    def end_span(self, span: Span, status: SpanStatus = SpanStatus.OK) -> None:
        """Stamp the span as ended, set status, pop it, and record it."""
        span.end_time = time.time()
        span.status = status
        # Pop only if the span is the current top; otherwise pop regardless to
        # keep the stack drained (start/end pairs are expected to be balanced).
        current = _GLOBAL_CONTEXT.current_span()
        if current is span:
            _GLOBAL_CONTEXT.pop()
        else:
            # Best-effort: remove any reference to *span* from the stack.
            stack = _GLOBAL_CONTEXT._stack()
            try:
                stack.remove(span)
            except ValueError:
                pass
        self._spans.append(span)

    # --------------------------------------------------------- context manager
    @contextmanager
    def span(
        self,
        name: str,
        kind: SpanKind = SpanKind.INTERNAL,
        attributes: Optional[dict] = None,
    ) -> Iterator[Span]:
        """Run a block as a span; auto-ends with OK or ERROR on exception."""
        sp = self.start_span(name=name, kind=kind, attributes=attributes)
        try:
            yield sp
        except Exception as exc:
            sp.set_status(SpanStatus.ERROR, description=str(exc))
            self.end_span(sp, status=SpanStatus.ERROR)
            raise
        else:
            self.end_span(sp, status=SpanStatus.OK)

    # ------------------------------------------------------------- introspect
    def get_spans(self) -> list[Span]:
        """Return a snapshot of completed spans (defensive copy)."""
        return list(self._spans)

    def clear(self) -> None:
        """Discard all recorded spans."""
        self._spans.clear()

    def export(self) -> list[dict]:
        """Serialize all recorded spans into a list of plain dicts."""
        result = []
        for sp in self._spans:
            result.append({
                "trace_id": sp.trace_id,
                "span_id": sp.span_id,
                "parent_span_id": sp.parent_span_id,
                "name": sp.name,
                "kind": sp.kind.name if isinstance(sp.kind, SpanKind) else str(sp.kind),
                "status": sp.status.name if isinstance(sp.status, SpanStatus) else str(sp.status),
                "start_time": sp.start_time,
                "end_time": sp.end_time,
                "duration": sp.duration(),
                "attributes": dict(sp.attributes),
                "events": list(sp.events),
                "service_name": self.service_name,
            })
        return result
