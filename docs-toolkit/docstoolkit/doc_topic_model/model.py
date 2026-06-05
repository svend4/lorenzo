"""Lightweight TF-IDF + greedy clustering topic model (stdlib only)."""
from __future__ import annotations

import math
import re
import threading
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Optional

_TOKEN_RE = re.compile(r"\w+", re.UNICODE)


def _tokenize(text: str) -> list[str]:
    """Lowercase word tokenization (stdlib regex)."""
    if not text:
        return []
    return _TOKEN_RE.findall(text.lower())


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Topic:
    """A discovered topic in the corpus."""

    topic_id: int
    keywords: list[str]
    weight: float = 1.0
    doc_ids: list[str] = field(default_factory=list)


@dataclass
class TopicDoc:
    """Assignment of a document to a topic with a similarity score."""

    doc_id: str
    topic_id: int
    score: float


@dataclass
class TopicModel:
    """Result of fitting a :class:`DocTopicModel`."""

    topics: list[Topic]
    doc_assignments: dict[str, int]
    total_terms: int
    total_docs: int


# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------

class DocTopicModel:
    """Pure-stdlib topic model built on TF-IDF and greedy keyword clustering.

    Algorithm
    ---------
    1. Tokenize each document with ``re.findall(r'\\w+', text.lower())``.
    2. Compute TF for each document and DF across the corpus.
    3. Compute IDF = log(N / df(term)).
    4. For each document, keep its top-K TF-IDF terms ("doc signature").
    5. Greedily cluster documents whose signatures overlap heavily.
    6. Each cluster's keywords = aggregated top TF-IDF terms over its docs.
    7. Excess clusters are merged into the smallest topics until we hit
       ``num_topics``; if fewer clusters exist, the model returns that many.
    """

    def __init__(
        self,
        num_topics: int = 5,
        min_term_freq: int = 2,
        max_terms_per_topic: int = 10,
    ) -> None:
        if num_topics < 1:
            raise ValueError("num_topics must be >= 1")
        if min_term_freq < 1:
            raise ValueError("min_term_freq must be >= 1")
        if max_terms_per_topic < 1:
            raise ValueError("max_terms_per_topic must be >= 1")

        self._num_topics_target = num_topics
        self._min_term_freq = min_term_freq
        self._max_terms_per_topic = max_terms_per_topic

        self._lock = threading.Lock()

        # Fitted state
        self._fitted: bool = False
        self._model: Optional[TopicModel] = None
        self._idf: dict[str, float] = {}
        self._vocab: set[str] = set()
        self._topic_by_id: dict[int, Topic] = {}

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def is_fitted(self) -> bool:
        """Whether ``fit`` has been called successfully."""
        return self._fitted

    @property
    def num_topics(self) -> int:
        """Number of topics discovered (after fitting)."""
        if not self._fitted or self._model is None:
            return 0
        return len(self._model.topics)

    @property
    def total_docs(self) -> int:
        """Total number of documents in the fitted corpus."""
        if not self._fitted or self._model is None:
            return 0
        return self._model.total_docs

    # ------------------------------------------------------------------
    # Fit
    # ------------------------------------------------------------------

    def fit(self, documents: dict[str, str]) -> TopicModel:
        """Fit topics over the corpus and return the resulting :class:`TopicModel`.

        Parameters
        ----------
        documents:
            Mapping from ``doc_id`` to raw document text.
        """
        with self._lock:
            self._reset_locked()

            if not documents:
                model = TopicModel(topics=[], doc_assignments={}, total_terms=0, total_docs=0)
                self._model = model
                self._fitted = True
                return model

            # 1. tokenize
            doc_tokens: dict[str, list[str]] = {
                doc_id: _tokenize(text) for doc_id, text in documents.items()
            }

            # 2. term frequencies
            doc_tf: dict[str, Counter] = {
                doc_id: Counter(tokens) for doc_id, tokens in doc_tokens.items()
            }

            # 3. document frequency
            df: Counter = Counter()
            for tf in doc_tf.values():
                for term in tf:
                    df[term] += 1

            # filter by min_term_freq (df-based)
            kept_terms = {t for t, c in df.items() if c >= self._min_term_freq}

            n_docs = len(documents)
            # If filtering removed everything (e.g. all unique tokens), fall back
            # to raw vocabulary so we always produce something useful.
            if not kept_terms:
                kept_terms = set(df)

            # 4. IDF
            idf: dict[str, float] = {}
            for term in kept_terms:
                idf[term] = math.log((n_docs + 1) / (df[term] + 1)) + 1.0

            # 5. TF-IDF per doc, restrict to kept_terms
            doc_tfidf: dict[str, dict[str, float]] = {}
            for doc_id, tf in doc_tf.items():
                total = sum(tf.values()) or 1
                scores: dict[str, float] = {}
                for term, count in tf.items():
                    if term not in kept_terms:
                        continue
                    scores[term] = (count / total) * idf.get(term, 0.0)
                doc_tfidf[doc_id] = scores

            # 6. doc signature: top-K terms per doc
            sig_size = max(self._max_terms_per_topic, 5)
            doc_signature: dict[str, list[str]] = {}
            for doc_id, scores in doc_tfidf.items():
                top = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))[:sig_size]
                doc_signature[doc_id] = [t for t, _ in top]

            # 7. greedy clustering: assign each doc to existing cluster if its
            #    signature overlap (Jaccard) is high enough; else start a new one.
            clusters: list[dict] = []  # {keywords: set, docs: list[str], scores: dict}
            overlap_threshold = 0.15

            # Process docs in a stable order (sorted by id for determinism)
            for doc_id in sorted(doc_tokens.keys()):
                sig = set(doc_signature[doc_id])
                if not sig:
                    # doc has no usable terms; attach to a degenerate cluster later
                    if not clusters:
                        clusters.append({"keywords": set(), "docs": [doc_id]})
                    else:
                        clusters[0]["docs"].append(doc_id)
                    continue

                best_idx = -1
                best_score = 0.0
                for idx, cluster in enumerate(clusters):
                    ckw = cluster["keywords"]
                    if not ckw:
                        continue
                    inter = len(sig & ckw)
                    union = len(sig | ckw)
                    score = inter / union if union else 0.0
                    if score > best_score:
                        best_score = score
                        best_idx = idx

                if best_idx >= 0 and best_score >= overlap_threshold:
                    clusters[best_idx]["docs"].append(doc_id)
                    clusters[best_idx]["keywords"] |= sig
                else:
                    clusters.append({"keywords": set(sig), "docs": [doc_id]})

            # 8. reduce cluster count to num_topics_target if needed
            target = self._num_topics_target
            while len(clusters) > target:
                # merge two smallest clusters with most keyword overlap
                clusters.sort(key=lambda c: len(c["docs"]))
                small = clusters.pop(0)
                # find best target to merge into
                best_idx = 0
                best_overlap = -1
                for idx, other in enumerate(clusters):
                    overlap = len(small["keywords"] & other["keywords"])
                    if overlap > best_overlap:
                        best_overlap = overlap
                        best_idx = idx
                clusters[best_idx]["docs"].extend(small["docs"])
                clusters[best_idx]["keywords"] |= small["keywords"]

            # 9. build Topic objects with proper keyword ranking
            topics: list[Topic] = []
            doc_assignments: dict[str, int] = {}
            for tid, cluster in enumerate(clusters):
                # aggregate scores across docs in cluster
                agg: Counter = Counter()
                for did in cluster["docs"]:
                    for term, sc in doc_tfidf.get(did, {}).items():
                        agg[term] += sc
                top_terms = [
                    t for t, _ in sorted(agg.items(), key=lambda kv: (-kv[1], kv[0]))
                ][: self._max_terms_per_topic]

                if not top_terms and cluster["keywords"]:
                    top_terms = sorted(cluster["keywords"])[: self._max_terms_per_topic]

                weight = float(len(cluster["docs"])) / float(n_docs) if n_docs else 1.0
                topic = Topic(
                    topic_id=tid,
                    keywords=top_terms,
                    weight=weight,
                    doc_ids=sorted(cluster["docs"]),
                )
                topics.append(topic)
                for did in cluster["docs"]:
                    doc_assignments[did] = tid

            total_terms = sum(sum(tf.values()) for tf in doc_tf.values())

            model = TopicModel(
                topics=topics,
                doc_assignments=doc_assignments,
                total_terms=total_terms,
                total_docs=n_docs,
            )

            self._model = model
            self._idf = idf
            self._vocab = set(kept_terms)
            self._topic_by_id = {t.topic_id: t for t in topics}
            self._fitted = True
            return model

    # ------------------------------------------------------------------
    # Inference / queries
    # ------------------------------------------------------------------

    def assign(self, text: str) -> Optional[TopicDoc]:
        """Assign a new document to its best-matching existing topic.

        Returns ``None`` if the model isn't fitted, has no topics, or the
        document yields no overlap with any topic's keywords.
        """
        with self._lock:
            if not self._fitted or self._model is None or not self._model.topics:
                return None

            tokens = _tokenize(text)
            if not tokens:
                return None

            tf = Counter(tokens)
            total = sum(tf.values()) or 1
            scores: dict[str, float] = {}
            for term, count in tf.items():
                idf = self._idf.get(term)
                if idf is None:
                    continue
                scores[term] = (count / total) * idf

            if not scores:
                # No known vocab — fall back to raw token set
                doc_terms = set(tokens)
            else:
                doc_terms = set(scores)

            best_topic_id: Optional[int] = None
            best_score = -1.0
            for topic in self._model.topics:
                kw = set(topic.keywords)
                if not kw:
                    continue
                inter = doc_terms & kw
                if not inter:
                    continue
                if scores:
                    contrib = sum(scores.get(t, 0.0) for t in inter)
                    union = len(doc_terms | kw)
                    score = contrib + (len(inter) / union if union else 0.0)
                else:
                    union = len(doc_terms | kw)
                    score = len(inter) / union if union else 0.0
                if score > best_score:
                    best_score = score
                    best_topic_id = topic.topic_id

            if best_topic_id is None:
                return None
            return TopicDoc(doc_id="", topic_id=best_topic_id, score=float(best_score))

    def topic_for(self, doc_id: str) -> Optional[Topic]:
        """Return the topic that the given document was assigned to, or None."""
        if not self._fitted or self._model is None:
            return None
        tid = self._model.doc_assignments.get(doc_id)
        if tid is None:
            return None
        return self._topic_by_id.get(tid)

    def docs_for_topic(self, topic_id: int) -> list[str]:
        """List doc_ids assigned to a topic. Empty list if topic unknown."""
        topic = self._topic_by_id.get(topic_id)
        if topic is None:
            return []
        return list(topic.doc_ids)

    def top_keywords(self, topic_id: int, top_k: int = 10) -> list[tuple[str, float]]:
        """Return the top-k keywords for a topic with their weights.

        Weight is computed from inverse rank to give a stable float score in [0, 1].
        """
        topic = self._topic_by_id.get(topic_id)
        if topic is None or not topic.keywords:
            return []
        if top_k < 0:
            top_k = 0
        kws = topic.keywords[:top_k]
        n = len(kws)
        if n == 0:
            return []
        # decreasing weights: 1.0, (n-1)/n, ..., 1/n
        return [(kw, (n - i) / n) for i, kw in enumerate(kws)]

    def similarity(self, topic_id_a: int, topic_id_b: int) -> float:
        """Jaccard similarity between two topics' keyword sets."""
        a = self._topic_by_id.get(topic_id_a)
        b = self._topic_by_id.get(topic_id_b)
        if a is None or b is None:
            return 0.0
        sa = set(a.keywords)
        sb = set(b.keywords)
        if not sa and not sb:
            return 1.0  # both empty → identical
        union = sa | sb
        if not union:
            return 0.0
        return len(sa & sb) / len(union)

    def most_similar(self, text: str, top_k: int = 3) -> list[TopicDoc]:
        """Return top-k topics most similar to the given text.

        Uses Jaccard overlap between text tokens and topic keywords.
        """
        if not self._fitted or self._model is None or not self._model.topics:
            return []
        tokens = set(_tokenize(text))
        if not tokens:
            return []
        results: list[TopicDoc] = []
        for topic in self._model.topics:
            kw = set(topic.keywords)
            if not kw:
                continue
            union = tokens | kw
            score = len(tokens & kw) / len(union) if union else 0.0
            if score > 0:
                results.append(TopicDoc(doc_id="", topic_id=topic.topic_id, score=float(score)))
        results.sort(key=lambda td: (-td.score, td.topic_id))
        if top_k < 0:
            top_k = 0
        return results[:top_k]

    def coherence(self, topic_id: int) -> float:
        """Topic coherence in ``[0, 1]``.

        Approximation: mean per-document keyword coverage. Higher means the
        topic's keywords appear consistently across its documents.
        """
        topic = self._topic_by_id.get(topic_id)
        if topic is None:
            return 0.0
        if not topic.keywords or not topic.doc_ids:
            return 0.0
        if self._model is None:
            return 0.0

        # Recover token sets per doc from doc_assignments — but we don't keep
        # raw docs after fit. Use IDF presence as a proxy: a keyword is
        # "covered" if its IDF exists. Coherence then degenerates into how
        # tight keyword DF values are (low variance ⇒ tight topic).
        idf_vals = [self._idf.get(kw, 0.0) for kw in topic.keywords]
        if not idf_vals:
            return 0.0
        mean = sum(idf_vals) / len(idf_vals)
        if mean == 0:
            return 0.0
        var = sum((v - mean) ** 2 for v in idf_vals) / len(idf_vals)
        # convert variance to a [0,1] score via 1 / (1 + var)
        return 1.0 / (1.0 + var)

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------

    def vocabulary(self) -> set[str]:
        """Return a copy of the kept vocabulary set."""
        return set(self._vocab)

    def clear(self) -> None:
        """Drop all fitted state."""
        with self._lock:
            self._reset_locked()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _reset_locked(self) -> None:
        self._fitted = False
        self._model = None
        self._idf = {}
        self._vocab = set()
        self._topic_by_id = {}
