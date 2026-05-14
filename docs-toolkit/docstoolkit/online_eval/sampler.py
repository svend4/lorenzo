"""Детерминированный сэмплер запросов для онлайн-оценки качества."""
import hashlib
import random
from dataclasses import dataclass, field


@dataclass
class OnlineEvalSampler:
    """Решает: нужно ли оценивать данный запрос (sampling decision).

    Использует hash(query) для детерминизма: один и тот же query всегда даёт
    одинаковое решение. При seed != None добавляет случайность.
    """

    sample_rate: float = 0.01   # доля запросов для оценки (0.0 — 1.0)
    seed: int | None = None

    _total_seen: int = field(default=0, init=False, repr=False)
    _total_sampled: int = field(default=0, init=False, repr=False)
    _rng: random.Random | None = field(default=None, init=False, repr=False)

    def __post_init__(self):
        if self.seed is not None:
            self._rng = random.Random(self.seed)

    def maybe_sample(self, query: str) -> bool:
        """Детерминированное решение на основе hash(query).

        С seed: добавляет случайность поверх хэш-порога.
        Без seed: чисто детерминировано — один query → всегда одно решение.
        """
        self._total_seen += 1

        # Детерминированный хэш запроса → bucket 0..99
        digest = int(hashlib.md5(query.encode("utf-8"), usedforsecurity=False).hexdigest(), 16)
        bucket = digest % 100

        threshold = int(self.sample_rate * 100)

        if self._rng is not None:
            # Seed-based: взвешенный случайный выбор
            selected = self._rng.random() < self.sample_rate
        else:
            # Чисто детерминированный hash-based
            selected = bucket < threshold

        if selected:
            self._total_sampled += 1
        return selected

    def stats(self) -> dict:
        """Статистика сэмплирования."""
        effective = (
            self._total_sampled / self._total_seen
            if self._total_seen > 0
            else 0.0
        )
        return {
            "total_seen": self._total_seen,
            "total_sampled": self._total_sampled,
            "effective_rate": effective,
        }
