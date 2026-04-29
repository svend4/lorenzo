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


class OpenAIAnswerer(Answerer):
    name = "openai"
    DEFAULT_MODEL = "gpt-4o-mini"
    PRICING = {
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    }

    def __init__(self, api_key: str | None = None):
        try:
            import openai
        except ImportError:
            raise ImportError("Для OpenAIAnswerer: pip install openai")
        self._client = openai.OpenAI(
            api_key=api_key or os.environ.get("OPENAI_API_KEY")
        )

    def answer(self, system: str, user: str, model: str = "") -> tuple[str, int, float]:
        model = model or self.DEFAULT_MODEL
        resp = self._client.chat.completions.create(
            model=model, max_tokens=1500,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        text = resp.choices[0].message.content or ""
        in_tok = resp.usage.prompt_tokens
        out_tok = resp.usage.completion_tokens
        pricing = self.PRICING.get(model, {"input": 0, "output": 0})
        cost = (in_tok * pricing["input"] + out_tok * pricing["output"]) / 1_000_000
        return text, in_tok + out_tok, cost


class OllamaAnswerer(Answerer):
    """Локальный Ollama — бесплатно, требует daemon на localhost:11434."""
    name = "ollama"
    DEFAULT_MODEL = "llama3.2"

    def __init__(self, host: str | None = None):
        import urllib.request
        import urllib.error
        self._urlreq = urllib.request
        self._urlerr = urllib.error
        self.host = host or os.environ.get("OLLAMA_HOST", "http://localhost:11434")

    def answer(self, system: str, user: str, model: str = "") -> tuple[str, int, float]:
        import json as _json
        model = model or self.DEFAULT_MODEL
        payload = _json.dumps({
            "model": model, "stream": False,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }).encode("utf-8")
        req = self._urlreq.Request(
            f"{self.host}/api/chat", data=payload,
            headers={"Content-Type": "application/json"},
        )
        try:
            with self._urlreq.urlopen(req, timeout=120) as resp:
                data = _json.loads(resp.read().decode("utf-8"))
        except self._urlerr.URLError as e:
            raise RuntimeError(f"Ollama недоступен по {self.host}: {e}")

        text = data.get("message", {}).get("content", "")
        in_tok = data.get("prompt_eval_count", 0)
        out_tok = data.get("eval_count", 0)
        return text, in_tok + out_tok, 0.0


class GeminiAnswerer(Answerer):
    name = "gemini"
    DEFAULT_MODEL = "gemini-2.0-flash-exp"
    PRICING = {
        "gemini-2.0-flash-exp": {"input": 0.0, "output": 0.0},
        "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
        "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    }

    def __init__(self, api_key: str | None = None):
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("Для GeminiAnswerer: pip install google-generativeai")
        self._genai = genai
        api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)

    def answer(self, system: str, user: str, model: str = "") -> tuple[str, int, float]:
        model = model or self.DEFAULT_MODEL
        gm = self._genai.GenerativeModel(model_name=model, system_instruction=system)
        resp = gm.generate_content(user)
        text = resp.text or ""
        usage = getattr(resp, "usage_metadata", None)
        in_tok = getattr(usage, "prompt_token_count", 0) if usage else 0
        out_tok = getattr(usage, "candidates_token_count", 0) if usage else 0
        pricing = self.PRICING.get(model, {"input": 0, "output": 0})
        cost = (in_tok * pricing["input"] + out_tok * pricing["output"]) / 1_000_000
        return text, in_tok + out_tok, cost


def register_answerer(name: str, cls: type[Answerer]):
    _REGISTRY[name] = cls


_OPTIONAL = {
    "anthropic": AnthropicAnswerer,
    "openai": OpenAIAnswerer,
    "ollama": OllamaAnswerer,
    "gemini": GeminiAnswerer,
}


def get_answerer(name: str = "echo", **kwargs) -> Answerer:
    """Создаёт answerer. Опциональные провайдеры fallback на echo при ошибке."""
    if name in _OPTIONAL:
        try:
            return _OPTIONAL[name](**kwargs)
        except (ImportError, Exception):
            return EchoAnswerer()
    if name not in _REGISTRY:
        return EchoAnswerer()
    return _REGISTRY[name](**kwargs)


def list_providers() -> list[dict]:
    """Возвращает доступные провайдеры с фактическим статусом deps."""
    result = [{"name": "echo", "available": True, "kind": "mock", "cost": "free"}]
    for name, cls in _OPTIONAL.items():
        kind = "local" if name == "ollama" else "cloud"
        cost = "free" if name == "ollama" else "paid"
        try:
            cls()
            result.append({"name": name, "available": True, "kind": kind, "cost": cost})
        except (ImportError, Exception) as e:
            result.append({"name": name, "available": False, "kind": kind,
                           "error": str(e)[:80]})
    return result
