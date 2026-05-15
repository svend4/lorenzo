"""KGRetriever — knowledge-graph-aware retrieval (Sprint 66 / M1).

Given a query, extracts entities, finds them in the KG, expands to
neighbours up to `max_hops`, and returns passages from documents
known to mention any of those entities.

Designed as a `Retriever` plugin compatible with the rag pipeline:
exposes `search(query, top_k)` → list[Passage].
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable, Sequence

from docstoolkit.knowledge_graph.entity import Entity
from docstoolkit.knowledge_graph.extractor import (
    ExtractionConfig,
    KGExtractor,
)
from docstoolkit.knowledge_graph.graph import KnowledgeGraph
from docstoolkit.rag.types import Passage


@dataclass
class DocSource:
    """A document indexed by which entities it mentions."""

    doc_id: str
    title: str
    text: str
    entity_ids: set[str] = field(default_factory=set)


class KGRetriever:
    """Walk the KG from query-entities to find passages.

    Lifecycle:
      kgr = KGRetriever()
      kgr.index_doc(doc_id="docs/a", text=md_text, title="A")
      kgr.index_doc(doc_id="docs/b", text=md_text2, title="B")
      kgr.search("Yodoca memory", top_k=5)
    """

    def __init__(
        self,
        graph: KnowledgeGraph | None = None,
        extractor: KGExtractor | None = None,
        max_hops: int = 1,
    ):
        self.graph = graph or KnowledgeGraph()
        self.extractor = extractor or KGExtractor()
        self.max_hops = max_hops
        self._docs: dict[str, DocSource] = {}

    # -- ingest --------------------------------------------------------

    def index_doc(self, doc_id: str, text: str, title: str = "") -> None:
        """Extract entities/relations from `text` and remember which docs
        mention which entity."""
        if not text:
            return
        entities, relations = self.extractor.extract(text, doc_id=doc_id)
        entity_ids: set[str] = set()
        for e in entities:
            existing = self.graph.find_entity(e.name)
            if existing is None:
                self.graph.add_entity(e)
                entity_ids.add(e.entity_id)
            else:
                entity_ids.add(existing.entity_id)
        for r in relations:
            self.graph.add_relation(r)
        self._docs[doc_id] = DocSource(
            doc_id=doc_id, title=title, text=text,
            entity_ids=entity_ids,
        )

    def index_passages(self, passages: Iterable[Passage]) -> None:
        for p in passages:
            self.index_doc(p.doc_id, p.text, title=p.title)

    # -- query ---------------------------------------------------------

    def _query_entities(self, query: str) -> list[Entity]:
        """Match `query` words against graph entities by name/alias."""
        words = set(re.findall(r"[A-Za-zА-Яа-я][\w-]{2,}", query))
        # Also try title-case bigrams
        for m in re.finditer(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b", query):
            words.add(m.group(0))
        hits: list[Entity] = []
        seen: set[str] = set()
        for w in words:
            e = self.graph.find_entity(w)
            if e and e.entity_id not in seen:
                hits.append(e)
                seen.add(e.entity_id)
        return hits

    def _expand(self, seeds: Sequence[Entity]) -> set[str]:
        """Return set of entity_ids reachable from seeds within max_hops."""
        frontier: set[str] = {e.entity_id for e in seeds}
        all_ids: set[str] = set(frontier)
        for _ in range(max(1, self.max_hops)):
            new_frontier: set[str] = set()
            for eid in frontier:
                for n in self.graph.neighbors(eid):
                    if n.entity_id not in all_ids:
                        new_frontier.add(n.entity_id)
            all_ids |= new_frontier
            if not new_frontier:
                break
            frontier = new_frontier
        return all_ids

    def search(self, query: str, top_k: int = 5) -> list[Passage]:
        """Return up to `top_k` passages from docs mentioning query entities
        (or any reachable neighbour entity, up to `max_hops`).
        Scoring: |doc.entities ∩ relevant_entities| / |relevant_entities|.
        """
        seeds = self._query_entities(query)
        if not seeds:
            return []
        relevant = self._expand(seeds)
        if not relevant:
            return []
        scored: list[tuple[float, DocSource]] = []
        for src in self._docs.values():
            hits = src.entity_ids & relevant
            if not hits:
                continue
            score = len(hits) / len(relevant)
            scored.append((score, src))
        scored.sort(key=lambda x: -x[0])
        out: list[Passage] = []
        for score, src in scored[:top_k]:
            out.append(Passage(
                text=src.text,
                doc_id=src.doc_id,
                title=src.title,
                score=score,
            ))
        return out

    # -- diagnostics ---------------------------------------------------

    def stats(self) -> dict:
        return {
            "docs": len(self._docs),
            "entities": self.graph.entity_count(),
            "relations": self.graph.relation_count(),
        }
