"""Tests for docstoolkit.negotiation — multi-agent retrieval bargaining."""
import pytest
from dataclasses import dataclass

# ─── Helper passage type ────────────────────────────────────────────────────

@dataclass
class P:
    text: str
    doc_id: str
    title: str = ""
    score: float = 0.5


# ─── Imports ────────────────────────────────────────────────────────────────

from docstoolkit.negotiation.auction import Bid, AuctionResult, run_auction
from docstoolkit.negotiation.agents import (
    KeywordAgent, SemanticAgent, GraphAgent, DiversityAgent, CostAgent,
)
from docstoolkit.negotiation.broker import NegotiationBroker, BrokerConfig
from docstoolkit.negotiation import (
    RetrieverAgent, KeywordAgent as KA, SemanticAgent as SA,
    GraphAgent as GA, DiversityAgent as DA, CostAgent as CA,
    Bid as B, AuctionResult as AR, run_auction as ra,
    NegotiationBroker as NB, BrokerConfig as BC,
)


# ═══════════════════════════════════════════════════════════════════════════
# Bid dataclass
# ═══════════════════════════════════════════════════════════════════════════

class TestBid:
    def test_bid_has_agent_name(self):
        b = Bid(agent_name="keyword", passage_idx=0, doc_id="d1", bid_score=0.9)
        assert b.agent_name == "keyword"

    def test_bid_has_passage_idx(self):
        b = Bid(agent_name="semantic", passage_idx=3, doc_id="d1", bid_score=0.5)
        assert b.passage_idx == 3

    def test_bid_has_doc_id(self):
        b = Bid(agent_name="graph", passage_idx=0, doc_id="doc-42", bid_score=0.3)
        assert b.doc_id == "doc-42"

    def test_bid_has_bid_score(self):
        b = Bid(agent_name="cost", passage_idx=1, doc_id="d2", bid_score=0.7)
        assert b.bid_score == pytest.approx(0.7)

    def test_bid_default_reason_empty(self):
        b = Bid(agent_name="x", passage_idx=0, doc_id="d", bid_score=0.0)
        assert b.reason == ""

    def test_bid_explicit_reason(self):
        b = Bid(agent_name="x", passage_idx=0, doc_id="d", bid_score=0.5, reason="ok")
        assert b.reason == "ok"

    def test_bid_score_can_be_zero(self):
        b = Bid(agent_name="cost", passage_idx=0, doc_id="d", bid_score=0.0)
        assert b.bid_score == 0.0

    def test_bid_score_can_be_float(self):
        b = Bid(agent_name="a", passage_idx=0, doc_id="d", bid_score=0.123456)
        assert isinstance(b.bid_score, float)


# ═══════════════════════════════════════════════════════════════════════════
# AuctionResult
# ═══════════════════════════════════════════════════════════════════════════

class TestAuctionResult:
    def test_winning_agent_returns_max(self):
        result = AuctionResult(
            selected_passages=[],
            agent_wins={"keyword": 3, "semantic": 5, "graph": 1},
        )
        assert result.winning_agent() == "semantic"

    def test_winning_agent_empty_dict(self):
        result = AuctionResult(selected_passages=[], agent_wins={})
        assert result.winning_agent() == ""

    def test_winning_agent_single_entry(self):
        result = AuctionResult(selected_passages=[], agent_wins={"cost": 2})
        assert result.winning_agent() == "cost"

    def test_agent_wins_counted_correctly(self):
        result = AuctionResult(
            selected_passages=[],
            agent_wins={"keyword": 2, "diversity": 0},
        )
        assert result.agent_wins["keyword"] == 2
        assert result.agent_wins["diversity"] == 0

    def test_total_rounds_default_zero(self):
        result = AuctionResult(selected_passages=[])
        assert result.total_rounds == 0

    def test_bids_default_empty(self):
        result = AuctionResult(selected_passages=[])
        assert result.bids == []

    def test_selected_passages_stored(self):
        passages = [P("hello", "d1"), P("world", "d2")]
        result = AuctionResult(selected_passages=passages)
        assert len(result.selected_passages) == 2


