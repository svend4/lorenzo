"""Tests for E193 doc_inbox_filter."""
from __future__ import annotations

import pytest

from docstoolkit.doc_inbox_filter import (
    Action,
    ActionType,
    Condition,
    DocInboxFilter,
    FilterRule,
    MatchResult,
    Operator,
)


# ---------------------------------------------------------------------------
# Enum tests
# ---------------------------------------------------------------------------


class TestOperator:
    def test_eq_value(self):
        assert Operator.EQ.value == "eq"

    def test_all_operators_present(self):
        names = {o.name for o in Operator}
        assert names == {
            "EQ",
            "NE",
            "CONTAINS",
            "STARTSWITH",
            "ENDSWITH",
            "MATCHES",
            "GT",
            "LT",
            "IN",
        }

    def test_can_construct_from_value(self):
        assert Operator("contains") is Operator.CONTAINS


class TestActionType:
    def test_tag_value(self):
        assert ActionType.TAG.value == "tag"

    def test_all_actions_present(self):
        names = {a.name for a in ActionType}
        assert names == {
            "TAG",
            "MOVE",
            "FLAG",
            "ARCHIVE",
            "DELETE",
            "ASSIGN",
            "NOTIFY",
        }

    def test_can_construct_from_value(self):
        assert ActionType("notify") is ActionType.NOTIFY


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestCondition:
    def test_fields(self):
        c = Condition(field="title", operator=Operator.EQ, value="x")
        assert c.field == "title"
        assert c.operator is Operator.EQ
        assert c.value == "x"

    def test_value_default(self):
        c = Condition(field="x", operator=Operator.EQ)
        assert c.value is None


class TestAction:
    def test_fields(self):
        a = Action(action_type=ActionType.TAG, args={"tag": "x"})
        assert a.action_type is ActionType.TAG
        assert a.args == {"tag": "x"}

    def test_args_default_is_empty_dict(self):
        a = Action(action_type=ActionType.ARCHIVE)
        assert a.args == {}

    def test_args_independent_per_instance(self):
        a1 = Action(action_type=ActionType.TAG)
        a2 = Action(action_type=ActionType.TAG)
        a1.args["k"] = 1
        assert a2.args == {}


class TestFilterRule:
    def test_defaults(self):
        r = FilterRule(
            rule_id="r1",
            name="n",
            conditions=[],
            actions=[],
        )
        assert r.match_mode == "all"
        assert r.enabled is True
        assert r.priority == 0

    def test_full_construction(self):
        c = Condition(field="x", operator=Operator.EQ, value=1)
        a = Action(action_type=ActionType.TAG)
        r = FilterRule(
            rule_id="r",
            name="n",
            conditions=[c],
            actions=[a],
            match_mode="any",
            enabled=False,
            priority=5,
        )
        assert r.conditions == [c]
        assert r.actions == [a]
        assert r.match_mode == "any"
        assert r.enabled is False
        assert r.priority == 5


class TestMatchResult:
    def test_defaults(self):
        m = MatchResult(doc_id="d1")
        assert m.doc_id == "d1"
        assert m.matched_rules == []
        assert m.applied_actions == []

    def test_with_values(self):
        a = Action(action_type=ActionType.TAG)
        m = MatchResult(doc_id="d1", matched_rules=["r1"], applied_actions=[a])
        assert m.matched_rules == ["r1"]
        assert m.applied_actions == [a]


# ---------------------------------------------------------------------------
# Rule CRUD
# ---------------------------------------------------------------------------


class TestAddRule:
    def test_add_returns_rule(self):
        f = DocInboxFilter()
        r = f.add_rule("n", [], [])
        assert isinstance(r, FilterRule)
        assert r.name == "n"

    def test_add_assigns_id(self):
        f = DocInboxFilter()
        r = f.add_rule("n", [], [])
        assert r.rule_id

    def test_add_increments_count(self):
        f = DocInboxFilter()
        assert f.rule_count == 0
        f.add_rule("a", [], [])
        f.add_rule("b", [], [])
        assert f.rule_count == 2

    def test_add_default_priority_zero(self):
        f = DocInboxFilter()
        r = f.add_rule("n", [], [])
        assert r.priority == 0

    def test_add_invalid_match_mode_raises(self):
        f = DocInboxFilter()
        with pytest.raises(ValueError):
            f.add_rule("n", [], [], match_mode="xor")

    def test_add_enabled_by_default(self):
        f = DocInboxFilter()
        r = f.add_rule("n", [], [])
        assert r.enabled is True


