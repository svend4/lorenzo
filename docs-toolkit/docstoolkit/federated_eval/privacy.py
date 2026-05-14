import random
import math
from dataclasses import dataclass

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

    def is_valid(self) -> bool:
        return self.epsilon > 0 and 0 <= self.delta < 1 and self.sensitivity > 0


def add_laplace_noise(value: float, budget: PrivacyBudget, seed: int | None = None) -> float:
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
