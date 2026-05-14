"""Tests for docstoolkit.doc_consensus (E250)."""
from __future__ import annotations

import pytest

from docstoolkit.doc_consensus import (
    ConsensusBallot,
    ConsensusResult,
    ConsensusState,
    DocConsensus,
    Vote,
    VoteType,
)


# ---------- helpers ----------

def _ballot(dc: DocConsensus, **kwargs) -> ConsensusBallot:
    defaults = dict(
        doc_id="doc-1",
        eligible_voters={"alice", "bob", "carol"},
        quorum=0.5,
    )
    defaults.update(kwargs)
    return dc.create_ballot(**defaults)


# ---------- enum and dataclass tests ----------

class TestVoteType:
    def test_members(self):
        assert VoteType.APPROVE.value == "approve"
        assert VoteType.REJECT.value == "reject"
        assert VoteType.ABSTAIN.value == "abstain"

    def test_distinct(self):
        assert VoteType.APPROVE != VoteType.REJECT
        assert VoteType.APPROVE != VoteType.ABSTAIN

    def test_iterable(self):
        assert {v.name for v in VoteType} == {"APPROVE", "REJECT", "ABSTAIN"}


class TestConsensusState:
    def test_members(self):
        for name in ("OPEN", "APPROVED", "REJECTED", "EXPIRED", "CANCELLED"):
            assert hasattr(ConsensusState, name)

    def test_open_value(self):
        assert ConsensusState.OPEN.value == "open"

    def test_distinct(self):
        assert ConsensusState.APPROVED != ConsensusState.REJECTED


class TestVote:
    def test_construct(self):
        v = Vote("alice", VoteType.APPROVE)
        assert v.voter_id == "alice"
        assert v.vote_type == VoteType.APPROVE
        assert v.weight == 1.0
        assert v.reason is None
        assert v.timestamp == 0.0

    def test_with_fields(self):
        v = Vote("bob", VoteType.REJECT, weight=2.5, reason="bad", timestamp=42.0)
        assert v.weight == 2.5
        assert v.reason == "bad"
        assert v.timestamp == 42.0


class TestConsensusBallot:
    def test_defaults(self):
        b = ConsensusBallot(
            ballot_id="x", doc_id="d", state=ConsensusState.OPEN, created_at=1.0
        )
        assert b.deadline is None
        assert b.quorum == 0.5
        assert b.votes == []
        assert b.eligible_voters == set()
        assert b.weights == {}
        assert b.description == ""

    def test_mutable_defaults_independent(self):
        b1 = ConsensusBallot("a", "d", ConsensusState.OPEN, 0.0)
        b2 = ConsensusBallot("b", "d", ConsensusState.OPEN, 0.0)
        b1.votes.append(Vote("x", VoteType.APPROVE))
        assert b2.votes == []


class TestConsensusResult:
    def test_construct(self):
        r = ConsensusResult(
            approved=True,
            approve_weight=2.0,
            reject_weight=1.0,
            abstain_weight=0.0,
            total_weight_cast=3.0,
            required_weight=1.5,
            quorum_met=True,
            state=ConsensusState.OPEN,
        )
        assert r.approved is True
        assert r.approve_weight == 2.0
        assert r.quorum_met is True


# ---------- create_ballot ----------

