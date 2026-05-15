"""Smoke tests for new benchmark suites (ask_features, helpers)."""
from __future__ import annotations

import pytest

from bench.runner import SUITES, run_suites


def test_ask_features_suite_registered():
    assert "ask_features" in SUITES


def test_helpers_suite_registered():
    assert "helpers" in SUITES


def test_ask_features_runs():
    results = run_suites(["ask_features"])
    assert len(results) >= 9
    names = {r["name"] for r in results}
    assert "ask_baseline" in names
    assert "ask_compose_5" in names


def test_ask_features_has_timing_keys():
    results = run_suites(["ask_features"])
    for r in results:
        assert "median_ms" in r
        assert "min_ms" in r
        assert "iterations" in r
        assert r["median_ms"] >= 0
        assert r["min_ms"] >= 0


def test_helpers_runs():
    results = run_suites(["helpers"])
    assert len(results) >= 3
    names = {r["name"] for r in results}
    assert "measure_voice_500ch" in names


def test_ask_baseline_under_50ms():
    """Sanity check: baseline ask on stub corpus should be well under 50ms."""
    [r] = [
        x for x in run_suites(["ask_features"])
        if x["name"] == "ask_baseline"
    ]
    assert r["median_ms"] < 50.0
