"""Tests for the E82 API rate quota module."""
import math
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.rate_quota import (
    QuotaDefinition,
    QuotaExceeded,
    QuotaManager,
    QuotaPeriod,
    QuotaStore,
    QuotaUsage,
)


# ---------- Fixtures -------------------------------------------------------- #
@pytest.fixture
def store(tmp_path):
    s = QuotaStore(db_path=str(tmp_path / "q.sqlite"))
    yield s
    s.close()


@pytest.fixture
def mem_store():
    s = QuotaStore()
    yield s
    s.close()


@pytest.fixture
def mgr(mem_store):
    return QuotaManager(store=mem_store)


# ============================================================================ #
# QuotaPeriod enum
# ============================================================================ #
def test_quota_period_second_value():
    assert QuotaPeriod.SECOND.value == 1


def test_quota_period_minute_value():
    assert QuotaPeriod.MINUTE.value == 60


def test_quota_period_hour_value():
    assert QuotaPeriod.HOUR.value == 3600


def test_quota_period_day_value():
    assert QuotaPeriod.DAY.value == 86400


def test_quota_period_members():
    names = {m.name for m in QuotaPeriod}
    assert names == {"SECOND", "MINUTE", "HOUR", "DAY"}


def test_quota_period_count():
    assert len(list(QuotaPeriod)) == 4


def test_quota_period_lookup_by_name():
    assert QuotaPeriod["MINUTE"] is QuotaPeriod.MINUTE


def test_quota_period_lookup_by_value():
    assert QuotaPeriod(3600) is QuotaPeriod.HOUR


def test_quota_period_identity():
    assert QuotaPeriod.DAY is QuotaPeriod.DAY


def test_quota_period_distinct():
    assert QuotaPeriod.SECOND is not QuotaPeriod.MINUTE


# ============================================================================ #
# QuotaDefinition dataclass
# ============================================================================ #
def test_quota_definition_basic_fields():
    qd = QuotaDefinition(key="api", limit=100, period=QuotaPeriod.MINUTE)
    assert qd.key == "api"
    assert qd.limit == 100
    assert qd.period is QuotaPeriod.MINUTE
    assert qd.description == ""


def test_quota_definition_with_description():
    qd = QuotaDefinition(
        key="api", limit=10, period=QuotaPeriod.SECOND, description="hello"
    )
    assert qd.description == "hello"


def test_quota_definition_equality():
    a = QuotaDefinition(key="x", limit=5, period=QuotaPeriod.HOUR)
    b = QuotaDefinition(key="x", limit=5, period=QuotaPeriod.HOUR)
    assert a == b


def test_quota_definition_inequality():
    a = QuotaDefinition(key="x", limit=5, period=QuotaPeriod.HOUR)
    b = QuotaDefinition(key="y", limit=5, period=QuotaPeriod.HOUR)
    assert a != b


def test_quota_definition_kwargs_order():
    qd = QuotaDefinition(period=QuotaPeriod.DAY, key="k", limit=1)
    assert qd.key == "k"


# ============================================================================ #
# QuotaUsage dataclass and remaining property
# ============================================================================ #
def test_quota_usage_fields():
    u = QuotaUsage(
        key="api", count=2, limit=10, period=QuotaPeriod.MINUTE, reset_at=12345.0
    )
    assert u.key == "api"
    assert u.count == 2
    assert u.limit == 10
    assert u.period is QuotaPeriod.MINUTE
    assert u.reset_at == 12345.0


def test_quota_usage_remaining_positive():
    u = QuotaUsage(
        key="k", count=3, limit=10, period=QuotaPeriod.MINUTE, reset_at=0.0
    )
    assert u.remaining == 7


def test_quota_usage_remaining_zero_at_limit():
    u = QuotaUsage(
        key="k", count=10, limit=10, period=QuotaPeriod.MINUTE, reset_at=0.0
    )
    assert u.remaining == 0


def test_quota_usage_remaining_zero_when_over_limit():
    u = QuotaUsage(
        key="k", count=15, limit=10, period=QuotaPeriod.MINUTE, reset_at=0.0
    )
    assert u.remaining == 0


def test_quota_usage_remaining_when_count_zero():
    u = QuotaUsage(
        key="k", count=0, limit=5, period=QuotaPeriod.HOUR, reset_at=0.0
    )
    assert u.remaining == 5


def test_quota_usage_remaining_with_limit_one():
    u = QuotaUsage(key="k", count=0, limit=1, period=QuotaPeriod.DAY, reset_at=0.0)
    assert u.remaining == 1


def test_quota_usage_equality():
    a = QuotaUsage(
        key="x", count=1, limit=10, period=QuotaPeriod.HOUR, reset_at=42.0
    )
    b = QuotaUsage(
        key="x", count=1, limit=10, period=QuotaPeriod.HOUR, reset_at=42.0
    )
    assert a == b


