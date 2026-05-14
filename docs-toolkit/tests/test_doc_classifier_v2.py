"""Tests for docstoolkit.doc_classifier_v2."""

from __future__ import annotations

import pytest

from docstoolkit.doc_classifier_v2 import (
    Classification,
    ClassifierConfig,
    ClassifierRule,
    DocClassifierV2,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_classifier(rules=None, **cfg) -> DocClassifierV2:
    rules = rules if rules is not None else []
    return DocClassifierV2(ClassifierConfig(rules=list(rules), **cfg))


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

class TestClassifierRule:
    def test_defaults(self):
        rule = ClassifierRule(category="tech", keywords=["python"])
        assert rule.category == "tech"
        assert rule.keywords == ["python"]
        assert rule.required == []
        assert rule.excluded == []
        assert rule.weight == 1.0
        assert rule.min_matches == 1

    def test_custom(self):
        rule = ClassifierRule(
            category="ml",
            keywords=["model", "training"],
            required=["dataset"],
            excluded=["draft"],
            weight=2.5,
            min_matches=2,
        )
        assert rule.required == ["dataset"]
        assert rule.excluded == ["draft"]
        assert rule.weight == 2.5
        assert rule.min_matches == 2


class TestClassification:
    def test_construct(self):
        c = Classification(
            category="tech",
            score=0.5,
            matched_keywords=["python"],
            confidence=1.0,
        )
        assert c.category == "tech"
        assert c.score == 0.5
        assert c.matched_keywords == ["python"]
        assert c.confidence == 1.0


class TestClassifierConfig:
    def test_defaults(self):
        cfg = ClassifierConfig(rules=[])
        assert cfg.rules == []
        assert cfg.case_sensitive is False
        assert cfg.tokenize is True
        assert cfg.default_category == "unknown"

    def test_custom(self):
        rule = ClassifierRule(category="a", keywords=["x"])
        cfg = ClassifierConfig(
            rules=[rule],
            case_sensitive=True,
            tokenize=False,
            default_category="other",
        )
        assert cfg.rules == [rule]
        assert cfg.case_sensitive is True
        assert cfg.tokenize is False
        assert cfg.default_category == "other"


# ---------------------------------------------------------------------------
# Basic classification
# ---------------------------------------------------------------------------

class TestClassifyBasic:
    def test_single_rule_single_match(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["python"]),
        ])
        result = clf.classify("I love python programming")
        assert result.category == "tech"
        assert result.score > 0
        assert "python" in result.matched_keywords

    def test_returns_classification_instance(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["python"]),
        ])
        assert isinstance(clf.classify("python"), Classification)

    def test_score_normalized_by_total_keywords(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["python", "java", "rust", "go"]),
        ])
        result = clf.classify("python only")
        # 1 of 4 keywords matched, weight 1.0
        assert result.score == pytest.approx(0.25)

    def test_full_match_score_one(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["python", "java"]),
        ])
        result = clf.classify("python and java together")
        assert result.score == pytest.approx(1.0)

    def test_predict_category_returns_string(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["python"]),
        ])
        assert clf.predict_category("python rules") == "tech"


# ---------------------------------------------------------------------------
# Multiple rules
# ---------------------------------------------------------------------------

class TestClassifyMultipleRules:
    def test_winner_has_higher_score(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["python", "java"]),
            ClassifierRule(category="food", keywords=["pizza", "pasta", "salad", "soup"]),
        ])
        result = clf.classify("python and java rule and pizza is fine")
        # tech matches 2/2 = 1.0, food matches 1/4 = 0.25
        assert result.category == "tech"

    def test_other_category_wins_when_more_matches(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["python", "java", "rust", "go"]),
            ClassifierRule(category="food", keywords=["pizza"]),
        ])
        result = clf.classify("pizza and only python here")
        # tech: 1/4=0.25, food: 1/1=1.0
        assert result.category == "food"

    def test_classify_returns_top(self):
        clf = make_classifier([
            ClassifierRule(category="a", keywords=["alpha"]),
            ClassifierRule(category="b", keywords=["beta"]),
        ])
        assert clf.classify("alpha beta").category in {"a", "b"}