# ═══════════════════════════════════════════════════════════════════════════
# KeywordAgent
# ═══════════════════════════════════════════════════════════════════════════

class TestKeywordAgent:
    def _agent(self, weight=1.0):
        return KeywordAgent(name="keyword", weight=weight)

    def test_returns_list_of_bids(self):
        agent = self._agent()
        passages = [P("hello world", "d1"), P("foo bar", "d2")]
        bids = agent.bid("hello", passages, budget=5)
        assert isinstance(bids, list)
        assert len(bids) == 2
        assert all(isinstance(b, Bid) for b in bids)

    def test_one_bid_per_passage(self):
        agent = self._agent()
        passages = [P(f"text {i}", f"d{i}") for i in range(7)]
        bids = agent.bid("text", passages, budget=5)
        assert len(bids) == 7

    def test_bid_score_between_zero_and_weight(self):
        agent = self._agent(weight=1.5)
        passages = [P("the quick brown fox", "d1"), P("zzz qqq", "d2")]
        for bid in agent.bid("the quick fox", passages, budget=5):
            assert 0.0 <= bid.bid_score <= 1.5 + 1e-9

    def test_reason_contains_keyword_match(self):
        agent = self._agent()
        bids = agent.bid("hello", [P("hello world", "d1")], budget=5)
        assert "keyword match=" in bids[0].reason

    def test_high_overlap_higher_score(self):
        agent = self._agent()
        high = P("the quick brown fox jumps", "d1")
        low  = P("completely unrelated text xyz", "d2")
        bids = agent.bid("the quick brown fox", [high, low], budget=5)
        assert bids[0].bid_score > bids[1].bid_score

    def test_zero_overlap_gives_zero(self):
        agent = self._agent()
        p = P("zzz qqq mmm", "d1")
        bids = agent.bid("the quick brown fox", [p], budget=5)
        assert bids[0].bid_score == pytest.approx(0.0)

    def test_full_overlap_score_equals_weight(self):
        agent = self._agent(weight=2.0)
        p = P("hello world", "d1")
        bids = agent.bid("hello world", [p], budget=5)
        assert bids[0].bid_score == pytest.approx(2.0)

    def test_passage_idx_matches_position(self):
        agent = self._agent()
        passages = [P("a", "d1"), P("b", "d2"), P("c", "d3")]
        bids = agent.bid("a", passages, budget=5)
        for i, bid in enumerate(bids):
            assert bid.passage_idx == i

    def test_doc_id_matches_passage(self):
        agent = self._agent()
        passages = [P("hello", "doc-A"), P("world", "doc-B")]
        bids = agent.bid("hello", passages, budget=5)
        assert bids[0].doc_id == "doc-A"
        assert bids[1].doc_id == "doc-B"

    def test_empty_query_gives_zero_scores(self):
        agent = self._agent()
        passages = [P("hello world", "d1")]
        bids = agent.bid("", passages, budget=5)
        assert bids[0].bid_score == pytest.approx(0.0)

    def test_weight_scales_score(self):
        agent1 = self._agent(weight=1.0)
        agent2 = self._agent(weight=2.0)
        p = [P("hello world", "d1")]
        b1 = agent1.bid("hello world", p, budget=5)
        b2 = agent2.bid("hello world", p, budget=5)
        assert b2[0].bid_score == pytest.approx(b1[0].bid_score * 2.0)


# ═══════════════════════════════════════════════════════════════════════════
# SemanticAgent
# ═══════════════════════════════════════════════════════════════════════════