# ============================================================================ #
# QuotaExceeded exception
# ============================================================================ #
def test_quota_exceeded_is_exception():
    assert issubclass(QuotaExceeded, Exception)


def test_quota_exceeded_carries_key_and_usage():
    u = QuotaUsage(
        key="api", count=10, limit=10, period=QuotaPeriod.MINUTE, reset_at=0.0
    )
    exc = QuotaExceeded("api", u)
    assert exc.key == "api"
    assert exc.usage is u


def test_quota_exceeded_message_contains_key():
    u = QuotaUsage(
        key="api", count=10, limit=10, period=QuotaPeriod.MINUTE, reset_at=0.0
    )
    exc = QuotaExceeded("api", u)
    assert "api" in str(exc)


def test_quota_exceeded_message_contains_counts():
    u = QuotaUsage(
        key="api", count=7, limit=10, period=QuotaPeriod.MINUTE, reset_at=0.0
    )
    exc = QuotaExceeded("api", u)
    s = str(exc)
    assert "7" in s and "10" in s


def test_quota_exceeded_can_be_raised_and_caught():
    u = QuotaUsage(
        key="k", count=5, limit=5, period=QuotaPeriod.SECOND, reset_at=0.0
    )
    with pytest.raises(QuotaExceeded) as ctx:
        raise QuotaExceeded("k", u)
    assert ctx.value.key == "k"


# ============================================================================ #
# QuotaStore.record
# ============================================================================ #
def test_store_record_initial_returns_one(mem_store):
    n = mem_store.record("k", "alice", 60.0, now=1000.0)
    assert n == 1


def test_store_record_increments_within_window(mem_store):
    mem_store.record("k", "alice", 60.0, now=1000.0)
    n = mem_store.record("k", "alice", 60.0, now=1005.0)
    assert n == 2


def test_store_record_with_amount(mem_store):
    n = mem_store.record("k", "alice", 60.0, now=1000.0, amount=5)
    assert n == 5


def test_store_record_amount_accumulates(mem_store):
    mem_store.record("k", "alice", 60.0, now=1000.0, amount=3)
    n = mem_store.record("k", "alice", 60.0, now=1010.0, amount=2)
    assert n == 5


def test_store_record_new_window_starts_fresh(mem_store):
    mem_store.record("k", "alice", 60.0, now=1000.0)
    mem_store.record("k", "alice", 60.0, now=1000.0)
    # Move into the next minute window (window_start 1020 -> next is 1080)
    n = mem_store.record("k", "alice", 60.0, now=1080.0)
    assert n == 1


def test_store_record_uses_floor_window(mem_store):
    # 1019 falls inside the window starting at 960 (with period=60),
    # 1020 falls inside the window starting at 1020.
    mem_store.record("k", "alice", 60.0, now=1019.0)
    n = mem_store.record("k", "alice", 60.0, now=1020.0)
    assert n == 1


def test_store_record_default_now_uses_time_time(mem_store, monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 2000.0)
    n = mem_store.record("k", "alice", 60.0)
    assert n == 1
    assert mem_store.get_count("k", "alice", 60.0, now=2000.5) == 1


def test_store_record_separate_keys(mem_store):
    mem_store.record("k1", "alice", 60.0, now=1000.0)
    n = mem_store.record("k2", "alice", 60.0, now=1000.0)
    assert n == 1


def test_store_record_separate_owners(mem_store):
    mem_store.record("k", "alice", 60.0, now=1000.0)
    mem_store.record("k", "alice", 60.0, now=1000.0)
    n = mem_store.record("k", "bob", 60.0, now=1000.0)
    assert n == 1


def test_store_record_owners_independent(mem_store):
    mem_store.record("k", "alice", 60.0, now=1000.0)
    mem_store.record("k", "bob", 60.0, now=1000.0)
    mem_store.record("k", "bob", 60.0, now=1000.0)
    assert mem_store.get_count("k", "alice", 60.0, now=1000.0) == 1
    assert mem_store.get_count("k", "bob", 60.0, now=1000.0) == 2


def test_store_record_invalid_period(mem_store):
    with pytest.raises(ValueError):
        mem_store.record("k", "alice", 0.0, now=1000.0)


def test_store_record_negative_period(mem_store):
    with pytest.raises(ValueError):
        mem_store.record("k", "alice", -60.0, now=1000.0)


# ============================================================================ #
# QuotaStore.get_count
# ============================================================================ #
def test_store_get_count_missing_returns_zero(mem_store):
    assert mem_store.get_count("k", "alice", 60.0, now=1000.0) == 0


def test_store_get_count_after_record(mem_store):
    mem_store.record("k", "alice", 60.0, now=1000.0)
    assert mem_store.get_count("k", "alice", 60.0, now=1000.0) == 1


