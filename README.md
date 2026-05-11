# Lorenzo — Knowledge OS для Svyazi 2.0
<!-- badges -->
![docs](docs.svg) ![words](words.svg) ![scripts](scripts.svg) ![health](health.svg) ![go/no-go](scoring.svg) ![license](license.svg) ![branch](branch.svg) 


> Локальная community intelligence platform: поиск, хранение и коллаборация знаний.
> Любой AI-агент подключается по OpenAI-протоколу.

## Что это

**Lorenzo** — монорепозиторий исследований и готовый Knowledge OS для проекта **Svyazi 2.0**:
- **2480 документов** в `docs/` (карточки проектов, анализ вакансий, технические синергии)
- **Гибридный поиск** (BM25 + TF-IDF + hnswlib ANN), Hit Rate@10 = 1.00
- **OpenAI-compatible API** — любой агент подключается без настройки
- **MCP-сервер** — интеграция с Claude Desktop и другими MCP-клиентами
- **165 скриптов** для построения и обслуживания базы знаний

## Быстрый старт

```bash
# 1. Установить зависимости
pip install fastapi uvicorn streamlit hnswlib numpy

# 2. Запустить HTTP gateway
python scripts/gateway.py
# → http://localhost:8083/docs (Swagger UI)
# → http://localhost:8083/api/health

# 3. Быстрый поиск (только results, без LLM-синтеза)
curl -X POST http://localhost:8083/api/search \
     -H "Content-Type: application/json" \
     -d '{"query": "агент с памятью консолидация", "top_k": 5}'

# 4. RAG-поиск с контекстом
curl -X POST http://localhost:8083/api/ask \
     -H "Content-Type: application/json" \
     -d '{"query": "агент с памятью консолидация", "top_k": 5}'

# 6. Поиск коллабораций напрямую
curl -X POST http://localhost:8083/api/collabs \
     -H "Content-Type: application/json" \
     -d '{"query": "YAML агент оркестрация", "top_k": 3}'

# 7. Проверить все критерии PROTOTYPE_SPEC §8
curl http://localhost:8083/api/benchmark

# 8. Или через OpenAI Python SDK
python -c "
from openai import OpenAI
client = OpenAI(base_url='http://localhost:8083/v1', api_key='not-needed')
r = client.chat.completions.create(
    model='lorenzo-gateway',
    messages=[{'role': 'user', 'content': 'Что такое Yodoca?'}]
)
print(r.choices[0].message.content)
"
```

## Архитектура

```
Любой AI-клиент (Claude Desktop / Cursor / GPT / агент)
        │  POST /v1/chat/completions  (OpenAI API)
        ▼
Lorenzo Gateway (FastAPI, порт 8083)
  ├── Intent router + 5 инструментов (function calling)
  ├── hybrid_search() = 0.6×TF-IDF + 0.4×BM25
  ├── ANN-поиск (hnswlib HNSW, 37× speedup, опционально)
  ├── POST /api/search   → лёгкий поиск (results only, без LLM)
  ├── POST /api/collabs  → find_collabs() (Jaccard + BM25)
  ├── GET  /api/benchmark → критерии PROTOTYPE_SPEC §8
  └── write-back: POST /api/cards → .md файл в docs/
        │
   search_index.json (2482 документа)
   passages.json (13 291 абзацев)
        │
   docs/ (markdown карточки)
```

## Структура docs/

| Раздел | Описание | Файлов |
|--------|----------|--------|
| [01-svyazi](docs/01-svyazi/) | Архитектура Svyazi 2.0: компоненты, ансамбли, MVP | 16 |
| [02-anthropic-vacancies](docs/02-anthropic-vacancies/) | Анализ 436 вакансий Anthropic по 12 кластерам | 356 |
| [03-technology-combinations](docs/03-technology-combinations/) | 40+ синергий технологий (hardware, agents, local-first) | 50 |
| [04-ai-collaborations](docs/04-ai-collaborations/) | 5 ансамблей OSS-проектов для Svyazi | 12 |
| [05-habr-projects](docs/05-habr-projects/) | 9 богатых карточек: Yodoca, AgentFS, MemNet, Rufler и др. | 20 |
| [PROTOTYPE_SPEC.md](docs/PROTOTYPE_SPEC.md) | Спецификация прототипа: 4 контракта + 4 итерации | — |
| [GATEWAY.md](docs/GATEWAY.md) | Документация Lorenzo Gateway | — |
| [CONTACTS.md](docs/CONTACTS.md) | 8 авторов проектов, письма готовы | — |

