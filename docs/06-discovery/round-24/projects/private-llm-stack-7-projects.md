---
date: 2026-05-29
tags: [memory, rag, orchestration, security, knowledge]
state: normalized
---

# 7 pet-проектов с LLM: приватность, скорость и безопасность своими руками

<!-- toc-auto -->
<!-- tags: private-llm-stack-7-projects, docs -->


<!-- summary -->
> 7 pet-проектов с LLM: приватность, скорость и безопасность своими руками — раздел документации проекта Lorenzo.
 
 
 
>   — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** независимый разработчик (Хабр, январь 2026)  
**Хабр:** https://habr.com/ru/articles/988774/  
**GitHub:** не опубликован (разбор архитектур + код в статье)  
**Слой:** orchestration / memory / security / ingestion  
**Дата:** январь 2026  
**Уникальность:** Практический разбор 7 pet-проектов, которые можно собрать самому для решения реальных ограничений облачных LLM: приватность, стоимость, latency, нестандартные источники знаний. Ключевая идея: 7 компонентов → единая privacy-first AI система. Чёткая карта «что строить дальше» для тех, у кого уже есть базовый RAG.

## Проблема облачных LLM

```
Почему не всегда можно использовать ChatGPT/Claude напрямую:

  Приватность: чувствительные данные → не выходят в облако
  Стоимость: при >100K токенов/день → дорого (R20 экономика)
  Latency: 2-5 секунд API round-trip = плохой UX
  Нестандартные данные: корпоративные БД, внутренние вики
  Vendor lock-in: зависимость от одного провайдера
  Reproducibility: результат меняется между версиями модели

Решение: собрать стек из открытых компонентов
```

## 7 проектов: от простого к сложному

### Проект 1: Private On-Device RAG
```python
# Полностью локальный RAG: документы никуда не уходят
from llama_cpp import Llama
from chromadb import Client

# Модель: GGUF (Qwen2.5:7b-Q4_K_M) — работает на CPU
llm = Llama(model_path="qwen2.5-7b-q4.gguf", n_ctx=4096)
db = Client()

def private_rag(question: str, docs_folder: str) -> str:
    # Embed документы (локально через nomic-embed или FRIDA)
    collection = index_documents(docs_folder, db)

    # Найти релевантные
    results = collection.query(query_texts=[question], n_results=3)

    # Ответить локально
    return llm(f"Context: {results}\nQuestion: {question}")
    # 100% локально: ни вопрос, ни документы, ни ответ не ушли в облако
```

### Проект 2: Tool Retrieval (динамические инструменты)
```python
# Проблема: при 50+ инструментах контекст переполнен
# Решение: хранить инструменты в векторной БД → выбирать N релевантных

TOOL_DB = VectorDB()  # все 50+ инструментов с описаниями

def smart_tool_selection(user_query: str, k=5) -> list[Tool]:
    """Вместо передачи всех 50 инструментов → только 5 релевантных"""
    relevant_tools = TOOL_DB.search(user_query, k=k)
    return relevant_tools

# Применение: LLM видит только нужные инструменты → точнее, дешевле
# Сэкономлено: (50 - 5) × N_вызовов × стоимость_токена
```

### Проект 3: Agent с Firewall
```python
# Проблема: агент может выполнить опасные действия (delete, send email)
# Решение: firewall слой между агентом и инструментами

class AgentFirewall:
    DANGEROUS_ACTIONS = {"delete", "send_email", "payment", "sudo"}

    def intercept(self, tool_call: ToolCall, context: str) -> ToolCall | None:
        if tool_call.name in self.DANGEROUS_ACTIONS:
            # Проверить через safety LLM (быстрая малая модель)
            is_safe = self.safety_check(tool_call, context)
            if not is_safe:
                return None  # блокировать
        return tool_call

    def safety_check(self, call: ToolCall, context: str) -> bool:
        return safety_llm.classify(
            f"Action: {call}\nContext: {context}\n"
            "Is this action safe and intended by the user? yes/no"
        ) == "yes"
```

### Проект 4: Privacy Gateway для внешних моделей
```python
# Когда нужна мощь Claude/GPT-4o, но данные нельзя передавать напрямую

class PrivacyGateway:
    def __init__(self, ner_model, external_llm):
        self.ner = ner_model      # локальная NER (как Jay Guard, R21)
        self.llm = external_llm  # Claude / GPT-4o

    def safe_query(self, query: str, context: str) -> str:
        # Шаг 1: анонимизировать локально
        anonymized_query, mapping = self.ner.anonymize(query)
        anonymized_context, ctx_mapping = self.ner.anonymize(context)

        # Шаг 2: отправить анонимизированное в облако
        response = self.llm.chat(anonymized_query, anonymized_context)

        # Шаг 3: деанонимизировать ответ
        return self.ner.deanonymize(response, {**mapping, **ctx_mapping})
        # Данные никогда не покидали контур в виде ПД
```

