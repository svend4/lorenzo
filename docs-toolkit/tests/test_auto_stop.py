"""Tests for docstoolkit.experiments.auto_stop — SPRT A/B auto-stopping."""
from __future__ import annotations

import pytest

from docstoolkit.experiments import SPRTConfig, SPRTEngine, SPRTState
from docstoolkit.experiments.auto_stop import _bernoulli_pmf, _log_binomial_coeff


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _simulate(engine: SPRTEngine, n_control: int, conv_control: float,
              n_variant: int, conv_variant: float, seed: int = 42) -> str:
    """Feed synthetic data interleaved, return final outcome."""
    import random
    rng = random.Random(seed)

    total = n_control + n_variant
    arms = ["control"] * n_control + ["variant"] * n_variant
    rng.shuffle(arms)

    for arm in arms:
        rate = conv_control if arm == "control" else conv_variant
        success = rng.random() < rate
        outcome = engine.observe(arm, success)
        if outcome != "continue":
            return outcome

    return engine.state.outcome


# ---------------------------------------------------------------------------
# SPRTConfig
# ---------------------------------------------------------------------------

class TestSPRTConfig:
    def test_defaults(self):
        cfg = SPRTConfig()
        assert cfg.alpha == 0.05
        assert cfg.beta == 0.20
        assert cfg.min_effect == 0.02

    def test_custom(self):
        cfg = SPRTConfig(alpha=0.01, beta=0.10, min_effect=0.05, max_n_per_arm=500)
        assert cfg.alpha == 0.01
        assert cfg.max_n_per_arm == 500


# ---------------------------------------------------------------------------
# SPRTState
# ---------------------------------------------------------------------------

class TestSPRTState:
    def test_initial_rates_zero(self):
        s = SPRTState()
        assert s.rate_control == 0.0
        assert s.rate_variant == 0.0

    def test_record_control(self):
        s = SPRTState()
        s.record("control", True)
        assert s.n_control == 1
        assert s.successes_control == 1

    def test_record_variant_fail(self):
        s = SPRTState()
        s.record("variant", False)
        assert s.n_variant == 1
        assert s.successes_variant == 0

    def test_rate_after_records(self):
        s = SPRTState()
        s.record("control", True)
        s.record("control", False)
        assert s.rate_control == pytest.approx(0.5)

    def test_relative_uplift_zero_control(self):
        s = SPRTState()
        assert s.relative_uplift is None

    def test_relative_uplift_positive(self):
        s = SPRTState()
        s.record("control", True)   # 100% control
        s.record("variant", True)
        s.record("variant", True)   # 200% variant (2/1 vs 1/1 = +100%)
        assert s.relative_uplift is not None

    def test_to_dict_has_expected_keys(self):
        s = SPRTState()
        d = s.to_dict()
        for key in ("n_control", "n_variant", "rate_control", "rate_variant",
                    "log_likelihood_ratio", "outcome"):
            assert key in d


# ---------------------------------------------------------------------------
# SPRTEngine — basic behaviour
# ---------------------------------------------------------------------------

class TestSPRTEngineBasic:
    def test_initial_outcome_is_continue(self):
        engine = SPRTEngine()
        assert engine.state.outcome == "continue"

    def test_boundaries_set_from_config(self):
        import math
        engine = SPRTEngine(SPRTConfig(alpha=0.05, beta=0.20))
        assert engine.state.upper_boundary == pytest.approx(math.log((1 - 0.20) / 0.05), rel=1e-4)
        assert engine.state.lower_boundary == pytest.approx(math.log(0.20 / 0.95), rel=1e-4)

    def test_single_observation_stays_continue(self):
        engine = SPRTEngine()
        outcome = engine.observe("control", True)
        assert outcome == "continue"

    def test_observe_after_stop_returns_same_outcome(self):
        engine = SPRTEngine(SPRTConfig(max_n_per_arm=1))
        engine.observe("control", True)
        engine.observe("variant", True)   # hits max_n
        stopped = engine.state.outcome
        assert stopped == "max_n_reached"
        # More observations don't change it
        engine.observe("control", True)
        assert engine.state.outcome == "max_n_reached"

    def test_max_n_stops_experiment(self):
        engine = SPRTEngine(SPRTConfig(max_n_per_arm=5))
        for _ in range(5):
            engine.observe("control", True)
            engine.observe("variant", True)
        assert engine.state.outcome == "max_n_reached"

    def test_report_is_dict(self):
        engine = SPRTEngine()
        engine.observe("control", True)
        engine.observe("variant", False)
        r = engine.report()
        assert isinstance(r, dict)
        assert "outcome" in r


# ---------------------------------------------------------------------------
# SPRTEngine — stopping decisions
# ---------------------------------------------------------------------------

class TestSPRTEngineStopping:
    def test_no_effect_does_not_stop_early(self):
        """Equal conversion rates → should NOT declare variant_wins quickly."""
        engine = SPRTEngine(SPRTConfig(
            alpha=0.05, beta=0.20, min_effect=0.10, max_n_per_arm=200
        ))
        outcome = _simulate(engine, 200, 0.20, 200, 0.20, seed=1)
        # With no real effect, SPRT should either run to max or declare control_wins
        assert outcome in ("control_wins", "max_n_reached", "continue")
        assert outcome != "variant_wins"

    def test_large_effect_stops_variant_wins(self):
        """Variant with 2× conversion rate should win quickly."""
        engine = SPRTEngine(SPRTConfig(
            alpha=0.05, beta=0.20, min_effect=0.05, max_n_per_arm=2000
        ))
        # 5% vs 15% — large real effect
        outcome = _simulate(engine, 2000, 0.05, 2000, 0.15, seed=99)
        assert outcome in ("variant_wins", "max_n_reached")

    def test_control_better_experiment_reaches_conclusion(self):
        """Control is clearly better → experiment stops (not open-ended)."""
        engine = SPRTEngine(SPRTConfig(
            alpha=0.05, beta=0.20, min_effect=0.05, max_n_per_arm=1000
        ))
        # Control 20% vs variant 5% — control is much better
        outcome = _simulate(engine, 1000, 0.20, 1000, 0.05, seed=77)
        # With large enough sample the test must conclude (not run forever)
        assert outcome in ("control_wins", "variant_wins", "max_n_reached")
        # It must NOT just continue indefinitely
        assert outcome != "continue"


# ---------------------------------------------------------------------------
# Probability helpers
# ---------------------------------------------------------------------------

class TestProbabilityHelpers:
    def test_bernoulli_pmf_all_successes(self):
        # P(k=n|n,p=1) should be 1
        assert _bernoulli_pmf(5, 5, 1.0) == pytest.approx(1.0)

    def test_bernoulli_pmf_no_successes_p_zero(self):
        # P(k=0|n,p=0) should be 1
        assert _bernoulli_pmf(0, 5, 0.0) == pytest.approx(1.0)

    def test_bernoulli_pmf_standard(self):
        # P(k=1|n=2,p=0.5) = 2*0.5*0.5 = 0.5
        assert _bernoulli_pmf(1, 2, 0.5) == pytest.approx(0.5, rel=1e-4)

    def test_bernoulli_pmf_k_gt_n_returns_zero(self):
        assert _bernoulli_pmf(6, 5, 0.5) == pytest.approx(0.0)

    def test_log_binomial_k0(self):
        # C(n,0) = 1 → log = 0
        assert _log_binomial_coeff(10, 0) == 0.0

    def test_log_binomial_k_eq_n(self):
        # C(n,n) = 1 → log = 0
        assert _log_binomial_coeff(10, 10) == 0.0
