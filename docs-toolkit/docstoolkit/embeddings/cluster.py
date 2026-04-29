"""Кластеризация и детекция дубликатов через embeddings.

Без зависимостей: реализован K-means++ с cosine distance для sparse и dense vectors.
"""
import math
import random
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Cluster:
    """Один кластер: id, центроид, члены."""
    id: int
    members: list[str]              # doc_ids
    centroid: dict | list           # sparse dict или dense list
    size: int = 0


def _cosine_sparse(a: dict, b: dict) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    if not common:
        return 0.0
    dot = sum(a[t] * b[t] for t in common)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _cosine_dense(a: list, b: list) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def cosine(a, b) -> float:
    """Универсальный cosine для sparse (dict) или dense (list)."""
    if isinstance(a, dict):
        return _cosine_sparse(a, b)
    return _cosine_dense(a, b)


def _cluster_centroid(vectors: list, is_sparse: bool):
    """Среднее по векторам: для sparse — sum по common keys, для dense — поэлементно."""
    if not vectors:
        return {} if is_sparse else []
    if is_sparse:
        sums: dict[str, float] = defaultdict(float)
        for v in vectors:
            for k, val in v.items():
                sums[k] += val
        n = len(vectors)
        return {k: v / n for k, v in sums.items()}
    # dense
    n = len(vectors)
    dim = len(vectors[0])
    return [sum(v[i] for v in vectors) / n for i in range(dim)]


def kmeans(items: list[tuple[str, dict | list]],
           k: int = 5,
           max_iter: int = 30,
           seed: int = 42) -> list[Cluster]:
    """K-means++ с cosine distance.

    items: [(doc_id, vector), ...] где vector — dict или list
    """
    if k < 1 or len(items) < k:
        return []

    is_sparse = isinstance(items[0][1], dict)
    rng = random.Random(seed)

    # K-means++ init: первый рандомный, далее с вероятностью ∝ d²
    centroids = [items[rng.randint(0, len(items) - 1)][1]]
    for _ in range(k - 1):
        weights = []
        for _id, vec in items:
            min_d = min(1 - cosine(vec, c) for c in centroids)
            weights.append(min_d ** 2)
        total = sum(weights) or 1
        target = rng.random() * total
        cum = 0.0
        for (_id, vec), w in zip(items, weights):
            cum += w
            if cum >= target:
                centroids.append(vec)
                break

    # Iterate
    assignments: list[int] = [0] * len(items)
    for it in range(max_iter):
        changed = False
        for i, (_id, vec) in enumerate(items):
            sims = [cosine(vec, c) for c in centroids]
            new_assign = sims.index(max(sims))
            if new_assign != assignments[i]:
                assignments[i] = new_assign
                changed = True

        # Recompute centroids
        for c_idx in range(k):
            cluster_vecs = [vec for (_id, vec), a in zip(items, assignments) if a == c_idx]
            if cluster_vecs:
                centroids[c_idx] = _cluster_centroid(cluster_vecs, is_sparse)

        if not changed and it > 0:
            break

    # Build clusters
    clusters: list[Cluster] = []
    for c_idx in range(k):
        members = [doc_id for (doc_id, _), a in zip(items, assignments) if a == c_idx]
        clusters.append(Cluster(
            id=c_idx,
            members=members,
            centroid=centroids[c_idx],
            size=len(members),
        ))
    return clusters


def detect_duplicates(items: list[tuple[str, dict | list]],
                      threshold: float = 0.92) -> list[tuple[str, str, float]]:
    """Возвращает [(id_a, id_b, similarity)] пар с похожестью ≥ threshold.

    O(n²) — для малых корпусов или после кластеризации.
    """
    pairs: list[tuple[str, str, float]] = []
    n = len(items)
    for i in range(n):
        for j in range(i + 1, n):
            sim = cosine(items[i][1], items[j][1])
            if sim >= threshold:
                pairs.append((items[i][0], items[j][0], sim))
    return sorted(pairs, key=lambda p: -p[2])


def find_near_duplicates_in_clusters(clusters: list[Cluster],
                                     id_to_vec: dict,
                                     threshold: float = 0.92
                                     ) -> list[tuple[str, str, float]]:
    """Дубли только внутри кластеров (быстрее чем full O(n²))."""
    pairs: list[tuple[str, str, float]] = []
    for cl in clusters:
        cluster_items = [(m, id_to_vec[m]) for m in cl.members if m in id_to_vec]
        pairs.extend(detect_duplicates(cluster_items, threshold))
    return sorted(pairs, key=lambda p: -p[2])
