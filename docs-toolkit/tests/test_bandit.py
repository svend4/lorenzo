"""Tests for docstoolkit.bandit — Thompson sampling A/B testing module.

Covers ArmStats, BetaBernoulliArm, ThompsonBandit, BanditExperiment.
"""
import math
import random
import tempfile
from pathlib import Path

import pytest

from docstoolkit.bandit import (
    ArmStats,
    BanditExperiment,
    BanditResult,
    BanditState,
    BetaBernoulliArm,
    ThompsonBandit,
)


# =============================================================================
# ArmStats
# =============================================================================


class TestArmStats:
    def test_fields_and_defaults(self):
        s = ArmStats(name="a", alpha=2.0, beta=3.0)
        assert s.name == "a"
        assert s.alpha == 2.0
        assert s.beta == 3.0
        assert s.total_pulls == 0
        assert s.total_successes == 0

    def test_mean_formula(self):
        s = ArmStats(name="x", alpha=3.0, beta=1.0)
        assert math.isclose(s.mean(), 3.0 / 4.0, rel_tol=1e-9)

    def test_mean_uniform_prior(self):
        s = ArmStats(name="x", alpha=1.0, beta=1.0)
        assert math.isclose(s.mean(), 0.5, rel_tol=1e-9)

    def test_sample_returns_float_in_unit_interval(self):
        s = ArmStats(name="x", alpha=2.0, beta=5.0)
        for _ in range(50):
            val = s.sample()
            assert 0.0 <= val <= 1.0

    def test_sample_with_rng(self):
        s = ArmStats(name="x", alpha=2.0, beta=5.0)
        rng = random.Random(42)
        val = s.sample(rng=rng)
        assert isinstance(val, float)
        assert 0.0 <= val <= 1.0

    def test_sample_reproducible_with_seeded_rng(self):
        s = ArmStats(name="x", alpha=2.0, beta=5.0)
        rng1 = random.Random(99)
        rng2 = random.Random(99)
        assert s.sample(rng=rng1) == s.sample(rng=rng2)

    def test_posterior_ci_ordering(self):
        s = ArmStats(name="x", alpha=10.0, beta=5.0)
        low, high = s.posterior_ci(confidence=0.95)
        mean = s.mean()
        assert low < mean < high

    def test_posterior_ci_bounds_in_unit_interval(self):
        s = ArmStats(name="x", alpha=1.0, beta=1.0)
        low, high = s.posterior_ci(confidence=0.95)
        assert 0.0 <= low
        assert high <= 1.0

    def test_posterior_ci_wider_for_higher_confidence(self):
        s = ArmStats(name="x", alpha=5.0, beta=5.0)
        low_90, high_90 = s.posterior_ci(confidence=0.90)
        low_99, high_99 = s.posterior_ci(confidence=0.99)
        width_90 = high_90 - low_90
        width_99 = high_99 - low_99
        assert width_99 > width_90


# =============================================================================
# BetaBernoulliArm
# =============================================================================


class TestBetaBernoulliArm:
    def test_update_success_increments_alpha(self):
        arm = BetaBernoulliArm("a", prior_alpha=1.0, prior_beta=1.0)
        arm.update(True)
        assert arm.stats.alpha == 2.0
        assert arm.stats.beta == 1.0

    def test_update_failure_increments_beta(self):
        arm = BetaBernoulliArm("a", prior_alpha=1.0, prior_beta=1.0)
        arm.update(False)
        assert arm.stats.alpha == 1.0
        assert arm.stats.beta == 2.0

    def test_update_with_weight(self):
        arm = BetaBernoulliArm("a", prior_alpha=1.0, prior_beta=1.0)
        arm.update(True, weight=2.0)
        assert arm.stats.alpha == 3.0
        assert arm.stats.beta == 1.0

    def test_update_failure_with_weight(self):
        arm = BetaBernoulliArm("a", prior_alpha=1.0, prior_beta=1.0)
        arm.update(False, weight=3.0)
        assert arm.stats.alpha == 1.0
        assert arm.stats.beta == 4.0

    def test_update_increments_total_pulls(self):
        arm = BetaBernoulliArm("a")
        arm.update(True)
        arm.update(False)
        assert arm.stats.total_pulls == 2

    def test_sample_returns_float_in_unit_interval(self):
        arm = BetaBernoulliArm("b", prior_alpha=2.0, prior_beta=5.0)
        for _ in range(30):
            assert 0.0 <= arm.sample() <= 1.0

    def test_sample_with_rng(self):
        arm = BetaBernoulliArm("b")
        rng = random.Random(7)
        val = arm.sample(rng=rng)
        assert isinstance(val, float)

    def test_mean_delegates_to_stats(self):
        arm = BetaBernoulliArm("c", prior_alpha=3.0, prior_beta=1.0)
        assert math.isclose(arm.mean(), 0.75, rel_tol=1e-9)

    def test_posterior_ci_returns_tuple(self):
        arm = BetaBernoulliArm("d", prior_alpha=5.0, prior_beta=5.0)
        ci = arm.posterior_ci()
        assert len(ci) == 2
        low, high = ci
        assert low < arm.mean() < high

    def test_stats_property_returns_arm_stats(self):
        arm = BetaBernoulliArm("e")
        assert isinstance(arm.stats, ArmStats)
        assert arm.stats.name == "e"

    def test_multiple_updates_accumulate(self):
        arm = BetaBernoulliArm("f", prior_alpha=1.0, prior_beta=1.0)
        for _ in range(5):
            arm.update(True)
        for _ in range(3):
            arm.update(False)
        assert arm.stats.alpha == 6.0
        assert arm.stats.beta == 4.0


