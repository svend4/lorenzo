---
date: 2026-06-05
tags: [memory, rag, orchestration, ingestion, architecture]
state: normalized
---

# LLM Observability & AI Agent Tracing: semantic span typing и 6 open-source инструментов

<!-- toc-auto -->
<!-- tags: antipov-llm-observability-agent-tracing-opentelemetry, docs -->


<!-- summary -->
> `antipov-llm-observability-agent-tracing-opentelemetry` — раздел документации проекта Lorenzo.


> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

**Автор:** antipov_dmitry  
**Хабр:** https://habr.com/ru/articles/972480/  
**GitHub:** нет (примеры в статье, инструменты — внешние)  
**Слой:** orchestration / analytics  
**Дата:** декабрь 2025  
**Уникальность:** Единственная русскоязычная статья, переосмысливающая observability для LLM-агентов через *semantic span typing* — вместо технических метрик (HTTP status, duration, token count) трассировка когнитивного слоя: `llm.reasoning`, `agent.planning`, `agent.observation`, `agent.memory`. Таксономия production-багов агентов (40% — галлюцинация параметров инструментов, context drift, RAG cascade failure). Сравнение 6 open-source платформ: Langfuse / Phoenix / OpenLIT / Langtrace / LangWatch / Lunary.

## Проблема: классическая observability не работает для LLM-агентов

```
Традиционный мониторинг (Prometheus + Grafana):
  → Метрики: HTTP 200, latency, RPS — детерминированные сервисы
  → Для LLM: токены/сек, стоимость/запрос — технические метрики
  → Что пропускаем:
    * "Почему агент пошёл не туда?"
    * "Где именно рассуждение сломалось?"
    * "Контекст drift или переполнение?"
    * "Какой инструмент вызвался с неверными параметрами?"

Основные классы production-багов LLM-агентов:
  → ~40%: галлюцинация параметров инструментов
    (агент вызывает search(query=None) вместо search(query="запрос"))
  → Context drift: не переполнение, а постепенный уход от задачи
  → RAG cascade failure: первый retrieval неудачен → весь chain деградирует
  → "Кроличья нора": агент зациклился на re-invocation одного инструмента
```

## Semantic Span Typing: новая парадигма трассировки

```python
# antipov_dmitry: LLM Observability & AI Agent Tracing
# habr.com/ru/articles/972480

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from dataclasses import dataclass, field
from typing import Optional, Any
import time

# Semantic span types (новая таксономия для LLM-агентов)
class LLMSpanType:
    LLM_CALL = "llm.call"
    LLM_REASONING = "llm.reasoning"      # внутренняя цепочка рассуждений
    AGENT_PLANNING = "agent.planning"    # выбор следующего действия
    AGENT_OBSERVATION = "agent.observation"  # обработка результата инструмента
    AGENT_MEMORY = "agent.memory"        # чтение/запись памяти
    WORKFLOW_STATE = "workflow.state_transition"  # переход состояния в графе
    RAG_RETRIEVAL = "rag.retrieval"
    RAG_RERANKING = "rag.reranking"
    TOOL_CALL = "tool.call"


@dataclass
class SemanticSpanAttributes:
    """
    Атрибуты semantic span — когнитивный слой поверх технического.

    Классический span: duration=1.2s, status=200, tokens=450
    Semantic span: + thought_process + confidence + alternative_paths
    """
    # Стандартные технические метрики
    model_name: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: float
    cost_usd: float

    # НОВОЕ: когнитивный слой
    thought_process: Optional[str] = None      # CoT reasoning (если доступен)
    confidence_score: Optional[float] = None   # уверенность модели (0-1)
    alternative_paths: list[str] = field(default_factory=list)  # отброшенные варианты
    context_drift_score: Optional[float] = None  # насколько ушли от задачи


class LLMAgentTracer:
    """
    Трассировка LLM-агента с semantic span typing.
    Интеграция с OpenTelemetry → любой backend (Langfuse/Phoenix/Grafana).
    """

    def __init__(self, service_name: str, exporter_endpoint: str):
        provider = TracerProvider()
        exporter = OTLPSpanExporter(endpoint=exporter_endpoint)
        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)
        self.tracer = trace.get_tracer(service_name)

    def trace_llm_call(self, model: str, prompt: str,
                        span_type: str = LLMSpanType.LLM_CALL):
        """
        Контекстный менеджер для трассировки LLM-вызова.
        Автоматически записывает cognitive attributes.
        """
        return self.tracer.start_as_current_span(
            span_type,
            attributes={
                "llm.model": model,
                "llm.prompt_preview": prompt[:200],
                "span.type": span_type
            }
        )

    def trace_agent_step(self, step_type: str, agent_state: dict):
        """
        Трассировка шага агента с когнитивными атрибутами.
        step_type: LLMSpanType.AGENT_PLANNING / AGENT_OBSERVATION / etc.
        """
        with self.tracer.start_as_current_span(step_type) as span:
            span.set_attribute("agent.current_task", agent_state.get("task", ""))
            span.set_attribute("agent.step_number", agent_state.get("step", 0))
            span.set_attribute("agent.tools_used", str(agent_state.get("tools_used", [])))

            # Когнитивные метрики
            context_drift = self._compute_context_drift(agent_state)
            span.set_attribute("agent.context_drift", context_drift)

            if context_drift > 0.4:
                span.set_attribute("agent.drift_warning", True)
                span.add_event("context_drift_detected", {
                    "drift_score": context_drift,
                    "original_task": agent_state.get("original_task", "")
                })

            yield span

    def _compute_context_drift(self, agent_state: dict) -> float:
        """
        Context drift score: насколько текущий контекст ушёл от исходной задачи.
        Используется cosine similarity текущего vs исходного embedding.
        Высокий drift = агент занялся "не тем".
        """
        original = agent_state.get("original_task_embedding")
        current = agent_state.get("current_context_embedding")
        if original is None or current is None:
            return 0.0

        # Cosine similarity (1 = идентично, 0 = ортогонально)
        similarity = float((original * current).sum() /
                           (original.norm() * current.norm()))
        return 1.0 - similarity  # drift = 1 - similarity
```