### Проект 5: Inference Optimization (стоимость и latency)
```python
# Три техники сокращения стоимости:

# 1. Кэширование промптов (prompt cache)
from anthropic import Anthropic
client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-6",
    messages=[{"role": "user", "content": query}],
    system=[{
        "type": "text",
        "text": LARGE_SYSTEM_PROMPT,
        "cache_control": {"type": "ephemeral"}  # кэшировать системный промпт
    }]
)
# Первый вызов: полная цена; следующие: -90% по системному промпту

# 2. Батчинг запросов (асинхронный)
async def batch_process(queries: list[str]) -> list[str]:
    return await asyncio.gather(*[llm.aquery(q) for q in queries])
# Параллельно = в N раз быстрее чем последовательно

# 3. Количественная оценка (quantization): Q4 → 4× меньше VRAM, -5% качество
```

### Проект 6: Multimodal Private Pipeline
```python
# Обработка документов с изображениями + текстом без облака

def process_multimodal_doc(pdf_path: str) -> dict:
    # Текст: pdfminer / Docling (R19)
    text_chunks = docling.extract(pdf_path)

    # Изображения: локальная vision модель
    images = extract_images(pdf_path)
    img_descriptions = [
        local_vision_llm.describe(img)  # InternVL2 / Qwen2-VL локально
        for img in images
    ]

    # Таблицы: Docling structured extraction
    tables = docling.extract_tables(pdf_path)

    # Объединить → единый контекст для RAG
    return {
        "text": text_chunks,
        "images": img_descriptions,
        "tables": tables
    }
```

### Проект 7: LLM Monitoring и Cost Tracker
```python
# Без мониторинга невозможно оптимизировать

class LLMMonitor:
    def track(self, call: LLMCall) -> None:
        self.db.insert({
            "model": call.model,
            "prompt_tokens": call.usage.input_tokens,
            "completion_tokens": call.usage.output_tokens,
            "cost": self.calculate_cost(call),
            "latency_ms": call.latency,
            "endpoint": call.endpoint,
            "success": call.success,
            "timestamp": now()
        })

    def daily_report(self) -> CostReport:
        return self.db.aggregate(
            group_by=["model", "endpoint"],
            metrics=["total_cost", "avg_latency", "error_rate"]
        )
        # → "improve_llm_qa.py тратит $2.3/день, 45% — повторяющиеся запросы"
        # → Решение: кэшировать часто запрашиваемые ответы
```

## Единая система: 7 → 1

```
Полный private AI стек:

User → [Agent Firewall (3)] → [Tool Retrieval (2)]
                                     ↓
                          [Privacy Gateway (4)] → External LLM (Claude)
                                     ↓
                          [Private RAG (1)] → Local LLM (Qwen2.5)
                                     ↓
                          [Multimodal Pipeline (6)]
                                     ↓
                          [Inference Optimizer (5)]
                                     ↓
                          [LLM Monitor (7)] → Dashboard

→ 100% контроль данных + внешний LLM только для сложных задач
```

## Применение к Lorenzo

Lorenzo уже использует Claude API + audit.db. Этот стек = следующий уровень:

```python
# Уже есть:
#   improve_llm_qa.py → Claude API (Проект 1 частично)
#   improve_audit_db.py → audit.db (Проект 7 частично)

# Что добавить:
#   Проект 2: Tool Retrieval — индекс 159+ скриптов в VectorDB → выбирать нужные
#   Проект 3: Firewall — проверять перед apply/write операциями
#   Проект 4: Privacy Gateway — анонимизировать если обрабатываем ПД
#   Проект 5: Кэш промптов — CLAUDE.md как ephemeral cache_control
#   Проект 7: Cost Tracker — сколько тратим на Claude API по скриптам
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **7 Projects + Jay Guard (R21)** | Проект 4 (Privacy Gateway) = улучшенный Jay Guard с двусторонней анонимизацией |
| **7 Projects + Self-hosted (R22)** | Проект 1 (Private RAG) + n8n оркестрирует = полностью локальный Lorenzo |
| **7 Projects + Phantom (R23)** | Проект 3 (Firewall) + structural injection check = двойная защита агентов |
| **7 Projects + LLM Router (R20)** | Проект 2 (Tool Retrieval) + роутинг: нужный инструмент + нужная модель |
| **7 Projects + Langfuse (R13)** | Проект 7 (Monitor) + Langfuse = полный observability стек |

## Контакт

- Статья: https://habr.com/ru/articles/988774/ (январь 2026)
- Смежная (как LLM-вендоры обращаются с данными): https://habr.com/ru/companies/pt/articles/973402/
- Смежная (7 кейсов Confer — первый безопасный AI): https://habr.com/ru/articles/988874/
- llama.cpp: github.com/ggerganov/llama.cpp (MIT)
- ChromaDB: github.com/chroma-core/chroma (Apache 2.0)
- nomic-embed-text: nomic.ai/blog/nomic-embed (Apache 2.0)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
