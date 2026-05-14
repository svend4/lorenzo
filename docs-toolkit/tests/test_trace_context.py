"""Tests for the trace_context module — 90+ tests covering all spec requirements."""
from __future__ import annotations

import re
import threading
import time

import pytest

from docstoolkit.trace_context import (
    Span,
    SpanKind,
    SpanStatus,
    TraceContext,
    Tracer,
    get_current_span,
    set_current_span,
)
from docstoolkit.trace_context.context import _GLOBAL_CONTEXT


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

HEX32 = re.compile(r"^[0-9a-f]{32}$")
HEX16 = re.compile(r"^[0-9a-f]{16}$")


@pytest.fixture(autouse=True)
def _drain_global_context():
    """Ensure the global context stack is empty before and after each test."""
    # Before: drain anything a previous failing test may have left.
    while _GLOBAL_CONTEXT.pop() is not None:
        pass
    yield
    while _GLOBAL_CONTEXT.pop() is not None:
        pass


# ---------------------------------------------------------------------------
# 1. SpanKind enum
# ---------------------------------------------------------------------------

class TestSpanKind:
    def test_internal_value(self):
        assert SpanKind.INTERNAL == "INTERNAL"

    def test_server_value(self):
        assert SpanKind.SERVER == "SERVER"

    def test_client_value(self):
        assert SpanKind.CLIENT == "CLIENT"

    def test_producer_value(self):
        assert SpanKind.PRODUCER == "PRODUCER"

    def test_consumer_value(self):
        assert SpanKind.CONSUMER == "CONSUMER"

    def test_exactly_five_members(self):
        assert len(SpanKind) == 5

    def test_is_str_enum(self):
        assert isinstance(SpanKind.INTERNAL, str)

    def test_members_distinct(self):
        values = {k.value for k in SpanKind}
        assert len(values) == 5

    def test_name_matches_value(self):
        for k in SpanKind:
            assert k.name == k.value


# ---------------------------------------------------------------------------
# 2. SpanStatus enum
# ---------------------------------------------------------------------------

class TestSpanStatus:
    def test_unset_value(self):
        assert SpanStatus.UNSET == "UNSET"

    def test_ok_value(self):
        assert SpanStatus.OK == "OK"

    def test_error_value(self):
        assert SpanStatus.ERROR == "ERROR"

    def test_exactly_three_members(self):
        assert len(SpanStatus) == 3

    def test_is_str_enum(self):
        assert isinstance(SpanStatus.UNSET, str)

    def test_members_distinct(self):
        values = {s.value for s in SpanStatus}
        assert len(values) == 3


# ---------------------------------------------------------------------------
# 3. Span dataclass — defaults / IDs
# ---------------------------------------------------------------------------

class TestSpanDefaults:
    def test_default_trace_id_is_32_hex(self):
        sp = Span()
        assert HEX32.match(sp.trace_id)

    def test_default_trace_id_length(self):
        sp = Span()
        assert len(sp.trace_id) == 32

    def test_default_span_id_is_16_hex(self):
        sp = Span()
        assert HEX16.match(sp.span_id)

    def test_default_span_id_length(self):
        sp = Span()
        assert len(sp.span_id) == 16

    def test_default_parent_span_id_empty(self):
        assert Span().parent_span_id == ""

    def test_default_name_empty(self):
        assert Span().name == ""

    def test_default_kind_internal(self):
        assert Span().kind == SpanKind.INTERNAL

    def test_default_status_unset(self):
        assert Span().status == SpanStatus.UNSET

    def test_default_start_time_zero(self):
        assert Span().start_time == 0.0

    def test_default_end_time_zero(self):
        assert Span().end_time == 0.0

    def test_default_attributes_empty_dict(self):
        sp = Span()
        assert sp.attributes == {}

    def test_default_events_empty_list(self):
        sp = Span()
        assert sp.events == []

    def test_trace_id_is_unique_per_instance(self):
        ids = {Span().trace_id for _ in range(20)}
        assert len(ids) == 20

    def test_span_id_is_unique_per_instance(self):
        ids = {Span().span_id for _ in range(20)}
        assert len(ids) == 20

    def test_attributes_are_independent_across_instances(self):
        a, b = Span(), Span()
        a.attributes["k"] = 1
        assert b.attributes == {}

    def test_events_are_independent_across_instances(self):
        a, b = Span(), Span()
        a.events.append((1.0, "e", {}))
        assert b.events == []


