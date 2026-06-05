"""Tests for E374 DocTagBlacklist."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_tag_blacklist import (
    BlacklistEntry,
    BlacklistStats,
    DocTagBlacklist,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestBlacklistEntryDataclass:
    def test_minimal_construction(self):
        entry = BlacklistEntry(pattern="foo")
        assert entry.pattern == "foo"
        assert entry.reason == ""
        assert entry.added_at == 0.0
        assert entry.added_by == ""
        assert entry.case_sensitive is True

    def test_full_construction(self):
        entry = BlacklistEntry(
            pattern="bar*",
            reason="deprecated",
            added_at=123.5,
            added_by="alice",
            case_sensitive=False,
        )
        assert entry.pattern == "bar*"
        assert entry.reason == "deprecated"
        assert entry.added_at == 123.5
        assert entry.added_by == "alice"
        assert entry.case_sensitive is False

    def test_equality(self):
        a = BlacklistEntry(pattern="x", reason="r", added_at=1.0)
        b = BlacklistEntry(pattern="x", reason="r", added_at=1.0)
        assert a == b

    def test_inequality(self):
        a = BlacklistEntry(pattern="x")
        b = BlacklistEntry(pattern="y")
        assert a != b


class TestBlacklistStatsDataclass:
    def test_construction(self):
        s = BlacklistStats(
            total_entries=10,
            exact_count=6,
            pattern_count=4,
            case_insensitive_count=2,
        )
        assert s.total_entries == 10
        assert s.exact_count == 6
        assert s.pattern_count == 4
        assert s.case_insensitive_count == 2

    def test_equality(self):
        a = BlacklistStats(total_entries=1, exact_count=1, pattern_count=0, case_insensitive_count=0)
        b = BlacklistStats(total_entries=1, exact_count=1, pattern_count=0, case_insensitive_count=0)
        assert a == b

    def test_zero_stats(self):
        s = BlacklistStats(total_entries=0, exact_count=0, pattern_count=0, case_insensitive_count=0)
        assert s.total_entries == 0


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_on_init(self):
        bl = DocTagBlacklist()
        assert bl.list_entries() == []

    def test_stats_empty(self):
        bl = DocTagBlacklist()
        s = bl.stats()
        assert s.total_entries == 0
        assert s.exact_count == 0
        assert s.pattern_count == 0
        assert s.case_insensitive_count == 0

    def test_independent_instances(self):
        a = DocTagBlacklist()
        b = DocTagBlacklist()
        a.add("foo")
        assert b.list_entries() == []


# ---------------------------------------------------------------------------
# Add
# ---------------------------------------------------------------------------


class TestAdd:
    def test_add_new_returns_entry(self):
        bl = DocTagBlacklist()
        entry = bl.add("foo")
        assert isinstance(entry, BlacklistEntry)
        assert entry.pattern == "foo"

    def test_add_stores_entry(self):
        bl = DocTagBlacklist()
        bl.add("foo")
        assert bl.get("foo") is not None

    def test_add_with_reason(self):
        bl = DocTagBlacklist()
        entry = bl.add("foo", reason="bad word")
        assert entry.reason == "bad word"

    def test_add_with_added_by(self):
        bl = DocTagBlacklist()
        entry = bl.add("foo", added_by="bob")
        assert entry.added_by == "bob"

    def test_add_with_case_sensitive_false(self):
        bl = DocTagBlacklist()
        entry = bl.add("Foo", case_sensitive=False)
        assert entry.case_sensitive is False

    def test_add_with_now(self):
        bl = DocTagBlacklist()
        entry = bl.add("foo", now=555.0)
        assert entry.added_at == 555.0

    def test_add_default_now_set(self):
        bl = DocTagBlacklist()
        entry = bl.add("foo")
        assert entry.added_at > 0

    def test_add_replace(self):
        bl = DocTagBlacklist()
        bl.add("foo", reason="r1", now=1.0)
        bl.add("foo", reason="r2", now=2.0)
        entry = bl.get("foo")
        assert entry.reason == "r2"
        assert entry.added_at == 2.0

    def test_add_replace_keeps_one_entry(self):
        bl = DocTagBlacklist()
        bl.add("foo")
        bl.add("foo")
        assert len(bl.list_entries()) == 1


# ---------------------------------------------------------------------------
# Remove
# ---------------------------------------------------------------------------


class TestRemove:
    def test_remove_existing_returns_true(self):
        bl = DocTagBlacklist()
        bl.add("foo")
        assert bl.remove("foo") is True

    def test_remove_missing_returns_false(self):
        bl = DocTagBlacklist()
        assert bl.remove("nonexistent") is False

    def test_remove_deletes_entry(self):
        bl = DocTagBlacklist()
        bl.add("foo")
        bl.remove("foo")
        assert bl.get("foo") is None

    def test_remove_twice(self):
        bl = DocTagBlacklist()
        bl.add("foo")
        assert bl.remove("foo") is True
        assert bl.remove("foo") is False


# ---------------------------------------------------------------------------
# is_blacklisted
# ---------------------------------------------------------------------------


class TestIsBlacklisted:
    def test_exact_match(self):
        bl = DocTagBlacklist()
        bl.add("internal")
        assert bl.is_blacklisted("internal") is True

    def test_exact_no_match(self):
        bl = DocTagBlacklist()
        bl.add("internal")
        assert bl.is_blacklisted("public") is False

    def test_empty_blacklist(self):
        bl = DocTagBlacklist()
        assert bl.is_blacklisted("anything") is False

    def test_wildcard_star(self):
        bl = DocTagBlacklist()
        bl.add("draft-*")
        assert bl.is_blacklisted("draft-1") is True
        assert bl.is_blacklisted("draft-final") is True

    def test_wildcard_star_no_match(self):
        bl = DocTagBlacklist()
        bl.add("draft-*")
        assert bl.is_blacklisted("final") is False

    def test_wildcard_question(self):
        bl = DocTagBlacklist()
        bl.add("v?")
        assert bl.is_blacklisted("v1") is True
        assert bl.is_blacklisted("v2") is True
        assert bl.is_blacklisted("v10") is False

    def test_wildcard_bracket(self):
        bl = DocTagBlacklist()
        bl.add("tag[12]")
        assert bl.is_blacklisted("tag1") is True
        assert bl.is_blacklisted("tag2") is True
        assert bl.is_blacklisted("tag3") is False

    def test_case_sensitive_default(self):
        bl = DocTagBlacklist()
        bl.add("Foo")
        assert bl.is_blacklisted("Foo") is True
        assert bl.is_blacklisted("foo") is False

    def test_case_insensitive(self):
        bl = DocTagBlacklist()
        bl.add("Foo", case_sensitive=False)
        assert bl.is_blacklisted("foo") is True
        assert bl.is_blacklisted("FOO") is True
        assert bl.is_blacklisted("Foo") is True

    def test_case_insensitive_wildcard(self):
        bl = DocTagBlacklist()
        bl.add("Draft-*", case_sensitive=False)
        assert bl.is_blacklisted("draft-1") is True
        assert bl.is_blacklisted("DRAFT-2") is True


# ---------------------------------------------------------------------------
# matching_patterns
# ---------------------------------------------------------------------------


class TestMatchingPatterns:
    def test_no_match_empty_list(self):
        bl = DocTagBlacklist()
        bl.add("foo")
        assert bl.matching_patterns("bar") == []

    def test_single_match(self):
        bl = DocTagBlacklist()
        bl.add("foo")
        assert bl.matching_patterns("foo") == ["foo"]

    def test_multiple_matches_sorted(self):
        bl = DocTagBlacklist()
        bl.add("zzz-*")
        bl.add("aaa-*")
        bl.add("*-temp")
        result = bl.matching_patterns("aaa-temp")
        assert result == sorted(result)
        assert "aaa-*" in result
        assert "*-temp" in result

    def test_returns_sorted(self):
        bl = DocTagBlacklist()
        bl.add("z*")
        bl.add("*z")
        result = bl.matching_patterns("zzz")
        assert result == ["*z", "z*"]


# ---------------------------------------------------------------------------
# filter_tags
# ---------------------------------------------------------------------------


class TestFilterTags:
    def test_empty_tags(self):
        bl = DocTagBlacklist()
        allowed, blocked = bl.filter_tags([])
        assert allowed == []
        assert blocked == []

    def test_all_allowed(self):
        bl = DocTagBlacklist()
        bl.add("internal")
        allowed, blocked = bl.filter_tags(["public", "open"])
        assert allowed == ["open", "public"]
        assert blocked == []

    def test_all_blocked(self):
        bl = DocTagBlacklist()
        bl.add("*")
        allowed, blocked = bl.filter_tags(["a", "b"])
        assert allowed == []
        assert blocked == ["a", "b"]

    def test_mixed(self):
        bl = DocTagBlacklist()
        bl.add("draft-*")
        allowed, blocked = bl.filter_tags(["draft-1", "final", "draft-2", "public"])
        assert allowed == ["final", "public"]
        assert blocked == ["draft-1", "draft-2"]

    def test_returns_tuple(self):
        bl = DocTagBlacklist()
        result = bl.filter_tags(["a"])
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_sorted_output(self):
        bl = DocTagBlacklist()
        bl.add("bad-*")
        allowed, blocked = bl.filter_tags(["z", "a", "m", "bad-z", "bad-a"])
        assert allowed == ["a", "m", "z"]
        assert blocked == ["bad-a", "bad-z"]


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


class TestGet:
    def test_get_found(self):
        bl = DocTagBlacklist()
        bl.add("foo", reason="x")
        entry = bl.get("foo")
        assert entry is not None
        assert entry.pattern == "foo"
        assert entry.reason == "x"

    def test_get_not_found(self):
        bl = DocTagBlacklist()
        assert bl.get("missing") is None

    def test_get_after_remove(self):
        bl = DocTagBlacklist()
        bl.add("foo")
        bl.remove("foo")
        assert bl.get("foo") is None


# ---------------------------------------------------------------------------
# list_entries
# ---------------------------------------------------------------------------


class TestListEntries:
    def test_empty(self):
        bl = DocTagBlacklist()
        assert bl.list_entries() == []

    def test_single(self):
        bl = DocTagBlacklist()
        bl.add("foo")
        entries = bl.list_entries()
        assert len(entries) == 1
        assert entries[0].pattern == "foo"

    def test_sorted_by_pattern(self):
        bl = DocTagBlacklist()
        bl.add("zzz")
        bl.add("aaa")
        bl.add("mmm")
        entries = bl.list_entries()
        assert [e.pattern for e in entries] == ["aaa", "mmm", "zzz"]

    def test_returns_list(self):
        bl = DocTagBlacklist()
        bl.add("foo")
        assert isinstance(bl.list_entries(), list)


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_clear_empty(self):
        bl = DocTagBlacklist()
        assert bl.clear() == 0

    def test_clear_returns_count(self):
        bl = DocTagBlacklist()
        bl.add("a")
        bl.add("b")
        bl.add("c")
        assert bl.clear() == 3

    def test_clear_removes_all(self):
        bl = DocTagBlacklist()
        bl.add("a")
        bl.add("b")
        bl.clear()
        assert bl.list_entries() == []

    def test_clear_idempotent_second(self):
        bl = DocTagBlacklist()
        bl.add("a")
        bl.clear()
        assert bl.clear() == 0


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty_stats(self):
        bl = DocTagBlacklist()
        s = bl.stats()
        assert s.total_entries == 0

    def test_exact_count(self):
        bl = DocTagBlacklist()
        bl.add("foo")
        bl.add("bar")
        s = bl.stats()
        assert s.exact_count == 2
        assert s.pattern_count == 0

    def test_pattern_count_star(self):
        bl = DocTagBlacklist()
        bl.add("foo-*")
        s = bl.stats()
        assert s.pattern_count == 1
        assert s.exact_count == 0

    def test_pattern_count_question(self):
        bl = DocTagBlacklist()
        bl.add("v?")
        s = bl.stats()
        assert s.pattern_count == 1

    def test_pattern_count_bracket(self):
        bl = DocTagBlacklist()
        bl.add("t[12]")
        s = bl.stats()
        assert s.pattern_count == 1

    def test_mixed_counts(self):
        bl = DocTagBlacklist()
        bl.add("foo")
        bl.add("bar-*")
        bl.add("baz")
        s = bl.stats()
        assert s.total_entries == 3
        assert s.exact_count == 2
        assert s.pattern_count == 1

    def test_case_insensitive_count(self):
        bl = DocTagBlacklist()
        bl.add("a", case_sensitive=False)
        bl.add("b", case_sensitive=False)
        bl.add("c", case_sensitive=True)
        s = bl.stats()
        assert s.case_insensitive_count == 2

    def test_total_matches_list_entries(self):
        bl = DocTagBlacklist()
        for p in ["a", "b", "c*", "d?"]:
            bl.add(p)
        s = bl.stats()
        assert s.total_entries == len(bl.list_entries())


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_add(self):
        bl = DocTagBlacklist()
        n_threads = 10
        per_thread = 50

        def worker(tid: int) -> None:
            for i in range(per_thread):
                bl.add(f"t{tid}-{i}")

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert len(bl.list_entries()) == n_threads * per_thread

    def test_concurrent_add_and_remove(self):
        bl = DocTagBlacklist()
        for i in range(100):
            bl.add(f"x{i}")

        def adder() -> None:
            for i in range(100):
                bl.add(f"a{i}")

        def remover() -> None:
            for i in range(100):
                bl.remove(f"x{i}")

        ta = threading.Thread(target=adder)
        tr = threading.Thread(target=remover)
        ta.start()
        tr.start()
        ta.join()
        tr.join()

        # All 'a*' entries should be present, all 'x*' gone
        entries = {e.pattern for e in bl.list_entries()}
        for i in range(100):
            assert f"a{i}" in entries
            assert f"x{i}" not in entries

    def test_concurrent_reads(self):
        bl = DocTagBlacklist()
        for i in range(50):
            bl.add(f"p{i}")

        results: list[int] = []
        lock = threading.Lock()

        def reader() -> None:
            for _ in range(20):
                entries = bl.list_entries()
                with lock:
                    results.append(len(entries))

        threads = [threading.Thread(target=reader) for _ in range(8)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert all(r == 50 for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