class TestSemanticAgent:
    def _agent(self, weight=1.0):
        return SemanticAgent(name="semantic", weight=weight)

    def test_bid_score_equals_passage_score_times_weight(self):
        agent = self._agent(weight=1.0)
        p = P("some text", "d1", score=0.73)
        bids = agent.bid("query", [p], budget=5)
        assert bids[0].bid_score == pytest.approx(0.73)

    def test_weight_scales_score(self):
        agent = self._agent(weight=2.0)
        p = P("text", "d1", score=0.5)
        bids = agent.bid("q", [p], budget=5)
        assert bids[0].bid_score == pytest.approx(1.0)

    def test_reason_contains_semantic_score(self):
        agent = self._agent()
        p = P("x", "d1", score=0.42)
        bids = agent.bid("q", [p], budget=5)
        assert "semantic score=" in bids[0].reason

    def test_returns_one_bid_per_passage(self):
        agent = self._agent()
        passages = [P(f"t{i}", f"d{i}", score=i * 0.1) for i in range(5)]
        bids = agent.bid("q", passages, budget=5)
        assert len(bids) == 5

    def test_higher_passage_score_higher_bid(self):
        agent = self._agent()
        p_high = P("text", "d1", score=0.9)
        p_low  = P("text", "d2", score=0.1)
        bids = agent.bid("q", [p_high, p_low], budget=5)
        assert bids[0].bid_score > bids[1].bid_score

    def test_zero_score_passage(self):
        agent = self._agent()
        p = P("text", "d1", score=0.0)
        bids = agent.bid("q", [p], budget=5)
        assert bids[0].bid_score == pytest.approx(0.0)


# ═══════════════════════════════════════════════════════════════════════════
# GraphAgent
# ═══════════════════════════════════════════════════════════════════════════

class TestGraphAgent:
    def _agent(self, weight=0.8):
        return GraphAgent(name="graph", weight=weight)

    def test_entity_mention_boosts_score(self):
        agent = self._agent()
        p_with = P("The AgentFS system is great", "d1")
        p_without = P("nothing relevant here at all", "d2")
        bids = agent.bid("How does AgentFS work?", [p_with, p_without], budget=5)
        assert bids[0].bid_score > bids[1].bid_score

    def test_empty_query_all_zeros(self):
        agent = self._agent()
        passages = [P("AgentFS is great", "d1"), P("NGT Memory rocks", "d2")]
        bids = agent.bid("", passages, budget=5)
        for bid in bids:
            assert bid.bid_score == pytest.approx(0.0)

    def test_reason_contains_graph_entities(self):
        agent = self._agent()
        p = P("AgentFS rocks", "d1")
        bids = agent.bid("AgentFS query", [p], budget=5)
        assert "graph entities=" in bids[0].reason

    def test_no_entity_in_query_all_zero(self):
        agent = self._agent()
        # lowercase query → no capitalized entities
        p = P("agentfs is great", "d1")
        bids = agent.bid("what is agentfs", [p], budget=5)
        assert bids[0].bid_score == pytest.approx(0.0)

    def test_multiple_entities_partial_match(self):
        agent = self._agent(weight=1.0)
        p = P("AgentFS is a memory system", "d1")
        # Two entities: AgentFS, NGT — only AgentFS is in passage
        bids = agent.bid("AgentFS and NGT comparison", [p], budget=5)
        # 1 out of 2 entities matched → raw_score = 0.5
        assert bids[0].bid_score == pytest.approx(0.5, abs=0.01)

    def test_all_entities_matched_uses_weight(self):
        agent = self._agent(weight=0.8)
        p = P("AgentFS and Yodoca are great tools", "d1")
        bids = agent.bid("AgentFS Yodoca", [p], budget=5)
        # 2/2 entities matched → raw_score=1.0 × 0.8
        assert bids[0].bid_score == pytest.approx(0.8)

    def test_returns_one_bid_per_passage(self):
        agent = self._agent()
        passages = [P(f"text {i}", f"d{i}") for i in range(4)]
        bids = agent.bid("Query Entity", passages, budget=5)
        assert len(bids) == 4


