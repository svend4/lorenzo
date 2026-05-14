"""Summary reduction and clustering — stdlib only."""
import math
import random
from collections import Counter


def _token_set(text: str) -> set[str]:
    """Lowercase words from text."""
    import re
    return set(re.findall(r"[a-zа-яё]+", text.lower()))


def _tf_vector(text: str) -> dict[str, float]:
    """Simple term-frequency vector."""
    import re
    words = re.findall(r"[a-zа-яё]+", text.lower())
    if not words:
        return {}
    counts = Counter(words)
    total = len(words)
    return {w: c / total for w, c in counts.items()}


def _cosine(a: str, b: str) -> float:
    """TF-IDF-lite cosine similarity between two strings (simple word freq)."""
    va = _tf_vector(a)
    vb = _tf_vector(b)
    if not va or not vb:
        return 0.0
    common = set(va) & set(vb)
    if not common:
        return 0.0
    dot = sum(va[t] * vb[t] for t in common)
    norm_a = math.sqrt(sum(v * v for v in va.values()))
    norm_b = math.sqrt(sum(v * v for v in vb.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def cluster_summaries(
    summaries: list[str],
    *,
    n_clusters: int = 5,
    seed: int = 42,
) -> list[list[int]]:
    """Group summaries into n_clusters using greedy cosine similarity clustering.

    Algorithm (greedy, no sklearn):
    1. If len(summaries) <= n_clusters: each summary is its own cluster
    2. Pick n_clusters seed summaries via k-means++ style: first random,
       then each next seed is the one maximally dissimilar to existing seeds
    3. Assign each summary to nearest seed (by cosine)
    4. Return list of clusters (each cluster is list of indices into summaries)
    """
    if not summaries:
        return []

    n = len(summaries)

    if n <= n_clusters:
        return [[i] for i in range(n)]

    rng = random.Random(seed)

    # k-means++ style seed selection
    seed_indices: list[int] = []
    first = rng.randint(0, n - 1)
    seed_indices.append(first)

    for _ in range(min(n_clusters, n) - 1):
        # Find the candidate that is most dissimilar to all current seeds
        best_idx = -1
        best_min_sim = -1.0
        for i in range(n):
            if i in seed_indices:
                continue
            # min similarity to existing seeds (we want max of min dissimilarity)
            min_sim = min(_cosine(summaries[i], summaries[s]) for s in seed_indices)
            # We want most dissimilar = lowest max similarity
            # Actually: pick candidate with lowest similarity to nearest seed
            if best_idx == -1 or min_sim < best_min_sim:
                best_min_sim = min_sim
                best_idx = i
        if best_idx != -1:
            seed_indices.append(best_idx)

    # Assign each summary to nearest seed
    clusters: list[list[int]] = [[] for _ in range(len(seed_indices))]
    for i in range(n):
        best_cluster = 0
        best_sim = -1.0
        for ci, si in enumerate(seed_indices):
            sim = _cosine(summaries[i], summaries[si])
            if sim > best_sim:
                best_sim = sim
                best_cluster = ci
        clusters[best_cluster].append(i)

    # Remove empty clusters
    return [c for c in clusters if c]


def reduce_summaries(
    summaries: list[str],
    *,
    query: str = "",
    max_length: int = 500,
) -> str:
    """Combine multiple summaries into one meta-summary (no LLM needed).

    Algorithm:
    1. If query: rank summaries by relevance to query (token overlap), take top 5
       Otherwise: take all
    2. Concatenate with '. ' separator
    3. Run textrank_summary on the concatenated text with n_sentences=5
    4. Truncate to max_length chars
    5. Return result
    """
    from docstoolkit.summarize.extractor import textrank_summary

    if not summaries:
        return ""

    if query:
        query_tokens = _token_set(query)
        if query_tokens:
            scored = []
            for s in summaries:
                s_tokens = _token_set(s)
                overlap = len(s_tokens & query_tokens)
                scored.append((overlap, s))
            scored.sort(key=lambda x: -x[0])
            selected = [s for _, s in scored[:5]]
        else:
            selected = summaries
    else:
        selected = summaries

    if len(selected) == 1:
        result = selected[0]
    else:
        combined = ". ".join(s.rstrip(". ") for s in selected)
        result = textrank_summary(combined, n_sentences=5)

    return result[:max_length]