# ---------------------------------------------------------------------------
# 4. Span — duration()
# ---------------------------------------------------------------------------

class TestSpanDuration:
    def test_duration_zero_when_both_unset(self):
        assert Span().duration() == 0.0

    def test_duration_zero_when_only_start(self):
        sp = Span(start_time=10.0)
        assert sp.duration() == 0.0

    def test_duration_zero_when_only_end(self):
        sp = Span(end_time=20.0)
        assert sp.duration() == 0.0

    def test_duration_computed_when_both_set(self):
        sp = Span(start_time=10.0, end_time=20.5)
        assert sp.duration() == pytest.approx(10.5)

    def test_duration_returns_float(self):
        sp = Span(start_time=1.0, end_time=2.0)
        assert isinstance(sp.duration(), float)

    def test_duration_negative_if_end_before_start(self):
        # The spec defines the math; we don't clamp.
        sp = Span(start_time=10.0, end_time=5.0)
        assert sp.duration() == pytest.approx(-5.0)


# ---------------------------------------------------------------------------
# 5. Span — set_attribute()
# ---------------------------------------------------------------------------

class TestSpanSetAttribute:
    def test_set_attribute_adds_key(self):
        sp = Span()
        sp.set_attribute("http.status", 200)
        assert sp.attributes["http.status"] == 200

    def test_set_attribute_overwrites(self):
        sp = Span()
        sp.set_attribute("k", 1)
        sp.set_attribute("k", 2)
        assert sp.attributes["k"] == 2

    def test_set_attribute_returns_none(self):
        sp = Span()
        assert sp.set_attribute("a", "b") is None

    def test_set_attribute_accepts_various_types(self):
        sp = Span()
        sp.set_attribute("int", 1)
        sp.set_attribute("str", "x")
        sp.set_attribute("list", [1, 2])
        sp.set_attribute("dict", {"y": 2})
        assert sp.attributes["int"] == 1
        assert sp.attributes["list"] == [1, 2]
        assert sp.attributes["dict"] == {"y": 2}

    def test_set_attribute_none_value(self):
        sp = Span()
        sp.set_attribute("k", None)
        assert sp.attributes["k"] is None


# ---------------------------------------------------------------------------
# 6. Span — add_event()
# ---------------------------------------------------------------------------

class TestSpanAddEvent:
    def test_add_event_default_timestamp(self):
        sp = Span()
        before = time.time()
        sp.add_event("ev")
        after = time.time()
        ts, name, attrs = sp.events[0]
        assert before <= ts <= after
        assert name == "ev"
        assert attrs == {}

    def test_add_event_with_attributes(self):
        sp = Span()
        sp.add_event("ev", attributes={"a": 1})
        ts, name, attrs = sp.events[0]
        assert attrs == {"a": 1}

    def test_add_event_explicit_timestamp(self):
        sp = Span()
        sp.add_event("ev", timestamp=12345.0)
        ts, name, attrs = sp.events[0]
        assert ts == 12345.0

    def test_add_event_multiple_appended_in_order(self):
        sp = Span()
        sp.add_event("a")
        sp.add_event("b")
        sp.add_event("c")
        names = [e[1] for e in sp.events]
        assert names == ["a", "b", "c"]

    def test_add_event_no_attrs_yields_empty_dict(self):
        sp = Span()
        sp.add_event("ev")
        _, _, attrs = sp.events[0]
        assert attrs == {}

    def test_add_event_returns_none(self):
        sp = Span()
        assert sp.add_event("e") is None

    def test_add_event_zero_timestamp_explicit(self):
        # Explicit timestamp=0 should be respected (not replaced by default).
        sp = Span()
        sp.add_event("ev", timestamp=0.0)
        ts, _, _ = sp.events[0]
        assert ts == 0.0

    def test_add_event_does_not_share_attrs_default(self):
        sp1, sp2 = Span(), Span()
        sp1.add_event("a")
        sp2.add_event("b")
        # Mutating one event's attrs dict must not leak into another.
        sp1.events[0][2]["x"] = 1
        assert sp2.events[0][2] == {}


