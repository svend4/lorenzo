"""
Тесты для scripts/improve_stats.py.

Покрытие:
  - analyze_file()  — детальная статистика файла
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_stats")


# ── analyze_file ──────────────────────────────────────────────────────────────

def test_analyze_file_returns_dict():
    result = mod.analyze_file("# Title\n\nContent here.")
    assert isinstance(result, dict)


def test_analyze_file_has_required_keys():
    result = mod.analyze_file("# Title\n\nContent here.")
    for key in ("words", "chars", "h1", "h2", "h3", "tables", "code", "links_i", "links_e", "images", "bold", "todos"):
        assert key in result


def test_analyze_file_counts_words():
    result = mod.analyze_file("one two three four five")
    assert result["words"] == 5


def test_analyze_file_counts_chars():
    text = "hello"
    result = mod.analyze_file(text)
    assert result["chars"] == 5


def test_analyze_file_counts_h1():
    result = mod.analyze_file("# Title\n\nContent.\n")
    assert result["h1"] == 1


def test_analyze_file_counts_h2():
    result = mod.analyze_file("## Section\n\nContent.\n")
    assert result["h2"] == 1


def test_analyze_file_counts_h3():
    result = mod.analyze_file("### Sub Section\n\nContent.\n")
    assert result["h3"] == 1


def test_analyze_file_counts_code_blocks():
    result = mod.analyze_file("```python\ncode\n```\n```yaml\nconfig\n```\n")
    assert result["code"] == 2


def test_analyze_file_counts_internal_links():
    result = mod.analyze_file("[Link](docs/file.md) and [Other](other.md)")
    assert result["links_i"] == 2


def test_analyze_file_counts_external_links():
    result = mod.analyze_file("See https://example.com and https://google.com")
    assert result["links_e"] == 2


def test_analyze_file_counts_todos():
    result = mod.analyze_file("TODO: fix this. FIXME: another. HACK: workaround.")
    assert result["todos"] == 3


def test_analyze_file_counts_bold():
    result = mod.analyze_file("**Bold text** and **another bold**.")
    assert result["bold"] == 2


def test_analyze_file_empty():
    result = mod.analyze_file("")
    assert result["words"] == 0
    assert result["h1"] == 0


def test_analyze_file_counts_images():
    result = mod.analyze_file("![Image](img.png) text here.")
    assert result["images"] == 1
