"""Tests for docstoolkit.doc_review (E200)."""
from __future__ import annotations

import pytest

from docstoolkit.doc_review import (
    Comment,
    ConsensusResult,
    DocReview,
    Review,
    ReviewState,
    ReviewVerdict,
    ReviewVerdictRecord,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _make_review(rv: DocReview, **kwargs) -> Review:
    defaults = dict(
        doc_id="doc-1",
        requester="alice",
        reviewers=["bob", "carol"],
        min_approvals=1,
        now=1.0,
    )
    defaults.update(kwargs)
    return rv.create_review(**defaults)


# ---------------------------------------------------------------------------
# Enum tests
# ---------------------------------------------------------------------------
class TestReviewState:
    def test_all_states_exist(self):
        assert ReviewState.REQUESTED
        assert ReviewState.IN_PROGRESS
        assert ReviewState.APPROVED
        assert ReviewState.REJECTED
        assert ReviewState.CHANGES_REQUESTED
        assert ReviewState.WITHDRAWN

    def test_states_are_distinct(self):
        values = {s.value for s in ReviewState}
        assert len(values) == 6

    def test_state_equality(self):
        assert ReviewState.REQUESTED == ReviewState.REQUESTED
        assert ReviewState.REQUESTED != ReviewState.APPROVED


class TestReviewVerdict:
    def test_all_verdicts_exist(self):
        assert ReviewVerdict.APPROVE
        assert ReviewVerdict.REQUEST_CHANGES
        assert ReviewVerdict.REJECT
        assert ReviewVerdict.COMMENT

    def test_verdicts_are_distinct(self):
        values = {v.value for v in ReviewVerdict}
        assert len(values) == 4


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------
class TestComment:
    def test_create_minimal(self):
        c = Comment(comment_id=1, reviewer="bob", text="hi", created_at=1.0)
        assert c.comment_id == 1
        assert c.reviewer == "bob"
        assert c.text == "hi"
        assert c.created_at == 1.0
        assert c.line_num is None
        assert c.resolved is False

    def test_create_with_line(self):
        c = Comment(
            comment_id=2, reviewer="carol", text="typo",
            created_at=2.0, line_num=42,
        )
        assert c.line_num == 42

    def test_mutable_resolved(self):
        c = Comment(comment_id=1, reviewer="bob", text="hi", created_at=1.0)
        c.resolved = True
        assert c.resolved is True


class TestReviewVerdictRecord:
    def test_create_minimal(self):
        v = ReviewVerdictRecord(
            reviewer="bob", verdict=ReviewVerdict.APPROVE, submitted_at=1.0,
        )
        assert v.reviewer == "bob"
        assert v.verdict == ReviewVerdict.APPROVE
        assert v.reason is None

    def test_create_with_reason(self):
        v = ReviewVerdictRecord(
            reviewer="bob", verdict=ReviewVerdict.REJECT,
            submitted_at=1.0, reason="too short",
        )
        assert v.reason == "too short"


class TestReview:
    def test_create_review_dataclass(self):
        r = Review(
            review_id="r1",
            doc_id="d1",
            requester="alice",
            reviewers={"bob"},
            state=ReviewState.REQUESTED,
            verdicts=[],
            comments=[],
            created_at=1.0,
            updated_at=1.0,
        )
        assert r.review_id == "r1"
        assert r.min_approvals == 1

    def test_review_fields_mutable(self):
        r = Review(
            review_id="r1",
            doc_id="d1",
            requester="alice",
            reviewers={"bob"},
            state=ReviewState.REQUESTED,
            verdicts=[],
            comments=[],
            created_at=1.0,
            updated_at=1.0,
        )
        r.state = ReviewState.APPROVED
        assert r.state == ReviewState.APPROVED


class TestConsensusResult:
    def test_create(self):
        c = ConsensusResult(
            approved=True, approve_count=2, reject_count=0,
            changes_count=0, pending_count=0,
        )
        assert c.approved is True
        assert c.approve_count == 2


# ---------------------------------------------------------------------------
# DocReview API tests
# ---------------------------------------------------------------------------
class TestCreateReview:
    def test_basic_create(self):
        rv = DocReview()
        r = _make_review(rv)
        assert r.doc_id == "doc-1"
        assert r.requester == "alice"
        assert r.reviewers == {"bob", "carol"}
        assert r.state == ReviewState.REQUESTED

    def test_review_id_unique(self):
        rv = DocReview()
        r1 = _make_review(rv)
        r2 = _make_review(rv)
        assert r1.review_id != r2.review_id

    def test_min_approvals_stored(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=3)
        assert r.min_approvals == 3

    def test_timestamps_set(self):
        rv = DocReview()
        r = _make_review(rv, now=42.5)
        assert r.created_at == 42.5
        assert r.updated_at == 42.5

    def test_total_reviews_increments(self):
        rv = DocReview()
        assert rv.total_reviews == 0
        _make_review(rv)
        assert rv.total_reviews == 1
        _make_review(rv)
        assert rv.total_reviews == 2

    def test_empty_reviewer_list(self):
        rv = DocReview()
        r = rv.create_review(
            doc_id="d", requester="alice", reviewers=[],
        )
        assert r.reviewers == set()


class TestAddRemoveReviewer:
    def test_add_reviewer(self):
        rv = DocReview()
        r = _make_review(rv)
        assert rv.add_reviewer(r.review_id, "dave") is True
        assert "dave" in rv.get_review(r.review_id).reviewers

    def test_add_existing_reviewer(self):
        rv = DocReview()
        r = _make_review(rv)
        assert rv.add_reviewer(r.review_id, "bob") is False

    def test_add_to_unknown_review(self):
        rv = DocReview()
        assert rv.add_reviewer("nope", "bob") is False

    def test_remove_reviewer(self):
        rv = DocReview()
        r = _make_review(rv)
        assert rv.remove_reviewer(r.review_id, "bob") is True
        assert "bob" not in rv.get_review(r.review_id).reviewers

    def test_remove_missing_reviewer(self):
        rv = DocReview()
        r = _make_review(rv)
        assert rv.remove_reviewer(r.review_id, "ghost") is False

    def test_cant_add_after_terminal(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=1)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        # Now APPROVED (terminal)
        assert rv.add_reviewer(r.review_id, "dave") is False


class TestSubmitVerdictApprove:
    def test_approve_moves_to_in_progress_then_approved(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=2)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        assert rv.state(r.review_id) == ReviewState.IN_PROGRESS
        rv.submit_verdict(r.review_id, "carol", ReviewVerdict.APPROVE)
        assert rv.state(r.review_id) == ReviewState.APPROVED

    def test_single_approve_with_min_one(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=1)
        assert rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        assert rv.state(r.review_id) == ReviewState.APPROVED

    def test_records_verdict(self):
        rv = DocReview()
        r = _make_review(rv)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE, now=5.0)
        review = rv.get_review(r.review_id)
        assert len(review.verdicts) == 1
        assert review.verdicts[0].submitted_at == 5.0

    def test_updates_updated_at(self):
        rv = DocReview()
        r = _make_review(rv, now=1.0)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE, now=10.0)
        assert rv.get_review(r.review_id).updated_at == 10.0