def test_store_get_count_within_window(mem_store):
    # window for now=1000 is [960, 1020); both events fall inside it
    mem_store.record("k", "alice", 60.0, now=1000.0)
    mem_store.record("k", "alice", 60.0, now=1010.0)
    assert mem_store.get_count("k", "alice", 60.0, now=1019.0) == 2


def test_store_get_count_new_window_is_zero(mem_store):
    # Record in window [960, 1020), query in window [1020, 1080)
    mem_store.record("k", "alice", 60.0, now=1000.0)
    assert mem_store.get_count("k", "alice", 60.0, now=1020.0) == 0


def test_store_get_count_default_now(mem_store, monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 3000.0)
    mem_store.record("k", "alice", 60.0, now=3000.0)
    assert mem_store.get_count("k", "alice", 60.0) == 1


def test_store_get_count_per_owner(mem_store):
    mem_store.record("k", "alice", 60.0, now=1000.0)
    assert mem_store.get_count("k", "bob", 60.0, now=1000.0) == 0


def test_store_get_count_per_key(mem_store):
    mem_store.record("k1", "alice", 60.0, now=1000.0)
    assert mem_store.get_count("k2", "alice", 60.0, now=1000.0) == 0


# ============================================================================ #
# QuotaStore.reset
# ============================================================================ #
def test_store_reset_all(mem_store):
    mem_store.record("k1", "alice", 60.0, now=1000.0)
    mem_store.record("k2", "bob", 60.0, now=1000.0)
    deleted = mem_store.reset()
    assert deleted == 2
    assert mem_store.get_count("k1", "alice", 60.0, now=1000.0) == 0
    assert mem_store.get_count("k2", "bob", 60.0, now=1000.0) == 0


def test_store_reset_by_key(mem_store):
    mem_store.record("k1", "alice", 60.0, now=1000.0)
    mem_store.record("k1", "bob", 60.0, now=1000.0)
    mem_store.record("k2", "alice", 60.0, now=1000.0)
    deleted = mem_store.reset(quota_key="k1")
    assert deleted == 2
    assert mem_store.get_count("k1", "alice", 60.0, now=1000.0) == 0
    assert mem_store.get_count("k2", "alice", 60.0, now=1000.0) == 1


def test_store_reset_by_owner(mem_store):
    mem_store.record("k1", "alice", 60.0, now=1000.0)
    mem_store.record("k2", "alice", 60.0, now=1000.0)
    mem_store.record("k1", "bob", 60.0, now=1000.0)
    deleted = mem_store.reset(owner="alice")
    assert deleted == 2
    assert mem_store.get_count("k1", "alice", 60.0, now=1000.0) == 0
    assert mem_store.get_count("k1", "bob", 60.0, now=1000.0) == 1


def test_store_reset_by_key_and_owner(mem_store):
    mem_store.record("k1", "alice", 60.0, now=1000.0)
    mem_store.record("k1", "bob", 60.0, now=1000.0)
    mem_store.record("k2", "alice", 60.0, now=1000.0)
    deleted = mem_store.reset(quota_key="k1", owner="alice")
    assert deleted == 1
    assert mem_store.get_count("k1", "alice", 60.0, now=1000.0) == 0
    assert mem_store.get_count("k1", "bob", 60.0, now=1000.0) == 1
    assert mem_store.get_count("k2", "alice", 60.0, now=1000.0) == 1


def test_store_reset_empty_returns_zero(mem_store):
    assert mem_store.reset() == 0


def test_store_reset_unknown_key(mem_store):
    mem_store.record("k", "alice", 60.0, now=1000.0)
    assert mem_store.reset(quota_key="missing") == 0
    assert mem_store.get_count("k", "alice", 60.0, now=1000.0) == 1


def test_store_reset_unknown_owner(mem_store):
    mem_store.record("k", "alice", 60.0, now=1000.0)
    assert mem_store.reset(owner="ghost") == 0


def test_store_reset_across_windows(mem_store):
    mem_store.record("k", "alice", 60.0, now=1000.0)
    mem_store.record("k", "alice", 60.0, now=2000.0)
    deleted = mem_store.reset(quota_key="k", owner="alice")
    assert deleted == 2


# ============================================================================ #
# QuotaStore.cleanup
# ============================================================================ #
def test_store_cleanup_old_windows(mem_store):
    mem_store.record("k", "alice", 60.0, now=100.0)   # window_start=60.0
    mem_store.record("k", "alice", 60.0, now=200.0)   # window_start=180.0
    mem_store.record("k", "alice", 60.0, now=1000.0)  # window_start=960.0
    deleted = mem_store.cleanup(older_than=500.0)
    assert deleted == 2
    assert mem_store.get_count("k", "alice", 60.0, now=1000.0) == 1


