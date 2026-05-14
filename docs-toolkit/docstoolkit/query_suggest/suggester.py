"""Query suggester combining trie prefix lookup with SQLite history."""
from __future__ import annotations

from dataclasses import dataclass

from docstoolkit.query_suggest.trie import QueryTrie
from docstoolkit.query_suggest.history import QueryHistory


@dataclass
class SuggestionConfig:
    """Configuration for :class:`QuerySuggester`.

    Attributes:
        max_suggestions: Maximum number of suggestions to return.
        min_prefix_len:  Minimum length of prefix before suggestions are produced.
        boost_recent:    Give extra weight to recently seen queries from history.
        boost_popular:   Give extra weight to frequently seen queries from history.
    """

    max_suggestions: int = 5
    min_prefix_len: int = 2
    boost_recent: bool = True
    boost_popular: bool = True


@dataclass
class Suggestion:
    """A single suggestion produced by :class:`QuerySuggester`.

    Attributes:
        query:  The suggested query string.
        score:  Relevance score in ``[0.0, 1.0]`` (higher is better).
        source: Where the suggestion originated — one of ``"trie"``,
                ``"history"``, or ``"completion"``.
    """

    query: str
    score: float
    source: str


class QuerySuggester:
    """High-level suggestion engine that merges trie prefix results with
    history-based popularity signals.

    Args:
        config:  Behaviour configuration.  Defaults to :class:`SuggestionConfig`
                 defaults.
        history: An existing :class:`QueryHistory` instance to use.  When
                 ``None`` a fresh in-memory history is created automatically.
    """

    def __init__(
        self,
        config: "SuggestionConfig | None" = None,
        history: "QueryHistory | None" = None,
    ) -> None:
        self._config = config if config is not None else SuggestionConfig()
        self._history = history if history is not None else QueryHistory()
        self._trie = QueryTrie()

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_query(self, query: str, count: int = 1) -> None:
        """Add *query* to both the trie and the history.

        The query is recorded in history ``count`` times so that frequency
        signals remain consistent between the two backends.
        """
        self._trie.insert(query, count)
        for _ in range(count):
            self._history.record(query)

    # ------------------------------------------------------------------
    # Suggestions
    # ------------------------------------------------------------------

    def suggest(self, prefix: str) -> list[Suggestion]:
        """Return up to ``config.max_suggestions`` suggestions for *prefix*.

        Returns an empty list when ``len(prefix) < config.min_prefix_len``.

        Scoring logic
        -------------
        1. Trie results are scored as ``count / max_count`` (normalised to
           ``[0, 1]``).
        2. History ``popular_for_prefix`` results are scored similarly.
        3. When ``boost_recent`` is True, queries that appear in
           ``recent_queries`` receive a bonus of ``+0.2`` (capped at 1.0).
        4. Results are deduplicated (last-writer-wins for the source field),
           sorted by score descending, and limited to ``max_suggestions``.
        """
        cfg = self._config
        normalized_prefix = prefix.lower().strip()

        if len(normalized_prefix) < cfg.min_prefix_len:
            return []

        scores: dict[str, tuple[float, str]] = {}  # query -> (score, source)

        # ---- trie candidates -------------------------------------------
        trie_results = self._trie.search(normalized_prefix)
        if trie_results:
            max_count = max(c for _, c in trie_results)
            for q, c in trie_results:
                score = c / max_count if max_count > 0 else 0.0
                scores[q] = (score, "trie")

        # ---- history candidates ----------------------------------------
        if cfg.boost_popular:
            hist_results = self._history.popular_for_prefix(
                normalized_prefix, n=cfg.max_suggestions * 2
            )
            if hist_results:
                hist_max = max(c for _, c in hist_results)
                for q, c in hist_results:
                    hist_score = c / hist_max if hist_max > 0 else 0.0
                    if q in scores:
                        # Blend: take the higher of the two scores
                        existing_score, _ = scores[q]
                        blended = max(existing_score, hist_score)
                        scores[q] = (blended, "history")
                    else:
                        scores[q] = (hist_score, "history")

        # ---- recent boost ----------------------------------------------
        if cfg.boost_recent:
            recent = set(self._history.recent_queries(n=cfg.max_suggestions * 2))
            boosted: dict[str, tuple[float, str]] = {}
            for q, (s, src) in scores.items():
                if q in recent:
                    boosted[q] = (min(1.0, s + 0.2), src)
                else:
                    boosted[q] = (s, src)
            scores = boosted

        # ---- sort and limit --------------------------------------------
        sorted_items = sorted(scores.items(), key=lambda kv: kv[1][0], reverse=True)
        suggestions = [
            Suggestion(query=q, score=round(s, 6), source=src)
            for q, (s, src) in sorted_items[: cfg.max_suggestions]
        ]
        return suggestions

    def complete(self, partial: str) -> list[str]:
        """Return only the query strings from :meth:`suggest`."""
        return [s.query for s in self.suggest(partial)]

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def query_count(self) -> int:
        """Return the number of distinct queries stored in the trie."""
        return self._trie.query_count()