# ---------------------------------------------------------------------------
# 7. Span — set_status()
# ---------------------------------------------------------------------------

class TestSpanSetStatus:
    def test_set_status_updates_status(self):
        sp = Span()
        sp.set_status(SpanStatus.OK)
        assert sp.status == SpanStatus.OK

    def test_set_status_error(self):
        sp = Span()
        sp.set_status(SpanStatus.ERROR)
        assert sp.status == SpanStatus.ERROR

    def test_set_status_no_description_no_attr(self):
        sp = Span()
        sp.set_status(SpanStatus.OK)
        assert "status.description" not in sp.attributes

    def test_set_status_empty_description_no_attr(self):
        sp = Span()
        sp.set_status(SpanStatus.OK, description="")
        assert "status.description" not in sp.attributes

    def test_set_status_with_description_stores_attr(self):
        sp = Span()
        sp.set_status(SpanStatus.ERROR, description="boom")
        assert sp.attributes["status.description"] == "boom"

    def test_set_status_returns_none(self):
        sp = Span()
        assert sp.set_status(SpanStatus.OK) is None

    def test_set_status_overwrites_description(self):
        sp = Span()
        sp.set_status(SpanStatus.ERROR, description="first")
        sp.set_status(SpanStatus.ERROR, description="second")
        assert sp.attributes["status.description"] == "second"


# ---------------------------------------------------------------------------
# 8. Span — is_recording()
# ---------------------------------------------------------------------------

class TestSpanIsRecording:
    def test_not_recording_before_start(self):
        assert Span().is_recording() is False

    def test_recording_after_start(self):
        sp = Span(start_time=time.time())
        assert sp.is_recording() is True

    def test_not_recording_after_end(self):
        sp = Span(start_time=1.0, end_time=2.0)
        assert sp.is_recording() is False

    def test_not_recording_when_only_end_set(self):
        sp = Span(end_time=5.0)
        assert sp.is_recording() is False

    def test_is_recording_returns_bool(self):
        sp = Span(start_time=1.0)
        assert isinstance(sp.is_recording(), bool)


# ---------------------------------------------------------------------------
# 9. TraceContext — push / pop / current
# ---------------------------------------------------------------------------

class TestTraceContext:
    def test_empty_current_span_is_none(self):
        ctx = TraceContext()
        assert ctx.current_span() is None

    def test_push_then_current_returns_span(self):
        ctx = TraceContext()
        sp = Span()
        ctx.push(sp)
        assert ctx.current_span() is sp

    def test_push_multiple_current_is_last(self):
        ctx = TraceContext()
        a, b, c = Span(), Span(), Span()
        for sp in (a, b, c):
            ctx.push(sp)
        assert ctx.current_span() is c

    def test_pop_returns_top(self):
        ctx = TraceContext()
        a, b = Span(), Span()
        ctx.push(a)
        ctx.push(b)
        assert ctx.pop() is b
        assert ctx.current_span() is a

    def test_pop_when_empty_returns_none(self):
        ctx = TraceContext()
        assert ctx.pop() is None

    def test_pop_until_empty(self):
        ctx = TraceContext()
        ctx.push(Span())
        ctx.push(Span())
        ctx.pop()
        ctx.pop()
        assert ctx.current_span() is None

    def test_get_trace_id_empty_when_no_span(self):
        ctx = TraceContext()
        assert ctx.get_trace_id() == ""

    def test_get_trace_id_returns_current(self):
        ctx = TraceContext()
        sp = Span()
        ctx.push(sp)
        assert ctx.get_trace_id() == sp.trace_id

    def test_get_trace_id_returns_top_when_nested(self):
        ctx = TraceContext()
        a, b = Span(), Span()
        ctx.push(a)
        ctx.push(b)
        assert ctx.get_trace_id() == b.trace_id

    def test_push_returns_none(self):
        ctx = TraceContext()
        assert ctx.push(Span()) is None

    def test_separate_contexts_are_independent(self):
        c1, c2 = TraceContext(), TraceContext()
        c1.push(Span())
        assert c1.current_span() is not None
        assert c2.current_span() is None

    def test_pop_after_push_returns_same_span(self):
        ctx = TraceContext()
        sp = Span()
        ctx.push(sp)
        assert ctx.pop() is sp


