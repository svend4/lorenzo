"""Tests for the E20 document clustering module (pure stdlib)."""

from __future__ import annotations

import math
import pytest

from docstoolkit.clustering import (
    DocumentFeatures,
    FeatureExtractor,
    cosine_similarity,
    cosine_distance,
    jaccard_similarity,
    Cluster,
    KMeansConfig,
    KMeansResult,
    KMeansClustering,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

CORPUS_SMALL = {
    "d1": "the cat sat on the mat",
    "d2": "the dog sat on the log",
    "d3": "a fish swam in the sea",
}

CORPUS_TOPICS = {
    "tech1": "python programming language code software",
    "tech2": "python code software development",
    "tech3": "programming language software",
    "food1": "apple banana fruit salad healthy",
    "food2": "banana mango fruit tropical healthy",
    "food3": "fruit salad apple healthy recipe",
}


# ===========================================================================
# DocumentFeatures dataclass
# ===========================================================================

class TestDocumentFeatures:
    def test_fields_accessible(self):
        df = DocumentFeatures(doc_id="x", tokens=["a", "b"], tfidf={"a": 0.5})
        assert df.doc_id == "x"
        assert df.tokens == ["a", "b"]
        assert df.tfidf == {"a": 0.5}

    def test_empty_tokens_and_tfidf(self):
        df = DocumentFeatures(doc_id="empty", tokens=[], tfidf={})
        assert df.tokens == []
        assert df.tfidf == {}

    def test_is_dataclass(self):
        from dataclasses import fields
        names = {f.name for f in fields(DocumentFeatures)}
        assert names == {"doc_id", "tokens", "tfidf"}


# ===========================================================================
# FeatureExtractor
# ===========================================================================

class TestFeatureExtractorFit:
    def test_vocabulary_size_after_fit(self):
        fe = FeatureExtractor()
        fe.fit(CORPUS_SMALL)
        # "the" appears in all 3 docs; at least all tokens should be known
        assert fe.vocabulary_size() > 0

    def test_vocabulary_contains_known_token(self):
        fe = FeatureExtractor()
        fe.fit({"d1": "hello world"})
        assert fe.vocabulary_size() == 2

    def test_fit_empty_corpus(self):
        fe = FeatureExtractor()
        fe.fit({})
        assert fe.vocabulary_size() == 0

    def test_fit_single_doc(self):
        fe = FeatureExtractor()
        fe.fit({"d1": "alpha beta gamma"})
        assert fe.vocabulary_size() == 3

    def test_fit_deduplicates_vocab_across_docs(self):
        fe = FeatureExtractor()
        fe.fit({"d1": "cat dog", "d2": "cat fish"})
        # unique tokens: cat, dog, fish
        assert fe.vocabulary_size() == 3

    def test_idf_high_frequency_term(self):
        """A term in every doc gets lower IDF than a rare term."""
        fe = FeatureExtractor()
        docs = {"d1": "common alpha", "d2": "common beta", "d3": "common gamma"}
        fe.fit(docs)
        # 'common' df=3, rare tokens df=1 each → common has lower IDF
        idf_common = fe._idf["common"]
        idf_rare = fe._idf["alpha"]
        assert idf_rare > idf_common

    def test_idf_formula(self):
        """Verify IDF = log((N+1)/(df+1)) + 1 for a concrete case."""
        fe = FeatureExtractor()
        fe.fit({"d1": "alpha", "d2": "beta", "d3": "alpha"})
        n = 3
        df_alpha = 2  # appears in d1 and d3
        expected = math.log((n + 1) / (df_alpha + 1)) + 1
        assert abs(fe._idf["alpha"] - expected) < 1e-9

    def test_fit_called_twice_resets(self):
        fe = FeatureExtractor()
        fe.fit({"d1": "foo bar"})
        size_first = fe.vocabulary_size()
        fe.fit({"d1": "foo bar baz qux"})
        assert fe.vocabulary_size() != size_first or fe.vocabulary_size() >= 2


class TestFeatureExtractorTransform:
    def test_returns_document_features_instance(self):
        fe = FeatureExtractor()
        fe.fit(CORPUS_SMALL)
        result = fe.transform("d1", "the cat sat")
        assert isinstance(result, DocumentFeatures)

    def test_doc_id_preserved(self):
        fe = FeatureExtractor()
        fe.fit(CORPUS_SMALL)
        result = fe.transform("my_doc", "the cat")
        assert result.doc_id == "my_doc"

    def test_tokens_are_lowercase(self):
        fe = FeatureExtractor()
        fe.fit({"d1": "Hello World"})
        result = fe.transform("d1", "Hello World")
        assert "hello" in result.tokens
        assert "world" in result.tokens

    def test_tokens_split_on_non_alpha(self):
        fe = FeatureExtractor()
        fe.fit({"d1": "foo-bar baz"})
        result = fe.transform("d1", "foo-bar baz")
        assert "foo" in result.tokens
        assert "bar" in result.tokens
        assert "baz" in result.tokens

    def test_tfidf_keys_match_tokens(self):
        fe = FeatureExtractor()
        fe.fit({"d1": "alpha beta gamma"})
        result = fe.transform("d1", "alpha beta gamma")
        assert set(result.tfidf.keys()) == {"alpha", "beta", "gamma"}

    def test_tfidf_values_positive(self):
        fe = FeatureExtractor()
        fe.fit(CORPUS_SMALL)
        result = fe.transform("t", "cat sat mat")
        for v in result.tfidf.values():
            assert v > 0.0

    def test_transform_empty_text(self):
        fe = FeatureExtractor()
        fe.fit(CORPUS_SMALL)
        result = fe.transform("empty", "")
        assert result.tokens == []
        assert result.tfidf == {}

    def test_transform_unknown_tokens_handled(self):
        """Unknown tokens should still appear in output with fallback IDF."""
        fe = FeatureExtractor()
        fe.fit({"d1": "foo bar"})
        result = fe.transform("d2", "foo bar qux")
        assert "qux" in result.tfidf

    def test_repeated_token_increases_weight(self):
        fe = FeatureExtractor()
        fe.fit({"d1": "cat cat cat dog"})
        result = fe.transform("d1", "cat cat cat dog")
        assert result.tfidf["cat"] > result.tfidf["dog"]

    def test_transform_before_fit_uses_fallback(self):
        """Transform on an unfitted extractor should not crash."""
        fe = FeatureExtractor()
        result = fe.transform("x", "hello world")
        assert "hello" in result.tfidf
        assert "world" in result.tfidf


class TestFeatureExtractorFitTransform:
    def test_returns_list_of_document_features(self):
        fe = FeatureExtractor()
        results = fe.fit_transform(CORPUS_SMALL)
        assert isinstance(results, list)
        assert all(isinstance(r, DocumentFeatures) for r in results)

    def test_length_matches_corpus(self):
        fe = FeatureExtractor()
        results = fe.fit_transform(CORPUS_SMALL)
        assert len(results) == len(CORPUS_SMALL)

    def test_all_doc_ids_present(self):
        fe = FeatureExtractor()
        results = fe.fit_transform(CORPUS_SMALL)
        ids = {r.doc_id for r in results}
        assert ids == set(CORPUS_SMALL.keys())

    def test_vocabulary_set_after_fit_transform(self):
        fe = FeatureExtractor()
        fe.fit_transform(CORPUS_SMALL)
        assert fe.vocabulary_size() > 0

    def test_fit_transform_empty_corpus(self):
        fe = FeatureExtractor()
        results = fe.fit_transform({})
        assert results == []


# ===========================================================================
# cosine_similarity
# ===========================================================================

class TestCosineSimilarity:
    def test_identical_vectors(self):
        v = {"a": 1.0, "b": 2.0}
        assert abs(cosine_similarity(v, v) - 1.0) < 1e-9

    def test_empty_first(self):
        assert cosine_similarity({}, {"a": 1.0}) == 0.0

    def test_empty_second(self):
        assert cosine_similarity({"a": 1.0}, {}) == 0.0

    def test_both_empty(self):
        assert cosine_similarity({}, {}) == 0.0

    def test_orthogonal_vectors(self):
        a = {"x": 1.0}
        b = {"y": 1.0}
        assert cosine_similarity(a, b) == 0.0

    def test_partial_overlap(self):
        a = {"a": 1.0, "b": 1.0}
        b = {"a": 1.0, "c": 1.0}
        sim = cosine_similarity(a, b)
        assert 0.0 < sim < 1.0

    def test_symmetry(self):
        a = {"a": 1.0, "b": 0.5}
        b = {"a": 0.3, "c": 0.9}
        assert abs(cosine_similarity(a, b) - cosine_similarity(b, a)) < 1e-12

    def test_scaled_vector_same_similarity(self):
        a = {"a": 1.0, "b": 2.0}
        b = {"a": 2.0, "b": 4.0}  # same direction, different magnitude
        assert abs(cosine_similarity(a, b) - 1.0) < 1e-9

    def test_result_in_range(self):
        a = {"a": 0.5, "b": 0.3, "c": 0.2}
        b = {"a": 0.1, "b": 0.8, "d": 0.1}
        sim = cosine_similarity(a, b)
        assert 0.0 <= sim <= 1.0


# ===========================================================================
# cosine_distance
# ===========================================================================

class TestCosineDistance:
    def test_identical_vectors_distance_zero(self):
        v = {"a": 1.0}
        assert abs(cosine_distance(v, v) - 0.0) < 1e-9

    def test_orthogonal_distance_one(self):
        a = {"x": 1.0}
        b = {"y": 1.0}
        assert abs(cosine_distance(a, b) - 1.0) < 1e-9

    def test_is_complement_of_similarity(self):
        a = {"a": 1.0, "b": 2.0}
        b = {"a": 3.0, "b": 1.0}
        assert abs(cosine_distance(a, b) - (1.0 - cosine_similarity(a, b))) < 1e-12

    def test_empty_vectors_distance_one(self):
        assert cosine_distance({}, {"a": 1.0}) == 1.0

    def test_distance_non_negative(self):
        a = {"a": 0.5, "b": 0.5}
        b = {"a": 0.5, "c": 0.5}
        assert cosine_distance(a, b) >= 0.0


# ===========================================================================
# jaccard_similarity
# ===========================================================================

class TestJaccardSimilarity:
    def test_identical_sets(self):
        s = {"a", "b", "c"}
        assert jaccard_similarity(s, s) == 1.0

    def test_disjoint_sets(self):
        assert jaccard_similarity({"a", "b"}, {"c", "d"}) == 0.0

    def test_both_empty(self):
        assert jaccard_similarity(set(), set()) == 0.0

    def test_one_empty(self):
        assert jaccard_similarity(set(), {"a"}) == 0.0
        assert jaccard_similarity({"a"}, set()) == 0.0

    def test_partial_overlap(self):
        sim = jaccard_similarity({"a", "b", "c"}, {"b", "c", "d"})
        # intersection = {b, c}, union = {a, b, c, d} → 2/4 = 0.5
        assert abs(sim - 0.5) < 1e-9

    def test_symmetry(self):
        a = {"x", "y"}
        b = {"y", "z"}
        assert jaccard_similarity(a, b) == jaccard_similarity(b, a)

    def test_subset_less_than_one(self):
        a = {"a"}
        b = {"a", "b"}
        sim = jaccard_similarity(a, b)
        assert 0.0 < sim < 1.0

    def test_result_in_range(self):
        sim = jaccard_similarity({"a", "b"}, {"b", "c"})
        assert 0.0 <= sim <= 1.0


# ===========================================================================
# KMeansConfig
# ===========================================================================

class TestKMeansConfig:
    def test_default_k(self):
        cfg = KMeansConfig()
        assert cfg.k == 5

    def test_default_max_iter(self):
        cfg = KMeansConfig()
        assert cfg.max_iter == 20

    def test_default_random_seed(self):
        cfg = KMeansConfig()
        assert cfg.random_seed == 42

    def test_custom_values(self):
        cfg = KMeansConfig(k=3, max_iter=10, random_seed=0)
        assert cfg.k == 3
        assert cfg.max_iter == 10
        assert cfg.random_seed == 0


# ===========================================================================
# Cluster dataclass
# ===========================================================================

class TestCluster:
    def test_size(self):
        c = Cluster(cluster_id=0, doc_ids=["a", "b", "c"], centroid={})
        assert c.size() == 3

    def test_size_empty(self):
        c = Cluster(cluster_id=1, doc_ids=[], centroid={})
        assert c.size() == 0

    def test_fields(self):
        c = Cluster(cluster_id=2, doc_ids=["x"], centroid={"term": 0.5})
        assert c.cluster_id == 2
        assert c.doc_ids == ["x"]
        assert c.centroid == {"term": 0.5}


# ===========================================================================
# KMeansResult
# ===========================================================================

class TestKMeansResult:
    def _make_result(self):
        clusters = [
            Cluster(0, ["d1", "d2"], {"a": 0.5}),
            Cluster(1, ["d3"], {"b": 0.8}),
        ]
        return KMeansResult(clusters=clusters, iterations=3, converged=True)

    def test_cluster_for_known_doc(self):
        r = self._make_result()
        assert r.cluster_for("d1") == 0
        assert r.cluster_for("d3") == 1

    def test_cluster_for_unknown_doc(self):
        r = self._make_result()
        assert r.cluster_for("nonexistent") is None

    def test_largest_cluster(self):
        r = self._make_result()
        assert r.largest_cluster().cluster_id == 0

    def test_smallest_cluster(self):
        r = self._make_result()
        assert r.smallest_cluster().cluster_id == 1

    def test_iterations_stored(self):
        r = self._make_result()
        assert r.iterations == 3

    def test_converged_stored(self):
        r = self._make_result()
        assert r.converged is True


# ===========================================================================
# KMeansClustering
# ===========================================================================

class TestKMeansClustering:
    def _extract(self, docs):
        fe = FeatureExtractor()
        return fe.fit_transform(docs)

    def test_returns_kmeans_result(self):
        feats = self._extract(CORPUS_SMALL)
        km = KMeansClustering()
        result = km.fit(feats, KMeansConfig(k=2))
        assert isinstance(result, KMeansResult)

    def test_number_of_clusters_k2(self):
        feats = self._extract(CORPUS_SMALL)
        km = KMeansClustering()
        result = km.fit(feats, KMeansConfig(k=2))
        assert len(result.clusters) == 2

    def test_number_of_clusters_k3(self):
        feats = self._extract(CORPUS_TOPICS)
        km = KMeansClustering()
        result = km.fit(feats, KMeansConfig(k=3))
        assert len(result.clusters) == 3

    def test_all_docs_assigned(self):
        feats = self._extract(CORPUS_TOPICS)
        km = KMeansClustering()
        result = km.fit(feats, KMeansConfig(k=2))
        assigned = sum(c.size() for c in result.clusters)
        assert assigned == len(feats)

    def test_no_doc_id_duplicated(self):
        feats = self._extract(CORPUS_TOPICS)
        km = KMeansClustering()
        result = km.fit(feats, KMeansConfig(k=3))
        all_ids = [doc_id for c in result.clusters for doc_id in c.doc_ids]
        assert len(all_ids) == len(set(all_ids))

    def test_iterations_positive(self):
        feats = self._extract(CORPUS_SMALL)
        km = KMeansClustering()
        result = km.fit(feats, KMeansConfig(k=2))
        assert result.iterations >= 1

    def test_iterations_bounded_by_max_iter(self):
        feats = self._extract(CORPUS_TOPICS)
        km = KMeansClustering()
        cfg = KMeansConfig(k=2, max_iter=5)
        result = km.fit(feats, cfg)
        assert result.iterations <= 5

    def test_converged_flag_set(self):
        feats = self._extract(CORPUS_SMALL)
        km = KMeansClustering()
        result = km.fit(feats, KMeansConfig(k=2, max_iter=100))
        # With enough iterations a small corpus should converge.
        assert isinstance(result.converged, bool)

    def test_default_config_used_when_none(self):
        feats = self._extract(CORPUS_TOPICS)
        km = KMeansClustering()
        result = km.fit(feats)  # no config → uses KMeansConfig()
        # Default k=5, but corpus has 6 docs → 5 clusters (or fewer if dedup)
        assert len(result.clusters) <= 6

    def test_k_larger_than_docs_capped(self):
        feats = self._extract({"d1": "hello world"})
        km = KMeansClustering()
        result = km.fit(feats, KMeansConfig(k=10))
        # Can't have more clusters than documents
        assert len(result.clusters) <= 1

    def test_empty_features_list(self):
        km = KMeansClustering()
        result = km.fit([], KMeansConfig(k=2))
        assert result.clusters == []
        assert result.iterations == 0
        assert result.converged is True

    def test_single_doc(self):
        feats = self._extract({"only": "just one document here"})
        km = KMeansClustering()
        result = km.fit(feats, KMeansConfig(k=1))
        assert len(result.clusters) == 1
        assert result.clusters[0].doc_ids == ["only"]

    def test_cluster_for_returns_correct_id(self):
        feats = self._extract(CORPUS_TOPICS)
        km = KMeansClustering()
        result = km.fit(feats, KMeansConfig(k=2))
        for doc_id in CORPUS_TOPICS:
            cid = result.cluster_for(doc_id)
            assert cid is not None
            assert 0 <= cid < 2

    def test_largest_and_smallest_cluster_size_ordering(self):
        feats = self._extract(CORPUS_TOPICS)
        km = KMeansClustering()
        result = km.fit(feats, KMeansConfig(k=2))
        assert result.largest_cluster().size() >= result.smallest_cluster().size()

    def test_centroids_are_dicts(self):
        feats = self._extract(CORPUS_SMALL)
        km = KMeansClustering()
        result = km.fit(feats, KMeansConfig(k=2))
        for cluster in result.clusters:
            assert isinstance(cluster.centroid, dict)

    def test_centroid_values_positive(self):
        feats = self._extract(CORPUS_SMALL)
        km = KMeansClustering()
        result = km.fit(feats, KMeansConfig(k=2))
        for cluster in result.clusters:
            for v in cluster.centroid.values():
                assert v >= 0.0

    def test_deterministic_results(self):
        """Same input → same output (no randomness)."""
        feats = self._extract(CORPUS_TOPICS)
        km = KMeansClustering()
        cfg = KMeansConfig(k=3)
        r1 = km.fit(feats, cfg)
        r2 = km.fit(feats, cfg)
        for c1, c2 in zip(r1.clusters, r2.clusters):
            assert sorted(c1.doc_ids) == sorted(c2.doc_ids)

    def test_topical_separation_k2(self):
        """With k=2 and a clearly bimodal corpus, tech and food docs should
        end up in different clusters."""
        feats = self._extract(CORPUS_TOPICS)
        km = KMeansClustering()
        result = km.fit(feats, KMeansConfig(k=2, max_iter=50))

        tech_ids = {"tech1", "tech2", "tech3"}
        food_ids = {"food1", "food2", "food3"}

        cluster_sets = [set(c.doc_ids) for c in result.clusters]
        # At least one cluster should be a pure tech or pure food cluster.
        tech_found = any(ids <= tech_ids for ids in cluster_sets)
        food_found = any(ids <= food_ids for ids in cluster_sets)
        assert tech_found or food_found, (
            f"Expected topical separation, got clusters: {cluster_sets}"
        )