## Ключевые скрипты

| Скрипт | Назначение |
|--------|-----------|
| `scripts/gateway.py` | OpenAI-compatible HTTP API (FastAPI, порт 8083) |
| `scripts/mcp_server.py` | MCP-сервер с 11 инструментами (для Claude Desktop) |
| `scripts/review_queue.py` | Streamlit UI: одобрение/отклонение карточек |
| `scripts/improve_ann_index.py` | hnswlib HNSW ANN-индекс (37× speedup vs линейный TF-IDF) |
| `scripts/improve_collab_finder.py` | Поиск кандидатов на коллаборацию |
| `scripts/improve_semantic_search.py` | Unified CLI поиск (BM25 / TF-IDF / hybrid) |
| `scripts/improve_precision_eval.py` | Авто-оценка Hit Rate@10 (1.00 ≥ 0.70 ✅) |
| `scripts/improve_run_all.py` | Оркестратор: --smart / --group / --parallel |

## Запуск компонентов

```bash
# HTTP Gateway
python scripts/gateway.py [--port 9000] [--reload]

# MCP-сервер (stdio, для Claude Desktop)
python scripts/mcp_server.py

# Review Queue UI
streamlit run scripts/review_queue.py   # → http://localhost:8501

# ANN-индекс (нужен один раз)
python scripts/improve_ann_index.py --build

# Поиск из CLI
python scripts/improve_semantic_search.py --query "агент память консолидация"
python scripts/improve_collab_finder.py --query "typed memory sqlite mcp"

# Тесты
pip install -r requirements-test.txt
pytest tests/ --ignore=tests/test_ann_index.py
```

## Проекты в базе знаний

| Проект | Слой | Автор (Хабр) |
|--------|------|-------------|
| [Yodoca](docs/05-habr-projects/memory/yodoca.md) | memory/consolidation | VitalyOborin |
| [NGT Memory](docs/05-habr-projects/memory/ngt-memory.md) | memory/graph | spbmolot |
| [MemNet](docs/05-habr-projects/memory/memnet.md) | memory/research | Antipozitive |
| [agent-memory-mcp](docs/05-habr-projects/memory/agent-memory-mcp.md) | memory/MCP | VitaliySemenov |
| [AgentFS](docs/05-habr-projects/knowledge/agentfs.md) | knowledge/filesystem | kksudo |
| [knowledge-space](docs/05-habr-projects/knowledge/knowledge-space.md) | knowledge/cards | AnastasiyaW |
| [Rufler](docs/05-habr-projects/knowledge/rufler.md) | orchestration/YAML | zodigancode |
| [LiteParse](docs/05-habr-projects/knowledge/research-docs-liteparse.md) | ingestion/evidence | nlaik |
| [Wikontic](docs/05-habr-projects/knowledge/wikontic.md) | knowledge/graph | VitalyOborin |

## Статус итераций (PROTOTYPE_SPEC)

| Итерация | Статус | Артефакты |
|----------|--------|-----------|
| 0 — Вертикальный срез | ✅ | 1632 карточки, MCP 11 инструментов |
| 1 — Retrieval Loop | ✅ | BM25+TF-IDF+ANN, Review Queue UI |
| 2 — Consolidation | ✅ | CI daily, SENTINEL, orphan rate 0% |
| 3 — Collaboration Finder | ✅ | 9 проектных файлов, письма авторам |
| 4 — Gateway & Enrichment | ✅ | OpenAI API, 286 тестов, Hit Rate@10=1.00 |

## Требования

```bash
# Минимум (поиск из CLI — только стандартная библиотека Python 3.11+)
python scripts/improve_semantic_search.py --query "..."

# HTTP Gateway
pip install fastapi uvicorn pydantic

# ANN-поиск
pip install hnswlib numpy

# Review Queue UI
pip install streamlit

# Тесты
pip install -r requirements-test.txt
```

---

_Документация: [docs/GATEWAY.md](docs/GATEWAY.md) · [docs/PROTOTYPE_SPEC.md](docs/PROTOTYPE_SPEC.md) · [docs/PROGRESS.md](docs/PROGRESS.md)_