def test_store_cleanup_no_match(mem_store):
    mem_store.record("k", "alice", 60.0, now=1000.0)
    assert mem_store.cleanup(older_than=0.0) == 0


def test_store_cleanup_all_match(mem_store):
    mem_store.record("k", "alice", 60.0, now=100.0)
    mem_store.record("k", "bob", 60.0, now=200.0)
    deleted = mem_store.cleanup(older_than=10_000.0)
    assert deleted == 2


def test_store_cleanup_uses_strict_less_than(mem_store):
    # window_start for now=120 with period 60 == 120.0
    mem_store.record("k", "alice", 60.0, now=120.0)
    # older_than equal to the window_start must NOT delete
    assert mem_store.cleanup(older_than=120.0) == 0
    # but older_than just above does
    assert mem_store.cleanup(older_than=120.5) == 1


def test_store_cleanup_empty(mem_store):
    assert mem_store.cleanup(older_than=time.time()) == 0


# ============================================================================ #
# QuotaStore.close
# ============================================================================ #
def test_store_close_can_be_called(tmp_path):
    s = QuotaStore(db_path=str(tmp_path / "x.sqlite"))
    s.close()  # should not raise


def test_store_close_blocks_further_use(tmp_path):
    import sqlite3 as _sql
    s = QuotaStore(db_path=str(tmp_path / "x.sqlite"))
    s.close()
    with pytest.raises(_sql.ProgrammingError):
        s.get_count("k", "alice", 60.0, now=1000.0)


def test_store_default_in_memory():
    s = QuotaStore()
    try:
        s.record("k", "alice", 60.0, now=1000.0)
        assert s.get_count("k", "alice", 60.0, now=1000.0) == 1
    finally:
        s.close()


def test_store_persistence_round_trip(tmp_path):
    path = str(tmp_path / "p.sqlite")
    s1 = QuotaStore(db_path=path)
    s1.record("k", "alice", 60.0, now=1000.0)
    s1.record("k", "alice", 60.0, now=1010.0)
    s1.close()

    s2 = QuotaStore(db_path=path)
    try:
        # Query in same window [960, 1020)
        assert s2.get_count("k", "alice", 60.0, now=1015.0) == 2
    finally:
        s2.close()


# ============================================================================ #
# QuotaManager.define / get_definition / list_definitions
# ============================================================================ #
def test_manager_init_creates_store():
    m = QuotaManager()
    try:
        assert isinstance(m.store, QuotaStore)
    finally:
        m.store.close()


def test_manager_init_uses_provided_store(mem_store):
    m = QuotaManager(store=mem_store)
    assert m.store is mem_store


def test_manager_define(mgr):
    qd = QuotaDefinition(key="api", limit=10, period=QuotaPeriod.MINUTE)
    mgr.define(qd)
    assert mgr.get_definition("api") is qd


def test_manager_get_definition_missing(mgr):
    assert mgr.get_definition("nope") is None


def test_manager_define_overrides(mgr):
    mgr.define(QuotaDefinition(key="api", limit=10, period=QuotaPeriod.MINUTE))
    mgr.define(QuotaDefinition(key="api", limit=20, period=QuotaPeriod.HOUR))
    qd = mgr.get_definition("api")
    assert qd.limit == 20
    assert qd.period is QuotaPeriod.HOUR


def test_manager_list_definitions_empty(mgr):
    assert mgr.list_definitions() == []


def test_manager_list_definitions(mgr):
    a = QuotaDefinition(key="a", limit=1, period=QuotaPeriod.MINUTE)
    b = QuotaDefinition(key="b", limit=2, period=QuotaPeriod.HOUR)
    mgr.define(a)
    mgr.define(b)
    items = mgr.list_definitions()
    assert len(items) == 2
    keys = {d.key for d in items}
    assert keys == {"a", "b"}


# ============================================================================ #
# QuotaManager.check
# ============================================================================ #
def test_manager_check_unknown_key_raises(mgr):
    with pytest.raises(KeyError):
        mgr.check("nope", "alice", now=1000.0)


def test_manager_check_returns_zero_count_initially(mgr):
    mgr.define(QuotaDefinition(key="api", limit=10, period=QuotaPeriod.MINUTE))
    u = mgr.check("api", "alice", now=1000.0)
    assert u.count == 0
    assert u.limit == 10
    assert u.remaining == 10
    assert u.period is QuotaPeriod.MINUTE
    assert u.key == "api"


def test_manager_check_does_not_increment(mgr):
    mgr.define(QuotaDefinition(key="api", limit=10, period=QuotaPeriod.MINUTE))
    mgr.check("api", "alice", now=1000.0)
    mgr.check("api", "alice", now=1000.0)
    assert mgr.check("api", "alice", now=1000.0).count == 0