# ---------------------------------------------------------------------------
# 10. TraceContext — thread-local isolation
# ---------------------------------------------------------------------------

class TestTraceContextThreadLocal:
    def test_thread_local_isolation(self):
        ctx = TraceContext()
        main_span = Span(name="main")
        ctx.push(main_span)

        results: dict[str, object] = {}

        def worker():
            # Other thread should see an empty stack.
            results["initial"] = ctx.current_span()
            worker_span = Span(name="worker")
            ctx.push(worker_span)
            results["after_push"] = ctx.current_span()
            results["trace_id"] = ctx.get_trace_id()

        t = threading.Thread(target=worker)
        t.start()
        t.join()

        assert results["initial"] is None
        assert results["after_push"].name == "worker"
        assert results["trace_id"] == results["after_push"].trace_id
        # Main thread still sees its own span.
        assert ctx.current_span() is main_span

    def test_thread_pop_does_not_affect_main(self):
        ctx = TraceContext()
        main_span = Span(name="main")
        ctx.push(main_span)

        def worker():
            # Popping in worker pops from worker's stack, which is empty.
            ctx.pop()

        t = threading.Thread(target=worker)
        t.start()
        t.join()
        assert ctx.current_span() is main_span

    def test_independent_get_trace_id_per_thread(self):
        ctx = TraceContext()
        main = Span(name="main")
        ctx.push(main)

        captured = {}

        def worker():
            captured["empty"] = ctx.get_trace_id()
            ctx.push(Span(name="w"))
            captured["set"] = ctx.get_trace_id()

        t = threading.Thread(target=worker)
        t.start()
        t.join()

        assert captured["empty"] == ""
        assert captured["set"] != main.trace_id
        assert ctx.get_trace_id() == main.trace_id


# ---------------------------------------------------------------------------
# 11. get_current_span / set_current_span helpers
# ---------------------------------------------------------------------------

class TestGlobalHelpers:
    def test_get_current_span_initially_none(self):
        assert get_current_span() is None

    def test_set_current_span_pushes(self):
        sp = Span()
        set_current_span(sp)
        assert get_current_span() is sp

    def test_set_current_span_none_pops(self):
        sp = Span()
        set_current_span(sp)
        set_current_span(None)
        assert get_current_span() is None

    def test_set_current_span_multiple(self):
        a, b = Span(), Span()
        set_current_span(a)
        set_current_span(b)
        assert get_current_span() is b
        set_current_span(None)
        assert get_current_span() is a
        set_current_span(None)
        assert get_current_span() is None


# ---------------------------------------------------------------------------
# 12. Tracer — start_span / end_span
# ---------------------------------------------------------------------------

