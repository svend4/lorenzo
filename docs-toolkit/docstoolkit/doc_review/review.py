"""Peer review tracking for documents (E200).

Implements review state, verdicts, comments, and consensus computation. The
:class:`DocReview` registry is thread-safe via a single :class:`threading.Lock`.
"""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ReviewState(Enum):
    """Lifecycle state of a peer review."""

    REQUESTED = "requested"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    CHANGES_REQUESTED = "changes_requested"
    WITHDRAWN = "withdrawn"


class ReviewVerdict(Enum):
    """Verdict that a single reviewer can submit."""

    APPROVE = "approve"
    REQUEST_CHANGES = "request_changes"
    REJECT = "reject"
    COMMENT = "comment"


@dataclass
class Comment:
    """A single comment left by a reviewer."""

    comment_id: int
    reviewer: str
    text: str
    created_at: float
    line_num: Optional[int] = None
    resolved: bool = False


@dataclass
class ReviewVerdictRecord:
    """An individual verdict submission by a reviewer."""

    reviewer: str
    verdict: ReviewVerdict
    submitted_at: float
    reason: Optional[str] = None


@dataclass
class Review:
    """A peer review on a document."""

    review_id: str
    doc_id: str
    requester: str
    reviewers: set
    state: ReviewState
    verdicts: list
    comments: list
    created_at: float
    updated_at: float
    min_approvals: int = 1


@dataclass
class ConsensusResult:
    """Aggregated counts of verdicts for a review."""

    approved: bool
    approve_count: int
    reject_count: int
    changes_count: int
    pending_count: int


# Terminal states that should not be updated further.
_TERMINAL_STATES = frozenset({
    ReviewState.APPROVED,
    ReviewState.REJECTED,
    ReviewState.WITHDRAWN,
})


