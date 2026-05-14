"""Tests for docstoolkit.doc_feedback_store (E289)."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_feedback_store import (
    DocFeedbackStore,
    DocSummary,
    FeedbackItem,
    FeedbackStats,
)


# ---------------------------------------------------------------------------
# Dataclass construction
# ---------------------------------------------------------------------------
class TestFeedbackItemConstruction:
    def test_all_fields(self):
        item = FeedbackItem(
            feedback_id=1,
            doc_id="d1",
            user_id="u1",
            feedback_type="rating",
            value=5,
            timestamp=100.0,
        )
        assert item.feedback_id == 1
        assert item.doc_id == "d1"
        assert item.user_id == "u1"
        assert item.feedback_type == "rating"
        assert item.value == 5
        assert item.timestamp == 100.0

    def test_value_can_be_string(self):
        item = FeedbackItem(1, "d1", "u1", "comment", "Great doc!", 0.0)
        assert item.value == "Great doc!"

    def test_value_can_be_none(self):
        item = FeedbackItem(1, "d1", "u1", "reaction", None, 0.0)
        assert item.value is None


class TestDocSummaryConstruction:
    def test_all_fields(self):
        s = DocSummary(
            doc_id="d1",
            total_feedback=5,
            avg_rating=4.2,
            reaction_counts={"thumbs_up": 3},
            comment_count=2,
        )
        assert s.doc_id == "d1"
        assert s.total_feedback == 5
        assert s.avg_rating == pytest.approx(4.2)
        assert s.reaction_counts == {"thumbs_up": 3}
        assert s.comment_count == 2

    def test_avg_rating_can_be_none(self):
        s = DocSummary("d1", 0, None, {}, 0)
        assert s.avg_rating is None


class TestFeedbackStatsConstruction:
    def test_all_fields(self):
        fs = FeedbackStats(
            total_items=10,
            total_docs=3,
            total_users=2,
            type_counts={"rating": 6, "comment": 4},
        )
        assert fs.total_items == 10
        assert fs.total_docs == 3
        assert fs.total_users == 2
        assert fs.type_counts["rating"] == 6


# ---------------------------------------------------------------------------
# add()
# ---------------------------------------------------------------------------
class TestAdd:
    def test_returns_feedback_item(self):
        store = DocFeedbackStore()
        item = store.add("d1", "u1", "rating", 5)
        assert isinstance(item, FeedbackItem)

    def test_feedback_id_starts_at_1(self):
        store = DocFeedbackStore()
        item = store.add("d1", "u1", "rating", 5)
        assert item.feedback_id == 1

    def test_feedback_id_auto_increments(self):
        store = DocFeedbackStore()
        a = store.add("d1", "u1", "rating", 5)
        b = store.add("d1", "u2", "rating", 3)
        c = store.add("d2", "u1", "comment", "Hi")
        assert a.feedback_id == 1
        assert b.feedback_id == 2
        assert c.feedback_id == 3

    def test_fields_stored_correctly(self):
        store = DocFeedbackStore()
        item = store.add("doc_a", "user_b", "comment", "Nice!", now=42.5)
        assert item.doc_id == "doc_a"
        assert item.user_id == "user_b"
        assert item.feedback_type == "comment"
        assert item.value == "Nice!"
        assert item.timestamp == 42.5

    def test_now_defaults_to_zero(self):
        store = DocFeedbackStore()
        item = store.add("d1", "u1", "rating", 4)
        assert item.timestamp == 0.0

    def test_now_explicit(self):
        store = DocFeedbackStore()
        item = store.add("d1", "u1", "rating", 4, now=99.9)
        assert item.timestamp == 99.9

    def test_total_items_grows(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        store.add("d1", "u2", "reaction", "thumbs_up")
        assert store.total_items == 2

    def test_multiple_feedback_types(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        store.add("d1", "u1", "comment", "Good")
        store.add("d1", "u1", "reaction", "heart")
        assert store.total_items == 3

    def test_same_user_same_doc_multiple_items(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 4)
        store.add("d1", "u1", "rating", 5)
        assert store.total_items == 2


# ---------------------------------------------------------------------------
# get()
# ---------------------------------------------------------------------------
class TestGet:
    def test_returns_item_by_id(self):
        store = DocFeedbackStore()
        added = store.add("d1", "u1", "rating", 5)
        fetched = store.get(added.feedback_id)
        assert fetched is added

    def test_returns_none_for_missing_id(self):
        store = DocFeedbackStore()
        assert store.get(999) is None

    def test_returns_none_after_delete(self):
        store = DocFeedbackStore()
        item = store.add("d1", "u1", "rating", 5)
        store.delete(item.feedback_id)
        assert store.get(item.feedback_id) is None


# ---------------------------------------------------------------------------
# delete()
# ---------------------------------------------------------------------------
class TestDelete:
    def test_delete_existing_returns_true(self):
        store = DocFeedbackStore()
        item = store.add("d1", "u1", "rating", 5)
        assert store.delete(item.feedback_id) is True

    def test_delete_missing_returns_false(self):
        store = DocFeedbackStore()
        assert store.delete(42) is False

    def test_delete_reduces_total_items(self):
        store = DocFeedbackStore()
        item = store.add("d1", "u1", "rating", 5)
        store.delete(item.feedback_id)
        assert store.total_items == 0

    def test_delete_only_targeted_item(self):
        store = DocFeedbackStore()
        a = store.add("d1", "u1", "rating", 5)
        b = store.add("d1", "u2", "rating", 3)
        store.delete(a.feedback_id)
        assert store.get(b.feedback_id) is not None
        assert store.total_items == 1

    def test_double_delete_returns_false_second_time(self):
        store = DocFeedbackStore()
        item = store.add("d1", "u1", "rating", 5)
        store.delete(item.feedback_id)
        assert store.delete(item.feedback_id) is False


# ---------------------------------------------------------------------------
# delete_doc_feedback()
# ---------------------------------------------------------------------------
class TestDeleteDocFeedback:
    def test_returns_count_removed(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        store.add("d1", "u2", "comment", "Hi")
        assert store.delete_doc_feedback("d1") == 2

    def test_returns_zero_for_unknown_doc(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        assert store.delete_doc_feedback("d_none") == 0

    def test_does_not_affect_other_docs(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        store.add("d2", "u1", "rating", 4)
        store.delete_doc_feedback("d1")
        assert store.total_items == 1
        remaining = store.feedback_for_doc("d2")
        assert len(remaining) == 1

    def test_removes_all_types_for_doc(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        store.add("d1", "u1", "comment", "Good")
        store.add("d1", "u1", "reaction", "fire")
        count = store.delete_doc_feedback("d1")
        assert count == 3
        assert store.total_items == 0


# ---------------------------------------------------------------------------
# feedback_for_doc()
# ---------------------------------------------------------------------------
class TestFeedbackForDoc:
    def test_empty_for_unknown_doc(self):
        store = DocFeedbackStore()
        assert store.feedback_for_doc("d_none") == []

    def test_returns_all_feedback_for_doc(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        store.add("d1", "u2", "comment", "Hi")
        store.add("d2", "u1", "rating", 3)
        result = store.feedback_for_doc("d1")
        assert len(result) == 2
        assert all(item.doc_id == "d1" for item in result)

    def test_filter_by_feedback_type(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        store.add("d1", "u2", "comment", "Good")
        store.add("d1", "u3", "reaction", "heart")
        ratings = store.feedback_for_doc("d1", feedback_type="rating")
        assert len(ratings) == 1
        assert ratings[0].feedback_type == "rating"

    def test_newest_first_ordering(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "comment", "first", now=1.0)
        store.add("d1", "u2", "comment", "second", now=5.0)
        store.add("d1", "u3", "comment", "third", now=3.0)
        result = store.feedback_for_doc("d1")
        timestamps = [item.timestamp for item in result]
        assert timestamps == sorted(timestamps, reverse=True)

    def test_limit_parameter(self):
        store = DocFeedbackStore()
        for i in range(10):
            store.add("d1", f"u{i}", "rating", i, now=float(i))
        result = store.feedback_for_doc("d1", limit=3)
        assert len(result) == 3

    def test_limit_none_returns_all(self):
        store = DocFeedbackStore()
        for i in range(5):
            store.add("d1", f"u{i}", "rating", i)
        result = store.feedback_for_doc("d1", limit=None)
        assert len(result) == 5

    def test_filter_type_and_limit_combined(self):
        store = DocFeedbackStore()
        for i in range(5):
            store.add("d1", f"u{i}", "comment", f"msg{i}", now=float(i))
        store.add("d1", "u99", "rating", 5, now=100.0)
        result = store.feedback_for_doc("d1", feedback_type="comment", limit=2)
        assert len(result) == 2
        assert all(item.feedback_type == "comment" for item in result)


# ---------------------------------------------------------------------------
# feedback_by_user()
# ---------------------------------------------------------------------------
class TestFeedbackByUser:
    def test_empty_for_unknown_user(self):
        store = DocFeedbackStore()
        assert store.feedback_by_user("u_none") == []

    def test_returns_all_for_user(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        store.add("d2", "u1", "comment", "Hi")
        store.add("d1", "u2", "rating", 4)
        result = store.feedback_by_user("u1")
        assert len(result) == 2
        assert all(item.user_id == "u1" for item in result)

    def test_filter_by_doc_id(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        store.add("d2", "u1", "rating", 3)
        result = store.feedback_by_user("u1", doc_id="d1")
        assert len(result) == 1
        assert result[0].doc_id == "d1"

    def test_filter_doc_returns_empty_when_no_match(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        result = store.feedback_by_user("u1", doc_id="d_other")
        assert result == []


# ---------------------------------------------------------------------------
# doc_summary()
# ---------------------------------------------------------------------------
class TestDocSummary:
    def test_empty_doc_summary(self):
        store = DocFeedbackStore()
        s = store.doc_summary("d_none")
        assert s.doc_id == "d_none"
        assert s.total_feedback == 0
        assert s.avg_rating is None
        assert s.reaction_counts == {}
        assert s.comment_count == 0

    def test_avg_rating_single(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 4)
        s = store.doc_summary("d1")
        assert s.avg_rating == pytest.approx(4.0)

    def test_avg_rating_multiple(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 4)
        store.add("d1", "u2", "rating", 2)
        s = store.doc_summary("d1")
        assert s.avg_rating == pytest.approx(3.0)

    def test_avg_rating_none_when_no_ratings(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "comment", "Good")
        s = store.doc_summary("d1")
        assert s.avg_rating is None

    def test_reaction_counts(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "reaction", "thumbs_up")
        store.add("d1", "u2", "reaction", "thumbs_up")
        store.add("d1", "u3", "reaction", "heart")
        s = store.doc_summary("d1")
        assert s.reaction_counts["thumbs_up"] == 2
        assert s.reaction_counts["heart"] == 1

    def test_comment_count(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "comment", "Nice")
        store.add("d1", "u2", "comment", "Good")
        s = store.doc_summary("d1")
        assert s.comment_count == 2

    def test_total_feedback_counts_all_types(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        store.add("d1", "u1", "comment", "Good")
        store.add("d1", "u1", "reaction", "heart")
        s = store.doc_summary("d1")
        assert s.total_feedback == 3

    def test_summary_isolated_to_doc(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        store.add("d2", "u1", "rating", 1)
        s = store.doc_summary("d1")
        assert s.avg_rating == pytest.approx(5.0)
        assert s.total_feedback == 1

    def test_summary_after_delete(self):
        store = DocFeedbackStore()
        item = store.add("d1", "u1", "rating", 5)
        store.add("d1", "u2", "rating", 3)
        store.delete(item.feedback_id)
        s = store.doc_summary("d1")
        assert s.avg_rating == pytest.approx(3.0)
        assert s.total_feedback == 1


# ---------------------------------------------------------------------------
# top_rated_docs()
# ---------------------------------------------------------------------------
class TestTopRatedDocs:
    def test_empty_store(self):
        store = DocFeedbackStore()
        assert store.top_rated_docs() == []

    def test_no_rating_items(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "comment", "Good")
        assert store.top_rated_docs() == []

    def test_single_doc(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 4)
        result = store.top_rated_docs()
        assert len(result) == 1
        assert result[0][0] == "d1"
        assert result[0][1] == pytest.approx(4.0)

    def test_sorted_descending(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 2)
        store.add("d2", "u1", "rating", 5)
        store.add("d3", "u1", "rating", 3)
        result = store.top_rated_docs()
        ratings = [r[1] for r in result]
        assert ratings == sorted(ratings, reverse=True)
        assert result[0][0] == "d2"

    def test_limit_respected(self):
        store = DocFeedbackStore()
        for i in range(10):
            store.add(f"d{i}", "u1", "rating", float(i))
        result = store.top_rated_docs(limit=3)
        assert len(result) == 3

    def test_avg_computed_correctly(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 3)
        store.add("d1", "u2", "rating", 5)
        result = store.top_rated_docs()
        assert result[0][1] == pytest.approx(4.0)

    def test_only_includes_rated_docs(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        store.add("d2", "u1", "comment", "No rating here")
        result = store.top_rated_docs()
        doc_ids = [r[0] for r in result]
        assert "d1" in doc_ids
        assert "d2" not in doc_ids


# ---------------------------------------------------------------------------
# stats()
# ---------------------------------------------------------------------------
class TestStats:
    def test_empty_store(self):
        store = DocFeedbackStore()
        s = store.stats()
        assert s.total_items == 0
        assert s.total_docs == 0
        assert s.total_users == 0
        assert s.type_counts == {}

    def test_counts_items_docs_users(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        store.add("d2", "u1", "comment", "Hi")
        store.add("d1", "u2", "reaction", "heart")
        s = store.stats()
        assert s.total_items == 3
        assert s.total_docs == 2
        assert s.total_users == 2

    def test_type_counts(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        store.add("d1", "u2", "rating", 4)
        store.add("d1", "u1", "comment", "Good")
        s = store.stats()
        assert s.type_counts["rating"] == 2
        assert s.type_counts["comment"] == 1

    def test_stats_after_delete(self):
        store = DocFeedbackStore()
        item = store.add("d1", "u1", "rating", 5)
        store.add("d2", "u2", "comment", "Hi")
        store.delete(item.feedback_id)
        s = store.stats()
        assert s.total_items == 1
        assert s.total_docs == 1

    def test_stats_custom_type(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "custom_type", "val")
        s = store.stats()
        assert "custom_type" in s.type_counts
        assert s.type_counts["custom_type"] == 1


# ---------------------------------------------------------------------------
# total_items property
# ---------------------------------------------------------------------------
class TestTotalItems:
    def test_zero_initially(self):
        assert DocFeedbackStore().total_items == 0

    def test_grows_on_add(self):
        store = DocFeedbackStore()
        store.add("d1", "u1", "rating", 5)
        assert store.total_items == 1

    def test_shrinks_on_delete(self):
        store = DocFeedbackStore()
        item = store.add("d1", "u1", "rating", 5)
        store.delete(item.feedback_id)
        assert store.total_items == 0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_adds(self):
        store = DocFeedbackStore()
        errors: list[Exception] = []

        def worker(uid: int) -> None:
            try:
                for i in range(50):
                    store.add(f"d{i % 5}", f"u{uid}", "rating", uid % 5 + 1)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        # 6 users × 50 items each = 300 total
        assert store.total_items == 300

    def test_concurrent_add_and_delete(self):
        store = DocFeedbackStore()
        added_ids: list[int] = []
        lock = threading.Lock()

        def adder() -> None:
            for i in range(30):
                item = store.add("d1", f"u_add_{i}", "rating", 3)
                with lock:
                    added_ids.append(item.feedback_id)

        def deleter() -> None:
            for _ in range(30):
                with lock:
                    if added_ids:
                        fid = added_ids.pop(0)
                    else:
                        fid = None
                if fid is not None:
                    store.delete(fid)

        t1 = threading.Thread(target=adder)
        t2 = threading.Thread(target=deleter)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        # Should not raise; total_items must be non-negative
        assert store.total_items >= 0

    def test_concurrent_feedback_for_doc(self):
        store = DocFeedbackStore()
        for i in range(20):
            store.add("d1", f"u{i}", "comment", f"msg{i}", now=float(i))

        results: list[int] = []

        def reader() -> None:
            items = store.feedback_for_doc("d1")
            results.append(len(items))

        threads = [threading.Thread(target=reader) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert all(r == 20 for r in results)
