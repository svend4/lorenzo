"""Tests for docstoolkit.doc_classification (E347)."""

from __future__ import annotations

import threading
from dataclasses import fields

import pytest

from docstoolkit.doc_classification import (
    Category,
    Classification,
    ClassificationStats,
    DocClassification,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_classifier() -> DocClassification:
    return DocClassification()


def make_classifier_with_categories() -> DocClassification:
    dc = make_classifier()
    dc.add_category(Category("tech", "Technology", "Tech stuff", "#ff0000"))
    dc.add_category(Category("biz", "Business", "Biz", "#00ff00"))
    dc.add_category(Category("misc", "Misc", "Other", "#0000ff"))
    return dc


# ---------------------------------------------------------------------------
# TestCategoryDataclass (5)
# ---------------------------------------------------------------------------


class TestCategoryDataclass:
    def test_category_id_stored(self):
        c = Category("tech", "Technology")
        assert c.category_id == "tech"

    def test_name_stored(self):
        c = Category("tech", "Technology")
        assert c.name == "Technology"

    def test_description_default_empty(self):
        c = Category("tech", "Technology")
        assert c.description == ""

    def test_color_default(self):
        c = Category("tech", "Technology")
        assert c.color == "#cccccc"

    def test_all_fields_present(self):
        names = {f.name for f in fields(Category)}
        assert names == {"category_id", "name", "description", "color"}


# ---------------------------------------------------------------------------
# TestClassificationDataclass (5)
# ---------------------------------------------------------------------------


class TestClassificationDataclass:
    def test_doc_id_stored(self):
        c = Classification(doc_id="d1", category_id="tech")
        assert c.doc_id == "d1"

    def test_category_id_stored(self):
        c = Classification(doc_id="d1", category_id="tech")
        assert c.category_id == "tech"

    def test_confidence_default(self):
        c = Classification(doc_id="d1", category_id="tech")
        assert c.confidence == 1.0

    def test_classified_at_default(self):
        c = Classification(doc_id="d1", category_id="tech")
        assert c.classified_at == 0.0

    def test_classified_by_default(self):
        c = Classification(doc_id="d1", category_id="tech")
        assert c.classified_by == ""


# ---------------------------------------------------------------------------
# TestClassificationStatsDataclass (5)
# ---------------------------------------------------------------------------


class TestClassificationStatsDataclass:
    def test_total_categories_stored(self):
        s = ClassificationStats(2, 3, 1, 0.9)
        assert s.total_categories == 2

    def test_total_classifications_stored(self):
        s = ClassificationStats(2, 3, 1, 0.9)
        assert s.total_classifications == 3

    def test_unique_docs_stored(self):
        s = ClassificationStats(2, 3, 1, 0.9)
        assert s.unique_docs == 1

    def test_avg_confidence_stored(self):
        s = ClassificationStats(2, 3, 1, 0.9)
        assert s.avg_confidence == 0.9

    def test_category_counts_default_empty(self):
        s = ClassificationStats(0, 0, 0, 0.0)
        assert s.category_counts == {}


# ---------------------------------------------------------------------------
# TestConstruction (3)
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_starts_with_no_categories(self):
        dc = make_classifier()
        assert dc.list_categories() == []

    def test_starts_with_no_classifications(self):
        dc = make_classifier()
        s = dc.stats()
        assert s.total_classifications == 0

    def test_stats_zero_avg_when_empty(self):
        dc = make_classifier()
        assert dc.stats().avg_confidence == 0.0


# ---------------------------------------------------------------------------
# TestAddCategory (3)
# ---------------------------------------------------------------------------


class TestAddCategory:
    def test_add_new_category(self):
        dc = make_classifier()
        dc.add_category(Category("tech", "Tech"))
        assert dc.get_category("tech") is not None

    def test_replace_existing_category(self):
        dc = make_classifier()
        dc.add_category(Category("tech", "Old"))
        dc.add_category(Category("tech", "New"))
        cat = dc.get_category("tech")
        assert cat is not None and cat.name == "New"

    def test_add_increases_count(self):
        dc = make_classifier()
        dc.add_category(Category("a", "A"))
        dc.add_category(Category("b", "B"))
        assert dc.stats().total_categories == 2


# ---------------------------------------------------------------------------
# TestRemoveCategory (4)
# ---------------------------------------------------------------------------


class TestRemoveCategory:
    def test_remove_existing_returns_true(self):
        dc = make_classifier_with_categories()
        assert dc.remove_category("tech") is True

    def test_remove_missing_returns_false(self):
        dc = make_classifier()
        assert dc.remove_category("nope") is False

    def test_remove_cleans_up_classifications(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech")
        dc.classify("d2", "tech")
        dc.remove_category("tech")
        assert dc.get_classification("d1", "tech") is None
        assert dc.get_classification("d2", "tech") is None

    def test_remove_does_not_touch_other_categories(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech")
        dc.classify("d1", "biz")
        dc.remove_category("tech")
        assert dc.get_classification("d1", "biz") is not None


# ---------------------------------------------------------------------------
# TestGetCategory (2)
# ---------------------------------------------------------------------------


class TestGetCategory:
    def test_get_found(self):
        dc = make_classifier_with_categories()
        cat = dc.get_category("tech")
        assert cat is not None and cat.category_id == "tech"

    def test_get_not_found(self):
        dc = make_classifier_with_categories()
        assert dc.get_category("nope") is None


# ---------------------------------------------------------------------------
# TestListCategories (3)
# ---------------------------------------------------------------------------


class TestListCategories:
    def test_list_empty(self):
        dc = make_classifier()
        assert dc.list_categories() == []

    def test_list_sorted_by_name(self):
        dc = make_classifier()
        dc.add_category(Category("z", "Zeta"))
        dc.add_category(Category("a", "Alpha"))
        dc.add_category(Category("m", "Mu"))
        names = [c.name for c in dc.list_categories()]
        assert names == ["Alpha", "Mu", "Zeta"]

    def test_list_returns_all(self):
        dc = make_classifier_with_categories()
        assert len(dc.list_categories()) == 3


# ---------------------------------------------------------------------------
# TestClassify (5)
# ---------------------------------------------------------------------------


class TestClassify:
    def test_classify_returns_none_for_undefined_category(self):
        dc = make_classifier()
        assert dc.classify("d1", "nope") is None

    def test_classify_creates_record(self):
        dc = make_classifier_with_categories()
        rec = dc.classify("d1", "tech", confidence=0.8)
        assert rec is not None
        assert rec.doc_id == "d1"
        assert rec.category_id == "tech"
        assert rec.confidence == 0.8

    def test_classify_replaces_existing(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech", confidence=0.5)
        dc.classify("d1", "tech", confidence=0.9)
        rec = dc.get_classification("d1", "tech")
        assert rec is not None and rec.confidence == 0.9

    def test_classify_uses_provided_now(self):
        dc = make_classifier_with_categories()
        rec = dc.classify("d1", "tech", now=1234.5)
        assert rec is not None and rec.classified_at == 1234.5

    def test_classify_stores_classified_by(self):
        dc = make_classifier_with_categories()
        rec = dc.classify("d1", "tech", classified_by="alice")
        assert rec is not None and rec.classified_by == "alice"


# ---------------------------------------------------------------------------
# TestUnclassify (3)
# ---------------------------------------------------------------------------


class TestUnclassify:
    def test_unclassify_existing_returns_true(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech")
        assert dc.unclassify("d1", "tech") is True

    def test_unclassify_missing_returns_false(self):
        dc = make_classifier_with_categories()
        assert dc.unclassify("d1", "tech") is False

    def test_unclassify_removes_record(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech")
        dc.unclassify("d1", "tech")
        assert dc.get_classification("d1", "tech") is None


# ---------------------------------------------------------------------------
# TestGetClassification (2)
# ---------------------------------------------------------------------------


class TestGetClassification:
    def test_get_found(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech", confidence=0.7)
        rec = dc.get_classification("d1", "tech")
        assert rec is not None and rec.confidence == 0.7

    def test_get_not_found(self):
        dc = make_classifier_with_categories()
        assert dc.get_classification("d1", "tech") is None


# ---------------------------------------------------------------------------
# TestCategoriesForDoc (3)
# ---------------------------------------------------------------------------


class TestCategoriesForDoc:
    def test_empty_for_unknown_doc(self):
        dc = make_classifier_with_categories()
        assert dc.categories_for_doc("ghost") == []

    def test_returns_all_categories(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech")
        dc.classify("d1", "biz")
        result = dc.categories_for_doc("d1")
        assert len(result) == 2

    def test_sorted_by_category_id(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech")
        dc.classify("d1", "biz")
        dc.classify("d1", "misc")
        cat_ids = [c.category_id for c in dc.categories_for_doc("d1")]
        assert cat_ids == ["biz", "misc", "tech"]


# ---------------------------------------------------------------------------
# TestDocsInCategory (4)
# ---------------------------------------------------------------------------


class TestDocsInCategory:
    def test_empty_for_unknown_category(self):
        dc = make_classifier_with_categories()
        assert dc.docs_in_category("nope") == []

    def test_returns_all_docs(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech")
        dc.classify("d2", "tech")
        assert dc.docs_in_category("tech") == ["d1", "d2"]

    def test_min_confidence_filters(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech", confidence=0.3)
        dc.classify("d2", "tech", confidence=0.9)
        assert dc.docs_in_category("tech", min_confidence=0.5) == ["d2"]

    def test_sorted_alphabetically(self):
        dc = make_classifier_with_categories()
        dc.classify("zeta", "tech")
        dc.classify("alpha", "tech")
        dc.classify("mu", "tech")
        assert dc.docs_in_category("tech") == ["alpha", "mu", "zeta"]


# ---------------------------------------------------------------------------
# TestClearDoc (3)
# ---------------------------------------------------------------------------


class TestClearDoc:
    def test_clear_returns_zero_for_unknown(self):
        dc = make_classifier_with_categories()
        assert dc.clear_doc("ghost") == 0

    def test_clear_returns_count(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech")
        dc.classify("d1", "biz")
        dc.classify("d1", "misc")
        assert dc.clear_doc("d1") == 3

    def test_clear_removes_all_records(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech")
        dc.classify("d1", "biz")
        dc.clear_doc("d1")
        assert dc.categories_for_doc("d1") == []
        assert dc.get_classification("d1", "tech") is None


# ---------------------------------------------------------------------------
# TestTopCategories (4)
# ---------------------------------------------------------------------------


class TestTopCategories:
    def test_empty_when_no_categories(self):
        dc = make_classifier()
        assert dc.top_categories() == []

    def test_sorted_by_count_desc(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech")
        dc.classify("d2", "tech")
        dc.classify("d3", "tech")
        dc.classify("d1", "biz")
        result = dc.top_categories()
        assert result[0] == ("tech", 3)
        assert result[1] == ("biz", 1)

    def test_ties_broken_by_category_id(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech")
        dc.classify("d1", "biz")
        result = dc.top_categories()
        # tech and biz both have 1; misc has 0
        # Order among ties: biz before tech (alpha asc)
        first_two = [item[0] for item in result[:2]]
        assert first_two == ["biz", "tech"]

    def test_limit_applies(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech")
        dc.classify("d1", "biz")
        dc.classify("d1", "misc")
        result = dc.top_categories(limit=2)
        assert len(result) == 2


# ---------------------------------------------------------------------------
# TestStats (5)
# ---------------------------------------------------------------------------


class TestStats:
    def test_total_categories(self):
        dc = make_classifier_with_categories()
        assert dc.stats().total_categories == 3

    def test_total_classifications(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech")
        dc.classify("d2", "biz")
        assert dc.stats().total_classifications == 2

    def test_unique_docs(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech")
        dc.classify("d1", "biz")
        dc.classify("d2", "tech")
        assert dc.stats().unique_docs == 2

    def test_avg_confidence(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech", confidence=0.4)
        dc.classify("d2", "biz", confidence=0.8)
        assert dc.stats().avg_confidence == pytest.approx(0.6)

    def test_category_counts(self):
        dc = make_classifier_with_categories()
        dc.classify("d1", "tech")
        dc.classify("d2", "tech")
        dc.classify("d1", "biz")
        counts = dc.stats().category_counts
        assert counts["tech"] == 2
        assert counts["biz"] == 1
        assert counts["misc"] == 0


# ---------------------------------------------------------------------------
# TestThreadSafety (2)
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_classify(self):
        dc = make_classifier_with_categories()
        n_threads = 10
        per_thread = 50

        def worker(start: int) -> None:
            for i in range(per_thread):
                doc_id = f"d{start * per_thread + i}"
                dc.classify(doc_id, "tech", confidence=0.5)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = dc.stats()
        assert s.total_classifications == n_threads * per_thread
        assert s.unique_docs == n_threads * per_thread

    def test_concurrent_mixed_operations(self):
        dc = make_classifier_with_categories()

        def classifier_w() -> None:
            for i in range(100):
                dc.classify(f"d{i}", "tech")

        def unclassifier() -> None:
            for i in range(100):
                dc.unclassify(f"d{i}", "tech")

        def reader() -> None:
            for _ in range(100):
                dc.stats()
                dc.list_categories()

        threads = [
            threading.Thread(target=classifier_w),
            threading.Thread(target=unclassifier),
            threading.Thread(target=reader),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # No exception means thread safety held; state is consistent.
        s = dc.stats()
        assert s.total_categories == 3
        assert 0 <= s.total_classifications <= 100
