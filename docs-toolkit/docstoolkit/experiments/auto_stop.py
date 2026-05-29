"""Sequential Probability Ratio Test (SPRT) for A/B auto-stopping.

Implements Wald's SPRT so that an A/B experiment automatically stops as
soon as the data is sufficient to declare significance — either control wins,
variant wins, or it's a draw — without waiting for a fixed sample size.

This prevents two classical mistakes:
* Peeking: stopping early on a random fluctuation (controlled by alpha / beta).
* Over-running: continuing past the point where the result is already clear.

References:
    Wald, A. (1945). Sequential Tests of Statistical Hypotheses. Ann. Math. Stat.
    Johari et al. (2022). Always Valid Inference. Management Science.

Pure stdlib — no external dependencies.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal, Optional


# ---------------------------------------------------------------------------
# Outcome constants
# ---------------------------------------------------------------------------

Outcome = Literal["control_wins", "variant_wins", "continue", "max_n_reached"]


# ---------------------------------------------------------------------------
# SPRT core
# ---------------------------------------------------------------------------

@dataclass
class SPRTConfig:
    """Parameters for the sequential test.

    Parameters
    ----------
    alpha:
        Maximum allowed Type-I error (false positive rate).  Default 0.05.
    beta:
        Maximum allowed Type-II error (false negative rate).  Default 0.20
        → power = 80 %.
    min_effect:
        Minimum detectable effect (absolute difference in conversion rate).
        SPRT compares H1 (effect = min_effect) vs H0 (no effect).
    max_n_per_arm:
        Hard upper bound on samples per arm.  The test stops regardless of
        significance once either arm hits this limit.
    max_days:
        Hard upper bound in calendar days (measured from first observation).
        None = unlimited.
    """
    alpha: float = 0.05
    beta: float = 0.20
    min_effect: float = 0.02
    max_n_per_arm: int = 10_000
    max_days: Optional[int] = 7


@dataclass
class SPRTState:
    """Running state accumulated across observations."""
    n_control: int = 0
    n_variant: int = 0
    successes_control: int = 0
    successes_variant: int = 0
    log_likelihood_ratio: float = 0.0
    first_observation_ts: Optional[str] = None
    last_observation_ts: Optional[str] = None
    outcome: Outcome = "continue"

    # Boundaries (computed once from config)
    upper_boundary: float = 0.0   # log(1-beta / alpha)  → variant wins
    lower_boundary: float = 0.0   # log(beta / (1-alpha)) → control wins

    def record(self, arm: Literal["control", "variant"], success: bool) -> None:
        """Append one observation."""
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        if self.first_observation_ts is None:
            self.first_observation_ts = now
        self.last_observation_ts = now

        if arm == "control":
            self.n_control += 1
            if success:
                self.successes_control += 1
        else:
            self.n_variant += 1
            if success:
                self.successes_variant += 1

    @property
    def rate_control(self) -> float:
        return self.successes_control / self.n_control if self.n_control else 0.0

    @property
    def rate_variant(self) -> float:
        return self.successes_variant / self.n_variant if self.n_variant else 0.0

    @property
    def relative_uplift(self) -> Optional[float]:
        if self.rate_control == 0:
            return None
        return (self.rate_variant - self.rate_control) / self.rate_control

    def to_dict(self) -> dict:
        return {
            "n_control": self.n_control,
            "n_variant": self.n_variant,
            "rate_control": self.rate_control,
            "rate_variant": self.rate_variant,
            "relative_uplift": self.relative_uplift,
            "log_likelihood_ratio": self.log_likelihood_ratio,
            "upper_boundary": self.upper_boundary,
            "lower_boundary": self.lower_boundary,
            "outcome": self.outcome,
            "first_observation_ts": self.first_observation_ts,
            "last_observation_ts": self.last_observation_ts,
        }


# ---------------------------------------------------------------------------
# SPRTEngine
# ---------------------------------------------------------------------------

def _safe_log(x: float) -> float:
    if x <= 0.0:
        return -1000.0
    return math.log(x)


class SPRTEngine:
    """Manages a single A/B experiment using the SPRT stopping rule.

    Usage::

        engine = SPRTEngine(SPRTConfig(alpha=0.05, beta=0.20, min_effect=0.03))

        for event in stream:
            outcome = engine.observe(event["arm"], event["converted"])
            if outcome != "continue":
                print("Experiment stopped:", outcome)
                break

        print(engine.report())
    """

    def __init__(self, config: Optional[SPRTConfig] = None) -> None:
        self._cfg = config or SPRTConfig()
        self._state = SPRTState()
        # Pre-compute boundaries
        alpha, beta = self._cfg.alpha, self._cfg.beta
        self._state.upper_boundary = _safe_log((1 - beta) / alpha)
        self._state.lower_boundary = _safe_log(beta / (1 - alpha))

    @property
    def state(self) -> SPRTState:
        return self._state

    def observe(
        self,
        arm: Literal["control", "variant"],
        success: bool,
    ) -> Outcome:
        """Record one observation and evaluate the stopping criterion.

        Returns the current :attr:`Outcome`.
        """
        if self._state.outcome != "continue":
            return self._state.outcome

        self._state.record(arm, success)
        self._state.outcome = self._evaluate()
        return self._state.outcome

    def _evaluate(self) -> Outcome:
        s = self._state
        n_c, n_v = s.n_control, s.n_variant

        # Check hard limits
        if n_c >= self._cfg.max_n_per_arm or n_v >= self._cfg.max_n_per_arm:
            return "max_n_reached"

        if self._cfg.max_days is not None and s.first_observation_ts:
            elapsed_days = self._elapsed_days(s.first_observation_ts)
            if elapsed_days >= self._cfg.max_days:
                return "max_n_reached"

        # Need at least 1 observation per arm to compute a ratio
        if n_c < 1 or n_v < 1:
            return "continue"

        # Bernoulli SPRT log-likelihood update
        p0_c = s.successes_control / n_c          # H0: same rate
        p0_v = s.successes_variant / n_v
        p0 = (s.successes_control + s.successes_variant) / (n_c + n_v)

        p1_c = p0_c                                # H1: variant is better by min_effect
        p1_v = min(1.0, p0_v + self._cfg.min_effect)

        llr = (
            _safe_log(_bernoulli_pmf(s.successes_control, n_c, p1_c))
            + _safe_log(_bernoulli_pmf(s.successes_variant, n_v, p1_v))
            - _safe_log(_bernoulli_pmf(s.successes_control, n_c, p0))
            - _safe_log(_bernoulli_pmf(s.successes_variant, n_v, p0))
        )

        s.log_likelihood_ratio = llr

        if llr >= s.upper_boundary:
            return "variant_wins"
        if llr <= s.lower_boundary:
            return "control_wins"
        return "continue"

    def report(self) -> dict:
        """Return a human-readable summary dict."""
        return self._state.to_dict()

    @staticmethod
    def _elapsed_days(iso_ts: str) -> float:
        """Return fractional days since *iso_ts* (UTC)."""
        try:
            start = datetime.fromisoformat(iso_ts)
            now = datetime.now(timezone.utc)
            return (now - start).total_seconds() / 86_400
        except Exception:
            return 0.0


def _bernoulli_pmf(k: int, n: int, p: float) -> float:
    """Binomial PMF P(X=k | n, p) without scipy.stats."""
    if p <= 0.0:
        return 1.0 if k == 0 else 0.0
    if p >= 1.0:
        return 1.0 if k == n else 0.0
    log_binom = _log_binomial_coeff(n, k)
    return math.exp(log_binom + k * _safe_log(p) + (n - k) * _safe_log(1 - p))


def _log_binomial_coeff(n: int, k: int) -> float:
    if k < 0 or k > n:
        return -1000.0
    if k == 0 or k == n:
        return 0.0
    return (
        math.lgamma(n + 1)
        - math.lgamma(k + 1)
        - math.lgamma(n - k + 1)
    )
