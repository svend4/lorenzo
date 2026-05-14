"""Tests for the query_rewrite module (E16).

Covers:
- RewriteRule: applies_to, apply (case-insensitive)
- RuleSet: add, remove, get, rules_for (priority ordering), all_rules
- ExpansionConfig defaults
- QueryExpander: add_synonym, expand (original first, dedup, max_expansions cap,
  min_query_len guard), synonym_count
- RewriteConfig defaults and fields
- RewriteResult: was_rewritten, expansion_count
- QueryRewriter: lowercase, strip_stopwords, apply_rules, expand_synonyms,
  no-op paths, dependency wiring
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.query_rewrite import (
    RewriteRule,
    RuleSet,
    ExpansionConfig,
    QueryExpander,
    RewriteConfig,
    RewriteResult,
    QueryRewriter,
)


# ===========================================================================
# RewriteRule
# ===========================================================================

class TestRewriteRuleAppliesTo:
    def test_exact_match(self):
        rule = RewriteRule("r1", "cat", "feline")
        assert rule.applies_to("I have a cat") is True

    def test_no_match(self):
        rule = RewriteRule("r1", "dog", "canine")
        assert rule.applies_to("I have a cat") is False

    def test_case_insensitive_upper(self):
        rule = RewriteRule("r1", "cat", "feline")
        assert rule.applies_to("CAT in the hat") is True

    def test_case_insensitive_mixed(self):
        rule = RewriteRule("r1", "CAT", "feline")
        assert rule.applies_to("I saw a cat today") is True

    def test_pattern_in_middle(self):
        rule = RewriteRule("r1", "doc", "document")
        assert rule.applies_to("docstring") is True

    def test_empty_query(self):
        rule = RewriteRule("r1", "cat", "feline")
        assert rule.applies_to("") is False

    def test_empty_pattern_always_matches(self):
        rule = RewriteRule("r1", "", "x")
        assert rule.applies_to("anything") is True

    def test_pattern_at_start(self):
        rule = RewriteRule("r1", "search", "find")
        assert rule.applies_to("search for documents") is True

    def test_pattern_at_end(self):
        rule = RewriteRule("r1", "docs", "documents")
        assert rule.applies_to("find the docs") is True


class TestRewriteRuleApply:
    def test_basic_replacement(self):
        rule = RewriteRule("r1", "cat", "feline")
        assert rule.apply("I have a cat") == "I have a feline"

    def test_case_insensitive_replacement(self):
        rule = RewriteRule("r1", "cat", "feline")
        assert rule.apply("CAT in the hat") == "feline in the hat"

    def test_all_occurrences_replaced(self):
        rule = RewriteRule("r1", "cat", "feline")
        result = rule.apply("cat and cat and CAT")
        assert result == "feline and feline and feline"

    def test_no_match_returns_original(self):
        rule = RewriteRule("r1", "dog", "canine")
        assert rule.apply("I have a cat") == "I have a cat"

    def test_replacement_preserves_surrounding_text(self):
        rule = RewriteRule("r1", "ML", "machine learning")
        result = rule.apply("use ML techniques")
        assert result == "use machine learning techniques"

    def test_rule_id_and_priority_fields(self):
        rule = RewriteRule("my-rule", "x", "y", priority=10, description="Test rule")
        assert rule.rule_id == "my-rule"
        assert rule.priority == 10
        assert rule.description == "Test rule"

    def test_default_priority_is_zero(self):
        rule = RewriteRule("r1", "x", "y")
        assert rule.priority == 0

    def test_default_description_is_empty(self):
        rule = RewriteRule("r1", "x", "y")
        assert rule.description == ""


# ===========================================================================
# RuleSet
# ===========================================================================

class TestRuleSetAdd:
    def test_add_single_rule(self):
        rs = RuleSet()
        rule = RewriteRule("r1", "cat", "feline")
        rs.add(rule)
        assert rs.get("r1") is rule

    def test_add_overwrites_existing(self):
        rs = RuleSet()
        rs.add(RewriteRule("r1", "cat", "feline"))
        new_rule = RewriteRule("r1", "cat", "kitty")
        rs.add(new_rule)
        assert rs.get("r1").replacement == "kitty"

    def test_all_rules_after_add(self):
        rs = RuleSet()
        rs.add(RewriteRule("r1", "a", "b"))
        rs.add(RewriteRule("r2", "c", "d"))
        ids = [r.rule_id for r in rs.all_rules()]
        assert "r1" in ids
        assert "r2" in ids


class TestRuleSetRemove:
    def test_remove_existing_returns_true(self):
        rs = RuleSet()
        rs.add(RewriteRule("r1", "a", "b"))
        assert rs.remove("r1") is True
        assert rs.get("r1") is None

    def test_remove_nonexistent_returns_false(self):
        rs = RuleSet()
        assert rs.remove("nonexistent") is False

    def test_remove_leaves_other_rules(self):
        rs = RuleSet()
        rs.add(RewriteRule("r1", "a", "b"))
        rs.add(RewriteRule("r2", "c", "d"))
        rs.remove("r1")
        assert rs.get("r2") is not None


class TestRuleSetGet:
    def test_get_existing(self):
        rs = RuleSet()
        rule = RewriteRule("r1", "a", "b")
        rs.add(rule)
        assert rs.get("r1") is rule

    def test_get_missing_returns_none(self):
        rs = RuleSet()
        assert rs.get("missing") is None


class TestRuleSetRulesFor:
    def test_returns_applicable_rules(self):
        rs = RuleSet()
        rs.add(RewriteRule("r1", "cat", "feline", priority=5))
        rs.add(RewriteRule("r2", "dog", "canine", priority=3))
        result = rs.rules_for("I have a cat")
        ids = [r.rule_id for r in result]
        assert "r1" in ids
        assert "r2" not in ids

    def test_sorted_by_priority_desc(self):
        rs = RuleSet()
        rs.add(RewriteRule("low", "cat", "a", priority=1))
        rs.add(RewriteRule("high", "cat", "b", priority=10))
        rs.add(RewriteRule("mid", "cat", "c", priority=5))
        result = rs.rules_for("cat")
        priorities = [r.priority for r in result]
        assert priorities == sorted(priorities, reverse=True)

    def test_no_rules_match(self):
        rs = RuleSet()
        rs.add(RewriteRule("r1", "dog", "canine"))
        result = rs.rules_for("I have a cat")
        assert result == []

    def test_empty_ruleset_returns_empty(self):
        rs = RuleSet()
        assert rs.rules_for("any query") == []

    def test_multiple_rules_match(self):
        rs = RuleSet()
        rs.add(RewriteRule("r1", "cat", "feline", priority=2))
        rs.add(RewriteRule("r2", "have", "own", priority=4))
        result = rs.rules_for("I have a cat")
        assert len(result) == 2
        assert result[0].rule_id == "r2"  # higher priority first

    def test_case_insensitive_matching(self):
        rs = RuleSet()
        rs.add(RewriteRule("r1", "CAT", "feline"))
        result = rs.rules_for("i have a cat")
        assert len(result) == 1


class TestRuleSetAllRules:
    def test_empty_returns_empty_list(self):
        rs = RuleSet()
        assert rs.all_rules() == []

    def test_returns_all_added_rules(self):
        rs = RuleSet()
        rs.add(RewriteRule("a", "x", "y"))
        rs.add(RewriteRule("b", "p", "q"))
        assert len(rs.all_rules()) == 2


# ===========================================================================
# ExpansionConfig
# ===========================================================================

class TestExpansionConfig:
    def test_defaults(self):
        cfg = ExpansionConfig()
        assert cfg.max_expansions == 5
        assert cfg.min_query_len == 3

    def test_custom_values(self):
        cfg = ExpansionConfig(max_expansions=10, min_query_len=5)
        assert cfg.max_expansions == 10
        assert cfg.min_query_len == 5


# ===========================================================================
# QueryExpander
# ===========================================================================

class TestQueryExpanderSynonymCount:
    def test_empty(self):
        qe = QueryExpander()
        assert qe.synonym_count() == 0

    def test_single_synonym(self):
        qe = QueryExpander()
        qe.add_synonym("cat", ["feline"])
        assert qe.synonym_count() == 1

    def test_multiple_synonyms(self):
        qe = QueryExpander()
        qe.add_synonym("cat", ["feline", "kitty"])
        assert qe.synonym_count() == 2

    def test_multiple_terms(self):
        qe = QueryExpander()
        qe.add_synonym("cat", ["feline"])
        qe.add_synonym("dog", ["canine", "hound"])
        assert qe.synonym_count() == 3


class TestQueryExpanderAddSynonym:
    def test_add_extends_existing(self):
        qe = QueryExpander()
        qe.add_synonym("cat", ["feline"])
        qe.add_synonym("cat", ["kitty"])
        assert qe.synonym_count() == 2

    def test_add_no_duplicate_synonyms(self):
        qe = QueryExpander()
        qe.add_synonym("cat", ["feline"])
        qe.add_synonym("cat", ["feline"])
        assert qe.synonym_count() == 1


class TestQueryExpanderExpand:
    def test_original_always_first(self):
        qe = QueryExpander()
        qe.add_synonym("cat", ["feline"])
        result = qe.expand("I have a cat")
        assert result[0] == "I have a cat"

    def test_synonym_produces_variant(self):
        qe = QueryExpander()
        qe.add_synonym("cat", ["feline"])
        result = qe.expand("I have a cat")
        assert "I have a feline" in result

    def test_no_synonyms_returns_original_only(self):
        qe = QueryExpander()
        result = qe.expand("I have a cat")
        assert result == ["I have a cat"]

    def test_deduplication(self):
        qe = QueryExpander()
        qe.add_synonym("cat", ["cat"])  # synonym same as original
        result = qe.expand("I have a cat")
        assert result.count("I have a cat") == 1

    def test_max_expansions_cap(self):
        qe = QueryExpander()
        qe.add_synonym("cat", ["feline", "kitty", "pussycat", "tabby", "mouser"])
        cfg = ExpansionConfig(max_expansions=3)
        result = qe.expand("I have a cat", config=cfg)
        assert len(result) <= 3

    def test_min_query_len_guard(self):
        qe = QueryExpander()
        qe.add_synonym("hi", ["hello"])
        cfg = ExpansionConfig(min_query_len=5)
        result = qe.expand("hi", config=cfg)
        assert result == ["hi"]

    def test_min_query_len_met(self):
        qe = QueryExpander()
        qe.add_synonym("cat", ["feline"])
        cfg = ExpansionConfig(min_query_len=3)
        result = qe.expand("cat", config=cfg)
        assert "feline" in result

    def test_case_insensitive_term_matching(self):
        qe = QueryExpander()
        qe.add_synonym("cat", ["feline"])
        result = qe.expand("I have a CAT")
        assert any("feline" in r for r in result)

    def test_default_config_used_when_none(self):
        qe = QueryExpander()
        qe.add_synonym("a", ["b"])
        result = qe.expand("a query")
        assert len(result) <= 5  # default max_expansions


# ===========================================================================
# RewriteConfig
# ===========================================================================

class TestRewriteConfig:
    def test_defaults(self):
        cfg = RewriteConfig()
        assert cfg.apply_rules is True
        assert cfg.expand_synonyms is False
        assert cfg.lowercase is True
        assert cfg.strip_stopwords is False
        assert cfg.stopwords == set()

    def test_custom_stopwords(self):
        cfg = RewriteConfig(stopwords={"the", "a", "is"})
        assert "the" in cfg.stopwords


# ===========================================================================
# RewriteResult
# ===========================================================================

class TestRewriteResult:
    def test_was_rewritten_true(self):
        rr = RewriteResult("Hello", "hello", [], [])
        assert rr.was_rewritten() is True

    def test_was_rewritten_false(self):
        rr = RewriteResult("hello", "hello", [], [])
        assert rr.was_rewritten() is False

    def test_expansion_count_zero(self):
        rr = RewriteResult("q", "q", [], [])
        assert rr.expansion_count() == 0

    def test_expansion_count_nonzero(self):
        rr = RewriteResult("q", "q", [], ["q1", "q2"])
        assert rr.expansion_count() == 2

    def test_fields(self):
        rr = RewriteResult("original", "rewritten", ["r1"], ["e1"])
        assert rr.original == "original"
        assert rr.rewritten == "rewritten"
        assert rr.rules_applied == ["r1"]
        assert rr.expansions == ["e1"]


# ===========================================================================
# QueryRewriter
# ===========================================================================

class TestQueryRewriterLowercase:
    def test_lowercase_enabled_by_default(self):
        qr = QueryRewriter()
        result = qr.rewrite("Hello World")
        assert result.rewritten == "hello world"

    def test_lowercase_disabled(self):
        cfg = RewriteConfig(lowercase=False)
        qr = QueryRewriter(config=cfg)
        result = qr.rewrite("Hello World")
        assert result.rewritten == "Hello World"

    def test_original_preserved(self):
        qr = QueryRewriter()
        result = qr.rewrite("Hello World")
        assert result.original == "Hello World"


class TestQueryRewriterStopwords:
    def test_strip_stopwords_removes_tokens(self):
        cfg = RewriteConfig(
            strip_stopwords=True,
            stopwords={"the", "a", "is"},
            lowercase=False,
        )
        qr = QueryRewriter(config=cfg)
        result = qr.rewrite("the cat is a feline")
        assert "the" not in result.rewritten
        assert "is" not in result.rewritten
        assert "cat" in result.rewritten
        assert "feline" in result.rewritten

    def test_strip_stopwords_disabled(self):
        cfg = RewriteConfig(
            strip_stopwords=False,
            stopwords={"the", "a"},
            lowercase=False,
        )
        qr = QueryRewriter(config=cfg)
        result = qr.rewrite("the cat")
        assert "the" in result.rewritten

    def test_empty_stopwords_no_change(self):
        cfg = RewriteConfig(strip_stopwords=True, stopwords=set(), lowercase=False)
        qr = QueryRewriter(config=cfg)
        result = qr.rewrite("the quick brown fox")
        assert result.rewritten == "the quick brown fox"


class TestQueryRewriterApplyRules:
    def test_rule_applied(self):
        rs = RuleSet()
        rs.add(RewriteRule("r1", "cat", "feline", priority=1))
        cfg = RewriteConfig(apply_rules=True, lowercase=False)
        qr = QueryRewriter(config=cfg, rule_set=rs)
        result = qr.rewrite("I have a cat")
        assert result.rewritten == "I have a feline"
        assert "r1" in result.rules_applied

    def test_apply_rules_disabled(self):
        rs = RuleSet()
        rs.add(RewriteRule("r1", "cat", "feline"))
        cfg = RewriteConfig(apply_rules=False, lowercase=False)
        qr = QueryRewriter(config=cfg, rule_set=rs)
        result = qr.rewrite("I have a cat")
        assert result.rewritten == "I have a cat"
        assert result.rules_applied == []

    def test_multiple_rules_applied(self):
        rs = RuleSet()
        rs.add(RewriteRule("r1", "cat", "feline", priority=2))
        rs.add(RewriteRule("r2", "have", "own", priority=1))
        cfg = RewriteConfig(apply_rules=True, lowercase=False)
        qr = QueryRewriter(config=cfg, rule_set=rs)
        result = qr.rewrite("I have a cat")
        assert "r1" in result.rules_applied
        assert "r2" in result.rules_applied

    def test_no_rules_returns_original_unchanged(self):
        qr = QueryRewriter(config=RewriteConfig(lowercase=False))
        result = qr.rewrite("some query")
        assert result.rewritten == "some query"
        assert result.rules_applied == []


class TestQueryRewriterExpandSynonyms:
    def test_expand_synonyms_produces_expansions(self):
        expander = QueryExpander()
        expander.add_synonym("cat", ["feline", "kitty"])
        cfg = RewriteConfig(expand_synonyms=True, lowercase=False)
        qr = QueryRewriter(config=cfg, expander=expander)
        result = qr.rewrite("I have a cat")
        assert result.expansion_count() > 0

    def test_expand_synonyms_disabled(self):
        expander = QueryExpander()
        expander.add_synonym("cat", ["feline"])
        cfg = RewriteConfig(expand_synonyms=False, lowercase=False)
        qr = QueryRewriter(config=cfg, expander=expander)
        result = qr.rewrite("I have a cat")
        assert result.expansion_count() == 0
        assert result.expansions == []

    def test_was_rewritten_false_no_change(self):
        qr = QueryRewriter(config=RewriteConfig(lowercase=False))
        result = qr.rewrite("unchanged query")
        assert result.was_rewritten() is False

    def test_was_rewritten_true_after_lowercase(self):
        qr = QueryRewriter(config=RewriteConfig(lowercase=True))
        result = qr.rewrite("Hello")
        assert result.was_rewritten() is True


class TestQueryRewriterDefaults:
    def test_default_constructor(self):
        qr = QueryRewriter()
        result = qr.rewrite("Hello")
        assert result.original == "Hello"
        assert result.rewritten == "hello"
        assert result.rules_applied == []
        assert result.expansions == []

    def test_result_type(self):
        qr = QueryRewriter()
        result = qr.rewrite("test")
        assert isinstance(result, RewriteResult)