# ---------------------------------------------------------------------------
# Required keywords
# ---------------------------------------------------------------------------

class TestClassifyRequired:
    def test_required_present(self):
        clf = make_classifier([
            ClassifierRule(
                category="ml",
                keywords=["model"],
                required=["dataset"],
            ),
        ])
        result = clf.classify("model trained on dataset")
        assert result.category == "ml"

    def test_required_absent_falls_back(self):
        clf = make_classifier([
            ClassifierRule(
                category="ml",
                keywords=["model"],
                required=["dataset"],
            ),
        ])
        result = clf.classify("model only here")
        assert result.category == "unknown"

    def test_all_required_must_be_present(self):
        clf = make_classifier([
            ClassifierRule(
                category="ml",
                keywords=["model"],
                required=["dataset", "training"],
            ),
        ])
        result = clf.classify("model and dataset present")
        assert result.category == "unknown"

    def test_all_required_present(self):
        clf = make_classifier([
            ClassifierRule(
                category="ml",
                keywords=["model"],
                required=["dataset", "training"],
            ),
        ])
        result = clf.classify("model dataset training")
        assert result.category == "ml"


# ---------------------------------------------------------------------------
# Excluded keywords
# ---------------------------------------------------------------------------

class TestClassifyExcluded:
    def test_excluded_disqualifies(self):
        clf = make_classifier([
            ClassifierRule(
                category="tech",
                keywords=["python"],
                excluded=["draft"],
            ),
        ])
        result = clf.classify("python draft document")
        assert result.category == "unknown"

    def test_excluded_absent_keeps_rule(self):
        clf = make_classifier([
            ClassifierRule(
                category="tech",
                keywords=["python"],
                excluded=["draft"],
            ),
        ])
        result = clf.classify("python only")
        assert result.category == "tech"

    def test_any_excluded_disqualifies(self):
        clf = make_classifier([
            ClassifierRule(
                category="tech",
                keywords=["python"],
                excluded=["draft", "outdated"],
            ),
        ])
        result = clf.classify("python outdated guide")
        assert result.category == "unknown"


# ---------------------------------------------------------------------------
# min_matches
# ---------------------------------------------------------------------------

class TestClassifyMinMatches:
    def test_below_min_matches_skipped(self):
        clf = make_classifier([
            ClassifierRule(
                category="tech",
                keywords=["python", "java", "rust"],
                min_matches=2,
            ),
        ])
        result = clf.classify("python alone")
        assert result.category == "unknown"

    def test_at_min_matches_included(self):
        clf = make_classifier([
            ClassifierRule(
                category="tech",
                keywords=["python", "java", "rust"],
                min_matches=2,
            ),
        ])
        result = clf.classify("python and java")
        assert result.category == "tech"

    def test_above_min_matches_included(self):
        clf = make_classifier([
            ClassifierRule(
                category="tech",
                keywords=["python", "java", "rust"],
                min_matches=2,
            ),
        ])
        result = clf.classify("python java rust")
        assert result.category == "tech"


# ---------------------------------------------------------------------------
# Weight
# ---------------------------------------------------------------------------

class TestClassifyWeight:
    def test_weight_boosts_score(self):
        clf = make_classifier([
            ClassifierRule(category="boost", keywords=["foo"], weight=5.0),
        ])
        result = clf.classify("foo")
        assert result.score == pytest.approx(5.0)

    def test_weight_changes_ranking(self):
        clf = make_classifier([
            ClassifierRule(category="low", keywords=["a", "b"], weight=1.0),
            ClassifierRule(category="high", keywords=["c", "d"], weight=10.0),
        ])
        # both rules match 1/2; weighted high wins
        result = clf.classify("a c")
        assert result.category == "high"

    def test_zero_weight_demotes_rule(self):
        clf = make_classifier([
            ClassifierRule(category="zero", keywords=["a"], weight=0.0),
            ClassifierRule(category="normal", keywords=["b"], weight=1.0),
        ])
        result = clf.classify("a b")
        assert result.category == "normal"


# ---------------------------------------------------------------------------
# classify_all
# ---------------------------------------------------------------------------

