"""Category hierarchy support for the keyword-based document classifier."""
from __future__ import annotations

from .category import Category
from .classifier import DocumentClassifier


class CategoryHierarchy:
    """Wraps a :class:`DocumentClassifier` to add parent/child awareness.

    Categories carry an optional ``parent`` field.  :meth:`build` registers
    all supplied categories in the underlying classifier and builds a
    ``parent → [children]`` mapping so that :meth:`children` and
    :meth:`ancestors` work in O(depth) time.

    :meth:`classify_hierarchical` classifies the text and returns scores for
    every matched category at each level of the tree.
    """

    def __init__(self, classifier: DocumentClassifier) -> None:
        self._classifier = classifier
        # parent_name (or None for roots) → list of child names
        self._children_map: dict[str | None, list[str]] = {}
        # child_name → parent_name
        self._parent_map: dict[str, str | None] = {}

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self, categories: list[Category]) -> None:
        """Register *categories* and construct the parent→children index.

        Calling ``build`` multiple times replaces the previous state.
        """
        self._children_map = {}
        self._parent_map = {}

        for cat in categories:
            self._classifier.add_category(cat)
            self._parent_map[cat.name] = cat.parent
            # ensure an entry exists for this node (even if it has no children)
            self._children_map.setdefault(cat.parent, [])
            self._children_map.setdefault(cat.name, [])
            if cat.parent is not None:
                self._children_map[cat.parent].append(cat.name)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def children(self, name: str) -> list[str]:
        """Return the names of direct children of the category called *name*.

        Returns an empty list when *name* is unknown or has no children.
        """
        return list(self._children_map.get(name, []))

    def ancestors(self, name: str) -> list[str]:
        """Return ancestor names from *name* upward (excluding *name* itself).

        The first element is the immediate parent, the last is the root.
        Returns an empty list for root categories or unknown names.
        """
        result: list[str] = []
        current = name
        seen: set[str] = {name}
        while True:
            parent = self._parent_map.get(current)
            if parent is None:
                break
            if parent in seen:
                # cycle guard
                break
            result.append(parent)
            seen.add(parent)
            current = parent
        return result

    # ------------------------------------------------------------------
    # Hierarchical classification
    # ------------------------------------------------------------------

    def classify_hierarchical(self, doc_id: str, text: str) -> dict[str, float]:
        """Classify *text* and return scores for matched categories at all levels.

        Strategy
        --------
        1. Run a standard :meth:`~DocumentClassifier.classify` call.
        2. From the full ``scores`` dict (all categories), propagate scores
           upward: each ancestor accumulates the score of its descendant
           (so a parent is counted even if the query only matches a child).
        3. The returned dict maps ``category_name → score`` for every
           category that has a non-zero score (direct or propagated).

        Returns:
            ``{category_name: score}`` — a flat dict covering all levels.
        """
        # Get scores for every category (temporarily use max_categories = all)
        original_max = self._classifier._config.max_categories
        original_normalize = self._classifier._config.normalize

        try:
            # Disable truncation so we see all categories; keep normalization
            self._classifier._config.max_categories = len(
                self._classifier._categories
            ) or 1
            result = self._classifier.classify(doc_id, text)
        finally:
            self._classifier._config.max_categories = original_max

        all_scores: dict[str, float] = dict(result.scores)

        # Propagate scores upward through the hierarchy
        propagated: dict[str, float] = dict(all_scores)
        for cat_name, score in all_scores.items():
            if score == 0.0:
                continue
            for ancestor in self.ancestors(cat_name):
                propagated[ancestor] = propagated.get(ancestor, 0.0) + score

        # Return only non-zero entries
        return {name: score for name, score in propagated.items() if score > 0.0}
