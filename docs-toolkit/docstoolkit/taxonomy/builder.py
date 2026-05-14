"""Build emergent taxonomy via TF-IDF k-means++ clustering (pure stdlib)."""
import re
import math
import random
import uuid
from dataclasses import dataclass

from docstoolkit.taxonomy.node import TaxonomyNode, TaxonomyTree


@dataclass
class TaxonomyConfig:
    n_clusters: int = 8
    min_docs_per_cluster: int = 1
    top_terms_per_label: int = 3
    seed: int = 42
    max_label_words: int = 5


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> list[str]:
    """Lowercase words >= 3 chars."""
    return [w for w in re.findall(r"[a-zA-Zа-яА-ЯёЁ]+", text.lower()) if len(w) >= 3]


def _tfidf_vectors(docs: dict[str, str]) -> dict[str, dict[str, float]]:
    """Compute TF-IDF for each doc. Returns {doc_id: {term: score}}.

    TF  = term count / doc length
    IDF = log(N / df)  where df = number of docs containing the term
    """
    N = len(docs)
    if N == 0:
        return {}

    # Build term frequencies per doc
    tf_raw: dict[str, dict[str, int]] = {}
    df: dict[str, int] = {}

    for doc_id, text in docs.items():
        tokens = _tokenize(text)
        counts: dict[str, int] = {}
        for tok in tokens:
            counts[tok] = counts.get(tok, 0) + 1
        tf_raw[doc_id] = counts
        for term in counts:
            df[term] = df.get(term, 0) + 1

    vectors: dict[str, dict[str, float]] = {}
    for doc_id, counts in tf_raw.items():
        doc_len = sum(counts.values()) or 1
        vec: dict[str, float] = {}
        for term, cnt in counts.items():
            tf = cnt / doc_len
            idf = math.log(N / df[term])
            score = tf * idf
            if score > 0:
                vec[term] = score
        vectors[doc_id] = vec

    return vectors


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    """Cosine similarity between two TF-IDF sparse vectors."""
    if not a or not b:
        return 0.0
    dot = sum(a[t] * b[t] for t in a if t in b)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _kmeans_plus_plus_seeds(
    vectors: dict[str, dict[str, float]],
    k: int,
    rng: random.Random,
) -> list[str]:
    """k-means++ seed selection. Returns k doc_ids as initial centroids."""
    doc_ids = list(vectors.keys())
    if not doc_ids:
        return []

    # Pick first centroid uniformly at random
    seeds: list[str] = [rng.choice(doc_ids)]

    while len(seeds) < k:
        # Compute D^2 distance from nearest existing seed for each point
        distances: list[float] = []
        for did in doc_ids:
            min_sim = max(_cosine(vectors[did], vectors[s]) for s in seeds)
            # distance = 1 - similarity (higher distance = farther from seeds)
            dist = max(0.0, 1.0 - min_sim)
            distances.append(dist)

        total = sum(distances)
        if total == 0:
            # All points coincide with existing seeds — just pick any remaining
            remaining = [d for d in doc_ids if d not in seeds]
            if remaining:
                seeds.append(rng.choice(remaining))
            else:
                break
            continue

        # Weighted random selection proportional to D^2
        r = rng.random() * total
        cumulative = 0.0
        chosen = doc_ids[-1]
        for did, dist in zip(doc_ids, distances):
            cumulative += dist
            if cumulative >= r:
                chosen = did
                break
        seeds.append(chosen)

    return seeds


def _assign_clusters(
    vectors: dict[str, dict[str, float]],
    centroids: list[dict[str, float]],
) -> list[int]:
    """Assign each doc to nearest centroid. Returns list of cluster indices."""
    assignments: list[int] = []
    doc_ids = list(vectors.keys())
    for did in doc_ids:
        best_idx = 0
        best_sim = -1.0
        for i, centroid in enumerate(centroids):
            sim = _cosine(vectors[did], centroid)
            if sim > best_sim:
                best_sim = sim
                best_idx = i
        assignments.append(best_idx)
    return assignments


def _compute_centroid(
    doc_ids: list[str],
    vectors: dict[str, dict[str, float]],
) -> dict[str, float]:
    """Average TF-IDF vector for a set of docs."""
    if not doc_ids:
        return {}
    centroid: dict[str, float] = {}
    n = len(doc_ids)
    for did in doc_ids:
        for term, score in vectors[did].items():
            centroid[term] = centroid.get(term, 0.0) + score / n
    return centroid


