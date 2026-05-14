"""Tests for docstoolkit.doc_change_dispatcher (E405)."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_change_dispatcher import (
    DispatcherStats,
    DispatchResult,
    DocChangeDispatcher,
    Handler,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------
class TestHandlerDataclass:
    def test_full_construction(self):
        cb = lambda d, c, p: None
        h = Handler(
            handler_id="abc",
            change_type="created",
            callback=cb,
            priority=5,
            enabled=True,
        )
        assert h.handler_id == "abc"
        assert h.change_type == "created"
        assert h.callback is cb
        assert h.priority == 5
        assert h.enabled is True

    def test_default_callback_is_none(self):
        h = Handler(handler_id="x", change_type="updated")
        assert h.callback is None

    def test_default_priority_is_zero(self):
        h = Handler(handler_id="x", change_type="updated")
        assert h.priority == 0

    def test_default_enabled_is_true(self):
        h = Handler(handler_id="x", change_type="updated")
        assert h.enabled is True

    def test_equality(self):
        h1 = Handler(handler_id="x", change_type="t", callback=None, priority=0)
        h2 = Handler(handler_id="x", change_type="t", callback=None, priority=0)
        assert h1 == h2


class TestDispatchResultDataclass:
    def test_basic_construction(self):
        r = DispatchResult(doc_id="doc1", change_type="created")
        assert r.doc_id == "doc1"
        assert r.change_type == "created"

    def test_defaults(self):
        r = DispatchResult(doc_id="d", change_type="t")
        assert r.delivered_count == 0
        assert r.failed_count == 0
        assert r.handlers_invoked == []
        assert r.errors == []

    def test_handlers_invoked_independent(self):
        r1 = DispatchResult(doc_id="d", change_type="t")
        r2 = DispatchResult(doc_id="d", change_type="t")
        r1.handlers_invoked.append("a")
        assert r2.handlers_invoked == []

    def test_errors_independent(self):
        r1 = DispatchResult(doc_id="d", change_type="t")
        r2 = DispatchResult(doc_id="d", change_type="t")
        r1.errors.append("boom")
        assert r2.errors == []


class TestDispatcherStatsDataclass:
    def test_construction(self):
        s = DispatcherStats(
            total_handlers=1,
            enabled_handlers=1,
            total_dispatches=2,
            total_deliveries=3,
            total_failures=0,
        )
        assert s.total_handlers == 1
        assert s.enabled_handlers == 1
        assert s.total_dispatches == 2
        assert s.total_deliveries == 3
        assert s.total_failures == 0


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------
class TestConstruction:
    def test_empty_on_init(self):
        d = DocChangeDispatcher()
        assert d.list_handlers() == []

    def test_stats_empty_on_init(self):
        d = DocChangeDispatcher()
        s = d.stats()
        assert s.total_handlers == 0
        assert s.enabled_handlers == 0
        assert s.total_dispatches == 0
        assert s.total_deliveries == 0
        assert s.total_failures == 0

    def test_independent_instances(self):
        d1 = DocChangeDispatcher()
        d2 = DocChangeDispatcher()
        d1.register_handler("created", lambda *a: None)
        assert len(d2.list_handlers()) == 0


# ---------------------------------------------------------------------------
# Register
# ---------------------------------------------------------------------------
class TestRegisterHandler:
    def test_returns_handler(self):
        d = DocChangeDispatcher()
        h = d.register_handler("created", lambda *a: None)
        assert isinstance(h, Handler)

    def test_handler_id_is_uuid_hex(self):
        d = DocChangeDispatcher()
        h = d.register_handler("created", lambda *a: None)
        # uuid4 hex is 32 chars
        assert isinstance(h.handler_id, str)
        assert len(h.handler_id) == 32

    def test_handler_id_unique(self):
        d = DocChangeDispatcher()
        h1 = d.register_handler("a", lambda *a: None)
        h2 = d.register_handler("a", lambda *a: None)
        assert h1.handler_id != h2.handler_id

    def test_enabled_default_true(self):
        d = DocChangeDispatcher()
        h = d.register_handler("created", lambda *a: None)
        assert h.enabled is True

    def test_priority_default_zero(self):
        d = DocChangeDispatcher()
        h = d.register_handler("created", lambda *a: None)
        assert h.priority == 0

    def test_priority_explicit(self):
        d = DocChangeDispatcher()
        h = d.register_handler("created", lambda *a: None, priority=10)
        assert h.priority == 10

    def test_stored(self):
        d = DocChangeDispatcher()
        h = d.register_handler("created", lambda *a: None)
        assert d.get_handler(h.handler_id) is h

    def test_callback_preserved(self):
        d = DocChangeDispatcher()
        cb = lambda doc, ct, p: None
        h = d.register_handler("c", cb)
        assert h.callback is cb


# ---------------------------------------------------------------------------
# Unregister
# ---------------------------------------------------------------------------
class TestUnregisterHandler:
    def test_returns_true_when_present(self):
        d = DocChangeDispatcher()
        h = d.register_handler("a", lambda *a: None)
        assert d.unregister_handler(h.handler_id) is True

    def test_returns_false_when_missing(self):
        d = DocChangeDispatcher()
        assert d.unregister_handler("nope") is False

    def test_removes_handler(self):
        d = DocChangeDispatcher()
        h = d.register_handler("a", lambda *a: None)
        d.unregister_handler(h.handler_id)
        assert d.get_handler(h.handler_id) is None

    def test_second_remove_returns_false(self):
        d = DocChangeDispatcher()
        h = d.register_handler("a", lambda *a: None)
        d.unregister_handler(h.handler_id)
        assert d.unregister_handler(h.handler_id) is False


# ---------------------------------------------------------------------------
# Enable/disable
# ---------------------------------------------------------------------------
class TestEnableDisable:
    def test_disable_returns_true(self):
        d = DocChangeDispatcher()
        h = d.register_handler("a", lambda *a: None)
        assert d.disable_handler(h.handler_id) is True

    def test_disable_changes_state(self):
        d = DocChangeDispatcher()
        h = d.register_handler("a", lambda *a: None)
        d.disable_handler(h.handler_id)
        assert d.get_handler(h.handler_id).enabled is False

    def test_enable_returns_true(self):
        d = DocChangeDispatcher()
        h = d.register_handler("a", lambda *a: None)
        d.disable_handler(h.handler_id)
        assert d.enable_handler(h.handler_id) is True

    def test_enable_changes_state(self):
        d = DocChangeDispatcher()
        h = d.register_handler("a", lambda *a: None)
        d.disable_handler(h.handler_id)
        d.enable_handler(h.handler_id)
        assert d.get_handler(h.handler_id).enabled is True

    def test_disable_unknown_returns_false(self):
        d = DocChangeDispatcher()
        assert d.disable_handler("nope") is False

    def test_enable_unknown_returns_false(self):
        d = DocChangeDispatcher()
        assert d.enable_handler("nope") is False


# ---------------------------------------------------------------------------
# Get
# ---------------------------------------------------------------------------
class TestGetHandler:
    def test_found(self):
        d = DocChangeDispatcher()
        h = d.register_handler("a", lambda *a: None)
        assert d.get_handler(h.handler_id) is h

    def test_missing(self):
        d = DocChangeDispatcher()
        assert d.get_handler("nope") is None


# ---------------------------------------------------------------------------
# List
# ---------------------------------------------------------------------------
class TestListHandlers:
    def test_empty(self):
        d = DocChangeDispatcher()
        assert d.list_handlers() == []

    def test_returns_all(self):
        d = DocChangeDispatcher()
        d.register_handler("a", lambda *a: None)
        d.register_handler("b", lambda *a: None)
        d.register_handler("c", lambda *a: None)
        assert len(d.list_handlers()) == 3

    def test_sorted_by_priority_desc(self):
        d = DocChangeDispatcher()
        d.register_handler("a", lambda *a: None, priority=1)
        d.register_handler("b", lambda *a: None, priority=10)
        d.register_handler("c", lambda *a: None, priority=5)
        result = d.list_handlers()
        priorities = [h.priority for h in result]
        assert priorities == sorted(priorities, reverse=True)

    def test_tiebreak_by_handler_id(self):
        d = DocChangeDispatcher()
        h1 = d.register_handler("a", lambda *a: None, priority=0)
        h2 = d.register_handler("b", lambda *a: None, priority=0)
        result = d.list_handlers()
        ids = [h.handler_id for h in result]
        assert ids == sorted(ids)


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------
class TestDispatch:
    def test_returns_dispatch_result(self):
        d = DocChangeDispatcher()
        r = d.dispatch("doc1", "created")
        assert isinstance(r, DispatchResult)

    def test_result_contains_doc_id_and_change_type(self):
        d = DocChangeDispatcher()
        r = d.dispatch("doc42", "deleted")
        assert r.doc_id == "doc42"
        assert r.change_type == "deleted"

    def test_calls_matching_handler(self):
        d = DocChangeDispatcher()
        called: list[tuple] = []
        d.register_handler("created", lambda doc, ct, p: called.append((doc, ct, p)))
        d.dispatch("doc1", "created", {"k": "v"})
        assert called == [("doc1", "created", {"k": "v"})]

    def test_does_not_call_non_matching(self):
        d = DocChangeDispatcher()
        called: list = []
        d.register_handler("updated", lambda *a: called.append(1))
        d.dispatch("doc1", "created")
        assert called == []

    def test_delivered_count_increments(self):
        d = DocChangeDispatcher()
        d.register_handler("created", lambda *a: None)
        d.register_handler("created", lambda *a: None)
        r = d.dispatch("doc1", "created")
        assert r.delivered_count == 2

    def test_handlers_invoked_list(self):
        d = DocChangeDispatcher()
        h1 = d.register_handler("created", lambda *a: None)
        h2 = d.register_handler("created", lambda *a: None)
        r = d.dispatch("doc1", "created")
        assert set(r.handlers_invoked) == {h1.handler_id, h2.handler_id}

    def test_no_handlers(self):
        d = DocChangeDispatcher()
        r = d.dispatch("doc1", "created")
        assert r.delivered_count == 0
        assert r.failed_count == 0
        assert r.handlers_invoked == []

    def test_payload_optional(self):
        d = DocChangeDispatcher()
        received: list = []
        d.register_handler("created", lambda doc, ct, p: received.append(p))
        d.dispatch("doc1", "created")
        assert received == [None]

    def test_none_callback_counts_as_delivered(self):
        d = DocChangeDispatcher()
        # Directly insert a handler with no callback
        d.register_handler("created", None)
        r = d.dispatch("doc1", "created")
        assert r.delivered_count == 1
        assert r.failed_count == 0


# ---------------------------------------------------------------------------
# Wildcard
# ---------------------------------------------------------------------------
class TestDispatchWildcard:
    def test_wildcard_receives_any(self):
        d = DocChangeDispatcher()
        seen: list[str] = []
        d.register_handler("*", lambda doc, ct, p: seen.append(ct))
        d.dispatch("doc1", "created")
        d.dispatch("doc1", "updated")
        d.dispatch("doc1", "deleted")
        assert seen == ["created", "updated", "deleted"]

    def test_wildcard_plus_specific(self):
        d = DocChangeDispatcher()
        seen: list[str] = []
        d.register_handler("*", lambda doc, ct, p: seen.append(f"*:{ct}"))
        d.register_handler("created", lambda doc, ct, p: seen.append(f"c:{ct}"))
        d.dispatch("doc1", "created")
        assert set(seen) == {"*:created", "c:created"}

    def test_wildcard_count(self):
        d = DocChangeDispatcher()
        d.register_handler("*", lambda *a: None)
        r = d.dispatch("doc1", "anything")
        assert r.delivered_count == 1

    def test_wildcard_does_not_match_string_literal_star_as_type(self):
        # If we dispatch a change_type "*", a handler with "*" matches
        # and a handler with "*" also exact-matches: both true. So only one handler.
        d = DocChangeDispatcher()
        d.register_handler("*", lambda *a: None)
        r = d.dispatch("doc1", "*")
        assert r.delivered_count == 1


# ---------------------------------------------------------------------------
# Priority
# ---------------------------------------------------------------------------
class TestDispatchPriority:
    def test_higher_priority_first(self):
        d = DocChangeDispatcher()
        order: list[int] = []
        d.register_handler("c", lambda *a: order.append(1), priority=1)
        d.register_handler("c", lambda *a: order.append(10), priority=10)
        d.register_handler("c", lambda *a: order.append(5), priority=5)
        d.dispatch("doc1", "c")
        assert order == [10, 5, 1]

    def test_equal_priority_stable_by_id(self):
        d = DocChangeDispatcher()
        ids: list[str] = []
        h1 = d.register_handler("c", lambda *a: None, priority=0)
        h2 = d.register_handler("c", lambda *a: None, priority=0)
        # callbacks must record their handler_id; rewire
        d.unregister_handler(h1.handler_id)
        d.unregister_handler(h2.handler_id)
        captured: list[str] = []
        hA = d.register_handler("c", lambda doc, ct, p: captured.append("A"), priority=0)
        hB = d.register_handler("c", lambda doc, ct, p: captured.append("B"), priority=0)
        r = d.dispatch("doc1", "c")
        assert r.handlers_invoked == sorted(r.handlers_invoked)

    def test_negative_priority_runs_last(self):
        d = DocChangeDispatcher()
        order: list[int] = []
        d.register_handler("c", lambda *a: order.append(-5), priority=-5)
        d.register_handler("c", lambda *a: order.append(0), priority=0)
        d.register_handler("c", lambda *a: order.append(3), priority=3)
        d.dispatch("doc1", "c")
        assert order == [3, 0, -5]


# ---------------------------------------------------------------------------
# Disabled handlers
# ---------------------------------------------------------------------------
class TestDispatchDisabled:
    def test_disabled_not_called(self):
        d = DocChangeDispatcher()
        called: list = []
        h = d.register_handler("c", lambda *a: called.append(1))
        d.disable_handler(h.handler_id)
        r = d.dispatch("doc1", "c")
        assert called == []
        assert r.delivered_count == 0

    def test_disabled_not_in_handlers_invoked(self):
        d = DocChangeDispatcher()
        h = d.register_handler("c", lambda *a: None)
        d.disable_handler(h.handler_id)
        r = d.dispatch("doc1", "c")
        assert h.handler_id not in r.handlers_invoked

    def test_other_handlers_still_called(self):
        d = DocChangeDispatcher()
        called: list = []
        hOff = d.register_handler("c", lambda *a: called.append("off"))
        d.register_handler("c", lambda *a: called.append("on"))
        d.disable_handler(hOff.handler_id)
        d.dispatch("doc1", "c")
        assert called == ["on"]


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------
class TestDispatchErrors:
    def test_exception_recorded_as_failure(self):
        d = DocChangeDispatcher()
        def boom(*a):
            raise ValueError("kaboom")
        d.register_handler("c", boom)
        r = d.dispatch("doc1", "c")
        assert r.failed_count == 1
        assert r.delivered_count == 0

    def test_error_message_recorded(self):
        d = DocChangeDispatcher()
        def boom(*a):
            raise ValueError("kaboom")
        h = d.register_handler("c", boom)
        r = d.dispatch("doc1", "c")
        assert len(r.errors) == 1
        assert h.handler_id in r.errors[0]
        assert "kaboom" in r.errors[0]

    def test_other_handlers_continue_after_error(self):
        d = DocChangeDispatcher()
        called: list = []
        def boom(*a):
            raise RuntimeError("x")
        d.register_handler("c", boom, priority=10)
        d.register_handler("c", lambda *a: called.append("ok"), priority=1)
        r = d.dispatch("doc1", "c")
        assert called == ["ok"]
        assert r.delivered_count == 1
        assert r.failed_count == 1

    def test_handler_invoked_recorded_even_on_failure(self):
        d = DocChangeDispatcher()
        def boom(*a):
            raise Exception("x")
        h = d.register_handler("c", boom)
        r = d.dispatch("doc1", "c")
        assert h.handler_id in r.handlers_invoked

    def test_multiple_failures(self):
        d = DocChangeDispatcher()
        def boom(*a):
            raise Exception("x")
        d.register_handler("c", boom)
        d.register_handler("c", boom)
        d.register_handler("c", boom)
        r = d.dispatch("doc1", "c")
        assert r.failed_count == 3
        assert len(r.errors) == 3


# ---------------------------------------------------------------------------
# matching_handlers
# ---------------------------------------------------------------------------
class TestMatchingHandlers:
    def test_empty(self):
        d = DocChangeDispatcher()
        assert d.matching_handlers("c") == []

    def test_exact_match(self):
        d = DocChangeDispatcher()
        h = d.register_handler("created", lambda *a: None)
        d.register_handler("updated", lambda *a: None)
        result = d.matching_handlers("created")
        assert [x.handler_id for x in result] == [h.handler_id]

    def test_wildcard_match(self):
        d = DocChangeDispatcher()
        h = d.register_handler("*", lambda *a: None)
        result = d.matching_handlers("anything")
        assert [x.handler_id for x in result] == [h.handler_id]

    def test_excludes_disabled(self):
        d = DocChangeDispatcher()
        h = d.register_handler("c", lambda *a: None)
        d.disable_handler(h.handler_id)
        assert d.matching_handlers("c") == []

    def test_sorted_by_priority(self):
        d = DocChangeDispatcher()
        d.register_handler("c", lambda *a: None, priority=1)
        d.register_handler("c", lambda *a: None, priority=10)
        d.register_handler("c", lambda *a: None, priority=5)
        result = d.matching_handlers("c")
        assert [h.priority for h in result] == [10, 5, 1]


# ---------------------------------------------------------------------------
# clear_handlers
# ---------------------------------------------------------------------------
class TestClearHandlers:
    def test_empty_returns_zero(self):
        d = DocChangeDispatcher()
        assert d.clear_handlers() == 0

    def test_returns_count(self):
        d = DocChangeDispatcher()
        d.register_handler("a", lambda *a: None)
        d.register_handler("b", lambda *a: None)
        d.register_handler("c", lambda *a: None)
        assert d.clear_handlers() == 3

    def test_empties_handlers(self):
        d = DocChangeDispatcher()
        d.register_handler("a", lambda *a: None)
        d.clear_handlers()
        assert d.list_handlers() == []


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------
class TestStats:
    def test_total_handlers(self):
        d = DocChangeDispatcher()
        d.register_handler("a", lambda *a: None)
        d.register_handler("b", lambda *a: None)
        assert d.stats().total_handlers == 2

    def test_enabled_handlers(self):
        d = DocChangeDispatcher()
        h1 = d.register_handler("a", lambda *a: None)
        d.register_handler("b", lambda *a: None)
        d.disable_handler(h1.handler_id)
        s = d.stats()
        assert s.total_handlers == 2
        assert s.enabled_handlers == 1

    def test_total_dispatches(self):
        d = DocChangeDispatcher()
        d.dispatch("doc", "c")
        d.dispatch("doc", "c")
        d.dispatch("doc", "c")
        assert d.stats().total_dispatches == 3

    def test_total_deliveries(self):
        d = DocChangeDispatcher()
        d.register_handler("c", lambda *a: None)
        d.register_handler("c", lambda *a: None)
        d.dispatch("doc", "c")
        assert d.stats().total_deliveries == 2

    def test_total_failures(self):
        d = DocChangeDispatcher()
        def boom(*a):
            raise Exception("x")
        d.register_handler("c", boom)
        d.register_handler("c", lambda *a: None)
        d.dispatch("doc", "c")
        s = d.stats()
        assert s.total_failures == 1
        assert s.total_deliveries == 1

    def test_dispatch_no_handlers_counts(self):
        d = DocChangeDispatcher()
        d.dispatch("doc", "c")
        s = d.stats()
        assert s.total_dispatches == 1
        assert s.total_deliveries == 0
        assert s.total_failures == 0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_register(self):
        d = DocChangeDispatcher()
        def worker():
            for _ in range(50):
                d.register_handler("c", lambda *a: None)
        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert d.stats().total_handlers == 400

    def test_concurrent_dispatch(self):
        d = DocChangeDispatcher()
        counter = {"n": 0}
        lock = threading.Lock()
        def inc(*a):
            with lock:
                counter["n"] += 1
        d.register_handler("c", inc)
        def worker():
            for _ in range(100):
                d.dispatch("doc", "c")
        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert counter["n"] == 800
        assert d.stats().total_dispatches == 800
        assert d.stats().total_deliveries == 800

    def test_concurrent_mixed_ops(self):
        d = DocChangeDispatcher()
        d.register_handler("c", lambda *a: None)
        def reg():
            for _ in range(50):
                d.register_handler("c", lambda *a: None)
        def disp():
            for _ in range(50):
                d.dispatch("doc", "c")
        threads = []
        for _ in range(4):
            threads.append(threading.Thread(target=reg))
            threads.append(threading.Thread(target=disp))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # 4 reg threads * 50 + initial 1 = 201
        assert d.stats().total_handlers == 201
        # 4 disp threads * 50 = 200
        assert d.stats().total_dispatches == 200
