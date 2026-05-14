"""Tests for docstoolkit.doc_status_tracker (E294).

Coverage areas
--------------
* set_status   — initial assignment, transitions, allowed_statuses validation
* get_status   — return value shape, unknown doc
* current_status — convenience accessor
* history      — ordering, limit, empty, transition_id sequence
* docs_with_status — correct filter and sort
* transition_count — accumulation, unknown doc
* bulk_set     — count returned, all docs updated, shared timestamp
* delete_doc   — removal, idempotent False return
* stats        — counts accuracy after mutations
* properties   — total_docs, total_transitions
* thread safety — concurrent writers produce no duplicate transition_ids
"""

from __future__ import annotations

import threading
import time
from typing import Optional

import pytest

from docstoolkit.doc_status_tracker import (
    DocStatus,
    DocStatusTracker,
    StatusStats,
    StatusTransition,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

DEFAULT_STATUSES = ["draft", "review", "published", "archived"]


def make_tracker(allowed: Optional[list] = None) -> DocStatusTracker:
    return DocStatusTracker(allowed_statuses=allowed)


# ---------------------------------------------------------------------------
# set_status — initial assignment
# ---------------------------------------------------------------------------


class TestSetStatusInitial:
    def test_returns_status_transition_instance(self):
        t = make_tracker()
        result = t.set_status("doc1", "draft", changed_by="alice")
        assert isinstance(result, StatusTransition)

    def test_from_status_is_none_on_first_set(self):
        t = make_tracker()
        tr = t.set_status("doc1", "draft", changed_by="alice")
        assert tr.from_status is None

    def test_to_status_matches_argument(self):
        t = make_tracker()
        tr = t.set_status("doc1", "draft")
        assert tr.to_status == "draft"

    def test_doc_id_stored_in_transition(self):
        t = make_tracker()
        tr = t.set_status("doc42", "draft")
        assert tr.doc_id == "doc42"

    def test_changed_by_stored(self):
        t = make_tracker()
        tr = t.set_status("doc1", "draft", changed_by="bob")
        assert tr.changed_by == "bob"

    def test_reason_stored(self):
        t = make_tracker()
        tr = t.set_status("doc1", "draft", reason="initial create")
        assert tr.reason == "initial create"

    def test_custom_timestamp_used(self):
        t = make_tracker()
        ts = 1_000_000.0
        tr = t.set_status("doc1", "draft", now=ts)
        assert tr.timestamp == ts

    def test_auto_timestamp_is_recent(self):
        t = make_tracker()
        before = time.time()
        tr = t.set_status("doc1", "draft")
        after = time.time()
        assert before <= tr.timestamp <= after

    def test_transition_id_starts_at_one(self):
        t = make_tracker()
        tr = t.set_status("doc1", "draft")
        assert tr.transition_id == 1

    def test_transition_ids_increment(self):
        t = make_tracker()
        tr1 = t.set_status("doc1", "draft")
        tr2 = t.set_status("doc2", "draft")
        assert tr2.transition_id == tr1.transition_id + 1


# ---------------------------------------------------------------------------
# set_status — transitions
# ---------------------------------------------------------------------------


class TestSetStatusTransition:
    def test_from_status_reflects_previous(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        tr2 = t.set_status("doc1", "review")
        assert tr2.from_status == "draft"

    def test_multiple_transitions_chain(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        t.set_status("doc1", "review")
        tr3 = t.set_status("doc1", "published")
        assert tr3.from_status == "review"

    def test_same_status_retransition_allowed(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        tr = t.set_status("doc1", "draft")
        assert tr.from_status == "draft"
        assert tr.to_status == "draft"

    def test_current_status_updated_after_transition(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        t.set_status("doc1", "published")
        assert t.current_status("doc1") == "published"


# ---------------------------------------------------------------------------
# set_status — allowed_statuses validation
# ---------------------------------------------------------------------------


class TestAllowedStatuses:
    def test_valid_status_accepted(self):
        t = make_tracker(DEFAULT_STATUSES)
        tr = t.set_status("doc1", "draft")
        assert tr.to_status == "draft"

    def test_invalid_status_raises_value_error(self):
        t = make_tracker(DEFAULT_STATUSES)
        with pytest.raises(ValueError):
            t.set_status("doc1", "unknown_status")

    def test_error_message_includes_bad_status(self):
        t = make_tracker(DEFAULT_STATUSES)
        with pytest.raises(ValueError, match="unknown_status"):
            t.set_status("doc1", "unknown_status")

    def test_no_allowed_statuses_accepts_anything(self):
        t = make_tracker()
        tr = t.set_status("doc1", "whatever")
        assert tr.to_status == "whatever"

    def test_transition_after_invalid_leaves_state_unchanged(self):
        t = make_tracker(DEFAULT_STATUSES)
        t.set_status("doc1", "draft")
        with pytest.raises(ValueError):
            t.set_status("doc1", "bad")
        # doc1 should still be in draft
        assert t.current_status("doc1") == "draft"

    def test_bulk_set_raises_for_invalid_status(self):
        t = make_tracker(DEFAULT_STATUSES)
        with pytest.raises(ValueError):
            t.bulk_set(["doc1", "doc2"], "invalid")


# ---------------------------------------------------------------------------
# get_status
# ---------------------------------------------------------------------------


class TestGetStatus:
    def test_returns_none_for_unknown_doc(self):
        t = make_tracker()
        assert t.get_status("nonexistent") is None

    def test_returns_doc_status_instance(self):
        t = make_tracker()
        t.set_status("doc1", "draft", changed_by="alice", now=500.0)
        result = t.get_status("doc1")
        assert isinstance(result, DocStatus)

    def test_doc_status_fields(self):
        t = make_tracker()
        t.set_status("doc1", "draft", changed_by="alice", now=500.0)
        s = t.get_status("doc1")
        assert s.doc_id == "doc1"
        assert s.current_status == "draft"
        assert s.changed_by == "alice"
        assert s.last_changed_at == 500.0
        assert s.transition_count == 1

    def test_transition_count_reflects_multiple_changes(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        t.set_status("doc1", "review")
        t.set_status("doc1", "published")
        s = t.get_status("doc1")
        assert s.transition_count == 3


# ---------------------------------------------------------------------------
# current_status
# ---------------------------------------------------------------------------


class TestCurrentStatus:
    def test_returns_none_for_unknown(self):
        t = make_tracker()
        assert t.current_status("ghost") is None

    def test_returns_status_string(self):
        t = make_tracker()
        t.set_status("doc1", "review")
        assert t.current_status("doc1") == "review"

    def test_reflects_latest_status(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        t.set_status("doc1", "archived")
        assert t.current_status("doc1") == "archived"


# ---------------------------------------------------------------------------
# history
# ---------------------------------------------------------------------------


class TestHistory:
    def test_returns_empty_for_unknown_doc(self):
        t = make_tracker()
        assert t.history("nonexistent") == []

    def test_single_entry_after_first_set(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        h = t.history("doc1")
        assert len(h) == 1

    def test_newest_first_ordering(self):
        t = make_tracker()
        t.set_status("doc1", "draft", now=1.0)
        t.set_status("doc1", "review", now=2.0)
        t.set_status("doc1", "published", now=3.0)
        h = t.history("doc1")
        assert h[0].to_status == "published"
        assert h[1].to_status == "review"
        assert h[2].to_status == "draft"

    def test_limit_respected(self):
        t = make_tracker()
        for i in range(5):
            t.set_status("doc1", f"s{i}", now=float(i))
        h = t.history("doc1", limit=2)
        assert len(h) == 2
        # Should be the two most recent
        assert h[0].to_status == "s4"
        assert h[1].to_status == "s3"

    def test_limit_larger_than_history_returns_all(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        h = t.history("doc1", limit=100)
        assert len(h) == 1

    def test_history_items_are_status_transition_instances(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        h = t.history("doc1")
        assert all(isinstance(item, StatusTransition) for item in h)


# ---------------------------------------------------------------------------
# docs_with_status
# ---------------------------------------------------------------------------


class TestDocsWithStatus:
    def test_returns_empty_when_no_docs(self):
        t = make_tracker()
        assert t.docs_with_status("draft") == []

    def test_returns_matching_doc(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        assert t.docs_with_status("draft") == ["doc1"]

    def test_excludes_docs_with_different_status(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        t.set_status("doc2", "review")
        assert "doc2" not in t.docs_with_status("draft")

    def test_result_is_sorted(self):
        t = make_tracker()
        t.set_status("z_doc", "draft")
        t.set_status("a_doc", "draft")
        t.set_status("m_doc", "draft")
        assert t.docs_with_status("draft") == ["a_doc", "m_doc", "z_doc"]

    def test_doc_moved_out_of_status(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        t.set_status("doc1", "published")
        assert t.docs_with_status("draft") == []
        assert "doc1" in t.docs_with_status("published")


# ---------------------------------------------------------------------------
# transition_count
# ---------------------------------------------------------------------------


class TestTransitionCount:
    def test_zero_for_unknown_doc(self):
        t = make_tracker()
        assert t.transition_count("ghost") == 0

    def test_one_after_initial_set(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        assert t.transition_count("doc1") == 1

    def test_increments_with_each_change(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        t.set_status("doc1", "review")
        t.set_status("doc1", "published")
        assert t.transition_count("doc1") == 3


# ---------------------------------------------------------------------------
# bulk_set
# ---------------------------------------------------------------------------


class TestBulkSet:
    def test_returns_count_of_updated_docs(self):
        t = make_tracker()
        n = t.bulk_set(["doc1", "doc2", "doc3"], "draft")
        assert n == 3

    def test_all_docs_have_new_status(self):
        t = make_tracker()
        t.bulk_set(["doc1", "doc2"], "published")
        assert t.current_status("doc1") == "published"
        assert t.current_status("doc2") == "published"

    def test_empty_list_returns_zero(self):
        t = make_tracker()
        assert t.bulk_set([], "draft") == 0

    def test_bulk_uses_same_timestamp(self):
        t = make_tracker()
        ts = 9_999.0
        t.bulk_set(["doc1", "doc2"], "draft", now=ts)
        assert t.get_status("doc1").last_changed_at == ts
        assert t.get_status("doc2").last_changed_at == ts

    def test_bulk_set_over_existing_docs(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        t.set_status("doc2", "review")
        t.bulk_set(["doc1", "doc2"], "archived")
        assert t.docs_with_status("archived") == ["doc1", "doc2"]


# ---------------------------------------------------------------------------
# delete_doc
# ---------------------------------------------------------------------------


class TestDeleteDoc:
    def test_returns_true_when_doc_existed(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        assert t.delete_doc("doc1") is True

    def test_returns_false_for_unknown_doc(self):
        t = make_tracker()
        assert t.delete_doc("ghost") is False

    def test_doc_no_longer_tracked_after_delete(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        t.delete_doc("doc1")
        assert t.get_status("doc1") is None
        assert t.current_status("doc1") is None
        assert t.history("doc1") == []

    def test_delete_reduces_total_docs(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        t.set_status("doc2", "draft")
        t.delete_doc("doc1")
        assert t.total_docs == 1

    def test_delete_reduces_transition_count_in_stats(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        t.set_status("doc1", "published")
        t.delete_doc("doc1")
        assert t.stats().total_transitions == 0


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_returns_status_stats_instance(self):
        t = make_tracker()
        assert isinstance(t.stats(), StatusStats)

    def test_total_docs_zero_initially(self):
        t = make_tracker()
        assert t.stats().total_docs == 0

    def test_total_transitions_zero_initially(self):
        t = make_tracker()
        assert t.stats().total_transitions == 0

    def test_status_counts_reflect_current_statuses(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        t.set_status("doc2", "draft")
        t.set_status("doc3", "published")
        s = t.stats()
        assert s.status_counts.get("draft") == 2
        assert s.status_counts.get("published") == 1

    def test_total_transitions_accumulates(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        t.set_status("doc1", "review")
        t.set_status("doc2", "published")
        assert t.stats().total_transitions == 3

    def test_status_counts_updated_after_transition(self):
        t = make_tracker()
        t.set_status("doc1", "draft")
        t.set_status("doc1", "review")
        s = t.stats()
        assert s.status_counts.get("draft", 0) == 0
        assert s.status_counts.get("review") == 1


# ---------------------------------------------------------------------------
# Properties
# ---------------------------------------------------------------------------


class TestProperties:
    def test_total_docs_increments(self):
        t = make_tracker()
        assert t.total_docs == 0
        t.set_status("doc1", "draft")
        assert t.total_docs == 1
        t.set_status("doc2", "draft")
        assert t.total_docs == 2

    def test_total_transitions_increments(self):
        t = make_tracker()
        assert t.total_transitions == 0
        t.set_status("doc1", "draft")
        assert t.total_transitions == 1
        t.set_status("doc1", "review")
        assert t.total_transitions == 2


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_set_status_no_duplicate_ids(self):
        """All transition IDs produced under concurrency must be unique."""
        t = make_tracker()
        results: list = []
        lock = threading.Lock()

        def worker(doc_id: str, status: str) -> None:
            tr = t.set_status(doc_id, status)
            with lock:
                results.append(tr.transition_id)

        threads = [
            threading.Thread(target=worker, args=(f"doc{i}", "draft"))
            for i in range(50)
        ]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert len(results) == len(set(results)), "Duplicate transition IDs detected"

    def test_concurrent_bulk_set_consistent_total(self):
        """Total docs after concurrent bulk_set matches expected count."""
        t = make_tracker()
        doc_groups = [
            [f"group{g}_doc{i}" for i in range(10)] for g in range(5)
        ]

        def bulk_worker(docs: list) -> None:
            t.bulk_set(docs, "draft")

        threads = [
            threading.Thread(target=bulk_worker, args=(group,))
            for group in doc_groups
        ]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert t.total_docs == 50
