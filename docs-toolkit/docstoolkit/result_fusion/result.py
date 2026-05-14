"""SearchResult dataclass for the result fusion module (E17)."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SearchResult:
    """A single result returned by a retrieval source.

    Parameters
    ----------
    doc_id:   Unique document identifier.
    score:    Raw relevance score from the source (higher is better).
    source:   Name of the retrieval source that produced this result.
    rank:     1-based position within the source result list (0 = unset).
    metadata: Arbitrary key/value annotations (e.g. title, snippet).
    """

    doc_id: str
    score: float
    source: str
    rank: int = 0
    metadata: dict = field(default_factory=dict)

    def normalized_score(self, min_s: float, max_s: float) -> float:
        """Return min-max normalised score in [0, 1].

        Returns 0.5 when *min_s* == *max_s* (degenerate range) to avoid
        division by zero while keeping the value centred.

        Parameters
        ----------
        min_s: Minimum score in the distribution.
        max_s: Maximum score in the distribution.
        """
        if min_s == max_s:
            return 0.5
        return (self.score - min_s) / (max_s - min_s)
