# docs-toolkit Architecture

Архитектурный обзор: слои, контракты, точки расширения. Документ
предназначен для контрибьюторов и для интеграторов, которые встраивают
`docs-toolkit` в собственный продукт.

---

## 1. Принципы

| Принцип | Что означает на практике |
|---|---|
| **stdlib-first** | Большинство модулей не требуют внешних зависимостей. Опциональные ML/cloud ингредиенты — fallback, не основа. |
| **local-first** | Всё работает offline. Cloud (Anthropic API, OpenAI API, Ollama) — пристёгиваемые answerer'ы, не обязательны. |
| **SQLite as backbone** | Persistent state — jobs, audit, vectors, feedback, sessions, webhooks, budget — все в SQLite. Один процесс — один WAL. |
| **PEP 621 plugins** | Сторонние ингредиенты подключаются через `entry_points` в `pyproject.toml` — нет ad-hoc регистрации. |
| **Composition over inheritance** | Один `ask()` принимает 17 ортогональных kwargs. Никаких субклассов "ChatRAG", "AgenticRAG" и т.п. |
| **Test-on-merge** | 38 352 теста, CI запускает их параллельно. Никакой код не мерджится без зелёного теста. |

---

## 2. Слои

```
                            ┌──────────────────────────────────┐
   User / Integration       │  Скрипт / Скилл / Плагин / CLI    │
                            └────────────────┬─────────────────┘
                                             │ Python API
                            ┌────────────────┴─────────────────┐
   Composition surface      │   docstoolkit.rag.ask(...)        │  ← 17 kwargs
                            │   docstoolkit.rag.presets.*       │  ← 6 bundles
                            └────────────────┬─────────────────┘
                                             │
                            ┌────────────────┴─────────────────┐
   Pipeline orchestrator    │   RAGPipeline.run()               │  ← stages
                            │   _self_rag_run() reflect-loop    │
                            └────────────────┬─────────────────┘
                                             │
            ┌────────────────┬──────────────┼──────────────┬──────────────┐
   Stages   │  Retrieve      │  Filter      │  Rerank      │  Compose      │
            └────────┬───────┴──────┬───────┴──────┬───────┴──────┬───────┘
                     │              │              │              │
            ┌────────┴───────┐ ┌────┴──────┐ ┌────┴──────┐ ┌────┴───────┐
   Backends │ Retriever      │ │ Facets    │ │ Reranker  │ │ Answerer   │
            │ ├ keyword      │ │ apply_    │ │ ├ TFIDF   │ │ ├ Echo     │
            │ ├ semantic     │ │  filters  │ │ ├ BGE     │ │ ├ Anthropic│
            │ ├ hybrid       │ │           │ │ ├ LLM-jdg │ │ ├ OpenAI   │
            │ ├ adaptive     │ │           │ │ └ NoOp    │ │ └ Ollama   │
            │ └ personalized │ │           │ │           │ │            │
            └────────────────┘ └───────────┘ └───────────┘ └────────────┘
                     │
            ┌────────┴────────────────────────────────────────┐
   Storage  │   SQLite caches: embeddings, vectors, eval,     │
            │   profiles, jobs, audit, feedback, sessions     │
            └─────────────────────────────────────────────────┘
```

Каждая стадия в `RAGPipeline.run()` обёрнута в `_TraceTimer` (Phase III.1),
поэтому `result.trace` содержит wall-clock каждой стадии и payload-метаданные.

---

## 3. Точки расширения

### 3.1. Новый retriever

1. Реализовать `Retriever`-протокол: метод `search(query: str, top_k: int) -> list[Passage]`.
2. Зарегистрировать в `docstoolkit.rag.retriever.RETRIEVERS` или через plugin entry-point:

```toml
[project.entry-points."docstoolkit.retrievers"]
my_retriever = "my_pkg.retrievers:MyRetriever"
```

3. Использовать через `ask("...", method="my_retriever")`.

### 3.2. Новый answerer

1. Имплементировать `Answerer`-протокол: `answer(system, user, model) -> (text, tokens, cost)`.
2. Зарегистрировать аналогично через `docstoolkit.answerers` entry-point.
3. Использовать через `ask("...", answerer="my_answerer")`.

### 3.3. Новый rerank

1. Implement `Reranker.rerank(query, passages, top_k) -> list[Passage]`.
2. Передать инстанс прямо в `ask("...", reranker=MyReranker())` — DI, не registry.

### 3.4. Новый pipeline stage

Сейчас стадии встроены в `RAGPipeline.run()` (см. `docstoolkit/rag/pipeline.py:140-380`).
Добавление новой стадии: добавить булевый kwarg, `_TraceTimer`-блок, и
поле в `AnswerResult`.

В долгосрочном плане (Phase II.4 roadmap) стадии могут быть выделены в
`docstoolkit/rag/_stages.py` с явным контрактом
`Stage.apply(state) -> state`. Это даст plugin-механизм для пользовательских
стадий без правки `pipeline.py`.

---

## 4. Контракты данных

### 4.1. `Passage` (rag/types.py)

```python
@dataclass
class Passage:
    text: str           # тело фрагмента
    doc_id: str         # уникальный идентификатор (часто относительный путь)
    title: str = ""
    score: float = 0.0  # релевантность 0-1
    snippet_start: int = 0  # offset для span-attribution
```

### 4.2. `RAGQuery` (rag/types.py)

```python
@dataclass
class RAGQuery:
    question: str
    top_k: int = 5
    method: str = "hybrid"     # имя retriever
    answerer: str = "echo"     # имя answerer
    model: str = "claude-haiku-4-5-20251001"
    max_context_tokens: int = 8000
    include_citations: bool = True
    locale: str = "auto"
```

