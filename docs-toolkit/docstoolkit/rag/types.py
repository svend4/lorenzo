"""Типы данных для RAG."""
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


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
class TraceEvent:
    """One step of the composition pipeline.

    Phase III.1 — every stage in `RAGPipeline.run()` and `_self_rag_run`
    emits a `TraceEvent` so callers can inspect _why_ the latency budget
    went where it did.

    Fields:
      stage:   short id like "retrieve", "rerank", "self_rag_iter",
               "got_run", "debate_round", "negotiation_auction", "answer"
      t_ms:    wall-clock duration of this stage in milliseconds
      payload: stage-specific dict (e.g. `{"n_passages": 5, "top_score": 0.92}`)
    """
    stage: str
    t_ms: float = 0.0
    payload: dict[str, Any] = field(default_factory=dict)


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
    facets: list = field(default_factory=list)         # Sprint 55 / S2
    provenance: object = None                          # Sprint 61 / I3
    got_result: object = None                          # Sprint 75 / N3
    debate_result: object = None                       # Sprint 72 / I2
    mapreduce_trace: object = None                     # Sprint 78 / I10
    auction_result: object = None                      # Sprint 85 / N2
    at_commit: str = ""                                # Sprint 79 / I8
    trace: list[TraceEvent] = field(default_factory=list)  # Phase III.1

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

    def to_trace_markdown(self) -> str:
        """Phase III.2 — render the per-stage trace as a markdown table.

        Empty if `trace` is empty. Useful for debugging composition
        latency:

            >>> r = ask("q", with_got=True, with_debate=True)
            >>> print(r.to_trace_markdown())
            | Stage             | Time (ms) | Payload |
            ...
        """
        if not self.trace:
            return ""
        lines = [
            f"## Trace ({len(self.trace)} stages, "
            f"sum={sum(ev.t_ms for ev in self.trace):.2f} ms)",
            "",
            "| Stage | Time (ms) | Payload |",
            "|-------|----------:|---------|",
        ]
        for ev in self.trace:
            payload = ", ".join(f"{k}={v}" for k, v in ev.payload.items())
            lines.append(f"| `{ev.stage}` | {ev.t_ms:.3f} | {payload} |")
        return "\n".join(lines)


class _TraceTimer:
    """Context manager that appends a `TraceEvent` to a list on exit.

    Phase III.1 — internal helper for `RAGPipeline.run()` to keep the
    instrumentation overhead small (~1 μs per stage) and avoid
    boilerplate at each call site.

    Usage:
        with _TraceTimer(self.trace, "retrieve") as tt:
            passages = self.retriever.search(...)
            tt.payload["n_passages"] = len(passages)
    """

    def __init__(self, trace: list[TraceEvent], stage: str):
        self.trace = trace
        self.stage = stage
        self.payload: dict[str, Any] = {}
        self._t0 = 0.0

    def __enter__(self):
        self._t0 = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        dt = (time.perf_counter() - self._t0) * 1000.0
        self.trace.append(TraceEvent(
            stage=self.stage, t_ms=dt, payload=dict(self.payload),
        ))
        return False  # don't suppress exceptions
