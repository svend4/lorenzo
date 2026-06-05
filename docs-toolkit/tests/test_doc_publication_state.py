"""Tests for E433 docstoolkit.doc_publication_state."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_publication_state import (
    DocPublicationState,
    PublicationRecord,
    PublicationStats,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestPublicationRecord:
    def test_minimal_construction(self):
        r = PublicationRecord(doc_id="d1", state="draft")
        assert r.doc_id == "d1"
        assert r.state == "draft"
        assert r.state_changed_at == 0.0
        assert r.published_at is None
        assert r.scheduled_for is None
        assert r.published_by == ""

    def test_full_construction(self):
        r = PublicationRecord(
            doc_id="d1",
            state="published",
            state_changed_at=10.0,
            published_at=10.0,
            scheduled_for=None,
            published_by="alice",
        )
        assert r.state == "published"
        assert r.published_at == 10.0
        assert r.published_by == "alice"


class TestPublicationStats:
    def test_default_state_counts_is_dict(self):
        s = PublicationStats(total_docs=0)
        assert s.total_docs == 0
        assert s.state_counts == {}
        assert s.scheduled_pending == 0

    def test_independent_default_dicts(self):
        s1 = PublicationStats(total_docs=1)
        s2 = PublicationStats(total_docs=2)
        s1.state_counts["draft"] = 1
        assert s2.state_counts == {}


# ---------------------------------------------------------------------------
# set_state
# ---------------------------------------------------------------------------


class TestSetState:
    def test_create_new_record(self):
        s = DocPublicationState()
        r = s.set_state("d1", "draft", now=100.0)
        assert r.doc_id == "d1"
        assert r.state == "draft"
        assert r.state_changed_at == 100.0
        assert r.published_at is None

    def test_overwrite_existing_record(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=10.0)
        r = s.set_state("d1", "published", by="bob", now=20.0)
        assert r.state == "published"
        assert r.state_changed_at == 20.0
        assert r.published_at == 20.0
        assert r.published_by == "bob"

    def test_invalid_state_raises(self):
        s = DocPublicationState()
        with pytest.raises(ValueError):
            s.set_state("d1", "ufo", now=1.0)

    def test_set_state_published_records_timestamp_and_by(self):
        s = DocPublicationState()
        r = s.set_state("d1", "published", by="alice", now=50.0)
        assert r.published_at == 50.0
        assert r.published_by == "alice"

    def test_set_state_non_publish_with_by(self):
        s = DocPublicationState()
        r = s.set_state("d1", "draft", by="alice", now=1.0)
        assert r.published_by == "alice"
        assert r.published_at is None

    def test_set_state_uses_real_clock_when_now_none(self):
        s = DocPublicationState()
        r = s.set_state("d1", "draft")
        assert r.state_changed_at > 0.0

    def test_set_state_all_valid(self):
        s = DocPublicationState()
        for st in ["draft", "review", "scheduled", "published", "unpublished", "archived"]:
            s.set_state(f"d_{st}", st, now=1.0)
            assert s.state_of(f"d_{st}") == st


# ---------------------------------------------------------------------------
# transition
# ---------------------------------------------------------------------------


class TestTransition:
    def test_unknown_doc_returns_none(self):
        s = DocPublicationState()
        assert s.transition("nope", "review", now=1.0) is None

    def test_invalid_target_state_returns_none(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        assert s.transition("d1", "ufo", now=2.0) is None

    def test_draft_to_review_ok(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        r = s.transition("d1", "review", now=2.0)
        assert r is not None
        assert r.state == "review"
        assert r.state_changed_at == 2.0

    def test_draft_to_scheduled_ok(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        r = s.transition("d1", "scheduled", now=2.0)
        assert r is not None
        assert r.state == "scheduled"

    def test_draft_to_published_ok(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        r = s.transition("d1", "published", by="x", now=5.0)
        assert r is not None
        assert r.state == "published"
        assert r.published_at == 5.0
        assert r.published_by == "x"

    def test_draft_to_unpublished_invalid(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        assert s.transition("d1", "unpublished", now=2.0) is None
        assert s.state_of("d1") == "draft"

    def test_draft_to_archived_invalid(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        assert s.transition("d1", "archived", now=2.0) is None

    def test_review_to_draft_ok(self):
        s = DocPublicationState()
        s.set_state("d1", "review", now=1.0)
        assert s.transition("d1", "draft", now=2.0).state == "draft"

    def test_review_to_scheduled_ok(self):
        s = DocPublicationState()
        s.set_state("d1", "review", now=1.0)
        assert s.transition("d1", "scheduled", now=2.0).state == "scheduled"

    def test_review_to_published_ok(self):
        s = DocPublicationState()
        s.set_state("d1", "review", now=1.0)
        r = s.transition("d1", "published", now=2.0)
        assert r.state == "published"
        assert r.published_at == 2.0

    def test_review_to_archived_invalid(self):
        s = DocPublicationState()
        s.set_state("d1", "review", now=1.0)
        assert s.transition("d1", "archived", now=2.0) is None

    def test_scheduled_to_draft_ok(self):
        s = DocPublicationState()
        s.set_state("d1", "scheduled", now=1.0)
        assert s.transition("d1", "draft", now=2.0).state == "draft"

    def test_scheduled_to_published_ok(self):
        s = DocPublicationState()
        s.set_state("d1", "scheduled", now=1.0)
        assert s.transition("d1", "published", now=2.0).state == "published"

    def test_scheduled_to_unpublished_ok(self):
        s = DocPublicationState()
        s.set_state("d1", "scheduled", now=1.0)
        assert s.transition("d1", "unpublished", now=2.0).state == "unpublished"

    def test_scheduled_to_review_invalid(self):
        s = DocPublicationState()
        s.set_state("d1", "scheduled", now=1.0)
        assert s.transition("d1", "review", now=2.0) is None

    def test_published_to_unpublished_ok(self):
        s = DocPublicationState()
        s.set_state("d1", "published", now=1.0)
        assert s.transition("d1", "unpublished", now=2.0).state == "unpublished"

    def test_published_to_archived_ok(self):
        s = DocPublicationState()
        s.set_state("d1", "published", now=1.0)
        assert s.transition("d1", "archived", now=2.0).state == "archived"

    def test_published_to_draft_invalid(self):
        s = DocPublicationState()
        s.set_state("d1", "published", now=1.0)
        assert s.transition("d1", "draft", now=2.0) is None

    def test_unpublished_to_draft_ok(self):
        s = DocPublicationState()
        s.set_state("d1", "unpublished", now=1.0)
        assert s.transition("d1", "draft", now=2.0).state == "draft"

    def test_unpublished_to_published_ok(self):
        s = DocPublicationState()
        s.set_state("d1", "unpublished", now=1.0)
        r = s.transition("d1", "published", now=2.0)
        assert r.state == "published"
        assert r.published_at == 2.0

    def test_unpublished_to_archived_ok(self):
        s = DocPublicationState()
        s.set_state("d1", "unpublished", now=1.0)
        assert s.transition("d1", "archived", now=2.0).state == "archived"

    def test_archived_terminal(self):
        s = DocPublicationState()
        s.set_state("d1", "archived", now=1.0)
        for target in ["draft", "review", "scheduled", "published", "unpublished"]:
            assert s.transition("d1", target, now=2.0) is None
        assert s.state_of("d1") == "archived"

    def test_transition_records_by(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        r = s.transition("d1", "review", by="alice", now=2.0)
        assert r.published_by == "alice"

    def test_transition_updates_state_changed_at(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        r = s.transition("d1", "review", now=42.0)
        assert r.state_changed_at == 42.0


# ---------------------------------------------------------------------------
# schedule
# ---------------------------------------------------------------------------


class TestSchedule:
    def test_unknown_doc_returns_none(self):
        s = DocPublicationState()
        assert s.schedule("nope", 100.0) is None

    def test_schedule_from_draft(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        r = s.schedule("d1", scheduled_for=100.0, by="alice", now=2.0)
        assert r is not None
        assert r.state == "scheduled"
        assert r.scheduled_for == 100.0
        assert r.state_changed_at == 2.0
        assert r.published_by == "alice"

    def test_schedule_from_review(self):
        s = DocPublicationState()
        s.set_state("d1", "review", now=1.0)
        r = s.schedule("d1", scheduled_for=100.0, now=2.0)
        assert r is not None
        assert r.state == "scheduled"

    def test_schedule_from_published_invalid(self):
        s = DocPublicationState()
        s.set_state("d1", "published", now=1.0)
        assert s.schedule("d1", scheduled_for=100.0, now=2.0) is None

    def test_schedule_from_archived_invalid(self):
        s = DocPublicationState()
        s.set_state("d1", "archived", now=1.0)
        assert s.schedule("d1", scheduled_for=100.0, now=2.0) is None


# ---------------------------------------------------------------------------
# publish / unpublish / archive
# ---------------------------------------------------------------------------


class TestPublishUnpublishArchive:
    def test_publish_unknown(self):
        s = DocPublicationState()
        assert s.publish("nope") is None

    def test_publish_from_draft(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        r = s.publish("d1", by="alice", now=5.0)
        assert r.state == "published"
        assert r.published_at == 5.0
        assert r.published_by == "alice"

    def test_publish_from_archived_invalid(self):
        s = DocPublicationState()
        s.set_state("d1", "archived", now=1.0)
        assert s.publish("d1", now=2.0) is None

    def test_unpublish_unknown(self):
        s = DocPublicationState()
        assert s.unpublish("nope") is None

    def test_unpublish_from_published(self):
        s = DocPublicationState()
        s.set_state("d1", "published", now=1.0)
        r = s.unpublish("d1", by="bob", now=2.0)
        assert r.state == "unpublished"
        assert r.published_by == "bob"

    def test_unpublish_from_draft_invalid(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        assert s.unpublish("d1", now=2.0) is None

    def test_unpublish_from_scheduled(self):
        s = DocPublicationState()
        s.set_state("d1", "scheduled", now=1.0)
        r = s.unpublish("d1", now=2.0)
        assert r.state == "unpublished"

    def test_archive_unknown(self):
        s = DocPublicationState()
        assert s.archive("nope") is None

    def test_archive_from_published(self):
        s = DocPublicationState()
        s.set_state("d1", "published", now=1.0)
        r = s.archive("d1", by="cab", now=3.0)
        assert r.state == "archived"
        assert r.published_by == "cab"

    def test_archive_from_unpublished(self):
        s = DocPublicationState()
        s.set_state("d1", "unpublished", now=1.0)
        assert s.archive("d1", now=2.0).state == "archived"

    def test_archive_from_draft_invalid(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        assert s.archive("d1", now=2.0) is None


# ---------------------------------------------------------------------------
# process_scheduled
# ---------------------------------------------------------------------------


class TestProcessScheduled:
    def test_empty_returns_empty(self):
        s = DocPublicationState()
        assert s.process_scheduled(now=100.0) == []

    def test_publishes_due(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        s.schedule("d1", scheduled_for=50.0, now=2.0)
        s.set_state("d2", "draft", now=1.0)
        s.schedule("d2", scheduled_for=200.0, now=2.0)
        out = s.process_scheduled(now=100.0)
        assert out == ["d1"]
        assert s.state_of("d1") == "published"
        assert s.state_of("d2") == "scheduled"
        assert s.get_record("d1").published_at == 100.0

    def test_only_scheduled_state_processed(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        # d1 is draft, not scheduled — should be ignored even if it had no scheduled_for
        out = s.process_scheduled(now=100.0)
        assert out == []
        assert s.state_of("d1") == "draft"

    def test_scheduled_without_scheduled_for_ignored(self):
        s = DocPublicationState()
        # set_state bypasses schedule(), so scheduled_for stays None
        s.set_state("d1", "scheduled", now=1.0)
        out = s.process_scheduled(now=100.0)
        assert out == []
        assert s.state_of("d1") == "scheduled"

    def test_returns_sorted(self):
        s = DocPublicationState()
        for d in ["c", "a", "b"]:
            s.set_state(d, "draft", now=1.0)
            s.schedule(d, scheduled_for=10.0, now=2.0)
        out = s.process_scheduled(now=100.0)
        assert out == ["a", "b", "c"]

    def test_published_at_set_to_now(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        s.schedule("d1", scheduled_for=50.0, now=2.0)
        s.process_scheduled(now=77.0)
        assert s.get_record("d1").published_at == 77.0
        assert s.get_record("d1").state_changed_at == 77.0


# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------


class TestQueries:
    def test_get_record_unknown(self):
        s = DocPublicationState()
        assert s.get_record("nope") is None

    def test_get_record(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        r = s.get_record("d1")
        assert r is not None
        assert r.doc_id == "d1"

    def test_state_of_unknown(self):
        s = DocPublicationState()
        assert s.state_of("nope") is None

    def test_state_of(self):
        s = DocPublicationState()
        s.set_state("d1", "review", now=1.0)
        assert s.state_of("d1") == "review"

    def test_docs_in_state_empty(self):
        s = DocPublicationState()
        assert s.docs_in_state("draft") == []

    def test_docs_in_state_sorted(self):
        s = DocPublicationState()
        for d in ["c", "a", "b"]:
            s.set_state(d, "draft", now=1.0)
        s.set_state("z", "published", now=1.0)
        assert s.docs_in_state("draft") == ["a", "b", "c"]
        assert s.docs_in_state("published") == ["z"]

    def test_published_docs(self):
        s = DocPublicationState()
        s.set_state("d2", "published", now=1.0)
        s.set_state("d1", "published", now=1.0)
        s.set_state("d3", "draft", now=1.0)
        assert s.published_docs() == ["d1", "d2"]

    def test_scheduled_docs_sorted_by_scheduled_for(self):
        s = DocPublicationState()
        s.set_state("late", "draft", now=1.0)
        s.schedule("late", scheduled_for=200.0, now=2.0)
        s.set_state("early", "draft", now=1.0)
        s.schedule("early", scheduled_for=50.0, now=2.0)
        s.set_state("mid", "draft", now=1.0)
        s.schedule("mid", scheduled_for=100.0, now=2.0)
        ids = [r.doc_id for r in s.scheduled_docs()]
        assert ids == ["early", "mid", "late"]

    def test_scheduled_docs_none_scheduled_for_sorted_last(self):
        s = DocPublicationState()
        s.set_state("a", "scheduled", now=1.0)  # no scheduled_for
        s.set_state("b", "draft", now=1.0)
        s.schedule("b", scheduled_for=10.0, now=2.0)
        ids = [r.doc_id for r in s.scheduled_docs()]
        assert ids == ["b", "a"]


# ---------------------------------------------------------------------------
# delete / clear_all
# ---------------------------------------------------------------------------


class TestDeleteClear:
    def test_delete_unknown_returns_false(self):
        s = DocPublicationState()
        assert s.delete("nope") is False

    def test_delete_existing(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        assert s.delete("d1") is True
        assert s.get_record("d1") is None

    def test_clear_all_empty(self):
        s = DocPublicationState()
        assert s.clear_all() == 0

    def test_clear_all_counts(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        s.set_state("d2", "draft", now=1.0)
        assert s.clear_all() == 2
        assert s.get_record("d1") is None


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self):
        s = DocPublicationState()
        st = s.stats(now=100.0)
        assert st.total_docs == 0
        # All valid states present with count 0
        assert set(st.state_counts.keys()) == {
            "draft", "review", "scheduled", "published", "unpublished", "archived"
        }
        assert all(v == 0 for v in st.state_counts.values())
        assert st.scheduled_pending == 0

    def test_state_counts(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        s.set_state("d2", "draft", now=1.0)
        s.set_state("d3", "published", now=1.0)
        st = s.stats(now=100.0)
        assert st.total_docs == 3
        assert st.state_counts["draft"] == 2
        assert st.state_counts["published"] == 1
        assert st.state_counts["archived"] == 0

    def test_scheduled_pending(self):
        s = DocPublicationState()
        s.set_state("future", "draft", now=1.0)
        s.schedule("future", scheduled_for=200.0, now=2.0)
        s.set_state("past", "draft", now=1.0)
        s.schedule("past", scheduled_for=50.0, now=2.0)
        st = s.stats(now=100.0)
        # only 'future' is still pending (scheduled_for > now)
        assert st.scheduled_pending == 1
        assert st.state_counts["scheduled"] == 2

    def test_stats_no_now_uses_real_clock(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", now=1.0)
        st = s.stats()
        assert st.total_docs == 1


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_set_state(self):
        s = DocPublicationState()
        N = 50
        T = 8

        def worker(start: int):
            for i in range(N):
                s.set_state(f"d_{start}_{i}", "draft", now=float(i))

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(T)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert s.stats().total_docs == N * T

    def test_concurrent_transitions_no_corruption(self):
        s = DocPublicationState()
        for i in range(20):
            s.set_state(f"d{i}", "draft", now=0.0)

        def worker():
            for i in range(20):
                s.transition(f"d{i}", "published", now=1.0)

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # All should be published exactly once (one of the threads wins)
        for i in range(20):
            assert s.state_of(f"d{i}") == "published"

    def test_concurrent_process_scheduled(self):
        s = DocPublicationState()
        for i in range(30):
            s.set_state(f"d{i}", "draft", now=0.0)
            s.schedule(f"d{i}", scheduled_for=10.0, now=1.0)

        results: list = []

        def worker():
            results.append(s.process_scheduled(now=100.0))

        threads = [threading.Thread(target=worker) for _ in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Each doc must be published exactly once across all threads
        flat = [d for lst in results for d in lst]
        assert sorted(flat) == [f"d{i}" for i in sorted(range(30), key=str)]
        for i in range(30):
            assert s.state_of(f"d{i}") == "published"


# ---------------------------------------------------------------------------
# End-to-end scenarios
# ---------------------------------------------------------------------------


class TestEndToEnd:
    def test_full_lifecycle(self):
        s = DocPublicationState()
        s.set_state("d1", "draft", by="alice", now=1.0)
        assert s.state_of("d1") == "draft"

        s.transition("d1", "review", by="bob", now=2.0)
        assert s.state_of("d1") == "review"

        s.schedule("d1", scheduled_for=10.0, by="bob", now=3.0)
        assert s.state_of("d1") == "scheduled"
        assert s.get_record("d1").scheduled_for == 10.0

        out = s.process_scheduled(now=15.0)
        assert out == ["d1"]
        assert s.state_of("d1") == "published"
        assert s.get_record("d1").published_at == 15.0

        s.unpublish("d1", by="carol", now=20.0)
        assert s.state_of("d1") == "unpublished"

        s.archive("d1", by="carol", now=25.0)
        assert s.state_of("d1") == "archived"

        # archived is terminal — nothing works further
        assert s.publish("d1", now=26.0) is None
        assert s.transition("d1", "draft", now=27.0) is None

    def test_initial_set_required(self):
        # transition on a fresh manager returns None — must call set_state first
        s = DocPublicationState()
        assert s.transition("d1", "draft", now=1.0) is None
        s.set_state("d1", "draft", now=1.0)
        assert s.transition("d1", "review", now=2.0) is not None
