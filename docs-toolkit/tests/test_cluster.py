"""Тесты cluster + dedup."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.embeddings.cluster import (
    cosine, kmeans, detect_duplicates, find_near_duplicates_in_clusters,
    Cluster,
)


def test_cosine_sparse():
    a = {"x": 1.0, "y": 0.5}
    assert cosine(a, a) == pytest.approx(1.0)
    b = {"z": 1.0}
    assert cosine(a, b) == 0.0


def test_cosine_dense():
    a = [1.0, 0.0, 0.0]
    assert cosine(a, a) == pytest.approx(1.0)
    b = [0.0, 1.0, 0.0]
    assert cosine(a, b) == 0.0


def test_cosine_empty():
    assert cosine({}, {"x": 1}) == 0.0
    assert cosine([], [1, 2]) == 0.0


def test_kmeans_groups_similar():
    items = [
        ("a1", {"cat": 1.0, "animal": 0.5}),
        ("a2", {"cat": 0.9, "animal": 0.4}),
        ("b1", {"car": 1.0, "engine": 0.5}),
        ("b2", {"car": 0.95, "engine": 0.6}),
    ]
    clusters = kmeans(items, k=2, seed=42)
    assert len(clusters) == 2

    # Similar items должны быть в одном кластере
    cluster_of = {}
    for c in clusters:
        for m in c.members:
            cluster_of[m] = c.id
    assert cluster_of["a1"] == cluster_of["a2"]
    assert cluster_of["b1"] == cluster_of["b2"]
    assert cluster_of["a1"] != cluster_of["b1"]


def test_kmeans_dense_vectors():
    items = [
        ("v1", [1.0, 0.0, 0.0]),
        ("v2", [0.9, 0.1, 0.0]),
        ("v3", [0.0, 0.0, 1.0]),
    ]
    clusters = kmeans(items, k=2, seed=42)
    assert len(clusters) == 2


def test_kmeans_too_few_items():
    items = [("a", {"x": 1})]
    assert kmeans(items, k=5) == []


def test_detect_duplicates():
    items = [
        ("a", {"x": 1.0, "y": 0.5}),
        ("b", {"x": 1.0, "y": 0.5}),  # точный дубль
        ("c", {"z": 1.0}),
    ]
    dups = detect_duplicates(items, threshold=0.9)
    assert len(dups) == 1
    assert {dups[0][0], dups[0][1]} == {"a", "b"}
    assert dups[0][2] == pytest.approx(1.0)


def test_detect_duplicates_no_match():
    items = [
        ("a", {"x": 1.0}),
        ("b", {"y": 1.0}),
    ]
    dups = detect_duplicates(items, threshold=0.5)
    assert dups == []


def test_find_near_duplicates_in_clusters():
    cluster = Cluster(id=0, members=["a", "b", "c"], centroid={}, size=3)
    id_to_vec = {
        "a": {"x": 1.0},
        "b": {"x": 0.95},
        "c": {"y": 1.0},
    }
    dups = find_near_duplicates_in_clusters([cluster], id_to_vec, threshold=0.9)
    assert len(dups) == 1
    assert {dups[0][0], dups[0][1]} == {"a", "b"}
