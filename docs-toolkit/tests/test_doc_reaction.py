"""Tests for docstoolkit.doc_reaction."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_reaction import (
    DocReaction,
    Reaction,
    ReactionSummary,
    ReactionType,
    UserActivity,
)


# ---------------------------------------------------------------------------
# Basic dataclasses / enum
# ---------------------------------------------------------------------------
class TestReactionType:
    def test_has_ten_members(self):
        assert len(list(ReactionType)) == 10

    def test_thumbs_up_value(self):
        assert ReactionType.THUMBS_UP.value == "thumbs_up"

    def test_members_present(self):
        names = {m.name for m in ReactionType}
        expected = {
            "THUMBS_UP",
            "THUMBS_DOWN",
            "HEART",
            "LAUGH",
            "WOW",
            "SAD",
            "ANGRY",
            "INSIGHTFUL",
            "FIRE",
            "EYES",
        }
        assert names == expected


class TestReaction:
    def test_construction(self):
        r = Reaction("d1", "u1", ReactionType.HEART, 12.5)
        assert r.doc_id == "d1"
        assert r.user_id == "u1"
        assert r.reaction_type is ReactionType.HEART
        assert r.created_at == 12.5

    def test_default_created_at(self):
        r = Reaction("d1", "u1", ReactionType.HEART)
        assert r.created_at == 0.0


class TestReactionSummary:
    def test_defaults(self):
        s = ReactionSummary(doc_id="d1")
        assert s.doc_id == "d1"
        assert s.counts == {}
        assert s.total == 0
        assert s.top_reaction is None
        assert s.unique_reactors == 0

    def test_custom_fields(self):
        s = ReactionSummary(
            doc_id="d1",
            counts={ReactionType.HEART: 2},
            total=2,
            top_reaction=ReactionType.HEART,
            unique_reactors=2,
        )
        assert s.counts[ReactionType.HEART] == 2
        assert s.top_reaction is ReactionType.HEART


class TestUserActivity:
    def test_defaults(self):
        u = UserActivity(user_id="u1")
        assert u.user_id == "u1"
        assert u.total_reactions == 0
        assert u.by_type == {}
        assert u.last_at == 0.0

    def test_custom_fields(self):
        u = UserActivity(
            user_id="u1",
            total_reactions=3,
            by_type={ReactionType.HEART: 2, ReactionType.FIRE: 1},
            last_at=99.0,
        )
        assert u.total_reactions == 3
        assert u.last_at == 99.0


# ---------------------------------------------------------------------------
# Add
# ---------------------------------------------------------------------------
class TestAdd:
    def test_basic_add(self):
        dr = DocReaction()
        r = dr.add("d1", "u1", ReactionType.HEART, now=1.0)
        assert r is not None
        assert r.doc_id == "d1"
        assert r.user_id == "u1"
        assert r.reaction_type is ReactionType.HEART
        assert r.created_at == 1.0

    def test_add_increments_total(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d1", "u2", ReactionType.HEART)
        assert dr.total_reactions == 2

    def test_add_with_invalid_reaction_type_returns_none(self):
        dr = DocReaction()
        assert dr.add("d1", "u1", "not-an-enum") is None  # type: ignore[arg-type]
        assert dr.total_reactions == 0

    def test_add_empty_doc_id_returns_none(self):
        dr = DocReaction()
        assert dr.add("", "u1", ReactionType.HEART) is None

    def test_add_empty_user_id_returns_none(self):
        dr = DocReaction()
        assert dr.add("d1", "", ReactionType.HEART) is None


class TestAddReplaces:
    """unique_per_user=True replaces existing reaction."""

    def test_replaces_previous(self):
        dr = DocReaction(unique_per_user=True)
        dr.add("d1", "u1", ReactionType.HEART, now=1.0)
        dr.add("d1", "u1", ReactionType.FIRE, now=2.0)
        # Only one reaction kept for (d1, u1).
        rs = dr.reactions_for_doc("d1")
        assert len(rs) == 1
        assert rs[0].reaction_type is ReactionType.FIRE
        assert rs[0].created_at == 2.0

    def test_same_reaction_re_added_replaces(self):
        dr = DocReaction(unique_per_user=True)
        dr.add("d1", "u1", ReactionType.HEART, now=1.0)
        dr.add("d1", "u1", ReactionType.HEART, now=5.0)
        rs = dr.reactions_for_doc("d1")
        assert len(rs) == 1
        assert rs[0].created_at == 5.0

    def test_different_users_independent(self):
        dr = DocReaction(unique_per_user=True)
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d1", "u2", ReactionType.FIRE)
        assert len(dr.reactions_for_doc("d1")) == 2


class TestAddMultiple:
    """unique_per_user=False allows multiple types per user per doc."""

    def test_multiple_types_kept(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART, now=1.0)
        dr.add("d1", "u1", ReactionType.FIRE, now=2.0)
        rs = dr.reactions_for_doc("d1")
        assert len(rs) == 2
        types = {r.reaction_type for r in rs}
        assert types == {ReactionType.HEART, ReactionType.FIRE}

    def test_duplicate_type_refreshes_timestamp(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART, now=1.0)
        dr.add("d1", "u1", ReactionType.HEART, now=10.0)
        rs = dr.reactions_for_doc("d1")
        assert len(rs) == 1
        assert rs[0].created_at == 10.0


# ---------------------------------------------------------------------------
# Remove
# ---------------------------------------------------------------------------
class TestRemove:
    def test_remove_specific_type(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d1", "u1", ReactionType.FIRE)
        assert dr.remove("d1", "u1", ReactionType.HEART) is True
        assert dr.count("d1") == 1

    def test_remove_all_for_user_on_doc(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d1", "u1", ReactionType.FIRE)
        dr.add("d1", "u2", ReactionType.HEART)
        assert dr.remove("d1", "u1") is True
        # u1's entries gone, u2's stays.
        assert dr.count("d1") == 1

    def test_remove_returns_false_when_missing(self):
        dr = DocReaction()
        assert dr.remove("d1", "u1") is False
        assert dr.remove("d1", "u1", ReactionType.HEART) is False

    def test_remove_only_targeted_type(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d1", "u1", ReactionType.FIRE)
        dr.remove("d1", "u1", ReactionType.HEART)
        remaining = dr.reactions_for_doc("d1")
        assert len(remaining) == 1
        assert remaining[0].reaction_type is ReactionType.FIRE


class TestRemoveAllForDoc:
    def test_removes_all(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d1", "u2", ReactionType.FIRE)
        dr.add("d2", "u1", ReactionType.HEART)
        removed = dr.remove_all_for_doc("d1")
        assert removed == 2
        assert dr.total_reactions == 1

    def test_returns_zero_when_unknown_doc(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.HEART)
        assert dr.remove_all_for_doc("d-unknown") == 0
        assert dr.total_reactions == 1


class TestRemoveAllForUser:
    def test_removes_all(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d2", "u1", ReactionType.FIRE)
        dr.add("d1", "u2", ReactionType.HEART)
        removed = dr.remove_all_for_user("u1")
        assert removed == 2
        assert dr.total_reactions == 1

    def test_returns_zero_when_unknown_user(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.HEART)
        assert dr.remove_all_for_user("u-unknown") == 0


# ---------------------------------------------------------------------------
# Lookups
# ---------------------------------------------------------------------------
class TestReactionsForDoc:
    def test_empty(self):
        dr = DocReaction()
        assert dr.reactions_for_doc("d1") == []

    def test_returns_correct_subset(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d2", "u2", ReactionType.FIRE)
        rs = dr.reactions_for_doc("d1")
        assert len(rs) == 1
        assert rs[0].doc_id == "d1"


class TestReactionsByUser:
    def test_empty(self):
        dr = DocReaction()
        assert dr.reactions_by_user("u1") == []

    def test_returns_correct_subset(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d2", "u1", ReactionType.FIRE)
        dr.add("d3", "u2", ReactionType.HEART)
        rs = dr.reactions_by_user("u1")
        assert len(rs) == 2
        assert {r.doc_id for r in rs} == {"d1", "d2"}


class TestSummary:
    def test_empty_doc(self):
        dr = DocReaction()
        s = dr.summary("d-missing")
        assert s.doc_id == "d-missing"
        assert s.counts == {}
        assert s.total == 0
        assert s.top_reaction is None
        assert s.unique_reactors == 0

    def test_aggregates_counts(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d1", "u2", ReactionType.HEART)
        dr.add("d1", "u3", ReactionType.FIRE)
        s = dr.summary("d1")
        assert s.total == 3
        assert s.unique_reactors == 3
        assert s.counts[ReactionType.HEART] == 2
        assert s.counts[ReactionType.FIRE] == 1
        assert s.top_reaction is ReactionType.HEART

    def test_top_reaction_with_single_kind(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.WOW)
        s = dr.summary("d1")
        assert s.top_reaction is ReactionType.WOW


class TestCount:
    def test_total_for_doc(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d1", "u2", ReactionType.FIRE)
        assert dr.count("d1") == 2

    def test_count_by_type(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d1", "u2", ReactionType.HEART)
        dr.add("d1", "u3", ReactionType.FIRE)
        assert dr.count("d1", ReactionType.HEART) == 2
        assert dr.count("d1", ReactionType.FIRE) == 1
        assert dr.count("d1", ReactionType.LAUGH) == 0

    def test_missing_doc_zero(self):
        dr = DocReaction()
        assert dr.count("d-missing") == 0


class TestTopReactions:
    def test_sorted_descending(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d1", "u2", ReactionType.HEART)
        dr.add("d1", "u1", ReactionType.FIRE)
        top = dr.top_reactions("d1", top_k=2)
        assert top[0] == (ReactionType.HEART, 2)
        assert top[1] == (ReactionType.FIRE, 1)

    def test_respects_top_k(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d1", "u1", ReactionType.FIRE)
        dr.add("d1", "u1", ReactionType.LAUGH)
        assert len(dr.top_reactions("d1", top_k=2)) == 2

    def test_top_k_zero(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.HEART)
        assert dr.top_reactions("d1", top_k=0) == []

    def test_no_reactions(self):
        dr = DocReaction()
        assert dr.top_reactions("d1") == []


class TestHasReacted:
    def test_true_any_type(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.HEART)
        assert dr.has_reacted("d1", "u1") is True

    def test_true_specific_type(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.HEART)
        assert dr.has_reacted("d1", "u1", ReactionType.HEART) is True

    def test_false_for_wrong_type(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.HEART)
        assert dr.has_reacted("d1", "u1", ReactionType.FIRE) is False

    def test_false_when_no_reactions(self):
        dr = DocReaction()
        assert dr.has_reacted("d1", "u1") is False


class TestUserActivityQuery:
    def test_returns_none_for_unknown(self):
        dr = DocReaction()
        assert dr.user_activity("u-missing") is None

    def test_aggregates(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART, now=1.0)
        dr.add("d2", "u1", ReactionType.FIRE, now=5.0)
        dr.add("d3", "u1", ReactionType.HEART, now=3.0)
        ua = dr.user_activity("u1")
        assert ua is not None
        assert ua.user_id == "u1"
        assert ua.total_reactions == 3
        assert ua.by_type[ReactionType.HEART] == 2
        assert ua.by_type[ReactionType.FIRE] == 1
        assert ua.last_at == 5.0


class TestMostReactedDocs:
    def test_ordering(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d1", "u2", ReactionType.FIRE)
        dr.add("d2", "u1", ReactionType.HEART)
        dr.add("d3", "u1", ReactionType.HEART)
        dr.add("d3", "u2", ReactionType.HEART)
        dr.add("d3", "u3", ReactionType.HEART)
        top = dr.most_reacted_docs(top_k=2)
        assert top[0] == ("d3", 3)
        assert top[1] == ("d1", 2)

    def test_top_k_zero(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.HEART)
        assert dr.most_reacted_docs(top_k=0) == []

    def test_empty(self):
        dr = DocReaction()
        assert dr.most_reacted_docs() == []


class TestMostActiveUsers:
    def test_ordering(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d2", "u1", ReactionType.FIRE)
        dr.add("d3", "u1", ReactionType.LAUGH)
        dr.add("d1", "u2", ReactionType.HEART)
        top = dr.most_active_users(top_k=2)
        assert top[0] == ("u1", 3)
        assert top[1] == ("u2", 1)

    def test_top_k_zero(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.HEART)
        assert dr.most_active_users(top_k=0) == []

    def test_empty(self):
        dr = DocReaction()
        assert dr.most_active_users() == []


# ---------------------------------------------------------------------------
# Properties
# ---------------------------------------------------------------------------
class TestTotalReactions:
    def test_zero_initially(self):
        assert DocReaction().total_reactions == 0

    def test_grows(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d2", "u2", ReactionType.FIRE)
        assert dr.total_reactions == 2


class TestTotalUniqueDocs:
    def test_zero_initially(self):
        assert DocReaction().total_unique_docs == 0

    def test_counts_distinct(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d1", "u2", ReactionType.FIRE)
        dr.add("d2", "u1", ReactionType.HEART)
        assert dr.total_unique_docs == 2


class TestTotalUniqueUsers:
    def test_zero_initially(self):
        assert DocReaction().total_unique_users == 0

    def test_counts_distinct(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d2", "u1", ReactionType.FIRE)
        dr.add("d1", "u2", ReactionType.HEART)
        assert dr.total_unique_users == 2


class TestClear:
    def test_clear_resets_everything(self):
        dr = DocReaction(unique_per_user=False)
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d2", "u2", ReactionType.FIRE)
        dr.clear()
        assert dr.total_reactions == 0
        assert dr.total_unique_docs == 0
        assert dr.total_unique_users == 0
        assert dr.reactions_for_doc("d1") == []


# ---------------------------------------------------------------------------
# Edge cases & thread safety
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_unique_per_user_default(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d1", "u1", ReactionType.FIRE)
        assert len(dr.reactions_for_doc("d1")) == 1

    def test_summary_after_remove(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d1", "u2", ReactionType.HEART)
        dr.remove("d1", "u1")
        s = dr.summary("d1")
        assert s.total == 1
        assert s.unique_reactors == 1

    def test_user_activity_after_remove_all(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.HEART)
        dr.remove_all_for_user("u1")
        assert dr.user_activity("u1") is None

    def test_thread_safety_concurrent_adds(self):
        dr = DocReaction(unique_per_user=False)

        def worker(uid: int):
            for i in range(20):
                dr.add(f"d{i % 5}", f"u{uid}", ReactionType.HEART, now=float(i))

        threads = [threading.Thread(target=worker, args=(u,)) for u in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # 8 users × 5 distinct docs × 1 type each (deduped per type) = 40.
        assert dr.total_reactions == 8 * 5
        assert dr.total_unique_users == 8
        assert dr.total_unique_docs == 5

    def test_remove_does_not_affect_other_docs(self):
        dr = DocReaction()
        dr.add("d1", "u1", ReactionType.HEART)
        dr.add("d2", "u1", ReactionType.HEART)
        dr.remove("d1", "u1")
        assert dr.has_reacted("d2", "u1") is True

    def test_replacement_preserves_unique_user_count(self):
        dr = DocReaction(unique_per_user=True)
        dr.add("d1", "u1", ReactionType.HEART, now=1.0)
        dr.add("d1", "u1", ReactionType.FIRE, now=2.0)
        s = dr.summary("d1")
        assert s.unique_reactors == 1
        assert s.total == 1
