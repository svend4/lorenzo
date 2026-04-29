"""Тесты benchmark suite."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from bench.runner import (
    Bench, run_suites, save_history, load_history,
    compare_with_baseline, render_text, SUITES,
)


def test_bench_basic():
    bench = Bench(
        name="trivial",
        fn=lambda: sum(range(100)),
        iterations=3,
        warmup=1,
        suite="test",
    )
    result = bench.run()
    assert result["name"] == "trivial"
    assert result["suite"] == "test"
    assert result["iterations"] == 3
    assert result["mean_ms"] >= 0
    assert result["min_ms"] <= result["mean_ms"] <= result["max_ms"]


def test_bench_with_setup():
    def setup():
        return list(range(1000))

    def fn(ctx):
        sum(ctx)

    bench = Bench(name="sum_list", fn=fn, setup=setup, iterations=2)
    result = bench.run()
    assert result["iterations"] == 2


def test_suites_registered():
    assert "frontmatter" in SUITES
    assert "embeddings" in SUITES
    assert "search" in SUITES
    assert "graph" in SUITES
    assert "jobs" in SUITES
    assert "cluster" in SUITES


def test_run_suite_frontmatter():
    results = run_suites(["frontmatter"])
    assert len(results) >= 1
    for r in results:
        assert r["suite"] == "frontmatter"
        assert "mean_ms" in r


def test_save_load_history(tmp_path, monkeypatch):
    fake_path = tmp_path / "h.jsonl"
    monkeypatch.setattr("bench.runner.HISTORY_PATH", fake_path)

    save_history([{"name": "x", "suite": "s", "mean_ms": 10}])
    save_history([{"name": "y", "suite": "s", "mean_ms": 20}])

    history = load_history()
    assert len(history) == 2
    assert history[0]["results"][0]["name"] == "x"
    assert history[1]["results"][0]["name"] == "y"


def test_compare_no_regressions():
    baseline = [{"suite": "s", "name": "fast", "mean_ms": 10}]
    current = [{"suite": "s", "name": "fast", "mean_ms": 11}]  # +10%
    cmp = compare_with_baseline(current, baseline, threshold_pct=30)
    assert cmp["regressions"] == []


def test_compare_detects_regression():
    baseline = [{"suite": "s", "name": "slow", "mean_ms": 10}]
    current = [{"suite": "s", "name": "slow", "mean_ms": 20}]  # +100%
    cmp = compare_with_baseline(current, baseline, threshold_pct=30)
    assert len(cmp["regressions"]) == 1
    assert cmp["regressions"][0]["delta_pct"] == 100.0


def test_compare_skips_missing():
    baseline = [{"suite": "s", "name": "old", "mean_ms": 10}]
    current = [{"suite": "s", "name": "new", "mean_ms": 100}]
    cmp = compare_with_baseline(current, baseline)
    assert cmp["regressions"] == []  # new нет в baseline → пропуск


def test_render_text():
    results = [
        {"suite": "embeddings", "name": "fit", "iterations": 5,
         "min_ms": 1.0, "mean_ms": 1.5, "max_ms": 2.0, "stdev_ms": 0.3}
    ]
    out = render_text(results)
    assert "embeddings" in out
    assert "fit" in out
    assert "1.5ms" in out
