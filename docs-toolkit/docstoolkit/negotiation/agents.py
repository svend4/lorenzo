"""Retriever agents that place bids in the context-window auction."""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


# Forward reference: Bid is defined in auction.py but agents need it.
# We import lazily to avoid a circular import.
def _make_bid(agent_name, passage_idx, doc_id, bid_score, reason=""):
    from docstoolkit.negotiation.auction import Bid
    return Bid(
        agent_name=agent_name,
        passage_idx=passage_idx,
        doc_id=doc_id,
        bid_score=bid_score,
        reason=reason,
    )


@dataclass
class RetrieverAgent(ABC):
    """Abstract base for a retriever that places bids."""
    name: str
    weight: float = 1.0  # global weight multiplier for this agent's bids

    @abstractmethod
    def bid(self, query: str, passages: list, budget: int) -> list:
        """Return list[Bid] for passages this agent wants to include.

        budget = max slots in context window.
        """


class KeywordAgent(RetrieverAgent):
    """BM25/keyword-based agent.

    Bids proportional to keyword overlap between query and passage.
    bid_score = token_overlap(query, passage.text) * weight
    reason = f"keyword match={score:.2f}"
    """

    name: str = field(default="keyword")
    weight: float = field(default=1.0)

    def __init__(self, name: str = "keyword", weight: float = 1.0):
        self.name = name
        self.weight = weight

    def _token_overlap(self, query: str, text: str) -> float:
        """Jaccard-like overlap between query tokens and passage tokens."""
        q_tokens = set(re.findall(r"\w+", query.lower()))
        t_tokens = set(re.findall(r"\w+", text.lower()))
        if not q_tokens:
            return 0.0
        overlap = q_tokens & t_tokens
        return len(overlap) / len(q_tokens)

    def bid(self, query: str, passages: list, budget: int) -> list:
        bids = []
        for idx, passage in enumerate(passages):
            score = self._token_overlap(query, passage.text) * self.weight
            reason = f"keyword match={score / max(self.weight, 1e-9):.2f}"
            bids.append(_make_bid(self.name, idx, passage.doc_id, score, reason))
        return bids


class SemanticAgent(RetrieverAgent):
    """Semantic similarity agent.

    Uses passage.score as semantic score.
    bid_score = passage.score * weight
    reason = f"semantic score={passage.score:.2f}"
    """

    def __init__(self, name: str = "semantic", weight: float = 1.0):
        self.name = name
        self.weight = weight

    def bid(self, query: str, passages: list, budget: int) -> list:
        bids = []
        for idx, passage in enumerate(passages):
            score = passage.score * self.weight
            reason = f"semantic score={passage.score:.2f}"
            bids.append(_make_bid(self.name, idx, passage.doc_id, score, reason))
        return bids


class GraphAgent(RetrieverAgent):
    """Graph connectivity agent.

    Boosts passages that mention entities from query (capitalized words).
    For each passage: count how many query_entities are in passage.text.
    bid_score = (entity_count / max(1, len(query_entities))) * weight
    reason = f"graph entities={entity_count}"
    """

    def __init__(self, name: str = "graph", weight: float = 0.8):
        self.name = name
        self.weight = weight

    def _query_entities(self, query: str) -> list:
        """Extract capitalized words as named entities from query."""
        return re.findall(r"\b[A-Z][a-zA-Z0-9_]*\b", query)

    def bid(self, query: str, passages: list, budget: int) -> list:
        entities = self._query_entities(query)
        bids = []
        for idx, passage in enumerate(passages):
            if not entities:
                entity_count = 0
                raw_score = 0.0
            else:
                entity_count = sum(
                    1 for e in entities if e in passage.text
                )
                raw_score = entity_count / max(1, len(entities))
            score = raw_score * self.weight
            reason = f"graph entities={entity_count}"
            bids.append(_make_bid(self.name, idx, passage.doc_id, score, reason))
        return bids


class DiversityAgent(RetrieverAgent):
    """Diversity agent: penalizes passages from same doc_id as earlier bids.

    Keep track of already-selected doc_ids (passed via passages list).
    If passage.doc_id appears more than once: bid_score -= 0.3
    reason = f"diversity (doc_id={passage.doc_id} seen={count}x)"
    """

    def __init__(self, name: str = "diversity", weight: float = 0.6):
        self.name = name
        self.weight = weight

    def bid(self, query: str, passages: list, budget: int) -> list:
        # Count occurrences of each doc_id in the passage list
        doc_id_counts: dict = {}
        for passage in passages:
            doc_id_counts[passage.doc_id] = doc_id_counts.get(passage.doc_id, 0) + 1

        bids = []
        for idx, passage in enumerate(passages):
            count = doc_id_counts.get(passage.doc_id, 1)
            # Base score from weight; subtract 0.3 per extra occurrence
            score = self.weight - 0.3 * max(0, count - 1)
            score = max(0.0, score)
            reason = f"diversity (doc_id={passage.doc_id} seen={count}x)"
            bids.append(_make_bid(self.name, idx, passage.doc_id, score, reason))
        return bids


class CostAgent(RetrieverAgent):
    """Cost-aware agent: penalizes long passages.

    passage_length = len(passage.text.split())
    cost_penalty = min(passage_length / 500, 1.0)  # max penalty at 500 words
    bid_score = (1.0 - cost_penalty) * weight
    reason = f"cost words={passage_length}"
    """

    def __init__(self, name: str = "cost", weight: float = 0.5):
        self.name = name
        self.weight = weight

    def bid(self, query: str, passages: list, budget: int) -> list:
        bids = []
        for idx, passage in enumerate(passages):
            passage_length = len(passage.text.split())
            cost_penalty = min(passage_length / 500, 1.0)
            score = (1.0 - cost_penalty) * self.weight
            reason = f"cost words={passage_length}"
            bids.append(_make_bid(self.name, idx, passage.doc_id, score, reason))
        return bids