## Детектирование production-багов агентов

```python
class AgentBugDetector:
    """
    Детектирование ключевых классов багов LLM-агентов по трассам.
    """

    def detect_parameter_hallucination(self,
                                        tool_call_span: dict) -> bool:
        """
        Галлюцинация параметров: агент вызвал инструмент с None/пустыми параметрами.
        ~40% production-багов агентов — этот класс.
        """
        tool_inputs = tool_call_span.get("tool.inputs", {})
        schema = self._get_tool_schema(tool_call_span["tool.name"])

        for required_param in schema.get("required", []):
            value = tool_inputs.get(required_param)
            if value is None or value == "" or value == []:
                return True  # галлюцинация параметра

        return False

    def detect_rabbit_hole(self,
                            agent_trace: list[dict],
                            window: int = 5) -> bool:
        """
        "Кроличья нора": агент повторяет один и тот же инструмент
        с похожими параметрами без прогресса.
        """
        if len(agent_trace) < window:
            return False

        recent_tools = [s["tool.name"] for s in agent_trace[-window:]
                        if s.get("span.type") == LLMSpanType.TOOL_CALL]

        # Если >70% вызовов — один инструмент → кроличья нора
        if not recent_tools:
            return False

        from collections import Counter
        most_common_count = Counter(recent_tools).most_common(1)[0][1]
        return most_common_count / len(recent_tools) > 0.7

    def detect_rag_cascade_failure(self,
                                    trace: list[dict]) -> dict:
        """
        RAG cascade failure: первый retrieval вернул мало → весь chain деградирует.
        Детектируется по низкому retrieval score на первом шаге.
        """
        rag_spans = [s for s in trace if s.get("span.type") == LLMSpanType.RAG_RETRIEVAL]
        if not rag_spans:
            return {"detected": False}

        first_rag = rag_spans[0]
        first_score = first_rag.get("rag.top_score", 1.0)

        if first_score < 0.5:
            return {
                "detected": True,
                "first_retrieval_score": first_score,
                "recommendation": (
                    "Рассмотреть fallback стратегию при low retrieval score: "
                    "переформулировать запрос или запросить clarification"
                )
            }
        return {"detected": False}
```

## Сравнение 6 open-source платформ

```python
OBSERVABILITY_PLATFORMS = {
    "Langfuse": {
        "storage": "PostgreSQL",
        "deployment": "Docker Compose / Cloud",
        "key_feature": "Production telemetry, native LangGraph integration",
        "strengths": ["Богатый UI", "LangGraph трассировка", "Dataset management"],
        "weakness": "Нет GPU метрик",
        "best_for": "Production LangGraph/LangChain агенты",
        "pip": "pip install langfuse"
    },

    "Phoenix": {
        "storage": "SQLite (локально)",
        "deployment": "Локальный (Arize)",
        "key_feature": "Span replay + drift detection через embeddings",
        "strengths": ["Анализ post-mortem", "Embedding drift", "Replay"],
        "weakness": "Не для real-time production",
        "best_for": "Отладка и исследование",
        "pip": "pip install arize-phoenix"
    },

    "OpenLIT": {
        "storage": "ClickHouse / Grafana stack",
        "deployment": "Self-hosted",
        "key_feature": "GPU metrics через NVIDIA DCGM + Prometheus/Tempo",
        "strengths": ["LLM + GPU correlation", "Prometheus интеграция", "Cost tracking"],
        "weakness": "Сложная настройка",
        "best_for": "Self-hosted + GPU мониторинг",
        "pip": "pip install openlit"
    },

    "Langtrace": {
        "storage": "Cloud / Self-hosted",
        "deployment": "TypeScript/JS native",
        "key_feature": "React UI компоненты для embedding в приложение",
        "strengths": ["JS/TS нативный", "Embed в продукт"],
        "weakness": "Слабее для Python-стека",
        "best_for": "TypeScript/Node.js приложения"
    },

    "LangWatch": {
        "storage": "Cloud",
        "deployment": "SaaS / Self-hosted",
        "key_feature": "Real-time quality assessment: toxicity/hallucination guardrails",
        "strengths": ["Встроенные guardrails", "Quality gates"],
        "weakness": "Дороже при масштабе",
        "best_for": "Нужны guardrails + observability в одном"
    },

    "Lunary": {
        "storage": "PostgreSQL",
        "deployment": "Fast deploy",
        "key_feature": "Prompt versioning + A/B testing",
        "strengths": ["Быстрый старт", "A/B тесты промптов"],
        "weakness": "Меньше возможностей для agent трассировки",
        "best_for": "Быстрый MVP + prompt experiments"
    }
}


DECISION_MATRIX = {
    "production_langgraph": "Langfuse",
    "gpu_heavy_workload": "OpenLIT",
    "debugging_analysis": "Phoenix",
    "typescript_stack": "Langtrace",
    "need_guardrails": "LangWatch",
    "fast_mvp": "Lunary"
}
```

