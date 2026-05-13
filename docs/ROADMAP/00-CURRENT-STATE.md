# 00 — Текущее состояние Lorenzo / Knowledge OS

<!-- summary -->
> > Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.
**Проекты:** AgentFS, Yodoca, NGT Memory

---



> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Дата:** 2026-04-29
**Спринтов завершено:** 53
**Тестов:** 546 passed
**Модулей:** ~30 в `docs-toolkit/docstoolkit/` + 96 batch-скриптов в `scripts/`
**Документ:** часть серии ROADMAP. Соседние: [01-SIMPLE](./01-SIMPLE.md), [02-MEDIUM](./02-MEDIUM.md), [03-INNOVATIVE](./03-INNOVATIVE.md), [04-NOVEL](./04-NOVEL.md), [05-PRIORITIES](./05-PRIORITIES.md).

---

## 1. Концептуальная стадия

### 1.1 Идея

**Knowledge OS** — операционная среда для документной базы знаний, где документ становится первоклассным объектом наряду с процессом и пользователем. Корпус — не пассивное хранилище, а активная инфраструктура для поиска, рассуждения, оркестрации и обратной связи.

### 1.2 Архитектурный принцип

```
Скрипт (КАК)  →  Шаблон (ЧТО)  →  Скилл (КОГДА)  →  Плагин (ГДЕ)
```

Каждая ступень не заменяет предыдущую, а оркеструет её. Это даёт:
- Воспроизводимость на уровне скрипта
- Унификацию форматов на уровне шаблона
- Автоматический выбор инструмента на уровне скилла
- Размещаемость на уровне плагина (CLI, MCP, web, federation)

### 1.3 Принципы инженерии

| Принцип | Реализация |
|---------|-----------|
| stdlib-first | Большинство модулей работают без внешних зависимостей |
| Optional advanced | sentence-transformers, anthropic, openai — опциональные |
| Local-first | Всё работает offline; cloud — fallback / option |
| SQLite as backbone | Job queue, audit, vectors, feedback, sessions, webhooks |
| PEP 621 plugins | Discovery через entry_points, регистрация без правки ядра |
| Test-on-merge | 546 тестов, mcp-test 30/30, template integrity 23/23 |

---

## 2. Зрелость по слоям

| Слой | % | Что есть | Чего нет |
|------|--:|----------|----------|
| **Ingestion** | 80 | chunker, semantic chunks, multi-modal, language split, frontmatter | Инкрементальный индекс, watcher с дельтами |
| **Retrieval** | 85 | keyword, BM25, semantic (опц.), hybrid (RRF), adaptive multi-hop | Cross-encoder reranking, hierarchical, knowledge-graph traversal |
| **Reasoning** | 70 | RAG ask, agent loop, plan-and-execute, tools | Multi-agent debate, self-RAG, reflection |
| **Orchestration** | 75 | workflow DAG (sync+async), router с failover, jobs queue | Distributed workers, priority queues, DLQ |
| **Observability** | 80 | OTel traces, Prometheus metrics, feedback Wilson, A/B exp | Drift detection, online eval, anomaly alerts |
| **Governance** | 65 | auth/RBAC, budget guards, audit | Policy engine, data classification, retention rules |
| **Integration** | 60 | MCP server, federation (NPP), webhooks, events bus, SSE | Long-poll subscriptions, GraphQL gateway, gRPC |
| **Eval** | 75 | golden datasets, A/B exp, P/R/F1, Wilson conf | Counterfactual eval, online eval, drift метрики |
| **Memory** | 70 | conversation sessions, squash-summarize, context-window mgmt | Hierarchical memory, episodic/semantic split, MemGPT-style |
| **UI** | 30 | serve.py REST + SSE, MCP интеграция | React web app, mobile, voice |

---

## 3. Карта модулей `docstoolkit/`

