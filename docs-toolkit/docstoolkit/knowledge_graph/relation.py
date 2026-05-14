"""Relation definitions for the Knowledge Graph module."""
import uuid
from dataclasses import dataclass, field
from enum import Enum


class RelationType(Enum):
    USES = "uses"
    PART_OF = "part_of"
    RELATED_TO = "related_to"
    MENTIONS = "mentions"
    AUTHORED_BY = "authored_by"
    LOCATED_IN = "located_in"
    DEPENDS_ON = "depends_on"


def _new_relation_id() -> str:
    return uuid.uuid4().hex[:8]


@dataclass
class Relation:
    """A directed relation between two entities in the knowledge graph."""
    source_id: str
    target_id: str
    relation_type: RelationType
    relation_id: str = field(default_factory=_new_relation_id)
    weight: float = 1.0
    evidence: str = ""
