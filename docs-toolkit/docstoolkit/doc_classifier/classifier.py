"""Keyword-frequency document classifier — stdlib only, no external deps."""
from __future__ import annotations

from dataclasses import dataclass, field

from .category import Category, ClassificationResult


@dataclass
class ClassifierConfig:
    """Configuration for :class:`DocumentClassifier`.

    Attributes:
        min_confidence: Minimum score to include a category in results
                        (applied before normalisation).  Not used to filter
                        the final ``scores`` dict — the top-N is the filter.
        max_categories: Maximum number of categories kept in
                        ``ClassificationResult.scores``.
        normalize:      When *True* divide each raw score by the sum of all
                        raw scores so that they sum to 1 (softmax-like).
    """

    min_confidence: float = 0.1
    max_categories: int = 3
    normalize: bool = True


class DocumentClassifier:
    """Keyword-count document classifier.

    Usage::

        clf = DocumentClassifier()
        clf.add_category(Category("tech", keywords=["python", "code"]))
        result = clf.classify("doc1", "python is great for coding")
    """

    def __init__(self, config: ClassifierConfig | None = None) -> None:
        self._config: ClassifierConfig = config if config is not None else ClassifierConfig()
        self._categories: dict[str, Category] = {}

    # ------------------------------------------------------------------
    # Category management
    # ------------------------------------------------------------------

    def add_category(self, category: Category) -> None:
        """Register *category*.  Overwrites a previous entry with the same name."""
        self._categories[category.name] = category

    def remove_category(self, name: str) -> bool:
        """Remove the category called *name*.

        Returns:
            *True* if the category existed and was removed, *False* otherwise.
        """
        if name in self._categories:
            del self._categories[name]
            return True
        return False

    def categories(self) -> list[Category]:
        """Return a list of all registered :class:`Category` objects."""
        return list(self._categories.values())

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    def classify(self, doc_id: str, text: str) -> ClassificationResult:
        """Classify a single document.

        Scoring
        -------
        For each category the raw score is:

            score = (number of keyword occurrences in *text*, case-insensitive)
                    / (len(text.split()) + 1)

        If ``config.normalize`` is *True* the scores are divided by their
        sum so they sum to 1 (when the sum is non-zero).

        The ``scores`` dict in the result contains only the top
        ``config.max_categories`` entries (by score).
        """
        words = text.lower().split()
        word_count = len(words)
        denominator = word_count + 1

        # --- raw scores ---------------------------------------------------
        raw: dict[str, float] = {}
        for name, cat in self._categories.items():
            count = 0
            for kw in cat.keywords:
                kw_lower = kw.lower()
                count += text.lower().count(kw_lower)
            raw[name] = count / denominator

        # --- normalise ----------------------------------------------------
        if self._config.normalize:
            total = sum(raw.values())
            if total > 0.0:
                raw = {n: s / total for n, s in raw.items()}

        # --- determine top category & confidence --------------------------
        if raw:
            top_category = max(raw, key=lambda n: raw[n])
            confidence = raw[top_category]
        else:
            top_category = ""
            confidence = 0.0

        # --- keep only top-N ----------------------------------------------
        sorted_cats = sorted(raw.items(), key=lambda x: x[1], reverse=True)
        top_scores: dict[str, float] = dict(sorted_cats[: self._config.max_categories])

        snippet = text[:200]

        return ClassificationResult(
            doc_id=doc_id,
            text_snippet=snippet,
            scores=top_scores,
            top_category=top_category,
            confidence=confidence,
        )

    def classify_batch(self, docs: dict[str, str]) -> list[ClassificationResult]:
        """Classify multiple documents.

        Args:
            docs: Mapping of ``doc_id → text``.

        Returns:
            List of :class:`ClassificationResult`, one per document, in the
            iteration order of *docs*.
        """
        return [self.classify(doc_id, text) for doc_id, text in docs.items()]
