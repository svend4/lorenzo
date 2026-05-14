"""Tests for E411 — doc_observer_chain."""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_observer_chain import (
    ChainStats,
    DocObserverChain,
    NotifyResult,
    Observer,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def noop(event_type, doc_id, payload):  # pragma: no cover - trivial
    return None


def echo(event_type, doc_id, payload):
    return {"echo": (event_type, doc_id)}


def record_to(sink):
    def _cb(event_type, doc_id, payload):
        sink.append((event_type, doc_id, dict(payload)))
        return None

    return _cb


def merge_kv(key, value):
    def _cb(event_type, doc_id, payload):
        return {key: value}

    return _cb


def raise_runtime(_e, _d, _p):
    raise RuntimeError("boom")


def raise_value(_e, _d, _p):
    raise ValueError("bad")


def returns_list(_e, _d, _p):
    return [1, 2, 3]


def returns_string(_e, _d, _p):
    return "not a dict"


# ---------------------------------------------------------------------------
class TestObserverDataclass:
    def test_observer_defaults(self):
        o = Observer(observer_id="x", event_type="evt")
        assert o.callback is None
        assert o.order == 0
        assert o.enabled is True

    def test_observer_fields(self):
        o = Observer(
            observer_id="abc",
            event_type="created",
            callback=noop,
            order=5,
            enabled=False,
        )
        assert o.observer_id == "abc"
        assert o.event_type == "created"
        assert o.callback is noop
        assert o.order == 5
        assert o.enabled is False


class TestNotifyResultDataclass:
    def test_notify_result_defaults(self):
        r = NotifyResult(event_type="e", doc_id="d")
        assert r.event_type == "e"
        assert r.doc_id == "d"
        assert r.observers_invoked == []
        assert r.final_payload == {}
        assert r.errors == []

    def test_notify_result_independence(self):
        a = NotifyResult(event_type="e", doc_id="d1")
        b = NotifyResult(event_type="e", doc_id="d2")
        a.observers_invoked.append("x")
        a.final_payload["k"] = 1
        a.errors.append("err")
        assert b.observers_invoked == []
        assert b.final_payload == {}
        assert b.errors == []


class TestChainStatsDataclass:
    def test_chain_stats(self):
        s = ChainStats(
            total_observers=3,
            enabled_observers=2,
            total_notifications=10,
            total_callbacks=15,
            total_errors=1,
        )
        assert s.total_observers == 3
        assert s.enabled_observers == 2
        assert s.total_notifications == 10
        assert s.total_callbacks == 15
        assert s.total_errors == 1


# ---------------------------------------------------------------------------
class TestRegisterObserver:
    def test_register_returns_observer(self):
        c = DocObserverChain()
        obs = c.register_observer("created", noop)
        assert isinstance(obs, Observer)
        assert obs.event_type == "created"
        assert obs.callback is noop
        assert obs.order == 0
        assert obs.enabled is True
        assert isinstance(obs.observer_id, str) and obs.observer_id

    def test_register_assigns_unique_ids(self):
        c = DocObserverChain()
        a = c.register_observer("e", noop)
        b = c.register_observer("e", noop)
        assert a.observer_id != b.observer_id

    def test_register_custom_order(self):
        c = DocObserverChain()
        obs = c.register_observer("e", noop, order=7)
        assert obs.order == 7

    def test_register_empty_event_type(self):
        c = DocObserverChain()
        with pytest.raises(ValueError):
            c.register_observer("", noop)

    def test_register_non_string_event_type(self):
        c = DocObserverChain()
        with pytest.raises(ValueError):
            c.register_observer(123, noop)  # type: ignore[arg-type]

    def test_register_non_callable(self):
        c = DocObserverChain()
        with pytest.raises(ValueError):
            c.register_observer("e", "not callable")  # type: ignore[arg-type]

    def test_register_non_int_order(self):
        c = DocObserverChain()
        with pytest.raises(ValueError):
            c.register_observer("e", noop, order="x")  # type: ignore[arg-type]

    def test_register_stored(self):
        c = DocObserverChain()
        obs = c.register_observer("e", noop)
        assert c.get_observer(obs.observer_id) is obs


# ---------------------------------------------------------------------------
class TestUnregisterObserver:
    def test_unregister_existing(self):
        c = DocObserverChain()
        obs = c.register_observer("e", noop)
        assert c.unregister_observer(obs.observer_id) is True
        assert c.get_observer(obs.observer_id) is None

    def test_unregister_missing(self):
        c = DocObserverChain()
        assert c.unregister_observer("missing") is False

    def test_unregister_twice(self):
        c = DocObserverChain()
        obs = c.register_observer("e", noop)
        c.unregister_observer(obs.observer_id)
        assert c.unregister_observer(obs.observer_id) is False


# ---------------------------------------------------------------------------
class TestEnableDisable:
    def test_disable(self):
        c = DocObserverChain()
        obs = c.register_observer("e", noop)
        assert c.disable_observer(obs.observer_id) is True
        assert c.get_observer(obs.observer_id).enabled is False

    def test_enable_after_disable(self):
        c = DocObserverChain()
        obs = c.register_observer("e", noop)
        c.disable_observer(obs.observer_id)
        assert c.enable_observer(obs.observer_id) is True
        assert c.get_observer(obs.observer_id).enabled is True

    def test_enable_missing(self):
        c = DocObserverChain()
        assert c.enable_observer("missing") is False

    def test_disable_missing(self):
        c = DocObserverChain()
        assert c.disable_observer("missing") is False

    def test_double_enable_is_idempotent(self):
        c = DocObserverChain()
        obs = c.register_observer("e", noop)
        c.enable_observer(obs.observer_id)
        c.enable_observer(obs.observer_id)
        assert c.get_observer(obs.observer_id).enabled is True


# ---------------------------------------------------------------------------
class TestGetObserver:
    def test_get_existing(self):
        c = DocObserverChain()
        obs = c.register_observer("e", noop)
        got = c.get_observer(obs.observer_id)
        assert got is obs

    def test_get_missing(self):
        c = DocObserverChain()
        assert c.get_observer("nope") is None


# ---------------------------------------------------------------------------
class TestListObservers:
    def test_list_empty(self):
        c = DocObserverChain()
        assert c.list_observers() == []

    def test_list_returns_all(self):
        c = DocObserverChain()
        a = c.register_observer("e1", noop)
        b = c.register_observer("e2", noop)
        ids = {o.observer_id for o in c.list_observers()}
        assert ids == {a.observer_id, b.observer_id}

    def test_list_filter_by_event_type(self):
        c = DocObserverChain()
        a = c.register_observer("created", noop)
        c.register_observer("deleted", noop)
        results = c.list_observers(event_type="created")
        assert len(results) == 1
        assert results[0].observer_id == a.observer_id

    def test_list_filter_unknown_event(self):
        c = DocObserverChain()
        c.register_observer("e", noop)
        assert c.list_observers(event_type="other") == []

    def test_list_sorted_by_order_then_id(self):
        c = DocObserverChain()
        # Register out of order
        o3 = c.register_observer("e", noop, order=5)
        o1 = c.register_observer("e", noop, order=1)
        o2 = c.register_observer("e", noop, order=3)
        seq = c.list_observers()
        assert [o.observer_id for o in seq] == [
            o1.observer_id,
            o2.observer_id,
            o3.observer_id,
        ]

    def test_list_stable_tie_break_by_id(self):
        c = DocObserverChain()
        a = c.register_observer("e", noop, order=0)
        b = c.register_observer("e", noop, order=0)
        ordered = c.list_observers()
        expected = sorted([a.observer_id, b.observer_id])
        assert [o.observer_id for o in ordered] == expected


# ---------------------------------------------------------------------------
class TestClearObservers:
    def test_clear_returns_count(self):
        c = DocObserverChain()
        c.register_observer("e", noop)
        c.register_observer("e", noop)
        assert c.clear_observers() == 2
        assert c.list_observers() == []

    def test_clear_empty(self):
        c = DocObserverChain()
        assert c.clear_observers() == 0


# ---------------------------------------------------------------------------
class TestNotifyBasics:
    def test_notify_no_observers(self):
        c = DocObserverChain()
        r = c.notify("created", "doc-1")
        assert isinstance(r, NotifyResult)
        assert r.event_type == "created"
        assert r.doc_id == "doc-1"
        assert r.observers_invoked == []
        assert r.final_payload == {}
        assert r.errors == []

    def test_notify_passes_event_and_doc(self):
        c = DocObserverChain()
        sink = []
        c.register_observer("e", record_to(sink))
        c.notify("e", "doc-99", {"a": 1})
        assert sink == [("e", "doc-99", {"a": 1})]

    def test_notify_default_payload_is_empty_dict(self):
        c = DocObserverChain()
        sink = []
        c.register_observer("e", record_to(sink))
        c.notify("e", "d")
        assert sink == [("e", "d", {})]

    def test_notify_invalid_event_type(self):
        c = DocObserverChain()
        with pytest.raises(ValueError):
            c.notify("", "d")

    def test_notify_invalid_doc_id(self):
        c = DocObserverChain()
        with pytest.raises(ValueError):
            c.notify("e", "")

    def test_notify_invalid_payload_type(self):
        c = DocObserverChain()
        with pytest.raises(TypeError):
            c.notify("e", "d", payload="not a dict")  # type: ignore[arg-type]

    def test_notify_filters_by_event_type(self):
        c = DocObserverChain()
        s1 = []
        s2 = []
        c.register_observer("e1", record_to(s1))
        c.register_observer("e2", record_to(s2))
        c.notify("e1", "d")
        assert s1 and not s2

    def test_notify_skips_disabled(self):
        c = DocObserverChain()
        sink = []
        obs = c.register_observer("e", record_to(sink))
        c.disable_observer(obs.observer_id)
        r = c.notify("e", "d")
        assert sink == []
        assert r.observers_invoked == []


# ---------------------------------------------------------------------------
class TestNotifyOrdering:
    def test_observers_invoked_in_order(self):
        c = DocObserverChain()
        sink = []

        def make(tag):
            def _cb(_e, _d, _p):
                sink.append(tag)
                return None

            return _cb

        c.register_observer("e", make("c"), order=10)
        c.register_observer("e", make("a"), order=1)
        c.register_observer("e", make("b"), order=5)
        c.notify("e", "d")
        assert sink == ["a", "b", "c"]

    def test_invoked_ids_listed_in_order(self):
        c = DocObserverChain()
        third = c.register_observer("e", noop, order=10)
        first = c.register_observer("e", noop, order=1)
        second = c.register_observer("e", noop, order=5)
        r = c.notify("e", "d")
        assert r.observers_invoked == [
            first.observer_id,
            second.observer_id,
            third.observer_id,
        ]


# ---------------------------------------------------------------------------
class TestChainMerging:
    def test_dict_return_merges(self):
        c = DocObserverChain()
        c.register_observer("e", merge_kv("a", 1), order=1)
        c.register_observer("e", merge_kv("b", 2), order=2)
        r = c.notify("e", "d")
        assert r.final_payload == {"a": 1, "b": 2}

    def test_later_observer_sees_merged_payload(self):
        c = DocObserverChain()
        c.register_observer("e", merge_kv("k", "first"), order=1)

        seen = {}

        def grab(_e, _d, payload):
            seen.update(payload)
            return None

        c.register_observer("e", grab, order=2)
        c.notify("e", "d")
        assert seen == {"k": "first"}

    def test_later_overwrites_earlier(self):
        c = DocObserverChain()
        c.register_observer("e", merge_kv("k", 1), order=1)
        c.register_observer("e", merge_kv("k", 2), order=2)
        r = c.notify("e", "d")
        assert r.final_payload == {"k": 2}

    def test_none_return_does_not_merge(self):
        c = DocObserverChain()
        c.register_observer("e", noop, order=1)
        c.register_observer("e", merge_kv("only", "me"), order=2)
        r = c.notify("e", "d")
        assert r.final_payload == {"only": "me"}

    def test_initial_payload_preserved_when_not_overwritten(self):
        c = DocObserverChain()
        c.register_observer("e", merge_kv("extra", 1))
        r = c.notify("e", "d", payload={"original": True})
        assert r.final_payload == {"original": True, "extra": 1}

    def test_input_payload_not_mutated(self):
        c = DocObserverChain()
        c.register_observer("e", merge_kv("x", 1))
        payload = {"a": 1}
        c.notify("e", "d", payload=payload)
        assert payload == {"a": 1}


# ---------------------------------------------------------------------------
class TestNotifyErrors:
    def test_callback_exception_recorded(self):
        c = DocObserverChain()
        obs = c.register_observer("e", raise_runtime)
        r = c.notify("e", "d")
        assert len(r.errors) == 1
        assert obs.observer_id in r.errors[0]
        assert "RuntimeError" in r.errors[0]
        assert "boom" in r.errors[0]

    def test_exception_continues_chain(self):
        c = DocObserverChain()
        c.register_observer("e", raise_runtime, order=1)
        c.register_observer("e", merge_kv("k", 1), order=2)
        r = c.notify("e", "d")
        assert r.final_payload == {"k": 1}
        assert len(r.errors) == 1
        assert len(r.observers_invoked) == 2

    def test_multiple_exceptions(self):
        c = DocObserverChain()
        c.register_observer("e", raise_runtime, order=1)
        c.register_observer("e", raise_value, order=2)
        r = c.notify("e", "d")
        assert len(r.errors) == 2

    def test_non_dict_return_recorded_as_error(self):
        c = DocObserverChain()
        c.register_observer("e", returns_list)
        r = c.notify("e", "d")
        assert len(r.errors) == 1
        assert "non-dict" in r.errors[0]

    def test_non_dict_return_continues_chain(self):
        c = DocObserverChain()
        c.register_observer("e", returns_string, order=1)
        c.register_observer("e", merge_kv("survives", True), order=2)
        r = c.notify("e", "d")
        assert r.final_payload == {"survives": True}
        assert len(r.errors) == 1

    def test_observers_invoked_includes_failing(self):
        c = DocObserverChain()
        obs = c.register_observer("e", raise_runtime)
        r = c.notify("e", "d")
        assert obs.observer_id in r.observers_invoked


# ---------------------------------------------------------------------------
class TestStats:
    def test_initial_stats(self):
        c = DocObserverChain()
        s = c.stats()
        assert s.total_observers == 0
        assert s.enabled_observers == 0
        assert s.total_notifications == 0
        assert s.total_callbacks == 0
        assert s.total_errors == 0

    def test_stats_count_observers(self):
        c = DocObserverChain()
        c.register_observer("e", noop)
        c.register_observer("e", noop)
        s = c.stats()
        assert s.total_observers == 2
        assert s.enabled_observers == 2

    def test_stats_enabled_count(self):
        c = DocObserverChain()
        a = c.register_observer("e", noop)
        c.register_observer("e", noop)
        c.disable_observer(a.observer_id)
        s = c.stats()
        assert s.total_observers == 2
        assert s.enabled_observers == 1

    def test_stats_notifications_increment(self):
        c = DocObserverChain()
        c.notify("e", "d")
        c.notify("e", "d")
        c.notify("e", "d")
        assert c.stats().total_notifications == 3

    def test_stats_callbacks_count(self):
        c = DocObserverChain()
        c.register_observer("e", noop)
        c.register_observer("e", noop)
        c.notify("e", "d")
        c.notify("e", "d")
        assert c.stats().total_callbacks == 4

    def test_stats_errors_count(self):
        c = DocObserverChain()
        c.register_observer("e", raise_runtime)
        c.register_observer("e", noop)
        c.notify("e", "d")
        c.notify("e", "d")
        assert c.stats().total_errors == 2

    def test_stats_includes_non_dict_errors(self):
        c = DocObserverChain()
        c.register_observer("e", returns_list)
        c.notify("e", "d")
        assert c.stats().total_errors == 1

    def test_stats_returns_chain_stats(self):
        c = DocObserverChain()
        assert isinstance(c.stats(), ChainStats)


# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_registration(self):
        c = DocObserverChain()

        def register():
            for _ in range(50):
                c.register_observer("e", noop)

        threads = [threading.Thread(target=register) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(c.list_observers()) == 200

    def test_concurrent_notify(self):
        c = DocObserverChain()
        counter = {"n": 0}
        lock = threading.Lock()

        def cb(_e, _d, _p):
            with lock:
                counter["n"] += 1
            return None

        c.register_observer("e", cb)

        def notify_many():
            for _ in range(50):
                c.notify("e", "d")

        threads = [threading.Thread(target=notify_many) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert counter["n"] == 200
        assert c.stats().total_notifications == 200
        assert c.stats().total_callbacks == 200

    def test_concurrent_mixed_ops(self):
        c = DocObserverChain()
        # Pre-register some observers
        ids = [c.register_observer("e", noop).observer_id for _ in range(5)]

        def reg():
            for _ in range(20):
                c.register_observer("e", noop)

        def notif():
            for _ in range(20):
                c.notify("e", "d")

        def toggle():
            for oid in ids:
                c.disable_observer(oid)
                c.enable_observer(oid)

        threads = [
            threading.Thread(target=reg),
            threading.Thread(target=notif),
            threading.Thread(target=toggle),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # No crash, observers grow predictably
        assert len(c.list_observers()) >= 5

    def test_callback_invoked_outside_lock(self):
        """A callback can register another observer without deadlock."""
        c = DocObserverChain()
        c.register_observer("e", lambda _e, _d, _p: c.register_observer("e2", noop))
        # Should not deadlock
        r = c.notify("e", "d")
        assert len(r.observers_invoked) == 1
        # The newly added observer exists
        assert any(o.event_type == "e2" for o in c.list_observers())

    def test_slow_callback_does_not_block_other_chains(self):
        """A slow callback must not hold the chain's lock during execution."""
        c = DocObserverChain()
        gate = threading.Event()

        def slow(_e, _d, _p):
            gate.wait(timeout=2.0)
            return None

        c.register_observer("slow", slow)

        results = {}

        def notify_slow():
            results["slow"] = c.notify("slow", "d")

        t = threading.Thread(target=notify_slow)
        t.start()
        # Give thread a moment to enter the slow callback
        time.sleep(0.05)
        # This must not block on the slow callback's lock
        stats = c.stats()
        assert stats.total_observers == 1
        gate.set()
        t.join(timeout=3.0)
        assert not t.is_alive()


# ---------------------------------------------------------------------------
class TestIntegration:
    def test_full_workflow(self):
        c = DocObserverChain()
        a = c.register_observer("doc.created", merge_kv("step", "a"), order=1)
        b = c.register_observer("doc.created", merge_kv("more", True), order=2)
        c.register_observer("doc.deleted", noop)
        r = c.notify("doc.created", "doc-1", {"start": 1})
        assert r.final_payload == {"start": 1, "step": "a", "more": True}
        assert r.observers_invoked == [a.observer_id, b.observer_id]
        s = c.stats()
        assert s.total_observers == 3
        assert s.total_notifications == 1
        assert s.total_callbacks == 2
        assert s.total_errors == 0

    def test_disable_unregister_lifecycle(self):
        c = DocObserverChain()
        obs = c.register_observer("e", merge_kv("v", 1))
        assert c.notify("e", "d").final_payload == {"v": 1}
        c.disable_observer(obs.observer_id)
        assert c.notify("e", "d").final_payload == {}
        c.enable_observer(obs.observer_id)
        assert c.notify("e", "d").final_payload == {"v": 1}
        c.unregister_observer(obs.observer_id)
        assert c.notify("e", "d").final_payload == {}

    def test_clear_resets_observers_but_keeps_counters(self):
        c = DocObserverChain()
        c.register_observer("e", noop)
        c.notify("e", "d")
        c.clear_observers()
        s = c.stats()
        assert s.total_observers == 0
        assert s.total_notifications == 1
        assert s.total_callbacks == 1
