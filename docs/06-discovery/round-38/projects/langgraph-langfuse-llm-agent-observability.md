---
date: 2026-06-05
tags: [rag, orchestration, security, ingestion, architecture]
state: normalized
---

# Наблюдаемость LLM-агентов: LangGraph + LangFuse self-hosted

<!-- toc-auto -->
<!-- tags: langgraph-langfuse-llm-agent-observability, docs -->


<!-- summary -->
> `langgraph-langfuse-llm-agent-observability` — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** Vladimir (Хабр, статья 1008300)  
**Хабр:** https://habr.com/ru/articles/1008300/ (Часть 2: https://habr.com/ru/articles/1008402/)  
**GitHub:** нет (код в статье)  
**Слой:** orchestration / analytics  
**Дата:** март 2026  
**Уникальность:** End-to-end разбор иерархической трассировки многоузлового LangGraph-агента (4 роли: Architect/Writer/Critic/Editor) через self-hosted LangFuse. Промпты как код с версионированием и миграциями — "prompts as code" паттерн. Каждый узел графа трейсируется отдельно: входы, выходы, token usage, latency per node.

## Проблема: агенты — черные ящики в production

```
Стандартный LLM-агент в production:
  → Облачные API (Langsmith, Helicone): данные уходят, vendor lock-in
  → Самописный logging: только входы/выходы, нет структуры вызовов
  → Нет версионирования промптов: изменил промпт → непонятно что сломалось

Специфика LangGraph:
  → Граф из узлов, каждый вызывает LLM и инструменты
  → Без трассировки: непонятно где агент "застрял" или "галлюцинирует"
  → Изменение промпта в одном узле ломает весь граф

LangFuse self-hosted решает:
  → Данные не покидают сервер
  → Иерархические трейсы: граф → узел → LLM call → tool call
  → Промпты версионируются отдельно от кода
```

## Архитектура: 4-узловой агент с трассировкой

```python
# LangGraph агент с LangFuse observability
# Из статьи habr.com/ru/articles/1008300

from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langfuse import Langfuse
from langfuse.callback import CallbackHandler
from pydantic_settings import BaseSettings

class AgentSettings(BaseSettings):
    """Конфигурация через .env (pydantic-settings)."""
    langfuse_host: str = "http://localhost:3000"    # self-hosted
    langfuse_public_key: str
    langfuse_secret_key: str
    openai_api_key: str

    class Config:
        env_file = ".env"


settings = AgentSettings()
langfuse = Langfuse(
    host=settings.langfuse_host,
    public_key=settings.langfuse_public_key,
    secret_key=settings.langfuse_secret_key
)

# LangFuse callback — подключается к любому LangChain/LangGraph пайплайну
langfuse_handler = CallbackHandler()


class ContentCreationAgent:
    """
    4-узловой LangGraph агент для создания контента.
    Каждый узел трейсируется отдельно в LangFuse.
    """

    def __init__(self):
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        from typing import TypedDict, Optional

        class AgentState(TypedDict):
            topic: str
            outline: Optional[str]
            draft: Optional[str]
            critique: Optional[str]
            final: Optional[str]

        graph = StateGraph(AgentState)

        # 4 узла: Architect → Writer → Critic → Editor
        graph.add_node("architect", self._architect_node)
        graph.add_node("writer", self._writer_node)
        graph.add_node("critic", self._critic_node)
        graph.add_node("editor", self._editor_node)

        graph.set_entry_point("architect")
        graph.add_edge("architect", "writer")
        graph.add_edge("writer", "critic")
        graph.add_edge("critic", "editor")
        graph.add_edge("editor", END)

        return graph.compile()

    def _architect_node(self, state: dict) -> dict:
        """Узел 1: создать структуру контента."""
        prompt = langfuse.get_prompt("architect-v2")  # промпт из хранилища
        response = self.llm.invoke(
            prompt.compile(topic=state["topic"]),
            config={"callbacks": [langfuse_handler]}  # трейс этого узла
        )
        return {"outline": response.content}

    def _writer_node(self, state: dict) -> dict:
        """Узел 2: написать черновик по структуре."""
        prompt = langfuse.get_prompt("writer-v3")
        response = self.llm.invoke(
            prompt.compile(outline=state["outline"], topic=state["topic"]),
            config={"callbacks": [langfuse_handler]}
        )
        return {"draft": response.content}

    def _critic_node(self, state: dict) -> dict:
        """Узел 3: критика черновика."""
        prompt = langfuse.get_prompt("critic-v1")
        response = self.llm.invoke(
            prompt.compile(draft=state["draft"]),
            config={"callbacks": [langfuse_handler]}
        )
        return {"critique": response.content}

    def _editor_node(self, state: dict) -> dict:
        """Узел 4: финальная правка с учётом критики."""
        prompt = langfuse.get_prompt("editor-v2")
        response = self.llm.invoke(
            prompt.compile(draft=state["draft"], critique=state["critique"]),
            config={"callbacks": [langfuse_handler]}
        )
        return {"final": response.content}

    def run(self, topic: str) -> str:
        result = self.graph.invoke(
            {"topic": topic},
            config={"callbacks": [langfuse_handler]}  # трейс всего графа
        )
        return result["final"]
```

## Prompts as Code: версионирование в LangFuse

