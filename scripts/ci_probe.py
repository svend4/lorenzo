"""
ci_probe.py — небольшой пробник для проверки CI-пайплайна.
Содержит три чистые функции без зависимостей. Используется тестами
в tests/test_ci_probe.py.
"""
from __future__ import annotations


def add(a: int, b: int) -> int:
    return a + b


def is_palindrome(text: str) -> bool:
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]


def word_count(text: str) -> int:
    return len(text.split())


if __name__ == "__main__":
    print("add(2, 3) =", add(2, 3))
    print("is_palindrome('А роза упала на лапу Азора') =",
          is_palindrome("А роза упала на лапу Азора"))
    print("word_count('Lorenzo Knowledge OS') =",
          word_count("Lorenzo Knowledge OS"))