### 4.3. `AnswerResult` (rag/types.py)

Поля, которые передаются между всеми стадиями. Все вторичные результаты
(provenance, got_result, debate_result, mapreduce_trace, auction_result,
facets) — `Optional[object]` с дефолтом `None`/`[]`.

| Поле | Тип | Заполняется когда |
|---|---|---|
| `answer` | str | всегда |
| `citations` | list[dict] | `include_citations=True` |
| `retrieved_passages` | list[Passage] | всегда |
| `duration_ms` | int | всегда |
| `trace` | list[TraceEvent] | всегда (Phase III.1) |
| `facets` | list | `with_facets=True` |
| `provenance` | ProvenancedAnswer | `with_provenance=True` |
| `got_result` | GoTReasoningResult | `with_got=True` |
| `debate_result` | DebateResult | `with_debate=True` |
| `mapreduce_trace` | ReduceResult | `with_mapreduce=True` |
| `auction_result` | AuctionResult | `with_negotiation=True` |
| `at_commit` | str | `at_commit="<sha>"` |

### 4.4. `TraceEvent` (rag/types.py, Phase III.1)

```python
@dataclass
class TraceEvent:
    stage: str                    # "retrieve", "rerank", ..., "self_rag_iter"
    t_ms: float = 0.0             # wall-clock duration of the stage
    payload: dict[str, Any] = {}  # stage-specific (n_passages, kept, score, …)
```

---

## 5. Storage backbone

Все persistent ingredients используют SQLite — один файл, WAL, без сетевых
зависимостей.

| Хранилище | Файл | Назначение |
|---|---|---|
| Embeddings cache | `.docstoolkit/embeddings.sqlite` | IDF + vectors с content-hash инвалидацией |
| Online eval | `.docstoolkit/eval.sqlite` | Sampled query/answer pairs + scores |
| User profiles | `.docstoolkit/profiles.sqlite` | S6 per-user prefs + S7 read-receipts |
| Saved searches | `.docstoolkit/saved.sqlite` | S1 cron-style saved queries + alerts |
| Bandit experiments | `.docstoolkit/bandit.sqlite` | I7 UCB1 arm counts |
| Feedback | `.docstoolkit/feedback.sqlite` | Wilson confidence quality score |
| Sessions | `.docstoolkit/sessions.sqlite` | Multi-turn conversation history |
| KG triples | `.docstoolkit/kg.sqlite` | (Phase V) subject-predicate-object index |

---

## 6. Decision log

Architecture Decision Records — короткие записи о ключевых выборах.

### ADR-001: Single `ask()` функция вместо классов

**Контекст:** были варианты — `RAGClient.ask()`, `class AgenticRAG`, fluent
builder `RAGBuilder().with_provenance().ask(...)`.

**Решение:** одна функция с kwargs. Композиция через `setdefault` в presets.

**Последствия:** signatures длинные (`ask()` — 17 kwargs), но единая точка
входа — поиск, документация, монитор покрытия фич. Phase IX.1 (`COOKBOOK.md`)
делает порог входа минимальным.

### ADR-002: SQLite вместо Redis / Postgres

**Контекст:** требуется persistent кеш embeddings, profiles, jobs.

**Решение:** SQLite в `.docstoolkit/` директории.

**Последствия:**
- (+) ноль зависимостей, ноль настройки, ноль сети
- (+) atomic write через WAL
- (−) не масштабируется горизонтально — но это явный non-goal (см. README §non-goals)

### ADR-003: `_TraceTimer` через context manager, не через декоратор

**Контекст:** Phase III.1 нужно инструментировать каждую стадию `RAGPipeline.run()`.

**Решение:** `with _TraceTimer(trace, "retrieve") as tt: ...; tt.payload[...]=...`

**Последствия:**
- (+) payload можно добавлять _во время_ выполнения стадии
- (+) перенос через `try/except` прозрачен (`__exit__` не подавляет исключения)
- (−) overhead ~5-15 μs/stage. На реальных LLM-запросах (10-2000 ms) шум.

### ADR-004: `self_rag` композируется с GoT/debate/negotiation (Phase II.1)

**Контекст:** изначально `_self_rag_run` имел собственный мини-pipeline, который
форвардил только 7 из 17 kwargs.

**Решение:** `_self_rag_run` принимает `pipeline_kwargs: dict`; `ask()` строит
этот dict один раз и переиспользует для self-RAG loop и single-shot.

**Последствия:** все 17 фич ортогональны. Pipeline-логика — один контрактный
путь. Никаких feature-конфликтов в presets.

### ADR-005: `bench/history.jsonl` коммитится в репо

**Контекст:** для CI regression-check нужен baseline.

**Решение:** один baseline-снимок в репо; CI добавляет запись на каждый merge в main.

**Последствия:**
- (+) PR-проверка работает с первого дня
- (−) `history.jsonl` будет расти; через 100 merge'й — нужно ротация. Можно
  хранить последние N через `git filter-branch` или внешний artefact store.

---

## 7. Что НЕ часть архитектуры

- Векторные базы данных (Pinecone, Weaviate, …). Хотите — пишите plugin.
- Распределённый retrieval / sharding. SQLite + один процесс.
- Real-time collaboration (Yjs, CRDT). Не цель.
- GUI / desktop app. Серверная сторона + любой UI поверх HTTP.

---

## 8. Развитие

См. [`DEVELOPMENT_STATUS.md`](DEVELOPMENT_STATUS.md) — детальный план девяти
фаз с конкретными файлами, сигнатурами, тестами и exit-критериями.

---

*Последнее обновление: 2026-05-15, HEAD `787f1434`*