class DocReview:
    """Thread-safe registry of peer reviews."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._reviews: dict = {}
        self._comment_counter: int = 0

    # ------------------------------------------------------------------
    # Creation / membership
    # ------------------------------------------------------------------
    def create_review(
        self,
        doc_id: str,
        requester: str,
        reviewers,
        min_approvals: int = 1,
        now: float = 0.0,
    ) -> Review:
        """Create a new review request for ``doc_id``."""
        review_id = uuid.uuid4().hex
        review = Review(
            review_id=review_id,
            doc_id=doc_id,
            requester=requester,
            reviewers=set(reviewers),
            state=ReviewState.REQUESTED,
            verdicts=[],
            comments=[],
            created_at=now,
            updated_at=now,
            min_approvals=min_approvals,
        )
        with self._lock:
            self._reviews[review_id] = review
        return review

    def add_reviewer(self, review_id: str, reviewer: str) -> bool:
        with self._lock:
            review = self._reviews.get(review_id)
            if review is None or review.state in _TERMINAL_STATES:
                return False
            if reviewer in review.reviewers:
                return False
            review.reviewers.add(reviewer)
            return True

    def remove_reviewer(self, review_id: str, reviewer: str) -> bool:
        with self._lock:
            review = self._reviews.get(review_id)
            if review is None or review.state in _TERMINAL_STATES:
                return False
            if reviewer not in review.reviewers:
                return False
            review.reviewers.discard(reviewer)
            return True

    # ------------------------------------------------------------------
    # Verdicts
    # ------------------------------------------------------------------
    def submit_verdict(
        self,
        review_id: str,
        reviewer: str,
        verdict: ReviewVerdict,
        reason: Optional[str] = None,
        now: float = 0.0,
    ) -> bool:
        with self._lock:
            review = self._reviews.get(review_id)
            if review is None or review.state in _TERMINAL_STATES:
                return False
            if reviewer not in review.reviewers:
                return False
            record = ReviewVerdictRecord(
                reviewer=reviewer,
                verdict=verdict,
                submitted_at=now,
                reason=reason,
            )
            review.verdicts.append(record)
            review.updated_at = now
            # Move from REQUESTED to IN_PROGRESS on first non-COMMENT submission
            # (the spec says: REQUESTED -> IN_PROGRESS on first verdict submission)
            if review.state == ReviewState.REQUESTED:
                review.state = ReviewState.IN_PROGRESS
            # Recompute state from latest verdicts per reviewer.
            self._recompute_state(review)
            return True

    # ------------------------------------------------------------------
    # Comments
    # ------------------------------------------------------------------
    def add_comment(
        self,
        review_id: str,
        reviewer: str,
        text: str,
        line_num: Optional[int] = None,
        now: float = 0.0,
    ) -> Optional[Comment]:
        with self._lock:
            review = self._reviews.get(review_id)
            if review is None or review.state in _TERMINAL_STATES:
                return None
            self._comment_counter += 1
            comment = Comment(
                comment_id=self._comment_counter,
                reviewer=reviewer,
                text=text,
                created_at=now,
                line_num=line_num,
                resolved=False,
            )
            review.comments.append(comment)
            review.updated_at = now
            return comment

    def resolve_comment(self, review_id: str, comment_id: int) -> bool:
        with self._lock:
            review = self._reviews.get(review_id)
            if review is None:
                return False
            for comment in review.comments:
                if comment.comment_id == comment_id:
                    if comment.resolved:
                        return False
                    comment.resolved = True
                    return True
            return False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------
    def withdraw(self, review_id: str, now: float = 0.0) -> bool:
        with self._lock:
            review = self._reviews.get(review_id)
            if review is None or review.state in _TERMINAL_STATES:
                return False
            review.state = ReviewState.WITHDRAWN
            review.updated_at = now
            return True

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def get_review(self, review_id: str) -> Optional[Review]:
        with self._lock:
            return self._reviews.get(review_id)

    def reviews_for_doc(self, doc_id: str) -> list:
        with self._lock:
            return [r for r in self._reviews.values() if r.doc_id == doc_id]

    def reviews_by_reviewer(self, reviewer: str) -> list:
        with self._lock:
            return [r for r in self._reviews.values() if reviewer in r.reviewers]

    def pending_reviews(self, reviewer: str) -> list:
        with self._lock:
            active = {ReviewState.REQUESTED, ReviewState.IN_PROGRESS}
            result = []
            for review in self._reviews.values():
                if review.state not in active:
                    continue
                if reviewer not in review.reviewers:
                    continue
                latest = self._latest_verdicts(review)
                if reviewer in latest:
                    # COMMENT verdict doesn't count as a "vote" for pending.
                    if latest[reviewer] == ReviewVerdict.COMMENT:
                        result.append(review)
                    continue
                result.append(review)
            return result

    def consensus(self, review_id: str) -> Optional[ConsensusResult]:
        with self._lock:
            review = self._reviews.get(review_id)
            if review is None:
                return None
            return self._compute_consensus(review)

    def is_consensus_reached(self, review_id: str) -> bool:
        with self._lock:
            review = self._reviews.get(review_id)
            if review is None:
                return False
            consensus = self._compute_consensus(review)
            return consensus.approve_count >= review.min_approvals

    def state(self, review_id: str) -> Optional[ReviewState]:
        with self._lock:
            review = self._reviews.get(review_id)
            if review is None:
                return None
            return review.state

    @property
    def total_reviews(self) -> int:
        with self._lock:
            return len(self._reviews)

    def clear(self) -> None:
        with self._lock:
            self._reviews.clear()
            self._comment_counter = 0

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _latest_verdicts(review: Review) -> dict:
        """Return the latest verdict per reviewer (insertion-order wins)."""
        latest: dict = {}
        for record in review.verdicts:
            latest[record.reviewer] = record.verdict
        return latest

    def _compute_consensus(self, review: Review) -> ConsensusResult:
        latest = self._latest_verdicts(review)
        approve_count = 0
        reject_count = 0
        changes_count = 0
        voted = set()
        for reviewer, verdict in latest.items():
            if verdict == ReviewVerdict.APPROVE:
                approve_count += 1
                voted.add(reviewer)
            elif verdict == ReviewVerdict.REJECT:
                reject_count += 1
                voted.add(reviewer)
            elif verdict == ReviewVerdict.REQUEST_CHANGES:
                changes_count += 1
                voted.add(reviewer)
            # COMMENT does not count as a vote.
        pending_count = len([r for r in review.reviewers if r not in voted])
        approved = approve_count >= review.min_approvals
        return ConsensusResult(
            approved=approved,
            approve_count=approve_count,
            reject_count=reject_count,
            changes_count=changes_count,
            pending_count=pending_count,
        )

    def _recompute_state(self, review: Review) -> None:
        """Recompute review.state from latest verdicts per reviewer.

        Priority: REJECT > APPROVED (>= min_approvals) > CHANGES_REQUESTED >
        IN_PROGRESS. Terminal states are not changed.
        """
        if review.state in _TERMINAL_STATES:
            return
        consensus = self._compute_consensus(review)
        if consensus.reject_count > 0:
            review.state = ReviewState.REJECTED
            return
        if consensus.approve_count >= review.min_approvals:
            review.state = ReviewState.APPROVED
            return
        if consensus.changes_count > 0:
            review.state = ReviewState.CHANGES_REQUESTED
            return
        # Some verdict was submitted (we already moved to IN_PROGRESS above);
        # leave IN_PROGRESS as-is, or REQUESTED if no verdicts at all.
        if not review.verdicts:
            review.state = ReviewState.REQUESTED
        else:
            review.state = ReviewState.IN_PROGRESS