class TestSubmitVerdictReject:
    def test_reject_sets_state(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=2)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.REJECT)
        assert rv.state(r.review_id) == ReviewState.REJECTED

    def test_reject_with_reason(self):
        rv = DocReview()
        r = _make_review(rv)
        rv.submit_verdict(
            r.review_id, "bob", ReviewVerdict.REJECT, reason="bad",
        )
        review = rv.get_review(r.review_id)
        assert review.verdicts[0].reason == "bad"

    def test_reject_is_terminal(self):
        rv = DocReview()
        r = _make_review(rv)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.REJECT)
        # cannot submit again
        assert rv.submit_verdict(
            r.review_id, "carol", ReviewVerdict.APPROVE,
        ) is False

    def test_reject_overrides_approve(self):
        # If one approves and another rejects, REJECT wins.
        rv = DocReview()
        r = _make_review(rv, min_approvals=2)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        rv.submit_verdict(r.review_id, "carol", ReviewVerdict.REJECT)
        assert rv.state(r.review_id) == ReviewState.REJECTED


class TestSubmitVerdictChanges:
    def test_changes_requested_state(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=2)
        rv.submit_verdict(
            r.review_id, "bob", ReviewVerdict.REQUEST_CHANGES,
        )
        assert rv.state(r.review_id) == ReviewState.CHANGES_REQUESTED

    def test_changes_not_terminal(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=1)
        rv.submit_verdict(
            r.review_id, "bob", ReviewVerdict.REQUEST_CHANGES,
        )
        assert rv.submit_verdict(
            r.review_id, "carol", ReviewVerdict.APPROVE,
        ) is True

    def test_changes_then_approve_moves_to_approved(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=1)
        rv.submit_verdict(
            r.review_id, "bob", ReviewVerdict.REQUEST_CHANGES,
        )
        rv.submit_verdict(r.review_id, "carol", ReviewVerdict.APPROVE)
        assert rv.state(r.review_id) == ReviewState.APPROVED


