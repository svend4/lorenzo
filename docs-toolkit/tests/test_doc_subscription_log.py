"""Tests for E426 DocSubscriptionLog."""
import threading
import time

import pytest

from docstoolkit.doc_subscription_log import (
    DocSubscriptionLog,
    SubLogEntry,
    SubLogStats,
)


# ----------------------------------------------------------------------
# Construction & basic logging
# ----------------------------------------------------------------------

def test_construct_empty():
    log = DocSubscriptionLog()
    assert log.stats().total_entries == 0


def test_log_returns_entry():
    log = DocSubscriptionLog()
    e = log.log("alice", "subscribe", "doc1")
    assert isinstance(e, SubLogEntry)
    assert e.subscriber_id == "alice"
    assert e.event == "subscribe"
    assert e.target == "doc1"


def test_log_assigns_entry_id_from_1():
    log = DocSubscriptionLog()
    e1 = log.log("a", "subscribe", "t1")
    e2 = log.log("b", "subscribe", "t2")
    assert e1.entry_id == 1
    assert e2.entry_id == 2


def test_log_entry_ids_monotonic():
    log = DocSubscriptionLog()
    ids = [log.log(f"s{i}", "subscribe", "t").entry_id for i in range(10)]
    assert ids == list(range(1, 11))


def test_log_with_explicit_now():
    log = DocSubscriptionLog()
    e = log.log("a", "subscribe", "t", now=100.0)
    assert e.timestamp == 100.0


def test_log_default_now_uses_time(monkeypatch):
    log = DocSubscriptionLog()
    monkeypatch.setattr(time, "time", lambda: 555.5)
    e = log.log("a", "subscribe", "t")
    assert e.timestamp == 555.5


def test_log_default_details_empty():
    log = DocSubscriptionLog()
    e = log.log("a", "subscribe", "t")
    assert e.details == ""


def test_log_with_details():
    log = DocSubscriptionLog()
    e = log.log("a", "subscribe", "t", details="newsletter signup")
    assert e.details == "newsletter signup"


def test_log_all_event_types():
    log = DocSubscriptionLog()
    for ev in ("subscribe", "unsubscribe", "reactivate", "expire"):
        e = log.log("a", ev, "t", now=1.0)
        assert e.event == ev


# ----------------------------------------------------------------------
# get_entry
# ----------------------------------------------------------------------

def test_get_entry_existing():
    log = DocSubscriptionLog()
    e = log.log("a", "subscribe", "t")
    got = log.get_entry(e.entry_id)
    assert got is not None
    assert got.entry_id == e.entry_id
    assert got.subscriber_id == "a"


def test_get_entry_missing_returns_none():
    log = DocSubscriptionLog()
    assert log.get_entry(999) is None


def test_get_entry_zero_missing():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t")
    assert log.get_entry(0) is None


def test_get_entry_after_delete_returns_none():
    log = DocSubscriptionLog()
    e = log.log("a", "subscribe", "t", now=10.0)
    log.log("b", "subscribe", "t", now=20.0)
    log.delete_old(before_timestamp=15.0)
    assert log.get_entry(e.entry_id) is None


# ----------------------------------------------------------------------
# entries_for_subscriber
# ----------------------------------------------------------------------

def test_entries_for_subscriber_empty():
    log = DocSubscriptionLog()
    assert log.entries_for_subscriber("nobody") == []


def test_entries_for_subscriber_most_recent_first():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t1", now=1.0)
    log.log("a", "subscribe", "t2", now=2.0)
    log.log("a", "unsubscribe", "t1", now=3.0)
    res = log.entries_for_subscriber("a")
    assert [e.entry_id for e in res] == [3, 2, 1]


def test_entries_for_subscriber_filtered_by_event():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t1", now=1.0)
    log.log("a", "unsubscribe", "t1", now=2.0)
    log.log("a", "subscribe", "t2", now=3.0)
    res = log.entries_for_subscriber("a", event="subscribe")
    assert [e.target for e in res] == ["t2", "t1"]


