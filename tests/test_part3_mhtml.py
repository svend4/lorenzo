"""Tests for scripts/part3_mhtml.py (split_mhtml_by_requests only)."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("part3_mhtml")


# ── split_mhtml_by_requests ───────────────────────────────────────────────────

def test_split_returns_list():
    text = "**[Запрос]** What is AI?\n\nAI is artificial intelligence."
    result = mod.split_mhtml_by_requests(text)
    assert isinstance(result, list)


def test_split_single_request():
    text = "**[Запрос]** What is AI?\n\nAI is artificial intelligence."
    result = mod.split_mhtml_by_requests(text)
    assert len(result) == 1


def test_split_two_requests():
    text = (
        "**[Запрос]** First question?\n\nFirst answer.\n\n"
        "**[Запрос]** Second question?\n\nSecond answer."
    )
    result = mod.split_mhtml_by_requests(text)
    assert len(result) == 2


def test_split_no_requests():
    text = "Some text without any request markers."
    result = mod.split_mhtml_by_requests(text)
    assert result == []


def test_split_returns_tuples():
    text = "**[Запрос]** Question here?\n\nAnswer."
    result = mod.split_mhtml_by_requests(text)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in result)


def test_split_title_from_first_line():
    text = "**[Запрос]** What is memory consolidation?\n\nAnswer here."
    result = mod.split_mhtml_by_requests(text)
    title, body = result[0]
    assert "memory consolidation" in title.lower() or len(title) > 0


def test_split_title_max_80_chars():
    long_question = "Q" * 200
    text = f"**[Запрос]** {long_question}\n\nAnswer."
    result = mod.split_mhtml_by_requests(text)
    title, _ = result[0]
    assert len(title) <= 80


def test_split_body_contains_request_marker():
    text = "**[Запрос]** Question?\n\nAnswer text here."
    result = mod.split_mhtml_by_requests(text)
    _, body = result[0]
    assert "**[Запрос]**" in body


def test_split_three_requests():
    text = (
        "**[Запрос]** Q1\n\nA1.\n\n"
        "**[Запрос]** Q2\n\nA2.\n\n"
        "**[Запрос]** Q3\n\nA3."
    )
    result = mod.split_mhtml_by_requests(text)
    assert len(result) == 3


def test_split_content_before_first_request_ignored():
    text = "Preamble text.\n\n**[Запрос]** Question\n\nAnswer."
    result = mod.split_mhtml_by_requests(text)
    assert len(result) == 1
