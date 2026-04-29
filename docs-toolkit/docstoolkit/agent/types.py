"""Типы для agent loop."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable


@dataclass
class Tool:
    """Один инструмент агента.

    fn: вызывается с **kwargs из tool_call. Возвращает str (для LLM context).
    schema: JSON Schema для inputs (как у MCP).
    """
    name: str
    fn: Callable
    description: str
    input_schema: dict = field(default_factory=lambda: {"type": "object", "properties": {}})

    def call(self, **kwargs) -> str:
        try:
            result = self.fn(**kwargs)
            if not isinstance(result, str):
                import json as _json
                result = _json.dumps(result, ensure_ascii=False)
            return result[:5000]  # max output per tool call
        except Exception as e:
            return f"❌ Ошибка инструмента {self.name}: {e}"


@dataclass
class ToolCall:
    """Один вызов инструмента."""
    name: str
    inputs: dict
    output: str = ""
    duration_ms: int = 0
    error: str = ""


@dataclass
class AgentStep:
    """Один шаг agent loop."""
    iteration: int
    thought: str = ""               # LLM-планирование (опционально)
    tool_calls: list[ToolCall] = field(default_factory=list)
    answer: str = ""                # финальный ответ (если есть)
    is_final: bool = False
    ts: str = field(default_factory=lambda: datetime.now().isoformat(timespec='seconds'))


@dataclass
class AgentResult:
    """Итог работы агента."""
    task: str
    answer: str
    steps: list[AgentStep] = field(default_factory=list)
    total_iterations: int = 0
    total_tool_calls: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    duration_ms: int = 0
    halted_reason: str = ""         # max_iter | error | done
    ts: str = field(default_factory=lambda: datetime.now().isoformat(timespec='seconds'))

    def to_markdown(self) -> str:
        lines = [f"# {self.task}\n"]
        lines.append(f"**Final answer:** {self.answer}\n")
        lines.append(f"**Iterations:** {self.total_iterations} | "
                     f"**Tool calls:** {self.total_tool_calls} | "
                     f"**Cost:** ${self.total_cost:.4f}\n")
        lines.append("\n## Trace\n")
        for s in self.steps:
            lines.append(f"\n### Step {s.iteration}")
            if s.thought:
                lines.append(f"_thought:_ {s.thought[:200]}")
            for tc in s.tool_calls:
                lines.append(f"- 🔧 `{tc.name}({tc.inputs})` → {len(tc.output)} chars")
            if s.is_final:
                lines.append(f"_final:_ {s.answer[:200]}")
        return "\n".join(lines)
