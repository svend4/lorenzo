"""Тесты A/B testing experiments framework."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.experiments import (
    Experiment, ExperimentResult, VariantResult,
    run_experiment, run_variant,
)
from docstoolkit.experiments.types import QueryRun
from docstoolkit.experiments.runner import load_experiment_from_yaml


def test_experiment_dataclass():
    e = Experiment(
        name="x",
        variants=[{"name": "A"}, {"name": "B"}],
        questions=["q1", "q2"],
    )
    assert e.name == "x"
    assert e.variant_names == ["A", "B"]
    assert len(e.questions) == 2


def test_experiment_defaults():
    e = Experiment(name="x", variants=[], questions=[])
    assert e.metric == "duration_ms"
    assert e.seed == 42
    assert e.description == ""


def test_query_run_defaults():
    r = QueryRun(question="?", answer="!")
    assert r.duration_ms == 0
    assert r.tokens == 0
    assert r.cost == 0.0
    assert r.error == ""
    assert r.citations == []


def test_variant_result_total_duration():
    vr = VariantResult(name="A", config={}, runs=[
        QueryRun(question="q1", answer="a1", duration_ms=100),
        QueryRun(question="q2", answer="a2", duration_ms=200),
    ])
    assert vr.total_duration_ms == 300


def test_variant_result_avg_duration():
    vr = VariantResult(name="A", config={}, runs=[
        QueryRun(question="q1", answer="a1", duration_ms=100),
        QueryRun(question="q2", answer="a2", duration_ms=200),
    ])
    assert vr.avg_duration_ms == 150.0


def test_variant_result_median_duration():
    vr = VariantResult(name="A", config={}, runs=[
        QueryRun(question="q1", answer="a1", duration_ms=100),
        QueryRun(question="q2", answer="a2", duration_ms=200),
        QueryRun(question="q3", answer="a3", duration_ms=300),
    ])
    assert vr.median_duration_ms == 200


def test_variant_result_empty_zero_props():
    vr = VariantResult(name="A", config={}, runs=[])
    assert vr.total_duration_ms == 0
    assert vr.avg_duration_ms == 0
    assert vr.median_duration_ms == 0
    assert vr.success_rate == 0


def test_variant_result_total_tokens_cost():
    vr = VariantResult(name="A", config={}, runs=[
        QueryRun(question="?", answer="!", tokens=10, cost=0.001),
        QueryRun(question="?", answer="!", tokens=20, cost=0.002),
    ])
    assert vr.total_tokens == 30
    assert vr.total_cost == pytest.approx(0.003)


def test_variant_result_success_rate():
    vr = VariantResult(name="A", config={}, runs=[
        QueryRun(question="?", answer="!"),
        QueryRun(question="?", answer="", error="boom"),
        QueryRun(question="?", answer="!"),
    ])
    assert vr.errors == 1
    assert vr.success_rate == pytest.approx(2/3 * 100)


def test_experiment_result_compare_basic():
    exp = Experiment(name="t", variants=[{"name": "A"}], questions=["?"])
    er = ExperimentResult(
        experiment=exp,
        variant_results=[
            VariantResult(name="A", config={}, runs=[
                QueryRun(question="?", answer="!", duration_ms=50, tokens=10),
            ]),
        ],
        duration_ms=100,
    )
    md = er.compare()
    assert "Experiment: t" in md
    assert "Summary" in md
    assert "`A`" in md
    assert "100%" in md
    assert "50" in md  # duration


def test_experiment_result_compare_two_variants_verdict():
    exp = Experiment(name="ab", variants=[{"name": "C"}, {"name": "T"}],
                     questions=["?"])
    er = ExperimentResult(
        experiment=exp,
        variant_results=[
            VariantResult(name="C", config={}, runs=[
                QueryRun(question="?", answer="a", duration_ms=200, cost=0.01),
            ]),
            VariantResult(name="T", config={}, runs=[
                QueryRun(question="?", answer="a", duration_ms=100, cost=0.02),
            ]),
        ],
    )
    md = er.compare()
    assert "Verdict" in md
    assert "Fastest" in md
    assert "`T`" in md  # T is faster
    assert "Cheapest" in md
    assert "`C`" in md  # C is cheaper
    # delta: (100-200)/200 = -50%
    assert "-50.0%" in md


def test_experiment_result_compare_empty():
    exp = Experiment(name="x", variants=[], questions=[])
    er = ExperimentResult(experiment=exp, variant_results=[])
    md = er.compare()
    assert "нет результатов" in md.lower() or "no results" in md.lower()


def test_run_variant_with_echo(tmp_path, monkeypatch):
    """Прогон echo answerer на вопросах."""
    monkeypatch.chdir(tmp_path)
    cfg = {"name": "test-echo", "method": "keyword", "answerer": "echo"}
    vr = run_variant(cfg, ["question1", "question2"])
    assert vr.name == "test-echo"
    assert len(vr.runs) == 2
    # Echo всегда отвечает (даже на пустом корпусе — fallback)
    for run in vr.runs:
        assert run.question in ("question1", "question2")


def test_run_experiment_executes_all_variants(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    exp = Experiment(
        name="multi-variant",
        variants=[
            {"name": "v1", "method": "keyword", "answerer": "echo"},
            {"name": "v2", "method": "hybrid", "answerer": "echo"},
        ],
        questions=["q?"],
    )
    er = run_experiment(exp)
    assert er.experiment.name == "multi-variant"
    assert len(er.variant_results) == 2
    assert er.variant_results[0].name == "v1"
    assert er.variant_results[1].name == "v2"
    assert er.duration_ms >= 0


def test_load_experiment_from_yaml_scalar_fields(tmp_path):
    """Минимальный YAML-парсер: scalars + flat list of strings."""
    yaml_text = """name: yaml-test
description: from YAML
metric: tokens
questions:
  - first
  - second
"""
    p = tmp_path / "exp.yaml"
    p.write_text(yaml_text)
    exp = load_experiment_from_yaml(str(p))
    assert exp.name == "yaml-test"
    assert exp.description == "from YAML"
    assert exp.questions == ["first", "second"]
    assert exp.metric == "tokens"


def test_load_experiment_from_yaml_defaults_when_missing(tmp_path):
    """Поля отсутствуют в YAML → дефолты."""
    yaml_text = """name: minimal
"""
    p = tmp_path / "exp.yaml"
    p.write_text(yaml_text)
    exp = load_experiment_from_yaml(str(p))
    assert exp.name == "minimal"
    assert exp.description == ""
    assert exp.metric == "duration_ms"
    assert exp.variants == []
    assert exp.questions == []
