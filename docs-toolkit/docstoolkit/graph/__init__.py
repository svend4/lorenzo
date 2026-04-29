"""Knowledge graph builder для docs-toolkit.

Извлекает сущности (NER) и строит концептуальный граф с co-occurrence weighted edges.

Без зависимостей: regex-NER + dict-based graph.
Опционально: networkx (для расширенных алгоритмов центральности).

Использование:
    from docstoolkit.graph import build_graph, export_dot

    g = build_graph(docs)
    print(g.top_concepts(20))
    print(g.top_pairs(15))
    export_dot(g, "concepts.dot")
"""
from docstoolkit.graph.ner import extract_entities, EntityKinds
from docstoolkit.graph.builder import (
    build_graph, ConceptGraph, build_from_docs_index,
)
from docstoolkit.graph.export import (
    export_dot, export_mermaid, export_json, export_markdown,
)

__all__ = [
    "extract_entities", "EntityKinds",
    "build_graph", "ConceptGraph", "build_from_docs_index",
    "export_dot", "export_mermaid", "export_json", "export_markdown",
]
