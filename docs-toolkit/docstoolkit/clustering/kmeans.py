"""K-Means clustering over TF-IDF document features (E20)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from docstoolkit.clustering.features import DocumentFeatures
from docstoolkit.clustering.distance import cosine_distance


@dataclass
class Cluster:
    """A single cluster produced by K-Means."""

    cluster_id: int
    doc_ids: list[str]
    centroid: dict[str, float]

    def size(self) -> int:
        """Number of documents in this cluster."""
        return len(self.doc_ids)


@dataclass
class KMeansConfig:
    """Configuration for K-Means clustering."""

    k: int = 5
    max_iter: int = 20
    random_seed: int = 42


@dataclass
class KMeansResult:
    """Result produced by :class:`KMeansClustering`."""

    clusters: list[Cluster]
    iterations: int
    converged: bool

    def cluster_for(self, doc_id: str) -> Optional[int]:
        """Return the cluster_id that contains *doc_id*, or None."""
        for cluster in self.clusters:
            if doc_id in cluster.doc_ids:
                return cluster.cluster_id
        return None

    def largest_cluster(self) -> Cluster:
        """Return the cluster with the most documents."""
        return max(self.clusters, key=lambda c: c.size())

    def smallest_cluster(self) -> Cluster:
        """Return the cluster with the fewest documents."""
        return min(self.clusters, key=lambda c: c.size())


def _mean_centroid(vectors: list[dict[str, float]]) -> dict[str, float]:
    """Compute the mean of a list of TF-IDF vectors (element-wise average)."""
    if not vectors:
        return {}
    total: dict[str, float] = {}
    for vec in vectors:
        for term, val in vec.items():
            total[term] = total.get(term, 0.0) + val
    n = len(vectors)
    return {term: val / n for term, val in total.items()}


class KMeansClustering:
    """K-Means clustering using cosine distance on TF-IDF vectors."""

    def fit(
        self,
        features: list[DocumentFeatures],
        config: Optional[KMeansConfig] = None,
    ) -> KMeansResult:
        """Cluster *features* and return a :class:`KMeansResult`.

        Centroids are initialised by picking *k* evenly-spaced documents from
        the feature list (deterministic, no randomness).
        """
        if config is None:
            config = KMeansConfig()

        n = len(features)
        k = min(config.k, n)  # can't have more clusters than documents

        if n == 0:
            return KMeansResult(clusters=[], iterations=0, converged=True)

        # --- Initialise centroids (evenly spaced indices) ---
        if k == 1:
            indices = [0]
        else:
            step = max(1, (n - 1) // (k - 1))
            indices = [min(i * step, n - 1) for i in range(k)]
            # Deduplicate while preserving order (edge case: very small n).
            seen: set[int] = set()
            unique: list[int] = []
            for idx in indices:
                if idx not in seen:
                    seen.add(idx)
                    unique.append(idx)
            indices = unique
            k = len(indices)

        centroids: list[dict[str, float]] = [
            dict(features[i].tfidf) for i in indices
        ]

        assignments: list[int] = [0] * n
        converged = False
        iterations = 0

        for iteration in range(config.max_iter):
            iterations += 1

            # --- Assignment step ---
            new_assignments: list[int] = []
            for feat in features:
                best_cluster = 0
                best_dist = float("inf")
                for cid, centroid in enumerate(centroids):
                    dist = cosine_distance(feat.tfidf, centroid)
                    if dist < best_dist:
                        best_dist = dist
                        best_cluster = cid
                new_assignments.append(best_cluster)

            # Check convergence.
            if new_assignments == assignments:
                converged = True
                break
            assignments = new_assignments

            # --- Update step ---
            groups: list[list[dict[str, float]]] = [[] for _ in range(k)]
            for feat, cid in zip(features, assignments):
                groups[cid].append(feat.tfidf)

            new_centroids: list[dict[str, float]] = []
            for cid, group in enumerate(groups):
                if group:
                    new_centroids.append(_mean_centroid(group))
                else:
                    # Keep old centroid if cluster became empty.
                    new_centroids.append(centroids[cid])
            centroids = new_centroids

        # --- Build Cluster objects ---
        group_doc_ids: list[list[str]] = [[] for _ in range(k)]
        for feat, cid in zip(features, assignments):
            group_doc_ids[cid].append(feat.doc_id)

        clusters = [
            Cluster(
                cluster_id=cid,
                doc_ids=group_doc_ids[cid],
                centroid=centroids[cid],
            )
            for cid in range(k)
        ]

        return KMeansResult(
            clusters=clusters,
            iterations=iterations,
            converged=converged,
        )
