# Lorenzo Gateway

<!-- toc -->
## Содержание

- [Содержание](#содержание)
- [Что это](#что-это)
- [Сравнение с DAF-gateway](#сравнение-с-daf-gateway)
- [Архитектура](#архитектура)
- [Запуск](#запуск)
- [Эндпоинты](#эндпоинты)
  - [`GET /api/health`](#get-apihealth)
  - [`GET /api/status`](#get-apistatus)
  - [`GET /api/benchmark`](#get-apibenchmark)
  - [`POST /api/ask`](#post-apiask)
  - [`POST /api/search`](#post-apisearch)
  - [`POST /api/collabs`](#post-apicollabs)
  - [`POST /api/cards`](#post-apicards)
  - [`POST /v1/chat/completions`](#post-v1chatcompletions)
  - [`GET /v1/models`](#get-v1models)
- [Инструменты (function calling)](#инструменты-function-calling)
- [Примеры использования](#примеры-использования)
  - [Простой поиск](#простой-поиск)
  - [Поиск коллаборации](#поиск-коллаборации)
  - [Обогащение корпуса через chat](#обогащение-корпуса-через-chat)
  - [Python-клиент (openai SDK)](#python-клиент-openai-sdk)
  - [С function calling](#с-function-calling)
- [Подключение AI-клиентов](#подключение-ai-клиентов)
  - [Claude Desktop](#claude-desktop)
  - [Cursor / Continue / Cody](#cursor-continue-cody)
  - [Другой агент (Python)](#другой-агент-python)
- [Режим обогащения](#режим-обогащения)

---


> [!NOTE]
> Раздел `GATEWAY` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- toc-auto -->
## Содержание

- [Что это](#что-это)
- [Сравнение с DAF-gateway](#сравнение-с-daf-gateway)
- [Архитектура](#архитектура)
- [Запуск](#запуск)
- [Эндпоинты](#эндпоинты) (`/api/health`, `/api/status`, `/api/benchmark`, `/api/ask`, `/api/search`, `/api/collabs`, `/api/cards`, `/v1/chat/completions`)
- [Инструменты (function calling)](#инструменты-function-calling)
- [Примеры использования](#примеры-использования)
- [Подключение AI-клиентов](#подключение-ai-клиентов)
- [Режим обогащения](#режим-обогащения)

<!-- summary -->
> OpenAI-совместимый HTTP-шлюз к базе знаний Lorenzo. Любой AI-агент подключается по стандартному протоколу и может читать корпус (2482 карточки) или обогащать его новыми карточками.

<!-- tags: gateway, openai-compatible, api, rag, function-calling, enrichment -->

---

## Что это

**Lorenzo Gateway** — HTTP-сервер, который превращает базу знаний Svyazi 2.0 в стандартный AI-сервис.

**Зачем:** любой AI-агент (Claude Desktop, Cursor, GPT-клиент, другой агент) может подключиться по OpenAI-протоколу и:
- **читать** корпус через гибридный поиск (BM25 + TF-IDF)
- **обогащать** его — добавлять новые карточки через API
- **вызывать инструменты** через стандартный function calling

**Ключевое отличие от DAF-gateway:** вся логика поиска — наша, pure Python, без чёрных ящиков. Поиск работает офлайн, без Redis и Docker.

---

## Сравнение с DAF-gateway

| Аспект | Lorenzo Gateway | DAF-gateway |
|--------|----------------|-------------|
| Поиск | `hybrid_search()` — наш BM25+TF-IDF | `docstoolkit.rag` — внешняя библиотека |
| Данные | `search_index.json` (2482 карточек) | собственный корпус DAF |
| Офлайн | ✅ полностью | ❌ требует Redis |
| Docker | ❌ не нужен | ✅ docker-compose |
| Зависимости | `fastapi`, `uvicorn` | FastAPI + Redis + Docker |
| Function calling | ✅ 5 инструментов | ❌ нет |
| Write-back | ✅ `POST /api/cards` → .md файл | ❌ нет |
| LLM синтез | ✅ опционально (ANTHROPIC_API_KEY) | ✅ внутри docstoolkit |
| Запуск | `python scripts/gateway.py` | `docker compose up` |

---

## Архитектура

```
┌─────────────────────────────────────────────┐
│   Любой AI-клиент                           │
│   (Claude Desktop / Cursor / GPT / агент)   │
└─────────────────┬───────────────────────────┘
                  │  POST /v1/chat/completions
                  │  (OpenAI API protocol)
                  ▼
┌─────────────────────────────────────────────┐
│           Lorenzo Gateway (FastAPI)          │
│                                             │
│  ┌─────────┐  ┌──────────┐  ┌───────────┐  │
│  │ Intent  │  │  Tools   │  │ LLM synth │  │
│  │ router  │  │ dispatch │  │ (optional)│  │
│  └────┬────┘  └────┬─────┘  └─────┬─────┘  │
│       └────────────┴───────────────┘        │
│                    │                        │
│         hybrid_search() — pure Python       │
└────────────────────┬────────────────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
   search_index.json       passages.json
   (2482 карточек)         (13291 абзацев)
          │
     docs/ (markdown)
```

**Два режима работы:**

1. **Без инструментов от клиента** — Gateway сам решает, что искать, выполняет поиск и возвращает готовый ответ. Если задан `ANTHROPIC_API_KEY` — синтезирует ответ через Claude.

2. **С инструментами (function calling)** — Gateway возвращает `tool_calls` в формате OpenAI. Клиент сам выполняет инструмент, возвращает результат, Gateway синтезирует финальный ответ.

---

## Запуск

```bash
# Установить зависимости
pip install fastapi uvicorn

# Запустить (базовый режим, без LLM)
python scripts/gateway.py

# С LLM-синтезом через Claude
export ANTHROPIC_API_KEY=sk-ant-...
python scripts/gateway.py

# Нестандартный порт
python scripts/gateway.py --port 9000

# Авто-перезагрузка при разработке
python scripts/gateway.py --reload
```

После запуска:
- Swagger UI: http://localhost:8083/docs
- Health check: http://localhost:8083/api/health

---

## Эндпоинты

### `GET /api/health`
Статус сервера.
```json
{
  "status": "ok",
  "cards": 2461,
  "passages": 13291,
  "version": "1.0.0",
  "llm": false
}
```

### `GET /api/status`
Детальная статистика корпуса.

### `GET /api/benchmark`
Все 5 критериев успеха PROTOTYPE_SPEC §8 одним запросом.
```bash
curl http://localhost:8083/api/benchmark
```
```json
{
  "criteria": {
    "latency_s":   {"value": 0.21, "threshold": "≤5.0s", "pass": true},
    "cards":       {"value": 2482, "threshold": "≥500",  "pass": true},
    "orphan_rate": {"value": 0.0,  "threshold": "≤0.15", "pass": true},
    "hit_rate_10": {"value": 1.0,  "threshold": "≥0.70", "pass": true}
  },
  "all_pass": true,
  "spec": "PROTOTYPE_SPEC §8"
}
```

### `POST /api/ask`
Прямой RAG-запрос без OpenAI-совместимости.
```bash
curl -X POST http://localhost:8083/api/ask \
     -H "Content-Type: application/json" \
     -d '{"query": "агент с памятью консолидация", "top_k": 5}'
```
```json
{
  "query": "агент с памятью консолидация",
  "answer": "...",
  "results": [...],
  "latency_s": 0.8
}
```

### `POST /api/search`
Лёгкий поиск — только список результатов, без LLM-синтеза и контекста.
Подходит для автодополнения и быстрого UI.
```bash
curl -X POST http://localhost:8083/api/search \
     -H "Content-Type: application/json" \
     -d '{"query": "агент память консолидация", "top_k": 5}'
```
```json
{
  "query": "агент память консолидация",
  "results": [...],
  "count": 5,
  "latency_s": 0.12
}
```

### `POST /api/collabs`
Прямой поиск кандидатов на коллаборацию без chat-слоя.
```bash
curl -X POST http://localhost:8083/api/collabs \
     -H "Content-Type: application/json" \
     -d '{"query": "YAML декларативный оркестратор агентов", "top_k": 3}'
```
```json
{
  "query": "YAML декларативный оркестратор агентов",
  "results": [
    {"title": "Rufler", "file": "docs/05-habr-projects/knowledge/rufler.md",
     "score": 0.042, "author": "zodigancode", "has_letter": false}
  ],
  "count": 3,
  "latency_s": 0.003
}
```

### `POST /api/cards`
Добавить карточку в корпус (обогащение базы знаний).
```bash
curl -X POST http://localhost:8083/api/cards \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Новый проект: GraphSync",
       "content": "GraphSync — инкрементальная синхронизация графов знаний...",
       "section": "04-ai-collaborations",
       "tags": ["graph", "sync", "oss"]
     }'
```

### `POST /v1/chat/completions`
OpenAI-совместимый эндпоинт.

### `GET /v1/models`
Список доступных моделей (возвращает `lorenzo-gateway`).

---

## Инструменты (function calling)

Gateway предоставляет 5 инструментов:

| Инструмент | Описание | Параметры |
|-----------|---------|----------|
| `search` | Гибридный поиск по корпусу | `query`, `top_k` |
| `get_card` | Прочитать документ по пути | `path` |
| `add_card` | Добавить карточку (обогащение) | `title`, `content`, `section`, `tags` |
| `find_collabs` | Найти кандидатов на коллаборацию | `query`, `top_k` |
| `get_contacts` | Получить контакт и письмо автора | `project` |

---

## Примеры использования

### Простой поиск
```bash
curl -X POST http://localhost:8083/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
       "model": "lorenzo-gateway",
       "messages": [{"role": "user", "content": "Что такое Yodoca и как там устроен decay?"}]
     }'
```

### Поиск коллаборации
```bash
curl -X POST http://localhost:8083/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
       "model": "lorenzo-gateway",
       "messages": [{"role": "user", "content": "найди коллабораций для проекта с типизированной памятью"}]
     }'
```

### Обогащение корпуса через chat
```bash
# Инструмент add_card создаёт .md файл в docs/ и сбрасывает кэш индекса
curl -X POST http://localhost:8083/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
       "model": "lorenzo-gateway",
       "messages": [{"role": "user", "content": "добавь карточку: GraphSync — синхронизация графов знаний через CRDT"}]
     }'
```

### Python-клиент (openai SDK)
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8083/v1",
    api_key="not-needed",   # gateway не требует ключа
)

response = client.chat.completions.create(
    model="lorenzo-gateway",
    messages=[{"role": "user", "content": "Как устроен CardEnvelope в Svyazi 2.0?"}],
)
print(response.choices[0].message.content)
```

### С function calling
```python
response = client.chat.completions.create(
    model="lorenzo-gateway",
    messages=[{"role": "user", "content": "найди проекты для памяти агента"}],
    tools=[{
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search knowledge base",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        }
    }],
)
# Gateway вернёт tool_calls → клиент выполняет → возвращает результат
```

---

## Подключение AI-клиентов

### Claude Desktop
Добавить в `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "lorenzo": {
      "command": "python",
      "args": ["/path/to/scripts/mcp_server.py"]
    }
  }
}
```
> Для Claude Desktop предпочтительнее MCP (`mcp_server.py`). Gateway полезен для других клиентов.

### Cursor / Continue / Cody
Добавить custom OpenAI endpoint:
```
Base URL: http://localhost:8083/v1
API Key:  not-needed
Model:    lorenzo-gateway
```

### Другой агент (Python)
```python
import httpx

resp = httpx.post(
    "http://localhost:8083/api/ask",
    json={"query": "NGT Memory ассоциативный граф"},
)
results = resp.json()["results"]
```

---

## Режим обогащения

Главное отличие от DAF: Gateway поддерживает **запись обратно в корпус**.

**Как работает `add_card`:**
1. AI-агент (или пользователь) вызывает `POST /api/cards` или инструмент `add_card`
2. Gateway создаёт `.md` файл в `docs/<section>/` с правильным frontmatter
3. Сбрасывает in-memory кэш индекса
4. Следующий поиск автоматически подхватывает новую карточку

**Полный цикл обогащения:**
```
Внешний источник (статья, разговор, результат анализа)
    ↓
AI-агент анализирует и структурирует
    ↓
POST /api/cards  →  docs/04-ai-collaborations/<slug>.md
    ↓
python scripts/improve_index_update.py --incremental  # обновить индекс
    ↓
Карточка доступна через поиск для всех агентов
```

---

_Файл: `scripts/gateway.py` · Версия: 1.0.0 · Дата: 2026-05-11_

<!-- similar-docs -->

---

**Похожие документы:**
- [GATEWAY](obsidian/GATEWAY.md) (сходство 0.99)
- [PROTOTYPE_SPEC](obsidian/PROTOTYPE_SPEC.md) (сходство 0.16)
- [PROTOTYPE_SPEC](PROTOTYPE_SPEC.md) (сходство 0.15)

