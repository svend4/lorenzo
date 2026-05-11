"""Tests for improve_precision_eval — Hit Rate@10 ≥ 0.70."""
import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


@pytest.fixture(scope="session")
def eval_result():
    """Run eval once per session; all tests share the result."""
    mod = importlib.import_module("improve_precision_eval")
    return mod.run_eval(k=10, verbose=False)


def test_run_eval_returns_expected_keys(eval_result):
    assert "hit_rate" in eval_result
    assert "hits" in eval_result
    assert "n_queries" in eval_result
    assert "mean_mrr" in eval_result
    assert "pass" in eval_result


def test_hit_rate_threshold(eval_result):
    assert eval_result["hit_rate"] >= 0.70, (
        f"Hit Rate@10 = {eval_result['hit_rate']:.3f} < 0.70 threshold"
    )


def test_pass_flag_consistent(eval_result):
    assert eval_result["pass"] == (eval_result["hit_rate"] >= 0.70)


def test_hits_consistent_with_n_queries(eval_result):
    assert 0 <= eval_result["hits"] <= eval_result["n_queries"]
    assert abs(eval_result["hit_rate"] - eval_result["hits"] / eval_result["n_queries"]) < 1e-9
