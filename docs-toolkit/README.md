# docs-toolkit

Универсальный Python-фреймворк для обработки markdown-монорепозиториев: **RAG, agent, workflow, eval, federation, observability**, всё в одном пакете. Извлечён из Lorenzo, но работает на любом markdown-корпусе.

**Статус (2026-04-29):** 53 спринта, 30+ модулей, 546 тестов passed, 30/30 MCP-инструментов, 23/23 шаблонов чисты.

**Принципы:**
- **stdlib-first** — большинство модулей работают без внешних зависимостей
- **local-first** — всё работает offline, cloud — fallback / option
- **SQLite as backbone** — jobs, audit, vectors, feedback, sessions, webhooks, budget, conversations
- **PEP 621 plugins** — discovery через entry_points
- **Test-on-merge** — 546 тестов покрывают все основные модули

---

## Что умеет (10 ключевых возможностей)

1. **Локальный RAG** — 5+ retrievers (`keyword`, `bm25`, `semantic`, `hybrid` через RRF, `adaptive`) × 4 answerers (`echo`, `anthropic`, `openai`, `ollama`)
2. **Adaptive multi-hop retrieval** — confidence-driven reformulation
3. **Streaming** — token-by-token через SSE (`/api/stream/rag`)
4. **Agent loop с tools** — ReAct pattern + plan-and-execute
5. **Workflow DAG** — sync + parallel async, dependency-aware
6. **A/B experiments** — multi-variant comparison с markdown reports
7. **Eval / golden datasets** — P/R/F1 для citations + keyword scores для answers
8. **Conversation memory** — sessions с squash-summarize
9. **Federation (NPP)** — мульти-нодовые distributed queries
10. **Observability** — OTel traces + Prometheus metrics

Полный список + sprint roadmap: [`../docs/ROADMAP/00-CURRENT-STATE.md`](../docs/ROADMAP/00-CURRENT-STATE.md).

---

## Карта модулей

```
docstoolkit/
├── agent/           # ReAct agent loop + planner (plan-and-execute)
├── auth/            # RBAC scopes с wildcards
├── budget/          # Per-scope LLM budget guards (day/week/month/total)
├── cache/           # TTL memoization
├── cluster/         # k-means++ embedding clustering
├── conversation/    # Multi-turn sessions, squash-summarize
├── embeddings/      # Pluggable embedding providers
├── eval/            # Golden datasets, P/R/F1 scoring
├── events/          # Pub-sub event bus
├── experiments/     # A/B testing framework
├── federation/      # NPP — Nautilus Portal Protocol
├── feedback/        # SQLite store + Wilson confidence quality score
├── graph/           # Concept graph builder
├── ingest/          # Document loaders (md / pdf / multi-modal)
├── jobs/            # Background queue
├── lang/            # RU/EN language detection + split
├── prompts/         # Versioned prompts с A/B variants
├── rag/             # RAG pipeline + adaptive multi-hop + streaming
├── router/          # Model chain failover (cheap/fast/balanced/high-quality)
├── skills/          # Skill registry + testing framework
├── telemetry/       # OTel + Prometheus
├── timetravel/      # Git-based historical queries
├── web/             # URL fetch + extract
├── webhooks/        # HTTP delivery с HMAC + DLQ
├── workflow/        # DAG runner (sync + parallel async)
│
├── frontmatter.py   # YAML frontmatter parser
├── plugins.py       # PEP 621 entry_points discovery
├── config.py        # docstoolkit.toml loader
├── core.py          # ROOT/DOCS, write_doc, clean
├── doctor.py        # health check
├── serve.py         # HTTP/REST + SSE + Prometheus endpoints
└── cli.py           # docstoolkit CLI
```

---

## Установка

### Vendored (из этого репо)
```bash
cd docs-toolkit
pip install -e .
```

### Опциональные зависимости
```bash
pip install -e ".[anthropic]"      # для AnthropicAnswerer
pip install -e ".[openai]"         # для OpenAIAnswerer
pip install -e ".[semantic]"       # sentence-transformers (semantic retrieval)
pip install -e ".[telemetry]"      # opentelemetry SDK
pip install -e ".[all]"            # всё разом
```

### Из PyPI (планируется)
```bash
pip install docs-toolkit
```

---

## Quick start

### CLI
```bash
# Создать docstoolkit.toml в текущем репо
docstoolkit init

# Создать документ из шаблона
docstoolkit doc new --type rfc --slug docs/rfcs/RFC-0001.md \
  --vars rfc_id=RFC-0001 title="My RFC"

# Валидация по JSON Schema
docstoolkit doc validate --section docs/contacts

# Список шаблонов
docstoolkit doc list-templates

# Health check
docstoolkit doctor
```

### Python API

#### RAG (offline echo)
```python
from docstoolkit.rag import ask

result = ask("что такое RAG?", method="hybrid", top_k=5)
print(result.answer)
print(result.citations)
```

#### Adaptive multi-hop retrieval
```python
from docstoolkit.rag.adaptive import adaptive_search

result = adaptive_search("сложный вопрос", max_hops=3,
                          confidence_threshold=0.65)
print(result.to_markdown())
```

#### A/B experiment
```python
from docstoolkit.experiments import Experiment, run_experiment

exp = Experiment(
    name="hybrid-vs-keyword",
    variants=[
        {"name": "control", "method": "keyword"},
        {"name": "treatment", "method": "hybrid"},
    ],
    questions=["вопрос 1", "вопрос 2", "вопрос 3"],
)
result = run_experiment(exp)
print(result.compare())  # markdown отчёт
```