class TestClassifyAll:
    def test_returns_all_matching(self):
        clf = make_classifier([
            ClassifierRule(category="a", keywords=["alpha"]),
            ClassifierRule(category="b", keywords=["beta"]),
            ClassifierRule(category="c", keywords=["gamma"]),
        ])
        results = clf.classify_all("alpha and beta")
        cats = {r.category for r in results}
        assert cats == {"a", "b"}

    def test_sorted_by_score_desc(self):
        clf = make_classifier([
            ClassifierRule(category="low", keywords=["a", "b", "c", "d"]),
            ClassifierRule(category="high", keywords=["x"]),
        ])
        results = clf.classify_all("a x")
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_empty_when_no_matches(self):
        clf = make_classifier([
            ClassifierRule(category="a", keywords=["alpha"]),
        ])
        results = clf.classify_all("nothing here")
        assert results == []

    def test_confidence_normalized(self):
        clf = make_classifier([
            ClassifierRule(category="a", keywords=["x"]),
            ClassifierRule(category="b", keywords=["y", "z", "w", "q"]),
        ])
        results = clf.classify_all("x y")
        # 'a' has 1/1=1.0; 'b' has 1/4=0.25. confidence normalized to top score.
        top = results[0]
        assert top.confidence == pytest.approx(1.0)
        assert all(0.0 <= r.confidence <= 1.0 for r in results)


# ---------------------------------------------------------------------------
# Default category
# ---------------------------------------------------------------------------

class TestClassifyDefault:
    def test_default_category_used(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["python"]),
        ])
        result = clf.classify("nothing related here")
        assert result.category == "unknown"
        assert result.score == 0.0
        assert result.matched_keywords == []
        assert result.confidence == 0.0

    def test_custom_default_category(self):
        clf = make_classifier(
            [ClassifierRule(category="tech", keywords=["python"])],
            default_category="misc",
        )
        result = clf.classify("nothing")
        assert result.category == "misc"

    def test_no_rules_returns_default(self):
        clf = make_classifier([])
        result = clf.classify("any text")
        assert result.category == "unknown"
        assert result.score == 0.0


# ---------------------------------------------------------------------------
# add_rule / remove_rule / categories / rule_count
# ---------------------------------------------------------------------------

class TestAddRemoveRule:
    def test_add_rule(self):
        clf = make_classifier([])
        assert clf.rule_count == 0
        clf.add_rule(ClassifierRule(category="tech", keywords=["python"]))
        assert clf.rule_count == 1
        assert "tech" in clf.categories

    def test_remove_existing_rule(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["python"]),
        ])
        assert clf.remove_rule("tech") is True
        assert clf.rule_count == 0

    def test_remove_missing_rule_returns_false(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["python"]),
        ])
        assert clf.remove_rule("nope") is False
        assert clf.rule_count == 1

    def test_categories_property(self):
        clf = make_classifier([
            ClassifierRule(category="a", keywords=["x"]),
            ClassifierRule(category="b", keywords=["y"]),
        ])
        assert clf.categories == ["a", "b"]

    def test_rule_count_property(self):
        clf = make_classifier([
            ClassifierRule(category="a", keywords=["x"]),
            ClassifierRule(category="b", keywords=["y"]),
            ClassifierRule(category="c", keywords=["z"]),
        ])
        assert clf.rule_count == 3


# ---------------------------------------------------------------------------
# Case sensitivity
# ---------------------------------------------------------------------------

class TestCaseSensitive:
    def test_default_case_insensitive(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["Python"]),
        ])
        result = clf.classify("i love PYTHON and python")
        assert result.category == "tech"

    def test_case_sensitive_match(self):
        clf = make_classifier(
            [ClassifierRule(category="tech", keywords=["Python"])],
            case_sensitive=True,
        )
        result = clf.classify("Python here")
        assert result.category == "tech"

    def test_case_sensitive_no_match(self):
        clf = make_classifier(
            [ClassifierRule(category="tech", keywords=["Python"])],
            case_sensitive=True,
        )
        result = clf.classify("python here")  # lowercase only
        assert result.category == "unknown"

    def test_case_sensitive_required(self):
        clf = make_classifier(
            [
                ClassifierRule(
                    category="tech",
                    keywords=["library"],
                    required=["Python"],
                ),
            ],
            case_sensitive=True,
        )
        # 'python' lowercase should not satisfy required 'Python'
        result = clf.classify("library python")
        assert result.category == "unknown"