## Архитектура post-mortem vs real-time

```python
OBSERVABILITY_PARADIGMS = {
    "real_time_monitoring": {
        "когда_подходит": "Детерминированные сервисы (HTTP API, базы данных)",
        "для_LLM_ограничения": [
            "LLM недетерминированы → живые дашборды шумные",
            "Агент зашёл не туда → real-time не объяснит почему",
            "Context drift → нужна полная история, не текущий срез"
        ]
    },

    "post_mortem_analysis": {
        "когда_подходит": "LLM-агенты, сложные reasoning chains",
        "преимущества": [
            "Полная трасса от начала до конца",
            "Можно воспроизвести: span replay (Phoenix)",
            "DAG-с-циклами: граф реального обхода агента",
            "Сравнить несколько неудачных запусков"
        ],
        "key_insight": (
            "Агентные баги проявляются в последовательности решений, "
            "не в одном моменте времени. Нужна полная история."
        )
    }
}

SYSTEM_PROFILE = {
    "автор": "antipov_dmitry (Дмитрий Антипов, 46 статей на Хабре)",
    "статус": "Обзор + оригинальная концепция (не библиотека)",
    "ключевая_концепция": "Semantic Span Typing для LLM-агентов",
    "инструменты": "6 open-source платформ (Langfuse, Phoenix, OpenLIT, Langtrace, LangWatch, Lunary)",
    "backend": "OpenTelemetry (OTLP) — vendor-neutral"
}
```

## Применение к Lorenzo

```python
# Lorenzo: LLM Observability для мониторинга MCP-сервера и gateway

class LorenzoObservabilitySetup:
    """
    antipov_dmitry паттерн для Lorenzo:
    Semantic span typing для gateway.py и mcp_server.py.
    Детектировать: какие запросы к /api/ask деградируют?
    Когда BM25-retrieval возвращает low score → RAG cascade failure?
    """

    def instrument_gateway(self, app):
        """
        Добавить OpenTelemetry трассировку к gateway.py.
        Каждый /api/ask = один trace с semantic spans:
        - rag.retrieval (BM25 + TF-IDF поиск)
        - llm.reasoning (если LLM обогащение включено)
        - workflow.state_transition (какой рецепт выбран)
        """
        tracer = LLMAgentTracer(
            service_name="lorenzo-gateway",
            exporter_endpoint="http://localhost:4317"  # Langfuse OTLP
        )
        return tracer

    def detect_retrieval_degradation(self,
                                      query: str,
                                      results: list) -> dict:
        """
        Если top-1 BM25 score < threshold → вероятен RAG cascade failure.
        Рекомендация: расширить корпус или переформулировать запрос.
        """
        if not results:
            return {"degraded": True, "reason": "empty_results"}
        top_score = results[0].get("score", 0)
        return {
            "degraded": top_score < 0.3,
            "top_score": top_score,
            "query": query
        }
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **LLM Observability + LangGraph (R44)** | Semantic spans для каждого LangGraph узла + checkpoint correlate с трассой |
| **LLM Observability + LangFuse (R38)** | LangFuse как backend для semantic span typing (OTLP → PostgreSQL) |
| **LLM Observability + SherlockOps (R42)** | SherlockOps расследует баги обнаруженные observability (context drift alert → SherlockOps) |
| **LLM Observability + LOCK-R (R43)** | Bayesian Regret метрика + span-level tracing = понять где CoT ошибся |
| **LLM Observability + Lorenzo Gateway** | /api/ask с полной трассой: знать когда BM25 деградирует, какой раздел docs/ не работает |

## Контакт

- Статья: https://habr.com/ru/articles/972480/ (декабрь 2025)
- Автор: antipov_dmitry (Дмитрий Антипов, Хабр, 46 публикаций)
- Langfuse: langfuse.com / github.com/langfuse/langfuse
- Phoenix: docs.arize.com/phoenix
- OpenLIT: openlit.io
- OpenTelemetry: opentelemetry.io
- Смежная (LangFuse observability R38): docs/06-discovery/round-38/
- Смежная (LangGraph checkpointing, R44): docs/06-discovery/round-44/projects/langgraph-checkpoint-fault-tolerant-agents.md
- Смежная (SherlockOps SRE агент, R42): docs/06-discovery/round-42/projects/sherlockops-llm-alert-investigation-devops.md

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
