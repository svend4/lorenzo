"""Vickrey-style auction that allocates context-window slots to passages."""

from dataclasses import dataclass, field


@dataclass
class Bid:
    """One agent's bid for one passage."""
    agent_name: str
    passage_idx: int       # index in original passages list
    doc_id: str
    bid_score: float       # 0-1, higher = more strongly wants this passage
    reason: str = ""


@dataclass
class AuctionResult:
    """Final selected passages after auction."""
    selected_passages: list                                 # list of Passage-like objects
    bids: list = field(default_factory=list)                # all Bid objects collected
    agent_wins: dict = field(default_factory=dict)          # {agent_name: count of winning bids}
    total_rounds: int = 0

    def winning_agent(self) -> str:
        """Return name of agent with most wins."""
        if not self.agent_wins:
            return ""
        return max(self.agent_wins, key=lambda k: self.agent_wins[k])


def run_auction(
    query: str,
    passages: list,
    agents: list,   # list[RetrieverAgent]
    budget: int = 5,
) -> AuctionResult:
    """Run a Vickrey-style auction for context window slots.

    Algorithm:
    1. Collect all bids from all agents.
    2. For each passage_idx: aggregate_score = sum of bid_scores from all agents.
    3. Sort passages by aggregate_score descending.
    4. Select top-budget passages.
    5. Track which agent had highest bid for each selected passage (agent_wins).
    """
    if not passages or not agents or budget <= 0:
        return AuctionResult(
            selected_passages=[],
            bids=[],
            agent_wins={},
            total_rounds=len(agents),
        )

    # Step 1: collect all bids
    all_bids: list = []
    for agent in agents:
        agent_bids = agent.bid(query, passages, budget)
        all_bids.extend(agent_bids)

    # Step 2: aggregate scores per passage index
    # agg_scores[idx] = sum of bid_scores
    agg_scores: dict = {i: 0.0 for i in range(len(passages))}
    # bids_by_idx[idx] = list of Bid objects
    bids_by_idx: dict = {i: [] for i in range(len(passages))}

    for bid in all_bids:
        if 0 <= bid.passage_idx < len(passages):
            agg_scores[bid.passage_idx] += bid.bid_score
            bids_by_idx[bid.passage_idx].append(bid)

    # Step 3: sort passage indices by aggregate score descending
    sorted_idxs = sorted(agg_scores.keys(), key=lambda i: agg_scores[i], reverse=True)

    # Step 4: select top-budget passages
    selected_idxs = sorted_idxs[:budget]
    selected_passages = [passages[i] for i in selected_idxs]

    # Step 5: track agent_wins — which agent had the highest individual bid
    # for each selected passage
    agent_wins: dict = {}
    for agent in agents:
        agent_wins[agent.name] = 0

    for idx in selected_idxs:
        passage_bids = bids_by_idx[idx]
        if passage_bids:
            best_bid = max(passage_bids, key=lambda b: b.bid_score)
            agent_wins[best_bid.agent_name] = agent_wins.get(best_bid.agent_name, 0) + 1

    return AuctionResult(
        selected_passages=selected_passages,
        bids=all_bids,
        agent_wins=agent_wins,
        total_rounds=len(agents),
    )