class TestRemoveRule:
    def test_remove_existing(self):
        f = DocInboxFilter()
        r = f.add_rule("n", [], [])
        assert f.remove_rule(r.rule_id) is True
        assert f.rule_count == 0

    def test_remove_missing_returns_false(self):
        f = DocInboxFilter()
        assert f.remove_rule("nonexistent") is False

    def test_remove_does_not_affect_others(self):
        f = DocInboxFilter()
        r1 = f.add_rule("a", [], [])
        r2 = f.add_rule("b", [], [])
        f.remove_rule(r1.rule_id)
        ids = {r.rule_id for r in f.list_rules()}
        assert ids == {r2.rule_id}


class TestUpdateRule:
    def test_update_name(self):
        f = DocInboxFilter()
        r = f.add_rule("orig", [], [])
        updated = f.update_rule(r.rule_id, name="new")
        assert updated.name == "new"

    def test_update_priority(self):
        f = DocInboxFilter()
        r = f.add_rule("n", [], [])
        f.update_rule(r.rule_id, priority=10)
        assert f.list_rules()[0].priority == 10

    def test_update_missing_returns_none(self):
        f = DocInboxFilter()
        assert f.update_rule("missing", name="x") is None

    def test_update_ignores_unknown_keys(self):
        f = DocInboxFilter()
        r = f.add_rule("n", [], [])
        out = f.update_rule(r.rule_id, foobar=123)
        assert out is r

    def test_update_invalid_match_mode_raises(self):
        f = DocInboxFilter()
        r = f.add_rule("n", [], [])
        with pytest.raises(ValueError):
            f.update_rule(r.rule_id, match_mode="bogus")


class TestEnableDisable:
    def test_disable(self):
        f = DocInboxFilter()
        r = f.add_rule("n", [], [])
        assert f.disable_rule(r.rule_id) is True
        assert not f.list_rules()[0].enabled

    def test_enable(self):
        f = DocInboxFilter()
        r = f.add_rule("n", [], [])
        f.disable_rule(r.rule_id)
        assert f.enable_rule(r.rule_id) is True
        assert f.list_rules()[0].enabled

    def test_disable_missing(self):
        f = DocInboxFilter()
        assert f.disable_rule("missing") is False

    def test_enable_missing(self):
        f = DocInboxFilter()
        assert f.enable_rule("missing") is False

    def test_enabled_count(self):
        f = DocInboxFilter()
        r1 = f.add_rule("a", [], [])
        f.add_rule("b", [], [])
        f.disable_rule(r1.rule_id)
        assert f.enabled_count == 1


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------


class TestEvaluateAllMode:
    def test_all_conditions_match(self):
        f = DocInboxFilter()
        f.add_rule(
            "n",
            [
                Condition("title", Operator.EQ, "x"),
                Condition("status", Operator.EQ, "new"),
            ],
            [Action(ActionType.TAG, {"t": "hot"})],
            match_mode="all",
        )
        result = f.evaluate({"title": "x", "status": "new"}, doc_id="d1")
        assert len(result.matched_rules) == 1
        assert len(result.applied_actions) == 1

    def test_partial_match_fails_in_all_mode(self):
        f = DocInboxFilter()
        f.add_rule(
            "n",
            [
                Condition("title", Operator.EQ, "x"),
                Condition("status", Operator.EQ, "new"),
            ],
            [Action(ActionType.TAG)],
            match_mode="all",
        )
        result = f.evaluate({"title": "x", "status": "old"})
        assert result.matched_rules == []

    def test_empty_conditions_all_mode_matches(self):
        f = DocInboxFilter()
        f.add_rule("n", [], [Action(ActionType.TAG)], match_mode="all")
        result = f.evaluate({"x": 1})
        assert len(result.matched_rules) == 1


