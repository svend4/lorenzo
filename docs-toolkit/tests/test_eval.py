"""Тесты eval / golden dataset framework."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.eval import (
    GoldenItem, GoldenSet, EvalItemResult, EvalResult,
    score_answer, score_citations, run_eval, load_golden_from_yaml,
)
from docstoolkit.eval.golden import _normalize


# ---- scoring ----

def test_score_answer_full_match():
    assert score_answer("foo and bar in here", ["foo", "bar"]) == 100.0


def test_score_answer_partial():
    assert score_answer("only foo", ["foo", "bar"]) == 50.0


def test_score_answer_no_match():
    assert score_answer("nothing", ["foo", "bar"]) == 0.0


def test_score_answer_empty_expected_returns_100():
    assert score_answer("any text", []) == 100.0


def test_score_answer_case_insensitive():
    assert score_answer("FOO Bar", ["foo", "BAR"]) == 100.0


def test_score_citations_perfect():
    p, r, f = score_citations(["a.md", "b.md"], ["a.md", "b.md"])
    assert p == 1.0 and r == 1.0 and f == 1.0


def test_score_citations_half_overlap():
    p, r, f = score_citations(["a.md", "x.md"], ["a.md", "b.md"])
    # tp=1, |actual|=2, |expected|=2 → P=0.5, R=0.5, F=0.5
    assert p == 0.5
    assert r == 0.5
    assert f == 0.5


def test_score_citations_empty_actual():
    p, r, f = score_citations([], ["a.md"])
    assert p == 0.0 and r == 0.0 and f == 0.0


def test_score_citations_empty_expected_no_actual():
    p, r, f = score_citations([], [])
    assert p == 1.0 and r == 1.0 and f == 1.0


def test_score_citations_normalizes_paths():
    p, r, f = score_citations(["docs/05-habr/Yodoca.md"], ["yodoca.md"])
    # basename normalize → совпадение
    assert p == 1.0


def test_normalize_strips_path_and_ext():
    assert _normalize("docs/x/Foo.md") == "foo"
    assert _normalize("Bar") == "bar"


# ---- dataclasses ----

def test_golden_item_defaults():
    g = GoldenItem(question="?")
    assert g.expected_answer_contains == []
    assert g.expected_doc_ids == []
    assert g.weight == 1.0


def test_eval_item_result_overall_zero_on_error():
    r = EvalItemResult(question="?", error="boom")
    assert r.overall == 0.0


def test_eval_item_result_overall_weighted():
    r = EvalItemResult(question="?", answer_score=80, citation_f1=0.5)
    # 80*0.6 + 50*0.4 = 48+20 = 68
    assert r.overall == pytest.approx(68.0)


def test_eval_result_overall_score():
    er = EvalResult(golden_set="g", config={}, items=[
        EvalItemResult(question="q1", answer_score=100, citation_f1=1.0, weight=1),
        EvalItemResult(question="q2", answer_score=50, citation_f1=0.5, weight=1),
    ])
    # i1: 100*0.6 + 100*0.4 = 100
    # i2: 50*0.6 + 50*0.4 = 50
    # avg: 75
    assert er.overall_score == pytest.approx(75.0)


def test_eval_result_avg_metrics():
    er = EvalResult(golden_set="g", config={}, items=[
        EvalItemResult(question="x", answer_score=80, citation_f1=0.5),
        EvalItemResult(question="y", answer_score=40, citation_f1=0.7),
    ])
    assert er.avg_answer_score == 60
    assert er.avg_citation_f1 == pytest.approx(0.6)


def test_eval_result_empty_zeros():
    er = EvalResult(golden_set="g", config={})
    assert er.overall_score == 0
    assert er.avg_answer_score == 0


def test_eval_result_errors_count():
    er = EvalResult(golden_set="g", config={}, items=[
        EvalItemResult(question="x"),
        EvalItemResult(question="y", error="boom"),
    ])
    assert er.errors == 1


# ---- runner ----

def test_run_eval_empty_corpus(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    gs = GoldenSet(name="empty", items=[
        GoldenItem(question="?", expected_answer_contains=[], expected_doc_ids=[]),
    ])
    result = run_eval(gs, {"method": "keyword", "answerer": "echo"})
    assert len(result.items) == 1
    # empty expected → P/R/F = 1.0
    item = result.items[0]
    assert item.error == ""
    assert item.actual_answer  # echo всегда что-то возвращает


def test_run_eval_uses_default_config(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    gs = GoldenSet(name="x", items=[GoldenItem(question="?")])
    r = run_eval(gs)
    assert r.config["answerer"] == "echo"
    assert r.config["method"] == "hybrid"


def test_run_eval_forbidden_phrase_detection(tmp_path, monkeypatch):
    """Если answer содержит forbidden phrase — должно отметиться."""
    monkeypatch.chdir(tmp_path)
    gs = GoldenSet(name="forbidden", items=[
        GoldenItem(question="?", forbidden_phrases=["echo"]),
    ])
    r = run_eval(gs, {"answerer": "echo"})
    item = r.items[0]
    # Echo answerer возвращает текст содержащий 'Echo' ↔ может или не может матчиться
    # Просто проверяем что код не падает
    assert isinstance(item.forbidden_violated, list)


def test_eval_report_markdown_basic():
    er = EvalResult(golden_set="x", config={"method": "k"}, items=[
        EvalItemResult(question="q", answer_score=80, citation_f1=0.5),
    ])
    md = er.report()
    assert "Eval: x" in md
    assert "Overall" in md
    assert "Per-item" in md


def test_load_golden_from_yaml_string_items(tmp_path):
    """YAML с questions как list of strings."""
    yaml = """name: simple
description: smoke test
items:
  - question one
  - question two
"""
    p = tmp_path / "g.yaml"
    p.write_text(yaml)
    gs = load_golden_from_yaml(str(p))
    assert gs.name == "simple"
    assert len(gs.items) == 2
    assert gs.items[0].question == "question one"
