"""Intent graph node definitions."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum


class IntentNodeType(str, Enum):
    """Types of nodes in an intent graph."""
    QUERY = "QUERY"
    CONCEPT = "CONCEPT"
    ENTITY = "ENTITY"
    ACTION = "ACTION"
    FILTER = "FILTER"


def _short_uuid() -> str:
    """Return an 8-character short UUID4 string."""
    return uuid.uuid4().hex[:8]


@dataclass
class IntentNode:
    """A node in an intent graph.

    Attributes:
        node_id: Unique identifier (auto-generated 8-char UUID4 hex).
        node_type: Type of the node.
        label: Human-readable label for the node.
        weight: Importance weight (default 1.0).
        metadata: Arbitrary extra data.
    """

    node_type: IntentNodeType
    label: str
    weight: float = 1.0
    metadata: dict = field(default_factory=dict)
    node_id: str = field(default_factory=_short_uuid)

    def __hash__(self) -> int:
        return hash(self.node_id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IntentNode):
            return NotImplemented
        return self.node_id == other.node_id
