import random
import math
from dataclasses import dataclass, field


@dataclass
class PrivacyBudget:
    """Differential privacy budget (epsilon-delta DP)."""
    epsilon: float = 1.0    # privacy loss parameter (lower = more private)
    delta: float = 1e-5     # failure probability
    sensitivity: float = 1.0  # global sensitivity of the metric

    def noise_scale(self) -> float:
        """Laplace mechanism noise scale = sensitivity / epsilon."""
        if self.epsilon <= 0:
            return float('inf')
        return self.sensitivity / self.epsilon

    def gaussian_sigma(self) -> float:
        """Phase VI.1 — sigma for the Gaussian mechanism.

        Classic Gaussian mechanism noise scale satisfying (epsilon, delta)-DP
        for L2-sensitivity:

            sigma = sqrt(2 · ln(1.25 / delta)) · sensitivity / epsilon

        Reference: Dwork & Roth, "The Algorithmic Foundations of Differential
        Privacy" (2014), Theorem 3.22.
        """
        if self.epsilon <= 0 or self.delta <= 0 or self.delta >= 1:
            return float("inf")
        return (
            math.sqrt(2.0 * math.log(1.25 / self.delta))
            * self.sensitivity
            / self.epsilon
        )

    def is_valid(self) -> bool:
        return self.epsilon > 0 and 0 <= self.delta < 1 and self.sensitivity > 0


def add_laplace_noise(value: float, budget: PrivacyBudget,
                      seed: int | None = None) -> float:
    """Add Laplace noise to a metric value.

    Laplace(0, scale) via inverse CDF:
      u = Uniform(-0.5, 0.5)
      noise = -scale * sign(u) * ln(1 - 2|u|)

    If scale is inf (epsilon=0): return value unchanged.
    Clip result to [0.0, 1.0] for metric values.
    """
    scale = budget.noise_scale()
    if scale == float('inf') or scale <= 0:
        return value
    rng = random.Random(seed)
    u = rng.uniform(-0.499, 0.499)  # avoid exactly ±0.5
    sign = 1.0 if u >= 0 else -1.0
    noise = -scale * sign * math.log(1 - 2 * abs(u))
    return max(0.0, min(1.0, value + noise))


def add_gaussian_noise(value: float, budget: PrivacyBudget,
                       seed: int | None = None) -> float:
    """Phase VI.1 — Gaussian mechanism for (epsilon, delta)-DP.

    Adds noise ~ N(0, sigma^2) where sigma = budget.gaussian_sigma().
    Useful when you compose many queries — Gaussian noise composes via
    the moments accountant much tighter than Laplace.
    """
    sigma = budget.gaussian_sigma()
    if sigma == float("inf") or sigma <= 0:
        return value
    rng = random.Random(seed)
    noise = rng.gauss(0.0, sigma)
    return max(0.0, min(1.0, value + noise))


@dataclass
class PrivacyAccountant:
    """Phase VI.1 — basic sequential composition accountant.

    Tracks how much (epsilon, delta) budget has been spent across multiple
    DP queries. Implements *basic composition* (the simplest correct rule):

        eps_total = sum(eps_i)
        delta_total = sum(delta_i)

    For tighter bounds use moments-accountant / RDP — out of scope here.
    """
    total_epsilon: float = 0.0
    total_delta: float = 0.0
    queries: list[tuple[float, float]] = field(default_factory=list)

    def spend(self, budget: PrivacyBudget) -> None:
        """Record one DP query against this accountant."""
        self.total_epsilon += budget.epsilon
        self.total_delta += budget.delta
        self.queries.append((budget.epsilon, budget.delta))

    def remaining(self,
                  epsilon_cap: float,
                  delta_cap: float = 1.0) -> tuple[float, float]:
        """Return (eps_left, delta_left) under the given caps."""
        return (
            max(0.0, epsilon_cap - self.total_epsilon),
            max(0.0, delta_cap - self.total_delta),
        )

    def is_exhausted(self,
                     epsilon_cap: float,
                     delta_cap: float = 1.0) -> bool:
        return (self.total_epsilon >= epsilon_cap or
                self.total_delta >= delta_cap)


def privatize_metrics(metrics: dict, budget: PrivacyBudget, seed: int | None = None) -> dict:
    """Add Laplace noise to all float values in metrics dict.

    Non-float values (int counts, strings) are passed through unchanged.
    For int values: add noise, round to nearest int, clip to >= 0.
    For float values: add noise, clip to [0, 1].
    """
    result = {}
    for k, v in metrics.items():
        if isinstance(v, float):
            result[k] = add_laplace_noise(v, budget, seed=seed)
        elif isinstance(v, int):
            noisy = add_laplace_noise(float(v) / max(v, 1), budget, seed=seed)
            result[k] = max(0, round(noisy * max(v, 1)))
        else:
            result[k] = v
    return result
