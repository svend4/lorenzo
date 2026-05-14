"""Incremental JSON builder.

:class:`StreamingBuilder` assembles a JSON document piece by piece without
materialising the full Python object first.  Internally it keeps a list of
text fragments and a stack of the currently-open containers; scalars are
serialised through :func:`json.dumps` so escaping is always correct.
"""

from __future__ import annotations

import json
from typing import Any


class StreamingBuilder:
    """Build a JSON document incrementally.

    The builder maintains a stack describing the currently-open containers.
    Each stack frame is a ``["object" | "array", item_count]`` pair used to
    decide whether a leading comma is required before the next item.

    Inside an object every item must be added with a string ``key``; inside
    an array ``key`` must be ``None``.  At the top level, exactly one value
    must be produced.
    """

    _OBJECT = "object"
    _ARRAY = "array"

    def __init__(self) -> None:
        self._parts: list[str] = []
        self._stack: list[list] = []  # each entry: [kind, count]
        self._root_written = False
        self._finalized = False

    # ------------------------------------------------------------------
    # public api
    # ------------------------------------------------------------------
    def start_object(self, key: str | None = None) -> None:
        """Open a new object.  Provide ``key`` if inside an object."""
        self._before_value(key)
        self._parts.append("{")
        self._stack.append([self._OBJECT, 0])

    def end_object(self) -> None:
        """Close the most recently opened object."""
        self._require_open(self._OBJECT, "end_object")
        self._parts.append("}")
        self._stack.pop()
        self._post_value()

    def start_array(self, key: str | None = None) -> None:
        """Open a new array.  Provide ``key`` if inside an object."""
        self._before_value(key)
        self._parts.append("[")
        self._stack.append([self._ARRAY, 0])

    def end_array(self) -> None:
        """Close the most recently opened array."""
        self._require_open(self._ARRAY, "end_array")
        self._parts.append("]")
        self._stack.pop()
        self._post_value()

    def add(self, key: str | None = None, value: Any = None) -> None:
        """Add a scalar (or pre-encodable) ``value``.

        Inside an object a ``key`` is required; inside an array (or at the
        top level) it must be ``None``.
        """
        self._before_value(key)
        # ``json.dumps`` handles strings, numbers, bool, None, lists and dicts.
        self._parts.append(json.dumps(value, ensure_ascii=False))
        self._post_value()

    def build(self) -> str:
        """Finalise the document and return the JSON string."""
        if self._stack:
            raise ValueError(
                f"cannot build: {len(self._stack)} container(s) still open"
            )
        if not self._root_written:
            raise ValueError("cannot build: no value was produced")
        self._finalized = True
        return "".join(self._parts)

    # ------------------------------------------------------------------
    # internal helpers
    # ------------------------------------------------------------------
    def _before_value(self, key: str | None) -> None:
        if self._finalized:
            raise ValueError("builder already finalized")
        if not self._stack:
            # top-level write
            if self._root_written:
                raise ValueError("root value already written")
            if key is not None:
                raise ValueError("top-level value cannot have a key")
            return
        frame = self._stack[-1]
        kind, count = frame
        if kind == self._OBJECT:
            if key is None:
                raise ValueError("key required inside an object")
            if not isinstance(key, str):
                raise TypeError("object key must be a string")
            if count > 0:
                self._parts.append(",")
            self._parts.append(json.dumps(key, ensure_ascii=False))
            self._parts.append(":")
        else:  # array
            if key is not None:
                raise ValueError("key not allowed inside an array")
            if count > 0:
                self._parts.append(",")

    def _post_value(self) -> None:
        if not self._stack:
            self._root_written = True
            return
        self._stack[-1][1] += 1
        # if a sibling closes a container, mark its parent's item count too
        # — but actually _post_value runs after every item, so this is
        # already correct for nested containers (because the inner container
        # call to _post_value will increment its own count, and after the
        # closing brace the outer call increments the outer count).

    def _require_open(self, kind: str, op: str) -> None:
        if self._finalized:
            raise ValueError("builder already finalized")
        if not self._stack:
            raise ValueError(f"{op}: no container is open")
        if self._stack[-1][0] != kind:
            raise ValueError(
                f"{op}: expected to close {self._stack[-1][0]}, not {kind}"
            )
