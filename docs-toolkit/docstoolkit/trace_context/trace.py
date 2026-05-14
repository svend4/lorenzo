"""Span, SpanKind, SpanStatus — primitives for distributed tracing."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4


class SpanKind(str, Enum):
    """OpenTelemetry-compatible span kinds."""
    INTERNAL = "INTERNAL"
    SERVER = "SERVER"
    CLIENT = "CLIENT"
    PRODUCER = "PRODUCER"
    CONSUMER = "CONSUMER"


class SpanStatus(str, Enum):
    """Status codes for a span."""
    UNSET = "UNSET"
    OK = "OK"
    ERROR = "ERROR"


@dataclass
class Span:
    """A single tracing span.

    `trace_id` is a 32-character hex string (group of related spans).
    `span_id` is a 16-character hex string (this individual operation).
    """
    trace_id: str = field(default_factory=lambda: uuid4().hex)
    span_id: str = field(default_factory=lambda: uuid4().hex[:16])
    parent_span_id: str = ""
    name: str = ""
    kind: SpanKind = SpanKind.INTERNAL
    status: SpanStatus = SpanStatus.UNSET
    start_time: float = 0.0
    end_time: float = 0.0
    attributes: dict = field(default_factory=dict)
    events: list = field(default_factory=list)

    def duration(self) -> float:
        """Return end_time - start_time when both are set, else 0.0."""
        if self.start_time > 0 and self.end_time > 0:
            return self.end_time - self.start_time
        return 0.0

    def set_attribute(self, key: str, value: Any) -> None:
        """Set a single attribute on this span."""
        self.attributes[key] = value

    def add_event(
        self,
        name: str,
        attributes: dict | None = None,
        timestamp: float | None = None,
    ) -> None:
        """Append a timestamped event to this span."""
        ts = timestamp if timestamp is not None else time.time()
        self.events.append((ts, name, attributes or {}))

    def set_status(self, status: SpanStatus, description: str = "") -> None:
        """Update the span status; stash description in attributes if given."""
        self.status = status
        if description:
            self.attributes["status.description"] = description

    def is_recording(self) -> bool:
        """A span is recording iff it has started but not ended."""
        return self.start_time > 0 and self.end_time == 0