def test_entries_for_subscriber_limit():
    log = DocSubscriptionLog()
    for i in range(5):
        log.log("a", "subscribe", f"t{i}", now=float(i))
    res = log.entries_for_subscriber("a", limit=2)
    assert len(res) == 2
    assert res[0].target == "t4"


def test_entries_for_subscriber_other_subscribers_excluded():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t")
    log.log("b", "subscribe", "t")
    res = log.entries_for_subscriber("a")
    assert len(res) == 1
    assert res[0].subscriber_id == "a"


# ----------------------------------------------------------------------
# entries_for_target
# ----------------------------------------------------------------------

def test_entries_for_target_empty():
    log = DocSubscriptionLog()
    assert log.entries_for_target("missing") == []


def test_entries_for_target_most_recent_first():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "topic", now=1.0)
    log.log("b", "subscribe", "topic", now=2.0)
    log.log("a", "unsubscribe", "topic", now=3.0)
    res = log.entries_for_target("topic")
    assert [e.entry_id for e in res] == [3, 2, 1]


def test_entries_for_target_limit():
    log = DocSubscriptionLog()
    for i in range(4):
        log.log(f"s{i}", "subscribe", "topic", now=float(i))
    res = log.entries_for_target("topic", limit=2)
    assert len(res) == 2


def test_entries_for_target_other_targets_excluded():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "doc1")
    log.log("a", "subscribe", "doc2")
    res = log.entries_for_target("doc1")
    assert len(res) == 1
    assert res[0].target == "doc1"


# ----------------------------------------------------------------------
# entries_by_event
# ----------------------------------------------------------------------

def test_entries_by_event_empty():
    log = DocSubscriptionLog()
    assert log.entries_by_event("subscribe") == []


def test_entries_by_event_most_recent_first():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t1", now=1.0)
    log.log("a", "subscribe", "t2", now=2.0)
    log.log("a", "unsubscribe", "t2", now=3.0)
    res = log.entries_by_event("subscribe")
    assert [e.target for e in res] == ["t2", "t1"]


def test_entries_by_event_limit():
    log = DocSubscriptionLog()
    for i in range(5):
        log.log("a", "subscribe", f"t{i}", now=float(i))
    res = log.entries_by_event("subscribe", limit=3)
    assert len(res) == 3


def test_entries_by_event_other_events_excluded():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t")
    log.log("a", "unsubscribe", "t")
    log.log("a", "expire", "t")
    assert len(log.entries_by_event("expire")) == 1


# ----------------------------------------------------------------------
# entries_in_range
# ----------------------------------------------------------------------

def test_entries_in_range_inclusive():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=1.0)
    log.log("a", "subscribe", "t", now=5.0)
    log.log("a", "subscribe", "t", now=10.0)
    res = log.entries_in_range(1.0, 10.0)
    assert len(res) == 3


def test_entries_in_range_excludes_outside():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=1.0)
    log.log("a", "subscribe", "t", now=5.0)
    log.log("a", "subscribe", "t", now=10.0)
    res = log.entries_in_range(2.0, 9.0)
    assert len(res) == 1
    assert res[0].timestamp == 5.0


def test_entries_in_range_sorted_asc():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=10.0)
    log.log("a", "subscribe", "t", now=1.0)
    log.log("a", "subscribe", "t", now=5.0)
    res = log.entries_in_range(0.0, 100.0)
    assert [e.timestamp for e in res] == [1.0, 5.0, 10.0]


def test_entries_in_range_filtered_by_subscriber():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=1.0)
    log.log("b", "subscribe", "t", now=2.0)
    log.log("a", "subscribe", "t", now=3.0)
    res = log.entries_in_range(0.0, 10.0, subscriber_id="a")
    assert len(res) == 2
    assert all(e.subscriber_id == "a" for e in res)


def test_entries_in_range_empty():
    log = DocSubscriptionLog()
    assert log.entries_in_range(0.0, 100.0) == []


