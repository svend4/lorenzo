"""Tests for docstoolkit.leaderboard."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.leaderboard import Entry, Leaderboard, RankInfo


# ---------------------------------------------------------------------- #
# Dataclasses
# ---------------------------------------------------------------------- #
class TestEntry:
    def test_basic_construction(self):
        e = Entry(entity_id="a", score=1.0)
        assert e.entity_id == "a"
        assert e.score == 1.0
        assert e.metadata == {}
        assert e.updated_at == 0.0

    def test_with_metadata(self):
        e = Entry(entity_id="a", score=2.0, metadata={"team": "blue"})
        assert e.metadata == {"team": "blue"}

    def test_metadata_default_is_unique(self):
        a = Entry(entity_id="a", score=1.0)
        b = Entry(entity_id="b", score=2.0)
        a.metadata["x"] = 1
        assert "x" not in b.metadata

    def test_updated_at(self):
        e = Entry(entity_id="a", score=1.0, updated_at=12.5)
        assert e.updated_at == 12.5


class TestRankInfo:
    def test_construction(self):
        info = RankInfo(entity_id="a", score=5.0, rank=1, percentile=100.0)
        assert info.entity_id == "a"
        assert info.score == 5.0
        assert info.rank == 1
        assert info.percentile == 100.0


# ---------------------------------------------------------------------- #
# Add / Update / Increment / Remove
# ---------------------------------------------------------------------- #
class TestAdd:
    def test_add_returns_entry(self):
        b = Leaderboard()
        e = b.add("alice", 10.0)
        assert isinstance(e, Entry)
        assert e.entity_id == "alice"
        assert e.score == 10.0

    def test_add_persists(self):
        b = Leaderboard()
        b.add("alice", 10.0)
        assert b.get("alice").score == 10.0

    def test_add_with_metadata(self):
        b = Leaderboard()
        b.add("alice", 10.0, metadata={"team": "red"})
        assert b.get("alice").metadata == {"team": "red"}

    def test_add_with_now(self):
        b = Leaderboard()
        b.add("alice", 10.0, now=42.0)
        assert b.get("alice").updated_at == 42.0

    def test_add_overrides_existing(self):
        b = Leaderboard()
        b.add("alice", 1.0)
        b.add("alice", 5.0)
        assert b.get("alice").score == 5.0
        assert b.count == 1

    def test_add_rejects_non_str_id(self):
        b = Leaderboard()
        with pytest.raises(TypeError):
            b.add(123, 1.0)  # type: ignore[arg-type]

    def test_add_coerces_score_to_float(self):
        b = Leaderboard()
        b.add("alice", 7)  # int
        assert isinstance(b.get("alice").score, float)


class TestUpdate:
    def test_update_existing(self):
        b = Leaderboard()
        b.add("alice", 1.0)
        e = b.update("alice", 9.0)
        assert e is not None
        assert e.score == 9.0
        assert b.get("alice").score == 9.0

    def test_update_missing_returns_none(self):
        b = Leaderboard()
        assert b.update("ghost", 1.0) is None

    def test_update_changes_timestamp(self):
        b = Leaderboard()
        b.add("alice", 1.0, now=1.0)
        b.update("alice", 2.0, now=5.0)
        assert b.get("alice").updated_at == 5.0

    def test_update_preserves_metadata(self):
        b = Leaderboard()
        b.add("alice", 1.0, metadata={"team": "red"})
        b.update("alice", 5.0)
        assert b.get("alice").metadata == {"team": "red"}


class TestIncrement:
    def test_increment_existing(self):
        b = Leaderboard()
        b.add("alice", 1.0)
        e = b.increment("alice", 4.0)
        assert e.score == 5.0

    def test_increment_negative(self):
        b = Leaderboard()
        b.add("alice", 10.0)
        b.increment("alice", -3.0)
        assert b.get("alice").score == 7.0

    def test_increment_missing(self):
        b = Leaderboard()
        assert b.increment("ghost", 1.0) is None

    def test_increment_updates_timestamp(self):
        b = Leaderboard()
        b.add("alice", 1.0, now=1.0)
        b.increment("alice", 1.0, now=10.0)
        assert b.get("alice").updated_at == 10.0


class TestRemove:
    def test_remove_existing(self):
        b = Leaderboard()
        b.add("alice", 1.0)
        assert b.remove("alice") is True
        assert b.get("alice") is None

    def test_remove_missing(self):
        b = Leaderboard()
        assert b.remove("ghost") is False

    def test_remove_decrements_count(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 2.0)
        b.remove("a")
        assert b.count == 1


# ---------------------------------------------------------------------- #
# Get / Rank
# ---------------------------------------------------------------------- #
class TestGet:
    def test_get_existing(self):
        b = Leaderboard()
        b.add("alice", 1.0)
        assert b.get("alice").entity_id == "alice"

    def test_get_missing(self):
        b = Leaderboard()
        assert b.get("ghost") is None


class TestRankOf:
    def test_rank_of_top(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 5.0)
        b.add("c", 3.0)
        assert b.rank_of("b") == 1

    def test_rank_of_middle(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 5.0)
        b.add("c", 3.0)
        assert b.rank_of("c") == 2

    def test_rank_of_bottom(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 5.0)
        b.add("c", 3.0)
        assert b.rank_of("a") == 3

    def test_rank_of_missing(self):
        b = Leaderboard()
        b.add("a", 1.0)
        assert b.rank_of("ghost") is None

    def test_rank_is_one_based(self):
        b = Leaderboard()
        b.add("only", 1.0)
        assert b.rank_of("only") == 1


class TestRankInfoMethod:
    def test_rank_info_top_percentile(self):
        b = Leaderboard()
        for i in range(5):
            b.add(f"e{i}", float(i))
        info = b.rank_info("e4")
        assert info.rank == 1
        assert info.percentile == 100.0

    def test_rank_info_bottom_percentile(self):
        b = Leaderboard()
        for i in range(5):
            b.add(f"e{i}", float(i))
        info = b.rank_info("e0")
        assert info.rank == 5
        assert info.percentile == 0.0

    def test_rank_info_single_entry(self):
        b = Leaderboard()
        b.add("only", 7.0)
        info = b.rank_info("only")
        assert info.rank == 1
        assert info.percentile == 100.0

    def test_rank_info_missing(self):
        b = Leaderboard()
        assert b.rank_info("ghost") is None

    def test_rank_info_score(self):
        b = Leaderboard()
        b.add("a", 3.5)
        assert b.rank_info("a").score == 3.5

    def test_rank_info_middle_percentile(self):
        b = Leaderboard()
        for i in range(5):
            b.add(f"e{i}", float(i))
        info = b.rank_info("e2")
        # rank 3 of 5 → (5-3)/(5-1)*100 = 50
        assert info.rank == 3
        assert info.percentile == 50.0


# ---------------------------------------------------------------------- #
# Top N / Bottom N / Range / Around
# ---------------------------------------------------------------------- #
class TestTopN:
    def test_top_n_returns_highest(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 5.0)
        b.add("c", 3.0)
        top = b.top_n(2)
        assert [e.entity_id for e in top] == ["b", "c"]

    def test_top_n_more_than_count(self):
        b = Leaderboard()
        b.add("a", 1.0)
        assert len(b.top_n(10)) == 1

    def test_top_n_zero(self):
        b = Leaderboard()
        b.add("a", 1.0)
        assert b.top_n(0) == []

    def test_top_n_negative(self):
        b = Leaderboard()
        b.add("a", 1.0)
        assert b.top_n(-1) == []

    def test_top_n_empty(self):
        b = Leaderboard()
        assert b.top_n(5) == []


class TestBottomN:
    def test_bottom_n_returns_lowest(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 5.0)
        b.add("c", 3.0)
        bottom = b.bottom_n(2)
        # worst first
        assert [e.entity_id for e in bottom] == ["a", "c"]

    def test_bottom_n_more_than_count(self):
        b = Leaderboard()
        b.add("a", 1.0)
        assert len(b.bottom_n(10)) == 1

    def test_bottom_n_zero(self):
        b = Leaderboard()
        b.add("a", 1.0)
        assert b.bottom_n(0) == []

    def test_bottom_n_empty(self):
        b = Leaderboard()
        assert b.bottom_n(3) == []


class TestRange:
    def test_range_basic(self):
        b = Leaderboard()
        for i, name in enumerate(["a", "b", "c", "d", "e"]):
            b.add(name, float(i))
        # ranks: e(4) d(3) c(2) b(1) a(0)
        r = b.range(2, 4)
        assert [e.entity_id for e in r] == ["d", "c", "b"]

    def test_range_single_rank(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 2.0)
        r = b.range(1, 1)
        assert [e.entity_id for e in r] == ["b"]

    def test_range_clipped_to_count(self):
        b = Leaderboard()
        b.add("a", 1.0)
        r = b.range(1, 10)
        assert len(r) == 1

    def test_range_invalid_returns_empty(self):
        b = Leaderboard()
        b.add("a", 1.0)
        assert b.range(5, 3) == []

    def test_range_start_below_one(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 2.0)
        # 0 should clamp to 1
        r = b.range(0, 2)
        assert len(r) == 2


class TestAround:
    def test_around_middle(self):
        b = Leaderboard()
        for i in range(7):
            b.add(f"e{i}", float(i))
        # ranks: e6 e5 e4 e3 e2 e1 e0
        r = b.around("e3", 1)
        assert [e.entity_id for e in r] == ["e4", "e3", "e2"]

    def test_around_top_clipped(self):
        b = Leaderboard()
        for i in range(5):
            b.add(f"e{i}", float(i))
        r = b.around("e4", 2)
        # top of board, no entries above
        assert r[0].entity_id == "e4"
        assert len(r) == 3

    def test_around_bottom_clipped(self):
        b = Leaderboard()
        for i in range(5):
            b.add(f"e{i}", float(i))
        r = b.around("e0", 2)
        assert r[-1].entity_id == "e0"
        assert len(r) == 3

    def test_around_window_zero(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 2.0)
        r = b.around("a", 0)
        assert [e.entity_id for e in r] == ["a"]

    def test_around_missing(self):
        b = Leaderboard()
        b.add("a", 1.0)
        assert b.around("ghost", 1) == []

    def test_around_negative_window(self):
        b = Leaderboard()
        b.add("a", 1.0)
        assert b.around("a", -1) == []


# ---------------------------------------------------------------------- #
# Score at rank / Entries with score
# ---------------------------------------------------------------------- #
class TestScoreAtRank:
    def test_score_at_rank_basic(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 5.0)
        assert b.score_at_rank(1) == 5.0
        assert b.score_at_rank(2) == 1.0

    def test_score_at_rank_out_of_range(self):
        b = Leaderboard()
        b.add("a", 1.0)
        assert b.score_at_rank(2) is None

    def test_score_at_rank_zero(self):
        b = Leaderboard()
        b.add("a", 1.0)
        assert b.score_at_rank(0) is None

    def test_score_at_rank_negative(self):
        b = Leaderboard()
        b.add("a", 1.0)
        assert b.score_at_rank(-1) is None

    def test_score_at_rank_empty(self):
        b = Leaderboard()
        assert b.score_at_rank(1) is None


class TestEntriesWithScore:
    def test_entries_with_score_basic(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 1.0)
        b.add("c", 2.0)
        ids = sorted(e.entity_id for e in b.entries_with_score(1.0))
        assert ids == ["a", "b"]

    def test_entries_with_score_none_match(self):
        b = Leaderboard()
        b.add("a", 1.0)
        assert b.entries_with_score(99.0) == []

    def test_entries_with_score_empty(self):
        b = Leaderboard()
        assert b.entries_with_score(1.0) == []


# ---------------------------------------------------------------------- #
# Count / Clear / all_entries
# ---------------------------------------------------------------------- #
class TestCount:
    def test_count_empty(self):
        assert Leaderboard().count == 0

    def test_count_after_adds(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 2.0)
        assert b.count == 2

    def test_count_after_remove(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 2.0)
        b.remove("a")
        assert b.count == 1

    def test_len_matches_count(self):
        b = Leaderboard()
        b.add("a", 1.0)
        assert len(b) == 1

    def test_contains(self):
        b = Leaderboard()
        b.add("a", 1.0)
        assert "a" in b
        assert "ghost" not in b


class TestClear:
    def test_clear_empties(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 2.0)
        b.clear()
        assert b.count == 0
        assert b.all_entries() == []

    def test_clear_when_empty(self):
        b = Leaderboard()
        b.clear()
        assert b.count == 0


class TestAllEntries:
    def test_all_entries_sorted(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 5.0)
        b.add("c", 3.0)
        ids = [e.entity_id for e in b.all_entries()]
        assert ids == ["b", "c", "a"]

    def test_all_entries_empty(self):
        assert Leaderboard().all_entries() == []


# ---------------------------------------------------------------------- #
# Ascending mode
# ---------------------------------------------------------------------- #
class TestAscendingMode:
    def test_lower_is_better_top(self):
        b = Leaderboard(higher_is_better=False)
        b.add("fast", 1.0)
        b.add("slow", 9.0)
        b.add("mid", 4.0)
        top = b.top_n(2)
        assert [e.entity_id for e in top] == ["fast", "mid"]

    def test_lower_is_better_rank(self):
        b = Leaderboard(higher_is_better=False)
        b.add("fast", 1.0)
        b.add("slow", 9.0)
        assert b.rank_of("fast") == 1
        assert b.rank_of("slow") == 2

    def test_lower_is_better_percentile(self):
        b = Leaderboard(higher_is_better=False)
        for i in range(5):
            b.add(f"e{i}", float(i))
        # lower is better → e0 should be rank 1 / 100th percentile
        info = b.rank_info("e0")
        assert info.rank == 1
        assert info.percentile == 100.0

    def test_lower_is_better_bottom_n(self):
        b = Leaderboard(higher_is_better=False)
        b.add("fast", 1.0)
        b.add("slow", 9.0)
        b.add("mid", 4.0)
        bottom = b.bottom_n(1)
        assert bottom[0].entity_id == "slow"


# ---------------------------------------------------------------------- #
# Tie-breaking
# ---------------------------------------------------------------------- #
class TestTies:
    def test_ties_broken_alphabetically(self):
        b = Leaderboard()
        b.add("charlie", 5.0)
        b.add("alpha", 5.0)
        b.add("bravo", 5.0)
        ids = [e.entity_id for e in b.all_entries()]
        assert ids == ["alpha", "bravo", "charlie"]

    def test_ties_ranks_distinct(self):
        b = Leaderboard()
        b.add("b", 1.0)
        b.add("a", 1.0)
        assert b.rank_of("a") == 1
        assert b.rank_of("b") == 2

    def test_ties_in_ascending_mode(self):
        b = Leaderboard(higher_is_better=False)
        b.add("b", 1.0)
        b.add("a", 1.0)
        # tiebreak still alphabetical
        ids = [e.entity_id for e in b.all_entries()]
        assert ids == ["a", "b"]


# ---------------------------------------------------------------------- #
# Edge cases
# ---------------------------------------------------------------------- #
class TestEdgeCases:
    def test_empty_board_top_n(self):
        assert Leaderboard().top_n(5) == []

    def test_empty_board_all_entries(self):
        assert Leaderboard().all_entries() == []

    def test_empty_board_rank_info(self):
        assert Leaderboard().rank_info("x") is None

    def test_single_entry_top_n(self):
        b = Leaderboard()
        b.add("solo", 1.0)
        top = b.top_n(5)
        assert len(top) == 1
        assert top[0].entity_id == "solo"

    def test_single_entry_around(self):
        b = Leaderboard()
        b.add("solo", 1.0)
        assert [e.entity_id for e in b.around("solo", 3)] == ["solo"]

    def test_n_greater_than_count_top(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 2.0)
        assert len(b.top_n(100)) == 2

    def test_n_greater_than_count_bottom(self):
        b = Leaderboard()
        b.add("a", 1.0)
        b.add("b", 2.0)
        assert len(b.bottom_n(100)) == 2

    def test_negative_scores(self):
        b = Leaderboard()
        b.add("a", -5.0)
        b.add("b", -1.0)
        b.add("c", -10.0)
        assert b.rank_of("b") == 1
        assert b.rank_of("c") == 3

    def test_float_scores(self):
        b = Leaderboard()
        b.add("a", 1.5)
        b.add("b", 1.51)
        assert b.rank_of("b") == 1

    def test_thread_safety_concurrent_adds(self):
        b = Leaderboard()

        def worker(start: int):
            for i in range(50):
                b.add(f"e{start}_{i}", float(i))

        threads = [threading.Thread(target=worker, args=(k,)) for k in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert b.count == 4 * 50

    def test_metadata_is_copied_not_aliased(self):
        b = Leaderboard()
        meta = {"k": "v"}
        b.add("a", 1.0, metadata=meta)
        meta["k"] = "modified"
        assert b.get("a").metadata["k"] == "v"
