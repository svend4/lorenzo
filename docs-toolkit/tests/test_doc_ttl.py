"""Tests for docstoolkit.doc_ttl."""

from __future__ import annotations

import pytest

from docstoolkit.doc_ttl import DocTtl, ExpiryMode, TtlEntry, TtlStats


# --------------------------------------------------------------------------- #
# Enum and dataclasses
# --------------------------------------------------------------------------- #
class TestExpiryMode:
    def test_has_fixed(self):
        assert ExpiryMode.FIXED.value == "fixed"

    def test_has_sliding(self):
        assert ExpiryMode.SLIDING.value == "sliding"

    def test_distinct(self):
        assert ExpiryMode.FIXED != ExpiryMode.SLIDING


class TestTtlEntry:
    def test_create_minimal(self):
        e = TtlEntry(
            doc_id="d1",
            created_at=0.0,
            expires_at=10.0,
            last_accessed=0.0,
        )
        assert e.doc_id == "d1"
        assert e.mode == ExpiryMode.FIXED
        assert e.ttl == 0.0

    def test_create_full(self):
        e = TtlEntry(
            doc_id="d1",
            created_at=1.0,
            expires_at=11.0,
            last_accessed=1.0,
            mode=ExpiryMode.SLIDING,
            ttl=10.0,
        )
        assert e.mode == ExpiryMode.SLIDING
        assert e.ttl == 10.0


class TestTtlStats:
    def test_defaults(self):
        s = TtlStats(total=0, active=0, expired=0)
        assert s.by_mode == {}
        assert s.expiring_soon == 0

    def test_explicit(self):
        s = TtlStats(
            total=5,
            active=3,
            expired=2,
            by_mode={"fixed": 4, "sliding": 1},
            expiring_soon=1,
        )
        assert s.total == 5
        assert s.by_mode["fixed"] == 4


