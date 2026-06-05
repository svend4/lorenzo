"""
Тесты для scripts/ci_probe.py — проверка работоспособности CI.
"""
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("ci_probe")


def test_add_positive():
    assert mod.add(2, 3) == 5


def test_add_negative():
    assert mod.add(-4, 1) == -3


def test_add_zero():
    assert mod.add(0, 0) == 0


def test_palindrome_simple():
    assert mod.is_palindrome("level") is True


def test_palindrome_with_spaces_and_case():
    assert mod.is_palindrome("А роза упала на лапу Азора") is True


def test_palindrome_negative():
    assert mod.is_palindrome("hello") is False


def test_palindrome_empty():
    assert mod.is_palindrome("") is True


def test_word_count_basic():
    assert mod.word_count("Lorenzo Knowledge OS") == 3


def test_word_count_empty():
    assert mod.word_count("") == 0


def test_word_count_multiple_spaces():
    assert mod.word_count("  foo   bar  ") == 2
