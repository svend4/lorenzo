---
date: 2026-05-28
tags: [memory, rag, orchestration, architecture, self-improve]
state: normalized
---

# Правильная агентская архитектура 2026 — Durable State, Approvals, Session Context

<!-- toc-auto -->
<!-- tags: production-agent-durable-state, docs -->


<!-- summary -->
> Проблема: Stateless агент в production Durable State: ключевая концепция SessionContext — не полный транскрипт
 
Durable State: ключевая концепция
 
SessionContext — не полный транскрипт
 
Human-in-the-Loop Approvals
 
Background Jobs: агент не блокирует пользователя
 
Полная схема production-ready агента
 
Часть 1: ReAc


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** независимый разработчик (Хабр, май 2026)  
**Хабр:** https://habr.com/ru/articles/1031440/ (Часть 2)  
**Смежная:** https://habr.com/ru/articles/981100/ (Часть 1: ReAct, Advanced RAG, Tools)  
**GitHub:** не опубликован (архитектурный паттерн + код в статье)  
**Слой:** orchestration / memory  
**Дата:** май 2026  
**Уникальность:** Первый публичный русскоязычный deep-dive по production-ready durable state для AI-агентов: SessionContext (не полный транскрипт, а компактная техкарта), Human-in-the-loop Approvals, Background Jobs. Прямой ответ на вопрос "почему агент ломается при перезагрузке страницы".

## Проблема: Stateless агент в production

```
Типичный production баг:
  Пользователь → начал длинный диалог с агентом
  → обновил страницу / переключил вкладку / сеть упала
  → агент потерял всё: контекст, текущую задачу, согласования

Почему это происходит:
  Большинство агентских фреймворков = stateless LLM + chat history в памяти
  → перезапуск процесса = потеря state
  → горизонтальное масштабирование невозможно (session привязана к instance)
  → reconnect = новый диалог "с нуля"
```

## Durable State: ключевая концепция

```
Ключевой принцип: State хранится вне агента, персистентно

Три слоя state:
  1. SessionContext   — текущая сессия (цель, шаги, статус)
  2. ApprovalQueue   — ожидающие подтверждения человека
  3. BackgroundJobs  — долгие задачи (асинхронно, без блокировки)
```

## SessionContext — не полный транскрипт

```python
# НЕПРАВИЛЬНО: хранить весь chat history
session_state = {
    "messages": [{"role": "user", "content": "..."}, ...]  # 50K токенов → дорого
}

# ПРАВИЛЬНО: компактная техкарта (паттерн из статьи)
class SessionContext(BaseModel):
    session_id: str
    goal: str                      # "Заказать командировку в Питер 15-17 мая"
    current_step: str              # "awaiting_hotel_approval"
    completed_steps: list[str]     # ["flight_booked", "taxi_ordered"]
    pending_approvals: list[str]   # ["hotel_booking_id_42"]
    extracted_facts: dict          # {"city": "SPB", "dates": ["2026-05-15",...]}
    last_active: datetime
    user_id: str

# Хранится в Redis/PostgreSQL, не в памяти агента
# Восстанавливается при reconnect: агент продолжает с current_step
```

## Human-in-the-Loop Approvals

```python
# Паттерн: агент не делает необратимые действия без подтверждения

class ApprovalRequest(BaseModel):
    approval_id: str
    session_id: str
    action_type: str          # "book_hotel" | "send_email" | "delete_record"
    action_description: str   # "Забронировать Radisson SPB 2 ночи за 12,000₽"
    action_params: dict
    expires_at: datetime      # автоотмена если нет ответа
    status: str               # "pending" | "approved" | "rejected"

# Агент останавливается → пишет в очередь → ждёт
async def book_hotel(params: HotelParams) -> str:
    approval = await approval_queue.create(
        action_type="book_hotel",
        description=f"Забронировать {params.hotel} {params.nights} ночи за {params.price}₽",
        params=params.dict()
    )
    # Пользователь получает уведомление (Telegram/email)
    await notify_user(approval.approval_id)

    # Ждём решения (webhook от UI)
    result = await approval_queue.wait(approval.approval_id, timeout=3600)

    if result.status == "approved":
        return await hotel_api.book(params)
    else:
        return "Бронирование отменено пользователем"
```

