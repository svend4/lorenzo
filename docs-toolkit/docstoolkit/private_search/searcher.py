"""Privacy-preserving searcher: wraps BM25-style search with PII anonymization
and optional k-anonymity generalization.
"""
import math
import re
from dataclasses import dataclass, field

from docstoolkit.private_search.anonymizer import QueryAnonymizer
from docstoolkit.private_search.k_anonymity import KAnonymizer, KAnonymityConfig


@dataclass
class PrivateSearchConfig:
    """Configuration for the privacy-preserving searcher."""

    anonymize_queries: bool = True
    k_anonymity: bool = False
    k: int = 5
    noise_queries: int = 0  # number of dummy queries to mix in


@dataclass
class PrivateSearchResult:
    """Result returned by :class:`PrivateSearcher.search`."""

    query: str
    anonymized_query: str
    results: list[str]
    privacy_applied: list[str]


# ---------------------------------------------------------------------------
# Internal BM25-style helpers
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> list[str]:
    return re.findall(r'[a-zA-Zа-яёА-ЯЁ0-9]+', text.lower())


def _bm25_score(
    query_tokens: list[str],
    doc_tokens: list[str],
    doc_freq: dict[str, int],
    num_docs: int,
    avg_doc_len: float,
    k1: float = 1.5,
    b: float = 0.75,
) -> float:
    """Compute a BM25 score for one document."""
    score = 0.0
    doc_len = len(doc_tokens)
    tf_map: dict[str, int] = {}
    for t in doc_tokens:
        tf_map[t] = tf_map.get(t, 0) + 1

    for token in set(query_tokens):
        tf = tf_map.get(token, 0)
        if tf == 0:
            continue
        df = doc_freq.get(token, 0)
        idf = math.log((num_docs - df + 0.5) / (df + 0.5) + 1.0)
        tf_norm = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / avg_doc_len))
        score += idf * tf_norm
    return score


class PrivateSearcher:
    """Search over documents with privacy-preserving query handling."""

    def __init__(
        self,
        config: PrivateSearchConfig | None = None,
        documents: dict[str, str] | None = None,
    ) -> None:
        self._config = config or PrivateSearchConfig()
        self._anonymizer = QueryAnonymizer()
        self._k_anonymizer: KAnonymizer | None = None
        if self._config.k_anonymity:
            self._k_anonymizer = KAnonymizer(
                KAnonymityConfig(k=self._config.k)
            )

        # Document store: doc_id → raw text
        self._docs: dict[str, str] = {}
        # Inverted index helpers
        self._doc_tokens: dict[str, list[str]] = {}
        self._doc_freq: dict[str, int] = {}
        self._avg_doc_len: float = 0.0

        if documents:
            self.index_documents(documents)

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------

    def index_documents(self, docs: dict[str, str]) -> None:
        """Index *docs* (doc_id → text) for BM25 retrieval."""
        self._docs.update(docs)
        # Re-build full index
        self._doc_tokens = {
            doc_id: _tokenize(text) for doc_id, text in self._docs.items()
        }
        # Document frequency (how many docs contain each token)
        df: dict[str, int] = {}
        for tokens in self._doc_tokens.values():
            for t in set(tokens):
                df[t] = df.get(t, 0) + 1
        self._doc_freq = df

        lengths = [len(t) for t in self._doc_tokens.values()]
        self._avg_doc_len = sum(lengths) / len(lengths) if lengths else 1.0

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(self, query: str) -> PrivateSearchResult:
        """Search documents for *query*, applying configured privacy techniques.

        Returns a :class:`PrivateSearchResult` with ranked document IDs.
        """
        privacy_applied: list[str] = []
        anonymized_query = query

        # Step 1 – PII anonymization
        if self._config.anonymize_queries:
            anonymized_query, redacted = self._anonymizer.anonymize(query)
            privacy_applied.append('anonymize_queries')
            if redacted:
                privacy_applied.extend(redacted)

        # Step 2 – k-anonymity generalization
        if self._config.k_anonymity and self._k_anonymizer is not None:
            generalized = self._k_anonymizer.anonymize_batch([anonymized_query])
            anonymized_query = generalized[0] if generalized else anonymized_query
            privacy_applied.append('k_anonymity')

        # Step 3 – noise queries (dummy queries to obscure the real one)
        if self._config.noise_queries > 0:
            privacy_applied.append('noise_queries')
            # We execute the noise queries internally but discard their results
            noise_tokens = ['the', 'a', 'is', 'in', 'of', 'and', 'to', 'for']
            for i in range(self._config.noise_queries):
                dummy = ' '.join(
                    noise_tokens[i % len(noise_tokens):i % len(noise_tokens) + 3]
                )
                self._bm25_search(dummy)  # fire and discard

        # Step 4 – actual BM25 search
        results = self._bm25_search(anonymized_query)

        return PrivateSearchResult(
            query=query,
            anonymized_query=anonymized_query,
            results=results,
            privacy_applied=privacy_applied,
        )

    # ------------------------------------------------------------------
    # Internal BM25 retrieval
    # ------------------------------------------------------------------

    def _bm25_search(self, query: str, top_k: int = 10) -> list[str]:
        """Return ranked doc IDs for *query* using BM25."""
        if not self._docs:
            return []

        query_tokens = _tokenize(query)
        if not query_tokens:
            return []

        scores: list[tuple[float, str]] = []
        num_docs = len(self._docs)
        for doc_id, tokens in self._doc_tokens.items():
            score = _bm25_score(
                query_tokens,
                tokens,
                self._doc_freq,
                num_docs,
                self._avg_doc_len,
            )
            if score > 0:
                scores.append((score, doc_id))

        scores.sort(key=lambda x: x[0], reverse=True)
        return [doc_id for _, doc_id in scores[:top_k]]
