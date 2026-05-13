import re
from collections import Counter
from dataclasses import dataclass, field


@dataclass
class ConceptAlignment:
    """Alignment between a concept in corpus A and corpus B."""
    concept: str           # the concept/term being aligned
    doc_id_a: str          # source document in corpus A
    doc_id_b: str          # matching document in corpus B
    similarity: float      # 0-1 Jaccard similarity of surrounding context
    aligned: bool          # True if similarity >= threshold


@dataclass
class AlignmentResult:
    """Result of aligning two corpora."""
    alignments: list = field(default_factory=list)   # list[ConceptAlignment]
    corpus_a_size: int = 0
    corpus_b_size: int = 0
    aligned_count: int = 0

    def alignment_rate(self) -> float:
        """Fraction of concepts that aligned."""
        if not self.alignments:
            return 0.0
        return self.aligned_count / len(self.alignments)

    def best_alignments(self, top_n: int = 5) -> list:
        """Return top-N alignments sorted by similarity desc."""
        return sorted(self.alignments, key=lambda a: -a.similarity)[:top_n]


def align_corpora(
    corpus_a: dict,    # {doc_id: content}
    corpus_b: dict,    # {doc_id: content}
    threshold: float = 0.15,
) -> AlignmentResult:
    """Find concept alignments between two corpora.

    Algorithm:
    1. Extract top-10 keywords from each doc in corpus_a
       (words >= 4 chars, not stopwords, sorted by frequency desc)
    2. For each keyword in corpus_a doc:
       - Find best matching doc in corpus_b by Jaccard overlap of
         keyword's context window (±20 words around keyword in doc_a)
         vs full content of doc_b
       - If similarity >= threshold: aligned=True
    3. Deduplicate alignments by (concept, doc_id_a, doc_id_b)

    Returns AlignmentResult.
    """
    result = AlignmentResult(
        corpus_a_size=len(corpus_a),
        corpus_b_size=len(corpus_b),
    )

    if not corpus_a or not corpus_b:
        return result

    # Pre-compute token sets for all corpus_b docs
    b_token_sets = {doc_id: _token_set(content) for doc_id, content in corpus_b.items()}

    seen = set()  # (concept, doc_id_a, doc_id_b)

    for doc_id_a, content_a in corpus_a.items():
        keywords = _extract_keywords(content_a, top_n=10)
        words_a = re.findall(r'\b\w+\b', content_a)

        for keyword in keywords:
            # Build context window ±20 words around first occurrence of keyword
            context_tokens = _context_window(words_a, keyword, window=20)
            context_set = {w.lower() for w in context_tokens if len(w) >= 4}

            # Find best matching doc in corpus_b
            best_doc_id_b = None
            best_sim = -1.0

            for doc_id_b, b_tokens in b_token_sets.items():
                sim = _jaccard(context_set, b_tokens)
                if sim > best_sim:
                    best_sim = sim
                    best_doc_id_b = doc_id_b

            if best_doc_id_b is None:
                continue

            key = (keyword, doc_id_a, best_doc_id_b)
            if key in seen:
                continue
            seen.add(key)

            aligned = best_sim >= threshold
            alignment = ConceptAlignment(
                concept=keyword,
                doc_id_a=doc_id_a,
                doc_id_b=best_doc_id_b,
                similarity=best_sim,
                aligned=aligned,
            )
            result.alignments.append(alignment)
            if aligned:
                result.aligned_count += 1

    return result


def _extract_keywords(text: str, top_n: int = 10) -> list:
    """Extract top-N keywords: words >= 4 chars, not stopwords, by freq."""
    words = re.findall(r'\b\w{4,}\b', text.lower())
    filtered = [w for w in words if w not in _STOPWORDS]
    counts = Counter(filtered)
    return [word for word, _ in counts.most_common(top_n)]


def _context_window(words: list, keyword: str, window: int = 20) -> list:
    """Return words within ±window of the first occurrence of keyword."""
    kw_lower = keyword.lower()
    for i, w in enumerate(words):
        if w.lower() == kw_lower:
            start = max(0, i - window)
            end = min(len(words), i + window + 1)
            return words[start:end]
    # keyword not found as exact token; return empty
    return []


def _token_set(text: str) -> set:
    return set(w.lower() for w in re.findall(r'\b\w{4,}\b', text))


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


_STOPWORDS = {
    "this", "that", "with", "from", "have", "been", "they", "their",
    "will", "would", "could", "should", "about", "which", "there",
    "what", "when", "where", "into", "your", "more", "also", "than",
    "then", "some", "were", "each", "just", "these", "those",
}