class TestSubmitVerdictComment:
    def test_comment_does_not_change_state(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=1)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.COMMENT)
        # COMMENT moves state to IN_PROGRESS (first verdict) but no further.
        assert rv.state(r.review_id) == ReviewState.IN_PROGRESS

    def test_comment_does_not_count_for_consensus(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=1)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.COMMENT)
        c = rv.consensus(r.review_id)
        assert c.approve_count == 0
        assert c.reject_count == 0
        assert c.changes_count == 0


class TestUpdateVerdict:
    def test_reviewer_can_resubmit(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=1)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.REQUEST_CHANGES)
        assert rv.state(r.review_id) == ReviewState.CHANGES_REQUESTED
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        assert rv.state(r.review_id) == ReviewState.APPROVED

    def test_latest_verdict_wins_in_consensus(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=2)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.REQUEST_CHANGES)
        c = rv.consensus(r.review_id)
        assert c.approve_count == 0
        assert c.changes_count == 1

    def test_history_preserved(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=2)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.REQUEST_CHANGES)
        review = rv.get_review(r.review_id)
        assert len(review.verdicts) == 2


class TestAddComment:
    def test_add_basic_comment(self):
        rv = DocReview()
        r = _make_review(rv)
        c = rv.add_comment(r.review_id, "bob", "looks good", now=3.0)
        assert c is not None
        assert c.reviewer == "bob"
        assert c.text == "looks good"
        assert c.line_num is None
        assert c.created_at == 3.0

    def test_add_with_line_num(self):
        rv = DocReview()
        r = _make_review(rv)
        c = rv.add_comment(r.review_id, "bob", "typo here", line_num=42)
        assert c.line_num == 42

    def test_comment_id_increments(self):
        rv = DocReview()
        r = _make_review(rv)
        c1 = rv.add_comment(r.review_id, "bob", "a")
        c2 = rv.add_comment(r.review_id, "bob", "b")
        assert c2.comment_id == c1.comment_id + 1

    def test_unknown_review(self):
        rv = DocReview()
        assert rv.add_comment("nope", "bob", "hello") is None

    def test_comment_stored(self):
        rv = DocReview()
        r = _make_review(rv)
        rv.add_comment(r.review_id, "bob", "first")
        rv.add_comment(r.review_id, "carol", "second")
        review = rv.get_review(r.review_id)
        assert len(review.comments) == 2

    def test_cant_comment_after_terminal(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=1)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        assert rv.add_comment(r.review_id, "bob", "post") is None


