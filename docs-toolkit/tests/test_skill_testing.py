"""Тесты skill testing framework."""
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.skills.testing import (
    _parse_simple_yaml, check_assertions, GoldenTest,
    load_golden_tests, render_results, TestResult,
)


def test_parse_simple_yaml_skill():
    text = "skill: search\ncases:\n  - name: x\n    input: {}\n    expects: {}"
    data = _parse_simple_yaml(text)
    assert data["skill"] == "search"
    assert len(data["cases"]) == 1
    assert data["cases"][0]["name"] == "x"


def test_parse_simple_yaml_inline_list():
    text = ('skill: foo\ncases:\n  - name: c\n    input: {}\n'
            '    expects:\n      mentions: [a, b, c]')
    data = _parse_simple_yaml(text)
    assert data["cases"][0]["expects"]["mentions"] == ["a", "b", "c"]


def test_check_assertions_mentions_pass():
    failures = check_assertions(
        "Hello world this is text",
        {"mentions": ["hello", "text"]}
    )
    assert failures == []


def test_check_assertions_mentions_fail():
    failures = check_assertions(
        "Only this text",
        {"mentions": ["missing"]}
    )
    assert len(failures) == 1
    assert "missing" in failures[0]


def test_check_assertions_not_mentions():
    failures = check_assertions(
        "Contains DROP TABLE statement",
        {"not_mentions": ["DROP"]}
    )
    assert len(failures) == 1


def test_check_assertions_length():
    failures = check_assertions(
        "short",
        {"min_length": 100}
    )
    assert any("min_length" in f for f in failures)

    failures = check_assertions(
        "x" * 1000,
        {"max_length": 100}
    )
    assert any("max_length" in f for f in failures)


def test_check_assertions_required_sections():
    text = "## Header One\nstuff\n## Header Two\nmore"
    failures = check_assertions(
        text,
        {"required_sections": ["Header One", "Missing Section"]}
    )
    assert len(failures) == 1
    assert "Missing Section" in failures[0]


def test_check_assertions_regex():
    failures = check_assertions(
        "Found 42 results",
        {"regex_match": r"Found \d+ results"}
    )
    assert failures == []

    failures = check_assertions(
        "No numbers here",
        {"regex_match": r"\d+ results"}
    )
    assert len(failures) == 1


def test_load_golden_tests(tmp_path):
    f = tmp_path / "search.test.yaml"
    f.write_text(
        "skill: search\ncases:\n  - name: t1\n    input: {}\n    expects:\n      min_length: 100"
    )
    tests = load_golden_tests(tmp_path)
    assert len(tests) == 1
    assert tests[0].skill == "search"
    assert tests[0].name == "t1"


def test_render_results():
    r = TestResult("test1", "search", "ok", duration_ms=5)
    out = render_results([r])
    assert "1 ok" in out
    assert "search" in out


def test_render_results_failures():
    r = TestResult("test1", "search", "fail",
                   failures=["mentions: missing 'x'"], duration_ms=3)
    out = render_results([r])
    assert "1 fail" in out
    assert "missing" in out
