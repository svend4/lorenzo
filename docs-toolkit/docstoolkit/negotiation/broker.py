"""High-level broker that wires agents together and runs the auction."""

from dataclasses import dataclass, field
from docstoolkit.negotiation.agents import (
    KeywordAgent, SemanticAgent, GraphAgent, DiversityAgent, CostAgent,
)
from docstoolkit.negotiation.auction import AuctionResult, run_auction


@dataclass
class BrokerConfig:
    budget: int = 5
    keyword_weight: float = 1.0
    semantic_weight: float = 1.0
    graph_weight: float = 0.8
    diversity_weight: float = 0.6
    cost_weight: float = 0.5


class NegotiationBroker:
    """High-level broker: instantiates agents and runs auction."""

    def __init__(self, config: BrokerConfig | None = None):
        self._config = config or BrokerConfig()

    def retrieve(self, query: str, passages: list) -> AuctionResult:
        """Instantiate all agents with config weights, run auction."""
        cfg = self._config
        agents = [
            KeywordAgent(name="keyword", weight=cfg.keyword_weight),
            SemanticAgent(name="semantic", weight=cfg.semantic_weight),
            GraphAgent(name="graph", weight=cfg.graph_weight),
            DiversityAgent(name="diversity", weight=cfg.diversity_weight),
            CostAgent(name="cost", weight=cfg.cost_weight),
        ]
        return run_auction(query, passages, agents, cfg.budget)