# =============================================================================
# ThompsonBandit
# =============================================================================


class TestThompsonBandit:
    def test_init_two_arms_both_present(self):
        bandit = ThompsonBandit(["a", "b"])
        state = bandit.state()
        names = {s.arm_name for s in state}
        assert names == {"a", "b"}

    def test_select_returns_valid_arm(self):
        bandit = ThompsonBandit(["x", "y", "z"], seed=0)
        choice = bandit.select()
        assert choice in ("x", "y", "z")

    def test_select_explores_all_arms(self):
        """Over 100 selections all arms must be chosen at least once."""
        bandit = ThompsonBandit(["a", "b", "c"], seed=42)
        seen = set()
        for _ in range(100):
            seen.add(bandit.select())
            bandit.update(bandit.select(), reward=0.0)  # keep pulls balanced
        assert seen == {"a", "b", "c"}

    def test_select_100_times_coverage(self):
        """Exploration floor ensures every arm gets some pulls."""
        bandit = ThompsonBandit(["p", "q"], exploration_floor=0.1, seed=1)
        counts = {"p": 0, "q": 0}
        for _ in range(100):
            arm = bandit.select()
            counts[arm] += 1
            bandit.update(arm, reward=random.random())
        assert counts["p"] > 0
        assert counts["q"] > 0

    def test_winner_after_many_successes_on_one_arm(self):
        bandit = ThompsonBandit(["good", "bad"], seed=5)
        for _ in range(200):
            bandit.update("good", reward=1.0)
        for _ in range(200):
            bandit.update("bad", reward=0.0)
        assert bandit.winner() == "good"

    def test_winner_returns_none_when_equal(self):
        bandit = ThompsonBandit(["a", "b"])
        # Arms are equal (same prior, no updates)
        # With very few pulls winner() should not be declared
        assert bandit.winner() is None

    def test_update_invalid_arm_raises_key_error(self):
        bandit = ThompsonBandit(["a", "b"])
        with pytest.raises(KeyError):
            bandit.update("nonexistent", reward=1.0)

    def test_state_returns_list_of_bandit_state(self):
        bandit = ThompsonBandit(["m", "n"])
        states = bandit.state()
        assert len(states) == 2
        for s in states:
            assert isinstance(s, BanditState)
            assert s.arm_name in ("m", "n")
            assert 0.0 <= s.mean <= 1.0
            assert s.ci_low <= s.mean <= s.ci_high

    def test_reset_returns_to_prior(self):
        bandit = ThompsonBandit(["a", "b"], prior_alpha=1.0, prior_beta=1.0)
        for _ in range(20):
            bandit.update("a", reward=1.0)
        # After updates, mean("a") should be > 0.5
        states_before = {s.arm_name: s for s in bandit.state()}
        assert states_before["a"].mean > 0.6

        bandit.reset()
        states_after = {s.arm_name: s for s in bandit.state()}
        # After reset, mean should be back near 0.5 (uniform prior)
        assert math.isclose(states_after["a"].mean, 0.5, rel_tol=1e-6)
        assert states_after["a"].total_pulls == 0

    def test_persistence_across_reload(self):
        """Bandit state survives process restart (file-backed SQLite)."""
        with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as f:
            db_path = f.name

        try:
            # Create and update
            b1 = ThompsonBandit(["x", "y"], db_path=db_path)
            for _ in range(10):
                b1.update("x", reward=1.0)

            # Reload from same file
            b2 = ThompsonBandit(["x", "y"], db_path=db_path)
            states = {s.arm_name: s for s in b2.state()}
            assert states["x"].total_pulls == 10
            assert states["x"].mean > 0.5
        finally:
            Path(db_path).unlink(missing_ok=True)

    def test_update_success_changes_mean_upward(self):
        bandit = ThompsonBandit(["a"], seed=0)
        mean_before = bandit.state()[0].mean
        for _ in range(20):
            bandit.update("a", reward=1.0)
        mean_after = bandit.state()[0].mean
        assert mean_after > mean_before

    def test_state_ci_low_below_ci_high(self):
        bandit = ThompsonBandit(["a", "b", "c"])
        for s in bandit.state():
            assert s.ci_low <= s.ci_high