def test_manager_check_reset_at_for_minute(mgr):
    mgr.define(QuotaDefinition(key="api", limit=10, period=QuotaPeriod.MINUTE))
    u = mgr.check("api", "alice", now=1000.0)
    # window_start = floor(1000/60)*60 = 960; reset_at = 960 + 60 = 1020
    assert u.reset_at == 1020.0


def test_manager_check_reset_at_for_second(mgr):
    mgr.define(QuotaDefinition(key="api", limit=5, period=QuotaPeriod.SECOND))
    u = mgr.check("api", "alice", now=1000.5)
    # window_start=1000, reset_at=1001
    assert u.reset_at == 1001.0


def test_manager_check_reset_at_for_hour(mgr):
    mgr.define(QuotaDefinition(key="api", limit=5, period=QuotaPeriod.HOUR))
    u = mgr.check("api", "alice", now=3600.0)
    assert u.reset_at == 7200.0


def test_manager_check_after_consume(mgr):
    mgr.define(QuotaDefinition(key="api", limit=10, period=QuotaPeriod.MINUTE))
    # All in the same minute window [960, 1020)
    mgr.consume("api", "alice", now=1000.0)
    mgr.consume("api", "alice", now=1010.0)
    u = mgr.check("api", "alice", now=1015.0)
    assert u.count == 2
    assert u.remaining == 8


# ============================================================================ #
# QuotaManager.consume
# ============================================================================ #
def test_manager_consume_unknown_raises(mgr):
    with pytest.raises(KeyError):
        mgr.consume("nope", "alice", now=1000.0)


def test_manager_consume_returns_usage(mgr):
    mgr.define(QuotaDefinition(key="api", limit=5, period=QuotaPeriod.MINUTE))
    u = mgr.consume("api", "alice", now=1000.0)
    assert isinstance(u, QuotaUsage)
    assert u.count == 1
    assert u.limit == 5
    assert u.remaining == 4


def test_manager_consume_increments(mgr):
    mgr.define(QuotaDefinition(key="api", limit=5, period=QuotaPeriod.MINUTE))
    mgr.consume("api", "alice", now=1000.0)
    u = mgr.consume("api", "alice", now=1001.0)
    assert u.count == 2


def test_manager_consume_to_limit(mgr):
    mgr.define(QuotaDefinition(key="api", limit=3, period=QuotaPeriod.MINUTE))
    for _ in range(3):
        mgr.consume("api", "alice", now=1000.0)
    assert mgr.check("api", "alice", now=1000.0).count == 3


def test_manager_consume_over_limit_raises(mgr):
    mgr.define(QuotaDefinition(key="api", limit=2, period=QuotaPeriod.MINUTE))
    mgr.consume("api", "alice", now=1000.0)
    mgr.consume("api", "alice", now=1001.0)
    with pytest.raises(QuotaExceeded):
        mgr.consume("api", "alice", now=1002.0)


def test_manager_consume_exceeded_exception_carries_usage(mgr):
    mgr.define(QuotaDefinition(key="api", limit=1, period=QuotaPeriod.MINUTE))
    mgr.consume("api", "alice", now=1000.0)
    with pytest.raises(QuotaExceeded) as ctx:
        mgr.consume("api", "alice", now=1001.0)
    assert ctx.value.key == "api"
    assert ctx.value.usage.count == 1
    assert ctx.value.usage.limit == 1


def test_manager_consume_does_not_increment_when_exceeded(mgr):
    mgr.define(QuotaDefinition(key="api", limit=1, period=QuotaPeriod.MINUTE))
    mgr.consume("api", "alice", now=1000.0)
    with pytest.raises(QuotaExceeded):
        mgr.consume("api", "alice", now=1001.0)
    # Count should still be 1, not 2
    assert mgr.check("api", "alice", now=1010.0).count == 1


def test_manager_consume_with_amount(mgr):
    mgr.define(QuotaDefinition(key="api", limit=10, period=QuotaPeriod.MINUTE))
    u = mgr.consume("api", "alice", now=1000.0, amount=4)
    assert u.count == 4
    assert u.remaining == 6


def test_manager_consume_amount_exceeds_remaining(mgr):
    mgr.define(QuotaDefinition(key="api", limit=5, period=QuotaPeriod.MINUTE))
    mgr.consume("api", "alice", now=1000.0, amount=3)
    with pytest.raises(QuotaExceeded):
        mgr.consume("api", "alice", now=1001.0, amount=3)
    # 3 + 3 > 5, so no consume
    assert mgr.check("api", "alice", now=1002.0).count == 3


def test_manager_consume_exact_remaining(mgr):
    mgr.define(QuotaDefinition(key="api", limit=5, period=QuotaPeriod.MINUTE))
    mgr.consume("api", "alice", now=1000.0, amount=3)
    u = mgr.consume("api", "alice", now=1001.0, amount=2)
    assert u.count == 5
    assert u.remaining == 0