#### Eval против golden dataset
```python
from docstoolkit.eval import GoldenItem, GoldenSet, run_eval

gset = GoldenSet(name="rag-baseline", items=[
    GoldenItem(question="что такое Yodoca?",
               expected_answer_contains=["memory", "hot path"],
               expected_doc_ids=["yodoca.md"]),
])
result = run_eval(gset, retriever_config={"method": "hybrid"})
print(result.report())
```

#### Workflow DAG
```python
from docstoolkit.workflow import Workflow, Step, run

wf = Workflow(name="rag-pipeline", steps=[
    Step("retrieve", fn=search, inputs={"q": "$.question"}),
    Step("rerank",   fn=rerank,  inputs={"passages": "$.retrieve.output"}),
    Step("answer",   fn=answer,  inputs={"q": "$.question",
                                          "ps": "$.rerank.output"}),
])
result = run(wf, {"question": "?"})
```

#### Plan-and-execute agent
```python
from docstoolkit.agent import plan_and_execute

result = plan_and_execute("1) найди про Yodoca 2) сделай резюме 3) контакт автора")
print(result.to_markdown())
```

#### Streaming RAG (для UI)
```python
from docstoolkit.rag.streaming import stream_rag

for chunk in stream_rag("вопрос?", answerer="echo"):
    if chunk.type == "token":
        print(chunk.data["text"], end="", flush=True)
    elif chunk.type == "done":
        print(f"\nDuration: {chunk.data['duration_ms']}ms")
```

---

## Конфиг (docstoolkit.toml)

```toml
[paths]
docs = "docs"
templates = "docs/templates"
schemas = "docs/templates/_schemas"

[validation]
strict = false
skip_dirs = ["templates", "_schemas", "node_modules"]

[language]
primary = "ru"
fallback = "en"

[sections]
"01-svyazi" = "Svyazi 2.0"
"05-habr-projects" = "Хабр-проекты"
```

---

## HTTP server

```bash
docstoolkit serve --port 8080
```

Эндпоинты:
- `GET /api/ask?q=...` — синхронный RAG
- `POST /api/stream/rag` — SSE streaming
- `GET /metrics` — Prometheus exposition format
- `POST /api/feedback` — record feedback (thumbs / rating / comment)

---

## Тесты

```bash
pytest tests/                       # 546 тестов
pytest tests/test_rag.py -v         # один модуль
pytest tests/ --cov=docstoolkit     # с coverage
```

Также:
```bash
python ../scripts/improve_mcp_test.py             # MCP integrity (30/30)
python ../scripts/improve_template_integrity.py   # шаблоны (23/23)
```

---

## Roadmap

Полный план развития на 35 идей × 4 уровня сложности — в [`../docs/ROADMAP/`](../docs/ROADMAP/):

- [00-CURRENT-STATE](../docs/ROADMAP/00-CURRENT-STATE.md) — что есть сейчас, что не умеет
- [01-SIMPLE](../docs/ROADMAP/01-SIMPLE.md) — 7 простых улучшений (1-3 спринта)
- [02-MEDIUM](../docs/ROADMAP/02-MEDIUM.md) — 8 mainstream RAG улучшений
- [03-INNOVATIVE](../docs/ROADMAP/03-INNOVATIVE.md) — 10 frontier research направлений (Self-RAG, multi-agent, provenance, MemGPT)
- [04-NOVEL](../docs/ROADMAP/04-NOVEL.md) — 10 никем не сделанных концепций (document metabolism, negotiating retrieval, graph-of-thoughts на корпусе)
- [05-PRIORITIES](../docs/ROADMAP/05-PRIORITIES.md) — 3 пути с конкретными первыми спринтами

### Текущие приоритеты (по [05-PRIORITIES.md](../docs/ROADMAP/05-PRIORITIES.md))

**Путь A — Quick value (12 спринтов, 3 месяца):**
- S6 per-user preferences → S2 faceted UI → S4 PageRank → M2 cross-encoder rerank → M5 online eval

**Путь B — Differentiation (15-18 спринтов, 4-5 месяцев):**
- M5 → I3 provenance + CI → M1 knowledge graph → I1 self-RAG

**Путь C — Long-game (8-12 месяцев на одну novel идею):**
- N3 graph-of-thoughts на корпусе (рекомендуется) или N1 document metabolism

---

## Связь с Lorenzo

В Lorenzo `docs-toolkit/` сейчас vendored через `pip install -e .`. После публикации в PyPI Lorenzo сможет:

```bash
pip install docs-toolkit
# и убрать собственные scripts/improve_validate_templates.py и т.п.
```

Связанные манифесты, шаблоны и скилы остаются специфичными для Lorenzo (в `docs/templates/`, `.claude/skills/`).

---

## Связанные документы

- [`CHANGELOG.md`](CHANGELOG.md) — изменения по версиям
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — как контрибьютить
- [`SECURITY.md`](SECURITY.md) — security policy
- [`RELEASE.md`](RELEASE.md) — процесс релиза
- [`../docs/ROADMAP/`](../docs/ROADMAP/) — план развития
- [`../CLAUDE.md`](../CLAUDE.md) — контекст для Claude Code
