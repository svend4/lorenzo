import re
from dataclasses import dataclass, field
from docstoolkit.got.node import ThoughtNode, NodeType
from docstoolkit.got.graph import ThoughtGraph


@dataclass
class ReasoningResult:
    """Result of GoT reasoning over a query."""
    query: str
    graph: ThoughtGraph
    final_answer: str
    confirmed_count: int
    refuted_count: int
    synthesis_node_id: str = ""

    def confidence(self) -> float:
        """Average confidence of FACT nodes, or 0.5 if none."""
        facts = self.graph.confirmed_facts()
        if not facts:
            return 0.5
        return sum(n.confidence for n in facts) / len(facts)


class GoTReasoner:
    """Builds and traverses graph-of-thoughts over corpus passages.

    Phase 1: Decompose query into sub-hypotheses (rule-based: split on "and", "?", ",")
    Phase 2: For each hypothesis, search passages for supporting/refuting evidence
    Phase 3: Synthesize confirmed facts into final answer
    """

    def __init__(self, passages: list):
        """passages: list of Passage-like objects with .text, .doc_id, .score"""
        self._passages = passages

    def reason(self, query: str, max_hypotheses: int = 5) -> ReasoningResult:
        """Full GoT pipeline.

        1. Decompose query → hypotheses (list of strings)
        2. For each hypothesis: create HYPOTHESIS node, find best passage,
           determine node_type (FACT if overlap > 0.2 else REFUTED)
           confidence = max passage score or 0.3 for refuted
        3. Create SYNTHESIS node with all FACT node_ids as parents
           synthesis text = "Based on {n} facts: " + ", ".join(short fact texts)
        4. Return ReasoningResult
        """
        graph = ThoughtGraph()
        hypotheses = self._decompose(query, max_hypotheses)

        fact_node_ids = []
        confirmed_count = 0
        refuted_count = 0

        for i, hyp_text in enumerate(hypotheses):
            node_id = f"h{i}"
            passage, overlap = self._find_support(hyp_text)

            if overlap > 0.2:
                node_type = NodeType.FACT
                confidence = passage.score if passage is not None else overlap
                source_passages = [passage.doc_id] if passage is not None else []
                confirmed_count += 1
                fact_node_ids.append(node_id)
            else:
                node_type = NodeType.REFUTED
                confidence = 0.3
                source_passages = [passage.doc_id] if passage is not None else []
                refuted_count += 1

            node = ThoughtNode(
                node_id=node_id,
                text=hyp_text,
                node_type=node_type,
                source_passages=source_passages,
                confidence=confidence,
                parent_ids=[],
                children_ids=[],
            )
            graph.add_node(node)

        # Phase 3: Synthesis node
        n_facts = len(fact_node_ids)
        if n_facts > 0:
            fact_nodes = [graph.get_node(nid) for nid in fact_node_ids]
            short_texts = [n.text[:40] for n in fact_nodes if n is not None]
            synthesis_text = f"Based on {n_facts} facts: " + ", ".join(short_texts)
        else:
            synthesis_text = f"Based on 0 facts: no supporting evidence found for query"

        synthesis_id = "synthesis"
        synthesis_node = ThoughtNode(
            node_id=synthesis_id,
            text=synthesis_text,
            node_type=NodeType.SYNTHESIS,
            source_passages=[],
            confidence=0.5,
            parent_ids=list(fact_node_ids),
            children_ids=[],
        )
        graph.add_node(synthesis_node)

        final_answer = synthesis_text

        return ReasoningResult(
            query=query,
            graph=graph,
            final_answer=final_answer,
            confirmed_count=confirmed_count,
            refuted_count=refuted_count,
            synthesis_node_id=synthesis_id,
        )

    def _decompose(self, query: str, max_hypotheses: int) -> list:
        """Split query into sub-hypotheses.

        Split on: " and ", "? ", ", " — filter empty, strip, lowercase.
        If only 1 result: return [query] as-is.
        Limit to max_hypotheses.
        """
        # Split on " and ", "? ", ", "
        parts = re.split(r' and |\? |, ', query)
        parts = [p.strip() for p in parts]
        parts = [p for p in parts if p]

        if len(parts) <= 1:
            return [query]

        # Lowercase sub-hypotheses
        parts = [p.lower() for p in parts]
        return parts[:max_hypotheses]

    def _find_support(self, hypothesis: str) -> tuple:
        """Find best supporting passage for hypothesis.

        Returns (passage_or_None, overlap_score: float)
        Compute Jaccard token overlap between hypothesis and each passage.text
        Return passage with highest overlap and that overlap score.
        """
        if not self._passages:
            return (None, 0.0)

        hyp_tokens = self._token_set(hypothesis)
        best_passage = None
        best_score = 0.0

        for passage in self._passages:
            passage_tokens = self._token_set(passage.text)
            score = self._jaccard(hyp_tokens, passage_tokens)
            if score > best_score:
                best_score = score
                best_passage = passage

        return (best_passage, best_score)

    def _token_set(self, text: str) -> set:
        return set(w.lower() for w in re.findall(r'\b\w{3,}\b', text))

    def _jaccard(self, a: set, b: set) -> float:
        if not a and not b:
            return 0.0
        inter = len(a & b)
        union = len(a | b)
        return inter / union if union else 0.0
