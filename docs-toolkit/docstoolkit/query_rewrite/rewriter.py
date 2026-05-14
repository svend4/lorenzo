"""High-level query rewriter combining rules, synonym expansion, and normalization."""
import re
from dataclasses import dataclass, field

from docstoolkit.query_rewrite.rules import RuleSet
from docstoolkit.query_rewrite.expander import QueryExpander, ExpansionConfig


@dataclass
class RewriteConfig:
    """Configuration for :class:`QueryRewriter`.

    Attributes:
        apply_rules:      Apply registered :class:`~rules.RewriteRule` objects.
        expand_synonyms:  Expand the rewritten query via registered synonyms.
        lowercase:        Convert the query to lowercase before other processing.
        strip_stopwords:  Remove stop-words listed in *stopwords*.
        stopwords:        Set of stop-words to remove (only active when *strip_stopwords* is True).
    """

    apply_rules: bool = True
    expand_synonyms: bool = False
    lowercase: bool = True
    strip_stopwords: bool = False
    stopwords: set[str] = field(default_factory=set)


@dataclass
class RewriteResult:
    """The outcome of a single :meth:`QueryRewriter.rewrite` call.

    Attributes:
        original:       The query string as passed in.
        rewritten:      The transformed query string.
        rules_applied:  IDs of rules that were applied.
        expansions:     Additional query variants produced by synonym expansion.
    """

    original: str
    rewritten: str
    rules_applied: list[str]
    expansions: list[str]

    def was_rewritten(self) -> bool:
        """Return True if the rewritten query differs from the original."""
        return self.original != self.rewritten

    def expansion_count(self) -> int:
        """Return the number of expansion variants (not counting the rewritten query itself)."""
        return len(self.expansions)


class QueryRewriter:
    """Combines normalization, rule-based rewriting, and synonym expansion.

    Args:
        config:   Behaviour configuration.  Defaults to :class:`RewriteConfig` defaults.
        rule_set: Collection of rewrite rules.  Defaults to an empty :class:`~rules.RuleSet`.
        expander: Synonym expander.  Defaults to an empty :class:`~expander.QueryExpander`.
    """

    def __init__(
        self,
        config: "RewriteConfig | None" = None,
        rule_set: "RuleSet | None" = None,
        expander: "QueryExpander | None" = None,
    ) -> None:
        self._config = config if config is not None else RewriteConfig()
        self._rule_set = rule_set if rule_set is not None else RuleSet()
        self._expander = expander if expander is not None else QueryExpander()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def rewrite(self, query: str) -> RewriteResult:
        """Rewrite *query* according to the current configuration.

        Processing order:
        1. Lowercase (if enabled).
        2. Strip stop-words (if enabled).
        3. Apply rewrite rules (if enabled), highest priority first.
        4. Expand synonyms (if enabled).

        Returns a :class:`RewriteResult` capturing all intermediate information.
        """
        cfg = self._config
        current = query
        rules_applied: list[str] = []

        # Step 1 — lowercase
        if cfg.lowercase:
            current = current.lower()

        # Step 2 — strip stop-words
        if cfg.strip_stopwords and cfg.stopwords:
            current = self._remove_stopwords(current, cfg.stopwords)

        # Step 3 — apply rules (highest priority first)
        if cfg.apply_rules:
            for rule in self._rule_set.rules_for(current):
                current = rule.apply(current)
                rules_applied.append(rule.rule_id)

        # Step 4 — expand synonyms
        expansions: list[str] = []
        if cfg.expand_synonyms:
            all_variants = self._expander.expand(current)
            # First item is the query itself; the rest are expansions
            expansions = all_variants[1:]

        return RewriteResult(
            original=query,
            rewritten=current,
            rules_applied=rules_applied,
            expansions=expansions,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _remove_stopwords(query: str, stopwords: set[str]) -> str:
        """Remove stop-word tokens from *query*, collapsing extra whitespace."""
        tokens = query.split()
        filtered = [t for t in tokens if t.lower() not in stopwords]
        return " ".join(filtered)
