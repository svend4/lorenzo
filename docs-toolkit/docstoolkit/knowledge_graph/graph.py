"""KnowledgeGraph: in-memory graph of entities and relations."""
from __future__ import annotations

from docstoolkit.knowledge_graph.entity import Entity
from docstoolkit.knowledge_graph.relation import Relation


class KnowledgeGraph:
    """In-memory knowledge graph storing entities and relations."""

    def __init__(self) -> None:
        self._entities: dict[str, Entity] = {}   # entity_id → Entity
        self._relations: dict[str, Relation] = {}  # relation_id → Relation

    # ------------------------------------------------------------------
    # Entities
    # ------------------------------------------------------------------

    def add_entity(self, entity: Entity) -> None:
        """Add or overwrite an entity by its entity_id."""
        self._entities[entity.entity_id] = entity

    def get_entity(self, entity_id: str) -> Entity | None:
        """Return entity by id, or None if not found."""
        return self._entities.get(entity_id)

    def find_entity(self, name: str) -> Entity | None:
        """Return first entity whose name or alias matches (case-insensitive)."""
        lower = name.lower()
        for entity in self._entities.values():
            if entity.name.lower() == lower:
                return entity
            if any(alias.lower() == lower for alias in entity.aliases):
                return entity
        return None

    # ------------------------------------------------------------------
    # Relations
    # ------------------------------------------------------------------

    def add_relation(self, relation: Relation) -> None:
        """Add or overwrite a relation by its relation_id."""
        self._relations[relation.relation_id] = relation

    def relations_for(self, entity_id: str) -> list[Relation]:
        """Return all relations where entity_id is source or target."""
        return [
            r for r in self._relations.values()
            if r.source_id == entity_id or r.target_id == entity_id
        ]

    def neighbors(self, entity_id: str) -> list[Entity]:
        """Return entities connected to entity_id by any relation."""
        result: list[Entity] = []
        seen: set[str] = set()
        for relation in self.relations_for(entity_id):
            other_id = (
                relation.target_id
                if relation.source_id == entity_id
                else relation.source_id
            )
            if other_id not in seen and other_id in self._entities:
                seen.add(other_id)
                result.append(self._entities[other_id])
        return result

    # ------------------------------------------------------------------
    # Counts
    # ------------------------------------------------------------------

    def entity_count(self) -> int:
        return len(self._entities)

    def relation_count(self) -> int:
        return len(self._relations)

    # ------------------------------------------------------------------
    # Subgraph
    # ------------------------------------------------------------------

    def subgraph(self, entity_ids: list[str]) -> "KnowledgeGraph":
        """Return a new KnowledgeGraph with only the given entities and
        inter-relations between them."""
        id_set = set(entity_ids)
        sub = KnowledgeGraph()
        for eid in entity_ids:
            entity = self._entities.get(eid)
            if entity is not None:
                sub.add_entity(entity)
        for relation in self._relations.values():
            if relation.source_id in id_set and relation.target_id in id_set:
                sub.add_relation(relation)
        return sub

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Serialise the graph to a plain dict (JSON-compatible)."""
        return {
            "entities": [
                {
                    "entity_id": e.entity_id,
                    "name": e.name,
                    "entity_type": e.entity_type.value,
                    "aliases": list(e.aliases),
                    "metadata": dict(e.metadata),
                }
                for e in self._entities.values()
            ],
            "relations": [
                {
                    "relation_id": r.relation_id,
                    "source_id": r.source_id,
                    "target_id": r.target_id,
                    "relation_type": r.relation_type.value,
                    "weight": r.weight,
                    "evidence": r.evidence,
                }
                for r in self._relations.values()
            ],
        }