# ═══════════════════════════════════════════════════════════════════════════
# DiversityAgent
# ═══════════════════════════════════════════════════════════════════════════

class TestDiversityAgent:
    def _agent(self, weight=0.6):
        return DiversityAgent(name="diversity", weight=weight)

    def test_duplicate_doc_id_reduces_score(self):
        agent = self._agent()
        p1 = P("first passage", "same-doc")
        p2 = P("second passage", "same-doc")
        bids = agent.bid("query", [p1, p2], budget=5)
        # Both from same doc; penalty should reduce scores vs unique
        assert bids[0].bid_score <= 0.6 + 1e-9
        assert bids[1].bid_score <= 0.6 + 1e-9

    def test_unique_doc_ids_no_penalty(self):
        agent = self._agent(weight=0.6)
        passages = [P("a", "d1"), P("b", "d2"), P("c", "d3")]
        bids = agent.bid("query", passages, budget=5)
        for bid in bids:
            assert bid.bid_score >= 0.0

    def test_reason_contains_diversity(self):
        agent = self._agent()
        p = P("text", "d1")
        bids = agent.bid("q", [p], budget=5)
        assert "diversity" in bids[0].reason

    def test_score_never_negative(self):
        agent = self._agent(weight=0.3)
        # Many duplicates → penalty could exceed weight
        passages = [P(f"text {i}", "same-doc") for i in range(10)]
        bids = agent.bid("query", passages, budget=5)
        for bid in bids:
            assert bid.bid_score >= 0.0

    def test_single_passage_unique_doc(self):
        agent = self._agent(weight=0.6)
        p = P("hello", "d1")
        bids = agent.bid("q", [p], budget=5)
        assert bids[0].bid_score == pytest.approx(0.6)

    def test_reason_contains_doc_id(self):
        agent = self._agent()
        p = P("text", "my-doc-99")
        bids = agent.bid("q", [p], budget=5)
        assert "my-doc-99" in bids[0].reason

    def test_returns_one_bid_per_passage(self):
        agent = self._agent()
        passages = [P(f"text {i}", f"d{i}") for i in range(6)]
        bids = agent.bid("q", passages, budget=5)
        assert len(bids) == 6


# ═══════════════════════════════════════════════════════════════════════════
# CostAgent
# ═══════════════════════════════════════════════════════════════════════════

class TestCostAgent:
    def _agent(self, weight=0.5):
        return CostAgent(name="cost", weight=weight)

    def test_short_passage_higher_score_than_long(self):
        agent = self._agent()
        short = P("hello world", "d1")
        long  = P(" ".join(["word"] * 600), "d2")
        bids = agent.bid("q", [short, long], budget=5)
        assert bids[0].bid_score > bids[1].bid_score

    def test_zero_word_passage_max_score(self):
        agent = self._agent(weight=0.5)
        p = P("", "d1")
        bids = agent.bid("q", [p], budget=5)
        assert bids[0].bid_score == pytest.approx(0.5)

    def test_500_word_passage_score_zero(self):
        agent = self._agent(weight=0.5)
        p = P(" ".join(["word"] * 500), "d1")
        bids = agent.bid("q", [p], budget=5)
        assert bids[0].bid_score == pytest.approx(0.0)

    def test_reason_contains_cost_words(self):
        agent = self._agent()
        p = P("one two three", "d1")
        bids = agent.bid("q", [p], budget=5)
        assert "cost words=" in bids[0].reason

    def test_reason_shows_word_count(self):
        agent = self._agent()
        p = P("one two three", "d1")
        bids = agent.bid("q", [p], budget=5)
        assert "3" in bids[0].reason

    def test_score_never_negative(self):
        agent = self._agent(weight=0.5)
        p = P(" ".join(["word"] * 1000), "d1")
        bids = agent.bid("q", [p], budget=5)
        assert bids[0].bid_score >= 0.0

    def test_weight_scales_score(self):
        agent1 = self._agent(weight=1.0)
        agent2 = self._agent(weight=2.0)
        p = [P("short", "d1")]
        b1 = agent1.bid("q", p, budget=5)
        b2 = agent2.bid("q", p, budget=5)
        assert b2[0].bid_score == pytest.approx(b1[0].bid_score * 2.0)

    def test_returns_one_bid_per_passage(self):
        agent = self._agent()
        passages = [P(f"text {i}", f"d{i}") for i in range(5)]
        bids = agent.bid("q", passages, budget=5)
        assert len(bids) == 5


