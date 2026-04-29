"""Answerer — LLM-провайдеры для генерации ответа."""
import os
from abc import ABC, abstractmethod

from docstoolkit.rag.types import Passage


class Answerer(ABC):
    name: str = "base"

    @abstractmethod
    def answer(self, system: str, user: str,
               model: str = "") -> tuple[str, int, float]:
        """Возвращает (answer_text, tokens_used, cost_usd)."""
        ...


class EchoAnswerer(Answerer):
    """Mock: возвращает первый пассаж + статистику.

    Полезно для тестов и dry-run.
    """
    name = "echo"

    def answer(self, system: str, user: str,
               model: str = "") -> tuple[str, int, float]:
        # Извлечь первый пассаж из user message
        import re
        m = re.search(r'\[1\]\s+\*\*(.+?)\*\*\n+Источник:\s+`(.+?)`\n+(.+?)(?=\n---|\Z)',
                      user, re.DOTALL)
        if m:
            title = m.group(1)
            doc = m.group(2)
            text = m.group(3).strip()[:300]
            answer = (f"[Echo answerer] Извлёк первый пассаж:\n\n"
                      f"**{title}** ({doc})\n\n{text}\n\n"
                      f"_(для реального ответа: pip install anthropic + установите ANTHROPIC_API_KEY)_")
        else:
            answer = "[Echo answerer] Нет пассажей для ответа."
        return answer, len(user) // 3, 0.0  # ~tokens, $0


class AnthropicAnswerer(Answerer):
    """Использует Anthropic Claude API."""
    name = "anthropic"

    DEFAULT_MODEL = "claude-haiku-4-5-20251001"

    # USD per 1M tokens (приблизительно)
    PRICING = {
        "claude-haiku-4-5-20251001": {"input": 1.0, "output": 5.0},
        "claude-sonnet-4-6": {"input": 3.0, "output": 15.0},
        "claude-opus-4-7": {"input": 15.0, "output": 75.0},
    }

    def __init__(self, api_key: str | None = None):
        try:
            import anthropic
        except ImportError:
            raise ImportError(
                "Для AnthropicAnswerer: pip install anthropic"
            )
        self._anthropic = anthropic
        self._client = anthropic.Anthropic(
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY")
        )

    def answer(self, system: str, user: str,
               model: str = "") -> tuple[str, int, float]:
        model = model or self.DEFAULT_MODEL
        resp = self._client.messages.create(
            model=model,
            max_tokens=1500,
            system=system,
            messages=[{"role": "user", "content": user}],
        )

        # Извлечь текст
        text = "".join(
            block.text for block in resp.content if hasattr(block, "text")
        )

        in_tok = resp.usage.input_tokens
        out_tok = resp.usage.output_tokens
        total = in_tok + out_tok

        pricing = self.PRICING.get(model, {"input": 0, "output": 0})
        cost = (in_tok * pricing["input"] + out_tok * pricing["output"]) / 1_000_000

        return text, total, cost


_REGISTRY: dict[str, type[Answerer]] = {
    "echo": EchoAnswerer,
}


def register_answerer(name: str, cls: type[Answerer]):
    _REGISTRY[name] = cls


def get_answerer(name: str = "echo", **kwargs) -> Answerer:
    """Создаёт answerer. anthropic — опциональный, fallback на echo."""
    if name == "anthropic":
        try:
            return AnthropicAnswerer(**kwargs)
        except (ImportError, Exception):
            return EchoAnswerer()
    if name not in _REGISTRY:
        return EchoAnswerer()
    return _REGISTRY[name](**kwargs)