class TestTracerStartEnd:
    def test_default_service_name(self):
        assert Tracer().service_name == "default"

    def test_custom_service_name(self):
        assert Tracer("svc").service_name == "svc"

    def test_initial_spans_empty(self):
        assert Tracer().get_spans() == []

    def test_start_span_sets_name(self):
        sp = Tracer().start_span("op")
        assert sp.name == "op"

    def test_start_span_sets_kind(self):
        sp = Tracer().start_span("op", kind=SpanKind.CLIENT)
        assert sp.kind == SpanKind.CLIENT

    def test_start_span_default_kind_internal(self):
        sp = Tracer().start_span("op")
        assert sp.kind == SpanKind.INTERNAL

    def test_start_span_sets_start_time(self):
        before = time.time()
        sp = Tracer().start_span("op")
        after = time.time()
        assert before <= sp.start_time <= after

    def test_start_span_pushes_onto_context(self):
        t = Tracer()
        sp = t.start_span("op")
        assert get_current_span() is sp

    def test_start_span_attributes_merged(self):
        sp = Tracer().start_span("op", attributes={"a": 1, "b": 2})
        assert sp.attributes["a"] == 1
        assert sp.attributes["b"] == 2

    def test_start_span_attributes_none_yields_empty(self):
        sp = Tracer().start_span("op")
        assert sp.attributes == {}

    def test_start_span_returns_recording_span(self):
        sp = Tracer().start_span("op")
        assert sp.is_recording() is True

    def test_start_span_explicit_parent_links_id(self):
        t = Tracer()
        parent = Span(name="p")
        sp = t.start_span("child", parent=parent)
        assert sp.parent_span_id == parent.span_id

    def test_start_span_explicit_parent_shares_trace_id(self):
        t = Tracer()
        parent = Span(name="p")
        sp = t.start_span("child", parent=parent)
        assert sp.trace_id == parent.trace_id

    def test_start_span_no_parent_no_current_has_empty_parent_id(self):
        sp = Tracer().start_span("op")
        assert sp.parent_span_id == ""

    def test_start_span_uses_current_as_implicit_parent(self):
        t = Tracer()
        outer = t.start_span("outer")
        inner = t.start_span("inner")
        assert inner.parent_span_id == outer.span_id
        assert inner.trace_id == outer.trace_id

    def test_end_span_sets_end_time(self):
        t = Tracer()
        sp = t.start_span("op")
        before = time.time()
        t.end_span(sp)
        after = time.time()
        assert before <= sp.end_time <= after

    def test_end_span_default_status_ok(self):
        t = Tracer()
        sp = t.start_span("op")
        t.end_span(sp)
        assert sp.status == SpanStatus.OK

    def test_end_span_custom_status(self):
        t = Tracer()
        sp = t.start_span("op")
        t.end_span(sp, status=SpanStatus.ERROR)
        assert sp.status == SpanStatus.ERROR

    def test_end_span_pops_context(self):
        t = Tracer()
        sp = t.start_span("op")
        t.end_span(sp)
        assert get_current_span() is None

    def test_end_span_appends_to_spans(self):
        t = Tracer()
        sp = t.start_span("op")
        t.end_span(sp)
        assert sp in t.get_spans()

    def test_get_spans_returns_completed_only(self):
        t = Tracer()
        t.start_span("active")  # never ended
        sp2 = t.start_span("done")
        t.end_span(sp2)
        spans = t.get_spans()
        assert len(spans) == 1
        assert spans[0] is sp2

    def test_get_spans_is_snapshot(self):
        t = Tracer()
        sp = t.start_span("op")
        t.end_span(sp)
        snap = t.get_spans()
        snap.append("garbage")
        assert "garbage" not in t.get_spans()

    def test_end_span_records_duration(self):
        t = Tracer()
        sp = t.start_span("op")
        time.sleep(0.01)
        t.end_span(sp)
        assert sp.duration() > 0


# ---------------------------------------------------------------------------
# 13. Tracer — context manager `.span(...)`
# ---------------------------------------------------------------------------