class TestCreateBallot:
    def test_basic_create(self):
        dc = DocConsensus()
        b = _ballot(dc)
        assert b.state == ConsensusState.OPEN
        assert b.doc_id == "doc-1"
        assert b.eligible_voters == {"alice", "bob", "carol"}
        assert b.ballot_id

    def test_unique_ballot_ids(self):
        dc = DocConsensus()
        b1 = _ballot(dc)
        b2 = _ballot(dc)
        assert b1.ballot_id != b2.ballot_id

    def test_stored(self):
        dc = DocConsensus()
        b = _ballot(dc)
        assert dc.get_ballot(b.ballot_id) is b

    def test_with_weights(self):
        dc = DocConsensus()
        b = _ballot(dc, weights={"alice": 3.0, "bob": 1.0})
        assert b.weights == {"alice": 3.0, "bob": 1.0}

    def test_with_deadline(self):
        dc = DocConsensus()
        b = _ballot(dc, deadline=100.0, now=0.0)
        assert b.deadline == 100.0
        assert b.created_at == 0.0

    def test_with_description(self):
        dc = DocConsensus()
        b = _ballot(dc, description="vote on draft")
        assert b.description == "vote on draft"

    def test_eligible_voters_copied(self):
        dc = DocConsensus()
        voters = {"x", "y"}
        b = _ballot(dc, eligible_voters=voters)
        voters.add("z")
        assert "z" not in b.eligible_voters


# ---------- submit_vote ----------

