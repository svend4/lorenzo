"""Category dataclasses for the keyword-based document classifier."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Category:
    """A classification category defined by a name, optional description,
    keyword list, and optional parent category name."""

    name: str
    description: str = ""
    keywords: list[str] = field(default_factory=list)
    parent: str | None = None


@dataclass
class ClassificationResult:
    """Result of classifying a single document.

    Attributes:
        doc_id:       Caller-supplied identifier for the document.
        text_snippet: First 200 characters of the text (for display/debugging).
        scores:       Mapping of category name → score (top ``max_categories`` only).
        top_category: Name of the highest-scoring category.
        confidence:   Score of the top category (after optional normalisation).
    """

    doc_id: str
    text_snippet: str
    scores: dict[str, float]
    top_category: str
    confidence: float

    def is_confident(self, threshold: float = 0.5) -> bool:
        """Return *True* when ``confidence`` meets or exceeds *threshold*."""
        return self.confidence >= threshold