# =============================================================================
# BanditExperiment
# =============================================================================


class TestBanditExperiment:
    def test_choose_returns_valid_variant(self):
        exp = BanditExperiment("test", ["bm25", "hybrid", "semantic"])
        choice = exp.choose()
        assert choice in ("bm25", "hybrid", "semantic")

    def test_record_updates_bandit(self):
        exp = BanditExperiment("test", ["a", "b"])
        exp.record("a", success=True)
        result = exp.result()
        states = {s.arm_name: s for s in result.arm_states}
        assert states["a"].total_pulls == 1

    def test_record_failure_updates_bandit(self):
        exp = BanditExperiment("test", ["a", "b"])
        exp.record("b", success=False)
        result = exp.result()
        states = {s.arm_name: s for s in result.arm_states}
        assert states["b"].total_pulls == 1

    def test_result_has_correct_name(self):
        exp = BanditExperiment("my-experiment", ["x", "y"])
        result = exp.result()
        assert result.experiment_name == "my-experiment"

    def test_result_has_correct_arm_count(self):
        exp = BanditExperiment("test", ["bm25", "hybrid", "semantic"])
        result = exp.result()
        assert len(result.arm_states) == 3

    def test_result_total_pulls(self):
        exp = BanditExperiment("test", ["a", "b"])
        exp.record("a", success=True)
        exp.record("b", success=False)
        result = exp.result()
        assert result.total_pulls == 2

    def test_summary_returns_non_empty_string(self):
        exp = BanditExperiment("test", ["bm25", "hybrid"])
        result = exp.result()
        s = result.summary()
        assert isinstance(s, str)
        assert len(s) > 0

    def test_summary_contains_variant_names(self):
        exp = BanditExperiment("test", ["bm25", "hybrid", "semantic"])
        result = exp.result()
        summary = result.summary()
        assert "bm25" in summary
        assert "hybrid" in summary
        assert "semantic" in summary

    def test_summary_contains_experiment_name(self):
        exp = BanditExperiment("my-rag-test", ["a", "b"])
        summary = exp.result().summary()
        assert "my-rag-test" in summary

    def test_auto_promote_winner_returns_none_when_no_winner(self):
        exp = BanditExperiment("test", ["a", "b"])
        assert exp.auto_promote_winner() is None

    def test_auto_promote_winner_returns_winner_after_clear_win(self):
        exp = BanditExperiment("test", ["winner", "loser"])
        for _ in range(200):
            exp.record("winner", success=True)
        for _ in range(200):
            exp.record("loser", success=False)
        winner = exp.auto_promote_winner()
        assert winner == "winner"

    def test_integration_choose_record_choose(self):
        """Full loop: choose → record → choose again doesn't crash."""
        exp = BanditExperiment("integration", ["bm25", "hybrid"])
        for _ in range(10):
            variant = exp.choose()
            exp.record(variant, success=random.random() > 0.5)
        # Should still return a valid choice
        choice = exp.choose()
        assert choice in ("bm25", "hybrid")

    def test_result_is_bandit_result_instance(self):
        exp = BanditExperiment("test", ["a", "b"])
        assert isinstance(exp.result(), BanditResult)

    def test_three_variants_all_reachable(self):
        """Over many selections all three variants must be chosen."""
        exp = BanditExperiment("test", ["bm25", "hybrid", "semantic"])
        seen = set()
        for _ in range(60):
            v = exp.choose()
            seen.add(v)
            exp.record(v, success=True)
        assert seen == {"bm25", "hybrid", "semantic"}