class TestEvaluateAnyMode:
    def test_any_one_match(self):
        f = DocInboxFilter()
        f.add_rule(
            "n",
            [
                Condition("title", Operator.EQ, "x"),
                Condition("status", Operator.EQ, "open"),
            ],
            [Action(ActionType.FLAG)],
            match_mode="any",
        )
        result = f.evaluate({"title": "y", "status": "open"})
        assert len(result.matched_rules) == 1

    def test_any_no_match(self):
        f = DocInboxFilter()
        f.add_rule(
            "n",
            [
                Condition("title", Operator.EQ, "x"),
                Condition("status", Operator.EQ, "open"),
            ],
            [Action(ActionType.FLAG)],
            match_mode="any",
        )
        result = f.evaluate({"title": "y", "status": "closed"})
        assert result.matched_rules == []

    def test_empty_conditions_any_mode_no_match(self):
        f = DocInboxFilter()
        f.add_rule("n", [], [Action(ActionType.TAG)], match_mode="any")
        result = f.evaluate({"x": 1})
        assert result.matched_rules == []


class TestEvaluateNoMatch:
    def test_no_rules(self):
        f = DocInboxFilter()
        r = f.evaluate({"x": 1}, doc_id="d")
        assert r.doc_id == "d"
        assert r.matched_rules == []
        assert r.applied_actions == []

    def test_disabled_rule_skipped(self):
        f = DocInboxFilter()
        r = f.add_rule(
            "n",
            [Condition("x", Operator.EQ, 1)],
            [Action(ActionType.TAG)],
        )
        f.disable_rule(r.rule_id)
        result = f.evaluate({"x": 1})
        assert result.matched_rules == []

    def test_doc_id_from_doc(self):
        f = DocInboxFilter()
        r = f.evaluate({"id": "abc"})
        assert r.doc_id == "abc"


class TestPriority:
    def test_priority_order_in_matched_rules(self):
        f = DocInboxFilter()
        low = f.add_rule(
            "low",
            [Condition("x", Operator.EQ, 1)],
            [Action(ActionType.TAG, {"p": "low"})],
            priority=1,
        )
        high = f.add_rule(
            "high",
            [Condition("x", Operator.EQ, 1)],
            [Action(ActionType.TAG, {"p": "high"})],
            priority=10,
        )
        result = f.evaluate({"x": 1})
        assert result.matched_rules == [high.rule_id, low.rule_id]

    def test_actions_concatenated_by_priority(self):
        f = DocInboxFilter()
        f.add_rule(
            "low",
            [Condition("x", Operator.EQ, 1)],
            [Action(ActionType.TAG, {"p": "low"})],
            priority=1,
        )
        f.add_rule(
            "high",
            [Condition("x", Operator.EQ, 1)],
            [Action(ActionType.TAG, {"p": "high"})],
            priority=10,
        )
        result = f.evaluate({"x": 1})
        assert [a.args["p"] for a in result.applied_actions] == ["high", "low"]

    def test_list_rules_priority_order(self):
        f = DocInboxFilter()
        f.add_rule("a", [], [], priority=1)
        f.add_rule("b", [], [], priority=5)
        f.add_rule("c", [], [], priority=3)
        priorities = [r.priority for r in f.list_rules()]
        assert priorities == [5, 3, 1]


# ---------------------------------------------------------------------------
# match_single per operator
# ---------------------------------------------------------------------------


class TestMatchSingleEq:
    def test_eq_match(self):
        f = DocInboxFilter()
        assert f.match_single({"x": 1}, Condition("x", Operator.EQ, 1))

    def test_eq_no_match(self):
        f = DocInboxFilter()
        assert not f.match_single({"x": 1}, Condition("x", Operator.EQ, 2))

    def test_ne_match(self):
        f = DocInboxFilter()
        assert f.match_single({"x": 1}, Condition("x", Operator.NE, 2))

    def test_ne_no_match(self):
        f = DocInboxFilter()
        assert not f.match_single({"x": 1}, Condition("x", Operator.NE, 1))


