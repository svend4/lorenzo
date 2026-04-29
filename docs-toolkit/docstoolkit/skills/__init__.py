"""Skill testing framework для docs-toolkit.

Модули:
  - testing.py — golden-output tests для скилов
  - registry.py — open .claude/skills/ + entry_points плагины

Использование:
    from docstoolkit.skills import run_golden_tests

    results = run_golden_tests(skill_dir="my_skill", fixtures_dir="tests/fixtures")
"""
from docstoolkit.skills.testing import (
    GoldenTest, TestResult, run_golden_tests, load_golden_tests,
)
from docstoolkit.skills.registry import (
    list_skills, get_skill_path, discover_skill_dirs,
)

__all__ = [
    "GoldenTest", "TestResult", "run_golden_tests", "load_golden_tests",
    "list_skills", "get_skill_path", "discover_skill_dirs",
]
