"""Extractive TextRank summarization and caching — stdlib only."""
import re
import hashlib
from dataclasses import dataclass, field


@dataclass
class SummaryCache:
    """Cache doc_hash → summary string to avoid re-summarizing unchanged docs."""
    _store: dict = None

    def __post_init__(self):
        self._store = {}

    def get(self, content: str) -> "str | None":
        """Return cached summary for content, or None if not cached."""
        return self._store.get(self._hash(content))

    def set(self, content: str, summary: str) -> None:
        """Store summary for content."""
        self._store[self._hash(content)] = summary

    def _hash(self, content: str) -> str:
        return hashlib.md5(content.encode()).hexdigest()

    @property
    def size(self) -> int:
        """Number of cached entries."""
        return len(self._store)


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences on '. ', '.\n', '? ', '! '."""
    # Split on sentence-ending punctuation followed by space or newline
    parts = re.split(r'(?<=[.?!])\s+', text.strip())
    # Filter out empty strings
    return [s.strip() for s in parts if s.strip()]


def _tokenize_set(text: str) -> set[str]:
    """Return set of lowercase word tokens."""
    return set(re.findall(r"[a-zа-яё]+", text.lower()))


def _jaccard(a: set[str], b: set[str]) -> float:
    """Jaccard similarity between two token sets."""
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    if union == 0:
        return 0.0
    return inter / union


def textrank_summary(
    text: str,
    *,
    n_sentences: int = 3,
    query: str = "",
) -> str:
    """Extractive TextRank summarization — pure stdlib.

    Algorithm:
    1. Split into sentences (on '. ', '.\\n', '? ', '! ')
    2. Build sentence similarity matrix: Jaccard token overlap between each pair
    3. Apply PageRank (alpha=0.85, max_iter=30, epsilon=1e-4):
       - Initialize scores = 1/N
       - Iterate: score[i] = (1-alpha)/N + alpha * sum(score[j] * sim[j][i] / sum(sim[j]))
    4. If query: add +0.2 bonus to sentences with query token overlap > 0
    5. Select top n_sentences by score (in original order)
    6. Return joined sentences

    Edge cases:
    - If fewer sentences than n_sentences: return all
    - Empty text: return ""
    - Single sentence: return it
    """
    if not text or not text.strip():
        return ""

    sentences = _split_sentences(text)

    if not sentences:
        return ""

    if len(sentences) == 1:
        return sentences[0]

    if len(sentences) <= n_sentences:
        return " ".join(sentences)

    N = len(sentences)
    alpha = 0.85
    max_iter = 30
    epsilon = 1e-4

    # Build token sets for each sentence
    token_sets = [_tokenize_set(s) for s in sentences]

    # Build similarity matrix
    sim = [[0.0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if i != j:
                sim[i][j] = _jaccard(token_sets[i], token_sets[j])

    # Row sums for normalization (outgoing sim from j to i)
    row_sums = [sum(sim[j]) for j in range(N)]

    # PageRank iteration
    scores = [1.0 / N] * N
    for _ in range(max_iter):
        new_scores = [0.0] * N
        for i in range(N):
            rank_sum = 0.0
            for j in range(N):
                if j != i and row_sums[j] > 0:
                    rank_sum += scores[j] * sim[j][i] / row_sums[j]
            new_scores[i] = (1 - alpha) / N + alpha * rank_sum
        # Check convergence
        delta = sum(abs(new_scores[i] - scores[i]) for i in range(N))
        scores = new_scores
        if delta < epsilon:
            break

    # Apply query boost
    if query:
        query_tokens = _tokenize_set(query)
        if query_tokens:
            for i in range(N):
                overlap = token_sets[i] & query_tokens
                if overlap:
                    scores[i] += 0.2

    # Select top n_sentences indices, preserving original order
    ranked = sorted(range(N), key=lambda i: -scores[i])
    top_indices = sorted(ranked[:n_sentences])

    selected = [sentences[i] for i in top_indices]
    return " ".join(selected)
