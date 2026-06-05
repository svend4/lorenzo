"""Tests for E412 DocQuotaTracker."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_quota_tracker import (
    DocQuotaTracker,
    QuotaDefinition,
    QuotaStats,
    QuotaUsage,
)


# ---------------------------------------------------------------------- #
# Dataclasses
# ---------------------------------------------------------------------- #
def test_quota_definition_basic():
    d = QuotaDefinition(resource="docs", limit=10)
    assert d.resource == "docs"
    assert d.limit == 10
    assert d.description == ""


def test_quota_definition_with_description():
    d = QuotaDefinition(resource="api", limit=100, description="API calls")
    assert d.description == "API calls"


def test_quota_usage_defaults():
    u = QuotaUsage(key="u1", resource="docs")
    assert u.current == 0
    assert u.last_updated_at == 0.0


def test_quota_usage_with_values():
    u = QuotaUsage(key="u1", resource="docs", current=5, last_updated_at=10.0)
    assert u.current == 5
    assert u.last_updated_at == 10.0


def test_quota_stats_construction():
    s = QuotaStats(
        total_definitions=2, total_keys=3, keys_at_limit=1, keys_over_limit=0
    )
    assert s.total_definitions == 2
    assert s.total_keys == 3
    assert s.keys_at_limit == 1
    assert s.keys_over_limit == 0


# ---------------------------------------------------------------------- #
# define_quota / remove_quota / get_definition / list_definitions
# ---------------------------------------------------------------------- #
def test_define_quota_registers():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    assert t.get_definition("docs") is not None
    assert t.get_definition("docs").limit == 10


def test_define_quota_replaces():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.define_quota(QuotaDefinition("docs", 20, "updated"))
    d = t.get_definition("docs")
    assert d.limit == 20
    assert d.description == "updated"


def test_get_definition_missing():
    t = DocQuotaTracker()
    assert t.get_definition("nope") is None


def test_remove_quota_present():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    assert t.remove_quota("docs") is True
    assert t.get_definition("docs") is None


def test_remove_quota_absent():
    t = DocQuotaTracker()
    assert t.remove_quota("nope") is False


def test_list_definitions_empty():
    t = DocQuotaTracker()
    assert t.list_definitions() == []


def test_list_definitions_sorted():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.define_quota(QuotaDefinition("api", 100))
    t.define_quota(QuotaDefinition("storage", 1000))
    names = [d.resource for d in t.list_definitions()]
    assert names == ["api", "docs", "storage"]


# ---------------------------------------------------------------------- #
# increment
# ---------------------------------------------------------------------- #
def test_increment_returns_none_when_undefined():
    t = DocQuotaTracker()
    assert t.increment("u1", "docs") is None


def test_increment_creates_usage():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    u = t.increment("u1", "docs", now=1.0)
    assert u is not None
    assert u.current == 1
    assert u.key == "u1"
    assert u.resource == "docs"
    assert u.last_updated_at == 1.0


def test_increment_default_amount_is_one():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", now=1.0)
    t.increment("u1", "docs", now=2.0)
    u = t.get_usage("u1", "docs")
    assert u.current == 2


def test_increment_custom_amount():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 100))
    u = t.increment("u1", "docs", amount=7, now=1.0)
    assert u.current == 7


def test_increment_updates_timestamp():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", now=1.0)
    t.increment("u1", "docs", now=5.0)
    u = t.get_usage("u1", "docs")
    assert u.last_updated_at == 5.0


def test_increment_can_exceed_limit():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 3))
    for _ in range(5):
        t.increment("u1", "docs", now=1.0)
    u = t.get_usage("u1", "docs")
    assert u.current == 5


def test_increment_uses_real_time_when_now_none():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    u = t.increment("u1", "docs")
    assert u.last_updated_at > 0.0


# ---------------------------------------------------------------------- #
# decrement
# ---------------------------------------------------------------------- #
def test_decrement_returns_none_when_undefined():
    t = DocQuotaTracker()
    assert t.decrement("u1", "docs") is None


def test_decrement_floors_at_zero():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", amount=2, now=1.0)
    u = t.decrement("u1", "docs", amount=5, now=2.0)
    assert u.current == 0


def test_decrement_creates_usage_at_zero():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    u = t.decrement("u1", "docs", now=1.0)
    assert u.current == 0
    assert u.last_updated_at == 1.0


def test_decrement_basic():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", amount=5, now=1.0)
    u = t.decrement("u1", "docs", amount=2, now=2.0)
    assert u.current == 3


def test_decrement_default_amount_is_one():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", amount=4, now=1.0)
    t.decrement("u1", "docs", now=2.0)
    assert t.get_usage("u1", "docs").current == 3


# ---------------------------------------------------------------------- #
# set_usage
# ---------------------------------------------------------------------- #
def test_set_usage_returns_none_when_undefined():
    t = DocQuotaTracker()
    assert t.set_usage("u1", "docs", 5) is None


def test_set_usage_creates_entry():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    u = t.set_usage("u1", "docs", 7, now=1.0)
    assert u.current == 7
    assert u.last_updated_at == 1.0


def test_set_usage_overwrites():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", amount=3, now=1.0)
    u = t.set_usage("u1", "docs", 9, now=2.0)
    assert u.current == 9


def test_set_usage_negative_becomes_zero():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    u = t.set_usage("u1", "docs", -5, now=1.0)
    assert u.current == 0


def test_set_usage_can_exceed_limit():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    u = t.set_usage("u1", "docs", 100, now=1.0)
    assert u.current == 100


# ---------------------------------------------------------------------- #
# get_usage
# ---------------------------------------------------------------------- #
def test_get_usage_missing():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    assert t.get_usage("u1", "docs") is None


def test_get_usage_after_increment():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", now=1.0)
    u = t.get_usage("u1", "docs")
    assert u is not None
    assert u.current == 1


# ---------------------------------------------------------------------- #
# check
# ---------------------------------------------------------------------- #
def test_check_undefined_returns_false():
    t = DocQuotaTracker()
    assert t.check("u1", "docs") is False


def test_check_empty_usage_within_limit():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    assert t.check("u1", "docs", amount=5) is True


def test_check_exactly_at_limit():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", amount=10, now=1.0)
    assert t.check("u1", "docs", amount=0) is True


def test_check_would_exceed_limit():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", amount=8, now=1.0)
    assert t.check("u1", "docs", amount=3) is False


def test_check_default_amount_is_one():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", amount=9, now=1.0)
    assert t.check("u1", "docs") is True
    t.increment("u1", "docs", now=2.0)
    assert t.check("u1", "docs") is False


# ---------------------------------------------------------------------- #
# available
# ---------------------------------------------------------------------- #
def test_available_undefined():
    t = DocQuotaTracker()
    assert t.available("u1", "docs") is None


def test_available_no_usage():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    assert t.available("u1", "docs") == 10


def test_available_after_increment():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", amount=3, now=1.0)
    assert t.available("u1", "docs") == 7


def test_available_can_go_negative():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.set_usage("u1", "docs", 25, now=1.0)
    assert t.available("u1", "docs") == -15


# ---------------------------------------------------------------------- #
# usage_for_key
# ---------------------------------------------------------------------- #
def test_usage_for_key_empty():
    t = DocQuotaTracker()
    assert t.usage_for_key("u1") == []


def test_usage_for_key_sorted_by_resource():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.define_quota(QuotaDefinition("api", 100))
    t.define_quota(QuotaDefinition("storage", 1000))
    t.increment("u1", "storage", now=1.0)
    t.increment("u1", "docs", now=2.0)
    t.increment("u1", "api", now=3.0)
    usages = t.usage_for_key("u1")
    assert [u.resource for u in usages] == ["api", "docs", "storage"]


def test_usage_for_key_isolation():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", now=1.0)
    t.increment("u2", "docs", now=1.0)
    assert len(t.usage_for_key("u1")) == 1
    assert len(t.usage_for_key("u2")) == 1


# ---------------------------------------------------------------------- #
# keys_at_limit
# ---------------------------------------------------------------------- #
def test_keys_at_limit_undefined_returns_empty():
    t = DocQuotaTracker()
    assert t.keys_at_limit("docs") == []


def test_keys_at_limit_none_at_limit():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", amount=5, now=1.0)
    assert t.keys_at_limit("docs") == []


def test_keys_at_limit_at_exact_limit():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 5))
    t.increment("u1", "docs", amount=5, now=1.0)
    t.increment("u2", "docs", amount=4, now=1.0)
    assert t.keys_at_limit("docs") == ["u1"]


def test_keys_at_limit_over_limit_included():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 5))
    t.set_usage("u1", "docs", 5, now=1.0)
    t.set_usage("u2", "docs", 10, now=1.0)
    assert t.keys_at_limit("docs") == ["u1", "u2"]


def test_keys_at_limit_sorted():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 5))
    t.set_usage("zeta", "docs", 5, now=1.0)
    t.set_usage("alpha", "docs", 5, now=1.0)
    t.set_usage("mu", "docs", 5, now=1.0)
    assert t.keys_at_limit("docs") == ["alpha", "mu", "zeta"]


def test_keys_at_limit_only_for_resource():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 5))
    t.define_quota(QuotaDefinition("api", 5))
    t.set_usage("u1", "docs", 5, now=1.0)
    t.set_usage("u2", "api", 5, now=1.0)
    assert t.keys_at_limit("docs") == ["u1"]
    assert t.keys_at_limit("api") == ["u2"]


# ---------------------------------------------------------------------- #
# reset_key / clear_resource
# ---------------------------------------------------------------------- #
def test_reset_key_zeros_all_entries():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.define_quota(QuotaDefinition("api", 100))
    t.increment("u1", "docs", amount=3, now=1.0)
    t.increment("u1", "api", amount=50, now=1.0)
    n = t.reset_key("u1")
    assert n == 2
    assert t.get_usage("u1", "docs").current == 0
    assert t.get_usage("u1", "api").current == 0


def test_reset_key_unknown_returns_zero():
    t = DocQuotaTracker()
    assert t.reset_key("nobody") == 0


def test_reset_key_does_not_affect_other_keys():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", amount=3, now=1.0)
    t.increment("u2", "docs", amount=5, now=1.0)
    t.reset_key("u1")
    assert t.get_usage("u2", "docs").current == 5


def test_clear_resource_removes_all_entries():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.define_quota(QuotaDefinition("api", 100))
    t.increment("u1", "docs", now=1.0)
    t.increment("u2", "docs", now=1.0)
    t.increment("u1", "api", now=1.0)
    n = t.clear_resource("docs")
    assert n == 2
    assert t.get_usage("u1", "docs") is None
    assert t.get_usage("u2", "docs") is None
    assert t.get_usage("u1", "api") is not None


def test_clear_resource_unknown_returns_zero():
    t = DocQuotaTracker()
    assert t.clear_resource("nope") == 0


def test_clear_resource_does_not_remove_definition():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", now=1.0)
    t.clear_resource("docs")
    assert t.get_definition("docs") is not None


# ---------------------------------------------------------------------- #
# stats
# ---------------------------------------------------------------------- #
def test_stats_empty():
    t = DocQuotaTracker()
    s = t.stats()
    assert s.total_definitions == 0
    assert s.total_keys == 0
    assert s.keys_at_limit == 0
    assert s.keys_over_limit == 0


def test_stats_counts_definitions():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.define_quota(QuotaDefinition("api", 100))
    assert t.stats().total_definitions == 2


def test_stats_counts_unique_keys():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.define_quota(QuotaDefinition("api", 100))
    t.increment("u1", "docs", now=1.0)
    t.increment("u1", "api", now=1.0)
    t.increment("u2", "docs", now=1.0)
    assert t.stats().total_keys == 2


def test_stats_at_limit():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 5))
    t.set_usage("u1", "docs", 5, now=1.0)
    t.set_usage("u2", "docs", 3, now=1.0)
    s = t.stats()
    assert s.keys_at_limit == 1
    assert s.keys_over_limit == 0


def test_stats_over_limit():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 5))
    t.set_usage("u1", "docs", 10, now=1.0)
    s = t.stats()
    assert s.keys_at_limit == 0
    assert s.keys_over_limit == 1


def test_stats_mixed():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 5))
    t.define_quota(QuotaDefinition("api", 5))
    t.set_usage("u1", "docs", 5, now=1.0)
    t.set_usage("u2", "docs", 6, now=1.0)
    t.set_usage("u3", "api", 5, now=1.0)
    t.set_usage("u4", "api", 2, now=1.0)
    s = t.stats()
    assert s.total_definitions == 2
    assert s.total_keys == 4
    assert s.keys_at_limit == 2
    assert s.keys_over_limit == 1


def test_stats_ignores_usage_without_definition():
    """If a definition is removed but usage remains, stats skips it."""
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 5))
    t.set_usage("u1", "docs", 5, now=1.0)
    t.remove_quota("docs")
    s = t.stats()
    assert s.total_definitions == 0
    assert s.total_keys == 1  # usage still recorded
    assert s.keys_at_limit == 0
    assert s.keys_over_limit == 0


# ---------------------------------------------------------------------- #
# Thread safety
# ---------------------------------------------------------------------- #
def test_thread_safety_increment_concurrent():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 1_000_000))
    n_threads = 8
    per_thread = 500

    def worker():
        for _ in range(per_thread):
            t.increment("u1", "docs", now=1.0)

    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()

    u = t.get_usage("u1", "docs")
    assert u.current == n_threads * per_thread


def test_thread_safety_multiple_keys():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 1_000_000))
    n_threads = 8
    per_thread = 200

    def worker(key: str):
        for _ in range(per_thread):
            t.increment(key, "docs", now=1.0)

    threads = [
        threading.Thread(target=worker, args=(f"u{i}",)) for i in range(n_threads)
    ]
    for th in threads:
        th.start()
    for th in threads:
        th.join()

    for i in range(n_threads):
        assert t.get_usage(f"u{i}", "docs").current == per_thread


def test_thread_safety_mixed_operations():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 1_000_000))
    t.set_usage("u1", "docs", 1000, now=1.0)
    errors: list = []

    def reader():
        try:
            for _ in range(200):
                _ = t.get_usage("u1", "docs")
                _ = t.check("u1", "docs")
                _ = t.available("u1", "docs")
                _ = t.stats()
                _ = t.usage_for_key("u1")
                _ = t.keys_at_limit("docs")
        except Exception as exc:  # noqa: BLE001
            errors.append(exc)

    def writer():
        try:
            for _ in range(200):
                t.increment("u1", "docs", now=1.0)
                t.decrement("u1", "docs", now=1.0)
        except Exception as exc:  # noqa: BLE001
            errors.append(exc)

    threads = [threading.Thread(target=reader) for _ in range(4)] + [
        threading.Thread(target=writer) for _ in range(4)
    ]
    for th in threads:
        th.start()
    for th in threads:
        th.join()

    assert errors == []
    # net change from writers is zero
    assert t.get_usage("u1", "docs").current == 1000


def test_thread_safety_define_and_use():
    t = DocQuotaTracker()
    errors: list = []

    def definer():
        try:
            for i in range(100):
                t.define_quota(QuotaDefinition(f"r{i % 10}", 100))
        except Exception as exc:  # noqa: BLE001
            errors.append(exc)

    def user():
        try:
            for i in range(100):
                t.increment("u1", f"r{i % 10}", now=1.0)
        except Exception as exc:  # noqa: BLE001
            errors.append(exc)

    threads = [threading.Thread(target=definer) for _ in range(4)] + [
        threading.Thread(target=user) for _ in range(4)
    ]
    for th in threads:
        th.start()
    for th in threads:
        th.join()

    assert errors == []


# ---------------------------------------------------------------------- #
# Integration-style scenarios
# ---------------------------------------------------------------------- #
def test_full_lifecycle():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 3, "user docs"))

    assert t.check("alice", "docs", 1) is True
    t.increment("alice", "docs", now=1.0)
    t.increment("alice", "docs", now=2.0)
    t.increment("alice", "docs", now=3.0)
    assert t.check("alice", "docs", 1) is False
    assert "alice" in t.keys_at_limit("docs")

    t.decrement("alice", "docs", now=4.0)
    assert t.check("alice", "docs", 1) is True
    assert t.keys_at_limit("docs") == []


def test_multi_resource_per_key():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.define_quota(QuotaDefinition("storage_mb", 1024))
    t.define_quota(QuotaDefinition("api_calls", 1000))

    t.increment("alice", "docs", amount=5, now=1.0)
    t.increment("alice", "storage_mb", amount=512, now=1.0)
    t.increment("alice", "api_calls", amount=750, now=1.0)

    usages = t.usage_for_key("alice")
    assert len(usages) == 3
    assert {u.resource for u in usages} == {"docs", "storage_mb", "api_calls"}


def test_undefined_resource_is_inert():
    """Operations on undefined resources don't create usage."""
    t = DocQuotaTracker()
    assert t.increment("u1", "ghost") is None
    assert t.decrement("u1", "ghost") is None
    assert t.set_usage("u1", "ghost", 5) is None
    assert t.get_usage("u1", "ghost") is None
    assert t.usage_for_key("u1") == []


def test_increment_zero_amount():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", amount=5, now=1.0)
    u = t.increment("u1", "docs", amount=0, now=2.0)
    assert u.current == 5
    assert u.last_updated_at == 2.0


def test_check_amount_zero_when_over_limit():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 5))
    t.set_usage("u1", "docs", 10, now=1.0)
    assert t.check("u1", "docs", amount=0) is False


def test_set_usage_to_zero():
    t = DocQuotaTracker()
    t.define_quota(QuotaDefinition("docs", 10))
    t.increment("u1", "docs", amount=5, now=1.0)
    u = t.set_usage("u1", "docs", 0, now=2.0)
    assert u.current == 0
