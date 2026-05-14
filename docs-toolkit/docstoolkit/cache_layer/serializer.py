"""Serializer implementations for cache values."""
from __future__ import annotations

import json
import pickle
from abc import ABC, abstractmethod
from typing import Any


class Serializer(ABC):
    """Abstract base class for value serializers."""

    @abstractmethod
    def serialize(self, value: Any) -> bytes:
        """Convert *value* to bytes suitable for storage."""

    @abstractmethod
    def deserialize(self, data: bytes) -> Any:
        """Reconstruct a Python object from raw *data* bytes."""


# ---------------------------------------------------------------------------
# Concrete serializers
# ---------------------------------------------------------------------------

class JsonSerializer(Serializer):
    """Serializer that uses :mod:`json`.

    Supports any value that ``json.dumps`` accepts.  The resulting bytes are
    UTF-8 encoded JSON text.
    """

    def serialize(self, value: Any) -> bytes:
        return json.dumps(value, ensure_ascii=False).encode("utf-8")

    def deserialize(self, data: bytes) -> Any:
        return json.loads(data.decode("utf-8"))


class PickleSerializer(Serializer):
    """Serializer that uses :mod:`pickle`.

    Supports arbitrary Python objects.  Uses the highest available protocol
    for best efficiency.
    """

    def serialize(self, value: Any) -> bytes:
        return pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)

    def deserialize(self, data: bytes) -> Any:
        return pickle.loads(data)  # noqa: S301


class StringSerializer(Serializer):
    """Lightweight serializer for plain strings only.

    Encodes/decodes as UTF-8 bytes.  Raises :class:`TypeError` when the
    supplied *value* is not a :class:`str`.
    """

    def serialize(self, value: Any) -> bytes:
        if not isinstance(value, str):
            raise TypeError(
                f"StringSerializer can only serialize str, got {type(value).__name__!r}"
            )
        return value.encode("utf-8")

    def deserialize(self, data: bytes) -> str:
        return data.decode("utf-8")
