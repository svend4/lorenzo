"""Entity definitions for the Knowledge Graph module."""
import uuid
from dataclasses import dataclass, field
from enum import Enum


class EntityType(Enum):
    PERSON = "person"
    ORGANIZATION = "organization"
    TECHNOLOGY = "technology"
    CONCEPT = "concept"
    LOCATION = "location"
    DATE = "date"
    UNKNOWN = "unknown"


def _new_entity_id() -> str:
    return uuid.uuid4().hex[:8]


@dataclass
class Entity:
    """A named entity in the knowledge graph."""
    name: str
    entity_type: EntityType
    entity_id: str = field(default_factory=_new_entity_id)
    aliases: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def matches(self, text: str) -> bool:
        """Return True if name or any alias appears in text (case-insensitive)."""
        lower_text = text.lower()
        if self.name.lower() in lower_text:
            return True
        return any(alias.lower() in lower_text for alias in self.aliases)

    def canonical_name(self) -> str:
        """Return the canonical (stripped) name."""
        return self.name.strip()
