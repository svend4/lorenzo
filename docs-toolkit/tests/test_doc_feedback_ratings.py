"""Tests for E439 DocFeedbackRatings."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_feedback_ratings import (
    DocFeedbackRatings,
    Feedback,
    FeedbackStats,
    RatingsSummary,
)


# ----------------------------------------------------------------------
# Submit / basic invariants
# ----------------------------------------------------------------------

def test_submit_returns_feedback_instance():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 5)
    assert isinstance(fb, Feedback)


def test_submit_assigns_feedback_id_starting_at_1():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 5)
    assert fb.feedback_id == 1


def test_submit_auto_increments_ids():
    r = DocFeedbackRatings()
    a = r.submit("d1", "u1", 5)
    b = r.submit("d1", "u2", 4)
    c = r.submit("d2", "u1", 3)
    assert (a.feedback_id, b.feedback_id, c.feedback_id) == (1, 2, 3)


def test_submit_stores_all_fields():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 4, comment="nice", now=123.0)
    assert fb.doc_id == "d1"
    assert fb.user_id == "u1"
    assert fb.rating == 4
    assert fb.comment == "nice"
    assert fb.created_at == 123.0


def test_submit_default_comment_empty():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 3)
    assert fb.comment == ""


def test_submit_default_created_at_is_zero():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 3)
    assert fb.created_at == 0.0


def test_submit_rejects_rating_below_1():
    r = DocFeedbackRatings()
    with pytest.raises(ValueError):
        r.submit("d1", "u1", 0)


def test_submit_rejects_rating_above_5():
    r = DocFeedbackRatings()
    with pytest.raises(ValueError):
        r.submit("d1", "u1", 6)


def test_submit_rejects_negative_rating():
    r = DocFeedbackRatings()
    with pytest.raises(ValueError):
        r.submit("d1", "u1", -3)


def test_submit_accepts_all_valid_ratings():
    r = DocFeedbackRatings()
    for rating in (1, 2, 3, 4, 5):
        fb = r.submit("d1", "u1", rating)
        assert fb.rating == rating


def test_submit_failed_does_not_advance_id():
    r = DocFeedbackRatings()
    with pytest.raises(ValueError):
        r.submit("d1", "u1", 10)
    fb = r.submit("d1", "u1", 5)
    assert fb.feedback_id == 1


# ----------------------------------------------------------------------
# Get
# ----------------------------------------------------------------------

def test_get_returns_stored_feedback():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 5, comment="hello")
    assert r.get(fb.feedback_id) == fb


def test_get_unknown_returns_none():
    r = DocFeedbackRatings()
    assert r.get(999) is None


def test_get_on_empty_store_returns_none():
    r = DocFeedbackRatings()
    assert r.get(1) is None


# ----------------------------------------------------------------------
# Update
# ----------------------------------------------------------------------

def test_update_rating_only():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 3, comment="meh")
    updated = r.update(fb.feedback_id, rating=5)
    assert updated.rating == 5
    assert updated.comment == "meh"


def test_update_comment_only():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 3, comment="meh")
    updated = r.update(fb.feedback_id, comment="great")
    assert updated.rating == 3
    assert updated.comment == "great"


def test_update_both_fields():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 3)
    updated = r.update(fb.feedback_id, rating=4, comment="ok")
    assert updated.rating == 4
    assert updated.comment == "ok"


def test_update_unknown_returns_none():
    r = DocFeedbackRatings()
    assert r.update(999, rating=5) is None


def test_update_invalid_rating_raises():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 3)
    with pytest.raises(ValueError):
        r.update(fb.feedback_id, rating=0)


def test_update_invalid_rating_does_not_mutate():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 3)
    with pytest.raises(ValueError):
        r.update(fb.feedback_id, rating=99)
    assert r.get(fb.feedback_id).rating == 3


def test_update_no_args_returns_unchanged():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 3, comment="x")
    updated = r.update(fb.feedback_id)
    assert updated.rating == 3
    assert updated.comment == "x"


# ----------------------------------------------------------------------
# Delete
# ----------------------------------------------------------------------

def test_delete_existing_returns_true():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 4)
    assert r.delete(fb.feedback_id) is True


def test_delete_unknown_returns_false():
    r = DocFeedbackRatings()
    assert r.delete(999) is False


def test_delete_removes_from_get():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 4)
    r.delete(fb.feedback_id)
    assert r.get(fb.feedback_id) is None


def test_delete_removes_from_doc_index():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 4)
    r.delete(fb.feedback_id)
    assert r.feedback_for_doc("d1") == []
    assert r.count_for_doc("d1") == 0


def test_delete_removes_from_user_index():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 4)
    r.delete(fb.feedback_id)
    assert r.feedback_by_user("u1") == []
    assert r.count_by_user("u1") == 0


def test_delete_twice_second_returns_false():
    r = DocFeedbackRatings()
    fb = r.submit("d1", "u1", 4)
    r.delete(fb.feedback_id)
    assert r.delete(fb.feedback_id) is False


# ----------------------------------------------------------------------
# feedback_for_doc / feedback_by_user
# ----------------------------------------------------------------------

def test_feedback_for_doc_empty_returns_empty_list():
    r = DocFeedbackRatings()
    assert r.feedback_for_doc("d1") == []


def test_feedback_for_doc_returns_only_that_doc():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5)
    r.submit("d2", "u1", 3)
    r.submit("d1", "u2", 4)
    items = r.feedback_for_doc("d1")
    assert len(items) == 2
    assert all(i.doc_id == "d1" for i in items)


def test_feedback_for_doc_newest_first():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5, now=1.0)
    r.submit("d1", "u1", 4, now=3.0)
    r.submit("d1", "u1", 3, now=2.0)
    items = r.feedback_for_doc("d1")
    assert [i.created_at for i in items] == [3.0, 2.0, 1.0]


def test_feedback_for_doc_limit():
    r = DocFeedbackRatings()
    for i in range(5):
        r.submit("d1", "u1", 3, now=float(i))
    items = r.feedback_for_doc("d1", limit=2)
    assert len(items) == 2
    assert items[0].created_at == 4.0
    assert items[1].created_at == 3.0


def test_feedback_by_user_empty():
    r = DocFeedbackRatings()
    assert r.feedback_by_user("u1") == []


def test_feedback_by_user_returns_only_that_user():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5)
    r.submit("d2", "u2", 4)
    r.submit("d3", "u1", 3)
    items = r.feedback_by_user("u1")
    assert len(items) == 2
    assert all(i.user_id == "u1" for i in items)


def test_feedback_by_user_newest_first():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5, now=1.0)
    r.submit("d2", "u1", 4, now=5.0)
    r.submit("d3", "u1", 3, now=2.0)
    items = r.feedback_by_user("u1")
    assert [i.created_at for i in items] == [5.0, 2.0, 1.0]


def test_feedback_by_user_limit():
    r = DocFeedbackRatings()
    for i in range(4):
        r.submit(f"d{i}", "u1", 3, now=float(i))
    items = r.feedback_by_user("u1", limit=2)
    assert len(items) == 2


# ----------------------------------------------------------------------
# Summary
# ----------------------------------------------------------------------

def test_summary_none_when_no_feedback():
    r = DocFeedbackRatings()
    assert r.summary("d1") is None


def test_summary_basic():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5)
    r.submit("d1", "u2", 3)
    s = r.summary("d1")
    assert isinstance(s, RatingsSummary)
    assert s.doc_id == "d1"
    assert s.count == 2
    assert s.avg_rating == 4.0


def test_summary_distribution_contains_all_keys():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 3)
    s = r.summary("d1")
    assert set(s.distribution.keys()) == {1, 2, 3, 4, 5}


def test_summary_distribution_counts():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5)
    r.submit("d1", "u2", 5)
    r.submit("d1", "u3", 3)
    r.submit("d1", "u4", 1)
    s = r.summary("d1")
    assert s.distribution[5] == 2
    assert s.distribution[3] == 1
    assert s.distribution[1] == 1
    assert s.distribution[2] == 0
    assert s.distribution[4] == 0


def test_summary_only_for_requested_doc():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5)
    r.submit("d2", "u1", 1)
    s1 = r.summary("d1")
    s2 = r.summary("d2")
    assert s1.avg_rating == 5.0
    assert s2.avg_rating == 1.0


# ----------------------------------------------------------------------
# top_rated / worst_rated
# ----------------------------------------------------------------------

def test_top_rated_empty():
    r = DocFeedbackRatings()
    assert r.top_rated() == []


def test_top_rated_basic_order():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 3)
    r.submit("d2", "u1", 5)
    r.submit("d3", "u1", 1)
    result = r.top_rated()
    assert [doc for doc, _ in result] == ["d2", "d1", "d3"]


def test_top_rated_respects_limit():
    r = DocFeedbackRatings()
    for i in range(5):
        r.submit(f"d{i}", "u1", i + 1)
    result = r.top_rated(limit=2)
    assert len(result) == 2


def test_top_rated_min_count_filter():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5)
    r.submit("d2", "u1", 4)
    r.submit("d2", "u2", 4)
    result = r.top_rated(min_count=2)
    assert [doc for doc, _ in result] == ["d2"]


def test_top_rated_tie_breaks_by_doc_id_asc():
    r = DocFeedbackRatings()
    r.submit("dB", "u1", 4)
    r.submit("dA", "u1", 4)
    result = r.top_rated()
    assert [doc for doc, _ in result] == ["dA", "dB"]


def test_worst_rated_basic_order():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 3)
    r.submit("d2", "u1", 5)
    r.submit("d3", "u1", 1)
    result = r.worst_rated()
    assert [doc for doc, _ in result] == ["d3", "d1", "d2"]


def test_worst_rated_min_count_filter():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 1)
    r.submit("d2", "u1", 2)
    r.submit("d2", "u2", 2)
    result = r.worst_rated(min_count=2)
    assert [doc for doc, _ in result] == ["d2"]


def test_worst_rated_tie_breaks_by_doc_id_asc():
    r = DocFeedbackRatings()
    r.submit("dB", "u1", 2)
    r.submit("dA", "u1", 2)
    result = r.worst_rated()
    assert [doc for doc, _ in result] == ["dA", "dB"]


def test_top_rated_averages_correctly():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5)
    r.submit("d1", "u2", 3)  # avg 4.0
    r.submit("d2", "u1", 4)
    r.submit("d2", "u2", 5)  # avg 4.5
    result = r.top_rated()
    assert result[0] == ("d2", 4.5)
    assert result[1] == ("d1", 4.0)


# ----------------------------------------------------------------------
# Counts / listings
# ----------------------------------------------------------------------

def test_count_for_doc_empty_is_zero():
    r = DocFeedbackRatings()
    assert r.count_for_doc("d1") == 0


def test_count_for_doc_basic():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5)
    r.submit("d1", "u2", 4)
    r.submit("d2", "u1", 3)
    assert r.count_for_doc("d1") == 2
    assert r.count_for_doc("d2") == 1


def test_count_by_user_basic():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5)
    r.submit("d2", "u1", 4)
    r.submit("d3", "u2", 3)
    assert r.count_by_user("u1") == 2
    assert r.count_by_user("u2") == 1
    assert r.count_by_user("u3") == 0


def test_all_doc_ids_empty():
    r = DocFeedbackRatings()
    assert r.all_doc_ids() == []


def test_all_doc_ids_sorted_and_unique():
    r = DocFeedbackRatings()
    r.submit("dB", "u1", 5)
    r.submit("dA", "u1", 4)
    r.submit("dB", "u2", 3)
    r.submit("dC", "u1", 2)
    assert r.all_doc_ids() == ["dA", "dB", "dC"]


# ----------------------------------------------------------------------
# clear_doc / clear_user
# ----------------------------------------------------------------------

def test_clear_doc_returns_count():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5)
    r.submit("d1", "u2", 4)
    r.submit("d2", "u1", 3)
    assert r.clear_doc("d1") == 2


def test_clear_doc_removes_only_that_doc():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5)
    r.submit("d2", "u1", 3)
    r.clear_doc("d1")
    assert r.count_for_doc("d1") == 0
    assert r.count_for_doc("d2") == 1


def test_clear_doc_unknown_returns_zero():
    r = DocFeedbackRatings()
    assert r.clear_doc("nope") == 0


def test_clear_doc_updates_user_index():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5)
    r.submit("d2", "u1", 4)
    r.clear_doc("d1")
    items = r.feedback_by_user("u1")
    assert len(items) == 1
    assert items[0].doc_id == "d2"


def test_clear_user_returns_count():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5)
    r.submit("d2", "u1", 4)
    r.submit("d1", "u2", 3)
    assert r.clear_user("u1") == 2


def test_clear_user_removes_only_that_user():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5)
    r.submit("d1", "u2", 4)
    r.clear_user("u1")
    assert r.count_by_user("u1") == 0
    assert r.count_by_user("u2") == 1


def test_clear_user_unknown_returns_zero():
    r = DocFeedbackRatings()
    assert r.clear_user("nope") == 0


def test_clear_user_updates_doc_index():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5)
    r.submit("d1", "u2", 3)
    r.clear_user("u1")
    items = r.feedback_for_doc("d1")
    assert len(items) == 1
    assert items[0].user_id == "u2"


# ----------------------------------------------------------------------
# Stats
# ----------------------------------------------------------------------

def test_stats_empty():
    r = DocFeedbackRatings()
    s = r.stats()
    assert isinstance(s, FeedbackStats)
    assert s.total_feedback == 0
    assert s.unique_docs == 0
    assert s.unique_users == 0
    assert s.global_avg_rating == 0.0


def test_stats_basic():
    r = DocFeedbackRatings()
    r.submit("d1", "u1", 5)
    r.submit("d1", "u2", 3)
    r.submit("d2", "u1", 4)
    s = r.stats()
    assert s.total_feedback == 3
    assert s.unique_docs == 2
    assert s.unique_users == 2
    assert s.global_avg_rating == pytest.approx(4.0)


def test_stats_after_deletes():
    r = DocFeedbackRatings()
    a = r.submit("d1", "u1", 5)
    r.submit("d2", "u2", 1)
    r.delete(a.feedback_id)
    s = r.stats()
    assert s.total_feedback == 1
    assert s.unique_docs == 1
    assert s.unique_users == 1
    assert s.global_avg_rating == 1.0


# ----------------------------------------------------------------------
# Thread safety
# ----------------------------------------------------------------------

def test_thread_safety_submit_concurrent_unique_ids():
    r = DocFeedbackRatings()
    ids: list[int] = []
    lock = threading.Lock()

    def worker(n: int) -> None:
        for _ in range(n):
            fb = r.submit("d1", "u1", 3)
            with lock:
                ids.append(fb.feedback_id)

    threads = [threading.Thread(target=worker, args=(50,)) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(ids) == 8 * 50
    assert len(set(ids)) == len(ids)
    assert r.stats().total_feedback == 8 * 50


def test_thread_safety_mixed_operations():
    r = DocFeedbackRatings()
    # Seed some data
    seeded = [r.submit("d1", f"u{i}", 3) for i in range(20)]

    def submitter() -> None:
        for _ in range(30):
            r.submit("d2", "uX", 4)

    def reader() -> None:
        for _ in range(30):
            r.feedback_for_doc("d1")
            r.summary("d1")
            r.stats()

    def deleter() -> None:
        for fb in seeded:
            r.delete(fb.feedback_id)

    threads = [
        threading.Thread(target=submitter),
        threading.Thread(target=submitter),
        threading.Thread(target=reader),
        threading.Thread(target=reader),
        threading.Thread(target=deleter),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # 20 seeded - 20 deleted + 60 new = 60
    assert r.stats().total_feedback == 60
    assert r.count_for_doc("d2") == 60