def test_manager_consume_separate_owners(mgr):
    mgr.define(QuotaDefinition(key="api", limit=1, period=QuotaPeriod.MINUTE))
    mgr.consume("api", "alice", now=1000.0)
    # bob should still be able to consume
    u = mgr.consume("api", "bob", now=1000.0)
    assert u.count == 1


def test_manager_consume_reset_at_field(mgr):
    mgr.define(QuotaDefinition(key="api", limit=10, period=QuotaPeriod.MINUTE))
    u = mgr.consume("api", "alice", now=1000.0)
    assert u.reset_at == 1020.0


# ============================================================================ #
# QuotaManager.try_consume
# ============================================================================ #
def test_manager_try_consume_success(mgr):
    mgr.define(QuotaDefinition(key="api", limit=2, period=QuotaPeriod.MINUTE))
    ok, u = mgr.try_consume("api", "alice", now=1000.0)
    assert ok is True
    assert u.count == 1


def test_manager_try_consume_failure(mgr):
    mgr.define(QuotaDefinition(key="api", limit=1, period=QuotaPeriod.MINUTE))
    mgr.try_consume("api", "alice", now=1000.0)
    ok, u = mgr.try_consume("api", "alice", now=1001.0)
    assert ok is False
    assert u.count == 1
    assert u.limit == 1
    assert u.remaining == 0


def test_manager_try_consume_does_not_increment_on_failure(mgr):
    mgr.define(QuotaDefinition(key="api", limit=1, period=QuotaPeriod.MINUTE))
    mgr.try_consume("api", "alice", now=1000.0)
    mgr.try_consume("api", "alice", now=1001.0)
    mgr.try_consume("api", "alice", now=1002.0)
    assert mgr.check("api", "alice", now=1003.0).count == 1


def test_manager_try_consume_returns_tuple(mgr):
    mgr.define(QuotaDefinition(key="api", limit=3, period=QuotaPeriod.MINUTE))
    out = mgr.try_consume("api", "alice", now=1000.0)
    assert isinstance(out, tuple)
    assert len(out) == 2


def test_manager_try_consume_with_amount(mgr):
    mgr.define(QuotaDefinition(key="api", limit=10, period=QuotaPeriod.MINUTE))
    ok, u = mgr.try_consume("api", "alice", now=1000.0, amount=7)
    assert ok is True
    assert u.count == 7


def test_manager_try_consume_amount_exceeds(mgr):
    mgr.define(QuotaDefinition(key="api", limit=5, period=QuotaPeriod.MINUTE))
    mgr.try_consume("api", "alice", now=1000.0, amount=3)
    ok, u = mgr.try_consume("api", "alice", now=1001.0, amount=5)
    assert ok is False
    assert u.count == 3


def test_manager_try_consume_unknown_key_raises(mgr):
    # try_consume should still raise on unknown key (KeyError, not QuotaExceeded)
    with pytest.raises(KeyError):
        mgr.try_consume("missing", "alice", now=1000.0)


# ============================================================================ #
# QuotaManager.reset
# ============================================================================ #
def test_manager_reset_clears_counts(mgr):
    mgr.define(QuotaDefinition(key="api", limit=10, period=QuotaPeriod.MINUTE))
    mgr.consume("api", "alice", now=1000.0)
    mgr.reset(key="api", owner="alice")
    assert mgr.check("api", "alice", now=1000.0).count == 0


def test_manager_reset_definitions_remain(mgr):
    mgr.define(QuotaDefinition(key="api", limit=10, period=QuotaPeriod.MINUTE))
    mgr.consume("api", "alice", now=1000.0)
    mgr.reset()
    assert mgr.get_definition("api") is not None


def test_manager_reset_by_owner_only(mgr):
    mgr.define(QuotaDefinition(key="api", limit=5, period=QuotaPeriod.MINUTE))
    mgr.consume("api", "alice", now=1000.0)
    mgr.consume("api", "bob", now=1000.0)
    mgr.reset(owner="alice")
    assert mgr.check("api", "alice", now=1000.0).count == 0
    assert mgr.check("api", "bob", now=1000.0).count == 1


def test_manager_reset_by_key_only(mgr):
    mgr.define(QuotaDefinition(key="a", limit=5, period=QuotaPeriod.MINUTE))
    mgr.define(QuotaDefinition(key="b", limit=5, period=QuotaPeriod.MINUTE))
    mgr.consume("a", "alice", now=1000.0)
    mgr.consume("b", "alice", now=1000.0)
    mgr.reset(key="a")
    assert mgr.check("a", "alice", now=1000.0).count == 0
    assert mgr.check("b", "alice", now=1000.0).count == 1