class TestResolveComment:
    def test_resolve_existing(self):
        rv = DocReview()
        r = _make_review(rv)
        c = rv.add_comment(r.review_id, "bob", "fix this")
        assert rv.resolve_comment(r.review_id, c.comment_id) is True
        review = rv.get_review(r.review_id)
        assert review.comments[0].resolved is True

    def test_resolve_unknown_comment(self):
        rv = DocReview()
        r = _make_review(rv)
        assert rv.resolve_comment(r.review_id, 9999) is False

    def test_resolve_unknown_review(self):
        rv = DocReview()
        assert rv.resolve_comment("nope", 1) is False

    def test_double_resolve_returns_false(self):
        rv = DocReview()
        r = _make_review(rv)
        c = rv.add_comment(r.review_id, "bob", "fix this")
        rv.resolve_comment(r.review_id, c.comment_id)
        assert rv.resolve_comment(r.review_id, c.comment_id) is False


class TestWithdraw:
    def test_withdraw_sets_state(self):
        rv = DocReview()
        r = _make_review(rv)
        assert rv.withdraw(r.review_id, now=99.0) is True
        assert rv.state(r.review_id) == ReviewState.WITHDRAWN

    def test_withdraw_updates_timestamp(self):
        rv = DocReview()
        r = _make_review(rv)
        rv.withdraw(r.review_id, now=99.0)
        assert rv.get_review(r.review_id).updated_at == 99.0

    def test_withdraw_is_terminal(self):
        rv = DocReview()
        r = _make_review(rv)
        rv.withdraw(r.review_id)
        assert rv.submit_verdict(
            r.review_id, "bob", ReviewVerdict.APPROVE,
        ) is False

    def test_withdraw_unknown(self):
        rv = DocReview()
        assert rv.withdraw("nope") is False

    def test_cant_withdraw_after_approved(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=1)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        assert rv.withdraw(r.review_id) is False


class TestReviewsForDoc:
    def test_filters_by_doc(self):
        rv = DocReview()
        a = _make_review(rv, doc_id="doc-a")
        b = _make_review(rv, doc_id="doc-b")
        _make_review(rv, doc_id="doc-a")
        result_a = rv.reviews_for_doc("doc-a")
        assert len(result_a) == 2
        assert all(r.doc_id == "doc-a" for r in result_a)
        result_b = rv.reviews_for_doc("doc-b")
        assert len(result_b) == 1
        assert result_b[0].review_id == b.review_id
        # silence unused
        assert a.doc_id == "doc-a"

    def test_no_match(self):
        rv = DocReview()
        _make_review(rv, doc_id="doc-a")
        assert rv.reviews_for_doc("ghost") == []


class TestReviewsByReviewer:
    def test_filters_by_reviewer(self):
        rv = DocReview()
        _make_review(rv, reviewers=["bob", "carol"])
        _make_review(rv, reviewers=["dave"])
        bob_reviews = rv.reviews_by_reviewer("bob")
        assert len(bob_reviews) == 1

    def test_no_match(self):
        rv = DocReview()
        _make_review(rv)
        assert rv.reviews_by_reviewer("ghost") == []


class TestPendingReviews:
    def test_pending_when_no_verdict(self):
        rv = DocReview()
        r = _make_review(rv)
        pending = rv.pending_reviews("bob")
        assert len(pending) == 1
        assert pending[0].review_id == r.review_id

    def test_not_pending_after_verdict(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=2)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        pending = rv.pending_reviews("bob")
        assert len(pending) == 0
        # carol still pending
        pending_c = rv.pending_reviews("carol")
        assert len(pending_c) == 1

    def test_comment_keeps_pending(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=2)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.COMMENT)
        pending = rv.pending_reviews("bob")
        assert len(pending) == 1
        assert pending[0].review_id == r.review_id

    def test_not_pending_when_terminal(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=1)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        # state is APPROVED. carol should no longer be "pending" since the
        # review itself is terminal.
        assert rv.pending_reviews("carol") == []

    def test_pending_excludes_non_reviewers(self):
        rv = DocReview()
        _make_review(rv)
        assert rv.pending_reviews("ghost") == []


