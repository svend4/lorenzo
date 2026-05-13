"""Tests for docstoolkit.doc_classifier (E58 — keyword-frequency classifier).

Coverage target: ≥ 72 tests.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.doc_classifier import (
    Category,
    CategoryHierarchy,
    ClassificationResult,
    ClassifierConfig,
    DocumentClassifier,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_classifier(**cfg_kwargs) -> DocumentClassifier:
    """Return a DocumentClassifier pre-loaded with three categories."""
    clf = DocumentClassifier(ClassifierConfig(**cfg_kwargs) if cfg_kwargs else None)
    clf.add_category(Category("tech", keywords=["python", "code", "algorithm", "function"]))
    clf.add_category(Category("cooking", keywords=["recipe", "bake", "oven", "flour", "butter"]))
    clf.add_category(Category("sports", keywords=["football", "players", "goal", "match", "team"]))
    return clf


# ===========================================================================
# 1. Category dataclass
# ===========================================================================

class TestCategoryDataclass:
    def test_name_field(self):
        c = Category("tech")
        assert c.name == "tech"

    def test_description_default(self):
        c = Category("tech")
        assert c.description == ""

    def test_description_set(self):
        c = Category("tech", description="Technology documents")
        assert c.description == "Technology documents"

    def test_keywords_default_empty_list(self):
        c = Category("tech")
        assert c.keywords == []

    def test_keywords_set(self):
        c = Category("tech", keywords=["python", "java"])
        assert c.keywords == ["python", "java"]

    def test_parent_default_none(self):
        c = Category("tech")
        assert c.parent is None

    def test_parent_set_string(self):
        c = Category("python", parent="tech")
        assert c.parent == "tech"

    def test_keywords_independent_across_instances(self):
        """Default factory must produce a separate list per instance."""
        a = Category("a")
        b = Category("b")
        a.keywords.append("x")
        assert b.keywords == []

    def test_category_equality(self):
        a = Category("tech", description="d", keywords=["k"], parent="root")
        b = Category("tech", description="d", keywords=["k"], parent="root")
        assert a == b

    def test_category_inequality_name(self):
        assert Category("tech") != Category("cooking")


# ===========================================================================
# 2. ClassificationResult dataclass
# ===========================================================================

class TestClassificationResult:
    def _make(self, **kwargs):
        defaults = dict(
            doc_id="doc1",
            text_snippet="some text",
            scores={"tech": 0.7, "cooking": 0.3},
            top_category="tech",
            confidence=0.7,
        )
        defaults.update(kwargs)
        return ClassificationResult(**defaults)

    def test_doc_id_field(self):
        r = self._make(doc_id="abc")
        assert r.doc_id == "abc"

    def test_text_snippet_field(self):
        r = self._make(text_snippet="hello world")
        assert r.text_snippet == "hello world"

    def test_scores_field(self):
        r = self._make(scores={"a": 0.9})
        assert r.scores == {"a": 0.9}

    def test_top_category_field(self):
        r = self._make(top_category="tech")
        assert r.top_category == "tech"

    def test_confidence_field(self):
        r = self._make(confidence=0.85)
        assert r.confidence == pytest.approx(0.85)

    def test_is_confident_above_default_threshold(self):
        r = self._make(confidence=0.6)
        assert r.is_confident() is True

    def test_is_confident_below_default_threshold(self):
        r = self._make(confidence=0.4)
        assert r.is_confident() is False

    def test_is_confident_at_default_threshold(self):
        r = self._make(confidence=0.5)
        assert r.is_confident() is True

    def test_is_confident_custom_threshold_high(self):
        r = self._make(confidence=0.7)
        assert r.is_confident(threshold=0.8) is False

    def test_is_confident_custom_threshold_zero(self):
        r = self._make(confidence=0.01)
        assert r.is_confident(threshold=0.0) is True

    def test_is_confident_returns_bool(self):
        r = self._make(confidence=0.9)
        result = r.is_confident()
        assert isinstance(result, bool)


# ===========================================================================
# 3. ClassifierConfig dataclass
# ===========================================================================

class TestClassifierConfig:
    def test_defaults(self):
        cfg = ClassifierConfig()
        assert cfg.min_confidence == pytest.approx(0.1)
        assert cfg.max_categories == 3
        assert cfg.normalize is True

    def test_custom_values(self):
        cfg = ClassifierConfig(min_confidence=0.2, max_categories=5, normalize=False)
        assert cfg.min_confidence == pytest.approx(0.2)
        assert cfg.max_categories == 5
        assert cfg.normalize is False


# ===========================================================================
# 4. DocumentClassifier — category management
# ===========================================================================

class TestDocumentClassifierCategories:
    def test_add_category(self):
        clf = DocumentClassifier()
        clf.add_category(Category("tech", keywords=["python"]))
        assert len(clf.categories()) == 1

    def test_add_multiple_categories(self):
        clf = DocumentClassifier()
        clf.add_category(Category("tech"))
        clf.add_category(Category("cooking"))
        assert len(clf.categories()) == 2

    def test_add_category_overwrite(self):
        clf = DocumentClassifier()
        clf.add_category(Category("tech", keywords=["python"]))
        clf.add_category(Category("tech", keywords=["java"]))
        cats = clf.categories()
        assert len(cats) == 1
        assert cats[0].keywords == ["java"]

    def test_remove_existing_category_returns_true(self):
        clf = DocumentClassifier()
        clf.add_category(Category("tech"))
        assert clf.remove_category("tech") is True

    def test_remove_existing_category_removes_it(self):
        clf = DocumentClassifier()
        clf.add_category(Category("tech"))
        clf.remove_category("tech")
        assert len(clf.categories()) == 0

    def test_remove_nonexistent_category_returns_false(self):
        clf = DocumentClassifier()
        assert clf.remove_category("ghost") is False

    def test_categories_returns_list(self):
        clf = DocumentClassifier()
        assert isinstance(clf.categories(), list)

    def test_categories_empty_initially(self):
        clf = DocumentClassifier()
        assert clf.categories() == []

    def test_categories_contains_category_instances(self):
        clf = DocumentClassifier()
        cat = Category("tech", keywords=["python"])
        clf.add_category(cat)
        assert clf.categories()[0] == cat


# ===========================================================================
# 5. DocumentClassifier — classify: keyword scoring
# ===========================================================================

class TestDocumentClassifierScoring:
    def test_classify_returns_classification_result(self):
        clf = make_classifier()
        result = clf.classify("doc1", "python code")
        assert isinstance(result, ClassificationResult)

    def test_classify_doc_id_preserved(self):
        clf = make_classifier()
        result = clf.classify("my-doc-42", "python code")
        assert result.doc_id == "my-doc-42"

    def test_classify_text_snippet_is_prefix(self):
        clf = make_classifier()
        text = "python " * 60  # > 200 chars
        result = clf.classify("d", text)
        assert result.text_snippet == text[:200]

    def test_classify_text_snippet_short_text(self):
        clf = make_classifier()
        text = "python code"
        result = clf.classify("d", text)
        assert result.text_snippet == text

    def test_classify_top_category_is_string(self):
        clf = make_classifier()
        result = clf.classify("d", "python code algorithm")
        assert isinstance(result.top_category, str)

    def test_classify_confidence_is_float(self):
        clf = make_classifier()
        result = clf.classify("d", "python code algorithm")
        assert isinstance(result.confidence, float)

    def test_classify_correct_top_category_tech(self):
        clf = make_classifier()
        result = clf.classify("d", "python code algorithm function function")
        assert result.top_category == "tech"

    def test_classify_correct_top_category_cooking(self):
        clf = make_classifier()
        result = clf.classify("d", "recipe bake oven flour butter butter")
        assert result.top_category == "cooking"

    def test_classify_correct_top_category_sports(self):
        clf = make_classifier()
        result = clf.classify("d", "football players goal match team")
        assert result.top_category == "sports"

    def test_classify_case_insensitive(self):
        clf = make_classifier()
        r_lower = clf.classify("d", "python code")
        r_upper = clf.classify("d", "PYTHON CODE")
        assert r_lower.top_category == r_upper.top_category

    def test_classify_raw_score_formula(self):
        """Score = keyword_occurrences / (word_count + 1)."""
        clf = DocumentClassifier(ClassifierConfig(normalize=False))
        clf.add_category(Category("a", keywords=["hello"]))
        # text = "hello hello hello" → 3 words, 3 occurrences of "hello"
        result = clf.classify("d", "hello hello hello")
        expected = 3 / (3 + 1)
        assert result.confidence == pytest.approx(expected)

    def test_classify_no_keywords_zero_score(self):
        """When text has no keyword matches the raw score is 0."""
        clf = DocumentClassifier(ClassifierConfig(normalize=False))
        clf.add_category(Category("a", keywords=["xyz"]))
        result = clf.classify("d", "nothing relevant here")
        assert result.confidence == pytest.approx(0.0)

    def test_classify_scores_sum_to_one_when_normalized(self):
        clf = make_classifier(normalize=True)
        result = clf.classify("d", "python code algorithm recipe bake football goal")
        # Extend to cover all 3 categories in scores by setting max_categories=3
        total = sum(result.scores.values())
        assert total == pytest.approx(1.0, abs=1e-9)

    def test_classify_scores_not_normalized_when_disabled(self):
        clf = make_classifier(normalize=False)
        result = clf.classify("d", "python code algorithm")
        # sum of raw scores should NOT equal 1 (unless by coincidence)
        # just check confidence equals the raw fraction
        words = "python code algorithm".split()
        expected_raw = 3 / (len(words) + 1)  # python, code, algorithm each once
        assert result.confidence == pytest.approx(expected_raw)

    def test_classify_scores_dict_keys_are_category_names(self):
        clf = make_classifier()
        result = clf.classify("d", "python code football goal")
        for key in result.scores:
            assert isinstance(key, str)

    def test_classify_scores_dict_values_are_floats(self):
        clf = make_classifier()
        result = clf.classify("d", "python code football goal")
        for v in result.scores.values():
            assert isinstance(v, float)

    def test_classify_confidence_equals_top_score(self):
        clf = make_classifier()
        result = clf.classify("d", "python code algorithm function")
        assert result.confidence == pytest.approx(result.scores[result.top_category])

    def test_classify_scores_limited_to_max_categories(self):
        clf = DocumentClassifier(ClassifierConfig(max_categories=2))
        clf.add_category(Category("a", keywords=["alpha"]))
        clf.add_category(Category("b", keywords=["beta"]))
        clf.add_category(Category("c", keywords=["gamma"]))
        clf.add_category(Category("d", keywords=["delta"]))
        result = clf.classify("doc", "alpha beta gamma delta")
        assert len(result.scores) <= 2

    def test_classify_scores_contains_top_category(self):
        clf = make_classifier()
        result = clf.classify("d", "python code algorithm function")
        assert result.top_category in result.scores

    def test_classify_scores_sorted_descending(self):
        clf = make_classifier()
        result = clf.classify("d", "python code algorithm function")
        values = list(result.scores.values())
        assert values == sorted(values, reverse=True)


# ===========================================================================
# 6. DocumentClassifier — edge cases
# ===========================================================================

class TestDocumentClassifierEdgeCases:
    def test_no_categories_empty_top(self):
        clf = DocumentClassifier()
        result = clf.classify("d", "some text here")
        assert result.top_category == ""
        assert result.confidence == pytest.approx(0.0)
        assert result.scores == {}

    def test_no_keyword_matches_all_zeros_normalized(self):
        clf = DocumentClassifier(ClassifierConfig(normalize=True))
        clf.add_category(Category("a", keywords=["xyz"]))
        clf.add_category(Category("b", keywords=["abc"]))
        result = clf.classify("d", "nothing matches at all")
        # all raw scores 0 → sum 0 → no normalization → all still 0
        assert result.confidence == pytest.approx(0.0)

    def test_no_keyword_matches_top_category_still_set(self):
        clf = DocumentClassifier(ClassifierConfig(normalize=True))
        clf.add_category(Category("a", keywords=["xyz"]))
        clf.add_category(Category("b", keywords=["abc"]))
        result = clf.classify("d", "nothing matches at all")
        # top_category is some valid category name (tied at 0)
        assert result.top_category in ("a", "b")

    def test_single_category(self):
        clf = DocumentClassifier()
        clf.add_category(Category("only", keywords=["hello"]))
        result = clf.classify("d", "hello world")
        assert result.top_category == "only"
        assert len(result.scores) == 1

    def test_single_category_normalized_confidence_one(self):
        clf = DocumentClassifier(ClassifierConfig(normalize=True))
        clf.add_category(Category("only", keywords=["hello"]))
        result = clf.classify("d", "hello world")
        # single non-zero category → normalized to 1.0
        assert result.confidence == pytest.approx(1.0)

    def test_empty_text(self):
        clf = make_classifier()
        result = clf.classify("d", "")
        assert isinstance(result, ClassificationResult)
        assert result.confidence == pytest.approx(0.0)

    def test_empty_keywords_in_category(self):
        clf = DocumentClassifier()
        clf.add_category(Category("empty", keywords=[]))
        result = clf.classify("d", "something")
        assert result.confidence == pytest.approx(0.0)

    def test_max_categories_one(self):
        clf = DocumentClassifier(ClassifierConfig(max_categories=1))
        clf.add_category(Category("a", keywords=["alpha"]))
        clf.add_category(Category("b", keywords=["beta"]))
        result = clf.classify("d", "alpha beta")
        assert len(result.scores) == 1


# ===========================================================================
# 7. DocumentClassifier — classify_batch
# ===========================================================================

class TestClassifyBatch:
    def test_classify_batch_returns_list(self):
        clf = make_classifier()
        results = clf.classify_batch({"d1": "python code", "d2": "recipe bake"})
        assert isinstance(results, list)

    def test_classify_batch_length_matches_input(self):
        clf = make_classifier()
        docs = {"d1": "python code", "d2": "recipe bake", "d3": "football goal"}
        results = clf.classify_batch(docs)
        assert len(results) == 3

    def test_classify_batch_doc_ids_preserved(self):
        clf = make_classifier()
        docs = {"alpha": "python code", "beta": "recipe bake"}
        results = clf.classify_batch(docs)
        ids = {r.doc_id for r in results}
        assert ids == {"alpha", "beta"}

    def test_classify_batch_empty_dict(self):
        clf = make_classifier()
        results = clf.classify_batch({})
        assert results == []

    def test_classify_batch_results_are_classification_results(self):
        clf = make_classifier()
        results = clf.classify_batch({"d1": "python code"})
        assert all(isinstance(r, ClassificationResult) for r in results)

    def test_classify_batch_each_result_correct(self):
        clf = make_classifier()
        docs = {
            "tech_doc": "python code algorithm function",
            "food_doc": "recipe bake oven flour butter",
        }
        results = {r.doc_id: r for r in clf.classify_batch(docs)}
        assert results["tech_doc"].top_category == "tech"
        assert results["food_doc"].top_category == "cooking"


# ===========================================================================
# 8. CategoryHierarchy — build / children / ancestors
# ===========================================================================

class TestCategoryHierarchyNavigation:
    def _make_hierarchy(self):
        clf = DocumentClassifier()
        hierarchy = CategoryHierarchy(clf)
        cats = [
            Category("root", keywords=["root"]),
            Category("tech", keywords=["python", "code"], parent="root"),
            Category("cooking", keywords=["recipe", "bake"], parent="root"),
            Category("python", keywords=["python", "pip"], parent="tech"),
            Category("java", keywords=["java", "jvm"], parent="tech"),
        ]
        hierarchy.build(cats)
        return hierarchy

    def test_build_registers_categories_in_classifier(self):
        hierarchy = self._make_hierarchy()
        names = {c.name for c in hierarchy._classifier.categories()}
        assert {"root", "tech", "cooking", "python", "java"} == names

    def test_children_of_root(self):
        hierarchy = self._make_hierarchy()
        children = hierarchy.children("root")
        assert set(children) == {"tech", "cooking"}

    def test_children_of_tech(self):
        hierarchy = self._make_hierarchy()
        children = hierarchy.children("tech")
        assert set(children) == {"python", "java"}

    def test_children_of_leaf_is_empty(self):
        hierarchy = self._make_hierarchy()
        assert hierarchy.children("python") == []

    def test_children_of_unknown_is_empty(self):
        hierarchy = self._make_hierarchy()
        assert hierarchy.children("ghost") == []

    def test_ancestors_of_python(self):
        hierarchy = self._make_hierarchy()
        ancs = hierarchy.ancestors("python")
        assert ancs == ["tech", "root"]

    def test_ancestors_of_tech(self):
        hierarchy = self._make_hierarchy()
        ancs = hierarchy.ancestors("tech")
        assert ancs == ["root"]

    def test_ancestors_of_root_is_empty(self):
        hierarchy = self._make_hierarchy()
        assert hierarchy.ancestors("root") == []

    def test_ancestors_of_unknown_is_empty(self):
        hierarchy = self._make_hierarchy()
        assert hierarchy.ancestors("ghost") == []

    def test_ancestors_order_bottom_up(self):
        hierarchy = self._make_hierarchy()
        ancs = hierarchy.ancestors("python")
        # immediate parent first
        assert ancs[0] == "tech"
        assert ancs[-1] == "root"


# ===========================================================================
# 9. CategoryHierarchy — classify_hierarchical
# ===========================================================================

class TestCategoryHierarchyClassify:
    def _make_hierarchy(self):
        clf = DocumentClassifier(ClassifierConfig(normalize=True, max_categories=10))
        hierarchy = CategoryHierarchy(clf)
        cats = [
            Category("root", keywords=["knowledge"]),
            Category("tech", keywords=["python", "code", "algorithm"], parent="root"),
            Category("cooking", keywords=["recipe", "bake", "oven"], parent="root"),
            Category("python", keywords=["python", "pip", "virtualenv"], parent="tech"),
        ]
        hierarchy.build(cats)
        return hierarchy

    def test_returns_dict(self):
        hierarchy = self._make_hierarchy()
        result = hierarchy.classify_hierarchical("d", "python code algorithm")
        assert isinstance(result, dict)

    def test_matched_category_present(self):
        hierarchy = self._make_hierarchy()
        result = hierarchy.classify_hierarchical("d", "python code algorithm pip")
        # "python" and "tech" should both be present
        assert "python" in result or "tech" in result

    def test_ancestor_score_propagated(self):
        hierarchy = self._make_hierarchy()
        result = hierarchy.classify_hierarchical("d", "python pip virtualenv")
        # "python" matches; its ancestor "tech" should receive propagated score
        assert "tech" in result
        assert result["tech"] > 0.0

    def test_no_match_no_entry(self):
        hierarchy = self._make_hierarchy()
        result = hierarchy.classify_hierarchical("d", "nothing matches")
        # all zero scores → nothing returned (or zeros filtered)
        assert all(v > 0.0 for v in result.values())

    def test_scores_are_floats(self):
        hierarchy = self._make_hierarchy()
        result = hierarchy.classify_hierarchical("d", "python code algorithm")
        for v in result.values():
            assert isinstance(v, float)

    def test_all_zero_when_empty_classifier(self):
        clf = DocumentClassifier()
        hierarchy = CategoryHierarchy(clf)
        hierarchy.build([])
        result = hierarchy.classify_hierarchical("d", "python code")
        assert result == {}

    def test_root_gets_propagated_from_children(self):
        """Root has no keywords itself; it should still appear if children match."""
        clf = DocumentClassifier(ClassifierConfig(normalize=True, max_categories=10))
        h = CategoryHierarchy(clf)
        h.build([
            Category("root"),          # no keywords
            Category("child", keywords=["hello"], parent="root"),
        ])
        result = h.classify_hierarchical("d", "hello world")
        assert "root" in result
        assert result["root"] > 0.0
