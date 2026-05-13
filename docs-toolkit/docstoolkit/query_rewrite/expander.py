"""Synonym-based query expansion for query rewriting."""
from dataclasses import dataclass


@dataclass
class ExpansionConfig:
    """Configuration for query expansion.

    Attributes:
        max_expansions: Maximum number of query variants to return (including the original).
        min_query_len:  Minimum character length required before expansion is attempted.
    """

    max_expansions: int = 5
    min_query_len: int = 3


_DEFAULT_CONFIG = ExpansionConfig()


class QueryExpander:
    """Expands a query by substituting registered synonyms for known terms."""

    def __init__(self) -> None:
        # Maps term (lowercased) → list of synonym strings
        self._synonyms: dict[str, list[str]] = {}

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def add_synonym(self, term: str, synonyms: list[str]) -> None:
        """Register *synonyms* for *term*.

        Subsequent calls for the same *term* extend (not replace) the synonym list,
        dropping duplicates.
        """
        key = term.lower()
        existing = self._synonyms.get(key, [])
        for s in synonyms:
            if s not in existing:
                existing.append(s)
        self._synonyms[key] = existing

    def synonym_count(self) -> int:
        """Return the total number of (term → synonym) mappings registered."""
        return sum(len(v) for v in self._synonyms.values())

    # ------------------------------------------------------------------
    # Expansion
    # ------------------------------------------------------------------

    def expand(self, query: str, config: "ExpansionConfig | None" = None) -> list[str]:
        """Return a deduplicated list of query variants (original first).

        For each synonym whose *term* appears in *query* (case-insensitive),
        one additional variant is produced where the term is replaced by that
        synonym.  Results are capped at ``config.max_expansions``.

        If *query* is shorter than ``config.min_query_len`` characters, only
        the original query is returned.
        """
        cfg = config if config is not None else _DEFAULT_CONFIG

        results: list[str] = [query]

        if len(query) < cfg.min_query_len:
            return results

        for term, synonyms in self._synonyms.items():
            # Check whether the term appears in the query (case-insensitive)
            import re
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            if not pattern.search(query):
                continue

            for synonym in synonyms:
                if len(results) >= cfg.max_expansions:
                    break
                variant = pattern.sub(synonym, query)
                if variant not in results:
                    results.append(variant)

            if len(results) >= cfg.max_expansions:
                break

        return results