class TestTracerSpanContextManager:
    def test_yields_span(self):
        t = Tracer()
        with t.span("op") as sp:
            assert isinstance(sp, Span)
            assert sp.name == "op"

    def test_auto_ends_on_normal_exit(self):
        t = Tracer()
        with t.span("op") as sp:
            pass
        assert sp.end_time > 0
        assert sp.status == SpanStatus.OK

    def test_appends_to_spans_after_exit(self):
        t = Tracer()
        with t.span("op") as sp:
            pass
        assert sp in t.get_spans()

    def test_pops_context_after_exit(self):
        t = Tracer()
        with t.span("op"):
            pass
        assert get_current_span() is None

    def test_kind_applied(self):
        t = Tracer()
        with t.span("op", kind=SpanKind.SERVER) as sp:
            pass
        assert sp.kind == SpanKind.SERVER

    def test_attributes_applied(self):
        t = Tracer()
        with t.span("op", attributes={"k": "v"}) as sp:
            pass
        assert sp.attributes["k"] == "v"

    def test_exception_sets_error_status(self):
        t = Tracer()
        with pytest.raises(ValueError):
            with t.span("op") as sp:
                raise ValueError("nope")
        assert sp.status == SpanStatus.ERROR

    def test_exception_is_reraised(self):
        t = Tracer()
        with pytest.raises(RuntimeError):
            with t.span("op"):
                raise RuntimeError("boom")

    def test_exception_records_description(self):
        t = Tracer()
        with pytest.raises(ValueError):
            with t.span("op") as sp:
                raise ValueError("explain me")
        assert sp.attributes.get("status.description") == "explain me"

    def test_exception_still_records_span(self):
        t = Tracer()
        with pytest.raises(ValueError):
            with t.span("op") as sp:
                raise ValueError("x")
        assert sp in t.get_spans()
        assert sp.end_time > 0

    def test_exception_pops_context(self):
        t = Tracer()
        with pytest.raises(ValueError):
            with t.span("op"):
                raise ValueError("x")
        assert get_current_span() is None

    def test_nested_context_manager_parent_link(self):
        t = Tracer()
        with t.span("outer") as outer:
            with t.span("inner") as inner:
                assert inner.parent_span_id == outer.span_id
                assert inner.trace_id == outer.trace_id

    def test_inner_exception_doesnt_break_outer(self):
        t = Tracer()
        with t.span("outer") as outer:
            with pytest.raises(RuntimeError):
                with t.span("inner") as inner:
                    raise RuntimeError("bad")
            # After inner failure, outer is still current.
            assert get_current_span() is outer
        assert outer.status == SpanStatus.OK
        assert inner.status == SpanStatus.ERROR

    def test_context_manager_records_duration(self):
        t = Tracer()
        with t.span("op") as sp:
            time.sleep(0.005)
        assert sp.duration() > 0


# ---------------------------------------------------------------------------
# 14. Tracer — nested / parent linking
# ---------------------------------------------------------------------------

class TestTracerNesting:
    def test_three_level_nesting_parent_links(self):
        t = Tracer()
        a = t.start_span("a")
        b = t.start_span("b")
        c = t.start_span("c")
        assert b.parent_span_id == a.span_id
        assert c.parent_span_id == b.span_id

    def test_three_level_nesting_shares_trace_id(self):
        t = Tracer()
        a = t.start_span("a")
        b = t.start_span("b")
        c = t.start_span("c")
        assert a.trace_id == b.trace_id == c.trace_id

    def test_root_has_empty_parent(self):
        t = Tracer()
        root = t.start_span("root")
        assert root.parent_span_id == ""
        t.end_span(root)

    def test_sibling_spans_get_independent_parents(self):
        t = Tracer()
        root = t.start_span("root")
        a = t.start_span("a")
        t.end_span(a)
        b = t.start_span("b")
        assert b.parent_span_id == root.span_id
        assert a.parent_span_id == root.span_id
        t.end_span(b)
        t.end_span(root)


# ---------------------------------------------------------------------------
# 15. Tracer — clear()
# ---------------------------------------------------------------------------

class TestTracerClear:
    def test_clear_empties_spans(self):
        t = Tracer()
        for _ in range(3):
            sp = t.start_span("op")
            t.end_span(sp)
        assert len(t.get_spans()) == 3
        t.clear()
        assert t.get_spans() == []

    def test_clear_on_empty_is_noop(self):
        t = Tracer()
        t.clear()
        assert t.get_spans() == []

    def test_clear_returns_none(self):
        t = Tracer()
        assert t.clear() is None


# ---------------------------------------------------------------------------
# 16. Tracer — export()
# ---------------------------------------------------------------------------

