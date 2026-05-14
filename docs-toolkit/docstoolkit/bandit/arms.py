"""Beta-Bernoulli bandit arms with Thompson sampling.

Uses only Python stdlib (random.gammavariate) — no numpy required.
"""
import math
import random
from dataclasses import dataclass, field


@dataclass
class ArmStats:
    """Sufficient statistics for a Beta-Bernoulli arm."""

    name: str
    alpha: float        # successes + prior
    beta: float         # failures + prior
    total_pulls: int = 0
    total_successes: int = 0

    def mean(self) -> float:
        """E[Beta(alpha, beta)] = alpha / (alpha + beta)."""
        return self.alpha / (self.alpha + self.beta)

    def sample(self, rng: random.Random | None = None) -> float:
        """Sample from Beta(alpha, beta) using stdlib gammavariate.

        Uses the identity: Beta(a,b) = Gamma(a) / (Gamma(a) + Gamma(b)).
        random.gammavariate(shape, 1.0) is available in all Python versions.
        """
        _rng = rng if rng is not None else random
        # gammavariate requires shape > 0 (our alpha/beta are always >= 1 from prior)
        x = _rng.gammavariate(self.alpha, 1.0)
        y = _rng.gammavariate(self.beta, 1.0)
        total = x + y
        if total == 0.0:
            return 0.5
        return x / total

    def posterior_ci(self, confidence: float = 0.95) -> tuple[float, float]:
        """Approximate credible interval using Normal approximation of Beta.

        mean ± z * std, where
            std = sqrt(alpha * beta / ((alpha+beta)^2 * (alpha+beta+1)))
        Result is clamped to [0, 1].
        """
        mu = self.mean()
        ab = self.alpha + self.beta
        variance = (self.alpha * self.beta) / (ab * ab * (ab + 1.0))
        std = math.sqrt(variance)
        # Two-sided z for given confidence level (normal approximation)
        # Use lookup table for common values, fall back to linear interpolation
        z = _z_score(confidence)
        low = max(0.0, mu - z * std)
        high = min(1.0, mu + z * std)
        return low, high


def _z_score(confidence: float) -> float:
    """Return two-sided z-score for a given confidence level."""
    # Common lookup table
    _TABLE = {
        0.80: 1.282,
        0.85: 1.440,
        0.90: 1.645,
        0.95: 1.960,
        0.99: 2.576,
        0.999: 3.291,
    }
    if confidence in _TABLE:
        return _TABLE[confidence]
    # Sorted pairs for linear interpolation
    keys = sorted(_TABLE)
    if confidence <= keys[0]:
        return _TABLE[keys[0]]
    if confidence >= keys[-1]:
        return _TABLE[keys[-1]]
    for i in range(len(keys) - 1):
        lo, hi = keys[i], keys[i + 1]
        if lo <= confidence <= hi:
            t = (confidence - lo) / (hi - lo)
            return _TABLE[lo] + t * (_TABLE[hi] - _TABLE[lo])
    return 1.960  # fallback


class BetaBernoulliArm:
    """Beta-Bernoulli bandit arm with persistent mutable state."""

    def __init__(
        self,
        name: str,
        prior_alpha: float = 1.0,
        prior_beta: float = 1.0,
    ):
        self._stats = ArmStats(
            name=name,
            alpha=prior_alpha,
            beta=prior_beta,
        )

    def update(self, success: bool, weight: float = 1.0) -> None:
        """Update posterior with a new observation.

        success=True  → alpha  += weight
        success=False → beta   += weight
        """
        if success:
            self._stats.alpha += weight
            self._stats.total_successes += int(round(weight))
        else:
            self._stats.beta += weight
        self._stats.total_pulls += 1

    def sample(self, rng: random.Random | None = None) -> float:
        """Sample from the current Beta posterior."""
        return self._stats.sample(rng=rng)

    def mean(self) -> float:
        """Expected success probability under current posterior."""
        return self._stats.mean()

    def posterior_ci(self, confidence: float = 0.95) -> tuple[float, float]:
        """Approximate credible interval for this arm's success rate."""
        return self._stats.posterior_ci(confidence=confidence)

    @property
    def stats(self) -> ArmStats:
        """Read-only view of the arm's current statistics."""
        return self._stats