| Модуль | Назначение | Ключевые типы |
|--------|------------|---------------|
| `agent/` | ReAct loop с tools + planner | `AgentLoop`, `Tool`, `Plan`, `Subtask` |
| `auth/` | RBAC scopes с wildcards | `User`, `Scope`, `check_scope` |
| `budget/` | Per-scope LLM budget guards | `BudgetTracker`, `BudgetRule`, `BudgetExceeded` |
| `cache/` | Memoize с TTL | `Cache`, `cached` |
| `cluster/` | k-means++ embedding clustering | `cluster_embeddings` |
| `conversation/` | Multi-turn sessions, squash-summarize | `ConversationStore`, `Session`, `Message` |
| `embeddings/` | Pluggable embedding providers | `Embedder`, `LocalEmbedder` |
| `eval/` | Golden datasets, P/R/F1 scoring | `GoldenSet`, `EvalResult` |
| `events/` | Pub-sub event bus | `EventBus`, `subscribe`, `publish` |
| `experiments/` | A/B framework | `Experiment`, `VariantResult`, `compare()` |
| `federation/` | NPP — Nautilus Portal Protocol | `Peer`, `query_peers`, `merge_results` |
| `feedback/` | SQLite store + Wilson quality score | `FeedbackStore`, `quality_score` |
| `frontmatter.py` | YAML frontmatter parser | `parse_yaml`, `extract_frontmatter` |
| `graph/` | Concept graph builder | `build_graph`, `to_dot`, `to_mermaid` |
| `ingest/` | Document loaders | `load_markdown`, `load_pdf` |
| `jobs/` | Background queue | `Job`, `Worker`, `enqueue` |
| `lang/` | RU/EN detection + split | `detect_language` |
| `prompts/` | Versioned prompts + A/B | `Prompt`, `PromptLibrary` |
| `rag/` | RAG pipeline + adaptive | `Retriever`, `ask`, `stream_rag`, `adaptive_search` |
| `router/` | Model chain failover | `ModelRouter`, `ModelChain`, `BUILTIN_CHAINS` |
| `serve.py` | HTTP/REST + SSE + Prometheus | endpoints `/api/ask`, `/api/stream/rag`, `/metrics` |
| `skills/` | Skill registry + testing | `Skill`, `SkillTestSuite` |
| `telemetry/` | OTel + Prometheus | `tracer`, `meter`, `prometheus_format` |
| `timetravel/` | Git-based historical queries | `query_at_commit`, `bisect_corpus` |
| `web/` | URL fetch + extract | `fetch_url`, `extract_main` |
| `webhooks/` | HTTP delivery с HMAC + DLQ | `WebhookDispatcher`, `Subscription`, `Delivery` |
| `workflow/` | DAG runner + parallel | `Workflow`, `Step`, `run`, `run_async` |

---

## 4. 96 batch-скриптов: 12 групп

| Группа | Скриптов | Назначение |
|--------|---------:|------------|
| `quality` | ~6 | Орфография, читаемость, content gaps, link preview |
| `export` | ~5 | Obsidian, EPUB, RSS/Atom, Confluence, REPORT.md |
| `cicd` | ~4 | GitHub Issues, workflows, pre-commit, dependabot |
| `analytics` | ~6 | Citations, reading time, version diff, topic model |
| `textwork` | ~9 | Reclassify, merge by topic, outline, compare, subtopic fill |
| `deeptext` | ~12 | TOC, abstracts, NER, timeline, concept graph, BM25, chunks |
| `nlpplus` | ~10 | TextRank, heading audit, language split, faceted search |
| `content` | ~3 | Auto-linker, gap-filler, empty sections fill |
| `meta` | ~9 | Tech radar, onboarding, risk register, KPI snapshot, INDEX |
| `llm` | ~4 | Enrich, summary, Q&A, contact (платные) |
| `reports` | ~10 | Health, metrics, scoring, badges, alerts |
| `infra` | ~18 | Run all, autofill, watch, benchmark, MCP server |

---

## 5. Что уже умеет (10 ключевых возможностей)

### 5.1 Полный локальный RAG

5+ retrievers (`keyword`, `bm25`, `semantic`, `hybrid` через RRF, `adaptive`) × 4 answerers (`echo`, `anthropic`, `openai`, `ollama`). Pipeline:

```
question → Retriever.search → assemble_prompt → Answerer.answer → AnswerResult
```

С автоматическим fallback до `echo` если LLM недоступен. Стабильно работает offline.

### 5.2 Многошаговый адаптивный поиск

`adaptive_search` (Sprint 53): запрос → confidence scoring → если низкая → reformulate → retry, до `max_hops` или порога. Накопление + dedup по `doc_id`, финальный re-ranking по score.

### 5.3 A/B-эксперименты любых конфигураций

`Experiment` (Sprint 44): варианты {retriever, answerer, model, params} × вопросы → markdown отчёт с Avg/Median ms, Tokens, Cost, Verdict (Fastest, Cheapest, Speed delta).

### 5.4 Eval против golden datasets

`GoldenSet` (Sprint 48): question + expected_answer_contains + expected_doc_ids + forbidden_phrases. Скоры: keyword overlap (0-100) для answer, P/R/F1 для citations. Итоговый weighted overall.

### 5.5 Многоходовые диалоги с памятью

`ConversationStore` (Sprint 49): SQLite sessions + messages. `history_for_llm` tail-fits к token budget. `squash_old` сжимает старые turns в `session.summary` через heuristic или custom summarizer.