# --------------------------------------------------------------------------- #
# Add
# --------------------------------------------------------------------------- #
class TestAdd:
    def test_add_with_default_ttl(self):
        m = DocTtl(default_ttl=100.0)
        e = m.add("d1", now=0.0)
        assert e.ttl == 100.0
        assert e.expires_at == 100.0

    def test_add_custom_ttl(self):
        m = DocTtl()
        e = m.add("d1", ttl=50.0, now=10.0)
        assert e.ttl == 50.0
        assert e.expires_at == 60.0

    def test_add_fixed_mode(self):
        m = DocTtl()
        e = m.add("d1", ttl=10.0, mode=ExpiryMode.FIXED, now=0.0)
        assert e.mode == ExpiryMode.FIXED

    def test_add_sliding_mode(self):
        m = DocTtl()
        e = m.add("d1", ttl=10.0, mode=ExpiryMode.SLIDING, now=0.0)
        assert e.mode == ExpiryMode.SLIDING

    def test_add_records_created_at(self):
        m = DocTtl()
        e = m.add("d1", ttl=10.0, now=5.5)
        assert e.created_at == 5.5

    def test_add_records_last_accessed(self):
        m = DocTtl()
        e = m.add("d1", ttl=10.0, now=2.0)
        assert e.last_accessed == 2.0

    def test_add_increments_total(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        m.add("d2", ttl=10.0, now=0.0)
        assert m.total_entries == 2

    def test_add_replaces_existing(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        e = m.add("d1", ttl=20.0, now=5.0)
        assert e.ttl == 20.0
        assert e.created_at == 5.0
        assert m.total_entries == 1


# --------------------------------------------------------------------------- #
# Remove
# --------------------------------------------------------------------------- #
class TestRemove:
    def test_remove_existing(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        assert m.remove("d1") is True
        assert m.total_entries == 0

    def test_remove_missing(self):
        m = DocTtl()
        assert m.remove("missing") is False


# --------------------------------------------------------------------------- #
# Get
# --------------------------------------------------------------------------- #
class TestGet:
    def test_get_returns_entry(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        assert m.get("d1", now=5.0) is not None

    def test_get_missing(self):
        m = DocTtl()
        assert m.get("missing", now=0.0) is None

    def test_get_expired_returns_none(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        assert m.get("d1", now=11.0) is None

    def test_get_does_not_remove_expired(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        m.get("d1", now=15.0)
        assert m.total_entries == 1

    def test_get_updates_last_accessed(self):
        m = DocTtl()
        m.add("d1", ttl=100.0, now=0.0)
        m.get("d1", now=5.0)
        entry = m.peek("d1")
        assert entry.last_accessed == 5.0


# --------------------------------------------------------------------------- #
# Peek
# --------------------------------------------------------------------------- #
class TestPeek:
    def test_peek_returns_active(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        assert m.peek("d1") is not None

    def test_peek_returns_expired(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        # Even with extreme time, peek ignores expiry
        e = m.peek("d1")
        assert e is not None
        assert e.expires_at == 10.0

    def test_peek_missing(self):
        m = DocTtl()
        assert m.peek("missing") is None

    def test_peek_does_not_update_last_accessed(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        e1 = m.peek("d1")
        last_before = e1.last_accessed
        m.peek("d1")
        e2 = m.peek("d1")
        assert e2.last_accessed == last_before


# --------------------------------------------------------------------------- #
# is_expired
# --------------------------------------------------------------------------- #
class TestIsExpired:
    def test_alive_entry_not_expired(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        assert m.is_expired("d1", now=5.0) is False

    def test_expired_entry(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        assert m.is_expired("d1", now=20.0) is True

    def test_at_boundary_expired(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        assert m.is_expired("d1", now=10.0) is True

    def test_missing_is_expired(self):
        m = DocTtl()
        assert m.is_expired("missing", now=0.0) is True


# --------------------------------------------------------------------------- #
# is_alive
# --------------------------------------------------------------------------- #
class TestIsAlive:
    def test_alive_entry(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        assert m.is_alive("d1", now=5.0) is True

    def test_expired_entry(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        assert m.is_alive("d1", now=15.0) is False

    def test_missing(self):
        m = DocTtl()
        assert m.is_alive("missing", now=0.0) is False


# --------------------------------------------------------------------------- #
# time_left
# --------------------------------------------------------------------------- #
class TestTimeLeft:
    def test_positive_when_active(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        assert m.time_left("d1", now=3.0) == 7.0

    def test_zero_at_boundary(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        assert m.time_left("d1", now=10.0) == 0.0

    def test_negative_after_expiry(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        assert m.time_left("d1", now=15.0) == -5.0

    def test_none_for_missing(self):
        m = DocTtl()
        assert m.time_left("missing", now=0.0) is None


# --------------------------------------------------------------------------- #
# extend
# --------------------------------------------------------------------------- #
class TestExtend:
    def test_extend_existing(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        assert m.extend("d1", additional_ttl=5.0, now=2.0) is True
        assert m.peek("d1").expires_at == 15.0

    def test_extend_missing(self):
        m = DocTtl()
        assert m.extend("missing", additional_ttl=5.0, now=0.0) is False

    def test_extend_revives_expired(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        # expires at 10, current now=15, add 100 -> 110
        m.extend("d1", additional_ttl=100.0, now=15.0)
        assert m.is_alive("d1", now=15.0) is True

    def test_extend_updates_last_accessed(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        m.extend("d1", additional_ttl=5.0, now=3.0)
        assert m.peek("d1").last_accessed == 3.0


# --------------------------------------------------------------------------- #
# refresh
# --------------------------------------------------------------------------- #
class TestRefresh:
    def test_refresh_resets_expiry(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        m.refresh("d1", now=5.0)
        assert m.peek("d1").expires_at == 15.0

    def test_refresh_missing(self):
        m = DocTtl()
        assert m.refresh("missing", now=0.0) is False

    def test_refresh_uses_original_ttl(self):
        m = DocTtl()
        m.add("d1", ttl=30.0, now=0.0)
        m.refresh("d1", now=100.0)
        assert m.peek("d1").expires_at == 130.0

    def test_refresh_updates_last_accessed(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        m.refresh("d1", now=4.0)
        assert m.peek("d1").last_accessed == 4.0


# --------------------------------------------------------------------------- #
# touch — FIXED
# --------------------------------------------------------------------------- #
class TestTouchFixed:
    def test_touch_updates_last_accessed(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, mode=ExpiryMode.FIXED, now=0.0)
        m.touch("d1", now=3.0)
        assert m.peek("d1").last_accessed == 3.0

    def test_touch_does_not_extend_expiry(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, mode=ExpiryMode.FIXED, now=0.0)
        m.touch("d1", now=5.0)
        assert m.peek("d1").expires_at == 10.0

    def test_touch_missing(self):
        m = DocTtl()
        assert m.touch("missing", now=0.0) is False


# --------------------------------------------------------------------------- #
# touch — SLIDING
# --------------------------------------------------------------------------- #
class TestTouchSliding:
    def test_touch_extends_expiry(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, mode=ExpiryMode.SLIDING, now=0.0)
        m.touch("d1", now=5.0)
        assert m.peek("d1").expires_at == 15.0

    def test_touch_updates_last_accessed(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, mode=ExpiryMode.SLIDING, now=0.0)
        m.touch("d1", now=4.0)
        assert m.peek("d1").last_accessed == 4.0

    def test_repeated_touch_keeps_alive(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, mode=ExpiryMode.SLIDING, now=0.0)
        m.touch("d1", now=5.0)
        m.touch("d1", now=10.0)
        m.touch("d1", now=15.0)
        assert m.is_alive("d1", now=20.0) is True

    def test_no_touch_eventually_expires(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, mode=ExpiryMode.SLIDING, now=0.0)
        assert m.is_expired("d1", now=11.0) is True


# --------------------------------------------------------------------------- #
# expired_doc_ids
# --------------------------------------------------------------------------- #
class TestExpiredDocIds:
    def test_empty(self):
        m = DocTtl()
        assert m.expired_doc_ids(now=0.0) == []

    def test_some_expired(self):
        m = DocTtl()
        m.add("d1", ttl=5.0, now=0.0)
        m.add("d2", ttl=20.0, now=0.0)
        assert m.expired_doc_ids(now=10.0) == ["d1"]

    def test_all_expired(self):
        m = DocTtl()
        m.add("d1", ttl=5.0, now=0.0)
        m.add("d2", ttl=10.0, now=0.0)
        assert sorted(m.expired_doc_ids(now=20.0)) == ["d1", "d2"]


# --------------------------------------------------------------------------- #
# active_doc_ids
# --------------------------------------------------------------------------- #
class TestActiveDocIds:
    def test_empty(self):
        m = DocTtl()
        assert m.active_doc_ids(now=0.0) == []

    def test_some_active(self):
        m = DocTtl()
        m.add("d1", ttl=5.0, now=0.0)
        m.add("d2", ttl=20.0, now=0.0)
        assert m.active_doc_ids(now=10.0) == ["d2"]

    def test_all_active(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        m.add("d2", ttl=10.0, now=0.0)
        assert sorted(m.active_doc_ids(now=5.0)) == ["d1", "d2"]


# --------------------------------------------------------------------------- #
# expiring_within
# --------------------------------------------------------------------------- #
class TestExpiringWithin:
    def test_empty(self):
        m = DocTtl()
        assert m.expiring_within(seconds=10.0, now=0.0) == []

    def test_returns_only_soon(self):
        m = DocTtl()
        m.add("d1", ttl=5.0, now=0.0)
        m.add("d2", ttl=100.0, now=0.0)
        assert m.expiring_within(seconds=10.0, now=0.0) == ["d1"]

    def test_excludes_already_expired(self):
        m = DocTtl()
        m.add("d1", ttl=5.0, now=0.0)
        # already expired (now=10, expires_at=5)
        assert m.expiring_within(seconds=10.0, now=10.0) == []

    def test_includes_at_threshold(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        assert "d1" in m.expiring_within(seconds=10.0, now=0.0)


# --------------------------------------------------------------------------- #
# cleanup_expired
# --------------------------------------------------------------------------- #
class TestCleanupExpired:
    def test_empty_returns_zero(self):
        m = DocTtl()
        assert m.cleanup_expired(now=0.0) == 0

    def test_removes_expired_only(self):
        m = DocTtl()
        m.add("d1", ttl=5.0, now=0.0)
        m.add("d2", ttl=20.0, now=0.0)
        removed = m.cleanup_expired(now=10.0)
        assert removed == 1
        assert m.peek("d1") is None
        assert m.peek("d2") is not None

    def test_removes_all_when_all_expired(self):
        m = DocTtl()
        m.add("d1", ttl=5.0, now=0.0)
        m.add("d2", ttl=10.0, now=0.0)
        assert m.cleanup_expired(now=100.0) == 2
        assert m.total_entries == 0


# --------------------------------------------------------------------------- #
# set_default_ttl
# --------------------------------------------------------------------------- #
class TestSetDefaultTtl:
    def test_update(self):
        m = DocTtl(default_ttl=10.0)
        m.set_default_ttl(50.0)
        e = m.add("d1", now=0.0)
        assert e.ttl == 50.0

    def test_does_not_affect_existing(self):
        m = DocTtl(default_ttl=10.0)
        m.add("d1", now=0.0)
        m.set_default_ttl(100.0)
        assert m.peek("d1").ttl == 10.0


# --------------------------------------------------------------------------- #
# stats
# --------------------------------------------------------------------------- #
class TestStats:
    def test_empty(self):
        m = DocTtl()
        s = m.stats(now=0.0)
        assert s.total == 0
        assert s.active == 0
        assert s.expired == 0
        assert s.by_mode == {}

    def test_counts_active_and_expired(self):
        m = DocTtl()
        m.add("d1", ttl=5.0, now=0.0)
        m.add("d2", ttl=100.0, now=0.0)
        s = m.stats(now=10.0)
        assert s.total == 2
        assert s.active == 1
        assert s.expired == 1

    def test_by_mode(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, mode=ExpiryMode.FIXED, now=0.0)
        m.add("d2", ttl=10.0, mode=ExpiryMode.SLIDING, now=0.0)
        m.add("d3", ttl=10.0, mode=ExpiryMode.FIXED, now=0.0)
        s = m.stats(now=0.0)
        assert s.by_mode["fixed"] == 2
        assert s.by_mode["sliding"] == 1

    def test_expiring_soon(self):
        m = DocTtl()
        m.add("d1", ttl=100.0, now=0.0)
        m.add("d2", ttl=1000.0, now=0.0)
        s = m.stats(now=0.0, expiring_soon_window=200.0)
        assert s.expiring_soon == 1


# --------------------------------------------------------------------------- #
# count_active
# --------------------------------------------------------------------------- #
class TestCountActive:
    def test_zero_empty(self):
        m = DocTtl()
        assert m.count_active(now=0.0) == 0

    def test_count(self):
        m = DocTtl()
        m.add("d1", ttl=5.0, now=0.0)
        m.add("d2", ttl=20.0, now=0.0)
        assert m.count_active(now=10.0) == 1


# --------------------------------------------------------------------------- #
# total_entries
# --------------------------------------------------------------------------- #
class TestTotalEntries:
    def test_zero(self):
        m = DocTtl()
        assert m.total_entries == 0

    def test_includes_expired(self):
        m = DocTtl()
        m.add("d1", ttl=5.0, now=0.0)
        m.add("d2", ttl=20.0, now=0.0)
        assert m.total_entries == 2


# --------------------------------------------------------------------------- #
# clear
# --------------------------------------------------------------------------- #
class TestClear:
    def test_clear_removes_all(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=0.0)
        m.add("d2", ttl=10.0, now=0.0)
        m.clear()
        assert m.total_entries == 0

    def test_clear_empty(self):
        m = DocTtl()
        m.clear()
        assert m.total_entries == 0


# --------------------------------------------------------------------------- #
# Edge cases
# --------------------------------------------------------------------------- #
class TestEdgeCases:
    def test_zero_ttl_immediately_expired(self):
        m = DocTtl()
        m.add("d1", ttl=0.0, now=0.0)
        assert m.is_expired("d1", now=0.0) is True

    def test_negative_now_works(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, now=-100.0)
        assert m.is_alive("d1", now=-95.0) is True

    def test_sliding_refresh_uses_original_ttl(self):
        m = DocTtl()
        m.add("d1", ttl=20.0, mode=ExpiryMode.SLIDING, now=0.0)
        m.touch("d1", now=5.0)
        assert m.peek("d1").expires_at == 25.0

    def test_get_after_touch_sliding(self):
        m = DocTtl()
        m.add("d1", ttl=10.0, mode=ExpiryMode.SLIDING, now=0.0)
        m.touch("d1", now=8.0)
        assert m.get("d1", now=12.0) is not None

    def test_large_number_of_entries(self):
        m = DocTtl()
        for i in range(500):
            m.add(f"d{i}", ttl=10.0, now=0.0)
        assert m.total_entries == 500
        assert m.count_active(now=5.0) == 500
        assert m.cleanup_expired(now=100.0) == 500