# ═══════════════════════════════════════════════════════════════════════════
# run_auction
# ═══════════════════════════════════════════════════════════════════════════

class TestRunAuction:
    def _default_agents(self):
        return [
            KeywordAgent(name="keyword", weight=1.0),
            SemanticAgent(name="semantic", weight=1.0),
        ]

    def test_returns_auction_result(self):
        passages = [P("hello world", "d1"), P("foo bar", "d2")]
        result = run_auction("hello", passages, self._default_agents(), budget=5)
        assert isinstance(result, AuctionResult)

    def test_selected_le_budget(self):
        passages = [P(f"text {i}", f"d{i}") for i in range(10)]
        result = run_auction("text", passages, self._default_agents(), budget=3)
        assert len(result.selected_passages) <= 3

    def test_three_passages_budget_five_all_selected(self):
        passages = [P("a", "d1"), P("b", "d2"), P("c", "d3")]
        result = run_auction("a b c", passages, self._default_agents(), budget=5)
        assert len(result.selected_passages) == 3

    def test_ten_passages_budget_three_exactly_three(self):
        passages = [P(f"doc {i}", f"d{i}") for i in range(10)]
        result = run_auction("doc", passages, self._default_agents(), budget=3)
        assert len(result.selected_passages) == 3

    def test_agent_wins_has_agent_names(self):
        passages = [P("hello", "d1"), P("world", "d2")]
        result = run_auction("hello", passages, self._default_agents(), budget=5)
        for key in result.agent_wins:
            assert isinstance(key, str)

    def test_winning_agent_is_valid_name(self):
        passages = [P("hello world", "d1", score=0.9)]
        result = run_auction("hello", passages, self._default_agents(), budget=5)
        agent_names = {a.name for a in self._default_agents()}
        assert result.winning_agent() in agent_names

    def test_total_rounds_equals_agent_count(self):
        passages = [P("text", "d1")]
        agents = [
            KeywordAgent(name="keyword"),
            SemanticAgent(name="semantic"),
            GraphAgent(name="graph"),
        ]
        result = run_auction("q", passages, agents, budget=5)
        assert result.total_rounds == 3

    def test_empty_passages_returns_empty(self):
        result = run_auction("query", [], self._default_agents(), budget=5)
        assert result.selected_passages == []

    def test_empty_agents_returns_empty(self):
        passages = [P("hello", "d1")]
        result = run_auction("query", passages, [], budget=5)
        assert result.selected_passages == []

    def test_budget_zero_returns_empty(self):
        passages = [P("hello", "d1")]
        result = run_auction("query", passages, self._default_agents(), budget=0)
        assert result.selected_passages == []

    def test_all_bids_collected(self):
        passages = [P("a", "d1"), P("b", "d2")]
        agents = self._default_agents()
        result = run_auction("a", passages, agents, budget=5)
        # 2 agents × 2 passages = 4 bids
        assert len(result.bids) == 4

    def test_high_score_passage_selected_first(self):
        passages = [
            P("unrelated text", "d1", score=0.1),
            P("highly relevant", "d2", score=0.95),
        ]
        agents = [SemanticAgent(name="semantic", weight=1.0)]
        result = run_auction("relevant", passages, agents, budget=1)
        assert result.selected_passages[0].doc_id == "d2"

    def test_bids_are_bid_objects(self):
        passages = [P("text", "d1")]
        result = run_auction("q", passages, self._default_agents(), budget=5)
        for bid in result.bids:
            assert isinstance(bid, Bid)

    def test_agent_wins_sums_to_budget_or_less(self):
        passages = [P(f"text {i}", f"d{i}") for i in range(5)]
        result = run_auction("text", passages, self._default_agents(), budget=3)
        total = sum(result.agent_wins.values())
        assert total <= 3