class TestSubmitVote:
    def test_basic(self):
        dc = DocConsensus()
        b = _ballot(dc)
        v = dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        assert v is not None
        assert v.voter_id == "alice"
        assert v.vote_type == VoteType.APPROVE

    def test_unknown_ballot(self):
        dc = DocConsensus()
        assert dc.submit_vote("nope", "alice", VoteType.APPROVE) is None

    def test_uses_default_weight(self):
        dc = DocConsensus()
        b = _ballot(dc)
        v = dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        assert v.weight == 1.0

    def test_uses_specified_weight(self):
        dc = DocConsensus()
        b = _ballot(dc, weights={"alice": 5.0})
        v = dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        assert v.weight == 5.0

    def test_reason_recorded(self):
        dc = DocConsensus()
        b = _ballot(dc)
        v = dc.submit_vote(b.ballot_id, "alice", VoteType.REJECT, reason="x")
        assert v.reason == "x"

    def test_timestamp_recorded(self):
        dc = DocConsensus()
        b = _ballot(dc)
        v = dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE, now=42.0)
        assert v.timestamp == 42.0

    def test_appended_to_ballot(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        assert len(dc.get_ballot(b.ballot_id).votes) == 1


class TestSubmitVoteChange:
    def test_replaces_previous(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        dc.submit_vote(b.ballot_id, "alice", VoteType.REJECT)
        votes = dc.get_ballot(b.ballot_id).votes
        assert len(votes) == 1
        assert votes[0].vote_type == VoteType.REJECT

    def test_other_voters_unaffected(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        dc.submit_vote(b.ballot_id, "bob", VoteType.APPROVE)
        dc.submit_vote(b.ballot_id, "alice", VoteType.REJECT)
        votes = {v.voter_id: v.vote_type for v in dc.get_ballot(b.ballot_id).votes}
        assert votes == {"alice": VoteType.REJECT, "bob": VoteType.APPROVE}


class TestSubmitVoteIneligible:
    def test_not_in_set(self):
        dc = DocConsensus()
        b = _ballot(dc)
        assert dc.submit_vote(b.ballot_id, "stranger", VoteType.APPROVE) is None
        assert dc.get_ballot(b.ballot_id).votes == []

    def test_after_cancel(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.cancel_ballot(b.ballot_id)
        assert dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE) is None

    def test_after_expire(self):
        dc = DocConsensus()
        b = _ballot(dc, deadline=10.0, now=0.0)
        assert (
            dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE, now=20.0) is None
        )
        assert dc.get_ballot(b.ballot_id).state == ConsensusState.EXPIRED


# ---------- cancel_ballot ----------

class TestCancelBallot:
    def test_cancel_open(self):
        dc = DocConsensus()
        b = _ballot(dc)
        assert dc.cancel_ballot(b.ballot_id) is True
        assert dc.get_ballot(b.ballot_id).state == ConsensusState.CANCELLED

    def test_cancel_unknown(self):
        dc = DocConsensus()
        assert dc.cancel_ballot("nope") is False

    def test_cancel_already_cancelled(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.cancel_ballot(b.ballot_id)
        assert dc.cancel_ballot(b.ballot_id) is False

    def test_cancel_after_decided(self):
        dc = DocConsensus()
        b = _ballot(dc, eligible_voters={"alice"})
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        # alice was the only eligible voter -> ballot should be decided
        assert dc.is_decided(b.ballot_id)
        assert dc.cancel_ballot(b.ballot_id) is False


# ---------- expire_overdue ----------

class TestExpireOverdue:
    def test_expire_one(self):
        dc = DocConsensus()
        b = _ballot(dc, deadline=10.0)
        n = dc.expire_overdue(now=20.0)
        assert n == 1
        assert dc.get_ballot(b.ballot_id).state == ConsensusState.EXPIRED

    def test_not_yet_due(self):
        dc = DocConsensus()
        b = _ballot(dc, deadline=100.0)
        n = dc.expire_overdue(now=50.0)
        assert n == 0
        assert dc.get_ballot(b.ballot_id).state == ConsensusState.OPEN

    def test_no_deadline_not_expired(self):
        dc = DocConsensus()
        b = _ballot(dc)
        n = dc.expire_overdue(now=10_000.0)
        assert n == 0
        assert dc.get_ballot(b.ballot_id).state == ConsensusState.OPEN

    def test_already_cancelled_not_expired(self):
        dc = DocConsensus()
        b = _ballot(dc, deadline=10.0)
        dc.cancel_ballot(b.ballot_id)
        n = dc.expire_overdue(now=20.0)
        assert n == 0
        assert dc.get_ballot(b.ballot_id).state == ConsensusState.CANCELLED

    def test_multiple_ballots(self):
        dc = DocConsensus()
        _ballot(dc, deadline=10.0)
        _ballot(dc, deadline=10.0)
        _ballot(dc, deadline=100.0)
        n = dc.expire_overdue(now=50.0)
        assert n == 2


# ---------- get_ballot ----------

class TestGetBallot:
    def test_present(self):
        dc = DocConsensus()
        b = _ballot(dc)
        assert dc.get_ballot(b.ballot_id).ballot_id == b.ballot_id

    def test_absent(self):
        dc = DocConsensus()
        assert dc.get_ballot("nope") is None


# ---------- result: approve ----------

class TestResultApprove:
    def test_simple_majority(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        dc.submit_vote(b.ballot_id, "bob", VoteType.APPROVE)
        r = dc.result(b.ballot_id)
        assert r.approved is True
        assert r.approve_weight == 2.0
        assert r.reject_weight == 0.0
        assert r.quorum_met is True

    def test_all_approve(self):
        dc = DocConsensus()
        b = _ballot(dc)
        for v in ("alice", "bob", "carol"):
            dc.submit_vote(b.ballot_id, v, VoteType.APPROVE)
        r = dc.result(b.ballot_id)
        assert r.approved is True
        assert r.approve_weight == 3.0

    def test_approve_state_terminal(self):
        dc = DocConsensus()
        b = _ballot(dc, eligible_voters={"alice"})
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        assert dc.get_ballot(b.ballot_id).state == ConsensusState.APPROVED


# ---------- result: reject ----------

class TestResultReject:
    def test_majority_reject(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.submit_vote(b.ballot_id, "alice", VoteType.REJECT)
        dc.submit_vote(b.ballot_id, "bob", VoteType.REJECT)
        r = dc.result(b.ballot_id)
        assert r.approved is False
        assert r.reject_weight == 2.0

    def test_tie_not_approved(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        dc.submit_vote(b.ballot_id, "bob", VoteType.REJECT)
        r = dc.result(b.ballot_id)
        # tie -> not approved (approve > reject required)
        assert r.approved is False

    def test_reject_state_terminal(self):
        dc = DocConsensus()
        b = _ballot(dc, eligible_voters={"alice"})
        dc.submit_vote(b.ballot_id, "alice", VoteType.REJECT)
        assert dc.get_ballot(b.ballot_id).state == ConsensusState.REJECTED


# ---------- result: quorum ----------

class TestResultQuorum:
    def test_no_votes(self):
        dc = DocConsensus()
        b = _ballot(dc)
        r = dc.result(b.ballot_id)
        assert r.approved is False
        assert r.quorum_met is False
        assert r.required_weight == pytest.approx(1.5)  # 0.5 * 3

    def test_below_quorum(self):
        dc = DocConsensus()
        b = _ballot(dc, quorum=0.75)
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        r = dc.result(b.ballot_id)
        # required = 0.75 * 3 = 2.25, cast = 1
        assert r.quorum_met is False
        assert r.approved is False

    def test_meets_quorum_via_abstain(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        dc.submit_vote(b.ballot_id, "bob", VoteType.ABSTAIN)
        r = dc.result(b.ballot_id)
        assert r.quorum_met is True  # 2/3 cast, 0.5*3=1.5 required
        assert r.approved is True

    def test_zero_quorum_always_met(self):
        dc = DocConsensus()
        b = _ballot(dc, quorum=0.0)
        r = dc.result(b.ballot_id)
        assert r.quorum_met is True

    def test_required_weight_calc(self):
        dc = DocConsensus()
        b = _ballot(dc, weights={"alice": 4.0, "bob": 2.0, "carol": 2.0}, quorum=0.5)
        r = dc.result(b.ballot_id)
        assert r.required_weight == pytest.approx(4.0)  # 0.5 * 8


# ---------- result: expired ----------

class TestResultExpired:
    def test_expired_state(self):
        dc = DocConsensus()
        b = _ballot(dc, deadline=10.0)
        r = dc.result(b.ballot_id, now=20.0)
        assert r.state == ConsensusState.EXPIRED

    def test_expired_not_approved(self):
        dc = DocConsensus()
        b = _ballot(dc, deadline=10.0)
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE, now=1.0)
        r = dc.result(b.ballot_id, now=20.0)
        # quorum not met (only 1/3), so even after expiry not approved
        assert r.state == ConsensusState.EXPIRED
        assert r.approved is False

    def test_result_unknown_ballot(self):
        dc = DocConsensus()
        assert dc.result("nope") is None


# ---------- is_decided ----------

class TestIsDecided:
    def test_open_not_decided(self):
        dc = DocConsensus()
        b = _ballot(dc)
        assert dc.is_decided(b.ballot_id) is False

    def test_approved_decided(self):
        dc = DocConsensus()
        b = _ballot(dc, eligible_voters={"alice"})
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        assert dc.is_decided(b.ballot_id) is True

    def test_cancelled_decided(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.cancel_ballot(b.ballot_id)
        assert dc.is_decided(b.ballot_id) is True

    def test_unknown_not_decided(self):
        dc = DocConsensus()
        assert dc.is_decided("nope") is False


# ---------- pending_voters ----------

class TestPendingVoters:
    def test_initially_all(self):
        dc = DocConsensus()
        b = _ballot(dc)
        assert dc.pending_voters(b.ballot_id) == {"alice", "bob", "carol"}

    def test_after_some_votes(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        assert dc.pending_voters(b.ballot_id) == {"bob", "carol"}

    def test_unknown(self):
        dc = DocConsensus()
        assert dc.pending_voters("nope") == set()


# ---------- voted_voters ----------

class TestVotedVoters:
    def test_initially_empty(self):
        dc = DocConsensus()
        b = _ballot(dc)
        assert dc.voted_voters(b.ballot_id) == set()

    def test_after_votes(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        dc.submit_vote(b.ballot_id, "bob", VoteType.REJECT)
        assert dc.voted_voters(b.ballot_id) == {"alice", "bob"}

    def test_unknown(self):
        dc = DocConsensus()
        assert dc.voted_voters("nope") == set()


# ---------- ballots_for_doc ----------

class TestBallotsForDoc:
    def test_empty(self):
        dc = DocConsensus()
        assert dc.ballots_for_doc("doc-1") == []

    def test_multiple_for_same_doc(self):
        dc = DocConsensus()
        b1 = _ballot(dc, doc_id="x")
        b2 = _ballot(dc, doc_id="x")
        _ballot(dc, doc_id="y")
        ids = {b.ballot_id for b in dc.ballots_for_doc("x")}
        assert ids == {b1.ballot_id, b2.ballot_id}


# ---------- open_ballots ----------

class TestOpenBallots:
    def test_lists_open(self):
        dc = DocConsensus()
        b = _ballot(dc)
        ids = {x.ballot_id for x in dc.open_ballots()}
        assert b.ballot_id in ids

    def test_excludes_cancelled(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.cancel_ballot(b.ballot_id)
        assert dc.open_ballots() == []

    def test_auto_expires_overdue(self):
        dc = DocConsensus()
        b = _ballot(dc, deadline=10.0)
        assert dc.open_ballots(now=20.0) == []
        assert dc.get_ballot(b.ballot_id).state == ConsensusState.EXPIRED


# ---------- revoke_vote ----------

class TestRevokeVote:
    def test_revoke_existing(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        assert dc.revoke_vote(b.ballot_id, "alice") is True
        assert dc.voted_voters(b.ballot_id) == set()

    def test_revoke_missing(self):
        dc = DocConsensus()
        b = _ballot(dc)
        assert dc.revoke_vote(b.ballot_id, "alice") is False

    def test_revoke_unknown_ballot(self):
        dc = DocConsensus()
        assert dc.revoke_vote("nope", "alice") is False

    def test_revoke_after_cancel(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        dc.cancel_ballot(b.ballot_id)
        assert dc.revoke_vote(b.ballot_id, "alice") is False


# ---------- extend_deadline ----------

class TestExtendDeadline:
    def test_extend(self):
        dc = DocConsensus()
        b = _ballot(dc, deadline=10.0)
        assert dc.extend_deadline(b.ballot_id, 100.0) is True
        assert dc.get_ballot(b.ballot_id).deadline == 100.0

    def test_extend_unknown(self):
        dc = DocConsensus()
        assert dc.extend_deadline("nope", 100.0) is False

    def test_extend_after_cancel(self):
        dc = DocConsensus()
        b = _ballot(dc, deadline=10.0)
        dc.cancel_ballot(b.ballot_id)
        assert dc.extend_deadline(b.ballot_id, 100.0) is False

    def test_extend_set_initial(self):
        dc = DocConsensus()
        b = _ballot(dc)  # no deadline
        assert dc.extend_deadline(b.ballot_id, 50.0) is True
        assert dc.get_ballot(b.ballot_id).deadline == 50.0


# ---------- weighted voting ----------

class TestWeightedVoting:
    def test_heavy_approve_wins(self):
        dc = DocConsensus()
        b = _ballot(
            dc,
            eligible_voters={"chair", "member1", "member2"},
            weights={"chair": 5.0, "member1": 1.0, "member2": 1.0},
            quorum=0.5,
        )
        dc.submit_vote(b.ballot_id, "chair", VoteType.APPROVE)
        dc.submit_vote(b.ballot_id, "member1", VoteType.REJECT)
        r = dc.result(b.ballot_id)
        assert r.approve_weight == 5.0
        assert r.reject_weight == 1.0
        assert r.approved is True

    def test_heavy_reject_wins(self):
        dc = DocConsensus()
        b = _ballot(
            dc,
            eligible_voters={"chair", "member1"},
            weights={"chair": 10.0, "member1": 1.0},
        )
        dc.submit_vote(b.ballot_id, "chair", VoteType.REJECT)
        dc.submit_vote(b.ballot_id, "member1", VoteType.APPROVE)
        r = dc.result(b.ballot_id)
        assert r.approved is False

    def test_default_weight_for_missing(self):
        dc = DocConsensus()
        b = _ballot(dc, weights={"alice": 3.0})  # bob, carol default 1.0
        dc.submit_vote(b.ballot_id, "bob", VoteType.APPROVE)
        v = dc.get_ballot(b.ballot_id).votes[0]
        assert v.weight == 1.0


# ---------- total_ballots ----------

class TestTotalBallots:
    def test_empty(self):
        dc = DocConsensus()
        assert dc.total_ballots == 0

    def test_grows(self):
        dc = DocConsensus()
        _ballot(dc)
        _ballot(dc)
        assert dc.total_ballots == 2


# ---------- clear ----------

class TestClear:
    def test_clear_empty(self):
        dc = DocConsensus()
        dc.clear()
        assert dc.total_ballots == 0

    def test_clear_removes_all(self):
        dc = DocConsensus()
        _ballot(dc)
        _ballot(dc)
        dc.clear()
        assert dc.total_ballots == 0

    def test_clear_then_create(self):
        dc = DocConsensus()
        _ballot(dc)
        dc.clear()
        b = _ballot(dc)
        assert dc.get_ballot(b.ballot_id) is b


# ---------- edge cases ----------

class TestEdgeCases:
    def test_single_voter_approve(self):
        dc = DocConsensus()
        b = _ballot(dc, eligible_voters={"alice"})
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        assert dc.get_ballot(b.ballot_id).state == ConsensusState.APPROVED

    def test_abstain_only_no_approval(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.submit_vote(b.ballot_id, "alice", VoteType.ABSTAIN)
        dc.submit_vote(b.ballot_id, "bob", VoteType.ABSTAIN)
        r = dc.result(b.ballot_id)
        assert r.approved is False
        assert r.quorum_met is True  # 2 cast >= 1.5 required
        assert r.approve_weight == 0
        assert r.reject_weight == 0
        assert r.abstain_weight == 2.0

    def test_quorum_one_means_unanimous_cast(self):
        dc = DocConsensus()
        b = _ballot(dc, quorum=1.0)
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        dc.submit_vote(b.ballot_id, "bob", VoteType.APPROVE)
        r = dc.result(b.ballot_id)
        assert r.quorum_met is False  # 2 cast < 3 required

    def test_change_vote_after_submission(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        dc.submit_vote(b.ballot_id, "alice", VoteType.REJECT)
        r = dc.result(b.ballot_id)
        assert r.approve_weight == 0
        assert r.reject_weight == 1.0

    def test_decide_when_everyone_votes(self):
        dc = DocConsensus()
        b = _ballot(dc)
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        dc.submit_vote(b.ballot_id, "bob", VoteType.APPROVE)
        # still open until carol votes
        assert dc.get_ballot(b.ballot_id).state == ConsensusState.OPEN
        dc.submit_vote(b.ballot_id, "carol", VoteType.REJECT)
        assert dc.get_ballot(b.ballot_id).state == ConsensusState.APPROVED

    def test_cannot_vote_after_decided(self):
        dc = DocConsensus()
        b = _ballot(dc, eligible_voters={"alice"})
        dc.submit_vote(b.ballot_id, "alice", VoteType.APPROVE)
        # ballot now APPROVED; another vote should fail
        assert dc.submit_vote(b.ballot_id, "alice", VoteType.REJECT) is None

    def test_empty_eligible_voters(self):
        dc = DocConsensus()
        b = dc.create_ballot(doc_id="d", eligible_voters=set())
        r = dc.result(b.ballot_id)
        assert r.required_weight == 0.0
        assert r.quorum_met is True
        assert r.approved is False  # 0 approve > 0 reject is False

    def test_result_after_expire_overdue(self):
        dc = DocConsensus()
        b = _ballot(dc, deadline=10.0)
        dc.expire_overdue(now=20.0)
        r = dc.result(b.ballot_id, now=20.0)
        assert r.state == ConsensusState.EXPIRED