def _top_terms(centroid: dict[str, float], n: int = 3) -> list[str]:
    """Top-n terms by TF-IDF score in centroid."""
    return [t for t, _ in sorted(centroid.items(), key=lambda x: -x[1])[:n]]


def _cluster_cohesion(
    doc_ids: list[str],
    vectors: dict[str, dict[str, float]],
) -> float:
    """Average pairwise cosine similarity within cluster."""
    if len(doc_ids) <= 1:
        return 1.0
    total = 0.0
    count = 0
    for i in range(len(doc_ids)):
        for j in range(i + 1, len(doc_ids)):
            total += _cosine(vectors[doc_ids[i]], vectors[doc_ids[j]])
            count += 1
    return total / count if count > 0 else 1.0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_taxonomy(
    docs: dict[str, str],
    config: TaxonomyConfig | None = None,
) -> TaxonomyTree:
    """Build taxonomy from documents using k-means++ TF-IDF clustering.

    Algorithm:
    1. Compute TF-IDF vectors for all docs
    2. If len(docs) <= n_clusters: each doc is its own cluster
    3. k-means++ seeds → iterate k-means 10 times:
       a. assign_clusters
       b. recompute centroids
    4. For each non-empty cluster:
       - top_terms = _top_terms(centroid, top_terms_per_label)
       - label = " / ".join(top_terms[:max_label_words])
       - cohesion = _cluster_cohesion(cluster_docs, vectors)
    5. Build TaxonomyNode for each cluster (id = uuid4)
    6. Return TaxonomyTree(nodes)

    Edge cases:
    - Empty docs → TaxonomyTree([])
    - Single doc → single node
    - n_clusters > len(docs): reduce to len(docs)
    """
    if config is None:
        config = TaxonomyConfig()

    if not docs:
        return TaxonomyTree([])

    vectors = _tfidf_vectors(docs)
    doc_ids = list(docs.keys())
    n = len(doc_ids)

    rng = random.Random(config.seed)

    # Each doc its own cluster when docs <= n_clusters
    if n <= config.n_clusters:
        nodes: list[TaxonomyNode] = []
        for did in doc_ids:
            vec = vectors[did]
            terms = _top_terms(vec, config.top_terms_per_label)
            label = " / ".join(terms[:config.max_label_words]) if terms else did
            node = TaxonomyNode(
                id=str(uuid.uuid4()),
                label=label,
                doc_ids=[did],
                top_terms=terms,
                cohesion=1.0,
            )
            nodes.append(node)
        return TaxonomyTree(nodes)

    k = min(config.n_clusters, n)

    # Initialise centroids using k-means++
    seed_ids = _kmeans_plus_plus_seeds(vectors, k, rng)
    centroids: list[dict[str, float]] = [vectors[s] for s in seed_ids]

    # k-means iterations
    for _ in range(10):
        assignments = _assign_clusters(vectors, centroids)

        # Group doc_ids by cluster
        clusters: list[list[str]] = [[] for _ in range(k)]
        for idx, cluster_idx in enumerate(assignments):
            clusters[cluster_idx].append(doc_ids[idx])

        new_centroids: list[dict[str, float]] = []
        for ci, cluster_doc_ids in enumerate(clusters):
            if cluster_doc_ids:
                new_centroids.append(_compute_centroid(cluster_doc_ids, vectors))
            else:
                # Keep old centroid for empty cluster
                new_centroids.append(centroids[ci])

        centroids = new_centroids

    # Final assignment
    assignments = _assign_clusters(vectors, centroids)
    clusters = [[] for _ in range(k)]
    for idx, cluster_idx in enumerate(assignments):
        clusters[cluster_idx].append(doc_ids[idx])

    nodes = []
    for ci, cluster_doc_ids in enumerate(clusters):
        if len(cluster_doc_ids) < config.min_docs_per_cluster:
            continue
        terms = _top_terms(centroids[ci], config.top_terms_per_label)
        label = " / ".join(terms[:config.max_label_words]) if terms else f"cluster-{ci}"
        cohesion = _cluster_cohesion(cluster_doc_ids, vectors)
        node = TaxonomyNode(
            id=str(uuid.uuid4()),
            label=label,
            doc_ids=cluster_doc_ids,
            top_terms=terms,
            cohesion=cohesion,
        )
        nodes.append(node)

    return TaxonomyTree(nodes)
