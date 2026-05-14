"""Tests for docstoolkit.doc_routing."""

from __future__ import annotations

import time

import pytest

from docstoolkit.doc_routing import (
    DocRouting,
    RouteMatch,
    RouteRule,
    RouterStats,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _always(_doc):
    return True


def _never(_doc):
    return False


def _identity(doc):
    return doc


def _label(label):
    def handler(_doc):
        return label
    return handler


# ---------------------------------------------------------------------------
# RouteRule
# ---------------------------------------------------------------------------


class TestRouteRule:
    def test_create_basic(self):
        r = RouteRule(rule_id="x", name="n", predicate=_always, handler=_identity)
        assert r.rule_id == "x"
        assert r.name == "n"

    def test_defaults_priority_zero(self):
        r = RouteRule(rule_id="x", name="n", predicate=_always, handler=_identity)
        assert r.priority == 0

    def test_default_stop_on_match_true(self):
        r = RouteRule(rule_id="x", name="n", predicate=_always, handler=_identity)
        assert r.stop_on_match is True

    def test_default_enabled_true(self):
        r = RouteRule(rule_id="x", name="n", predicate=_always, handler=_identity)
        assert r.enabled is True

    def test_custom_priority(self):
        r = RouteRule(
            rule_id="x", name="n", predicate=_always, handler=_identity, priority=5
        )
        assert r.priority == 5

    def test_stop_on_match_false(self):
        r = RouteRule(
            rule_id="x",
            name="n",
            predicate=_always,
            handler=_identity,
            stop_on_match=False,
        )
        assert r.stop_on_match is False


# ---------------------------------------------------------------------------
# RouteMatch
# ---------------------------------------------------------------------------


class TestRouteMatch:
    def test_create(self):
        m = RouteMatch(rule_id="x", rule_name="n", result="r", matched_at=1.0)
        assert m.rule_id == "x"
        assert m.rule_name == "n"
        assert m.result == "r"
        assert m.matched_at == 1.0

    def test_result_can_be_any(self):
        m = RouteMatch(rule_id="x", rule_name="n", result={"k": 1}, matched_at=0.0)
        assert m.result == {"k": 1}

    def test_result_can_be_none(self):
        m = RouteMatch(rule_id="x", rule_name="n", result=None, matched_at=0.0)
        assert m.result is None


# ---------------------------------------------------------------------------
# RouterStats
# ---------------------------------------------------------------------------


class TestRouterStats:
    def test_create(self):
        s = RouterStats(
            total_rules=1, total_routed=2, total_matches=3, total_unmatched=4
        )
        assert s.total_rules == 1
        assert s.total_routed == 2
        assert s.total_matches == 3
        assert s.total_unmatched == 4

    def test_by_rule_default_empty(self):
        s = RouterStats(
            total_rules=0, total_routed=0, total_matches=0, total_unmatched=0
        )
        assert s.by_rule == {}

    def test_by_rule_explicit(self):
        s = RouterStats(
            total_rules=1,
            total_routed=2,
            total_matches=3,
            total_unmatched=4,
            by_rule={"a": 1, "b": 2},
        )
        assert s.by_rule == {"a": 1, "b": 2}


# ---------------------------------------------------------------------------
# add_rule
# ---------------------------------------------------------------------------


class TestAddRule:
    def test_returns_rule(self):
        r = DocRouting()
        rule = r.add_rule("test", _always, _identity)
        assert isinstance(rule, RouteRule)

    def test_generates_unique_ids(self):
        r = DocRouting()
        a = r.add_rule("a", _always, _identity)
        b = r.add_rule("b", _always, _identity)
        assert a.rule_id != b.rule_id

    def test_increments_total_rules(self):
        r = DocRouting()
        assert r.total_rules == 0
        r.add_rule("a", _always, _identity)
        assert r.total_rules == 1
        r.add_rule("b", _always, _identity)
        assert r.total_rules == 2

    def test_default_priority(self):
        r = DocRouting()
        rule = r.add_rule("a", _always, _identity)
        assert rule.priority == 0

    def test_custom_priority(self):
        r = DocRouting()
        rule = r.add_rule("a", _always, _identity, priority=10)
        assert rule.priority == 10

    def test_default_stop_on_match(self):
        r = DocRouting()
        rule = r.add_rule("a", _always, _identity)
        assert rule.stop_on_match is True

    def test_custom_stop_on_match(self):
        r = DocRouting()
        rule = r.add_rule("a", _always, _identity, stop_on_match=False)
        assert rule.stop_on_match is False


# ---------------------------------------------------------------------------
# remove_rule
# ---------------------------------------------------------------------------


class TestRemoveRule:
    def test_remove_existing(self):
        r = DocRouting()
        rule = r.add_rule("a", _always, _identity)
        assert r.remove_rule(rule.rule_id) is True
        assert r.total_rules == 0

    def test_remove_missing(self):
        r = DocRouting()
        assert r.remove_rule("nope") is False

    def test_remove_twice(self):
        r = DocRouting()
        rule = r.add_rule("a", _always, _identity)
        r.remove_rule(rule.rule_id)
        assert r.remove_rule(rule.rule_id) is False


# ---------------------------------------------------------------------------
# enable / disable
# ---------------------------------------------------------------------------


class TestEnableDisable:
    def test_disable_existing(self):
        r = DocRouting()
        rule = r.add_rule("a", _always, _identity)
        assert r.disable_rule(rule.rule_id) is True
        assert r.get_rule(rule.rule_id).enabled is False

    def test_disable_missing(self):
        r = DocRouting()
        assert r.disable_rule("nope") is False

    def test_enable_after_disable(self):
        r = DocRouting()
        rule = r.add_rule("a", _always, _identity)
        r.disable_rule(rule.rule_id)
        assert r.enable_rule(rule.rule_id) is True
        assert r.get_rule(rule.rule_id).enabled is True

    def test_enable_missing(self):
        r = DocRouting()
        assert r.enable_rule("nope") is False

    def test_disabled_rule_skipped_during_routing(self):
        r = DocRouting()
        rule = r.add_rule("a", _always, _label("X"))
        r.disable_rule(rule.rule_id)
        matches = r.route({"doc": 1})
        assert matches == []


# ---------------------------------------------------------------------------
# route
# ---------------------------------------------------------------------------


class TestRoute:
    def test_single_match(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("hit"))
        matches = r.route({"x": 1})
        assert len(matches) == 1
        assert matches[0].result == "hit"

    def test_match_returns_routematch(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("hit"))
        matches = r.route({"x": 1})
        assert isinstance(matches[0], RouteMatch)

    def test_match_records_name(self):
        r = DocRouting()
        r.add_rule("my-rule", _always, _label("hit"))
        matches = r.route({"x": 1})
        assert matches[0].rule_name == "my-rule"

    def test_priority_order_descending(self):
        r = DocRouting()
        r.add_rule("low", _always, _label("low"), priority=1, stop_on_match=False)
        r.add_rule("high", _always, _label("high"), priority=10, stop_on_match=False)
        matches = r.route({})
        assert [m.rule_name for m in matches] == ["high", "low"]

    def test_handler_receives_doc(self):
        r = DocRouting()
        captured = []

        def handler(doc):
            captured.append(doc)
            return "ok"

        r.add_rule("a", _always, handler)
        r.route({"k": "v"})
        assert captured == [{"k": "v"}]

    def test_predicate_receives_doc(self):
        r = DocRouting()
        captured = []

        def pred(doc):
            captured.append(doc)
            return True

        r.add_rule("a", pred, _identity)
        r.route({"k": "v"})
        assert captured == [{"k": "v"}]

    def test_matched_at_set(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("ok"))
        before = time.time()
        matches = r.route({})
        after = time.time()
        assert before <= matches[0].matched_at <= after

    def test_handler_exception_captured(self):
        r = DocRouting()

        def boom(_doc):
            raise ValueError("kaboom")

        r.add_rule("bad", _always, boom)
        matches = r.route({})
        assert len(matches) == 1
        assert isinstance(matches[0].result, dict)
        assert "error" in matches[0].result
        assert matches[0].result["type"] == "ValueError"

    def test_predicate_exception_treated_as_no_match(self):
        r = DocRouting()

        def boom(_doc):
            raise RuntimeError("nope")

        r.add_rule("bad", boom, _label("x"))
        matches = r.route({})
        assert matches == []


# ---------------------------------------------------------------------------
# route — no match
# ---------------------------------------------------------------------------


class TestRouteNoMatch:
    def test_no_rules_returns_empty(self):
        r = DocRouting()
        assert r.route({"x": 1}) == []

    def test_no_matching_predicate_returns_empty(self):
        r = DocRouting()
        r.add_rule("a", _never, _label("nope"))
        assert r.route({"x": 1}) == []

    def test_unmatched_increments_stats(self):
        r = DocRouting()
        r.add_rule("a", _never, _label("nope"))
        r.route({})
        assert r.stats().total_unmatched == 1


# ---------------------------------------------------------------------------
# route — stop_on_match
# ---------------------------------------------------------------------------


class TestRouteStopOnMatch:
    def test_stops_after_first_match_when_true(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("a"), priority=10, stop_on_match=True)
        r.add_rule("b", _always, _label("b"), priority=5, stop_on_match=True)
        matches = r.route({})
        assert len(matches) == 1
        assert matches[0].rule_name == "a"

    def test_none_result_does_not_short_circuit(self):
        r = DocRouting()
        r.add_rule(
            "first", _always, lambda _d: None, priority=10, stop_on_match=True
        )
        r.add_rule("second", _always, _label("b"), priority=5, stop_on_match=True)
        matches = r.route({})
        # First rule returned None — second still runs
        assert len(matches) == 2

    def test_handler_error_does_not_short_circuit(self):
        r = DocRouting()

        def boom(_d):
            raise RuntimeError("x")

        r.add_rule("first", _always, boom, priority=10, stop_on_match=True)
        r.add_rule("second", _always, _label("b"), priority=5, stop_on_match=True)
        matches = r.route({})
        assert len(matches) == 2
        assert matches[1].rule_name == "second"


# ---------------------------------------------------------------------------
# route — stop_on_match=False (run all matches)
# ---------------------------------------------------------------------------


class TestRouteAllMatch:
    def test_all_rules_run_when_stop_false(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("a"), priority=10, stop_on_match=False)
        r.add_rule("b", _always, _label("b"), priority=5, stop_on_match=False)
        r.add_rule("c", _always, _label("c"), priority=1, stop_on_match=False)
        matches = r.route({})
        assert [m.rule_name for m in matches] == ["a", "b", "c"]

    def test_mixed_stop_on_match(self):
        r = DocRouting()
        r.add_rule("low", _always, _label("low"), priority=1, stop_on_match=False)
        r.add_rule("high", _always, _label("high"), priority=10, stop_on_match=False)
        r.add_rule("mid", _always, _label("mid"), priority=5, stop_on_match=True)
        matches = r.route({})
        # high (non-stop), mid (stop) — should halt after mid
        assert [m.rule_name for m in matches] == ["high", "mid"]


# ---------------------------------------------------------------------------
# route_batch
# ---------------------------------------------------------------------------


class TestRouteBatch:
    def test_returns_list_per_doc(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("ok"))
        out = r.route_batch([{}, {}, {}])
        assert len(out) == 3
        assert all(len(m) == 1 for m in out)

    def test_empty_batch(self):
        r = DocRouting()
        assert r.route_batch([]) == []

    def test_mixed_match_unmatch(self):
        r = DocRouting()
        r.add_rule("has_x", lambda d: "x" in d, _label("hit"))
        out = r.route_batch([{"x": 1}, {"y": 2}, {"x": 3}])
        assert len(out[0]) == 1
        assert out[1] == []
        assert len(out[2]) == 1


# ---------------------------------------------------------------------------
# match_rules
# ---------------------------------------------------------------------------


class TestMatchRules:
    def test_returns_matching_rules_only(self):
        r = DocRouting()
        a = r.add_rule("a", _always, _label("a"))
        r.add_rule("b", _never, _label("b"))
        rules = r.match_rules({})
        assert len(rules) == 1
        assert rules[0].rule_id == a.rule_id

    def test_handlers_not_invoked(self):
        r = DocRouting()
        called = []
        r.add_rule("a", _always, lambda d: called.append("yes"))
        r.match_rules({})
        assert called == []

    def test_skips_disabled(self):
        r = DocRouting()
        rule = r.add_rule("a", _always, _identity)
        r.disable_rule(rule.rule_id)
        assert r.match_rules({}) == []

    def test_priority_order(self):
        r = DocRouting()
        r.add_rule("low", _always, _identity, priority=1)
        r.add_rule("high", _always, _identity, priority=10)
        names = [r_.name for r_ in r.match_rules({})]
        assert names == ["high", "low"]


# ---------------------------------------------------------------------------
# rules
# ---------------------------------------------------------------------------


class TestRules:
    def test_returns_all_rules(self):
        r = DocRouting()
        r.add_rule("a", _always, _identity)
        r.add_rule("b", _always, _identity)
        assert len(r.rules()) == 2

    def test_enabled_only_filters(self):
        r = DocRouting()
        a = r.add_rule("a", _always, _identity)
        r.add_rule("b", _always, _identity)
        r.disable_rule(a.rule_id)
        assert len(r.rules(enabled_only=True)) == 1

    def test_empty(self):
        r = DocRouting()
        assert r.rules() == []


# ---------------------------------------------------------------------------
# rules_by_priority
# ---------------------------------------------------------------------------


class TestRulesByPriority:
    def test_orders_descending(self):
        r = DocRouting()
        r.add_rule("low", _always, _identity, priority=1)
        r.add_rule("high", _always, _identity, priority=10)
        r.add_rule("mid", _always, _identity, priority=5)
        names = [r_.name for r_ in r.rules_by_priority()]
        assert names == ["high", "mid", "low"]

    def test_empty_returns_empty(self):
        r = DocRouting()
        assert r.rules_by_priority() == []


# ---------------------------------------------------------------------------
# get_rule
# ---------------------------------------------------------------------------


class TestGetRule:
    def test_get_existing(self):
        r = DocRouting()
        rule = r.add_rule("a", _always, _identity)
        assert r.get_rule(rule.rule_id) is rule

    def test_get_missing(self):
        r = DocRouting()
        assert r.get_rule("nope") is None


# ---------------------------------------------------------------------------
# clear_history
# ---------------------------------------------------------------------------


class TestClearHistory:
    def test_returns_count_cleared(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("x"))
        r.route({})
        r.route({})
        assert r.clear_history() == 2

    def test_history_empty_after_clear(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("x"))
        r.route({})
        r.clear_history()
        assert r.routing_history() == []

    def test_returns_zero_when_empty(self):
        r = DocRouting()
        assert r.clear_history() == 0


# ---------------------------------------------------------------------------
# routing_history
# ---------------------------------------------------------------------------


class TestRoutingHistory:
    def test_records_each_match(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("x"))
        r.route({})
        r.route({})
        assert len(r.routing_history()) == 2

    def test_no_match_no_history(self):
        r = DocRouting()
        r.add_rule("a", _never, _label("x"))
        r.route({})
        assert r.routing_history() == []

    def test_limit_returns_last_n(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("x"))
        for _ in range(5):
            r.route({})
        hist = r.routing_history(limit=2)
        assert len(hist) == 2

    def test_limit_zero(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("x"))
        r.route({})
        assert r.routing_history(limit=0) == []


# ---------------------------------------------------------------------------
# match_by_metadata
# ---------------------------------------------------------------------------


class TestMatchByMetadata:
    def test_basic_match(self):
        pred = DocRouting.match_by_metadata("type", "article")
        assert pred({"type": "article"}) is True

    def test_no_match(self):
        pred = DocRouting.match_by_metadata("type", "article")
        assert pred({"type": "book"}) is False

    def test_missing_field(self):
        pred = DocRouting.match_by_metadata("type", "article")
        assert pred({}) is False

    def test_nested_dotted_path(self):
        pred = DocRouting.match_by_metadata("meta.author", "alice")
        assert pred({"meta": {"author": "alice"}}) is True

    def test_nested_missing_path(self):
        pred = DocRouting.match_by_metadata("meta.author", "alice")
        assert pred({"meta": {}}) is False

    def test_works_with_router(self):
        r = DocRouting()
        r.add_rule("kind", r.match_by_metadata("kind", "post"), _label("post"))
        matches = r.route({"kind": "post"})
        assert matches[0].result == "post"


# ---------------------------------------------------------------------------
# match_by_pattern
# ---------------------------------------------------------------------------


class TestMatchByPattern:
    def test_regex_search_hit(self):
        pred = DocRouting.match_by_pattern("title", r"^Intro")
        assert pred({"title": "Introduction"}) is True

    def test_regex_search_miss(self):
        pred = DocRouting.match_by_pattern("title", r"^XYZ")
        assert pred({"title": "Introduction"}) is False

    def test_missing_field(self):
        pred = DocRouting.match_by_pattern("title", r".+")
        assert pred({}) is False

    def test_non_string_value(self):
        pred = DocRouting.match_by_pattern("count", r"\d+")
        # value is int, not str
        assert pred({"count": 42}) is False

    def test_pattern_anywhere(self):
        pred = DocRouting.match_by_pattern("body", r"foo")
        assert pred({"body": "hello foo world"}) is True

    def test_nested_path(self):
        pred = DocRouting.match_by_pattern("meta.tags", r"py")
        assert pred({"meta": {"tags": "python, ml"}}) is True


# ---------------------------------------------------------------------------
# match_all
# ---------------------------------------------------------------------------


class TestMatchAll:
    def test_all_true(self):
        pred = DocRouting.match_all(_always, _always)
        assert pred({}) is True

    def test_any_false(self):
        pred = DocRouting.match_all(_always, _never)
        assert pred({}) is False

    def test_empty_returns_true(self):
        pred = DocRouting.match_all()
        assert pred({}) is True

    def test_combines_with_metadata_preds(self):
        pred = DocRouting.match_all(
            DocRouting.match_by_metadata("type", "post"),
            DocRouting.match_by_metadata("status", "published"),
        )
        assert pred({"type": "post", "status": "published"}) is True
        assert pred({"type": "post", "status": "draft"}) is False

    def test_exception_treated_as_false(self):
        def boom(_d):
            raise RuntimeError("x")

        pred = DocRouting.match_all(_always, boom)
        assert pred({}) is False


# ---------------------------------------------------------------------------
# match_any
# ---------------------------------------------------------------------------


class TestMatchAny:
    def test_any_true(self):
        pred = DocRouting.match_any(_never, _always)
        assert pred({}) is True

    def test_all_false(self):
        pred = DocRouting.match_any(_never, _never)
        assert pred({}) is False

    def test_empty_returns_false(self):
        pred = DocRouting.match_any()
        assert pred({}) is False

    def test_short_circuits_after_first_true(self):
        pred = DocRouting.match_any(_always, _never)
        assert pred({}) is True

    def test_exception_skipped(self):
        def boom(_d):
            raise RuntimeError("x")

        pred = DocRouting.match_any(boom, _always)
        assert pred({}) is True


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_initial_state(self):
        r = DocRouting()
        s = r.stats()
        assert s.total_rules == 0
        assert s.total_routed == 0
        assert s.total_matches == 0
        assert s.total_unmatched == 0
        assert s.by_rule == {}

    def test_total_routed_increments(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("x"))
        r.route({})
        r.route({})
        assert r.stats().total_routed == 2

    def test_total_matches_increments(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("x"))
        r.route({})
        assert r.stats().total_matches == 1

    def test_by_rule_tracks_each_rule(self):
        r = DocRouting()
        rule = r.add_rule("a", _always, _label("x"))
        r.route({})
        r.route({})
        s = r.stats()
        assert s.by_rule[rule.rule_id] == 2

    def test_stats_is_routerstats(self):
        r = DocRouting()
        assert isinstance(r.stats(), RouterStats)


# ---------------------------------------------------------------------------
# total_rules
# ---------------------------------------------------------------------------


class TestTotalRules:
    def test_initial_zero(self):
        assert DocRouting().total_rules == 0

    def test_after_add(self):
        r = DocRouting()
        r.add_rule("a", _always, _identity)
        assert r.total_rules == 1

    def test_after_remove(self):
        r = DocRouting()
        rule = r.add_rule("a", _always, _identity)
        r.remove_rule(rule.rule_id)
        assert r.total_rules == 0


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_removes_all_rules(self):
        r = DocRouting()
        r.add_rule("a", _always, _identity)
        r.add_rule("b", _always, _identity)
        r.clear()
        assert r.total_rules == 0

    def test_clears_history(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("x"))
        r.route({})
        r.clear()
        assert r.routing_history() == []

    def test_resets_stats(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("x"))
        r.route({})
        r.clear()
        s = r.stats()
        assert s.total_routed == 0
        assert s.total_matches == 0
        assert s.total_unmatched == 0
        assert s.by_rule == {}


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_route_empty_doc(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("x"))
        matches = r.route({})
        assert len(matches) == 1

    def test_equal_priority_stable_within_eval(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("a"), priority=5, stop_on_match=False)
        r.add_rule("b", _always, _label("b"), priority=5, stop_on_match=False)
        matches = r.route({})
        # Both should fire; their relative order may depend on insertion
        names = sorted(m.rule_name for m in matches)
        assert names == ["a", "b"]

    def test_complex_handler_returning_dict(self):
        r = DocRouting()
        r.add_rule("a", _always, lambda d: {"echo": d.get("k")})
        matches = r.route({"k": "v"})
        assert matches[0].result == {"echo": "v"}

    def test_history_grows_across_routes(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("x"))
        r.route({})
        r.route({})
        r.route({})
        assert len(r.routing_history()) == 3

    def test_disabled_then_enabled_routes_again(self):
        r = DocRouting()
        rule = r.add_rule("a", _always, _label("x"))
        r.disable_rule(rule.rule_id)
        assert r.route({}) == []
        r.enable_rule(rule.rule_id)
        assert len(r.route({})) == 1

    def test_routing_history_no_limit_returns_all(self):
        r = DocRouting()
        r.add_rule("a", _always, _label("x"))
        for _ in range(4):
            r.route({})
        assert len(r.routing_history()) == 4

    def test_predicate_helpers_compose(self):
        r = DocRouting()
        pred = DocRouting.match_all(
            DocRouting.match_by_metadata("type", "post"),
            DocRouting.match_any(
                DocRouting.match_by_pattern("title", r"^Intro"),
                DocRouting.match_by_metadata("featured", True),
            ),
        )
        r.add_rule("featured-post", pred, _label("HIT"))
        assert r.route({"type": "post", "title": "Intro to Python"})[0].result == "HIT"
        assert r.route({"type": "post", "featured": True})[0].result == "HIT"
        assert r.route({"type": "post", "title": "Other"}) == []