class TestMatchSingleContains:
    def test_str_contains(self):
        f = DocInboxFilter()
        assert f.match_single(
            {"title": "hello world"},
            Condition("title", Operator.CONTAINS, "world"),
        )

    def test_str_not_contains(self):
        f = DocInboxFilter()
        assert not f.match_single(
            {"title": "hello world"},
            Condition("title", Operator.CONTAINS, "zzz"),
        )

    def test_list_contains(self):
        f = DocInboxFilter()
        assert f.match_single(
            {"tags": ["a", "b"]},
            Condition("tags", Operator.CONTAINS, "a"),
        )

    def test_list_not_contains(self):
        f = DocInboxFilter()
        assert not f.match_single(
            {"tags": ["a", "b"]},
            Condition("tags", Operator.CONTAINS, "z"),
        )

    def test_contains_on_int_is_false(self):
        f = DocInboxFilter()
        assert not f.match_single(
            {"x": 7}, Condition("x", Operator.CONTAINS, 7)
        )


class TestMatchSingleStarts:
    def test_startswith(self):
        f = DocInboxFilter()
        assert f.match_single(
            {"name": "report-001"},
            Condition("name", Operator.STARTSWITH, "report"),
        )

    def test_not_startswith(self):
        f = DocInboxFilter()
        assert not f.match_single(
            {"name": "report-001"},
            Condition("name", Operator.STARTSWITH, "memo"),
        )

    def test_endswith(self):
        f = DocInboxFilter()
        assert f.match_single(
            {"name": "report.md"},
            Condition("name", Operator.ENDSWITH, ".md"),
        )

    def test_not_endswith(self):
        f = DocInboxFilter()
        assert not f.match_single(
            {"name": "report.md"},
            Condition("name", Operator.ENDSWITH, ".txt"),
        )

    def test_startswith_non_string_false(self):
        f = DocInboxFilter()
        assert not f.match_single(
            {"x": 5}, Condition("x", Operator.STARTSWITH, "5")
        )


class TestMatchSingleMatches:
    def test_regex_match(self):
        f = DocInboxFilter()
        assert f.match_single(
            {"name": "ABC-123"},
            Condition("name", Operator.MATCHES, r"^[A-Z]+-\d+$"),
        )

    def test_regex_no_match(self):
        f = DocInboxFilter()
        assert not f.match_single(
            {"name": "abc"},
            Condition("name", Operator.MATCHES, r"^\d+$"),
        )

    def test_regex_partial(self):
        f = DocInboxFilter()
        # re.search is used → partial matches succeed
        assert f.match_single(
            {"name": "prefix-123-suffix"},
            Condition("name", Operator.MATCHES, r"\d+"),
        )

    def test_invalid_regex_returns_false(self):
        f = DocInboxFilter()
        assert not f.match_single(
            {"name": "x"},
            Condition("name", Operator.MATCHES, r"("),
        )


class TestMatchSingleGtLt:
    def test_gt(self):
        f = DocInboxFilter()
        assert f.match_single({"n": 5}, Condition("n", Operator.GT, 3))

    def test_gt_false(self):
        f = DocInboxFilter()
        assert not f.match_single({"n": 1}, Condition("n", Operator.GT, 3))

    def test_lt(self):
        f = DocInboxFilter()
        assert f.match_single({"n": 1}, Condition("n", Operator.LT, 3))

    def test_lt_false(self):
        f = DocInboxFilter()
        assert not f.match_single({"n": 5}, Condition("n", Operator.LT, 3))

    def test_gt_type_error_returns_false(self):
        f = DocInboxFilter()
        assert not f.match_single(
            {"n": "abc"}, Condition("n", Operator.GT, 3)
        )


class TestMatchSingleIn:
    def test_in_list(self):
        f = DocInboxFilter()
        assert f.match_single(
            {"status": "open"},
            Condition("status", Operator.IN, ["open", "review"]),
        )

    def test_in_tuple(self):
        f = DocInboxFilter()
        assert f.match_single(
            {"status": "open"},
            Condition("status", Operator.IN, ("open", "review")),
        )

    def test_not_in(self):
        f = DocInboxFilter()
        assert not f.match_single(
            {"status": "closed"},
            Condition("status", Operator.IN, ["open", "review"]),
        )

    def test_in_non_collection_value_false(self):
        f = DocInboxFilter()
        assert not f.match_single(
            {"status": "open"},
            Condition("status", Operator.IN, "open"),
        )


