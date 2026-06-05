"""Span: single unit of distributed tracing work."""
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum


class SpanStatus(Enum):
    OK = "ok"
    ERROR = "error"
    TIMEOUT = "timeout"


@dataclass
class Span:
    """A single timed operation within a trace."""

    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    trace_id: str = ""
    parent_id: str | None = None
    name: str = ""
    start_ts: float = field(default_factory=time.time)
    end_ts: float | None = None
    status: SpanStatus = SpanStatus.OK
    tags: dict = field(default_factory=dict)
    error: str = ""

    def duration_ms(self) -> float | None:
        """Return span duration in milliseconds, or None if not finished."""
        if self.end_ts is None:
            return None
        return (self.end_ts - self.start_ts) * 1000

    def finish(self, status: SpanStatus = SpanStatus.OK, error: str = "") -> None:
        """Mark span as finished with given status and optional error message."""
        self.end_ts = time.time()
        self.status = status
        self.error = error

    def is_finished(self) -> bool:
        """Return True if the span has been finished."""
        return self.end_ts is not None

    def set_tag(self, key: str, value) -> None:
        """Attach a key/value tag to this span."""
        self.tags[key] = value