## Background Jobs: агент не блокирует пользователя

```python
# Проблема: агент выполняет задачу 30 минут → UI зависает
# Решение: агент стартует job → возвращает job_id → пользователь отсоединяется

class BackgroundJob(BaseModel):
    job_id: str
    session_id: str
    status: str         # "running" | "done" | "failed"
    progress: float     # 0.0 → 1.0
    result: Any | None
    created_at: datetime

# Паттерн запуска:
async def run_long_analysis(query: str, user_id: str) -> str:
    job = await job_store.create(session_id=session_id)

    # Запускаем async, не ждём
    asyncio.create_task(
        _do_analysis(job.job_id, query)
    )

    return f"Задача запущена (ID: {job.job_id}). Уведомлю когда закончу."
    # Уведомление через Telegram/webhook когда job.status == "done"
```

## Полная схема production-ready агента

```
User (UI) → HTTP / WebSocket
      ↓
API Gateway
      ↓
Agent Orchestrator
  ├── SessionContext Store (Redis/Postgres) ← персистентный state
  ├── Approval Queue (Postgres + notifications)
  ├── Background Job Scheduler (Celery/Dramatiq)
  └── LLM Client (Claude/OpenAI)
        ↓ tools
  ├── Domain Tools (бронирование, email, CRM...)
  ├── RAG Retriever (векторная БД)
  └── MCP Servers (внешние интеграции)
```

## Часть 1: ReAct + Advanced RAG (981100)

```python
# ReAct loop (Reason + Act) — основа агента:
while not task_complete:
    thought = llm.think(context, tools_available)      # Reason
    if thought.needs_tool:
        observation = execute_tool(thought.tool_call)  # Act
        context.add_observation(observation)
    else:
        final_answer = thought.answer
        break

# Advanced RAG в агенте:
#   Не "найти похожее" → "найти нужное для текущего шага"
#   HyDE: сначала сгенерировать гипотетический ответ → embedding → поиск
#   Multi-query: разложить вопрос → несколько поисков → RRF слияние
```

## Применение к Lorenzo

Lorenzo агенты (`improve_watcher.py`, `improve_workflow_v2.py`) stateless.  
Durable State паттерн = SessionContext для долгих операций:

```python
# improve_session_state.py (паттерн):
class LorenzoSessionContext(BaseModel):
    session_id: str
    task: str                    # "enrichment" | "discovery" | "qa"
    processed_files: list[str]   # уже обработаны
    pending_files: list[str]     # ещё нужно обработать
    approvals_needed: list[str]  # файлы требующие ревью
    last_checkpoint: datetime

# Преимущество: improve_run_all.py можно останавливать и продолжать
# Текущая проблема: если прервать → начинает заново
# С SessionContext: перезапуск → продолжить с last_checkpoint
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Durable State + A2A (R21)** | SessionContext синхронизируется между агентами через A2A protocol |
| **Durable State + Langfuse (R13)** | Трейсинг каждого шага SessionContext → наблюдаемость производства |
| **Durable State + 3-Agent Case (R21)** | Discovery/Enricher/Monitor получают персистентный state |
| **Durable State + LLM Router (R20)** | Background jobs роутятся на дешёвые модели (Haiku) |
| **Durable State + improve_workflow_v2** | Workflow engine получает checkpoint/resume вместо restart |

## Контакт

- Часть 2 (Durable State): https://habr.com/ru/articles/1031440/ (май 2026)
- Часть 1 (ReAct + RAG): https://habr.com/ru/articles/981100/ (декабрь 2025)
- Смежная (готовим агента к production): https://habr.com/ru/companies/llmstart/articles/1015508/
- Смежная (субъектный подход, инверсия управления LLM): https://habr.com/ru/articles/987518/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
