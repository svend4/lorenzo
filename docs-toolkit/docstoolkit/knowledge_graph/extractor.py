"""KGExtractor: regex-based entity and relation extraction. Pure stdlib only."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from docstoolkit.knowledge_graph.entity import Entity, EntityType
from docstoolkit.knowledge_graph.relation import Relation, RelationType
from docstoolkit.knowledge_graph.graph import KnowledgeGraph


# ---------------------------------------------------------------------------
# Tech keyword set (lower-case)
# ---------------------------------------------------------------------------
_TECH_KEYWORDS: frozenset[str] = frozenset({
    "python", "api", "llm", "rag", "nlp", "ml", "ai", "gpt", "bert",
    "docker", "kubernetes", "k8s", "sql", "nosql", "json", "yaml", "xml",
    "rest", "grpc", "graphql", "http", "https", "git", "github", "ci", "cd",
    "rust", "golang", "go", "java", "javascript", "typescript", "react",
    "node", "npm", "pip", "pytorch", "tensorflow", "keras", "sklearn",
    "embeddings", "vector", "index", "redis", "postgres", "mongodb",
    "elasticsearch", "kafka", "celery", "fastapi", "flask", "django",
    "pandas", "numpy", "scipy", "cuda", "gpu", "cpu", "aws", "gcp", "azure",
    "llama", "mistral", "claude", "openai", "anthropic", "huggingface",
    "transformer", "tokenizer", "tokenize", "langchain", "llamaindex",
    "weaviate", "pinecone", "chroma", "faiss", "hnswlib", "milvus",
})

# Matches a run of Title Case words (1 or more capital-starting words),
# separated by a single space only (not multiple spaces or newlines).
_TITLE_CASE_RE = re.compile(r'\b([A-Z][a-zA-Z0-9]*(?:[ ][A-Z][a-zA-Z0-9]*)*)\b')

# All-caps token ≥ 2 chars
_ALL_CAPS_RE = re.compile(r'\b([A-Z]{2,})\b')


@dataclass
class ExtractionConfig:
    min_entity_len: int = 3
    relation_window: int = 100  # characters between entities to create a relation


class KGExtractor:
    """Regex-based entity and relation extractor. No external dependencies."""

    def __init__(self, config: ExtractionConfig | None = None) -> None:
        self.config = config or ExtractionConfig()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract(
        self, text: str, doc_id: str = ""
    ) -> tuple[list[Entity], list[Relation]]:
        """Extract entities and relations from *text*.

        Returns (entities, relations).
        """
        if not text or not text.strip():
            return [], []

        entities = self._extract_entities(text)
        relations = self._extract_relations(text, entities)
        return entities, relations

    def enrich(
        self, graph: KnowledgeGraph, text: str, doc_id: str = ""
    ) -> None:
        """Extract from *text* and add results to an existing *graph*."""
        entities, relations = self.extract(text, doc_id)

        # Add entities; reuse existing entity if same name already present
        id_map: dict[str, str] = {}  # extracted entity_id → graph entity_id
        for entity in entities:
            existing = graph.find_entity(entity.name)
            if existing is None:
                graph.add_entity(entity)
                id_map[entity.entity_id] = entity.entity_id
            else:
                id_map[entity.entity_id] = existing.entity_id

        # Remap relation ids and add
        for relation in relations:
            new_src = id_map.get(relation.source_id, relation.source_id)
            new_tgt = id_map.get(relation.target_id, relation.target_id)
            if new_src == new_tgt:
                continue
            relation.source_id = new_src
            relation.target_id = new_tgt
            graph.add_relation(relation)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _classify(self, name: str) -> EntityType:
        """Classify an extracted name into an EntityType."""
        lower = name.lower().strip()

        # All-caps token → ORGANIZATION
        if re.match(r'^[A-Z]{2,}$', name.strip()):
            return EntityType.ORGANIZATION

        # Any token matches tech keywords → TECHNOLOGY
        tokens = re.split(r'[\s_\-/]+', lower)
        if any(tok in _TECH_KEYWORDS for tok in tokens):
            return EntityType.TECHNOLOGY
        if lower in _TECH_KEYWORDS:
            return EntityType.TECHNOLOGY

        return EntityType.CONCEPT

    _STOP_WORDS: frozenset[str] = frozenset({
        "the", "a", "an", "in", "on", "at", "to", "of", "and", "or",
        "but", "if", "is", "it", "be", "as", "by", "we", "he", "she",
        "they", "you", "i", "its", "this", "that", "these", "those",
    })

    def _extract_entities(self, text: str) -> list[Entity]:
        """Extract deduplicated entities from text."""
        cfg = self.config
        seen: dict[str, Entity] = {}  # canonical lower name → Entity

        def _add(name: str) -> None:
            name = name.strip()
            if len(name) < cfg.min_entity_len:
                return
            if name.lower() in self._STOP_WORDS:
                return
            key = name.lower()
            if key not in seen:
                seen[key] = Entity(name=name, entity_type=self._classify(name))

        # Title Case runs: extract both the full multi-word run AND
        # each individual word inside the run (for deduplication purposes).
        for m in _TITLE_CASE_RE.finditer(text):
            run = m.group(1).strip()
            words = run.split()
            if len(words) > 1:
                # Add the full multi-word phrase
                _add(run)
                # Also add each individual word
                for w in words:
                    _add(w)
            else:
                _add(run)

        # All-caps tokens (may not be Title Case)
        for m in _ALL_CAPS_RE.finditer(text):
            name = m.group(1).strip()
            if len(name) < cfg.min_entity_len:
                continue
            key = name.lower()
            if key not in seen:
                seen[key] = Entity(name=name, entity_type=EntityType.ORGANIZATION)

        return list(seen.values())

    def _extract_relations(
        self, text: str, entities: list[Entity]
    ) -> list[Relation]:
        """Create RELATED_TO relations for entity pairs within the window."""
        if len(entities) < 2:
            return []

        cfg = self.config
        relations: list[Relation] = []

        # Find all positions of each entity in text
        positions: list[tuple[int, Entity]] = []
        for entity in entities:
            for m in re.finditer(re.escape(entity.name), text, re.IGNORECASE):
                positions.append((m.start(), entity))

        positions.sort(key=lambda x: x[0])

        # For each consecutive pair within the window, create a relation
        created: set[tuple[str, str]] = set()
        for i, (pos_a, ent_a) in enumerate(positions):
            for pos_b, ent_b in positions[i + 1:]:
                if ent_a.entity_id == ent_b.entity_id:
                    continue
                if pos_b - pos_a > cfg.relation_window:
                    break
                pair = (
                    min(ent_a.entity_id, ent_b.entity_id),
                    max(ent_a.entity_id, ent_b.entity_id),
                )
                if pair in created:
                    continue
                created.add(pair)

                # Evidence: the surrounding text snippet
                start = max(0, pos_a)
                end = min(len(text), pos_b + len(ent_b.name))
                evidence = text[start:end].strip()

                relations.append(
                    Relation(
                        source_id=ent_a.entity_id,
                        target_id=ent_b.entity_id,
                        relation_type=RelationType.RELATED_TO,
                        evidence=evidence,
                    )
                )

        return relations
