"""FeedbackAggregator — derives per-document scores from SignalStore signals."""
from dataclasses import dataclass

from docstoolkit.feedback.store import SignalStore


@dataclass
class DocScore:
    """Aggregated feedback score for a single document.

    Attributes
    ----------
    doc_id:
        Identifier of the document.
    avg_value:
        Mean signal value across all feedback signals for this document.
    signal_count:
        Total number of feedback signals recorded for this document.
    positive_rate:
        Fraction of signals that are positive (value > 0), in [0.0, 1.0].
    """

    doc_id: str
    avg_value: float
    signal_count: int
    positive_rate: float


class FeedbackAggregator:
    """Derive document-level quality scores from a :class:`SignalStore`.

    Parameters
    ----------
    store:
        A :class:`SignalStore` instance to read signals from.
    """

    def __init__(self, store: SignalStore) -> None:
        self._store = store

    # ------------------------------------------------------------------
    # Per-document scoring
    # ------------------------------------------------------------------

    def score_doc(self, doc_id: str) -> DocScore | None:
        """Return a :class:`DocScore` for *doc_id*, or ``None`` if no signals exist."""
        signals = self._store.for_doc(doc_id)
        if not signals:
            return None
        values = [s.value for s in signals]
        count = len(values)
        avg = sum(values) / count
        positive = sum(1 for v in values if v > 0.0)
        positive_rate = positive / count
        return DocScore(
            doc_id=doc_id,
            avg_value=avg,
            signal_count=count,
            positive_rate=positive_rate,
        )

    def score_all(self) -> list[DocScore]:
        """Return :class:`DocScore` for every document that has signals.

        The result is sorted by *avg_value* descending (best-first).
        """
        # Collect unique doc_ids from the store
        top = self._store.top_docs(n=100_000)  # get all
        scores: list[DocScore] = []
        for doc_id, _ in top:
            ds = self.score_doc(doc_id)
            if ds is not None:
                scores.append(ds)
        # sort descending by avg_value
        scores.sort(key=lambda ds: ds.avg_value, reverse=True)
        return scores

    # ------------------------------------------------------------------
    # Query-level satisfaction
    # ------------------------------------------------------------------

    def query_satisfaction(self, query: str) -> float:
        """Return average signal value for *query*.

        Returns ``0.0`` if no signals exist for the query.
        """
        signals = self._store.for_query(query)
        if not signals:
            return 0.0
        values = [s.value for s in signals]
        return sum(values) / len(values)

    # ------------------------------------------------------------------
    # Re-ranking
    # ------------------------------------------------------------------

    def rerank(
        self, doc_ids: list[str], boost_factor: float = 0.1
    ) -> list[str]:
        """Re-order *doc_ids* by combining original rank with feedback score.

        The ranking score for position *i* (0-indexed) is:

            rank_score = 1.0 / (i + 1)   (reciprocal-rank style)
            final_score = rank_score + avg_value * boost_factor

        Documents without any feedback signals are treated as having
        ``avg_value = 0.0``.

        Returns a new list of ``doc_id`` strings sorted by *final_score*
        descending.
        """
        # Pre-fetch avg values for all doc_ids in one pass
        avg_values: dict[str, float] = {}
        for doc_id in doc_ids:
            signals = self._store.for_doc(doc_id)
            if signals:
                values = [s.value for s in signals]
                avg_values[doc_id] = sum(values) / len(values)
            else:
                avg_values[doc_id] = 0.0

        scored = []
        for i, doc_id in enumerate(doc_ids):
            rank_score = 1.0 / (i + 1)
            final = rank_score + avg_values[doc_id] * boost_factor
            scored.append((doc_id, final))

        scored.sort(key=lambda t: t[1], reverse=True)
        return [doc_id for doc_id, _ in scored]
