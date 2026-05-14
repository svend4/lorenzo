"""Rule-based document classifier (stdlib only).

Each :class:`ClassifierRule` describes a category through a set of keywords plus
optional required/excluded constraints. The :class:`DocClassifierV2` walks every
rule, scores it, and reports the best match.

Scoring algorithm
-----------------
For each rule:

* Skip if any excluded keyword is present in the text.
* Skip if any required keyword is absent.
* Count keyword occurrences (each occurrence counts once).
* If matches < min_matches, skip.
* score = (matches / total_keywords) * weight

After scoring, rules are sorted by score (desc). When no rule matches, a
``default_category`` classification with zero score is returned.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable


@dataclass
class ClassifierRule:
    """A single classification rule.

    Attributes:
        category: Category name produced when this rule wins.
        keywords: Keywords that indicate this category.
        required: All keywords that *must* be present for the rule to fire.
        excluded: Keywords whose presence disqualifies the rule.
        weight: Multiplier applied to the normalized match score.
        min_matches: Minimum number of keyword matches required to keep the rule.
    """

    category: str
    keywords: list[str]
    required: list[str] = field(default_factory=list)
    excluded: list[str] = field(default_factory=list)
    weight: float = 1.0
    min_matches: int = 1


@dataclass
class Classification:
    """Result of classifying a single piece of text."""

    category: str
    score: float
    matched_keywords: list[str]
    confidence: float


@dataclass
class ClassifierConfig:
    """Configuration for :class:`DocClassifierV2`."""

    rules: list[ClassifierRule]
    case_sensitive: bool = False
    tokenize: bool = True
    default_category: str = "unknown"


def _normalize(text: str, case_sensitive: bool) -> str:
    return text if case_sensitive else text.lower()


def _contains(needle: str, haystack: str, tokenize: bool) -> bool:
    """Return True if ``needle`` is present in ``haystack``.

    When ``tokenize`` is True, matches whole words / phrases on word boundaries.
    Otherwise performs a plain substring search.
    """
    if not needle:
        return False
    if not tokenize:
        return needle in haystack
    # Whole-word match with word boundaries. ``re.escape`` keeps spaces/dashes
    # working so we can match multi-word keywords as phrases.
    pattern = r"(?<!\w)" + re.escape(needle) + r"(?!\w)"
    return re.search(pattern, haystack) is not None


class DocClassifierV2:
    """Rule-based classifier driven by :class:`ClassifierConfig`."""

    def __init__(self, config: ClassifierConfig) -> None:
        self.config = config

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    @property
    def categories(self) -> list[str]:
        """List of category names registered in the classifier."""
        return [rule.category for rule in self.config.rules]

    @property
    def rule_count(self) -> int:
        """Number of rules currently configured."""
        return len(self.config.rules)

    def add_rule(self, rule: ClassifierRule) -> None:
        """Append a new rule to the configuration."""
        self.config.rules.append(rule)

    def remove_rule(self, category: str) -> bool:
        """Remove the first rule for ``category``.

        Returns True if a rule was removed, False otherwise.
        """
        for i, rule in enumerate(self.config.rules):
            if rule.category == category:
                del self.config.rules[i]
                return True
        return False

    def classify(self, text: str) -> Classification:
        """Return the highest-scoring classification for ``text``."""
        results = self.classify_all(text)
        if not results:
            return Classification(
                category=self.config.default_category,
                score=0.0,
                matched_keywords=[],
                confidence=0.0,
            )
        return results[0]

    def classify_all(self, text: str) -> list[Classification]:
        """Return every matching classification, sorted by score (desc)."""
        normalized = _normalize(text, self.config.case_sensitive)
        results: list[Classification] = []
        max_score = 0.0
        for rule in self.config.rules:
            classification = self._score_rule(rule, normalized)
            if classification is None:
                continue
            results.append(classification)
            if classification.score > max_score:
                max_score = classification.score

        # Normalize confidence relative to the best score seen.
        if max_score > 0:
            for c in results:
                c.confidence = min(1.0, c.score / max_score)
        else:
            for c in results:
                c.confidence = 0.0

        results.sort(key=lambda c: c.score, reverse=True)
        return results

    def classify_batch(self, texts: list[str]) -> list[Classification]:
        """Classify a batch of texts in order."""
        return [self.classify(text) for text in texts]

    def predict_category(self, text: str) -> str:
        """Convenience helper returning only the predicted category name."""
        return self.classify(text).category

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _score_rule(
        self, rule: ClassifierRule, normalized_text: str
    ) -> Classification | None:
        case_sensitive = self.config.case_sensitive
        tokenize = self.config.tokenize

        def norm_kw(kw: str) -> str:
            return _normalize(kw, case_sensitive)

        # Excluded keywords disqualify the rule.
        for kw in rule.excluded:
            if _contains(norm_kw(kw), normalized_text, tokenize):
                return None

        # Required keywords must all be present.
        for kw in rule.required:
            if not _contains(norm_kw(kw), normalized_text, tokenize):
                return None

        matched: list[str] = []
        for kw in rule.keywords:
            if not kw:
                continue
            if _contains(norm_kw(kw), normalized_text, tokenize):
                matched.append(kw)

        if len(matched) < rule.min_matches:
            return None

        total = len([k for k in rule.keywords if k])
        if total == 0:
            return None

        score = (len(matched) / total) * rule.weight
        return Classification(
            category=rule.category,
            score=score,
            matched_keywords=matched,
            confidence=0.0,  # filled in by classify_all
        )


__all__ = [
    "Classification",
    "ClassifierConfig",
    "ClassifierRule",
    "DocClassifierV2",
]