def test_entries_in_range_stable_for_same_timestamp():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t1", now=5.0)
    log.log("a", "subscribe", "t2", now=5.0)
    res = log.entries_in_range(0.0, 10.0)
    assert [e.entry_id for e in res] == [1, 2]


# ----------------------------------------------------------------------
# is_currently_subscribed
# ----------------------------------------------------------------------

def test_is_currently_subscribed_no_history():
    log = DocSubscriptionLog()
    assert log.is_currently_subscribed("a", "t") is False


def test_is_currently_subscribed_after_subscribe():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=1.0)
    assert log.is_currently_subscribed("a", "t") is True


def test_is_currently_subscribed_after_unsubscribe():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=1.0)
    log.log("a", "unsubscribe", "t", now=2.0)
    assert log.is_currently_subscribed("a", "t") is False


def test_is_currently_subscribed_after_expire():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=1.0)
    log.log("a", "expire", "t", now=2.0)
    assert log.is_currently_subscribed("a", "t") is False


def test_is_currently_subscribed_after_reactivate():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=1.0)
    log.log("a", "unsubscribe", "t", now=2.0)
    log.log("a", "reactivate", "t", now=3.0)
    assert log.is_currently_subscribed("a", "t") is True


def test_is_currently_subscribed_lifecycle():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=1.0)
    log.log("a", "expire", "t", now=2.0)
    log.log("a", "reactivate", "t", now=3.0)
    log.log("a", "unsubscribe", "t", now=4.0)
    assert log.is_currently_subscribed("a", "t") is False


def test_is_currently_subscribed_other_target_ignored():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t1", now=1.0)
    log.log("a", "unsubscribe", "t2", now=2.0)
    assert log.is_currently_subscribed("a", "t1") is True
    assert log.is_currently_subscribed("a", "t2") is False


# ----------------------------------------------------------------------
# last_event_for
# ----------------------------------------------------------------------

def test_last_event_for_none():
    log = DocSubscriptionLog()
    assert log.last_event_for("a", "t") is None


def test_last_event_for_single():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=1.0)
    e = log.last_event_for("a", "t")
    assert e is not None
    assert e.event == "subscribe"


def test_last_event_for_returns_most_recent():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=1.0)
    log.log("a", "unsubscribe", "t", now=2.0)
    log.log("a", "reactivate", "t", now=3.0)
    e = log.last_event_for("a", "t")
    assert e.event == "reactivate"


def test_last_event_for_other_target_none():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t1")
    assert log.last_event_for("a", "t2") is None


# ----------------------------------------------------------------------
# subscriber_history
# ----------------------------------------------------------------------

def test_subscriber_history_empty():
    log = DocSubscriptionLog()
    assert log.subscriber_history("a") == {}


def test_subscriber_history_basic():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t1", now=1.0)
    log.log("a", "subscribe", "t2", now=2.0)
    log.log("a", "unsubscribe", "t1", now=3.0)
    hist = log.subscriber_history("a")
    assert hist == {"t1": "not_subscribed", "t2": "subscribed"}


def test_subscriber_history_multiple_targets():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t1", now=1.0)
    log.log("a", "subscribe", "t2", now=2.0)
    log.log("a", "subscribe", "t3", now=3.0)
    log.log("a", "expire", "t3", now=4.0)
    hist = log.subscriber_history("a")
    assert hist["t1"] == "subscribed"
    assert hist["t2"] == "subscribed"
    assert hist["t3"] == "not_subscribed"


def test_subscriber_history_reactivation():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=1.0)
    log.log("a", "unsubscribe", "t", now=2.0)
    log.log("a", "reactivate", "t", now=3.0)
    assert log.subscriber_history("a") == {"t": "subscribed"}


# ----------------------------------------------------------------------
# delete_old
# ----------------------------------------------------------------------