# ---------------------------------------------------------------------------
# Tokenization
# ---------------------------------------------------------------------------

class TestTokenize:
    def test_tokenize_whole_word_only(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["go"]),
        ])
        # 'go' appears only as substring inside 'ago'
        result = clf.classify("a long time ago")
        assert result.category == "unknown"

    def test_tokenize_matches_whole_word(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["go"]),
        ])
        result = clf.classify("go is a language")
        assert result.category == "tech"

    def test_substring_mode(self):
        clf = make_classifier(
            [ClassifierRule(category="tech", keywords=["go"])],
            tokenize=False,
        )
        result = clf.classify("a long time ago")
        assert result.category == "tech"

    def test_tokenize_phrase(self):
        clf = make_classifier([
            ClassifierRule(category="ml", keywords=["machine learning"]),
        ])
        result = clf.classify("modern machine learning systems")
        assert result.category == "ml"

    def test_tokenize_punctuation_boundary(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["python"]),
        ])
        result = clf.classify("Python, Java, and Rust.")
        assert result.category == "tech"


# ---------------------------------------------------------------------------
# Batch
# ---------------------------------------------------------------------------

class TestBatch:
    def test_batch_returns_one_result_per_text(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["python"]),
            ClassifierRule(category="food", keywords=["pizza"]),
        ])
        results = clf.classify_batch(["python here", "pizza time", "nothing"])
        assert len(results) == 3
        assert results[0].category == "tech"
        assert results[1].category == "food"
        assert results[2].category == "unknown"

    def test_batch_empty(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["python"]),
        ])
        assert clf.classify_batch([]) == []

    def test_batch_preserves_order(self):
        clf = make_classifier([
            ClassifierRule(category="a", keywords=["alpha"]),
            ClassifierRule(category="b", keywords=["beta"]),
        ])
        results = clf.classify_batch(["beta", "alpha", "beta"])
        assert [r.category for r in results] == ["b", "a", "b"]


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_empty_text(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["python"]),
        ])
        result = clf.classify("")
        assert result.category == "unknown"
        assert result.score == 0.0

    def test_no_rules(self):
        clf = make_classifier([])
        result = clf.classify("anything goes here")
        assert result.category == "unknown"
        assert result.matched_keywords == []

    def test_empty_keywords_list(self):
        clf = make_classifier([
            ClassifierRule(category="empty", keywords=[]),
            ClassifierRule(category="tech", keywords=["python"]),
        ])
        result = clf.classify("python")
        assert result.category == "tech"

    def test_keyword_with_empty_string_ignored(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["", "python"]),
        ])
        result = clf.classify("python here")
        # empty string is ignored, only 'python' counts
        assert result.category == "tech"
        assert "python" in result.matched_keywords
        assert "" not in result.matched_keywords

    def test_duplicate_keywords_count_once_per_occurrence(self):
        clf = make_classifier([
            ClassifierRule(category="tech", keywords=["python"]),
        ])
        result = clf.classify("python python python")
        # Score is matches/total; with single keyword full score is 1.0
        assert result.score == pytest.approx(1.0)

    def test_excluded_required_combined(self):
        clf = make_classifier([
            ClassifierRule(
                category="ml",
                keywords=["model"],
                required=["dataset"],
                excluded=["draft"],
            ),
        ])
        # required present, excluded absent -> matches
        result = clf.classify("model with dataset")
        assert result.category == "ml"
        # excluded present even with required -> disqualified
        result2 = clf.classify("model with dataset draft")
        assert result2.category == "unknown"

    def test_unicode_text(self):
        clf = make_classifier([
            ClassifierRule(category="ru", keywords=["агент"]),
        ])
        result = clf.classify("умный агент с памятью")
        assert result.category == "ru"
