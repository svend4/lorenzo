"""Knowledge Graph module for docs-toolkit.

Provides entity extraction, relation modelling, and an in-memory graph
with no external dependencies.

Usage::

    from docstoolkit.knowledge_graph import (
        Entity, EntityType,
        Relation, RelationType,
        KnowledgeGraph,
        KGExtractor, ExtractionConfig,
    )

    extractor = KGExtractor()
    entities, relations = extractor.extract("Python and RAG are used by LangChain.")
"""

from docstoolkit.knowledge_graph.entity import Entity, EntityType
from docstoolkit.knowledge_graph.relation import Relation, RelationType
from docstoolkit.knowledge_graph.graph import KnowledgeGraph
from docstoolkit.knowledge_graph.extractor import KGExtractor, ExtractionConfig
from docstoolkit.knowledge_graph.retriever import KGRetriever, DocSource

__all__ = [
    "Entity",
    "EntityType",
    "Relation",
    "RelationType",
    "KnowledgeGraph",
    "KGExtractor",
    "ExtractionConfig",
    "KGRetriever",
    "DocSource",
]
