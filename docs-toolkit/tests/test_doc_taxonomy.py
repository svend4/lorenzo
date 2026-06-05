"""Tests for docstoolkit.doc_taxonomy."""

from __future__ import annotations

import pytest

from docstoolkit.doc_taxonomy import (
    Classification,
    ClassificationRule,
    DocTaxonomy,
    TaxonomyTerm,
)


# --------------------------------------------------------------------------- #
# Dataclasses                                                                 #
# --------------------------------------------------------------------------- #
class TestTaxonomyTerm:
    def test_required_fields(self):
        t = TaxonomyTerm(term_id="t1", name="AI")
        assert t.term_id == "t1"
        assert t.name == "AI"

    def test_defaults(self):
        t = TaxonomyTerm(term_id="t1", name="AI")
        assert t.parent_id is None
        assert t.taxonomy == "default"
        assert t.synonyms == []
        assert t.metadata == {}

    def test_custom_taxonomy(self):
        t = TaxonomyTerm(term_id="t1", name="AI", taxonomy="topics")
        assert t.taxonomy == "topics"

    def test_synonyms_and_metadata(self):
        t = TaxonomyTerm(
            term_id="t1",
            name="AI",
            synonyms=["artificial intelligence"],
            metadata={"created": 1},
        )
        assert "artificial intelligence" in t.synonyms
        assert t.metadata["created"] == 1


class TestClassification:
    def test_basic(self):
        c = Classification(doc_id="d1", term_id="t1")
        assert c.doc_id == "d1"
        assert c.term_id == "t1"
        assert c.confidence == 1.0
        assert c.assigned_by is None
        assert c.assigned_at == 0.0

    def test_full(self):
        c = Classification(
            doc_id="d1",
            term_id="t1",
            confidence=0.7,
            assigned_by="rule_1",
            assigned_at=100.0,
        )
        assert c.confidence == 0.7
        assert c.assigned_by == "rule_1"
        assert c.assigned_at == 100.0


class TestClassificationRule:
    def test_basic(self):
        r = ClassificationRule(
            rule_id="r1", name="r", term_id="t1", condition=lambda d: True
        )
        assert r.enabled is True
        assert r.confidence == 1.0

    def test_condition_callable(self):
        r = ClassificationRule(
            rule_id="r1",
            name="r",
            term_id="t1",
            condition=lambda d: d.get("x") == 1,
        )
        assert r.condition({"x": 1}) is True
        assert r.condition({"x": 2}) is False


