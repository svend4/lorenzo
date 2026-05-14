"""Tests for the E66 embedding_store module.

Coverage targets:
- EmbeddingVector: dimension, norm, normalize, dot, cosine_similarity
- EmbeddingStore: add/get/remove/search/all_ids/size/clear, dimension
  mismatch, normalize_on_add, search ranking
- Metric: cosine vs dot differences
- EmbeddingPersistence: save/load roundtrip, search after load
- Edge cases: empty store, remove non-existent, top_k > size
"""

from __future__ import annotations

import json
import math
import tempfile
import os
import time
from pathlib import Path

import pytest

from docstoolkit.embedding_store import (
    EmbeddingVector,
    EmbeddingStore,
    EmbeddingPersistence,
    StoreConfig,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_vec(doc_id: str, values: list[float], metadata: dict | None = None) -> EmbeddingVector:
    return EmbeddingVector(doc_id=doc_id, vector=values, metadata=metadata or {})


def unit_vec(doc_id: str, dim: int, axis: int) -> EmbeddingVector:
    """Return a unit vector along *axis* in *dim* dimensions."""
    v = [0.0] * dim
    v[axis] = 1.0
    return EmbeddingVector(doc_id=doc_id, vector=v)


# ===========================================================================
# EmbeddingVector tests
# ===========================================================================

class TestEmbeddingVectorDimension:
    def test_dimension_basic(self):
        v = make_vec("a", [1.0, 2.0, 3.0])
        assert v.dimension() == 3

    def test_dimension_single(self):
        v = make_vec("a", [5.0])
        assert v.dimension() == 1

    def test_dimension_empty(self):
        v = make_vec("a", [])
        assert v.dimension() == 0

    def test_dimension_large(self):
        v = make_vec("a", [1.0] * 512)
        assert v.dimension() == 512


class TestEmbeddingVectorNorm:
    def test_norm_unit_axis(self):
        v = make_vec("a", [1.0, 0.0, 0.0])
        assert math.isclose(v.norm(), 1.0)

    def test_norm_zero_vector(self):
        v = make_vec("a", [0.0, 0.0, 0.0])
        assert v.norm() == 0.0

    def test_norm_known_value(self):
        v = make_vec("a", [3.0, 4.0])
        assert math.isclose(v.norm(), 5.0)

    def test_norm_negative_components(self):
        v = make_vec("a", [-3.0, 4.0])
        assert math.isclose(v.norm(), 5.0)

    def test_norm_all_ones(self):
        n = 4
        v = make_vec("a", [1.0] * n)
        assert math.isclose(v.norm(), math.sqrt(n))

    def test_norm_single(self):
        v = make_vec("a", [7.0])
        assert math.isclose(v.norm(), 7.0)


class TestEmbeddingVectorNormalize:
    def test_normalize_unit_length(self):
        v = make_vec("a", [3.0, 4.0])
        n = v.normalize()
        assert math.isclose(n.norm(), 1.0, rel_tol=1e-9)

    def test_normalize_already_unit(self):
        v = make_vec("a", [1.0, 0.0])
        n = v.normalize()
        assert math.isclose(n.norm(), 1.0)

    def test_normalize_zero_vector_unchanged(self):
        v = make_vec("a", [0.0, 0.0])
        n = v.normalize()
        assert n.vector == [0.0, 0.0]

    def test_normalize_preserves_doc_id(self):
        v = make_vec("my_doc", [1.0, 2.0])
        assert v.normalize().doc_id == "my_doc"

    def test_normalize_preserves_metadata(self):
        v = make_vec("a", [1.0, 2.0], metadata={"tag": "x"})
        assert v.normalize().metadata == {"tag": "x"}

    def test_normalize_preserves_created_at(self):
        ts = 12345.0
        v = EmbeddingVector(doc_id="a", vector=[1.0, 2.0], created_at=ts)
        assert v.normalize().created_at == ts

    def test_normalize_returns_new_object(self):
        v = make_vec("a", [1.0, 2.0])
        n = v.normalize()
        assert n is not v

    def test_normalize_direction_preserved(self):
        """After normalisation the direction (ratio of components) is unchanged."""
        v = make_vec("a", [3.0, 4.0])
        n = v.normalize()
        assert math.isclose(n.vector[0] / n.vector[1], 3.0 / 4.0, rel_tol=1e-9)

    def test_normalize_idempotent(self):
        v = make_vec("a", [2.0, 3.0, 6.0])
        n1 = v.normalize()
        n2 = n1.normalize()
        for a, b in zip(n1.vector, n2.vector):
            assert math.isclose(a, b, rel_tol=1e-9)


class TestEmbeddingVectorDot:
    def test_dot_orthogonal_zero(self):
        a = make_vec("a", [1.0, 0.0])
        b = make_vec("b", [0.0, 1.0])
        assert math.isclose(a.dot(b), 0.0)

    def test_dot_parallel(self):
        a = make_vec("a", [1.0, 0.0])
        b = make_vec("b", [2.0, 0.0])
        assert math.isclose(a.dot(b), 2.0)

    def test_dot_commutative(self):
        a = make_vec("a", [1.0, 2.0, 3.0])
        b = make_vec("b", [4.0, 5.0, 6.0])
        assert math.isclose(a.dot(b), b.dot(a))

    def test_dot_known_value(self):
        a = make_vec("a", [1.0, 2.0, 3.0])
        b = make_vec("b", [4.0, 5.0, 6.0])
        assert math.isclose(a.dot(b), 32.0)

    def test_dot_negative(self):
        a = make_vec("a", [1.0, 0.0])
        b = make_vec("b", [-1.0, 0.0])
        assert math.isclose(a.dot(b), -1.0)

    def test_dot_self(self):
        v = make_vec("a", [3.0, 4.0])
        assert math.isclose(v.dot(v), v.norm() ** 2)


class TestEmbeddingVectorCosineSimilarity:
    def test_cosine_identical_unit_vectors(self):
        a = make_vec("a", [1.0, 0.0])
        b = make_vec("b", [1.0, 0.0])
        assert math.isclose(a.cosine_similarity(b), 1.0)

    def test_cosine_orthogonal_zero(self):
        a = make_vec("a", [1.0, 0.0])
        b = make_vec("b", [0.0, 1.0])
        assert math.isclose(a.cosine_similarity(b), 0.0, abs_tol=1e-9)

    def test_cosine_anti_parallel(self):
        a = make_vec("a", [1.0, 0.0])
        b = make_vec("b", [-1.0, 0.0])
        assert math.isclose(a.cosine_similarity(b), -1.0)

    def test_cosine_scale_invariant(self):
        a = make_vec("a", [1.0, 1.0])
        b = make_vec("b", [10.0, 10.0])
        assert math.isclose(a.cosine_similarity(b), 1.0)

    def test_cosine_zero_vector_returns_zero(self):
        a = make_vec("a", [0.0, 0.0])
        b = make_vec("b", [1.0, 1.0])
        assert a.cosine_similarity(b) == 0.0

    def test_cosine_both_zero_vectors_returns_zero(self):
        a = make_vec("a", [0.0, 0.0])
        b = make_vec("b", [0.0, 0.0])
        assert a.cosine_similarity(b) == 0.0

    def test_cosine_symmetric(self):
        a = make_vec("a", [1.0, 2.0])
        b = make_vec("b", [3.0, 1.0])
        assert math.isclose(a.cosine_similarity(b), b.cosine_similarity(a))

    def test_cosine_range(self):
        a = make_vec("a", [1.0, 2.0, 3.0])
        b = make_vec("b", [-3.0, 1.0, 0.5])
        sim = a.cosine_similarity(b)
        assert -1.0 <= sim <= 1.0

    def test_cosine_parallel_non_unit(self):
        a = make_vec("a", [3.0, 4.0])
        b = make_vec("b", [6.0, 8.0])
        assert math.isclose(a.cosine_similarity(b), 1.0)


class TestEmbeddingVectorDataclass:
    def test_default_metadata_is_dict(self):
        v = EmbeddingVector(doc_id="a", vector=[1.0])
        assert isinstance(v.metadata, dict)

    def test_default_metadata_independent(self):
        v1 = EmbeddingVector(doc_id="a", vector=[1.0])
        v2 = EmbeddingVector(doc_id="b", vector=[2.0])
        v1.metadata["k"] = "v"
        assert "k" not in v2.metadata

    def test_created_at_auto_set(self):
        before = time.time()
        v = EmbeddingVector(doc_id="a", vector=[1.0])
        after = time.time()
        assert before <= v.created_at <= after

    def test_created_at_custom(self):
        v = EmbeddingVector(doc_id="a", vector=[1.0], created_at=999.0)
        assert v.created_at == 999.0


# ===========================================================================
# StoreConfig tests
# ===========================================================================

class TestStoreConfig:
    def test_defaults(self):
        cfg = StoreConfig()
        assert cfg.dimension == 128
        assert cfg.metric == "cosine"
        assert cfg.normalize_on_add is True

    def test_custom_config(self):
        cfg = StoreConfig(dimension=64, metric="dot", normalize_on_add=False)
        assert cfg.dimension == 64
        assert cfg.metric == "dot"
        assert cfg.normalize_on_add is False


# ===========================================================================
# EmbeddingStore tests
# ===========================================================================

class TestEmbeddingStoreBasic:
    def test_initial_size_zero(self):
        store = EmbeddingStore()
        assert store.size() == 0

    def test_add_and_size(self):
        store = EmbeddingStore(StoreConfig(dimension=2))
        store.add(make_vec("a", [1.0, 0.0]))
        assert store.size() == 1

    def test_add_multiple(self):
        store = EmbeddingStore(StoreConfig(dimension=2))
        for i in range(5):
            store.add(make_vec(f"doc{i}", [float(i), float(i)]))
        assert store.size() == 5

    def test_add_replaces_existing(self):
        store = EmbeddingStore(StoreConfig(dimension=2, normalize_on_add=False))
        store.add(make_vec("a", [1.0, 0.0]))
        store.add(make_vec("a", [0.0, 1.0]))
        assert store.size() == 1
        assert store.get("a").vector == [0.0, 1.0]

    def test_get_existing(self):
        store = EmbeddingStore(StoreConfig(dimension=2, normalize_on_add=False))
        v = make_vec("x", [1.0, 2.0])
        store.add(v)
        got = store.get("x")
        assert got is not None
        assert got.doc_id == "x"

    def test_get_nonexistent_returns_none(self):
        store = EmbeddingStore(StoreConfig(dimension=2))
        assert store.get("missing") is None

    def test_remove_existing(self):
        store = EmbeddingStore(StoreConfig(dimension=2))
        store.add(make_vec("a", [1.0, 0.0]))
        assert store.remove("a") is True
        assert store.size() == 0

    def test_remove_nonexistent_returns_false(self):
        store = EmbeddingStore(StoreConfig(dimension=2))
        assert store.remove("ghost") is False

    def test_remove_then_get_is_none(self):
        store = EmbeddingStore(StoreConfig(dimension=2))
        store.add(make_vec("a", [1.0, 0.0]))
        store.remove("a")
        assert store.get("a") is None

    def test_all_ids_empty(self):
        store = EmbeddingStore(StoreConfig(dimension=2))
        assert store.all_ids() == []

    def test_all_ids_reflects_added(self):
        store = EmbeddingStore(StoreConfig(dimension=2))
        store.add(make_vec("a", [1.0, 0.0]))
        store.add(make_vec("b", [0.0, 1.0]))
        assert set(store.all_ids()) == {"a", "b"}

    def test_clear_empties_store(self):
        store = EmbeddingStore(StoreConfig(dimension=2))
        store.add(make_vec("a", [1.0, 0.0]))
        store.add(make_vec("b", [0.0, 1.0]))
        store.clear()
        assert store.size() == 0
        assert store.all_ids() == []

    def test_clear_then_get_none(self):
        store = EmbeddingStore(StoreConfig(dimension=2))
        store.add(make_vec("a", [1.0, 0.0]))
        store.clear()
        assert store.get("a") is None


class TestEmbeddingStoreDimensionCheck:
    def test_dimension_mismatch_raises(self):
        store = EmbeddingStore(StoreConfig(dimension=3))
        with pytest.raises(ValueError):
            store.add(make_vec("bad", [1.0, 2.0]))  # dim=2, not 3

    def test_dimension_correct_no_error(self):
        store = EmbeddingStore(StoreConfig(dimension=2))
        store.add(make_vec("ok", [1.0, 2.0]))  # should not raise

    def test_dimension_mismatch_message(self):
        store = EmbeddingStore(StoreConfig(dimension=4))
        with pytest.raises(ValueError, match="dimension"):
            store.add(make_vec("bad", [1.0]))


class TestEmbeddingStoreNormalizeOnAdd:
    def test_normalize_on_add_true(self):
        cfg = StoreConfig(dimension=2, normalize_on_add=True)
        store = EmbeddingStore(cfg)
        store.add(make_vec("a", [3.0, 4.0]))
        stored = store.get("a")
        assert math.isclose(stored.norm(), 1.0, rel_tol=1e-9)

    def test_normalize_on_add_false(self):
        cfg = StoreConfig(dimension=2, normalize_on_add=False)
        store = EmbeddingStore(cfg)
        store.add(make_vec("a", [3.0, 4.0]))
        stored = store.get("a")
        assert math.isclose(stored.norm(), 5.0)


class TestEmbeddingStoreSearch:
    def _make_store(self, metric: str = "cosine", normalize: bool = True) -> EmbeddingStore:
        cfg = StoreConfig(dimension=2, metric=metric, normalize_on_add=normalize)
        store = EmbeddingStore(cfg)
        return store

    def test_search_empty_returns_empty(self):
        store = self._make_store()
        results = store.search(make_vec("q", [1.0, 0.0]))
        assert results == []

    def test_search_single_match(self):
        store = self._make_store()
        store.add(make_vec("a", [1.0, 0.0]))
        results = store.search(make_vec("q", [1.0, 0.0]))
        assert len(results) == 1
        assert results[0][0] == "a"

    def test_search_returns_doc_id_score_tuples(self):
        store = self._make_store()
        store.add(make_vec("a", [1.0, 0.0]))
        results = store.search(make_vec("q", [1.0, 0.0]))
        doc_id, score = results[0]
        assert isinstance(doc_id, str)
        assert isinstance(score, float)

    def test_search_cosine_identical_score_one(self):
        store = self._make_store(metric="cosine")
        store.add(make_vec("a", [1.0, 0.0]))
        results = store.search(make_vec("q", [1.0, 0.0]))
        assert math.isclose(results[0][1], 1.0, rel_tol=1e-9)

    def test_search_cosine_orthogonal_score_zero(self):
        store = self._make_store(metric="cosine")
        store.add(make_vec("a", [1.0, 0.0]))
        results = store.search(make_vec("q", [0.0, 1.0]))
        assert math.isclose(results[0][1], 0.0, abs_tol=1e-9)

    def test_search_sorted_descending(self):
        store = self._make_store(metric="cosine")
        # doc_a perfectly aligned with query; doc_b orthogonal; doc_c at 45°
        store.add(make_vec("doc_a", [1.0, 0.0]))
        store.add(make_vec("doc_b", [0.0, 1.0]))
        store.add(make_vec("doc_c", [1.0, 1.0]))
        results = store.search(make_vec("q", [1.0, 0.0]))
        scores = [s for _, s in results]
        assert scores == sorted(scores, reverse=True)

    def test_search_most_similar_first(self):
        store = self._make_store(metric="cosine")
        store.add(make_vec("best", [1.0, 0.0]))
        store.add(make_vec("middle", [1.0, 1.0]))
        store.add(make_vec("worst", [0.0, 1.0]))
        results = store.search(make_vec("q", [1.0, 0.0]))
        assert results[0][0] == "best"

    def test_search_top_k_limits_results(self):
        store = self._make_store()
        for i in range(10):
            store.add(make_vec(f"doc{i}", [float(i + 1), 0.0]))
        results = store.search(make_vec("q", [1.0, 0.0]), top_k=3)
        assert len(results) == 3

    def test_search_top_k_larger_than_size_returns_all(self):
        store = self._make_store()
        store.add(make_vec("a", [1.0, 0.0]))
        store.add(make_vec("b", [0.0, 1.0]))
        results = store.search(make_vec("q", [1.0, 0.0]), top_k=100)
        assert len(results) == 2

    def test_search_default_top_k(self):
        store = self._make_store()
        for i in range(15):
            store.add(make_vec(f"doc{i}", [float(i + 1), 0.0]))
        results = store.search(make_vec("q", [1.0, 0.0]))
        assert len(results) == 10


class TestEmbeddingStoreMetric:
    """Verify that cosine and dot metrics can give different rankings."""

    def test_cosine_vs_dot_different_rankings(self):
        # doc_a: small magnitude, perfectly aligned with query
        # doc_b: large magnitude, slightly off-angle
        # For cosine, doc_a should score higher (direction match).
        # For dot product (no normalisation), doc_b may score higher.
        cfg_cosine = StoreConfig(dimension=2, metric="cosine", normalize_on_add=False)
        store_cos = EmbeddingStore(cfg_cosine)
        store_cos.add(make_vec("doc_a", [1.0, 0.0]))      # perfectly aligned, small
        store_cos.add(make_vec("doc_b", [100.0, 50.0]))   # off-angle, large

        cfg_dot = StoreConfig(dimension=2, metric="dot", normalize_on_add=False)
        store_dot = EmbeddingStore(cfg_dot)
        store_dot.add(make_vec("doc_a", [1.0, 0.0]))
        store_dot.add(make_vec("doc_b", [100.0, 50.0]))

        query = make_vec("q", [1.0, 0.0])

        cosine_top = store_cos.search(query)[0][0]
        dot_top = store_dot.search(query)[0][0]

        # Cosine: doc_a (cos=1.0) beats doc_b (cos<1)
        assert cosine_top == "doc_a"
        # Dot: doc_b (dot=100) beats doc_a (dot=1)
        assert dot_top == "doc_b"

    def test_dot_metric_unknown_raises(self):
        cfg = StoreConfig(dimension=2, metric="euclidean", normalize_on_add=False)
        store = EmbeddingStore(cfg)
        store.add(make_vec("a", [1.0, 0.0]))
        with pytest.raises(ValueError, match="metric"):
            store.search(make_vec("q", [1.0, 0.0]))


# ===========================================================================
# EmbeddingPersistence tests
# ===========================================================================

class TestEmbeddingPersistence:
    def _make_store(self) -> EmbeddingStore:
        cfg = StoreConfig(dimension=3, metric="cosine", normalize_on_add=True)
        store = EmbeddingStore(cfg)
        store.add(make_vec("alpha", [1.0, 0.0, 0.0], metadata={"lang": "en"}))
        store.add(make_vec("beta",  [0.0, 1.0, 0.0]))
        store.add(make_vec("gamma", [0.0, 0.0, 1.0]))
        return store

    def test_save_creates_file(self):
        store = self._make_store()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            EmbeddingPersistence.save(store, path)
            assert os.path.exists(path)
        finally:
            os.unlink(path)

    def test_save_produces_valid_json(self):
        store = self._make_store()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            EmbeddingPersistence.save(store, path)
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            assert isinstance(data, dict)
        finally:
            os.unlink(path)

    def test_roundtrip_size(self):
        store = self._make_store()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            EmbeddingPersistence.save(store, path)
            loaded = EmbeddingPersistence.load(path)
            assert loaded.size() == store.size()
        finally:
            os.unlink(path)

    def test_roundtrip_config_dimension(self):
        store = self._make_store()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            EmbeddingPersistence.save(store, path)
            loaded = EmbeddingPersistence.load(path)
            assert loaded._config.dimension == 3
        finally:
            os.unlink(path)

    def test_roundtrip_config_metric(self):
        store = self._make_store()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            EmbeddingPersistence.save(store, path)
            loaded = EmbeddingPersistence.load(path)
            assert loaded._config.metric == "cosine"
        finally:
            os.unlink(path)

    def test_roundtrip_doc_ids(self):
        store = self._make_store()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            EmbeddingPersistence.save(store, path)
            loaded = EmbeddingPersistence.load(path)
            assert set(loaded.all_ids()) == {"alpha", "beta", "gamma"}
        finally:
            os.unlink(path)

    def test_roundtrip_vectors_preserved(self):
        cfg = StoreConfig(dimension=2, normalize_on_add=False)
        store = EmbeddingStore(cfg)
        store.add(make_vec("v", [0.6, 0.8]))
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            EmbeddingPersistence.save(store, path)
            loaded = EmbeddingPersistence.load(path)
            got = loaded.get("v")
            assert math.isclose(got.vector[0], 0.6)
            assert math.isclose(got.vector[1], 0.8)
        finally:
            os.unlink(path)

    def test_roundtrip_metadata_preserved(self):
        store = self._make_store()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            EmbeddingPersistence.save(store, path)
            loaded = EmbeddingPersistence.load(path)
            assert loaded.get("alpha").metadata == {"lang": "en"}
        finally:
            os.unlink(path)

    def test_roundtrip_created_at(self):
        ts = 42000.0
        v = EmbeddingVector(doc_id="t", vector=[1.0, 0.0, 0.0], created_at=ts)
        cfg = StoreConfig(dimension=3, normalize_on_add=False)
        store = EmbeddingStore(cfg)
        store.add(v)
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            EmbeddingPersistence.save(store, path)
            loaded = EmbeddingPersistence.load(path)
            assert loaded.get("t").created_at == ts
        finally:
            os.unlink(path)

    def test_search_works_after_load(self):
        store = self._make_store()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            EmbeddingPersistence.save(store, path)
            loaded = EmbeddingPersistence.load(path)
            results = loaded.search(make_vec("q", [1.0, 0.0, 0.0]))
            assert results[0][0] == "alpha"
        finally:
            os.unlink(path)

    def test_search_ranking_after_load(self):
        store = self._make_store()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            EmbeddingPersistence.save(store, path)
            loaded = EmbeddingPersistence.load(path)
            results = loaded.search(make_vec("q", [0.0, 1.0, 0.0]))
            assert results[0][0] == "beta"
        finally:
            os.unlink(path)

    def test_save_accepts_path_object(self):
        store = self._make_store()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "store.json"
            EmbeddingPersistence.save(store, path)
            assert path.exists()

    def test_load_accepts_path_object(self):
        store = self._make_store()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "store.json"
            EmbeddingPersistence.save(store, path)
            loaded = EmbeddingPersistence.load(path)
            assert loaded.size() == 3

    def test_roundtrip_dot_metric(self):
        cfg = StoreConfig(dimension=2, metric="dot", normalize_on_add=False)
        store = EmbeddingStore(cfg)
        store.add(make_vec("a", [1.0, 2.0]))
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            EmbeddingPersistence.save(store, path)
            loaded = EmbeddingPersistence.load(path)
            assert loaded._config.metric == "dot"
        finally:
            os.unlink(path)

    def test_empty_store_roundtrip(self):
        cfg = StoreConfig(dimension=4)
        store = EmbeddingStore(cfg)
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            EmbeddingPersistence.save(store, path)
            loaded = EmbeddingPersistence.load(path)
            assert loaded.size() == 0
        finally:
            os.unlink(path)

    def test_schema_version_present(self):
        store = self._make_store()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            EmbeddingPersistence.save(store, path)
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            assert "schema_version" in data
        finally:
            os.unlink(path)


# ===========================================================================
# Edge-case / integration tests
# ===========================================================================

class TestEdgeCases:
    def test_remove_from_empty_store(self):
        store = EmbeddingStore(StoreConfig(dimension=3))
        assert store.remove("nonexistent") is False

    def test_search_empty_store_no_error(self):
        store = EmbeddingStore(StoreConfig(dimension=3))
        assert store.search(make_vec("q", [1.0, 0.0, 0.0])) == []

    def test_search_top_k_zero(self):
        store = EmbeddingStore(StoreConfig(dimension=2))
        store.add(make_vec("a", [1.0, 0.0]))
        results = store.search(make_vec("q", [1.0, 0.0]), top_k=0)
        assert results == []

    def test_search_top_k_exceeds_size_returns_all(self):
        store = EmbeddingStore(StoreConfig(dimension=2))
        store.add(make_vec("a", [1.0, 0.0]))
        store.add(make_vec("b", [0.0, 1.0]))
        results = store.search(make_vec("q", [1.0, 0.0]), top_k=999)
        assert len(results) == 2

    def test_add_after_clear_works(self):
        store = EmbeddingStore(StoreConfig(dimension=2))
        store.add(make_vec("a", [1.0, 0.0]))
        store.clear()
        store.add(make_vec("b", [0.0, 1.0]))
        assert store.size() == 1
        assert store.get("b") is not None

    def test_high_dimensional_store(self):
        dim = 512
        cfg = StoreConfig(dimension=dim)
        store = EmbeddingStore(cfg)
        for i in range(20):
            v = [0.0] * dim
            v[i] = 1.0
            store.add(make_vec(f"doc{i}", v))
        query_v = [0.0] * dim
        query_v[0] = 1.0
        results = store.search(make_vec("q", query_v), top_k=1)
        assert results[0][0] == "doc0"

    def test_metadata_not_shared_between_copies(self):
        v = make_vec("a", [1.0, 2.0], metadata={"key": "val"})
        n = v.normalize()
        n.metadata["extra"] = "new"
        assert "extra" not in v.metadata

    def test_store_default_config(self):
        store = EmbeddingStore()
        assert store._config.dimension == 128
