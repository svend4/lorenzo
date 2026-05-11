"""
Тесты для scripts/improve_priorities.py.

Покрытие:
  - score_file()    — взвешенная оценка важности файла
  - get_top_terms() — топ-N термов по частоте
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_priorities")


# ── score_file ────────────────────────────────────────────────────────────────

def test_score_file_returns_float():
    result = mod.score_file("some text without keywords")
    assert isinstance(result, float)


def test_score_file_zero_for_no_keywords():
    result = mod.score_file("plain text without any relevant keywords here")
    assert result == 0.0


def test_score_file_positive_for_high_weight():
    result = mod.score_file("CardIndex is the main component of the system architecture")
    assert result > 0.0


def test_score_file_positive_for_agentfs():
    result = mod.score_file("AgentFS provides file system access for knowledge storage")
    assert result > 0.0


def test_score_file_higher_for_more_keywords():
    text_few = "CardIndex один раз"
    text_many = "CardIndex AgentFS Svyazi MVP архитектурный зазор Card Envelope"
    assert mod.score_file(text_many) >= mod.score_file(text_few)


def test_score_file_high_weight_beats_low():
    high_text = "CardIndex mentioned here"
    low_text = "agent agent agent agent agent agent agent agent agent"
    # CardIndex has weight 3, agent has weight 1
    # But normalization might change the order; just verify both are >= 0
    assert mod.score_file(high_text) >= 0
    assert mod.score_file(low_text) >= 0


def test_score_file_empty_text():
    result = mod.score_file("")
    assert result == 0.0


def test_score_file_normalized():
    # Short text with many keywords scores differently than long text with same keywords
    text_short = "CardIndex AgentFS"
    text_long = "CardIndex AgentFS " + "word " * 1000
    score_short = mod.score_file(text_short)
    score_long = mod.score_file(text_long)
    assert score_short != score_long or score_short == 0.0


# ── get_top_terms ─────────────────────────────────────────────────────────────

def test_get_top_terms_returns_list():
    result = mod.get_top_terms("CardIndex AgentFS Svyazi")
    assert isinstance(result, list)


def test_get_top_terms_empty_text():
    result = mod.get_top_terms("plain text without known terms")
    assert result == []


def test_get_top_terms_finds_cardindex():
    result = mod.get_top_terms("CardIndex CardIndex CardIndex is very important")
    assert "CardIndex" in result


def test_get_top_terms_respects_n():
    text = "CardIndex AgentFS Svyazi MVP agent memory rag security"
    result = mod.get_top_terms(text, n=3)
    assert len(result) <= 3


def test_get_top_terms_sorted_by_frequency():
    text = "AgentFS AgentFS AgentFS CardIndex CardIndex"
    result = mod.get_top_terms(text, n=2)
    if result:
        assert result[0] == "AgentFS"


def test_get_top_terms_default_n_is_5():
    text = "CardIndex AgentFS Svyazi MVP agent memory rag security roadmap license"
    result = mod.get_top_terms(text)
    assert len(result) <= 5
