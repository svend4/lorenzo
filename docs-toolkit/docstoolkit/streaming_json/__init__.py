"""Streaming JSON parser/filter/builder (E91).

Pure stdlib.  Provides a streaming-style API for traversing, filtering and
constructing JSON documents.

Public API
----------
JSONStreamError   — invalid JSON encountered by the streaming parser
StreamEvent       — single event yielded by the parser
StreamingParser   — walks JSON and yields events
JSONPathFilter    — match events against a path pattern
StreamFilter      — high-level value selector
StreamingBuilder  — assemble a JSON string incrementally
"""

from docstoolkit.streaming_json.parser import (
    JSONStreamError,
    StreamEvent,
    StreamingParser,
)
from docstoolkit.streaming_json.filter import JSONPathFilter, StreamFilter
from docstoolkit.streaming_json.builder import StreamingBuilder

__all__ = [
    "JSONStreamError",
    "StreamEvent",
    "StreamingParser",
    "JSONPathFilter",
    "StreamFilter",
    "StreamingBuilder",
]
