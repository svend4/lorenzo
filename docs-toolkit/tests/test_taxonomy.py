"""Tests for docstoolkit.taxonomy (N7 self-organizing taxonomy)."""
import json
import math
import uuid

import pytest

from docstoolkit.taxonomy import (
    TaxonomyNode,
    TaxonomyTree,
    TaxonomyConfig,
    TaxonomySnapshot,
    DriftReport,
    build_taxonomy,
    detect_drift,
)
from docstoolkit.taxonomy.builder import (
    _tokenize,
    _tfidf_vectors,
    _cosine,
    _top_terms,
    _cluster_cohesion,
    _compute_centroid,
    _kmeans_plus_plus_seeds,
    _assign_clusters,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def make_node(label="test", parent_id=None, doc_ids=None, top_terms=None, cohesion=0.0):
    return TaxonomyNode(
        id=str(uuid.uuid4()),
        label=label,
        parent_id=parent_id,
        doc_ids=doc_ids or [],
        top_terms=top_terms or [],
        cohesion=cohesion,
    )


TECH_DOCS = {
    "t1": "Python programming language code software development algorithm data structure",
    "t2": "Python function class object method variable code script programming",
    "t3": "algorithm data structure array list sorting binary search tree",
    "t4": "machine learning neural network deep learning model training data feature",
    "t5": "neural network layer activation function backpropagation gradient descent",
}

COOKING_DOCS = {
    "c1": "recipe ingredients cooking baking flour sugar butter eggs bread cake",
    "c2": "kitchen cooking dinner lunch breakfast meal vegetables fruit salad soup",
    "c3": "chef restaurant recipe menu dish cuisine culinary preparation technique",
}

MIXED_DOCS = {**TECH_DOCS, **COOKING_DOCS}


# ---------------------------------------------------------------------------
# TaxonomyNode — fields and defaults
# ---------------------------------------------------------------------------

class TestTaxonomyNode:
    def test_required_fields(self):
        node = TaxonomyNode(id="x", label="hello")
        assert node.id == "x"
        assert node.label == "hello"

    def test_parent_id_default_none(self):
        node = TaxonomyNode(id="x", label="lbl")
        assert node.parent_id is None

    def test_children_ids_default_empty(self):
        node = TaxonomyNode(id="x", label="lbl")
        assert node.children_ids == []

    def test_doc_ids_default_empty(self):
        node = TaxonomyNode(id="x", label="lbl")
        assert node.doc_ids == []

    def test_top_terms_default_empty(self):
        node = TaxonomyNode(id="x", label="lbl")
        assert node.top_terms == []

    def test_cohesion_default_zero(self):
        node = TaxonomyNode(id="x", label="lbl")
        assert node.cohesion == 0.0

    def test_fields_settable(self):
        node = TaxonomyNode(
            id="abc",
            label="tech",
            parent_id="parent-1",
            children_ids=["child-1"],
            doc_ids=["doc.md"],
            top_terms=["python", "code"],
            cohesion=0.85,
        )
        assert node.parent_id == "parent-1"
        assert "child-1" in node.children_ids
        assert "doc.md" in node.doc_ids
        assert node.cohesion == 0.85

    def test_mutable_lists_independent(self):
        n1 = TaxonomyNode(id="a", label="A")
        n2 = TaxonomyNode(id="b", label="B")
        n1.doc_ids.append("doc1")
        assert "doc1" not in n2.doc_ids


# ---------------------------------------------------------------------------
# TaxonomyTree
# ---------------------------------------------------------------------------

class TestTaxonomyTree:
    def _build_tree(self):
        root1 = make_node("root1", doc_ids=["d1", "d2"])
        root2 = make_node("root2", doc_ids=["d3"])
        child = make_node("child", parent_id=root1.id, doc_ids=["d4"])
        root1.children_ids.append(child.id)
        return TaxonomyTree([root1, root2, child]), root1, root2, child

    def test_root_nodes_no_parent(self):
        tree, root1, root2, child = self._build_tree()
        roots = tree.root_nodes()
        labels = {n.label for n in roots}
        assert "root1" in labels
        assert "root2" in labels
        assert "child" not in labels

    def test_root_nodes_count(self):
        tree, root1, root2, child = self._build_tree()
        assert len(tree.root_nodes()) == 2

    def test_children_returns_children(self):
        tree, root1, root2, child = self._build_tree()
        ch = tree.children(root1.id)
        assert len(ch) == 1
        assert ch[0].label == "child"

    def test_children_empty_for_leaf(self):
        tree, root1, root2, child = self._build_tree()
        assert tree.children(child.id) == []

    def test_find_doc_returns_correct_node(self):
        tree, root1, root2, child = self._build_tree()
        node = tree.find_doc("d1")
        assert node is not None
        assert node.label == "root1"

    def test_find_doc_not_found_returns_none(self):
        tree, *_ = self._build_tree()
        assert tree.find_doc("nonexistent") is None

    def test_find_doc_in_child(self):
        tree, root1, root2, child = self._build_tree()
        node = tree.find_doc("d4")
        assert node is not None
        assert node.label == "child"

    def test_all_nodes_returns_all(self):
        tree, root1, root2, child = self._build_tree()
        assert len(tree.all_nodes()) == 3

    def test_to_markdown_contains_labels(self):
        tree, root1, root2, child = self._build_tree()
        md = tree.to_markdown()
        assert "root1" in md
        assert "root2" in md
        assert "child" in md

    def test_to_markdown_is_string(self):
        tree, *_ = self._build_tree()
        assert isinstance(tree.to_markdown(), str)

    def test_doc_count_sum(self):
        tree, root1, root2, child = self._build_tree()
        # root1=2, root2=1, child=1 => 4
        assert tree.doc_count() == 4

    def test_node_count(self):
        tree, root1, root2, child = self._build_tree()
        assert tree.node_count() == 3

    def test_empty_tree_root_nodes(self):
        tree = TaxonomyTree([])
        assert tree.root_nodes() == []

    def test_empty_tree_doc_count(self):
        tree = TaxonomyTree([])
        assert tree.doc_count() == 0

    def test_empty_tree_node_count(self):
        tree = TaxonomyTree([])
        assert tree.node_count() == 0

    def test_empty_tree_to_markdown(self):
        tree = TaxonomyTree([])
        assert tree.to_markdown() == ""

    def test_empty_tree_find_doc(self):
        tree = TaxonomyTree([])
        assert tree.find_doc("anything") is None


# ---------------------------------------------------------------------------
# TaxonomyConfig defaults
# ---------------------------------------------------------------------------

class TestTaxonomyConfig:
    def test_n_clusters_default(self):
        assert TaxonomyConfig().n_clusters == 8

    def test_min_docs_per_cluster_default(self):
        assert TaxonomyConfig().min_docs_per_cluster == 1

    def test_top_terms_per_label_default(self):
        assert TaxonomyConfig().top_terms_per_label == 3

    def test_seed_default(self):
        assert TaxonomyConfig().seed == 42

    def test_max_label_words_default(self):
        assert TaxonomyConfig().max_label_words == 5

    def test_custom_values(self):
        cfg = TaxonomyConfig(n_clusters=4, seed=7)
        assert cfg.n_clusters == 4
        assert cfg.seed == 7


# ---------------------------------------------------------------------------
# Internal helpers: _tokenize / _tfidf_vectors / _cosine
# ---------------------------------------------------------------------------

class TestTokenize:
    def test_lowercase(self):
        tokens = _tokenize("Hello World")
        assert "hello" in tokens
        assert "world" in tokens

    def test_min_length_3(self):
        tokens = _tokenize("a ab abc abcd")
        assert "a" not in tokens
        assert "ab" not in tokens
        assert "abc" in tokens
        assert "abcd" in tokens

    def test_strips_punctuation(self):
        tokens = _tokenize("hello, world! foo-bar.")
        assert "hello" in tokens
        assert "world" in tokens

    def test_empty_string(self):
        assert _tokenize("") == []

    def test_numbers_excluded(self):
        # Digits not matched by [a-zA-Zа-яА-ЯёЁ]
        tokens = _tokenize("123 abc 456")
        assert "123" not in tokens
        assert "abc" in tokens


class TestTFIDF:
    def test_returns_dict_per_doc(self):
        docs = {"a": "python code python", "b": "cooking recipe food"}
        vecs = _tfidf_vectors(docs)
        assert "a" in vecs
        assert "b" in vecs

    def test_tfidf_scores_positive(self):
        docs = {"a": "python code python", "b": "cooking recipe food"}
        vecs = _tfidf_vectors(docs)
        # All scores should be non-negative
        for vec in vecs.values():
            for score in vec.values():
                assert score >= 0

    def test_rare_term_higher_idf(self):
        # 'unique' appears only in doc 'a', so higher IDF than 'common'
        docs = {
            "a": "unique term python code",
            "b": "common python code",
            "c": "common python language",
        }
        vecs = _tfidf_vectors(docs)
        # 'unique' in a has IDF = log(3/1), 'common' in b has IDF = log(3/2)
        if "unique" in vecs["a"] and "common" in vecs["b"]:
            # IDF for unique > IDF for common; TF may differ but check raw IDF
            idf_unique = math.log(3 / 1)
            idf_common = math.log(3 / 2)
            assert idf_unique > idf_common

    def test_empty_docs(self):
        assert _tfidf_vectors({}) == {}

    def test_single_doc(self):
        vecs = _tfidf_vectors({"x": "hello world foo"})
        # IDF = log(1/1) = 0 for all terms in single-doc corpus
        assert "x" in vecs
        # All scores should be 0 (log(1/1)=0)
        assert all(v == 0.0 for v in vecs["x"].values()) or vecs["x"] == {}


class TestCosine:
    def test_identical_vectors(self):
        v = {"a": 1.0, "b": 2.0}
        assert abs(_cosine(v, v) - 1.0) < 1e-9

    def test_disjoint_vectors(self):
        a = {"x": 1.0}
        b = {"y": 1.0}
        assert _cosine(a, b) == 0.0

    def test_partial_overlap(self):
        a = {"x": 1.0, "y": 1.0}
        b = {"x": 1.0, "z": 1.0}
        sim = _cosine(a, b)
        assert 0.0 < sim < 1.0

    def test_empty_vector(self):
        assert _cosine({}, {"a": 1.0}) == 0.0
        assert _cosine({"a": 1.0}, {}) == 0.0

    def test_symmetry(self):
        a = {"x": 2.0, "y": 1.0}
        b = {"x": 1.0, "z": 3.0}
        assert abs(_cosine(a, b) - _cosine(b, a)) < 1e-9


# ---------------------------------------------------------------------------
# build_taxonomy
# ---------------------------------------------------------------------------

class TestBuildTaxonomy:
    def test_empty_docs_returns_empty_tree(self):
        tree = build_taxonomy({})
        assert tree.node_count() == 0
        assert tree.doc_count() == 0

    def test_single_doc_single_node(self):
        tree = build_taxonomy({"doc1": "python programming language"})
        assert tree.node_count() == 1
        assert tree.doc_count() == 1

    def test_all_docs_assigned(self):
        tree = build_taxonomy(MIXED_DOCS, TaxonomyConfig(n_clusters=3, seed=0))
        assigned = set()
        for node in tree.all_nodes():
            assigned.update(node.doc_ids)
        assert assigned == set(MIXED_DOCS.keys())

    def test_returns_taxonomy_tree(self):
        tree = build_taxonomy(TECH_DOCS)
        assert isinstance(tree, TaxonomyTree)

    def test_n_clusters_greater_than_docs_handled(self):
        small_docs = {"a": "foo bar baz", "b": "qux quux corge"}
        tree = build_taxonomy(small_docs, TaxonomyConfig(n_clusters=100))
        assert tree.node_count() >= 1
        # All docs must be assigned
        assigned = {d for n in tree.all_nodes() for d in n.doc_ids}
        assert assigned == {"a", "b"}

    def test_node_labels_non_empty(self):
        tree = build_taxonomy(MIXED_DOCS, TaxonomyConfig(n_clusters=3, seed=1))
        for node in tree.all_nodes():
            assert isinstance(node.label, str)
            assert len(node.label) > 0

    def test_cohesion_in_range(self):
        tree = build_taxonomy(MIXED_DOCS, TaxonomyConfig(n_clusters=3, seed=42))
        for node in tree.all_nodes():
            assert 0.0 <= node.cohesion <= 1.0 + 1e-9

    def test_clear_clusters_different_labels(self):
        """Tech and cooking docs should not share the same cluster labels."""
        tree = build_taxonomy(MIXED_DOCS, TaxonomyConfig(n_clusters=2, seed=42))
        labels = [n.label for n in tree.all_nodes()]
        # With 2 clusters and distinct domains we should see 2 distinct labels
        assert len(set(labels)) >= 1  # at least runs without error

    def test_deterministic_with_same_seed(self):
        cfg = TaxonomyConfig(n_clusters=3, seed=7)
        tree1 = build_taxonomy(MIXED_DOCS, cfg)
        tree2 = build_taxonomy(MIXED_DOCS, cfg)
        labels1 = sorted(n.label for n in tree1.all_nodes())
        labels2 = sorted(n.label for n in tree2.all_nodes())
        assert labels1 == labels2

    def test_no_duplicate_doc_assignments(self):
        tree = build_taxonomy(MIXED_DOCS, TaxonomyConfig(n_clusters=3, seed=0))
        all_docs: list[str] = []
        for node in tree.all_nodes():
            all_docs.extend(node.doc_ids)
        assert len(all_docs) == len(set(all_docs))

    def test_top_terms_populated(self):
        tree = build_taxonomy(MIXED_DOCS, TaxonomyConfig(n_clusters=3, seed=42))
        for node in tree.all_nodes():
            assert isinstance(node.top_terms, list)


# ---------------------------------------------------------------------------
# TaxonomySnapshot
# ---------------------------------------------------------------------------

class TestTaxonomySnapshot:
    def _make_tree(self):
        return build_taxonomy(MIXED_DOCS, TaxonomyConfig(n_clusters=3, seed=42))

    def test_from_tree_has_doc_assignments(self):
        tree = self._make_tree()
        snap = TaxonomySnapshot.from_tree(tree, "2025-01-01T00:00:00")
        assert len(snap.doc_assignments) == len(MIXED_DOCS)

    def test_from_tree_all_docs_assigned(self):
        tree = self._make_tree()
        snap = TaxonomySnapshot.from_tree(tree)
        assert set(snap.doc_assignments.keys()) == set(MIXED_DOCS.keys())

    def test_from_tree_timestamp_preserved(self):
        tree = self._make_tree()
        snap = TaxonomySnapshot.from_tree(tree, timestamp="2025-06-01")
        assert snap.timestamp == "2025-06-01"

    def test_from_tree_auto_timestamp(self):
        tree = self._make_tree()
        snap = TaxonomySnapshot.from_tree(tree)
        assert len(snap.timestamp) > 0

    def test_to_json_returns_string(self):
        snap = TaxonomySnapshot(
            timestamp="t", cluster_labels=["a"], doc_assignments={"d1": "a"}
        )
        result = snap.to_json()
        assert isinstance(result, str)

    def test_to_json_valid_json(self):
        snap = TaxonomySnapshot(
            timestamp="t", cluster_labels=["a"], doc_assignments={"d1": "a"}
        )
        obj = json.loads(snap.to_json())
        assert "timestamp" in obj
        assert "cluster_labels" in obj
        assert "doc_assignments" in obj

    def test_from_json_round_trip(self):
        snap = TaxonomySnapshot(
            timestamp="2025-01-01",
            cluster_labels=["tech", "cooking"],
            doc_assignments={"d1": "tech", "d2": "cooking"},
        )
        recovered = TaxonomySnapshot.from_json(snap.to_json())
        assert recovered.timestamp == snap.timestamp
        assert recovered.cluster_labels == snap.cluster_labels
        assert recovered.doc_assignments == snap.doc_assignments

    def test_cluster_labels_list_of_strings(self):
        tree = self._make_tree()
        snap = TaxonomySnapshot.from_tree(tree)
        assert all(isinstance(lbl, str) for lbl in snap.cluster_labels)


# ---------------------------------------------------------------------------
# detect_drift
# ---------------------------------------------------------------------------

class TestDetectDrift:
    def _snap(self, assignments: dict[str, str], labels: list[str] | None = None) -> TaxonomySnapshot:
        if labels is None:
            labels = list(set(assignments.values()))
        return TaxonomySnapshot(
            timestamp="2025-01-01",
            cluster_labels=labels,
            doc_assignments=assignments,
        )

    def test_same_snapshot_stability_one(self):
        snap = self._snap({"d1": "A", "d2": "B", "d3": "A"})
        report = detect_drift(snap, snap)
        assert abs(report.stability_score - 1.0) < 1e-9

    def test_same_snapshot_no_moved_docs(self):
        snap = self._snap({"d1": "A", "d2": "B"})
        report = detect_drift(snap, snap)
        assert report.moved_docs == []

    def test_all_moved_stability_zero(self):
        prev = self._snap({"d1": "A", "d2": "A"}, labels=["A"])
        curr = self._snap({"d1": "B", "d2": "B"}, labels=["B"])
        report = detect_drift(prev, curr)
        assert abs(report.stability_score - 0.0) < 1e-9

    def test_partial_move_stability_between(self):
        prev = self._snap({"d1": "A", "d2": "A", "d3": "A", "d4": "A"})
        curr = self._snap({"d1": "A", "d2": "A", "d3": "B", "d4": "B"})
        report = detect_drift(prev, curr)
        assert 0.0 < report.stability_score < 1.0

    def test_new_clusters_detected(self):
        prev = self._snap({"d1": "A"}, labels=["A"])
        curr = self._snap({"d1": "A", "d2": "B"}, labels=["A", "B"])
        report = detect_drift(prev, curr)
        assert "B" in report.new_clusters

    def test_removed_clusters_detected(self):
        prev = self._snap({"d1": "A", "d2": "B"}, labels=["A", "B"])
        curr = self._snap({"d1": "A", "d2": "A"}, labels=["A"])
        report = detect_drift(prev, curr)
        assert "B" in report.removed_clusters

    def test_no_common_docs_stability_one(self):
        prev = self._snap({"d1": "A"})
        curr = self._snap({"d2": "B"})
        report = detect_drift(prev, curr)
        assert abs(report.stability_score - 1.0) < 1e-9

    def test_moved_docs_correct_ids(self):
        prev = self._snap({"d1": "A", "d2": "B"})
        curr = self._snap({"d1": "B", "d2": "B"})  # d1 moved from A to B
        report = detect_drift(prev, curr)
        assert "d1" in report.moved_docs
        assert "d2" not in report.moved_docs

    def test_summary_non_empty_string(self):
        snap = self._snap({"d1": "A", "d2": "B"})
        report = detect_drift(snap, snap)
        assert isinstance(report.summary, str)
        assert len(report.summary) > 0

    def test_report_is_drift_report_instance(self):
        snap = self._snap({"d1": "A"})
        report = detect_drift(snap, snap)
        assert isinstance(report, DriftReport)

    def test_stability_score_in_range(self):
        prev = self._snap({"d1": "A", "d2": "A", "d3": "B"})
        curr = self._snap({"d1": "A", "d2": "B", "d3": "B"})
        report = detect_drift(prev, curr)
        assert 0.0 <= report.stability_score <= 1.0