def test_manager_reset_returns_deleted_count(mgr):
    mgr.define(QuotaDefinition(key="a", limit=5, period=QuotaPeriod.MINUTE))
    mgr.consume("a", "alice", now=1000.0)
    mgr.consume("a", "bob", now=1000.0)
    assert mgr.reset() == 2


# ============================================================================ #
# Window rollover behaviour
# ============================================================================ #
def test_window_rollover_minute(mgr):
    mgr.define(QuotaDefinition(key="api", limit=2, period=QuotaPeriod.MINUTE))
    # All in same minute window [960, 1020)
    mgr.consume("api", "alice", now=1000.0)
    mgr.consume("api", "alice", now=1010.0)
    # next consume in same window should fail
    with pytest.raises(QuotaExceeded):
        mgr.consume("api", "alice", now=1019.0)
    # but in the next window [1020, 1080) it should succeed
    u = mgr.consume("api", "alice", now=1020.0)
    assert u.count == 1


def test_window_rollover_second(mgr):
    mgr.define(QuotaDefinition(key="api", limit=1, period=QuotaPeriod.SECOND))
    mgr.consume("api", "alice", now=1000.0)
    with pytest.raises(QuotaExceeded):
        mgr.consume("api", "alice", now=1000.5)
    u = mgr.consume("api", "alice", now=1001.0)
    assert u.count == 1


def test_window_rollover_hour(mgr):
    mgr.define(QuotaDefinition(key="api", limit=1, period=QuotaPeriod.HOUR))
    mgr.consume("api", "alice", now=0.0)
    with pytest.raises(QuotaExceeded):
        mgr.consume("api", "alice", now=3599.0)
    u = mgr.consume("api", "alice", now=3600.0)
    assert u.count == 1


def test_window_rollover_day(mgr):
    mgr.define(QuotaDefinition(key="api", limit=1, period=QuotaPeriod.DAY))
    mgr.consume("api", "alice", now=0.0)
    with pytest.raises(QuotaExceeded):
        mgr.consume("api", "alice", now=86399.0)
    u = mgr.consume("api", "alice", now=86400.0)
    assert u.count == 1


def test_window_count_resets_in_new_window(mgr):
    mgr.define(QuotaDefinition(key="api", limit=5, period=QuotaPeriod.MINUTE))
    for _ in range(5):
        mgr.consume("api", "alice", now=1000.0)
    # New minute window
    u = mgr.check("api", "alice", now=1080.0)
    assert u.count == 0
    assert u.remaining == 5


# ============================================================================ #
# Multiple periods coexisting
# ============================================================================ #
def test_multiple_periods_independent(mgr):
    mgr.define(QuotaDefinition(key="per_minute", limit=5, period=QuotaPeriod.MINUTE))
    mgr.define(QuotaDefinition(key="per_hour", limit=100, period=QuotaPeriod.HOUR))
    for _ in range(5):
        mgr.consume("per_minute", "alice", now=1000.0)
        mgr.consume("per_hour", "alice", now=1000.0)
    assert mgr.check("per_minute", "alice", now=1000.0).count == 5
    assert mgr.check("per_hour", "alice", now=1000.0).count == 5
    with pytest.raises(QuotaExceeded):
        mgr.consume("per_minute", "alice", now=1001.0)
    # per_hour still has plenty
    u = mgr.consume("per_hour", "alice", now=1001.0)
    assert u.count == 6


def test_multiple_periods_different_reset_at(mgr):
    mgr.define(QuotaDefinition(key="m", limit=1, period=QuotaPeriod.MINUTE))
    mgr.define(QuotaDefinition(key="h", limit=1, period=QuotaPeriod.HOUR))
    um = mgr.check("m", "alice", now=1000.0)
    uh = mgr.check("h", "alice", now=1000.0)
    assert um.reset_at == 1020.0  # 960+60
    assert uh.reset_at == 3600.0  # 0+3600


def test_multiple_owners_independent_consume(mgr):
    mgr.define(QuotaDefinition(key="api", limit=2, period=QuotaPeriod.MINUTE))
    mgr.consume("api", "alice", now=1000.0)
    mgr.consume("api", "alice", now=1000.0)
    mgr.consume("api", "bob", now=1000.0)
    with pytest.raises(QuotaExceeded):
        mgr.consume("api", "alice", now=1000.0)
    # bob still has room
    u = mgr.consume("api", "bob", now=1000.0)
    assert u.count == 2


# ============================================================================ #
# End-to-end behaviours
# ============================================================================ #
def test_full_cycle_consume_exceed_reset_consume(mgr):
    mgr.define(QuotaDefinition(key="api", limit=2, period=QuotaPeriod.MINUTE))
    mgr.consume("api", "alice", now=1000.0)
    mgr.consume("api", "alice", now=1000.0)
    with pytest.raises(QuotaExceeded):
        mgr.consume("api", "alice", now=1000.0)
    mgr.reset(key="api", owner="alice")
    u = mgr.consume("api", "alice", now=1000.0)
    assert u.count == 1