class TestConsensus:
    def test_no_verdicts(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=2)
        c = rv.consensus(r.review_id)
        assert c.approve_count == 0
        assert c.pending_count == 2
        assert c.approved is False

    def test_one_approve_of_two_required(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=2)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        c = rv.consensus(r.review_id)
        assert c.approve_count == 1
        assert c.pending_count == 1
        assert c.approved is False

    def test_meets_min_approvals(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=2)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        rv.submit_verdict(r.review_id, "carol", ReviewVerdict.APPROVE)
        c = rv.consensus(r.review_id)
        assert c.approve_count == 2
        assert c.approved is True

    def test_changes_count(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=2)
        rv.submit_verdict(
            r.review_id, "bob", ReviewVerdict.REQUEST_CHANGES,
        )
        c = rv.consensus(r.review_id)
        assert c.changes_count == 1
        assert c.pending_count == 1

    def test_unknown_review(self):
        rv = DocReview()
        assert rv.consensus("nope") is None


class TestIsConsensusReached:
    def test_reached(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=1)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        assert rv.is_consensus_reached(r.review_id) is True

    def test_not_reached(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=2)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        assert rv.is_consensus_reached(r.review_id) is False

    def test_unknown_review(self):
        rv = DocReview()
        assert rv.is_consensus_reached("nope") is False


class TestState:
    def test_initial_requested(self):
        rv = DocReview()
        r = _make_review(rv)
        assert rv.state(r.review_id) == ReviewState.REQUESTED

    def test_state_unknown(self):
        rv = DocReview()
        assert rv.state("nope") is None

    def test_state_progression(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=2)
        assert rv.state(r.review_id) == ReviewState.REQUESTED
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.COMMENT)
        assert rv.state(r.review_id) == ReviewState.IN_PROGRESS


class TestTotalReviews:
    def test_zero_initially(self):
        assert DocReview().total_reviews == 0

    def test_counts_all(self):
        rv = DocReview()
        for _ in range(5):
            _make_review(rv)
        assert rv.total_reviews == 5


class TestClear:
    def test_clear_empties(self):
        rv = DocReview()
        _make_review(rv)
        _make_review(rv)
        rv.clear()
        assert rv.total_reviews == 0

    def test_clear_resets_comment_counter(self):
        rv = DocReview()
        r1 = _make_review(rv)
        rv.add_comment(r1.review_id, "bob", "first")
        rv.clear()
        r2 = _make_review(rv)
        c = rv.add_comment(r2.review_id, "bob", "after-clear")
        assert c.comment_id == 1

    def test_clear_idempotent(self):
        rv = DocReview()
        rv.clear()
        rv.clear()
        assert rv.total_reviews == 0


class TestEdgeCases:
    def test_unknown_reviewer_cannot_vote(self):
        rv = DocReview()
        r = _make_review(rv)
        assert rv.submit_verdict(
            r.review_id, "ghost", ReviewVerdict.APPROVE,
        ) is False

    def test_unknown_review_submit(self):
        rv = DocReview()
        assert rv.submit_verdict(
            "nope", "bob", ReviewVerdict.APPROVE,
        ) is False

    def test_double_approve_same_reviewer_no_double_count(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=2)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        c = rv.consensus(r.review_id)
        assert c.approve_count == 1

    def test_min_approvals_higher_than_reviewers(self):
        rv = DocReview()
        r = _make_review(rv, reviewers=["bob"], min_approvals=5)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        # Cannot reach 5 with only 1 reviewer
        assert rv.state(r.review_id) == ReviewState.IN_PROGRESS
        assert rv.is_consensus_reached(r.review_id) is False

    def test_get_review_unknown(self):
        rv = DocReview()
        assert rv.get_review("nope") is None

    def test_resubmit_after_approved_blocked(self):
        rv = DocReview()
        r = _make_review(rv, min_approvals=1)
        rv.submit_verdict(r.review_id, "bob", ReviewVerdict.APPROVE)
        # bob tries to change his mind, but APPROVED is terminal
        assert rv.submit_verdict(
            r.review_id, "bob", ReviewVerdict.REQUEST_CHANGES,
        ) is False
        assert rv.state(r.review_id) == ReviewState.APPROVED

    def test_withdrawn_review_returns_none_for_comment(self):
        rv = DocReview()
        r = _make_review(rv)
        rv.withdraw(r.review_id)
        assert rv.add_comment(r.review_id, "bob", "late") is None
