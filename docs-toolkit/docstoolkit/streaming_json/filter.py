"""JSON path filtering on top of :class:`StreamingParser`.

The path syntax is intentionally simple:

* ``.`` separates path segments.
* ``*`` matches exactly one segment (key or array index).
* ``**`` matches zero or more segments.
* Numeric segments compare against integer array indices and against
  string keys that look like the number.
* Everything else compares as a literal string against the segment.

Examples
--------
``"users.*.name"`` matches ``("users", 0, "name")`` or
``("users", "alice", "name")``.

``"a.**.x"`` matches ``("a", "x")``, ``("a", "b", "x")`` and
``("a", "b", "c", "x")``.
"""

from __future__ import annotations

from typing import Any

from docstoolkit.streaming_json.parser import StreamEvent, StreamingParser


class JSONPathFilter:
    """Match :class:`StreamEvent` instances against a JSON-path-like pattern.

    Parameters
    ----------
    pattern:
        The pattern string, e.g. ``"users.*.name"``.  An empty pattern
        matches only the root path (``()``).
    """

    def __init__(self, pattern: str) -> None:
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a string")
        self.pattern = pattern
        self._segments: list[str] = self._split(pattern)

    @staticmethod
    def _split(pattern: str) -> list[str]:
        if pattern == "":
            return []
        # Split on dots but keep ``**`` as a single segment for clarity.
        return pattern.split(".")

    def match(self, event: StreamEvent) -> bool:
        """Return ``True`` if ``event.path`` matches this filter."""
        return self._match_path(event.path)

    def match_path(self, path: tuple) -> bool:
        """Public alias used by :class:`StreamFilter`."""
        return self._match_path(path)

    # ------------------------------------------------------------------
    def _match_path(self, path: tuple) -> bool:
        return _glob_match(self._segments, list(path))


def _segment_equal(pattern_seg: str, path_seg: Any) -> bool:
    """Check a single literal segment.

    Numeric strings in the pattern also match integer indices in the path.
    """
    if pattern_seg == "*":
        return True
    if isinstance(path_seg, int):
        if pattern_seg.lstrip("-").isdigit():
            try:
                return int(pattern_seg) == path_seg
            except ValueError:
                return False
        # Allow ``*`` already handled; otherwise string compare with str(idx)
        return pattern_seg == str(path_seg)
    return pattern_seg == path_seg


def _glob_match(pattern: list[str], path: list[Any]) -> bool:
    """Recursive glob matcher supporting ``*`` (single) and ``**`` (multi)."""
    # Standard recursive glob — small inputs so recursion depth is fine.
    if not pattern:
        return not path
    head, *tail = pattern
    if head == "**":
        # Match zero or more path segments.
        # Zero segments — consume `**` and try remaining pattern.
        if _glob_match(tail, path):
            return True
        # One or more — consume one path segment and keep `**`.
        if path and _glob_match(pattern, path[1:]):
            return True
        return False
    if not path:
        return False
    if _segment_equal(head, path[0]):
        return _glob_match(tail, path[1:])
    return False


class StreamFilter:
    """High-level selector over a JSON document.

    Wraps a :class:`StreamingParser` and returns the **values** at paths
    matching a given pattern.

    Only scalar ``"value"`` events whose path matches the pattern are
    returned; containers and key events are skipped because they do not
    carry a meaningful value.
    """

    def __init__(self, parser: StreamingParser) -> None:
        self.parser = parser

    def select(self, text: str, pattern: str) -> list:
        """Parse ``text`` and return values whose path matches ``pattern``."""
        path_filter = JSONPathFilter(pattern)
        results: list = []
        for event in self.parser.parse(text):
            if event.event_type != "value":
                continue
            if path_filter.match(event):
                results.append(event.value)
        return results
