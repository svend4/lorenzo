"""Tests for E198 — doc_filter_chain."""
from __future__ import annotations

import pytest

from docstoolkit.doc_filter_chain import (
    BatchResult,
    ChainFilter,
    ChainResult,
    DocFilterChain,
    FilterContext,
    FilterPhase,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def identity(doc: dict) -> dict:
    return doc


def add_marker(name: str):
    def _f(doc: dict) -> dict:
        doc.setdefault("marks", []).append(name)
        return doc

    return _f


def drop_all(_doc: dict):
    return None


def raises(_doc: dict):
    raise RuntimeError("boom")


# ---------------------------------------------------------------------------
class TestFilterPhase:
    def test_phase_members(self):
        assert {p.name for p in FilterPhase} == {"PRE", "MAIN", "POST"}

    def test_phase_distinct(self):
        assert FilterPhase.PRE != FilterPhase.MAIN
        assert FilterPhase.MAIN != FilterPhase.POST
        assert FilterPhase.PRE != FilterPhase.POST

    def test_phase_values(self):
        assert FilterPhase.PRE.value == "pre"
        assert FilterPhase.MAIN.value == "main"
        assert FilterPhase.POST.value == "post"


class TestChainFilter:
    def test_construction_defaults(self):
        cf = ChainFilter(name="x", func=identity)
        assert cf.name == "x"
        assert cf.phase == FilterPhase.MAIN
        assert cf.priority == 0
        assert cf.enabled is True

    def test_construction_custom(self):
        cf = ChainFilter(name="x", func=identity, phase=FilterPhase.PRE, priority=5)
        assert cf.phase == FilterPhase.PRE
        assert cf.priority == 5

    def test_filter_callable(self):
        cf = ChainFilter(name="x", func=add_marker("a"))
        out = cf.func({"k": 1})
        assert out["marks"] == ["a"]


class TestFilterContext:
    def test_default_history_independent(self):
        c1 = FilterContext(original={"a": 1}, current={"a": 1})
        c2 = FilterContext(original={"b": 2}, current={"b": 2})
        c1.history.append("x")
        assert c2.history == []

    def test_dropped_defaults(self):
        c = FilterContext(original={}, current={})
        assert c.dropped is False
        assert c.dropped_by is None


class TestChainResult:
    def test_success_result(self):
        ctx = FilterContext(original={}, current={"k": 1})
        r = ChainResult(final={"k": 1}, context=ctx, success=True)
        assert r.success is True
        assert r.error is None

    def test_error_result(self):
        ctx = FilterContext(original={}, current={})
        r = ChainResult(final=None, context=ctx, success=False, error="bad")
        assert r.success is False
        assert r.error == "bad"


class TestBatchResult:
    def test_counts_consistent(self):
        ctx = FilterContext(original={}, current={})
        results = [ChainResult(final={}, context=ctx, success=True)]
        b = BatchResult(results=results, processed_count=1, dropped_count=0, error_count=0)
        assert b.processed_count == 1
        assert len(b.results) == 1


class TestAddFilter:
    def test_add_returns_chainfilter(self):
        ch = DocFilterChain()
        cf = ch.add_filter("a", identity)
        assert isinstance(cf, ChainFilter)
        assert cf.name == "a"

    def test_add_increases_count(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        ch.add_filter("b", identity)
        assert ch.filter_count == 2

    def test_add_duplicate_name_raises(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        with pytest.raises(ValueError):
            ch.add_filter("a", identity)

    def test_add_empty_name_raises(self):
        ch = DocFilterChain()
        with pytest.raises(ValueError):
            ch.add_filter("", identity)

    def test_add_non_callable_raises(self):
        ch = DocFilterChain()
        with pytest.raises(ValueError):
            ch.add_filter("a", "not callable")  # type: ignore[arg-type]

    def test_add_with_custom_phase(self):
        ch = DocFilterChain()
        cf = ch.add_filter("a", identity, phase=FilterPhase.POST)
        assert cf.phase == FilterPhase.POST

    def test_add_with_priority(self):
        ch = DocFilterChain()
        cf = ch.add_filter("a", identity, priority=10)
        assert cf.priority == 10

    def test_add_invalid_phase_type(self):
        ch = DocFilterChain()
        with pytest.raises(ValueError):
            ch.add_filter("a", identity, phase="pre")  # type: ignore[arg-type]


class TestRemoveFilter:
    def test_remove_existing(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        assert ch.remove_filter("a") is True
        assert ch.filter_count == 0

    def test_remove_missing(self):
        ch = DocFilterChain()
        assert ch.remove_filter("zzz") is False

    def test_remove_only_matching(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        ch.add_filter("b", identity)
        ch.remove_filter("a")
        names = [f.name for f in ch.list_filters()]
        assert names == ["b"]


class TestEnableDisable:
    def test_disable(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        assert ch.disable_filter("a") is True
        assert ch.list_filters()[0].enabled is False

    def test_enable(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        ch.disable_filter("a")
        assert ch.enable_filter("a") is True
        assert ch.list_filters()[0].enabled is True

    def test_enable_missing(self):
        ch = DocFilterChain()
        assert ch.enable_filter("missing") is False

    def test_disable_missing(self):
        ch = DocFilterChain()
        assert ch.disable_filter("missing") is False

    def test_disabled_skipped_in_process(self):
        ch = DocFilterChain()
        ch.add_filter("m", add_marker("m"))
        ch.disable_filter("m")
        res = ch.process({"k": 1})
        assert res.final == {"k": 1}
        assert res.context.history == []


class TestProcessBasic:
    def test_no_filters_returns_doc(self):
        ch = DocFilterChain()
        res = ch.process({"k": 1})
        assert res.success is True
        assert res.final == {"k": 1}
        assert res.context.history == []

    def test_history_records_names(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        ch.add_filter("b", identity)
        res = ch.process({"k": 1})
        assert res.context.history == ["a", "b"]

    def test_original_preserved(self):
        ch = DocFilterChain()
        ch.add_filter("a", add_marker("a"))
        original = {"k": 1}
        res = ch.process(original)
        assert res.context.original == {"k": 1}
        assert original == {"k": 1}  # input not mutated

    def test_process_requires_dict(self):
        ch = DocFilterChain()
        with pytest.raises(TypeError):
            ch.process("not a dict")  # type: ignore[arg-type]


class TestProcessTransform:
    def test_transform_adds_field(self):
        ch = DocFilterChain()

        def add_field(doc):
            doc["added"] = True
            return doc

        ch.add_filter("add", add_field)
        res = ch.process({"k": 1})
        assert res.final == {"k": 1, "added": True}

    def test_chained_transforms(self):
        ch = DocFilterChain()
        ch.add_filter("a", add_marker("a"))
        ch.add_filter("b", add_marker("b"))
        ch.add_filter("c", add_marker("c"))
        res = ch.process({})
        assert res.final["marks"] == ["a", "b", "c"]

    def test_input_not_mutated(self):
        ch = DocFilterChain()
        ch.add_filter("a", add_marker("a"))
        doc = {"items": [1, 2]}
        ch.process(doc)
        assert doc == {"items": [1, 2]}


class TestProcessDrop:
    def test_drop_marks_dropped(self):
        ch = DocFilterChain()
        ch.add_filter("drop", drop_all)
        res = ch.process({"k": 1})
        assert res.context.dropped is True
        assert res.context.dropped_by == "drop"
        assert res.final is None
        assert res.success is True  # drop is not an error

    def test_drop_stops_chain(self):
        ch = DocFilterChain()
        ch.add_filter("a", add_marker("a"))
        ch.add_filter("drop", drop_all)
        ch.add_filter("b", add_marker("b"))
        res = ch.process({})
        assert res.context.dropped_by == "drop"
        assert res.context.history == ["a", "drop"]

    def test_drop_records_in_history(self):
        ch = DocFilterChain()
        ch.add_filter("d", drop_all)
        res = ch.process({})
        assert "d" in res.context.history


class TestProcessError:
    def test_error_marks_failure(self):
        ch = DocFilterChain()
        ch.add_filter("bad", raises)
        res = ch.process({"k": 1})
        assert res.success is False
        assert res.final is None
        assert res.error is not None
        assert "boom" in res.error

    def test_error_sets_dropped_by(self):
        ch = DocFilterChain()
        ch.add_filter("bad", raises)
        res = ch.process({})
        assert res.context.dropped_by == "bad"

    def test_error_stops_chain(self):
        ch = DocFilterChain()
        ch.add_filter("a", add_marker("a"))
        ch.add_filter("bad", raises)
        ch.add_filter("c", add_marker("c"))
        res = ch.process({})
        assert res.success is False
        assert "a" in res.context.history
        assert "c" not in res.context.history

    def test_non_dict_return_is_error(self):
        ch = DocFilterChain()
        ch.add_filter("weird", lambda d: 42)  # type: ignore[arg-type, return-value]
        res = ch.process({})
        assert res.success is False
        assert "non-dict" in (res.error or "")


class TestPhaseOrder:
    def test_pre_runs_first(self):
        ch = DocFilterChain()
        ch.add_filter("main", add_marker("main"))
        ch.add_filter("pre", add_marker("pre"), phase=FilterPhase.PRE)
        res = ch.process({})
        assert res.context.history == ["pre", "main"]

    def test_post_runs_last(self):
        ch = DocFilterChain()
        ch.add_filter("post", add_marker("post"), phase=FilterPhase.POST)
        ch.add_filter("main", add_marker("main"))
        ch.add_filter("pre", add_marker("pre"), phase=FilterPhase.PRE)
        res = ch.process({})
        assert res.context.history == ["pre", "main", "post"]

    def test_phase_order_when_registered_out_of_order(self):
        ch = DocFilterChain()
        ch.add_filter("p1", add_marker("p1"), phase=FilterPhase.POST)
        ch.add_filter("p2", add_marker("p2"), phase=FilterPhase.PRE)
        ch.add_filter("p3", add_marker("p3"), phase=FilterPhase.MAIN)
        res = ch.process({})
        assert res.context.history == ["p2", "p3", "p1"]


class TestPriorityOrder:
    def test_lower_priority_runs_first(self):
        ch = DocFilterChain()
        ch.add_filter("hi", add_marker("hi"), priority=10)
        ch.add_filter("lo", add_marker("lo"), priority=1)
        res = ch.process({})
        assert res.context.history == ["lo", "hi"]

    def test_equal_priority_keeps_insertion_order(self):
        ch = DocFilterChain()
        ch.add_filter("a", add_marker("a"), priority=5)
        ch.add_filter("b", add_marker("b"), priority=5)
        ch.add_filter("c", add_marker("c"), priority=5)
        res = ch.process({})
        assert res.context.history == ["a", "b", "c"]

    def test_priority_scoped_within_phase(self):
        ch = DocFilterChain()
        ch.add_filter("main_lo", add_marker("main_lo"), priority=0)
        ch.add_filter("pre_hi", add_marker("pre_hi"), phase=FilterPhase.PRE, priority=100)
        res = ch.process({})
        # pre always runs before main even at higher numeric priority
        assert res.context.history == ["pre_hi", "main_lo"]

    def test_negative_priority(self):
        ch = DocFilterChain()
        ch.add_filter("a", add_marker("a"), priority=0)
        ch.add_filter("b", add_marker("b"), priority=-5)
        res = ch.process({})
        assert res.context.history == ["b", "a"]


class TestProcessBatch:
    def test_batch_processes_all(self):
        ch = DocFilterChain()
        ch.add_filter("mark", add_marker("m"))
        b = ch.process_batch([{"k": 1}, {"k": 2}, {"k": 3}])
        assert b.processed_count == 3
        assert b.dropped_count == 0
        assert b.error_count == 0

    def test_batch_counts_drops(self):
        ch = DocFilterChain()
        ch.add_filter("d", lambda d: None if d.get("drop") else d)
        b = ch.process_batch([{"drop": True}, {"drop": False}, {"drop": True}])
        assert b.dropped_count == 2
        assert b.processed_count == 1

    def test_batch_counts_errors(self):
        ch = DocFilterChain()
        ch.add_filter("bad", lambda d: (_ for _ in ()).throw(RuntimeError("x")) if d.get("bad") else d)
        b = ch.process_batch([{"bad": True}, {"bad": False}])
        assert b.error_count == 1
        assert b.processed_count == 1

    def test_batch_empty(self):
        ch = DocFilterChain()
        b = ch.process_batch([])
        assert b.processed_count == 0
        assert b.dropped_count == 0
        assert b.error_count == 0
        assert b.results == []

    def test_batch_requires_list(self):
        ch = DocFilterChain()
        with pytest.raises(TypeError):
            ch.process_batch("not a list")  # type: ignore[arg-type]

    def test_batch_results_match_input_count(self):
        ch = DocFilterChain()
        b = ch.process_batch([{}, {}, {}])
        assert len(b.results) == 3


class TestFilterCount:
    def test_initial_zero(self):
        assert DocFilterChain().filter_count == 0

    def test_after_adds(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        ch.add_filter("b", identity)
        ch.add_filter("c", identity)
        assert ch.filter_count == 3

    def test_after_remove(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        ch.add_filter("b", identity)
        ch.remove_filter("a")
        assert ch.filter_count == 1


class TestFiltersInPhase:
    def test_empty_phase(self):
        ch = DocFilterChain()
        assert ch.filters_in_phase(FilterPhase.PRE) == []

    def test_only_pre(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity, phase=FilterPhase.PRE)
        ch.add_filter("b", identity, phase=FilterPhase.MAIN)
        pre = ch.filters_in_phase(FilterPhase.PRE)
        assert len(pre) == 1
        assert pre[0].name == "a"

    def test_invalid_phase_raises(self):
        ch = DocFilterChain()
        with pytest.raises(ValueError):
            ch.filters_in_phase("pre")  # type: ignore[arg-type]


class TestTotalPhases:
    def test_no_filters(self):
        assert DocFilterChain().total_phases() == 0

    def test_single_phase(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        ch.add_filter("b", identity)
        assert ch.total_phases() == 1

    def test_all_phases(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity, phase=FilterPhase.PRE)
        ch.add_filter("b", identity, phase=FilterPhase.MAIN)
        ch.add_filter("c", identity, phase=FilterPhase.POST)
        assert ch.total_phases() == 3


class TestListFilters:
    def test_list_all(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        ch.add_filter("b", identity)
        assert [f.name for f in ch.list_filters()] == ["a", "b"]

    def test_list_enabled_only(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        ch.add_filter("b", identity)
        ch.disable_filter("a")
        names = [f.name for f in ch.list_filters(enabled_only=True)]
        assert names == ["b"]

    def test_list_returns_copy(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        lst = ch.list_filters()
        lst.clear()
        assert ch.filter_count == 1


class TestSetPriority:
    def test_set_existing(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity, priority=1)
        assert ch.set_priority("a", 99) is True
        assert ch.list_filters()[0].priority == 99

    def test_set_missing(self):
        ch = DocFilterChain()
        assert ch.set_priority("missing", 1) is False

    def test_set_priority_changes_order(self):
        ch = DocFilterChain()
        ch.add_filter("a", add_marker("a"), priority=1)
        ch.add_filter("b", add_marker("b"), priority=2)
        ch.set_priority("b", 0)
        res = ch.process({})
        assert res.context.history == ["b", "a"]


class TestMoveFilter:
    def test_move_existing(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        assert ch.move_filter("a", FilterPhase.POST) is True
        assert ch.list_filters()[0].phase == FilterPhase.POST

    def test_move_missing(self):
        ch = DocFilterChain()
        assert ch.move_filter("missing", FilterPhase.PRE) is False

    def test_move_invalid_phase(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        with pytest.raises(ValueError):
            ch.move_filter("a", "pre")  # type: ignore[arg-type]

    def test_move_changes_execution_order(self):
        ch = DocFilterChain()
        ch.add_filter("a", add_marker("a"))
        ch.add_filter("b", add_marker("b"))
        ch.move_filter("a", FilterPhase.POST)
        res = ch.process({})
        assert res.context.history == ["b", "a"]


class TestClear:
    def test_clear_empty(self):
        ch = DocFilterChain()
        ch.clear()
        assert ch.filter_count == 0

    def test_clear_after_adds(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        ch.add_filter("b", identity)
        ch.clear()
        assert ch.filter_count == 0
        assert ch.list_filters() == []

    def test_clear_then_add(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        ch.clear()
        ch.add_filter("a", identity)  # name reusable after clear
        assert ch.filter_count == 1


class TestEdgeCases:
    def test_no_filters_passthrough(self):
        ch = DocFilterChain()
        res = ch.process({"x": [1, 2, 3]})
        assert res.success is True
        assert res.final == {"x": [1, 2, 3]}

    def test_all_disabled_passthrough(self):
        ch = DocFilterChain()
        ch.add_filter("a", drop_all)
        ch.add_filter("b", raises)
        ch.disable_filter("a")
        ch.disable_filter("b")
        res = ch.process({"k": 1})
        assert res.success is True
        assert res.final == {"k": 1}
        assert res.context.history == []

    def test_filter_returning_new_dict(self):
        ch = DocFilterChain()
        ch.add_filter("replace", lambda d: {"replaced": True})
        res = ch.process({"old": 1})
        assert res.final == {"replaced": True}

    def test_deep_copy_isolation(self):
        ch = DocFilterChain()

        def append_to_list(d):
            d["items"].append("x")
            return d

        ch.add_filter("a", append_to_list)
        doc = {"items": []}
        ch.process(doc)
        ch.process(doc)
        # original list not mutated across calls
        assert doc == {"items": []}

    def test_context_original_distinct_from_current_after_mutation(self):
        ch = DocFilterChain()
        ch.add_filter("a", add_marker("a"))
        res = ch.process({"items": [1]})
        assert "marks" not in res.context.original
        assert res.context.current["marks"] == ["a"]

    def test_dropped_by_none_on_success(self):
        ch = DocFilterChain()
        ch.add_filter("a", identity)
        res = ch.process({})
        assert res.context.dropped is False
        assert res.context.dropped_by is None