class TestTracerExport:
    def test_export_empty_is_list(self):
        assert Tracer().export() == []

    def test_export_one_span_returns_one_dict(self):
        t = Tracer()
        sp = t.start_span("op")
        t.end_span(sp)
        data = t.export()
        assert len(data) == 1
        assert isinstance(data[0], dict)

    def test_export_includes_core_fields(self):
        t = Tracer()
        sp = t.start_span("op")
        t.end_span(sp)
        d = t.export()[0]
        for key in (
            "trace_id",
            "span_id",
            "parent_span_id",
            "name",
            "kind",
            "status",
            "start_time",
            "end_time",
            "attributes",
            "events",
        ):
            assert key in d

    def test_export_kind_is_string_name(self):
        t = Tracer()
        sp = t.start_span("op", kind=SpanKind.SERVER)
        t.end_span(sp)
        assert t.export()[0]["kind"] == "SERVER"

    def test_export_status_is_string_name(self):
        t = Tracer()
        sp = t.start_span("op")
        t.end_span(sp, status=SpanStatus.ERROR)
        assert t.export()[0]["status"] == "ERROR"

    def test_export_status_unset_when_default(self):
        t = Tracer()
        sp = t.start_span("op")
        # Don't end — but export only returns completed spans (none yet).
        assert t.export() == []
        t.end_span(sp, status=SpanStatus.UNSET)
        assert t.export()[0]["status"] == "UNSET"

    def test_export_preserves_name(self):
        t = Tracer()
        sp = t.start_span("myop")
        t.end_span(sp)
        assert t.export()[0]["name"] == "myop"

    def test_export_includes_attributes(self):
        t = Tracer()
        sp = t.start_span("op", attributes={"k": "v"})
        t.end_span(sp)
        assert t.export()[0]["attributes"] == {"k": "v"}

    def test_export_includes_events(self):
        t = Tracer()
        sp = t.start_span("op")
        sp.add_event("e", attributes={"x": 1}, timestamp=42.0)
        t.end_span(sp)
        events = t.export()[0]["events"]
        assert events == [(42.0, "e", {"x": 1})]

    def test_export_includes_duration_if_present(self):
        t = Tracer()
        sp = t.start_span("op")
        time.sleep(0.001)
        t.end_span(sp)
        d = t.export()[0]
        # duration may or may not be a key; if present, sanity-check it.
        if "duration" in d:
            assert d["duration"] >= 0.0
        else:
            assert d["end_time"] >= d["start_time"]

    def test_export_independent_per_call(self):
        t = Tracer()
        sp = t.start_span("op")
        t.end_span(sp)
        a = t.export()
        b = t.export()
        a[0]["name"] = "mutated"
        assert b[0]["name"] == "op"

    def test_export_parent_relationship(self):
        t = Tracer()
        with t.span("outer"):
            with t.span("inner"):
                pass
        data = t.export()
        # The inner span is recorded first (ends first), outer recorded second.
        names = [d["name"] for d in data]
        assert "inner" in names
        assert "outer" in names
        inner_d = next(d for d in data if d["name"] == "inner")
        outer_d = next(d for d in data if d["name"] == "outer")
        assert inner_d["parent_span_id"] == outer_d["span_id"]
        assert inner_d["trace_id"] == outer_d["trace_id"]


# ---------------------------------------------------------------------------
# 17. Integration / sanity
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_full_lifecycle(self):
        t = Tracer("svc")
        with t.span("root", kind=SpanKind.SERVER) as root:
            root.set_attribute("user", "alice")
            with t.span("db", kind=SpanKind.CLIENT) as db:
                db.add_event("query")
        spans = t.get_spans()
        assert len(spans) == 2
        assert all(sp.end_time > 0 for sp in spans)

    def test_record_then_clear_then_record(self):
        t = Tracer()
        with t.span("a"):
            pass
        assert len(t.get_spans()) == 1
        t.clear()
        with t.span("b"):
            pass
        assert len(t.get_spans()) == 1
        assert t.get_spans()[0].name == "b"

    def test_set_current_span_then_tracer_uses_it_as_parent(self):
        # Pre-existing span set via helper; tracer should treat it as parent.
        outer = Span(name="manual")
        set_current_span(outer)
        try:
            t = Tracer()
            child = t.start_span("child")
            assert child.parent_span_id == outer.span_id
            assert child.trace_id == outer.trace_id
            t.end_span(child)
        finally:
            set_current_span(None)