def test_delete_old_removes_entries():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=1.0)
    log.log("a", "subscribe", "t", now=2.0)
    log.log("a", "subscribe", "t", now=3.0)
    removed = log.delete_old(before_timestamp=2.5)
    assert removed == 2
    assert log.stats().total_entries == 1


def test_delete_old_zero_when_nothing_old():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=10.0)
    assert log.delete_old(before_timestamp=5.0) == 0


def test_delete_old_rebuilds_indexes():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=1.0)
    log.log("a", "subscribe", "t", now=10.0)
    log.delete_old(before_timestamp=5.0)
    res = log.entries_for_subscriber("a")
    assert len(res) == 1
    assert res[0].timestamp == 10.0


def test_delete_old_preserves_newer_entries():
    log = DocSubscriptionLog()
    e_old = log.log("a", "subscribe", "t", now=1.0)
    e_new = log.log("a", "subscribe", "t", now=10.0)
    log.delete_old(before_timestamp=5.0)
    assert log.get_entry(e_old.entry_id) is None
    assert log.get_entry(e_new.entry_id) is not None


def test_delete_old_does_not_reset_next_id():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=1.0)
    log.log("a", "subscribe", "t", now=2.0)
    log.delete_old(before_timestamp=10.0)
    e = log.log("a", "subscribe", "t", now=20.0)
    assert e.entry_id == 3


def test_delete_old_indexes_consistent_after():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t1", now=1.0)
    log.log("b", "subscribe", "t2", now=2.0)
    log.log("a", "subscribe", "t1", now=10.0)
    log.delete_old(before_timestamp=5.0)
    s = log.stats()
    assert s.unique_subscribers == 1
    assert s.unique_targets == 1


# ----------------------------------------------------------------------
# stats
# ----------------------------------------------------------------------

def test_stats_empty():
    log = DocSubscriptionLog()
    s = log.stats()
    assert s.total_entries == 0
    assert s.unique_subscribers == 0
    assert s.unique_targets == 0
    assert s.event_counts == {}


def test_stats_total():
    log = DocSubscriptionLog()
    for i in range(7):
        log.log(f"s{i}", "subscribe", f"t{i}")
    assert log.stats().total_entries == 7


def test_stats_unique_subscribers():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t")
    log.log("a", "subscribe", "t2")
    log.log("b", "subscribe", "t")
    assert log.stats().unique_subscribers == 2


def test_stats_unique_targets():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t1")
    log.log("a", "subscribe", "t2")
    log.log("b", "subscribe", "t1")
    assert log.stats().unique_targets == 2


def test_stats_event_counts():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t")
    log.log("a", "subscribe", "t2")
    log.log("a", "unsubscribe", "t")
    log.log("a", "expire", "t2")
    s = log.stats()
    assert s.event_counts == {"subscribe": 2, "unsubscribe": 1, "expire": 1}


def test_stats_is_sublogstats_instance():
    log = DocSubscriptionLog()
    assert isinstance(log.stats(), SubLogStats)


# ----------------------------------------------------------------------
# Dataclass behaviour
# ----------------------------------------------------------------------

def test_sublogentry_defaults():
    e = SubLogEntry()
    assert e.entry_id == 0
    assert e.timestamp == 0.0
    assert e.details == ""


def test_sublogstats_defaults():
    s = SubLogStats()
    assert s.total_entries == 0
    assert s.event_counts == {}


def test_sublogstats_event_counts_independent():
    a = SubLogStats()
    b = SubLogStats()
    a.event_counts["x"] = 1
    assert "x" not in b.event_counts


# ----------------------------------------------------------------------
# Thread safety
# ----------------------------------------------------------------------

def test_threadsafe_concurrent_log():
    log = DocSubscriptionLog()
    n_threads = 8
    per_thread = 50

    def worker(tid: int):
        for i in range(per_thread):
            log.log(f"sub{tid}", "subscribe", f"t{i}", now=float(i))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    s = log.stats()
    assert s.total_entries == n_threads * per_thread
    assert s.unique_subscribers == n_threads


