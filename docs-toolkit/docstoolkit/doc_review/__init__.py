"""Document peer review module for docs-toolkit (E200).

Provides peer review tracking for documents: review requests, approve/reject
verdicts, threaded comments, and consensus computation. Stdlib-only.

Quick start::

    from docstoolkit.doc_review import (
        DocReview, ReviewVerdict, ReviewState,
    )

    rv = DocReview()
    review = rv.create_review(
        doc_id="doc-1",
        requester="alice",
        reviewers=["bob", "carol"],
        min_approvals=2,
    )
    rv.submit_verdict(review.review_id, "bob", ReviewVerdict.APPROVE)
    rv.submit_verdict(review.review_id, "carol", ReviewVerdict.APPROVE)
    assert rv.state(review.review_id) == ReviewState.APPROVED
"""
from docstoolkit.doc_review.review import (
    ReviewState,
    ReviewVerdict,
    Comment,
    ReviewVerdictRecord,
    Review,
    ConsensusResult,
    DocReview,
)

__all__ = [
    "ReviewState",
    "ReviewVerdict",
    "Comment",
    "ReviewVerdictRecord",
    "Review",
    "ConsensusResult",
    "DocReview",
]