### 5.6 Plan-and-execute

`heuristic_planner` + `execute_plan` (Sprint 50): декомпозирует «1) X 2) Y 3) Z» или «X и Y» в Subtasks, dependency-aware (depends_on). Опциональный `replanner` на failure.

### 5.7 Workflow DAG

`Workflow` (Sprint 47): топологическая сортировка + parallel execution per level. `$.context_var` / `$.STEP.output` reference syntax. on_error: fail/skip/retry. Cycle detection.

### 5.8 Cost-aware маршрутизация LLM

`ModelRouter` (Sprint 46): `ModelChain` из `ModelHop[]`, failover при ошибках, retry+backoff per hop, opt budget_check callback. Built-in: cheap/fast/balanced/high-quality.

### 5.9 Streaming token-by-token

`stream_rag` (Sprint 42): generator yields `passages_retrieved → token* → done | error`. SSE-endpoint `/api/stream/rag` в serve.py. Все answerers поддерживают (echo эмулирует chunked).

### 5.10 Federated retrieval

NPP протокол (Sprint 36): запрос распределяется по списку peers, ответы мерджатся через RRF. Каждый peer — независимый Lorenzo-инстанс с своим корпусом.

---

## 6. ~~Чего ещё **не** умеет (10 главных дыр)~~ — **РЕАЛИЗОВАНО** (спринт 54, 2026-05-13)

### 6.1 Knowledge graph reasoning

**Что не так:** entities извлекаются (`improve_named_entity_index.py`), но рассуждение по триплетам отсутствует. Нельзя спросить «какие проекты используются авторами из Anthropic vacancies, которые упоминают memory engines».

**Workaround сейчас:** ручной grep по NER-индексу + concept graph.

**Для чего нужно:** multi-hop вопросы по связям сущностей, factoid queries, transitive reasoning.

### 6.2 Cross-document synthesis

**Что не так:** retrieval отдаёт ranked passages, answerer склеивает в один prompt. Не умеет «сравни 5 этих с 3 теми, что общего, что разное» — фактически просто конкатенация.

**Workaround:** plan-and-execute с явной декомпозицией задачи.

**Для чего нужно:** аналитические задачи, обзоры литературы, сравнительные таблицы.

### 6.3 Cross-modal grounding

**Что не так:** multi-modal ingest есть (Sprint 38), но image-to-text связи не используются в retrieval. Картинка лежит в файле, но не привязана к relevant text spans.

**Workaround:** нет.

**Для чего нужно:** «найди диаграммы где упоминается AgentFS», «покажи мне фото системы X».

### 6.4 Active clarification

**Что не так:** ambiguous query («что насчёт памяти?») обрабатывается напрямую, без вопроса «вы про NGT Memory или Yodoca?». Нет detection двусмысленности.

**Workaround:** пользователь сам уточняет, видя плохой ответ.

**Для чего нужно:** меньше iteration cycles, лучший UX, особенно для новичков.

### 6.5 Корпусная динамика

**Что не так:** `improve_passage_retrieval.py --index` пересобирает всё. Нет инкрементального обновления при изменении одного файла. Watcher (`improve_watch.py`) только триггерит full rerun.

**Workaround:** периодический полный rebuild (быстрый на ~500 docs).

**Для чего нужно:** масштабируемость на 10K+ docs, near-real-time freshness.

### 6.6 Distributed processing

**Что не так:** jobs/workflow только в одном процессе (ThreadPoolExecutor). Нельзя раздать workers по машинам.

**Workaround:** запустить N инстансов с разными task subsets.

**Для чего нужно:** horizontal scaling, multi-tenant deployments, fault isolation.

### 6.7 Personalization

**Что не так:** один пользователь — один retriever default. Нет per-user стилевых предпочтений, истории интересов, learned ranking.

**Workaround:** ручная настройка via config per session.

**Для чего нужно:** разные команды используют общий корпус, но имеют разные приоритеты.

### 6.8 Counterfactual reasoning

**Что не так:** нельзя спросить «как изменился бы ответ если убрать документ X». Attribution не отслеживается на уровне span→source.

**Workaround:** ручной A/B с вариантом без файла.

**Для чего нужно:** debugging RAG, источниковедение, отладка hallucinations.

### 6.9 Self-improvement loop

**Что не так:** feedback собирается через `FeedbackStore`, Wilson scoring считается, но автоматически не используется для:
- замены prompt variant'а с лучшим winrate
- замены retriever method'а с лучшим P/R
- дообучения rerank weights

**Workaround:** manual review feedback report → ручная переконфигурация.