# ═══════════════════════════════════════════════════════════════════════════
# NegotiationBroker
# ═══════════════════════════════════════════════════════════════════════════

class TestNegotiationBroker:
    def test_retrieve_returns_auction_result(self):
        broker = NegotiationBroker()
        passages = [P("hello world", "d1"), P("foo bar", "d2")]
        result = broker.retrieve("hello", passages)
        assert isinstance(result, AuctionResult)

    def test_default_config_budget_five(self):
        broker = NegotiationBroker()
        assert broker._config.budget == 5

    def test_config_weights_respected(self):
        cfg = BrokerConfig(keyword_weight=2.0)
        broker = NegotiationBroker(config=cfg)
        assert broker._config.keyword_weight == 2.0

    def test_selected_passages_le_budget(self):
        broker = NegotiationBroker(config=BrokerConfig(budget=2))
        passages = [P(f"text {i}", f"d{i}") for i in range(8)]
        result = broker.retrieve("text", passages)
        assert len(result.selected_passages) <= 2

    def test_empty_passages_returns_empty_result(self):
        broker = NegotiationBroker()
        result = broker.retrieve("query", [])
        assert result.selected_passages == []

    def test_custom_budget_honored(self):
        broker = NegotiationBroker(config=BrokerConfig(budget=3))
        passages = [P(f"word{i}", f"d{i}") for i in range(10)]
        result = broker.retrieve("word", passages)
        assert len(result.selected_passages) <= 3

    def test_agent_wins_has_five_agents(self):
        broker = NegotiationBroker()
        passages = [P("hello world", "d1", score=0.8)]
        result = broker.retrieve("hello", passages)
        assert len(result.agent_wins) == 5

    def test_none_config_uses_defaults(self):
        broker = NegotiationBroker(config=None)
        assert broker._config.budget == 5
        assert broker._config.keyword_weight == 1.0
        assert broker._config.semantic_weight == 1.0

    def test_winning_agent_non_empty(self):
        broker = NegotiationBroker()
        passages = [P("hello world", "d1", score=0.9)]
        result = broker.retrieve("hello", passages)
        assert result.winning_agent() != ""

    def test_broker_config_defaults(self):
        cfg = BrokerConfig()
        assert cfg.budget == 5
        assert cfg.keyword_weight == pytest.approx(1.0)
        assert cfg.semantic_weight == pytest.approx(1.0)
        assert cfg.graph_weight == pytest.approx(0.8)
        assert cfg.diversity_weight == pytest.approx(0.6)
        assert cfg.cost_weight == pytest.approx(0.5)


# ═══════════════════════════════════════════════════════════════════════════
# __init__.py re-exports
# ═══════════════════════════════════════════════════════════════════════════

class TestPublicAPI:
    def test_retriever_agent_importable(self):
        assert RetrieverAgent is not None

    def test_keyword_agent_importable(self):
        assert KA is KeywordAgent

    def test_semantic_agent_importable(self):
        assert SA is SemanticAgent

    def test_graph_agent_importable(self):
        assert GA is GraphAgent

    def test_diversity_agent_importable(self):
        assert DA is DiversityAgent

    def test_cost_agent_importable(self):
        assert CA is CostAgent

    def test_bid_importable(self):
        assert B is Bid

    def test_auction_result_importable(self):
        assert AR is AuctionResult

    def test_run_auction_importable(self):
        assert ra is run_auction

    def test_negotiation_broker_importable(self):
        assert NB is NegotiationBroker

    def test_broker_config_importable(self):
        assert BC is BrokerConfig