```python
class PromptsAsCode:
    """
    Промпты хранятся в LangFuse, не в коде.
    Версионирование + миграции + A/B тестирование.
    """

    def push_prompt_version(self, name: str, template: str,
                             version_note: str):
        """
        Загрузить новую версию промпта в LangFuse.
        Старые версии сохраняются — можно откатиться.
        """
        langfuse.create_prompt(
            name=name,
            prompt=template,
            labels=["production"],  # или "staging", "experiment"
            config={"version_note": version_note}
        )

    def migrate_prompt(self, name: str, old_version: int,
                        new_template: str):
        """
        Безопасная миграция: новая версия → тестирование → продвижение.
        """
        # 1. Создать новую версию (не деплоить сразу)
        self.push_prompt_version(name, new_template, "migration")

        # 2. Протестировать на выборке
        test_results = self._test_prompt(name, new_version=True)

        # 3. Если качество ≥ старой версии — продвинуть
        if test_results["quality"] >= self._get_baseline(name, old_version):
            langfuse.update_prompt(name, labels=["production"])
            print(f"Мигрировали {name}: v{old_version} → latest")
        else:
            print(f"Откат: новая версия хуже на {test_results['delta']:.2f}")


# Пример промпта в LangFuse (хранится как template с переменными)
ARCHITECT_PROMPT_V2 = """
Ты — архитектор контента. Создай структуру для статьи на тему: {{topic}}

Структура должна включать:
1. Проблему/боль читателя
2. 3-5 ключевых разделов
3. Конкретный вывод/CTA

Верни Markdown outline.
"""
```

## Что видно в трейсе LangFuse

```python
TRACE_STRUCTURE = {
    "trace_id": "tr_abc123",
    "name": "content-creation-agent",
    "total_latency_ms": 8420,
    "total_tokens": 3847,
    "total_cost_usd": 0.023,

    "spans": [
        {
            "name": "architect",
            "latency_ms": 1230,
            "prompt_version": "architect-v2",
            "tokens_in": 145,
            "tokens_out": 312,
            "cost_usd": 0.004
        },
        {
            "name": "writer",
            "latency_ms": 3890,
            "prompt_version": "writer-v3",
            "tokens_in": 512,
            "tokens_out": 1840,
            "cost_usd": 0.014
        },
        {
            "name": "critic",
            "latency_ms": 1650,
            "prompt_version": "critic-v1",
            "tokens_in": 1840,
            "tokens_out": 420,
            "cost_usd": 0.003
        },
        {
            "name": "editor",
            "latency_ms": 1650,
            "prompt_version": "editor-v2",
            "tokens_in": 2260,
            "tokens_out": 580,
            "cost_usd": 0.002
        }
    ]
}
# → В UI LangFuse виден граф вызовов, узкие места (writer=46% времени),
#   cost по каждому узлу, версия промпта на каждом шаге
```

## Self-hosted LangFuse: Docker Compose

```yaml
# docker-compose.yml для self-hosted LangFuse
# Данные не покидают инфраструктуру

version: "3.8"
services:
  langfuse-server:
    image: langfuse/langfuse:latest
    environment:
      DATABASE_URL: "postgresql://langfuse:secret@db:5432/langfuse"
      NEXTAUTH_SECRET: "your-secret-here"
      NEXTAUTH_URL: "http://localhost:3000"
      SALT: "your-salt"
    ports:
      - "3000:3000"
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: langfuse
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: langfuse
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Применение к Lorenzo

```python
# Lorenzo: трассировка Q&A пайплайна через LangFuse

from langfuse import Langfuse

langfuse = Langfuse(host="http://localhost:3000", ...)

class ObservableLorenzoPipeline:
    """
    improve_llm_qa.py + LangFuse = видимость каждого шага:
    BM25 retrieval latency, LLM generation cost, answer quality.
    """

    def ask(self, question: str) -> dict:
        trace = langfuse.trace(name="lorenzo-qa", input={"question": question})

        # Span 1: поиск документов
        with trace.span(name="retrieval") as span:
            docs = self.retriever.search(question, top_k=5)
            span.update(output={"n_docs": len(docs), "top_score": docs[0].score})

        # Span 2: LLM генерация
        with trace.span(name="generation") as span:
            answer = self.llm.generate(question, context=docs)
            span.update(output={"answer": answer, "tokens": answer.usage})

        trace.update(output={"answer": answer.text})
        return {"answer": answer.text, "trace_id": trace.id}
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **LangFuse + LangGraph (R35)** | Полная трассировка ReAct циклов: видно где агент "зациклился" |
| **LangFuse + Meta-Monitor (R29)** | LangFuse metrics → Meta-Monitor: LLM observability как часть общей AI мониторинга |
| **LangFuse + LLM Judge (R28)** | Автоматическая оценка качества ответов сохраняется в LangFuse trace |
| **LangFuse + MAESTRO (R38)** | CARL DAG трейсы в LangFuse: аудитируемое медицинское рассуждение |
| **LangFuse + Lorenzo Gateway** | /api/ask endpoint: каждый запрос → LangFuse trace с cost attribution |

## Контакт

- Статья Часть 1: https://habr.com/ru/articles/1008300/ (март 2026)
- Статья Часть 2: https://habr.com/ru/articles/1008402/ (март 2026)
- LangFuse GitHub: https://github.com/langfuse/langfuse (MIT)
- Self-hosted docs: langfuse.com/docs/deployment/self-host
- Смежная (YADRO production Langfuse): https://habr.com/ru/companies/yadro/articles/978516/
- Смежная (AI анализирует AI трейсы): https://habr.com/ru/articles/987230/
- Смежная (обзор LLM observability ландшафта): https://habr.com/ru/articles/972480/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
