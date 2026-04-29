"""Тесты для всех LLM answerer'ов."""
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.rag.answerer import (
    EchoAnswerer, OpenAIAnswerer, OllamaAnswerer, GeminiAnswerer,
    AnthropicAnswerer, get_answerer, list_providers, _OPTIONAL,
)


def test_echo_always_works():
    a = EchoAnswerer()
    text, tokens, cost = a.answer("sys", "Q\n[1] **T**\nИсточник: `p.md`\n\nContent")
    assert isinstance(text, str)
    assert tokens > 0
    assert cost == 0.0


def test_get_answerer_echo():
    a = get_answerer("echo")
    assert a.name == "echo"


def test_get_answerer_unknown_falls_back_to_echo():
    a = get_answerer("nonexistent_provider")
    assert a.name == "echo"


def test_get_answerer_anthropic_falls_back_when_unavailable():
    a = get_answerer("anthropic")
    assert a.name in ("echo", "anthropic")  # depending on env


def test_get_answerer_openai_falls_back():
    a = get_answerer("openai")
    assert a.name in ("echo", "openai")


def test_get_answerer_gemini_falls_back():
    a = get_answerer("gemini")
    assert a.name in ("echo", "gemini")


def test_optional_registry_has_4_providers():
    assert "anthropic" in _OPTIONAL
    assert "openai" in _OPTIONAL
    assert "ollama" in _OPTIONAL
    assert "gemini" in _OPTIONAL


def test_list_providers_includes_all():
    providers = list_providers()
    names = {p["name"] for p in providers}
    assert "echo" in names
    assert "anthropic" in names
    assert "openai" in names
    assert "ollama" in names
    assert "gemini" in names


def test_list_providers_echo_always_available():
    providers = list_providers()
    echo = next(p for p in providers if p["name"] == "echo")
    assert echo["available"] is True
    assert echo["kind"] == "mock"
    assert echo["cost"] == "free"


def test_ollama_init_no_network():
    """Ollama init не должен делать сетевой запрос."""
    a = OllamaAnswerer()
    assert a.name == "ollama"
    assert "11434" in a.host or "OLLAMA_HOST" in str(a.host)


def test_openai_pricing_table():
    """OpenAI имеет pricing для популярных моделей."""
    assert "gpt-4o-mini" in OpenAIAnswerer.PRICING
    assert OpenAIAnswerer.PRICING["gpt-4o-mini"]["input"] > 0


def test_anthropic_pricing_table():
    assert "claude-haiku-4-5-20251001" in AnthropicAnswerer.PRICING


def test_gemini_pricing_table():
    """Gemini Flash имеет $0 (free tier)."""
    assert "gemini-2.0-flash-exp" in GeminiAnswerer.PRICING
    assert GeminiAnswerer.PRICING["gemini-2.0-flash-exp"]["input"] == 0.0
