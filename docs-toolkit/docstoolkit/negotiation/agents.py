"""Retriever agents that place bids in the context-window auction."""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

# Phase IV.1 — hoist Bid import out of _make_bid hot path. The original
# code lazy-imported on every bid construction (5×N passages = 12 500 calls
# per 500-iter bench) to avoid a circular import; but `agents.py` is
# imported only by `broker.py` and `auction.py`, never the other way
# around, so the cycle never existed.
from docstoolkit.negotiation.auction import Bid

# Phase IV.1 — pre-compiled patterns (re.findall recompiled on every call
# in the original implementation; this cuts the ~3 μs of re cache lookup).
_WORD_RE = re.compile(r"\w+")
_ENTITY_RE = re.compile(r"\b[A-Z][a-zA-Z0-9_]*\b")


def _make_bid(agent_name, passage_idx, doc_id, bid_score, reason=""):
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

    def bid(self, query: str, passages: list, budget: int) -> list:
        # Phase IV.1 — tokenise the query exactly once per `bid()` call
        # instead of N times inside `_token_overlap` (re.findall was the
        # hottest pure-Python frame in cProfile).
        q_tokens = set(_WORD_RE.findall(query.lower()))
        if not q_tokens:
            return [
                _make_bid(self.name, idx, p.doc_id, 0.0, "keyword match=0.00")
                for idx, p in enumerate(passages)
            ]
        weight = self.weight
        denom = len(q_tokens)
        bids = []
        for idx, passage in enumerate(passages):
            t_tokens = set(_WORD_RE.findall(passage.text.lower()))
            overlap = q_tokens & t_tokens
            raw = len(overlap) / denom
            score = raw * weight
            reason = f"keyword match={raw:.2f}"
            bids.append(
                _make_bid(self.name, idx, passage.doc_id, score, reason)
            )
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

    def bid(self, query: str, passages: list, budget: int) -> list:
        # Phase IV.1 — query entities are query-derived; compute once.
        entities = _ENTITY_RE.findall(query)
        n_entities = len(entities)
        weight = self.weight
        bids = []
        if not entities:
            return [
                _make_bid(self.name, idx, p.doc_id, 0.0, "graph entities=0")
                for idx, p in enumerate(passages)
            ]
        for idx, passage in enumerate(passages):
            text = passage.text
            entity_count = sum(1 for e in entities if e in text)
            raw_score = entity_count / n_entities
            score = raw_score * weight
            reason = f"graph entities={entity_count}"
            bids.append(
                _make_bid(self.name, idx, passage.doc_id, score, reason)
            )
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
        # Phase IV.1 — single pass for counting; was two passes before.
        weight = self.weight
        doc_id_counts: dict = {}
        for passage in passages:
            doc_id = passage.doc_id
            doc_id_counts[doc_id] = doc_id_counts.get(doc_id, 0) + 1
        bids = []
        for idx, passage in enumerate(passages):
            doc_id = passage.doc_id
            count = doc_id_counts.get(doc_id, 1)
            score = weight - 0.3 * (count - 1)
            if score < 0.0:
                score = 0.0
            reason = f"diversity (doc_id={doc_id} seen={count}x)"
            bids.append(_make_bid(self.name, idx, doc_id, score, reason))
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
