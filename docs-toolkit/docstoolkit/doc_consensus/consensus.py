"""Voting/consensus mechanism for documents (E250).

Multi-reviewer approval with weighted votes, quorum thresholds, and deadlines.
Stdlib-only, thread-safe via threading.Lock.
"""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class VoteType(Enum):
    """Type of vote cast by a voter."""

    APPROVE = "approve"
    REJECT = "reject"
    ABSTAIN = "abstain"


class ConsensusState(Enum):
    """State of a consensus ballot."""

    OPEN = "open"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


@dataclass
class Vote:
    """A single vote cast on a ballot."""

    voter_id: str
    vote_type: VoteType
    weight: float = 1.0
    reason: Optional[str] = None
    timestamp: float = 0.0


@dataclass
class ConsensusBallot:
    """A consensus ballot collecting weighted votes from eligible voters."""

    ballot_id: str
    doc_id: str
    state: ConsensusState
    created_at: float
    deadline: Optional[float] = None
    quorum: float = 0.5
    votes: list[Vote] = field(default_factory=list)
    eligible_voters: set[str] = field(default_factory=set)
    weights: dict[str, float] = field(default_factory=dict)
    description: str = ""


@dataclass
class ConsensusResult:
    """Outcome of evaluating a ballot."""

    approved: bool
    approve_weight: float
    reject_weight: float
    abstain_weight: float
    total_weight_cast: float
    required_weight: float
    quorum_met: bool
    state: ConsensusState