class TestFieldDotted:
    def test_dotted_access(self):
        f = DocInboxFilter()
        doc = {"metadata": {"tags": ["a", "b"]}}
        assert f.match_single(
            doc, Condition("metadata.tags", Operator.CONTAINS, "a")
        )

    def test_dotted_deep(self):
        f = DocInboxFilter()
        doc = {"a": {"b": {"c": 5}}}
        assert f.match_single(doc, Condition("a.b.c", Operator.EQ, 5))

    def test_dotted_missing_intermediate(self):
        f = DocInboxFilter()
        doc = {"a": {"b": 1}}
        assert not f.match_single(doc, Condition("a.x.c", Operator.EQ, 5))


class TestMissingField:
    def test_missing_field_eq_false(self):
        f = DocInboxFilter()
        assert not f.match_single(
            {}, Condition("x", Operator.EQ, 1)
        )

    def test_missing_field_ne_true(self):
        f = DocInboxFilter()
        assert f.match_single(
            {}, Condition("x", Operator.NE, 1)
        )

    def test_missing_field_contains_false(self):
        f = DocInboxFilter()
        assert not f.match_single(
            {}, Condition("x", Operator.CONTAINS, "a")
        )

    def test_missing_field_in_false(self):
        f = DocInboxFilter()
        assert not f.match_single(
            {}, Condition("x", Operator.IN, [1, 2])
        )


# ---------------------------------------------------------------------------
# Batch + listing + import/export + clear + edge cases
# ---------------------------------------------------------------------------


class TestEvaluateBatch:
    def test_batch_basic(self):
        f = DocInboxFilter()
        f.add_rule(
            "n",
            [Condition("status", Operator.EQ, "open")],
            [Action(ActionType.FLAG)],
        )
        docs = [
            {"id": "a", "status": "open"},
            {"id": "b", "status": "closed"},
            {"id": "c", "status": "open"},
        ]
        results = f.evaluate_batch(docs)
        assert len(results) == 3
        assert len(results[0].matched_rules) == 1
        assert len(results[1].matched_rules) == 0
        assert len(results[2].matched_rules) == 1

    def test_batch_empty(self):
        f = DocInboxFilter()
        assert f.evaluate_batch([]) == []

    def test_batch_doc_ids_propagated(self):
        f = DocInboxFilter()
        docs = [{"id": "x"}, {"id": "y"}]
        results = f.evaluate_batch(docs)
        assert [r.doc_id for r in results] == ["x", "y"]


class TestListRules:
    def test_empty(self):
        f = DocInboxFilter()
        assert f.list_rules() == []

    def test_enabled_only(self):
        f = DocInboxFilter()
        r1 = f.add_rule("a", [], [])
        f.add_rule("b", [], [])
        f.disable_rule(r1.rule_id)
        names = [r.name for r in f.list_rules(enabled_only=True)]
        assert names == ["b"]

    def test_lists_all_by_default(self):
        f = DocInboxFilter()
        r1 = f.add_rule("a", [], [])
        f.add_rule("b", [], [])
        f.disable_rule(r1.rule_id)
        assert len(f.list_rules()) == 2


