"""Document consensus module for docs-toolkit (E250).

Provides voting/consensus mechanism for documents: weighted votes, quorum
thresholds, deadlines. Stdlib-only.

Quick start::

    from docstoolkit.doc_consensus import (
        DocConsensus, VoteType, ConsensusState,
    )

    dc = DocConsensus()
    ballot = dc.create_ballot(
        doc_id="doc-1",
        eligible_voters={"alice", "bob", "carol"},
        weights={"alice": 2.0, "bob": 1.0, "carol": 1.0},
        quorum=0.5,
    )
    dc.submit_vote(ballot.ballot_id, "alice", VoteType.APPROVE)
    dc.submit_vote(ballot.ballot_id, "bob", VoteType.APPROVE)
    result = dc.result(ballot.ballot_id)
    assert result.approved is True
"""
from docstoolkit.doc_consensus.consensus import (
    VoteType,
    ConsensusState,
    Vote,
    ConsensusBallot,
    ConsensusResult,
    DocConsensus,
)

__all__ = [
    "VoteType",
    "ConsensusState",
    "Vote",
    "ConsensusBallot",
    "ConsensusResult",
    "DocConsensus",
]