class DocConsensus:
    """Thread-safe registry of consensus ballots."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._ballots: dict[str, ConsensusBallot] = {}

    # --- ballot lifecycle ---

    def create_ballot(
        self,
        doc_id: str,
        eligible_voters: set[str],
        weights: dict[str, float] = None,
        quorum: float = 0.5,
        deadline: float = None,
        description: str = "",
        now: float = 0.0,
    ) -> ConsensusBallot:
        """Create a new ballot for the given document."""
        ballot_id = uuid.uuid4().hex
        weights = dict(weights) if weights else {}
        ballot = ConsensusBallot(
            ballot_id=ballot_id,
            doc_id=doc_id,
            state=ConsensusState.OPEN,
            created_at=now,
            deadline=deadline,
            quorum=quorum,
            votes=[],
            eligible_voters=set(eligible_voters),
            weights=weights,
            description=description,
        )
        with self._lock:
            self._ballots[ballot_id] = ballot
        return ballot

    def submit_vote(
        self,
        ballot_id: str,
        voter_id: str,
        vote_type: VoteType,
        reason: str = None,
        now: float = 0.0,
    ) -> Optional[Vote]:
        """Submit a vote. Replaces existing vote from same voter."""
        with self._lock:
            ballot = self._ballots.get(ballot_id)
            if ballot is None:
                return None
            if ballot.state != ConsensusState.OPEN:
                return None
            if ballot.deadline is not None and now >= ballot.deadline:
                ballot.state = ConsensusState.EXPIRED
                return None
            if voter_id not in ballot.eligible_voters:
                return None
            weight = ballot.weights.get(voter_id, 1.0)
            vote = Vote(
                voter_id=voter_id,
                vote_type=vote_type,
                weight=weight,
                reason=reason,
                timestamp=now,
            )
            # Remove previous vote from this voter
            ballot.votes = [v for v in ballot.votes if v.voter_id != voter_id]
            ballot.votes.append(vote)
            # Try to decide ballot state immediately
            self._maybe_decide(ballot)
            return vote

    def cancel_ballot(self, ballot_id: str) -> bool:
        """Cancel an open ballot."""
        with self._lock:
            ballot = self._ballots.get(ballot_id)
            if ballot is None:
                return False
            if ballot.state != ConsensusState.OPEN:
                return False
            ballot.state = ConsensusState.CANCELLED
            return True

    def expire_overdue(self, now: float = 0.0) -> int:
        """Mark all OPEN ballots past their deadline as EXPIRED. Returns count."""
        count = 0
        with self._lock:
            for ballot in self._ballots.values():
                if (
                    ballot.state == ConsensusState.OPEN
                    and ballot.deadline is not None
                    and now >= ballot.deadline
                ):
                    ballot.state = ConsensusState.EXPIRED
                    count += 1
        return count

    def revoke_vote(self, ballot_id: str, voter_id: str) -> bool:
        """Remove an existing vote from the ballot."""
        with self._lock:
            ballot = self._ballots.get(ballot_id)
            if ballot is None:
                return False
            if ballot.state != ConsensusState.OPEN:
                return False
            before = len(ballot.votes)
            ballot.votes = [v for v in ballot.votes if v.voter_id != voter_id]
            return len(ballot.votes) != before

    def extend_deadline(self, ballot_id: str, new_deadline: float) -> bool:
        """Extend (or set) the deadline of an open ballot."""
        with self._lock:
            ballot = self._ballots.get(ballot_id)
            if ballot is None:
                return False
            if ballot.state != ConsensusState.OPEN:
                return False
            ballot.deadline = new_deadline
            return True

    # --- queries ---

    def get_ballot(self, ballot_id: str) -> Optional[ConsensusBallot]:
        """Return a ballot by id, or None."""
        with self._lock:
            return self._ballots.get(ballot_id)

    def result(self, ballot_id: str, now: float = 0.0) -> Optional[ConsensusResult]:
        """Compute the current result of a ballot."""
        with self._lock:
            ballot = self._ballots.get(ballot_id)
            if ballot is None:
                return None
            # Apply expiry if necessary (does not change weights).
            if (
                ballot.state == ConsensusState.OPEN
                and ballot.deadline is not None
                and now >= ballot.deadline
            ):
                ballot.state = ConsensusState.EXPIRED
            return self._compute_result(ballot)

    def is_decided(self, ballot_id: str) -> bool:
        """True if ballot is no longer OPEN."""
        with self._lock:
            ballot = self._ballots.get(ballot_id)
            if ballot is None:
                return False
            return ballot.state != ConsensusState.OPEN

    def pending_voters(self, ballot_id: str) -> set[str]:
        """Eligible voters who haven't voted yet."""
        with self._lock:
            ballot = self._ballots.get(ballot_id)
            if ballot is None:
                return set()
            voted = {v.voter_id for v in ballot.votes}
            return set(ballot.eligible_voters) - voted

    def voted_voters(self, ballot_id: str) -> set[str]:
        """Eligible voters who have cast a vote."""
        with self._lock:
            ballot = self._ballots.get(ballot_id)
            if ballot is None:
                return set()
            return {v.voter_id for v in ballot.votes}

    def ballots_for_doc(self, doc_id: str) -> list[ConsensusBallot]:
        """All ballots for a given document, in insertion order."""
        with self._lock:
            return [b for b in self._ballots.values() if b.doc_id == doc_id]

    def open_ballots(self, now: float = 0.0) -> list[ConsensusBallot]:
        """All currently open ballots (auto-expires overdue ones first)."""
        with self._lock:
            for ballot in self._ballots.values():
                if (
                    ballot.state == ConsensusState.OPEN
                    and ballot.deadline is not None
                    and now >= ballot.deadline
                ):
                    ballot.state = ConsensusState.EXPIRED
            return [
                b for b in self._ballots.values() if b.state == ConsensusState.OPEN
            ]

    @property
    def total_ballots(self) -> int:
        """Total number of ballots tracked."""
        with self._lock:
            return len(self._ballots)

    def clear(self) -> None:
        """Remove all ballots."""
        with self._lock:
            self._ballots.clear()

    # --- internals ---

    def _eligible_total_weight(self, ballot: ConsensusBallot) -> float:
        total = 0.0
        for voter in ballot.eligible_voters:
            total += ballot.weights.get(voter, 1.0)
        return total

    def _compute_result(self, ballot: ConsensusBallot) -> ConsensusResult:
        approve_w = sum(
            v.weight for v in ballot.votes if v.vote_type == VoteType.APPROVE
        )
        reject_w = sum(
            v.weight for v in ballot.votes if v.vote_type == VoteType.REJECT
        )
        abstain_w = sum(
            v.weight for v in ballot.votes if v.vote_type == VoteType.ABSTAIN
        )
        total_cast = approve_w + reject_w + abstain_w
        eligible_total = self._eligible_total_weight(ballot)
        required = ballot.quorum * eligible_total
        quorum_met = total_cast >= required
        approved = quorum_met and (approve_w > reject_w)
        return ConsensusResult(
            approved=approved,
            approve_weight=approve_w,
            reject_weight=reject_w,
            abstain_weight=abstain_w,
            total_weight_cast=total_cast,
            required_weight=required,
            quorum_met=quorum_met,
            state=ballot.state,
        )

    def _maybe_decide(self, ballot: ConsensusBallot) -> None:
        """If all eligible voters have voted, transition ballot to terminal state."""
        if ballot.state != ConsensusState.OPEN:
            return
        voted = {v.voter_id for v in ballot.votes}
        if voted != set(ballot.eligible_voters):
            return  # not everyone has voted yet
        result = self._compute_result(ballot)
        if result.approved:
            ballot.state = ConsensusState.APPROVED
        else:
            ballot.state = ConsensusState.REJECTED