def test_cleanup_does_not_affect_current_window(mgr):
    mgr.define(QuotaDefinition(key="api", limit=5, period=QuotaPeriod.MINUTE))
    mgr.consume("api", "alice", now=1000.0)
    # window_start is 960.0; cleanup older than 500 should leave it alone.
    deleted = mgr.store.cleanup(older_than=500.0)
    assert deleted == 0
    assert mgr.check("api", "alice", now=1000.0).count == 1


def test_try_consume_returns_false_repeatedly(mgr):
    mgr.define(QuotaDefinition(key="api", limit=1, period=QuotaPeriod.MINUTE))
    ok1, _ = mgr.try_consume("api", "alice", now=1000.0)
    ok2, _ = mgr.try_consume("api", "alice", now=1001.0)
    ok3, _ = mgr.try_consume("api", "alice", now=1002.0)
    assert ok1 is True
    assert ok2 is False
    assert ok3 is False


def test_default_now_consume_uses_time(mgr, monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 50_000.0)
    mgr.define(QuotaDefinition(key="api", limit=3, period=QuotaPeriod.MINUTE))
    u = mgr.consume("api", "alice")
    assert u.count == 1
    # Re-check using the same frozen time
    assert mgr.check("api", "alice").count == 1


def test_default_now_check_uses_time(mgr, monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 70_000.0)
    mgr.define(QuotaDefinition(key="api", limit=3, period=QuotaPeriod.MINUTE))
    u = mgr.check("api", "alice")
    assert u.count == 0
    assert u.reset_at == math.floor(70_000.0 / 60) * 60 + 60


def test_definition_can_be_listed_after_consume(mgr):
    mgr.define(QuotaDefinition(key="api", limit=1, period=QuotaPeriod.MINUTE))
    mgr.consume("api", "alice", now=1000.0)
    defs = mgr.list_definitions()
    assert len(defs) == 1
    assert defs[0].key == "api"


def test_consume_amount_zero_records_zero(mgr):
    # Amount=0 means "no change but still validates"; consumes 0 entries.
    mgr.define(QuotaDefinition(key="api", limit=1, period=QuotaPeriod.MINUTE))
    u = mgr.consume("api", "alice", now=1000.0, amount=0)
    assert u.count == 0


def test_manager_check_for_other_owner_after_consume(mgr):
    mgr.define(QuotaDefinition(key="api", limit=5, period=QuotaPeriod.MINUTE))
    mgr.consume("api", "alice", now=1000.0)
    u = mgr.check("api", "bob", now=1000.0)
    assert u.count == 0
    assert u.remaining == 5


def test_manager_check_returns_new_object(mgr):
    mgr.define(QuotaDefinition(key="api", limit=5, period=QuotaPeriod.MINUTE))
    u1 = mgr.check("api", "alice", now=1000.0)
    u2 = mgr.check("api", "alice", now=1000.0)
    assert u1 is not u2  # fresh instance each call


def test_store_record_returns_int(mem_store):
    n = mem_store.record("k", "alice", 60.0, now=1000.0)
    assert isinstance(n, int)


def test_store_get_count_returns_int(mem_store):
    mem_store.record("k", "alice", 60.0, now=1000.0)
    assert isinstance(mem_store.get_count("k", "alice", 60.0, now=1000.0), int)


def test_store_window_floor_day(mem_store):
    # day period; events at 100 (window 0) and 86399 (window 0) and 86400 (window 86400)
    mem_store.record("k", "alice", 86400.0, now=100.0)
    n = mem_store.record("k", "alice", 86400.0, now=86399.0)
    assert n == 2
    n2 = mem_store.record("k", "alice", 86400.0, now=86400.0)
    assert n2 == 1


def test_store_window_floor_hour(mem_store):
    mem_store.record("k", "alice", 3600.0, now=3000.0)
    mem_store.record("k", "alice", 3600.0, now=3500.0)
    assert mem_store.get_count("k", "alice", 3600.0, now=3599.0) == 2
    assert mem_store.get_count("k", "alice", 3600.0, now=3600.0) == 0


def test_init_module_exports():
    import docstoolkit.rate_quota as rq
    for name in (
        "QuotaPeriod",
        "QuotaDefinition",
        "QuotaUsage",
        "QuotaExceeded",
        "QuotaStore",
        "QuotaManager",
    ):
        assert hasattr(rq, name)


def test_init_all_contains_expected_names():
    import docstoolkit.rate_quota as rq
    assert set(rq.__all__) == {
        "QuotaPeriod",
        "QuotaDefinition",
        "QuotaUsage",
        "QuotaExceeded",
        "QuotaStore",
        "QuotaManager",
    }
