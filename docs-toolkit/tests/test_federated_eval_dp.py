"""Phase VI.1 — Gaussian mechanism + PrivacyAccountant tests."""
from __future__ import annotations

import math
import statistics

import pytest

from docstoolkit.federated_eval import (
    PrivacyBudget, PrivacyAccountant,
    add_laplace_noise, add_gaussian_noise,
)


# ---------- Gaussian mechanism ----------

def test_gaussian_sigma_formula():
    """sigma = sqrt(2 ln(1.25 / delta)) * sensitivity / epsilon."""
    b = PrivacyBudget(epsilon=1.0, delta=1e-5, sensitivity=1.0)
    expected = math.sqrt(2 * math.log(1.25 / 1e-5))
    assert b.gaussian_sigma() == pytest.approx(expected, rel=1e-6)


def test_gaussian_sigma_scales_with_sensitivity():
    a = PrivacyBudget(epsilon=1.0, delta=1e-5, sensitivity=1.0).gaussian_sigma()
    b = PrivacyBudget(epsilon=1.0, delta=1e-5, sensitivity=2.0).gaussian_sigma()
    assert b == pytest.approx(2 * a, rel=1e-6)


def test_gaussian_noise_zero_epsilon_returns_value():
    b = PrivacyBudget(epsilon=0.0, delta=1e-5, sensitivity=1.0)
    assert add_gaussian_noise(0.5, b, seed=42) == 0.5


def test_gaussian_noise_clipped_to_unit_interval():
    b = PrivacyBudget(epsilon=0.01, delta=0.5, sensitivity=1.0)
    out = add_gaussian_noise(0.5, b, seed=42)
    assert 0.0 <= out <= 1.0


def test_gaussian_noise_unbiased_on_average():
    """Mean over many samples ≈ original value."""
    b = PrivacyBudget(epsilon=10.0, delta=1e-5, sensitivity=0.05)
    samples = [add_gaussian_noise(0.5, b, seed=i) for i in range(500)]
    mean = statistics.mean(samples)
    # Generous tolerance because we clipped; with eps=10 noise is small.
    assert abs(mean - 0.5) < 0.05


# ---------- PrivacyAccountant ----------

def test_accountant_initial_state():
    a = PrivacyAccountant()
    assert a.total_epsilon == 0.0
    assert a.total_delta == 0.0
    assert a.queries == []


def test_accountant_spend_accumulates():
    a = PrivacyAccountant()
    b1 = PrivacyBudget(epsilon=0.5, delta=1e-5)
    b2 = PrivacyBudget(epsilon=0.3, delta=2e-5)
    a.spend(b1)
    a.spend(b2)
    assert a.total_epsilon == pytest.approx(0.8)
    assert a.total_delta == pytest.approx(3e-5)
    assert len(a.queries) == 2


def test_accountant_remaining_under_cap():
    a = PrivacyAccountant()
    a.spend(PrivacyBudget(epsilon=0.3))
    eps_left, delta_left = a.remaining(epsilon_cap=1.0, delta_cap=1e-3)
    assert eps_left == pytest.approx(0.7)


def test_accountant_remaining_floors_at_zero():
    a = PrivacyAccountant()
    a.spend(PrivacyBudget(epsilon=2.0))
    eps_left, _ = a.remaining(epsilon_cap=1.0)
    assert eps_left == 0.0


def test_accountant_is_exhausted():
    a = PrivacyAccountant()
    assert not a.is_exhausted(epsilon_cap=1.0)
    a.spend(PrivacyBudget(epsilon=1.0))
    assert a.is_exhausted(epsilon_cap=1.0)


def test_laplace_still_works_after_phase_vi():
    """Phase VI shouldn't change the Laplace API."""
    b = PrivacyBudget(epsilon=1.0, delta=1e-5, sensitivity=1.0)
    out = add_laplace_noise(0.5, b, seed=42)
    assert 0.0 <= out <= 1.0
