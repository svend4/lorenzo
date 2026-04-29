"""Типы данных для RAG."""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Passage:
    """Один пассаж: фрагмент документа с метаданными."""
    text: str
    doc_id: str
    title: str = ""
    score: float = 0.0
    snippet_start: int = 0  # offset в documenta для citation


@dataclass
class RAGQuery:
    """Параметры RAG-запроса."""
    question: str
    top_k: int = 5
    method: str = "hybrid"      # keyword | semantic | hybrid
    answerer: str = "echo"       # echo | anthropic | (custom)
    model: str = "claude-haiku-4-5-20251001"
    max_context_tokens: int = 8000
    include_citations: bool = True
    locale: str = "auto"


@dataclass
class AnswerResult:
    """Результат RAG: ответ + использованные пассажи + метаданные."""
    answer: str
    citations: list[dict] = field(default_factory=list)
    retrieved_passages: list[Passage] = field(default_factory=list)
    query: str = ""
    method: str = ""
    answerer: str = ""
    duration_ms: int = 0
    ts: str = field(default_factory=lambda: datetime.now().isoformat(timespec='seconds'))
    cost_estimate: float = 0.0  # USD
    tokens_used: int = 0
    error: str = ""

    def to_markdown(self) -> str:
        lines = [f"# {self.query}\n"]
        lines.append(self.answer)
        lines.append("")
        if self.citations:
            lines.append("## Источники\n")
            for i, c in enumerate(self.citations, 1):
                lines.append(f"{i}. [{c.get('title', c.get('doc_id', '?'))}]"
                             f"({c.get('doc_id', '')}) — score {c.get('score', 0):.3f}")
        if self.duration_ms:
            lines.append(f"\n_Время: {self.duration_ms}ms · Tokens: {self.tokens_used}_")
        return "\n".join(lines)
