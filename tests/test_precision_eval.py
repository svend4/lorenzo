"""Tests for improve_precision_eval — Hit Rate@10 ≥ 0.70."""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


def test_run_eval_returns_expected_keys():
    mod = importlib.import_module("improve_precision_eval")
    result = mod.run_eval(k=10, verbose=False)
    assert "hit_rate" in result
    assert "hits" in result
    assert "n_queries" in result
    assert "mean_mrr" in result
    assert "pass" in result


def test_hit_rate_threshold():
    mod = importlib.import_module("improve_precision_eval")
    result = mod.run_eval(k=10, verbose=False)
    assert result["hit_rate"] >= 0.70, (
        f"Hit Rate@10 = {result['hit_rate']:.3f} < 0.70 threshold"
    )


def test_pass_flag_consistent():
    mod = importlib.import_module("improve_precision_eval")
    result = mod.run_eval(k=10, verbose=False)
    assert result["pass"] == (result["hit_rate"] >= 0.70)


def test_hits_consistent_with_n_queries():
    mod = importlib.import_module("improve_precision_eval")
    result = mod.run_eval(k=10, verbose=False)
    assert 0 <= result["hits"] <= result["n_queries"]
    assert abs(result["hit_rate"] - result["hits"] / result["n_queries"]) < 1e-9
