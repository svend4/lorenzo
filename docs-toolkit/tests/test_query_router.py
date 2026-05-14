"""Tests for the query_router module (E59).

Covers RouteRule.matches, QueryRouter routing logic, middleware pipeline,
and a wide range of edge cases.  At least 75 tests.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.query_router import (
    RouteCondition,
    RouteAction,
    RouteRule,
    RouteResult,
    QueryRouter,
    QueryMiddleware,
    NormalizationMiddleware,
    TruncationMiddleware,
    MiddlewarePipeline,
)


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------

def _keyword_rule(name="kw", keywords=None, action=RouteAction.FORWARD,
                  priority=0, target="default"):
    return RouteRule(
        name=name,
        condition=RouteCondition.KEYWORD_MATCH,
        action=action,
        priority=priority,
        keywords=keywords or ["hello"],
        target=target,
    )


def _length_rule(name="len", min_length=0, max_length=10_000,
                 action=RouteAction.FORWARD, priority=0, target="default"):
    return RouteRule(
        name=name,
        condition=RouteCondition.LENGTH_THRESHOLD,
        action=action,
        priority=priority,
        min_length=min_length,
        max_length=max_length,
        target=target,
    )


def _regex_rule(name="rx", pattern="", action=RouteAction.FORWARD,
                priority=0, target="default"):
    return RouteRule(
        name=name,
        condition=RouteCondition.REGEX_MATCH,
        action=action,
        priority=priority,
        pattern=pattern,
        target=target,
    )


def _always_rule(name="always", action=RouteAction.FORWARD, priority=0,
                 target="default"):
    return RouteRule(
        name=name,
        condition=RouteCondition.ALWAYS,
        action=action,
        priority=priority,
        target=target,
    )


# ===========================================================================
# RouteCondition & RouteAction enum tests
# ===========================================================================

class TestRouteConditionEnum:
    def test_keyword_match_member_exists(self):
        assert RouteCondition.KEYWORD_MATCH

    def test_length_threshold_member_exists(self):
        assert RouteCondition.LENGTH_THRESHOLD

    def test_regex_match_member_exists(self):
        assert RouteCondition.REGEX_MATCH

    def test_always_member_exists(self):
        assert RouteCondition.ALWAYS

    def test_all_four_conditions(self):
        assert len(RouteCondition) == 4


class TestRouteActionEnum:
    def test_forward_member_exists(self):
        assert RouteAction.FORWARD

    def test_transform_member_exists(self):
        assert RouteAction.TRANSFORM

    def test_reject_member_exists(self):
        assert RouteAction.REJECT

    def test_cache_member_exists(self):
        assert RouteAction.CACHE

    def test_all_four_actions(self):
        assert len(RouteAction) == 4


# ===========================================================================
# RouteRule defaults
# ===========================================================================

class TestRouteRuleDefaults:
    def test_priority_default_zero(self):
        r = RouteRule(name="x", condition=RouteCondition.ALWAYS, action=RouteAction.FORWARD)
        assert r.priority == 0

    def test_keywords_default_empty_list(self):
        r = RouteRule(name="x", condition=RouteCondition.ALWAYS, action=RouteAction.FORWARD)
        assert r.keywords == []

    def test_min_length_default(self):
        r = RouteRule(name="x", condition=RouteCondition.ALWAYS, action=RouteAction.FORWARD)
        assert r.min_length == 0

    def test_max_length_default(self):
        r = RouteRule(name="x", condition=RouteCondition.ALWAYS, action=RouteAction.FORWARD)
        assert r.max_length == 10_000

    def test_pattern_default_empty(self):
        r = RouteRule(name="x", condition=RouteCondition.ALWAYS, action=RouteAction.FORWARD)
        assert r.pattern == ""

    def test_transform_fn_default_none(self):
        r = RouteRule(name="x", condition=RouteCondition.ALWAYS, action=RouteAction.FORWARD)
        assert r.transform_fn is None

    def test_target_default(self):
        r = RouteRule(name="x", condition=RouteCondition.ALWAYS, action=RouteAction.FORWARD)
        assert r.target == "default"


# ===========================================================================
# RouteRule.matches — ALWAYS
# ===========================================================================

class TestRouteRuleMatchesAlways:
    def test_always_matches_non_empty(self):
        r = _always_rule()
        assert r.matches("anything") is True

    def test_always_matches_empty_string(self):
        r = _always_rule()
        assert r.matches("") is True

    def test_always_matches_whitespace(self):
        r = _always_rule()
        assert r.matches("   ") is True

    def test_always_matches_very_long_query(self):
        r = _always_rule()
        assert r.matches("x" * 100_000) is True


# ===========================================================================
# RouteRule.matches — KEYWORD_MATCH
# ===========================================================================

class TestRouteRuleMatchesKeyword:
    def test_keyword_present(self):
        r = _keyword_rule(keywords=["hello"])
        assert r.matches("say hello world") is True

    def test_keyword_absent(self):
        r = _keyword_rule(keywords=["hello"])
        assert r.matches("goodbye world") is False

    def test_keyword_case_insensitive(self):
        r = _keyword_rule(keywords=["HELLO"])
        assert r.matches("say hello world") is True

    def test_keyword_query_uppercase(self):
        r = _keyword_rule(keywords=["hello"])
        assert r.matches("SAY HELLO WORLD") is True

    def test_multiple_keywords_any_match(self):
        r = _keyword_rule(keywords=["foo", "bar"])
        assert r.matches("I like bar") is True

    def test_multiple_keywords_none_match(self):
        r = _keyword_rule(keywords=["foo", "bar"])
        assert r.matches("I like baz") is False

    def test_keyword_empty_list_never_matches(self):
        r = RouteRule(
            name="k",
            condition=RouteCondition.KEYWORD_MATCH,
            action=RouteAction.FORWARD,
            keywords=[],
        )
        assert r.matches("hello") is False

    def test_keyword_match_empty_query(self):
        r = _keyword_rule(keywords=["hello"])
        assert r.matches("") is False

    def test_keyword_partial_word_match(self):
        # keyword is a substring
        r = _keyword_rule(keywords=["ell"])
        assert r.matches("hello world") is True

    def test_keyword_exact_query(self):
        r = _keyword_rule(keywords=["hello"])
        assert r.matches("hello") is True


# ===========================================================================
# RouteRule.matches — LENGTH_THRESHOLD
# ===========================================================================

class TestRouteRuleMatchesLength:
    def test_length_within_range(self):
        r = _length_rule(min_length=5, max_length=20)
        assert r.matches("hello") is True  # len=5

    def test_length_below_min(self):
        r = _length_rule(min_length=5, max_length=20)
        assert r.matches("hi") is False  # len=2

    def test_length_above_max(self):
        r = _length_rule(min_length=5, max_length=10)
        assert r.matches("this is a very long query") is False

    def test_length_exactly_min(self):
        r = _length_rule(min_length=3, max_length=100)
        assert r.matches("abc") is True

    def test_length_exactly_max(self):
        r = _length_rule(min_length=0, max_length=5)
        assert r.matches("hello") is True  # len=5

    def test_length_empty_string_min_zero(self):
        r = _length_rule(min_length=0, max_length=100)
        assert r.matches("") is True  # len=0, min=0

    def test_length_empty_string_min_one(self):
        r = _length_rule(min_length=1, max_length=100)
        assert r.matches("") is False

    def test_length_default_range_matches_normal_query(self):
        r = RouteRule(
            name="x",
            condition=RouteCondition.LENGTH_THRESHOLD,
            action=RouteAction.FORWARD,
        )
        assert r.matches("some query text") is True

    def test_length_default_range_matches_very_long(self):
        r = RouteRule(
            name="x",
            condition=RouteCondition.LENGTH_THRESHOLD,
            action=RouteAction.FORWARD,
        )
        assert r.matches("x" * 10_000) is True

    def test_length_default_range_excludes_over_max(self):
        r = RouteRule(
            name="x",
            condition=RouteCondition.LENGTH_THRESHOLD,
            action=RouteAction.FORWARD,
        )
        assert r.matches("x" * 10_001) is False


# ===========================================================================
# RouteRule.matches — REGEX_MATCH
# ===========================================================================

class TestRouteRuleMatchesRegex:
    def test_regex_simple_match(self):
        r = _regex_rule(pattern=r"\d+")
        assert r.matches("query with 42 numbers") is True

    def test_regex_no_match(self):
        r = _regex_rule(pattern=r"\d+")
        assert r.matches("no numbers here") is False

    def test_regex_anchored_start(self):
        r = _regex_rule(pattern=r"^hello")
        assert r.matches("hello world") is True
        assert r.matches("say hello world") is False

    def test_regex_empty_pattern_matches_everything(self):
        r = _regex_rule(pattern="")
        assert r.matches("anything") is True
        assert r.matches("") is True

    def test_regex_compiled_on_first_use(self):
        r = _regex_rule(pattern=r"foo")
        assert r._compiled_pattern is None
        r.matches("foo bar")
        assert r._compiled_pattern is not None

    def test_regex_compiled_once_reused(self):
        r = _regex_rule(pattern=r"foo")
        r.matches("foo")
        first = r._compiled_pattern
        r.matches("foo again")
        assert r._compiled_pattern is first  # same object

    def test_regex_case_sensitive_by_default(self):
        r = _regex_rule(pattern=r"foo")
        assert r.matches("FOO") is False

    def test_regex_inline_flag_case_insensitive(self):
        r = _regex_rule(pattern=r"(?i)foo")
        assert r.matches("FOO") is True

    def test_regex_empty_query(self):
        r = _regex_rule(pattern=r"\w+")
        assert r.matches("") is False


# ===========================================================================
# QueryRouter — add/remove/rules
# ===========================================================================

class TestQueryRouterManagement:
    def test_add_rule_and_retrieve(self):
        qr = QueryRouter()
        rule = _always_rule(name="r1")
        qr.add_rule(rule)
        assert rule in qr.rules()

    def test_rules_sorted_by_priority_descending(self):
        qr = QueryRouter()
        qr.add_rule(_always_rule(name="low", priority=1))
        qr.add_rule(_always_rule(name="high", priority=10))
        qr.add_rule(_always_rule(name="mid", priority=5))
        names = [r.name for r in qr.rules()]
        assert names == ["high", "mid", "low"]

    def test_remove_existing_rule(self):
        qr = QueryRouter()
        qr.add_rule(_always_rule(name="r1"))
        removed = qr.remove_rule("r1")
        assert removed is True
        assert all(r.name != "r1" for r in qr.rules())

    def test_remove_nonexistent_rule(self):
        qr = QueryRouter()
        assert qr.remove_rule("ghost") is False

    def test_rules_empty_by_default(self):
        qr = QueryRouter()
        assert qr.rules() == []

    def test_add_multiple_same_priority(self):
        qr = QueryRouter()
        qr.add_rule(_always_rule(name="a", priority=5))
        qr.add_rule(_always_rule(name="b", priority=5))
        names = {r.name for r in qr.rules()}
        assert names == {"a", "b"}

    def test_remove_only_one_rule_leaves_others(self):
        qr = QueryRouter()
        qr.add_rule(_always_rule(name="r1"))
        qr.add_rule(_always_rule(name="r2"))
        qr.remove_rule("r1")
        names = [r.name for r in qr.rules()]
        assert names == ["r2"]


# ===========================================================================
# QueryRouter — route (unmatched default)
# ===========================================================================

class TestQueryRouterUnmatched:
    def test_no_rules_returns_forward_default(self):
        qr = QueryRouter()
        result = qr.route("hello")
        assert result.action is RouteAction.FORWARD
        assert result.target == "default"
        assert result.matched is False
        assert result.rule_name == ""

    def test_no_rules_preserves_query(self):
        qr = QueryRouter()
        result = qr.route("my query")
        assert result.query == "my query"
        assert result.original_query == "my query"

    def test_no_match_empty_query_returns_default(self):
        qr = QueryRouter()
        qr.add_rule(_keyword_rule(keywords=["find"]))
        result = qr.route("")
        assert result.matched is False


# ===========================================================================
# QueryRouter — route (FORWARD / CACHE)
# ===========================================================================

class TestQueryRouterForwardCache:
    def test_keyword_match_forward(self):
        qr = QueryRouter()
        qr.add_rule(_keyword_rule(name="fwd", keywords=["search"], action=RouteAction.FORWARD,
                                  target="search_handler"))
        result = qr.route("please search for cats")
        assert result.matched is True
        assert result.action is RouteAction.FORWARD
        assert result.target == "search_handler"
        assert result.rule_name == "fwd"

    def test_cache_action_preserved(self):
        qr = QueryRouter()
        qr.add_rule(_always_rule(name="cache_all", action=RouteAction.CACHE, target="cache"))
        result = qr.route("any query")
        assert result.action is RouteAction.CACHE
        assert result.target == "cache"

    def test_query_unchanged_for_forward(self):
        qr = QueryRouter()
        qr.add_rule(_always_rule(action=RouteAction.FORWARD))
        result = qr.route("original text")
        assert result.query == "original text"
        assert result.original_query == "original text"

    def test_original_query_preserved_after_match(self):
        qr = QueryRouter()
        qr.add_rule(_always_rule(action=RouteAction.FORWARD))
        result = qr.route("  spaced  ")
        assert result.original_query == "  spaced  "


# ===========================================================================
# QueryRouter — route (REJECT)
# ===========================================================================

class TestQueryRouterReject:
    def test_reject_action(self):
        qr = QueryRouter()
        qr.add_rule(_always_rule(name="reject_all", action=RouteAction.REJECT))
        result = qr.route("anything")
        assert result.action is RouteAction.REJECT
        assert result.matched is True

    def test_reject_preserves_query(self):
        qr = QueryRouter()
        qr.add_rule(_always_rule(name="rej", action=RouteAction.REJECT))
        result = qr.route("keep me")
        assert result.query == "keep me"

    def test_reject_with_keyword_match(self):
        qr = QueryRouter()
        qr.add_rule(_keyword_rule(name="ban", keywords=["spam"], action=RouteAction.REJECT))
        assert qr.route("this is spam").action is RouteAction.REJECT
        assert qr.route("this is fine").matched is False


# ===========================================================================
# QueryRouter — route (TRANSFORM)
# ===========================================================================

class TestQueryRouterTransform:
    def test_transform_applies_fn(self):
        qr = QueryRouter()
        rule = RouteRule(
            name="upper",
            condition=RouteCondition.ALWAYS,
            action=RouteAction.TRANSFORM,
            transform_fn=str.upper,
        )
        qr.add_rule(rule)
        result = qr.route("hello")
        assert result.query == "HELLO"
        assert result.original_query == "hello"

    def test_transform_preserves_original(self):
        qr = QueryRouter()
        rule = RouteRule(
            name="rev",
            condition=RouteCondition.ALWAYS,
            action=RouteAction.TRANSFORM,
            transform_fn=lambda q: q[::-1],
        )
        qr.add_rule(rule)
        result = qr.route("abc")
        assert result.original_query == "abc"
        assert result.query == "cba"

    def test_transform_fn_none_leaves_query_unchanged(self):
        """TRANSFORM with no transform_fn: query should be unchanged."""
        qr = QueryRouter()
        rule = RouteRule(
            name="t",
            condition=RouteCondition.ALWAYS,
            action=RouteAction.TRANSFORM,
            transform_fn=None,
        )
        qr.add_rule(rule)
        result = qr.route("hello")
        assert result.query == "hello"
        assert result.matched is True

    def test_transform_action_is_transform(self):
        qr = QueryRouter()
        rule = RouteRule(
            name="t",
            condition=RouteCondition.ALWAYS,
            action=RouteAction.TRANSFORM,
            transform_fn=lambda q: q + "!",
        )
        qr.add_rule(rule)
        result = qr.route("hello")
        assert result.action is RouteAction.TRANSFORM


# ===========================================================================
# QueryRouter — priority ordering
# ===========================================================================

class TestQueryRouterPriority:
    def test_higher_priority_wins(self):
        qr = QueryRouter()
        qr.add_rule(_always_rule(name="low", action=RouteAction.CACHE, priority=1, target="slow"))
        qr.add_rule(_always_rule(name="high", action=RouteAction.FORWARD, priority=10, target="fast"))
        result = qr.route("q")
        assert result.rule_name == "high"
        assert result.target == "fast"

    def test_equal_priority_first_added_wins(self):
        """When priorities are equal, insertion order determines which comes first
        after stable sort (Python's sorted is stable)."""
        qr = QueryRouter()
        qr.add_rule(_always_rule(name="first", priority=5, target="A"))
        qr.add_rule(_always_rule(name="second", priority=5, target="B"))
        result = qr.route("q")
        # Both have priority 5; sorted is stable so "first" stays before "second"
        assert result.rule_name == "first"

    def test_priority_with_non_overlapping_conditions(self):
        qr = QueryRouter()
        qr.add_rule(_keyword_rule(name="kw", keywords=["special"], priority=10, target="special_h"))
        qr.add_rule(_always_rule(name="catch", priority=0, target="general"))
        assert qr.route("a special query").target == "special_h"
        assert qr.route("normal query").target == "general"

    def test_negative_priority(self):
        qr = QueryRouter()
        qr.add_rule(_always_rule(name="neg", priority=-1, target="last"))
        qr.add_rule(_always_rule(name="pos", priority=1, target="first"))
        result = qr.route("q")
        assert result.rule_name == "pos"


# ===========================================================================
# QueryRouter — route_batch
# ===========================================================================

class TestQueryRouterBatch:
    def test_route_batch_empty_list(self):
        qr = QueryRouter()
        results = qr.route_batch([])
        assert results == []

    def test_route_batch_single_item(self):
        qr = QueryRouter()
        qr.add_rule(_always_rule(action=RouteAction.FORWARD))
        results = qr.route_batch(["hello"])
        assert len(results) == 1
        assert results[0].query == "hello"

    def test_route_batch_multiple_items(self):
        qr = QueryRouter()
        qr.add_rule(_keyword_rule(keywords=["foo"], action=RouteAction.REJECT, target="blocked"))
        results = qr.route_batch(["foo bar", "baz qux"])
        assert results[0].action is RouteAction.REJECT
        assert results[1].matched is False

    def test_route_batch_returns_correct_count(self):
        qr = QueryRouter()
        queries = ["a", "b", "c", "d", "e"]
        results = qr.route_batch(queries)
        assert len(results) == len(queries)

    def test_route_batch_preserves_order(self):
        qr = QueryRouter()
        qr.add_rule(_always_rule(action=RouteAction.FORWARD))
        queries = ["first", "second", "third"]
        results = qr.route_batch(queries)
        for q, r in zip(queries, results):
            assert r.query == q


# ===========================================================================
# RouteResult dataclass
# ===========================================================================

class TestRouteResult:
    def test_route_result_fields(self):
        rr = RouteResult(
            query="q",
            original_query="Q",
            action=RouteAction.FORWARD,
            target="default",
            rule_name="",
            matched=False,
        )
        assert rr.query == "q"
        assert rr.original_query == "Q"
        assert rr.action is RouteAction.FORWARD
        assert rr.target == "default"
        assert rr.rule_name == ""
        assert rr.matched is False


# ===========================================================================
# NormalizationMiddleware
# ===========================================================================

class TestNormalizationMiddleware:
    def test_lowercases_query(self):
        m = NormalizationMiddleware()
        result = m.process("HELLO WORLD", lambda q: q)
        assert result == "hello world"

    def test_strips_leading_whitespace(self):
        m = NormalizationMiddleware()
        result = m.process("   hello", lambda q: q)
        assert result == "hello"

    def test_strips_trailing_whitespace(self):
        m = NormalizationMiddleware()
        result = m.process("hello   ", lambda q: q)
        assert result == "hello"

    def test_strips_both_ends(self):
        m = NormalizationMiddleware()
        result = m.process("  Hello World  ", lambda q: q)
        assert result == "hello world"

    def test_empty_string_unchanged(self):
        m = NormalizationMiddleware()
        result = m.process("", lambda q: q)
        assert result == ""

    def test_already_normalized_unchanged(self):
        m = NormalizationMiddleware()
        result = m.process("already normalized", lambda q: q)
        assert result == "already normalized"

    def test_calls_next_fn(self):
        m = NormalizationMiddleware()
        calls = []
        def capture(q):
            calls.append(q)
            return q
        m.process("  Hello  ", capture)
        assert calls == ["hello"]


# ===========================================================================
# TruncationMiddleware
# ===========================================================================

class TestTruncationMiddleware:
    def test_truncates_long_query(self):
        m = TruncationMiddleware(max_length=10)
        result = m.process("hello world this is long", lambda q: q)
        assert result == "hello worl"

    def test_short_query_unchanged(self):
        m = TruncationMiddleware(max_length=100)
        result = m.process("hello", lambda q: q)
        assert result == "hello"

    def test_exactly_max_length(self):
        m = TruncationMiddleware(max_length=5)
        result = m.process("hello", lambda q: q)
        assert result == "hello"

    def test_empty_string(self):
        m = TruncationMiddleware(max_length=10)
        result = m.process("", lambda q: q)
        assert result == ""

    def test_default_max_length_500(self):
        m = TruncationMiddleware()
        long_query = "x" * 1000
        result = m.process(long_query, lambda q: q)
        assert len(result) == 500

    def test_max_length_zero_empties_query(self):
        m = TruncationMiddleware(max_length=0)
        result = m.process("hello", lambda q: q)
        assert result == ""

    def test_calls_next_fn_with_truncated(self):
        m = TruncationMiddleware(max_length=5)
        calls = []
        def capture(q):
            calls.append(q)
            return q
        m.process("hello world", capture)
        assert calls == ["hello"]


# ===========================================================================
# MiddlewarePipeline
# ===========================================================================

class TestMiddlewarePipeline:
    def test_empty_pipeline_returns_query_unchanged(self):
        p = MiddlewarePipeline()
        assert p.run("Hello World") == "Hello World"

    def test_single_normalization_middleware(self):
        p = MiddlewarePipeline([NormalizationMiddleware()])
        assert p.run("  HELLO  ") == "hello"

    def test_single_truncation_middleware(self):
        p = MiddlewarePipeline([TruncationMiddleware(max_length=5)])
        assert p.run("hello world") == "hello"

    def test_normalization_then_truncation(self):
        p = MiddlewarePipeline([
            NormalizationMiddleware(),
            TruncationMiddleware(max_length=5),
        ])
        # "  HELLO WORLD  " → strip+lower → "hello world" → truncate 5 → "hello"
        assert p.run("  HELLO WORLD  ") == "hello"

    def test_truncation_then_normalization(self):
        p = MiddlewarePipeline([
            TruncationMiddleware(max_length=7),
            NormalizationMiddleware(),
        ])
        # "  HELLO WORLD  " → truncate 7 → "  HELLO" → strip+lower → "hello"
        assert p.run("  HELLO WORLD  ") == "hello"

    def test_add_middleware_appends_in_order(self):
        p = MiddlewarePipeline()
        p.add(NormalizationMiddleware())
        p.add(TruncationMiddleware(max_length=3))
        # "  HELLO  " → norm → "hello" → trunc 3 → "hel"
        assert p.run("  HELLO  ") == "hel"

    def test_pipeline_init_with_none_is_empty(self):
        p = MiddlewarePipeline(middlewares=None)
        assert p.run("test") == "test"

    def test_pipeline_does_not_mutate_input_list(self):
        mw_list = [NormalizationMiddleware()]
        p = MiddlewarePipeline(mw_list)
        p.add(TruncationMiddleware())
        # original list should not be modified
        assert len(mw_list) == 1

    def test_custom_middleware(self):
        class AddExclamation(QueryMiddleware):
            def process(self, query, next_fn):
                return next_fn(query + "!")

        p = MiddlewarePipeline([AddExclamation()])
        assert p.run("hello") == "hello!"

    def test_chaining_three_custom_middlewares(self):
        """Middlewares are applied left-to-right; each receives the output of
        the previous one.  Prefix("A-") receives "q" and passes "A-q" to
        Prefix("B-"), which passes "B-A-q" to Prefix("C-"), yielding "C-B-A-q".
        """
        class Prefix(QueryMiddleware):
            def __init__(self, prefix):
                self.prefix = prefix
            def process(self, query, next_fn):
                return next_fn(self.prefix + query)

        p = MiddlewarePipeline([
            Prefix("A-"),
            Prefix("B-"),
            Prefix("C-"),
        ])
        # A- prepends first → "A-q"; B- prepends second → "B-A-q";
        # C- prepends last → "C-B-A-q"
        assert p.run("q") == "C-B-A-q"

    def test_middleware_can_short_circuit(self):
        class EarlyReturn(QueryMiddleware):
            def process(self, query, next_fn):
                return "STOPPED"  # does not call next_fn

        class NeverReached(QueryMiddleware):
            def process(self, query, next_fn):
                raise AssertionError("Should not be reached")

        p = MiddlewarePipeline([EarlyReturn(), NeverReached()])
        assert p.run("hello") == "STOPPED"


# ===========================================================================
# Edge-case integration tests
# ===========================================================================

class TestEdgeCases:
    def test_empty_query_through_router(self):
        qr = QueryRouter()
        qr.add_rule(_length_rule(min_length=1, action=RouteAction.REJECT))
        result = qr.route("")
        assert result.matched is False  # length 0 < min_length 1

    def test_very_long_query_rejected_by_length(self):
        qr = QueryRouter()
        qr.add_rule(_length_rule(min_length=0, max_length=100, action=RouteAction.REJECT,
                                 priority=10))
        qr.add_rule(_always_rule(action=RouteAction.FORWARD, priority=0))
        long_q = "x" * 200
        result = qr.route(long_q)
        # 200 > 100 so length rule doesn't match; fallback ALWAYS fires
        assert result.rule_name == "always"

    def test_overlapping_priorities_first_wins(self):
        qr = QueryRouter()
        qr.add_rule(_always_rule(name="p10", priority=10, action=RouteAction.CACHE, target="c"))
        qr.add_rule(_always_rule(name="p5", priority=5, action=RouteAction.FORWARD, target="f"))
        result = qr.route("q")
        assert result.rule_name == "p10"

    def test_transform_and_then_no_further_rules_applied(self):
        """TRANSFORM fires; subsequent rules (if any) are not applied."""
        qr = QueryRouter()
        qr.add_rule(RouteRule(
            name="upper",
            condition=RouteCondition.ALWAYS,
            action=RouteAction.TRANSFORM,
            priority=10,
            transform_fn=str.upper,
        ))
        qr.add_rule(_always_rule(name="catch", priority=0, action=RouteAction.REJECT))
        result = qr.route("hello")
        assert result.rule_name == "upper"
        assert result.query == "HELLO"

    def test_regex_and_keyword_overlap(self):
        """Both regex and keyword rules; highest priority wins."""
        qr = QueryRouter()
        qr.add_rule(_regex_rule(name="rx", pattern=r"urgent", priority=5, target="urgent_h"))
        qr.add_rule(_keyword_rule(name="kw", keywords=["urgent"], priority=3, target="kw_h"))
        result = qr.route("this is urgent")
        assert result.rule_name == "rx"
        assert result.target == "urgent_h"

    def test_pipeline_with_router(self):
        """Middleware normalises query before routing."""
        pipeline = MiddlewarePipeline([NormalizationMiddleware()])
        qr = QueryRouter()
        qr.add_rule(_keyword_rule(name="greet", keywords=["hello"], action=RouteAction.FORWARD,
                                  target="greeter"))
        # Raw query is uppercase; after pipeline it becomes lowercase
        normalized = pipeline.run("  HELLO THERE  ")
        result = qr.route(normalized)
        assert result.target == "greeter"

    def test_remove_then_readd_rule(self):
        qr = QueryRouter()
        rule = _always_rule(name="r", action=RouteAction.CACHE)
        qr.add_rule(rule)
        qr.remove_rule("r")
        assert qr.route("q").matched is False
        qr.add_rule(rule)
        assert qr.route("q").action is RouteAction.CACHE

    def test_all_conditions_can_be_used_in_one_router(self):
        qr = QueryRouter()
        qr.add_rule(_keyword_rule(name="kw", keywords=["keyword"], priority=4, target="kw_t"))
        qr.add_rule(_length_rule(name="len", min_length=50, priority=3, target="long_t"))
        qr.add_rule(_regex_rule(name="rx", pattern=r"^\d", priority=2, target="num_t"))
        qr.add_rule(_always_rule(name="catch", priority=1, target="catch_t"))

        assert qr.route("contains keyword here").target == "kw_t"
        assert qr.route("x" * 60).target == "long_t"
        assert qr.route("42 starts with number").target == "num_t"
        assert qr.route("nothing special").target == "catch_t"
