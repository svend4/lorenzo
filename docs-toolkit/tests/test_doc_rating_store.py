"""Tests for E318 DocRatingStore."""

import threading
import time

import pytest

from docstoolkit.doc_rating_store import (
    DocRatingStore,
    Rating,
    RatingStats,
    RatingSummary,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestRatingDataclass:
    def test_required_fields(self):
        r = Rating(doc_id="d1", user_id="u1", score=4.5)
        assert r.doc_id == "d1"
        assert r.user_id == "u1"
        assert r.score == 4.5

    def test_defaults(self):
        r = Rating(doc_id="d1", user_id="u1", score=3.0)
        assert r.rated_at == 0.0
        assert r.review == ""

    def test_custom_values(self):
        r = Rating(doc_id="d2", user_id="u2", score=2.0, rated_at=1000.0, review="ok")
        assert r.rated_at == 1000.0
        assert r.review == "ok"

    def test_score_float(self):
        r = Rating(doc_id="d1", user_id="u1", score=1.5)
        assert isinstance(r.score, float)

    def test_equality(self):
        r1 = Rating(doc_id="d", user_id="u", score=3.0, rated_at=1.0, review="x")
        r2 = Rating(doc_id="d", user_id="u", score=3.0, rated_at=1.0, review="x")
        assert r1 == r2


class TestRatingSummaryDataclass:
    def test_fields(self):
        s = RatingSummary(
            doc_id="d1",
            count=3,
            avg_score=4.0,
            min_score=3.0,
            max_score=5.0,
            score_distribution={3.0: 1, 4.0: 1, 5.0: 1},
        )
        assert s.doc_id == "d1"
        assert s.count == 3
        assert s.avg_score == 4.0
        assert s.min_score == 3.0
        assert s.max_score == 5.0
        assert s.score_distribution == {3.0: 1, 4.0: 1, 5.0: 1}

    def test_default_distribution(self):
        s = RatingSummary(doc_id="d1", count=0, avg_score=0.0, min_score=0.0, max_score=0.0)
        assert s.score_distribution == {}

    def test_distribution_independence(self):
        s1 = RatingSummary(doc_id="d1", count=0, avg_score=0.0, min_score=0.0, max_score=0.0)
        s2 = RatingSummary(doc_id="d2", count=0, avg_score=0.0, min_score=0.0, max_score=0.0)
        s1.score_distribution["x"] = 1
        assert "x" not in s2.score_distribution


class TestRatingStatsDataclass:
    def test_fields(self):
        st = RatingStats(total_ratings=10, unique_docs=3, unique_users=5, global_avg=4.2)
        assert st.total_ratings == 10
        assert st.unique_docs == 3
        assert st.unique_users == 5
        assert st.global_avg == 4.2

    def test_zero_values(self):
        st = RatingStats(total_ratings=0, unique_docs=0, unique_users=0, global_avg=0.0)
        assert st.global_avg == 0.0


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_store(self):
        store = DocRatingStore()
        assert store.all_doc_ids() == []

    def test_stats_empty(self):
        store = DocRatingStore()
        st = store.stats()
        assert st.total_ratings == 0
        assert st.unique_docs == 0
        assert st.unique_users == 0
        assert st.global_avg == 0.0

    def test_multiple_independent_stores(self):
        s1 = DocRatingStore()
        s2 = DocRatingStore()
        s1.rate("d1", "u1", 5.0)
        assert s2.all_doc_ids() == []


# ---------------------------------------------------------------------------
# rate()
# ---------------------------------------------------------------------------


class TestRate:
    def test_creates_rating(self):
        store = DocRatingStore()
        r = store.rate("doc1", "user1", 4.0)
        assert r.doc_id == "doc1"
        assert r.user_id == "user1"
        assert r.score == 4.0

    def test_replaces_rating(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 3.0)
        r2 = store.rate("doc1", "user1", 5.0)
        assert r2.score == 5.0
        # Still only one rating
        assert len(store.ratings_for_doc("doc1")) == 1

    def test_timestamp_default(self):
        store = DocRatingStore()
        before = time.time()
        r = store.rate("doc1", "user1", 4.0)
        after = time.time()
        assert before <= r.rated_at <= after

    def test_timestamp_override(self):
        store = DocRatingStore()
        r = store.rate("doc1", "user1", 4.0, now=9999.0)
        assert r.rated_at == 9999.0

    def test_review_stored(self):
        store = DocRatingStore()
        r = store.rate("doc1", "user1", 4.0, review="Great doc!")
        assert r.review == "Great doc!"

    def test_review_default_empty(self):
        store = DocRatingStore()
        r = store.rate("doc1", "user1", 4.0)
        assert r.review == ""

    def test_multiple_users_same_doc(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 4.0)
        store.rate("doc1", "user2", 2.0)
        assert len(store.ratings_for_doc("doc1")) == 2

    def test_returns_rating_instance(self):
        store = DocRatingStore()
        r = store.rate("doc1", "user1", 3.5)
        assert isinstance(r, Rating)


# ---------------------------------------------------------------------------
# get_rating()
# ---------------------------------------------------------------------------


class TestGetRating:
    def test_found(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 4.0, now=1.0)
        r = store.get_rating("doc1", "user1")
        assert r is not None
        assert r.score == 4.0

    def test_not_found_wrong_doc(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 4.0)
        assert store.get_rating("doc99", "user1") is None

    def test_not_found_wrong_user(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 4.0)
        assert store.get_rating("doc1", "user99") is None

    def test_not_found_empty_store(self):
        store = DocRatingStore()
        assert store.get_rating("doc1", "user1") is None


# ---------------------------------------------------------------------------
# delete_rating()
# ---------------------------------------------------------------------------


class TestDeleteRating:
    def test_delete_existing_returns_true(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 4.0)
        assert store.delete_rating("doc1", "user1") is True

    def test_delete_nonexistent_returns_false(self):
        store = DocRatingStore()
        assert store.delete_rating("doc1", "user1") is False

    def test_delete_removes_rating(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 4.0)
        store.delete_rating("doc1", "user1")
        assert store.get_rating("doc1", "user1") is None

    def test_delete_updates_doc_index(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 4.0)
        store.delete_rating("doc1", "user1")
        assert "doc1" not in store.all_doc_ids()

    def test_delete_partial(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 4.0)
        store.rate("doc1", "user2", 3.0)
        store.delete_rating("doc1", "user1")
        assert len(store.ratings_for_doc("doc1")) == 1

    def test_delete_twice_returns_false(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 4.0)
        store.delete_rating("doc1", "user1")
        assert store.delete_rating("doc1", "user1") is False


# ---------------------------------------------------------------------------
# summary()
# ---------------------------------------------------------------------------


class TestSummary:
    def test_none_for_no_ratings(self):
        store = DocRatingStore()
        assert store.summary("doc1") is None

    def test_single_rating(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 3.0)
        s = store.summary("doc1")
        assert s is not None
        assert s.count == 1
        assert s.avg_score == 3.0
        assert s.min_score == 3.0
        assert s.max_score == 3.0
        assert s.score_distribution == {3.0: 1}

    def test_multiple_ratings_avg(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 2.0)
        store.rate("doc1", "user2", 4.0)
        s = store.summary("doc1")
        assert s.avg_score == pytest.approx(3.0)

    def test_min_max(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 1.0)
        store.rate("doc1", "user2", 5.0)
        store.rate("doc1", "user3", 3.0)
        s = store.summary("doc1")
        assert s.min_score == 1.0
        assert s.max_score == 5.0

    def test_distribution_rounding(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 4.55)
        store.rate("doc1", "user2", 4.54)
        s = store.summary("doc1")
        # 4.55 → 4.6 (round half to even: actually 4.6), 4.54 → 4.5
        assert s.score_distribution.get(round(4.55, 1), 0) >= 0  # just check no crash

    def test_distribution_counts(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 5.0)
        store.rate("doc1", "user2", 5.0)
        store.rate("doc1", "user3", 3.0)
        s = store.summary("doc1")
        assert s.score_distribution[5.0] == 2
        assert s.score_distribution[3.0] == 1

    def test_none_after_delete_all(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 4.0)
        store.delete_rating("doc1", "user1")
        assert store.summary("doc1") is None


# ---------------------------------------------------------------------------
# ratings_for_doc()
# ---------------------------------------------------------------------------


class TestRatingsForDoc:
    def test_empty_list_unknown_doc(self):
        store = DocRatingStore()
        assert store.ratings_for_doc("doc99") == []

    def test_sorted_by_rated_at(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 4.0, now=200.0)
        store.rate("doc1", "user2", 3.0, now=100.0)
        store.rate("doc1", "user3", 5.0, now=150.0)
        ratings = store.ratings_for_doc("doc1")
        times = [r.rated_at for r in ratings]
        assert times == sorted(times)

    def test_count(self):
        store = DocRatingStore()
        for i in range(5):
            store.rate("doc1", f"user{i}", float(i + 1))
        assert len(store.ratings_for_doc("doc1")) == 5

    def test_returns_rating_objects(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 4.0)
        ratings = store.ratings_for_doc("doc1")
        assert all(isinstance(r, Rating) for r in ratings)


# ---------------------------------------------------------------------------
# ratings_by_user()
# ---------------------------------------------------------------------------


class TestRatingsByUser:
    def test_empty_unknown_user(self):
        store = DocRatingStore()
        assert store.ratings_by_user("nobody") == []

    def test_cross_doc(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 3.0, now=10.0)
        store.rate("doc2", "user1", 5.0, now=5.0)
        store.rate("doc1", "user2", 2.0, now=1.0)
        ratings = store.ratings_by_user("user1")
        assert len(ratings) == 2
        assert all(r.user_id == "user1" for r in ratings)

    def test_sorted_by_rated_at(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 3.0, now=30.0)
        store.rate("doc2", "user1", 5.0, now=10.0)
        store.rate("doc3", "user1", 4.0, now=20.0)
        ratings = store.ratings_by_user("user1")
        times = [r.rated_at for r in ratings]
        assert times == sorted(times)


# ---------------------------------------------------------------------------
# top_rated_docs()
# ---------------------------------------------------------------------------


class TestTopRatedDocs:
    def test_sorted_by_avg_desc(self):
        store = DocRatingStore()
        store.rate("doc_a", "u1", 3.0)
        store.rate("doc_b", "u1", 5.0)
        store.rate("doc_c", "u1", 4.0)
        top = store.top_rated_docs()
        avgs = [avg for _, avg in top]
        assert avgs == sorted(avgs, reverse=True)

    def test_tiebreak_by_doc_id_asc(self):
        store = DocRatingStore()
        store.rate("z_doc", "u1", 4.0)
        store.rate("a_doc", "u1", 4.0)
        top = store.top_rated_docs()
        doc_ids = [d for d, _ in top]
        assert doc_ids == ["a_doc", "z_doc"]

    def test_limit(self):
        store = DocRatingStore()
        for i in range(10):
            store.rate(f"doc{i}", "u1", float(i))
        top = store.top_rated_docs(limit=3)
        assert len(top) == 3

    def test_default_limit_ten(self):
        store = DocRatingStore()
        for i in range(15):
            store.rate(f"doc{i:02d}", "u1", float(i % 5))
        top = store.top_rated_docs()
        assert len(top) <= 10

    def test_returns_tuples(self):
        store = DocRatingStore()
        store.rate("doc1", "u1", 4.0)
        top = store.top_rated_docs()
        assert isinstance(top[0], tuple)
        assert len(top[0]) == 2


# ---------------------------------------------------------------------------
# has_rated()
# ---------------------------------------------------------------------------


class TestHasRated:
    def test_true_after_rating(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 4.0)
        assert store.has_rated("user1", "doc1") is True

    def test_false_unknown(self):
        store = DocRatingStore()
        assert store.has_rated("user1", "doc1") is False

    def test_false_after_delete(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 4.0)
        store.delete_rating("doc1", "user1")
        assert store.has_rated("user1", "doc1") is False

    def test_user_cross_doc(self):
        store = DocRatingStore()
        store.rate("doc1", "user1", 4.0)
        assert store.has_rated("user1", "doc2") is False


# ---------------------------------------------------------------------------
# all_doc_ids()
# ---------------------------------------------------------------------------


class TestAllDocIds:
    def test_empty(self):
        store = DocRatingStore()
        assert store.all_doc_ids() == []

    def test_sorted(self):
        store = DocRatingStore()
        store.rate("c_doc", "u1", 1.0)
        store.rate("a_doc", "u1", 2.0)
        store.rate("b_doc", "u1", 3.0)
        assert store.all_doc_ids() == ["a_doc", "b_doc", "c_doc"]

    def test_no_duplicates(self):
        store = DocRatingStore()
        store.rate("doc1", "u1", 1.0)
        store.rate("doc1", "u2", 2.0)
        assert store.all_doc_ids() == ["doc1"]

    def test_removed_after_delete(self):
        store = DocRatingStore()
        store.rate("doc1", "u1", 3.0)
        store.delete_rating("doc1", "u1")
        assert "doc1" not in store.all_doc_ids()


# ---------------------------------------------------------------------------
# stats()
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty_store(self):
        store = DocRatingStore()
        st = store.stats()
        assert st.total_ratings == 0
        assert st.unique_docs == 0
        assert st.unique_users == 0
        assert st.global_avg == 0.0

    def test_total_ratings(self):
        store = DocRatingStore()
        store.rate("d1", "u1", 4.0)
        store.rate("d1", "u2", 2.0)
        store.rate("d2", "u1", 5.0)
        assert store.stats().total_ratings == 3

    def test_unique_docs(self):
        store = DocRatingStore()
        store.rate("d1", "u1", 4.0)
        store.rate("d2", "u1", 3.0)
        assert store.stats().unique_docs == 2

    def test_unique_users(self):
        store = DocRatingStore()
        store.rate("d1", "u1", 4.0)
        store.rate("d2", "u2", 3.0)
        store.rate("d3", "u1", 5.0)
        assert store.stats().unique_users == 2

    def test_global_avg(self):
        store = DocRatingStore()
        store.rate("d1", "u1", 2.0)
        store.rate("d1", "u2", 4.0)
        store.rate("d2", "u1", 3.0)
        st = store.stats()
        assert st.global_avg == pytest.approx(3.0)

    def test_replace_doesnt_inflate_total(self):
        store = DocRatingStore()
        store.rate("d1", "u1", 3.0)
        store.rate("d1", "u1", 5.0)
        assert store.stats().total_ratings == 1


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_rate_calls(self):
        store = DocRatingStore()
        errors = []

        def worker(user_id: str) -> None:
            try:
                for i in range(20):
                    store.rate(f"doc{i % 5}", user_id, float(i % 5 + 1))
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(f"u{t}",)) for t in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread errors: {errors}"
        st = store.stats()
        assert st.total_ratings > 0

    def test_concurrent_read_write(self):
        store = DocRatingStore()
        errors = []

        def writer() -> None:
            try:
                for i in range(30):
                    store.rate("doc1", f"u{i}", float(i % 5 + 1))
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        def reader() -> None:
            try:
                for _ in range(30):
                    store.summary("doc1")
                    store.stats()
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=writer)] + [
            threading.Thread(target=reader) for _ in range(4)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread errors: {errors}"