def test_threadsafe_unique_entry_ids():
    log = DocSubscriptionLog()
    n_threads = 8
    per_thread = 50
    ids: list[int] = []
    ids_lock = threading.Lock()

    def worker():
        local = []
        for _ in range(per_thread):
            local.append(log.log("a", "subscribe", "t").entry_id)
        with ids_lock:
            ids.extend(local)

    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(ids) == n_threads * per_thread
    assert len(set(ids)) == len(ids)  # all unique


def test_threadsafe_mixed_read_write():
    log = DocSubscriptionLog()
    stop = threading.Event()

    def writer():
        i = 0
        while not stop.is_set():
            log.log("a", "subscribe", f"t{i}", now=float(i))
            i += 1

    def reader():
        while not stop.is_set():
            log.stats()
            log.entries_for_subscriber("a", limit=10)

    threads = [threading.Thread(target=writer) for _ in range(2)]
    threads += [threading.Thread(target=reader) for _ in range(2)]
    for t in threads:
        t.start()
    time.sleep(0.2)
    stop.set()
    for t in threads:
        t.join()

    # If we got here without exceptions, the lock is working
    assert log.stats().total_entries > 0


# ----------------------------------------------------------------------
# Integration scenarios
# ----------------------------------------------------------------------

def test_integration_full_lifecycle():
    log = DocSubscriptionLog()
    log.log("alice", "subscribe", "weekly", now=1.0)
    log.log("alice", "subscribe", "daily", now=2.0)
    log.log("bob", "subscribe", "weekly", now=3.0)
    log.log("alice", "unsubscribe", "daily", now=4.0)
    log.log("alice", "expire", "weekly", now=5.0)
    log.log("alice", "reactivate", "weekly", now=6.0)

    assert log.is_currently_subscribed("alice", "weekly") is True
    assert log.is_currently_subscribed("alice", "daily") is False
    assert log.is_currently_subscribed("bob", "weekly") is True

    hist = log.subscriber_history("alice")
    assert hist == {"weekly": "subscribed", "daily": "not_subscribed"}


def test_integration_query_by_target_then_event():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "doc1", now=1.0)
    log.log("b", "subscribe", "doc1", now=2.0)
    log.log("c", "subscribe", "doc2", now=3.0)
    log.log("a", "unsubscribe", "doc1", now=4.0)

    target_events = log.entries_for_target("doc1")
    assert len(target_events) == 3

    subs = log.entries_by_event("subscribe")
    assert len(subs) == 3


def test_integration_range_with_subscriber_filter():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=1.0)
    log.log("b", "subscribe", "t", now=2.0)
    log.log("a", "subscribe", "t2", now=3.0)
    log.log("a", "unsubscribe", "t", now=4.0)
    log.log("b", "subscribe", "t2", now=5.0)

    res = log.entries_in_range(1.5, 4.5, subscriber_id="a")
    assert len(res) == 2
    assert all(e.subscriber_id == "a" for e in res)
    assert [e.timestamp for e in res] == [3.0, 4.0]


def test_integration_delete_then_continue_logging():
    log = DocSubscriptionLog()
    log.log("a", "subscribe", "t", now=1.0)
    log.log("a", "subscribe", "t2", now=2.0)
    log.delete_old(before_timestamp=10.0)
    assert log.stats().total_entries == 0

    e = log.log("a", "subscribe", "t3", now=20.0)
    assert e.entry_id == 3
    assert log.stats().total_entries == 1


def test_integration_get_entry_post_partial_delete():
    log = DocSubscriptionLog()
    e1 = log.log("a", "subscribe", "t", now=1.0)
    e2 = log.log("a", "subscribe", "t", now=10.0)
    e3 = log.log("a", "subscribe", "t", now=20.0)
    log.delete_old(before_timestamp=5.0)
    assert log.get_entry(e1.entry_id) is None
    assert log.get_entry(e2.entry_id) is not None
    assert log.get_entry(e3.entry_id) is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