# --------------------------------------------------------------------------- #
# Terms                                                                       #
# --------------------------------------------------------------------------- #
class TestAddTerm:
    def test_returns_term(self):
        t = DocTaxonomy().add_term("AI")
        assert isinstance(t, TaxonomyTerm)
        assert t.name == "AI"

    def test_assigns_id(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B")
        assert a.term_id != b.term_id

    def test_with_parent(self):
        tx = DocTaxonomy()
        parent = tx.add_term("AI")
        child = tx.add_term("ML", parent_id=parent.term_id)
        assert child.parent_id == parent.term_id

    def test_missing_parent_raises(self):
        tx = DocTaxonomy()
        with pytest.raises(ValueError):
            tx.add_term("ML", parent_id="nonexistent")

    def test_with_synonyms(self):
        tx = DocTaxonomy()
        t = tx.add_term("AI", synonyms=["artificial intelligence"])
        assert "artificial intelligence" in t.synonyms

    def test_with_metadata(self):
        tx = DocTaxonomy()
        t = tx.add_term("AI", metadata={"weight": 5})
        assert t.metadata["weight"] == 5

    def test_with_custom_taxonomy(self):
        tx = DocTaxonomy()
        t = tx.add_term("Tech", taxonomy="topics")
        assert t.taxonomy == "topics"

    def test_parent_taxonomy_mismatch(self):
        tx = DocTaxonomy()
        parent = tx.add_term("X", taxonomy="a")
        with pytest.raises(ValueError):
            tx.add_term("Y", parent_id=parent.term_id, taxonomy="b")


class TestRemoveTerm:
    def test_returns_true_on_success(self):
        tx = DocTaxonomy()
        t = tx.add_term("X")
        assert tx.remove_term(t.term_id) is True

    def test_returns_false_on_missing(self):
        tx = DocTaxonomy()
        assert tx.remove_term("missing") is False

    def test_term_gone(self):
        tx = DocTaxonomy()
        t = tx.add_term("X")
        tx.remove_term(t.term_id)
        assert tx.get_term(t.term_id) is None

    def test_cascades_children(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B", parent_id=a.term_id)
        c = tx.add_term("C", parent_id=b.term_id)
        tx.remove_term(a.term_id)
        assert tx.get_term(b.term_id) is None
        assert tx.get_term(c.term_id) is None

    def test_cascades_classifications(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B", parent_id=a.term_id)
        tx.classify("doc1", a.term_id)
        tx.classify("doc2", b.term_id)
        tx.remove_term(a.term_id)
        assert tx.classifications_for_doc("doc1") == []
        assert tx.classifications_for_doc("doc2") == []


class TestMoveTerm:
    def test_basic_move(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B")
        c = tx.add_term("C", parent_id=a.term_id)
        assert tx.move_term(c.term_id, b.term_id) is True
        assert tx.get_term(c.term_id).parent_id == b.term_id

    def test_move_to_root(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B", parent_id=a.term_id)
        assert tx.move_term(b.term_id, None) is True
        assert tx.get_term(b.term_id).parent_id is None

    def test_missing_term(self):
        tx = DocTaxonomy()
        assert tx.move_term("missing", None) is False

    def test_missing_parent(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        assert tx.move_term(a.term_id, "nonexistent") is False

    def test_self_parent_rejected(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        assert tx.move_term(a.term_id, a.term_id) is False

    def test_cycle_detected(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B", parent_id=a.term_id)
        c = tx.add_term("C", parent_id=b.term_id)
        # cannot move A under C (descendant)
        assert tx.move_term(a.term_id, c.term_id) is False
        assert tx.get_term(a.term_id).parent_id is None

    def test_cross_taxonomy_rejected(self):
        tx = DocTaxonomy()
        a = tx.add_term("A", taxonomy="t1")
        b = tx.add_term("B", taxonomy="t2")
        assert tx.move_term(a.term_id, b.term_id) is False


class TestGetTerm:
    def test_existing(self):
        tx = DocTaxonomy()
        t = tx.add_term("A")
        assert tx.get_term(t.term_id) is t

    def test_missing(self):
        tx = DocTaxonomy()
        assert tx.get_term("missing") is None


class TestFindByName:
    def test_found(self):
        tx = DocTaxonomy()
        t = tx.add_term("AI")
        assert tx.find_by_name("AI") is t

    def test_not_found(self):
        tx = DocTaxonomy()
        assert tx.find_by_name("missing") is None

    def test_with_taxonomy_filter(self):
        tx = DocTaxonomy()
        a = tx.add_term("X", taxonomy="t1")
        b = tx.add_term("X", taxonomy="t2")
        found = tx.find_by_name("X", taxonomy="t2")
        assert found is b
        assert tx.find_by_name("X", taxonomy="t1") is a

    def test_taxonomy_mismatch_returns_none(self):
        tx = DocTaxonomy()
        tx.add_term("X", taxonomy="t1")
        assert tx.find_by_name("X", taxonomy="t2") is None


class TestFindBySynonym:
    def test_found(self):
        tx = DocTaxonomy()
        t = tx.add_term("AI", synonyms=["ai", "artificial intelligence"])
        assert tx.find_by_synonym("ai") is t
        assert tx.find_by_synonym("artificial intelligence") is t

    def test_not_found(self):
        tx = DocTaxonomy()
        tx.add_term("AI", synonyms=["ai"])
        assert tx.find_by_synonym("missing") is None


class TestAddRemoveSynonym:
    def test_add(self):
        tx = DocTaxonomy()
        t = tx.add_term("AI")
        assert tx.add_synonym(t.term_id, "ai") is True
        assert "ai" in tx.get_term(t.term_id).synonyms

    def test_add_duplicate_returns_false(self):
        tx = DocTaxonomy()
        t = tx.add_term("AI", synonyms=["ai"])
        assert tx.add_synonym(t.term_id, "ai") is False

    def test_add_missing_term(self):
        tx = DocTaxonomy()
        assert tx.add_synonym("missing", "x") is False

    def test_remove(self):
        tx = DocTaxonomy()
        t = tx.add_term("AI", synonyms=["ai"])
        assert tx.remove_synonym(t.term_id, "ai") is True
        assert "ai" not in tx.get_term(t.term_id).synonyms

    def test_remove_missing_synonym(self):
        tx = DocTaxonomy()
        t = tx.add_term("AI")
        assert tx.remove_synonym(t.term_id, "missing") is False

    def test_remove_missing_term(self):
        tx = DocTaxonomy()
        assert tx.remove_synonym("missing", "x") is False


class TestChildren:
    def test_empty(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        assert tx.children(a.term_id) == []

    def test_returns_direct_only(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B", parent_id=a.term_id)
        tx.add_term("C", parent_id=b.term_id)
        kids = tx.children(a.term_id)
        assert len(kids) == 1
        assert kids[0].term_id == b.term_id

    def test_missing_term(self):
        tx = DocTaxonomy()
        assert tx.children("missing") == []


class TestDescendants:
    def test_empty(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        assert tx.descendants(a.term_id) == []

    def test_recursive(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B", parent_id=a.term_id)
        c = tx.add_term("C", parent_id=b.term_id)
        d = tx.add_term("D", parent_id=a.term_id)
        ids = {t.term_id for t in tx.descendants(a.term_id)}
        assert ids == {b.term_id, c.term_id, d.term_id}

    def test_missing_term(self):
        tx = DocTaxonomy()
        assert tx.descendants("missing") == []


class TestAncestors:
    def test_root_has_none(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        assert tx.ancestors(a.term_id) == []

    def test_chain(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B", parent_id=a.term_id)
        c = tx.add_term("C", parent_id=b.term_id)
        anc_ids = [t.term_id for t in tx.ancestors(c.term_id)]
        assert anc_ids == [b.term_id, a.term_id]

    def test_missing_term(self):
        tx = DocTaxonomy()
        assert tx.ancestors("missing") == []


class TestRootTerms:
    def test_default(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B")
        tx.add_term("C", parent_id=a.term_id)
        roots = {t.term_id for t in tx.root_terms()}
        assert roots == {a.term_id, b.term_id}

    def test_specific_taxonomy(self):
        tx = DocTaxonomy()
        tx.add_term("A", taxonomy="topics")
        tx.add_term("B", taxonomy="formats")
        assert len(tx.root_terms(taxonomy="topics")) == 1
        assert len(tx.root_terms(taxonomy="formats")) == 1


class TestAllTerms:
    def test_unfiltered(self):
        tx = DocTaxonomy()
        tx.add_term("A")
        tx.add_term("B", taxonomy="topics")
        assert len(tx.all_terms()) == 2

    def test_filtered(self):
        tx = DocTaxonomy()
        tx.add_term("A")
        tx.add_term("B", taxonomy="topics")
        assert len(tx.all_terms(taxonomy="topics")) == 1
        assert len(tx.all_terms(taxonomy="default")) == 1


class TestTaxonomies:
    def test_empty(self):
        tx = DocTaxonomy()
        assert tx.taxonomies() == []

    def test_unique_sorted(self):
        tx = DocTaxonomy()
        tx.add_term("A", taxonomy="b")
        tx.add_term("B", taxonomy="a")
        tx.add_term("C", taxonomy="b")
        assert tx.taxonomies() == ["a", "b"]


# --------------------------------------------------------------------------- #
# Classification                                                              #
# --------------------------------------------------------------------------- #
class TestClassify:
    def test_basic(self):
        tx = DocTaxonomy()
        t = tx.add_term("A")
        c = tx.classify("doc1", t.term_id)
        assert isinstance(c, Classification)
        assert c.doc_id == "doc1"
        assert c.term_id == t.term_id

    def test_missing_term(self):
        tx = DocTaxonomy()
        assert tx.classify("doc1", "missing") is None

    def test_default_assigned_by(self):
        tx = DocTaxonomy()
        t = tx.add_term("A")
        c = tx.classify("doc1", t.term_id)
        assert c.assigned_by == "manual"

    def test_custom_confidence(self):
        tx = DocTaxonomy()
        t = tx.add_term("A")
        c = tx.classify("doc1", t.term_id, confidence=0.5)
        assert c.confidence == 0.5

    def test_assigned_at(self):
        tx = DocTaxonomy()
        t = tx.add_term("A")
        c = tx.classify("doc1", t.term_id, now=123.0)
        assert c.assigned_at == 123.0

    def test_overwrites(self):
        tx = DocTaxonomy()
        t = tx.add_term("A")
        tx.classify("doc1", t.term_id, confidence=0.5)
        tx.classify("doc1", t.term_id, confidence=0.9)
        cs = tx.classifications_for_doc("doc1")
        assert len(cs) == 1
        assert cs[0].confidence == 0.9


class TestUnclassify:
    def test_success(self):
        tx = DocTaxonomy()
        t = tx.add_term("A")
        tx.classify("doc1", t.term_id)
        assert tx.unclassify("doc1", t.term_id) is True
        assert tx.classifications_for_doc("doc1") == []

    def test_missing(self):
        tx = DocTaxonomy()
        assert tx.unclassify("doc1", "missing") is False


class TestClassificationsForDoc:
    def test_empty(self):
        tx = DocTaxonomy()
        assert tx.classifications_for_doc("nobody") == []

    def test_multiple_terms(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B")
        tx.classify("doc1", a.term_id)
        tx.classify("doc1", b.term_id)
        tx.classify("doc2", a.term_id)
        cs = tx.classifications_for_doc("doc1")
        assert len(cs) == 2


class TestDocsForTerm:
    def test_empty(self):
        tx = DocTaxonomy()
        t = tx.add_term("A")
        assert tx.docs_for_term(t.term_id) == []

    def test_returns_docs(self):
        tx = DocTaxonomy()
        t = tx.add_term("A")
        tx.classify("doc1", t.term_id)
        tx.classify("doc2", t.term_id)
        assert set(tx.docs_for_term(t.term_id)) == {"doc1", "doc2"}

    def test_missing_term(self):
        tx = DocTaxonomy()
        assert tx.docs_for_term("missing") == []


class TestDocsForTermWithDescendants:
    def test_includes_descendants(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B", parent_id=a.term_id)
        c = tx.add_term("C", parent_id=b.term_id)
        tx.classify("doc1", a.term_id)
        tx.classify("doc2", b.term_id)
        tx.classify("doc3", c.term_id)
        docs = tx.docs_for_term(a.term_id, include_descendants=True)
        assert set(docs) == {"doc1", "doc2", "doc3"}

    def test_excludes_descendants_by_default(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B", parent_id=a.term_id)
        tx.classify("doc1", a.term_id)
        tx.classify("doc2", b.term_id)
        assert tx.docs_for_term(a.term_id) == ["doc1"]

    def test_dedupes(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B", parent_id=a.term_id)
        tx.classify("doc1", a.term_id)
        tx.classify("doc1", b.term_id)
        docs = tx.docs_for_term(a.term_id, include_descendants=True)
        assert docs == ["doc1"]


# --------------------------------------------------------------------------- #
# Rules                                                                       #
# --------------------------------------------------------------------------- #
class TestAddRule:
    def test_returns_rule(self):
        tx = DocTaxonomy()
        t = tx.add_term("A")
        r = tx.add_rule("r1", t.term_id, lambda d: True)
        assert isinstance(r, ClassificationRule)
        assert r.name == "r1"
        assert r.enabled is True

    def test_missing_term(self):
        tx = DocTaxonomy()
        with pytest.raises(ValueError):
            tx.add_rule("r1", "missing", lambda d: True)

    def test_unique_ids(self):
        tx = DocTaxonomy()
        t = tx.add_term("A")
        r1 = tx.add_rule("r1", t.term_id, lambda d: True)
        r2 = tx.add_rule("r2", t.term_id, lambda d: True)
        assert r1.rule_id != r2.rule_id

    def test_custom_confidence(self):
        tx = DocTaxonomy()
        t = tx.add_term("A")
        r = tx.add_rule("r1", t.term_id, lambda d: True, confidence=0.3)
        assert r.confidence == 0.3


class TestRemoveRule:
    def test_success(self):
        tx = DocTaxonomy()
        t = tx.add_term("A")
        r = tx.add_rule("r1", t.term_id, lambda d: True)
        assert tx.remove_rule(r.rule_id) is True

    def test_missing(self):
        tx = DocTaxonomy()
        assert tx.remove_rule("missing") is False


class TestApplyRules:
    def test_condition_true_classifies(self):
        tx = DocTaxonomy()
        t = tx.add_term("python")
        tx.add_rule("py", t.term_id, lambda d: "python" in d.get("tags", []))
        produced = tx.apply_rules("doc1", {"tags": ["python", "ml"]})
        assert len(produced) == 1
        assert produced[0].term_id == t.term_id

    def test_condition_false_no_classification(self):
        tx = DocTaxonomy()
        t = tx.add_term("python")
        tx.add_rule("py", t.term_id, lambda d: "python" in d.get("tags", []))
        produced = tx.apply_rules("doc1", {"tags": ["rust"]})
        assert produced == []
        assert tx.classifications_for_doc("doc1") == []

    def test_assigned_by_rule_id(self):
        tx = DocTaxonomy()
        t = tx.add_term("python")
        rule = tx.add_rule("py", t.term_id, lambda d: True)
        produced = tx.apply_rules("doc1", {})
        assert produced[0].assigned_by == rule.rule_id

    def test_uses_rule_confidence(self):
        tx = DocTaxonomy()
        t = tx.add_term("python")
        tx.add_rule("py", t.term_id, lambda d: True, confidence=0.7)
        produced = tx.apply_rules("doc1", {})
        assert produced[0].confidence == 0.7

    def test_multiple_rules(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B")
        tx.add_rule("ra", a.term_id, lambda d: True)
        tx.add_rule("rb", b.term_id, lambda d: True)
        produced = tx.apply_rules("doc1", {})
        assert len(produced) == 2

    def test_disabled_rule_skipped(self):
        tx = DocTaxonomy()
        t = tx.add_term("python")
        r = tx.add_rule("py", t.term_id, lambda d: True)
        r.enabled = False
        assert tx.apply_rules("doc1", {}) == []

    def test_exception_in_condition_is_safe(self):
        tx = DocTaxonomy()
        t = tx.add_term("python")

        def bad(d):
            raise RuntimeError("boom")

        tx.add_rule("py", t.term_id, bad)
        assert tx.apply_rules("doc1", {}) == []

    def test_classification_persisted(self):
        tx = DocTaxonomy()
        t = tx.add_term("python")
        tx.add_rule("py", t.term_id, lambda d: True)
        tx.apply_rules("doc1", {}, now=99.0)
        cs = tx.classifications_for_doc("doc1")
        assert len(cs) == 1
        assert cs[0].assigned_at == 99.0


# --------------------------------------------------------------------------- #
# Aggregates                                                                  #
# --------------------------------------------------------------------------- #
class TestTermCount:
    def test_empty(self):
        assert DocTaxonomy().term_count == 0

    def test_after_adds(self):
        tx = DocTaxonomy()
        tx.add_term("A")
        tx.add_term("B")
        assert tx.term_count == 2

    def test_after_remove(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        tx.add_term("B")
        tx.remove_term(a.term_id)
        assert tx.term_count == 1


class TestDocCount:
    def test_empty(self):
        assert DocTaxonomy().doc_count() == 0

    def test_unique_docs(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B")
        tx.classify("doc1", a.term_id)
        tx.classify("doc1", b.term_id)
        tx.classify("doc2", a.term_id)
        assert tx.doc_count() == 2

    def test_decreases_on_unclassify(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        tx.classify("doc1", a.term_id)
        assert tx.doc_count() == 1
        tx.unclassify("doc1", a.term_id)
        assert tx.doc_count() == 0


class TestClear:
    def test_clears_everything(self):
        tx = DocTaxonomy()
        t = tx.add_term("A")
        tx.classify("doc1", t.term_id)
        tx.add_rule("r", t.term_id, lambda d: True)
        tx.clear()
        assert tx.term_count == 0
        assert tx.doc_count() == 0
        assert tx.all_terms() == []

    def test_counters_reset(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        tx.clear()
        b = tx.add_term("B")
        # IDs should restart from term_1
        assert b.term_id == "term_1"
        # and shouldn't collide with previously issued id (a was term_1 too)
        assert a.term_id == b.term_id  # both first


# --------------------------------------------------------------------------- #
# Edge cases                                                                  #
# --------------------------------------------------------------------------- #
class TestEdgeCases:
    def test_remove_term_with_grandchildren(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B", parent_id=a.term_id)
        c = tx.add_term("C", parent_id=b.term_id)
        d = tx.add_term("D", parent_id=c.term_id)
        tx.remove_term(a.term_id)
        for x in (a, b, c, d):
            assert tx.get_term(x.term_id) is None

    def test_descendants_count_after_remove(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        for _ in range(5):
            tx.add_term("child", parent_id=a.term_id)
        assert len(tx.descendants(a.term_id)) == 5
        tx.remove_term(a.term_id)
        assert tx.descendants(a.term_id) == []

    def test_classify_then_remove_term_cleans_classification(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        tx.classify("doc1", a.term_id)
        tx.remove_term(a.term_id)
        assert tx.doc_count() == 0

    def test_docs_for_term_dedup_across_descendants(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B", parent_id=a.term_id)
        c = tx.add_term("C", parent_id=a.term_id)
        tx.classify("d1", b.term_id)
        tx.classify("d1", c.term_id)
        docs = tx.docs_for_term(a.term_id, include_descendants=True)
        assert sorted(docs) == ["d1"]

    def test_move_term_keeps_subtree(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        b = tx.add_term("B")
        c = tx.add_term("C", parent_id=a.term_id)
        d = tx.add_term("D", parent_id=c.term_id)
        tx.move_term(c.term_id, b.term_id)
        # d should still be a descendant of c (and of b)
        ids = {t.term_id for t in tx.descendants(b.term_id)}
        assert c.term_id in ids
        assert d.term_id in ids

    def test_apply_rules_updates_existing_classification(self):
        tx = DocTaxonomy()
        t = tx.add_term("A")
        tx.classify("doc1", t.term_id, confidence=0.1, assigned_by="manual")
        tx.add_rule("r", t.term_id, lambda d: True, confidence=0.9)
        tx.apply_rules("doc1", {})
        cs = tx.classifications_for_doc("doc1")
        assert len(cs) == 1
        assert cs[0].confidence == 0.9

    def test_taxonomies_with_only_non_default(self):
        tx = DocTaxonomy()
        tx.add_term("X", taxonomy="custom")
        assert tx.taxonomies() == ["custom"]

    def test_root_terms_empty_when_all_children(self):
        tx = DocTaxonomy()
        a = tx.add_term("A")
        tx.add_term("B", parent_id=a.term_id)
        roots = tx.root_terms()
        assert len(roots) == 1
        assert roots[0].term_id == a.term_id