**Для чего нужно:** evergreen system, что улучшается без human intervention.

### 6.10 True long-context

**Что не так:** `assemble_prompt` усекает по `max_context_tokens`. Нет hierarchical attention к нужным фрагментам в большом наборе passages, нет map-reduce summarization для запросов с >50 documents.

**Workaround:** уменьшить `top_k`, надеяться что top-K достаточно.

**Для чего нужно:** queries вроде «обобщи всё что мы знаем про authoring tools».

---

## 7. Метрики проекта

_Обновлено: 2026-05-13 (спринт 54)_

| Метрика | Значение |
|---------|---------:|
| Спринтов завершено | **54** |
| Модулей в `docstoolkit/` | **~42** |
| Batch-скриптов в `scripts/` | 155 |
| Тестов pytest | **888** |
| MCP-инструментов | 30 |
| Шаблонов с integrity check | 23 |
| Документов в `docs/` | 2484 |
| Habr-проектов проанализировано | 22 |
| Контактов авторов готово | 14 |
| LOC `docs-toolkit/` (.py) | ~21K |
| Здоровье репо (HEALTH.md) | **99/100** |
| GO/No-Go score (SCORING.md) | 96% → GO |
| Версия `docs-toolkit` | **0.3.0** |

### Новые модули (спринт 54)

| Модуль | Фича | Тестов |
|--------|------|-------:|
| `graph/reasoning.py` | Knowledge Graph: TripletStore, BFS, multi-hop | 24 |
| `rag/synthesis.py` | Cross-doc synthesis: compare/summarize/contrast | 33 |
| `ingest/grounding.py` | Cross-modal grounding: ImageIndex→Passage | 20 |
| `rag/clarifier.py` | Active clarification: detect_ambiguity, ClarifyingRAG | 21 |
| `embeddings/incremental.py` + `watcher.py` | Incremental index + polling watcher | 23 |
| `jobs/distributed.py` | Distributed workers: SQLite atomic claim, tag routing | 21 |
| `conversation/profile.py` | Personalization: ProfileStore, PersonalizedRetriever | 28 |
| `rag/counterfactual.py` | Forensic RAG: SpanAttribution, ForensicRAG.explain() | 40 |
| `feedback/autotuner.py` | Self-improvement: AutoTuner, wilson_lower, apply_to_config | 28 |
| `rag/mapreduce.py` | True long-context: map_reduce_ask, chunk→map→reduce | 37 |
| `rerank/reranker.py` | Cross-encoder reranking: TFIDF/LLM/BGE, rerank() | 42 |
| `online_eval/` | Continuous online eval: sampler, DriftReport | 32 |
| `alerts/store.py` | Saved searches + alerts: cooldown, tick() | 27 |
| `citations/graph.py` | Citation graph + PageRank (alpha=0.85) | 33 |
| `serve.py` (+/faceted) | Faceted Search UI: HTML + /api/faceted | 23 |

---

## 8. Что это значит — стратегически

Текущее состояние — **production-ready platform для knowledge workers**, с полным покрытием всех архитектурных слоёв, 888 тестами и 42 модулями. Все 10 архитектурных дыр закрыты. Добавлены реранкинг, online eval, алерты, citation graph, faceted UI.

**Сильные стороны:**
- **Все 10 gaps закрыты** — от knowledge graph до long-context map-reduce
- Stdlib-first позволяет deploy куда угодно
- 888 тестов (было 546)
- 53 спринта прошли без архитектурных переписываний → дизайн стабилен

**Узкие места:**
- Многое работает, но не всегда хорошо (semantic search требует sentence-transformers, knowledge graph отсутствует)
- UI слабый — fokus был на CLI/SDK/API
- Нет deploy story для multi-tenant / multi-user / SaaS

**Возможности развития** — см. документы `01-SIMPLE.md`, `02-MEDIUM.md`, `03-INNOVATIVE.md`, `04-NOVEL.md`. Приоритеты — в `05-PRIORITIES.md`.

<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [01-SIMPLE](01-SIMPLE.md)
- [02-MEDIUM](02-MEDIUM.md)
- [03-INNOVATIVE](03-INNOVATIVE.md)
- [04-NOVEL](04-NOVEL.md)
- [05-PRIORITIES](05-PRIORITIES.md)
- [README](README.md)


<!-- see-also -->

---

**Смотрите также:**
- [02-MEDIUM](02-MEDIUM.md)
- [CHANGELOG_AUTO](../CHANGELOG_AUTO.md)
- [03-INNOVATIVE](03-INNOVATIVE.md)
- [01-SIMPLE](01-SIMPLE.md)

