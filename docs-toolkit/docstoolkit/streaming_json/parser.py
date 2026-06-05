"""Streaming JSON parser (E91).

Pure stdlib. Presents a streaming-style API on top of :mod:`json`.

The parser uses :class:`json.JSONDecoder.raw_decode` to materialise the JSON
tree, then walks it lazily, yielding :class:`StreamEvent` objects as it
encounters containers, keys and scalar values.

This is **not** a true incremental parser — the full document is decoded
first.  The streaming API allows downstream consumers to filter or transform
the document without having to keep a parallel representation of it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Iterator


class JSONStreamError(Exception):
    """Raised when invalid JSON is encountered by the streaming parser."""


@dataclass
class StreamEvent:
    """A single event emitted by :class:`StreamingParser`.

    Attributes
    ----------
    event_type:
        One of ``"start_object"``, ``"end_object"``, ``"start_array"``,
        ``"end_array"``, ``"key"``, ``"value"``.
    value:
        For ``"key"`` events this is the key string.  For ``"value"`` events
        this is the scalar value (``str``, ``int``, ``float``, ``bool`` or
        ``None``).  ``None`` for container start/end events.
    path:
        Tuple representing the JSON path of the event.  Each element is
        either a key (``str``) or an array index (``int``).
    """

    event_type: str
    value: Any = None
    path: tuple = field(default_factory=tuple)


class StreamingParser:
    """Walk a JSON document and yield :class:`StreamEvent` instances.

    The parser uses :func:`json.JSONDecoder.raw_decode` so any document that
    is valid JSON is accepted.
    """

    def __init__(self) -> None:
        self._decoder = json.JSONDecoder()

    # ------------------------------------------------------------------ API
    def parse(self, text: str) -> Iterator[StreamEvent]:
        """Parse a JSON document and yield events.

        Parameters
        ----------
        text:
            Raw JSON text.  Leading whitespace is ignored.

        Raises
        ------
        JSONStreamError
            If ``text`` is not valid JSON.
        """
        if not isinstance(text, str):
            raise JSONStreamError("input must be a string")
        stripped = text.lstrip()
        if not stripped:
            raise JSONStreamError("empty input")
        try:
            obj, _end = self._decoder.raw_decode(stripped)
        except json.JSONDecodeError as exc:
            raise JSONStreamError(f"invalid JSON: {exc.msg}") from exc
        yield from self._walk(obj, ())

    def parse_file(self, path: str) -> Iterator[StreamEvent]:
        """Read ``path`` and yield events for its JSON contents."""
        try:
            with open(path, "r", encoding="utf-8") as handle:
                text = handle.read()
        except OSError as exc:
            raise JSONStreamError(f"cannot read file {path!r}: {exc}") from exc
        yield from self.parse(text)

    # -------------------------------------------------------------- helpers
    def _walk(self, obj: Any, path: tuple) -> Iterator[StreamEvent]:
        """Recursively walk ``obj`` yielding events at ``path``."""
        if isinstance(obj, dict):
            yield StreamEvent("start_object", None, path)
            for key, value in obj.items():
                key_str = key if isinstance(key, str) else str(key)
                child_path = path + (key_str,)
                yield StreamEvent("key", key_str, child_path)
                yield from self._walk(value, child_path)
            yield StreamEvent("end_object", None, path)
        elif isinstance(obj, list):
            yield StreamEvent("start_array", None, path)
            for index, item in enumerate(obj):
                child_path = path + (index,)
                yield from self._walk(item, child_path)
            yield StreamEvent("end_array", None, path)
        else:
            # Scalar — str / int / float / bool / None
            yield StreamEvent("value", obj, path)