class TestImportExport:
    def test_export_empty(self):
        f = DocInboxFilter()
        assert f.export_rules() == []

    def test_round_trip(self):
        f = DocInboxFilter()
        f.add_rule(
            "n",
            [Condition("title", Operator.CONTAINS, "foo")],
            [Action(ActionType.TAG, {"tag": "x"})],
            match_mode="any",
            priority=3,
        )
        exported = f.export_rules()
        assert len(exported) == 1

        f2 = DocInboxFilter()
        count = f2.import_rules(exported)
        assert count == 1

        e2 = f2.export_rules()
        assert e2 == exported

    def test_import_skips_invalid_operator(self):
        f = DocInboxFilter()
        count = f.import_rules(
            [
                {
                    "name": "bad",
                    "conditions": [
                        {"field": "x", "operator": "nope", "value": 1}
                    ],
                    "actions": [],
                }
            ]
        )
        assert count == 0
        assert f.rule_count == 0

    def test_import_skips_invalid_action(self):
        f = DocInboxFilter()
        count = f.import_rules(
            [
                {
                    "name": "bad",
                    "conditions": [],
                    "actions": [{"action_type": "nope", "args": {}}],
                }
            ]
        )
        assert count == 0

    def test_import_skips_invalid_match_mode(self):
        f = DocInboxFilter()
        count = f.import_rules(
            [{"name": "n", "conditions": [], "actions": [], "match_mode": "x"}]
        )
        assert count == 0

    def test_import_skips_non_dict_entries(self):
        f = DocInboxFilter()
        count = f.import_rules([None, "foo", 42])
        assert count == 0

    def test_export_preserves_priority_and_enabled(self):
        f = DocInboxFilter()
        r = f.add_rule("n", [], [], priority=7)
        f.disable_rule(r.rule_id)
        exp = f.export_rules()
        assert exp[0]["priority"] == 7
        assert exp[0]["enabled"] is False


class TestClear:
    def test_clear_removes_all(self):
        f = DocInboxFilter()
        f.add_rule("a", [], [])
        f.add_rule("b", [], [])
        f.clear()
        assert f.rule_count == 0

    def test_clear_on_empty(self):
        f = DocInboxFilter()
        f.clear()  # should not raise
        assert f.rule_count == 0


class TestEdgeCases:
    def test_match_conditions_invalid_mode(self):
        f = DocInboxFilter()
        with pytest.raises(ValueError):
            f.match_conditions({"x": 1}, [], mode="xor")

    def test_evaluate_doc_without_id(self):
        f = DocInboxFilter()
        result = f.evaluate({"x": 1})
        # No id field → empty string default
        assert result.doc_id == ""

    def test_evaluate_explicit_doc_id_overrides(self):
        f = DocInboxFilter()
        result = f.evaluate({"id": "from-doc"}, doc_id="explicit")
        assert result.doc_id == "explicit"

    def test_multiple_rules_with_different_modes(self):
        f = DocInboxFilter()
        f.add_rule(
            "all",
            [
                Condition("a", Operator.EQ, 1),
                Condition("b", Operator.EQ, 2),
            ],
            [Action(ActionType.TAG, {"t": "all"})],
            match_mode="all",
        )
        f.add_rule(
            "any",
            [
                Condition("a", Operator.EQ, 99),
                Condition("b", Operator.EQ, 2),
            ],
            [Action(ActionType.TAG, {"t": "any"})],
            match_mode="any",
        )
        result = f.evaluate({"a": 1, "b": 2})
        tags = {a.args["t"] for a in result.applied_actions}
        assert tags == {"all", "any"}

    def test_thread_safety_smoke(self):
        import threading as _t

        f = DocInboxFilter()
        errors: list = []

        def worker() -> None:
            try:
                for i in range(50):
                    r = f.add_rule(f"n{i}", [], [])
                    f.disable_rule(r.rule_id)
                    f.enable_rule(r.rule_id)
                    f.remove_rule(r.rule_id)
            except Exception as exc:  # pragma: no cover
                errors.append(exc)

        threads = [_t.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert errors == []
        assert f.rule_count == 0

    def test_update_rule_replace_conditions(self):
        f = DocInboxFilter()
        r = f.add_rule(
            "n",
            [Condition("x", Operator.EQ, 1)],
            [Action(ActionType.TAG)],
        )
        f.update_rule(
            r.rule_id, conditions=[Condition("y", Operator.EQ, 2)]
        )
        # Old condition should no longer match
        res1 = f.evaluate({"x": 1})
        res2 = f.evaluate({"y": 2})
        assert res1.matched_rules == []
        assert len(res2.matched_rules) == 1

    def test_disabled_rule_not_in_enabled_count(self):
        f = DocInboxFilter()
        r = f.add_rule("a", [], [])
        f.disable_rule(r.rule_id)
        assert f.rule_count == 1
        assert f.enabled_count == 0
