"""Fitness evaluation with caching for GA prompt evolution."""
import hashlib
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class FitnessCache:
    """Cache fitness evaluations to avoid redundant LLM calls."""
    _store: dict = field(default=None, repr=False)

    def __post_init__(self):
        self._store = {}

    def get(self, template: str) -> float | None:
        """Return cached score for template, or None if not cached."""
        return self._store.get(self._hash(template))

    def set(self, template: str, score: float) -> None:
        """Cache score for template."""
        self._store[self._hash(template)] = score

    def _hash(self, template: str) -> str:
        return hashlib.md5(template.encode()).hexdigest()

    @property
    def size(self) -> int:
        """Number of cached entries."""
        return len(self._store)


def evaluate_population(
    templates: list[str],
    fitness_fn: Callable[[str], float],
    cache: FitnessCache | None = None,
) -> list[float]:
    """Evaluate fitness for each template, using cache to skip already-evaluated ones."""
    scores: list[float] = []
    for tmpl in templates:
        if cache is not None:
            cached = cache.get(tmpl)
            if cached is not None:
                scores.append(cached)
                continue
        score = fitness_fn(tmpl)
        if cache is not None:
            cache.set(tmpl, score)
        scores.append(score)
    return scores
