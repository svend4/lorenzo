---
state: approved
tags: [roadmap, architecture, planning, knowledge-os, docs-toolkit, sprint-plan]
---

# Lorenzo — План продолжения разработки: Phases X–XX

> [!IMPORTANT]
> Документ описывает **следующий горизонт работ** (после Phases I–IX
> docs-toolkit и итераций 0–15 прототипа Knowledge OS).
> Фокус — **новые возможности** (по выбору пользователя 2026-05-15).
> Закрытие MVP, hardening и unblock отложенных фаз идут параллельно
> отдельными треками — см. §10 «Сопутствующие треки».

_Дата: 2026-05-15 · Ветка: `claude/continue-development-BrDvi` · HEAD: `26fc001c`_

---

## 0. TL;DR

| Параметр | Значение |
|---|---|
| Длительность плана | **10 фаз / ~26 спринтов / ~6 месяцев** |
| Стартовая база | docs-toolkit v0.3.0 (489 модулей, 546 test-files), MVP 64% (7/11) |
| Целевой выпуск | docs-toolkit **v0.5.0** (production-grade) → дальше v1.0 |
| Главный риск | Расхождение API при росте поверхности (контракт-тесты обязательны на каждой ветке) |
| Критерий успеха | Все 10 «Чего нет» из `ROADMAP/00-CURRENT-STATE.md §2` закрыты, либо явно отложены с обоснованием |

**Фазовая структура** (каждая фаза самодостаточна и может быть отгружена изолированно):

| # | Фаза | Сприн­тов | Что закрывает |
|---|---|---:|---|
| X | Distributed orchestration | 4 | workers, priority queues, DLQ at scale |
| XI | Observability & drift detection | 3 | drift, anomaly alerts, eval-history dashboard |
| XII | Governance & retention | 3 | policy engine, retention rules, PII-классификация |
| XIII | Integration surface | 3 | GraphQL gateway, gRPC, long-poll subscriptions |
| XIV | Eval science | 3 | counterfactual rigour, drift-метрики, online A/B |
| XV | Memory tiering | 2 | episodic/semantic split, MemGPT-grade promotion |
| XVI | UI & voice | 3 | React web app, voice (Whisper), mobile-ready |
| XVII | Deferred unblock | 3 | NPP hosted federation, marketplace registry, OpenAI gateway |
| XVIII | Multi-tenancy | 2 | workspaces с изоляцией, per-tenant quotas |
| XIX | Agentic v2 | 2 | MCP-native loops, tool composition, autonomous agents |

**Параллельные треки** (не блокируют roadmap): MVP-completion, release 0.4.0, security review.

---

## 1. Reference state (snapshot 2026-05-15)

### 1.1 Что уже есть

| Слой | Зрелость | Артефакты |
|---|---:|---|
| Ingestion | 80 % | `ingest/` (md/pdf/mhtml/jupyter/html/url/arxiv/hackernews/habr), `frontmatter`, `lang/`, `M7` incremental indexing |
| Retrieval | **95 %** | keyword / BM25 / semantic / hybrid RRF / adaptive multi-hop / hierarchical / KG-boosted / PageRank-boosted / cross-encoder / fused (learned) |
| Reasoning | **90 %** | RAG `ask()` с 17 ortho-kwargs, ReAct agent, plan-and-execute, self-RAG, multi-agent debate, graph-of-thoughts, negotiation, map-reduce |
| Orchestration | 75 % | workflow DAG (sync+async), router failover, jobs queue — **нет distributed workers и full DLQ** |
| Observability | 80 % | OTel traces, Prometheus, feedback Wilson, A/B exp, trace markdown — **нет drift detection и anomaly alerts** |
| Governance | 70 % | RBAC scopes, budget guards, audit, doc classification — **нет policy engine и retention** |
| Integration | 65 % | MCP server (17 tools), NPP federation (3 nodes local), webhooks с HMAC+DLQ, events bus, SSE — **нет GraphQL/gRPC/long-poll** |
| Eval | 80 % | golden datasets P/R/F1, A/B exp, Wilson, counterfactual probing, federated eval — **нет drift-метрик в production** |
| Memory | 75 % | conversation sessions, squash-summarize, TieredMemory (MemGPT-style) — **нет episodic/semantic явного split** |
| UI | 35 % | `serve.py` REST + SSE + Prometheus, MCP, Streamlit Review Queue — **нет web app, mobile, voice** |
| Privacy | 75 % | Gaussian DP, PrivacyAccountant, secure aggregation (Bonawitz) |
| Knowledge Graph | 85 % | TripleStore (SQLite WAL), mini Query DSL, hash-join, KGRetriever, kg bench suite |
| Deployment | 70 % | `Dockerfile`, `Dockerfile.bge`, docker-compose profiles, Helm chart |
| Composition | 100 % | 17 ortho kwargs + 6 presets + 18 standalone helpers + 8 demo scripts |

### 1.2 Что отложено (из DEVELOPMENT_STATUS.md)

| ID | Фаза | Причина отложения |
|---|---|---|
| VI.3 | NPP federation hosted server | Нужна hosted сетевая инфраструктура |
| VII.3 | Marketplace registry | PyPI остаётся каналом, hosted registry — backlog |
| VIII.3 | OpenAI-compatible gateway в `serve.py` | Частично есть в Lorenzo `gateway.py`, нужно портирование |

### 1.3 Что недозакрыто на стороне прототипа Knowledge OS

| Артефакт | Статус | Действие |
|---|---|---|
| 32 контакт-файла в `docs/contacts/` | ⏳ не отправлены | Ручная отправка |
| LLM-обогащение проектных файлов | ⏳ не запущено | `improve_llm_enrich.py` за ~$0.011 |
| Публикация MVP на GitHub | ⏳ не сделано | Создать публичное зеркало |

→ Эти три пункта закрываются параллельным треком (см. §10).

---

## 2. Gap analysis: «Чего нет» → план Phase X+

Все 35 пунктов roadmap (Path A/B/C) закрыты в Phases I–IX. План Phase X+
адресует **второй слой** — gaps, которые видны при росте production usage:

```
                       │ Quick win │ Medium │ Strategic
───────────────────────┼───────────┼────────┼───────────
 Distributed scale     │     —     │  Ph.X  │  Ph.XVIII
 Observability mature  │  Ph.XI    │  Ph.XIV│
 Compliance/security   │  Ph.XII   │  —     │  Ph.XVII security audit
 Integration breadth   │  Ph.XIII  │  —     │  Ph.XVII (deferred unblock)
 Eval rigour           │  —        │  Ph.XIV│
 Memory depth          │  Ph.XV    │  —     │
 UI/UX surface         │  —        │  Ph.XVI│  Ph.XIX (agentic)
```

---

## 3. Phase X — Distributed orchestration (4 спринта)

**Цель:** убрать ограничение «один процесс — одна очередь», подготовить пакет
к горизонтальному масштабированию.

### X.1 — Distributed worker pool

- 📦 `docstoolkit/jobs/distributed.py` — координация через SQLite WAL +
  `SELECT ... FOR UPDATE SKIP LOCKED` (PostgreSQL-fallback)
- 🔧 `Worker` класс с heartbeat, lease, graceful shutdown
- 🧪 `tests/test_jobs_distributed.py` — N-worker, no double-take, lease expiry
- **Exit:** 4 worker × 1000 jobs выполняются без дубликатов, latency P99 ≤ baseline × 1.2

### X.2 — Priority queues + fair scheduling

- 🔧 `docstoolkit/priority_queue/scheduler.py` — weighted round-robin между tenants
- 🧪 `tests/test_priority_scheduler.py` — голодание не возникает при ratio 10:1
- **Exit:** при загрузке 80 % high-prio jobs, low-prio jobs обрабатываются с задержкой ≤ 5×

### X.3 — Full DLQ с replay

- 🔧 `docstoolkit/dlq/store.py` — расширить, добавить replay-API и retry-budget per job-type
- 📦 `docstoolkit/dlq/replay.py` — `replay_dlq(filter, mode="dry-run|apply")`
- 🧪 `tests/test_dlq_replay.py` — корректно обрабатывает дубли через idempotency keys
- **Exit:** failed job можно replay с конкретного шага после фикса без потери порядка

### X.4 — Distributed lock service

- 🔧 `docstoolkit/dist_lock/manager.py` — SQLite/Postgres-backed lease locks
  (уже частично есть; нужно добавить fencing tokens)
- 🧪 `tests/test_dist_lock.py` — раздельный fencing token проверка
- **Exit:** при network partition expired lock не позволяет write-back с устаревшим token

**Метрики фазы X:** jobs throughput 4× (с 4-worker), zero lost jobs в 24 h soak test.

---

## 4. Phase XI — Observability & drift detection (3 спринта)

**Цель:** добавить production-grade сигналы качества и аномалий.

### XI.1 — Drift detection в retrieval

- 📦 `docstoolkit/concept_drift/detector.py` — KS-тест на distribution scores
- 🔧 `RAGPipeline.run()` — эмитит `drift_score` в trace
- 🧪 `tests/test_concept_drift.py` — synthetic shift detection
- **Exit:** drift detected на golden-set после искусственного 20 %-перекоса query-distribution

### XI.2 — Anomaly alerts

- 📦 `docstoolkit/anomaly/detector.py` — sliding window z-score over latency / error rate
- 🔧 `serve.py` → `/api/alerts/recent` + Webhook delivery через `webhooks/`
- 🧪 `tests/test_anomaly_alerts.py`
- **Exit:** при p95 latency × 3 webhook доставлен ≤ 30 с

### XI.3 — Eval-history dashboard

- 📦 `docs-toolkit/QUALITY_HISTORY.md` — autogenerated из `bench/history.jsonl` + golden eval runs
- 🔧 `bench/runner.py` — добавить золотую регрессионную suite (P/R/F1 over time)
- 🔧 `serve.py` → `/api/eval/history` (HTML + JSON)
- **Exit:** в CI блокируется PR при регрессии Recall@5 > 3 % p-stat значимая

**Метрики фазы XI:** все production-инциденты последних 90 дней реконструируемы из traces+alerts.

---

## 5. Phase XII — Governance & retention (3 спринта)

**Цель:** закрыть compliance-gap для коммерческого использования.

### XII.1 — Policy engine

- 📦 `docstoolkit/policy_engine/engine.py` — declarative rules (Rego-style mini-DSL)
- 🔧 RAG `ask()` и MCP-tools прогоняют запрос через policy перед выполнением
- 📝 `docs-toolkit/POLICIES.md` — примеры (PII-блокировка, scope-restrictions)
- 🧪 `tests/test_policy_engine.py` — 20+ scenarios
- **Exit:** запрещённый запрос блокируется до retrieval с понятной ошибкой

### XII.2 — PII classification + redaction

- 📦 `docstoolkit/data_masking/classifier.py` — regex + stoplist + (опц.) NER
- 🔧 ingest pipeline помечает passages `pii: true|false|category`
- 🔧 `ask(redact_pii=True)` — заменяет PII на `[REDACTED]`
- 🧪 `tests/test_pii_masking.py`
- **Exit:** golden-set с PII-инъекциями redacted на 95 % без false-positive > 5 %

### XII.3 — Retention rules

- 📦 `docstoolkit/doc_retention_policy/policy.py` — TTL, archive-after, hard-delete-after
- 🔧 Daily CI: `improve_retention_apply.py` — переносит истёкшие документы в `_archive/`
- 🔧 Audit trail для каждой retention-операции
- 🧪 `tests/test_retention_policy.py`
- **Exit:** документ с `retain_until: 2026-01-01` архивирован при следующем run

**Метрики фазы XII:** policy + PII + retention покрывают GDPR Art. 5, 17, 25 (документировано в COMPLIANCE.md).

---

## 6. Phase XIII — Integration surface (3 спринта)

**Цель:** расширить набор протоколов для интеграции в чужие стеки.

### XIII.1 — GraphQL gateway

- 📦 `docstoolkit/web/graphql.py` — strawberry-schema (опц. зависимость)
- 🔧 schema: `Query { ask, docs, traces }`, `Mutation { addCard, decay }`, `Subscription { traces, alerts }`
- 🧪 `tests/test_graphql_gateway.py`
- **Exit:** Apollo Client сделает Ask-запрос с фильтрами через GraphQL

### XIII.2 — gRPC bindings (опц.)

- 📦 `docstoolkit/web/grpc/` — proto + server stub для `Ask`, `IngestStream`, `WatchAlerts`
- 🔧 (опц. зависимость `grpcio`)
- 🧪 `tests/test_grpc_bindings.py`
- **Exit:** gRPC-клиент на Python и Go может вызвать `Ask`

### XIII.3 — Long-poll subscriptions

- 🔧 `serve.py` → `/api/subscribe?topic=...&since=...` — long-poll до 60s
- 🔧 интеграция с `events/` bus
- 🧪 `tests/test_long_poll.py`
- **Exit:** клиент получает event ≤ 1 с после публикации

**Метрики фазы XIII:** один и тот же запрос можно сделать через REST, GraphQL, gRPC, MCP — все 4 эндпоинта возвращают эквивалентный ответ (контракт-тест).

---

## 7. Phase XIV — Eval science (3 спринта)

**Цель:** перевести eval из retrospective в continuous quality science.

### XIV.1 — Counterfactual eval rigour

- 🔧 `docstoolkit/rag/counterfactual.py` — расширить, добавить **delta attribution**
- 📦 `docstoolkit/counterfactual_corpus/runner.py` — генерация alt-корпусов и diff metrics
- 🧪 `tests/test_counterfactual_rigour.py`
- **Exit:** для каждого topic из TOPIC_MODEL — отдельный counterfactual score

### XIV.2 — Drift метрики в production

- 📦 `docstoolkit/online_eval/drift.py` — population stability index по query→answer
- 🔧 `/api/eval/drift` — текущий PSI, ChiSquare
- 🧪 `tests/test_online_drift.py`
- **Exit:** при искусственном 30 %-сдвиге PSI > 0.25 в течение 24h

### XIV.3 — Online A/B-tests с auto-stop

- 🔧 `docstoolkit/experiments/auto_stop.py` — Sequential Probability Ratio Test (SPRT)
- 🔧 `experiments/runner.py` — авто-останов A/B при p < 0.05 или min_n
- 🧪 `tests/test_auto_stop.py`
- **Exit:** A/B бежит max 7 дней либо до значимости, что наступит раньше

**Метрики фазы XIV:** Recall@5, drift-PSI, A/B win-rate доступны в `/api/eval/dashboard` без ручных запусков.

---

## 8. Phase XV — Memory tiering (2 спринта)

**Цель:** дать пользователю чёткую модель «что помнится, что забывается».

### XV.1 — Episodic / semantic split

- 📦 `docstoolkit/memory/tiered.py` — расширить `TieredMemory`:
  - **episodic**: raw events (last N hours), FIFO
  - **semantic**: extracted facts (consolidated), permanent
- 🔧 `ask(memory=...)` — раздельный recall по tier
- 🧪 `tests/test_memory_tiers.py`
- **Exit:** факт из эпизода 7-дневной давности промотируется в semantic после 3 ре-упоминаний

### XV.2 — MemGPT-grade promotion policy

- 🔧 `docstoolkit/memory/promotion.py` — правила promotion/demotion
  (по frequency, recency, importance score из LLM-judge)
- 🔧 daily CI job для replay promotion на исторических сессиях
- 🧪 `tests/test_memory_promotion.py`
- **Exit:** на golden conversation set semantic memory hit rate ≥ 60 %

**Метрики фазы XV:** working set ≤ 4 K токенов при корпусе фактов ≥ 100 K.

---

## 9. Phase XVI — UI & voice layer (3 спринта)

**Цель:** закрыть критический gap зрелости (UI 35 % → 70 %).

### XVI.1 — React web app (минимальный)

- 📦 `packages/web-ui/` — Vite + React + TanStack Query
- Стартовые views: Ask, Traces, Eval History, Cards-Inbox
- 🔧 build → `dist/` мounted под `serve.py /ui`
- 🧪 e2e via Playwright (опц.)
- **Exit:** локальный `docker run` отдаёт работающий UI на `:8000/ui`

### XVI.2 — Voice input (Whisper opt-in)

- 📦 `docstoolkit/web/voice.py` — `/api/voice/transcribe` (whisper-cpp wrapper, опц.)
- 🔧 UI-кнопка mic → upload → transcribe → ask
- 🧪 `tests/test_voice_endpoint.py` (mock whisper)
- **Exit:** короткий WAV → текстовый ответ ≤ 5 с end-to-end

### XVI.3 — Mobile-ready PWA

- 🔧 PWA manifest + service worker (offline-first для последнего ответа)
- **Exit:** Lighthouse score ≥ 80 для PWA category

**Метрики фазы XVI:** UI зрелость 35 % → ≥ 70 % (по таблице из ROADMAP/00).

---

## 10. Phase XVII — Deferred unblock (3 спринта)

Закрывает 3 пункта, оставленные «отложенными» в Phases I–IX.

### XVII.1 — NPP federation hosted нод

- 🔧 `docstoolkit/federation/npp_server.py` — standalone NPP node-runner
- 🔧 `deploy/helm/npp-node/` — Helm chart для node-deployment
- 🧪 `tests/test_npp_3node.py` — реальная 3-node simulation (через docker-compose в CI)
- **Exit:** 3 nodes на разных хостах отдают консолидированный P/R/F1 с DP-noise

### XVII.2 — Plugin marketplace registry

- 📦 `docstoolkit/plugins/registry.py` — `discover_remote(index_url)`
- 🔧 `docs-toolkit-registry` — отдельный мини-репо с `index.json`
- 🔧 CLI: `docstoolkit plugins search`, `install`, `enable`
- 🧪 `tests/test_marketplace.py`
- **Exit:** третий пакет можно поставить и активировать без правок ядра

### XVII.3 — OpenAI gateway в `serve.py`

- 🔧 портировать `scripts/gateway.py` функционал в `docstoolkit/serve.py`
  как `/v1/chat/completions`, `/v1/embeddings`, `/v1/models`
- 🧪 `tests/test_openai_compat.py` — `openai` SDK как клиент
- **Exit:** `OPENAI_BASE_URL=http://localhost:8000/v1 openai api …` работает

**Метрики фазы XVII:** все 3 deferred-пункта из DEVELOPMENT_STATUS закрыты.

---

## 11. Phase XVIII — Multi-tenancy & workspaces (2 спринта)

**Цель:** изоляция данных и квот между tenants на одном инстансе.

### XVIII.1 — Workspace isolation

- 📦 `docstoolkit/doc_workspace/manager.py` — расширить, добавить `WorkspaceContext`
- 🔧 все store-операции принимают `workspace_id`, фильтруют по нему
- 🧪 `tests/test_workspace_isolation.py` — cross-workspace leak отсутствует
- **Exit:** `ask(workspace="A")` не видит документы из workspace B

### XVIII.2 — Per-tenant quotas & budgets

- 🔧 `docstoolkit/budget/multitenant.py` — расширить scope: tenant + user + global
- 🔧 `/api/admin/quotas` — CRUD для admin
- 🧪 `tests/test_multitenant_quota.py`
- **Exit:** tenant с 0 budget получает 402 Payment Required

---

## 12. Phase XIX — Agentic workflows v2 (2 спринта)

**Цель:** перевести агентов в MCP-native loop с tool composition.

### XIX.1 — MCP-native agent loop

- 📦 `docstoolkit/agent/mcp_loop.py` — агент работает поверх MCP-tools
  (не через REST), tool-calls сериализуются как MCP-сообщения
- 🔧 пример: «исследовать корпус, написать summary, отправить webhook»
- 🧪 `tests/test_mcp_agent_loop.py`
- **Exit:** агент выполняет 5-step workflow только через MCP-вызовы

### XIX.2 — Tool composition + autonomous loops

- 📦 `docstoolkit/agent/composition.py` — DSL для композиции tools
- 🔧 авто-останов через `budget_guard` + max steps
- 🧪 `tests/test_tool_composition.py`
- **Exit:** агент исполняет план из 3 связанных tool-calls без human-in-the-loop

---

## 13. Сопутствующие треки (параллельно roadmap)

### 13.1 MVP completion (1-2 недели, **не блокирует Phase X**)

| Задача | Скрипт / артефакт | Эффорт |
|---|---|---|
| Отправить 16 контактных писем | `docs/contacts/*.md` → email/Habr/GitHub | 4 часа ручной работы |
| LLM-обогащение проектных файлов | `pip install anthropic && python scripts/improve_llm_enrich.py` | 30 мин + ~$0.011 |
| Сбор и логирование ответов | `improve_contact_status.py --note` | rolling |
| Публикация MVP на GitHub | `git push` на публичное зеркало + README polish | 2 часа |

→ Закрывает milestones 6, 7, 8, 11 в `PROGRESS.md` (MVP 64 % → 100 %).

### 13.2 Release 0.4.0 (после Phases X–XII)

- Bump `pyproject.toml` 0.3.0 → 0.4.0
- CHANGELOG entries за все 10 фаз
- API stability review (что в `__all__`, что deprecate)
- Migration guide дополнить (`MIGRATING.md` §2 «from 0.3 to 0.4»)

### 13.3 Security review (после Phase XII)

- Threat model document
- Dependency audit (`pip-audit`)
- Secrets scan в CI (`gitleaks` уже стоит)
- Sandbox hardening review (VII.2 уже частично закрыт)

### 13.4 Documentation sync (continuous)

- `ROADMAP/00-CURRENT-STATE.md` — обновлять после каждой фазы
- `KNOWLEDGE_SNAPSHOT.md` — daily CI
- `DEVELOPMENT_STATUS.md` — расширять таблицу Phases X+ по мере завершения

---

## 14. Dependency graph (критический путь)

```
              ┌──────── Phase X  (distributed orchestration) ────────┐
              │                                                       │
   start ─────┤                                                       │
              │                                                       ▼
              ├──────── Phase XI (observability/drift) ──────┐  Phase XVIII
              │                                              │  (multi-tenant)
              │                                              ▼
              ├──────── Phase XII (governance) ──────────► COMPLIANCE
              │                                              │
              │                                              ▼
              ├──────── Phase XIII (integration: GraphQL/gRPC) ─► Phase XVII.3
              │                                              │     (OpenAI gateway)
              │                                              │
              ├──────── Phase XIV (eval science) ───────────►│
              │                                              │
              ├──────── Phase XV (memory tiering) ──────────►│
              │                                              │
              ├──────── Phase XVI (UI/voice) ────────────────┤
              │                                              │
              ├──────── Phase XVII (deferred unblock) ──────►│
              │                                              │
              └──────── Phase XIX (agentic v2) ─────────────►└──► v1.0
```

**Параллельно можно вести:** X+XI (разные слои), XII+XIII (compliance vs.
integration), XIV+XV+XVI (квалитет/память/UI независимы).

**Блокирующие зависимости:**
- XVII.3 (OpenAI gateway) проще после XIII (общий router/streaming layer)
- XVIII (multi-tenant) опирается на XII (policy engine для scope-rules)
- XIX (agentic v2) опирается на XVII.2 (marketplace для шаринга tools)

---

## 15. Risk register

| ID | Риск | Уровень | Митигация |
|---|---|:---:|---|
| R-1 | Phase X (distributed) ломает single-process flow | M | Feature-flag `DOCSTOOLKIT_DISTRIBUTED=1` + backwards-compat тесты |
| R-2 | Policy engine (XII.1) усложняет каждый запрос | M | Кешировать compiled policies, bench overhead ≤ 50 μs |
| R-3 | GraphQL/gRPC (XIII) тянут heavy deps | L | Опциональные зависимости через extras_require |
| R-4 | Drift detection (XI.1) даёт false alarms | M | Hysteresis + min sample size в детекторе |
| R-5 | Multi-tenant (XVIII) — leaks через shared cache | H | Cache namespace по `workspace_id`, контракт-тест на изоляцию |
| R-6 | React UI (XVI.1) растёт неконтролируемо | M | Cap при 5 ключевых views; web-ui отдельный pnpm-package |
| R-7 | NPP federation (XVII.1) DP-noise делает данные шумными | M | Сначала semi-honest, потом добавлять DP по необходимости |
| R-8 | OpenAI gateway compatibility (XVII.3) drift с upstream | M | Pin OpenAI SDK version в test, smoke-тесты раз в 2 недели |
| R-9 | Agentic v2 loops (XIX) — стоимость в LLM | M | Жёсткий `budget_guard` + max_steps по умолчанию |
| R-10 | Documentation rot при росте поверхности | H | `docs.yml` CI отвергает PR без обновления CHANGELOG / PROFILES |

---

## 16. Sprint allocation (suggested)

| Спринт | Главная работа | Параллельно |
|:---:|---|---|
| 1 | X.1 distributed worker pool | MVP track: отправить первые 5 контактов |
| 2 | X.2 priority queues + X.3 DLQ replay | MVP track: LLM-обогащение |
| 3 | X.4 dist lock + XI.1 drift detector | doc sync |
| 4 | XI.2 anomaly alerts + XI.3 eval history | release 0.4.0-rc1 |
| 5 | XII.1 policy engine | XIII.1 GraphQL gateway parallel |
| 6 | XII.2 PII masking | XIII.2 gRPC bindings |
| 7 | XII.3 retention rules | XIII.3 long-poll |
| 8 | XIV.1 counterfactual rigour | release 0.4.0 final |
| 9 | XIV.2 drift metrics | XV.1 memory tiers |
| 10 | XIV.3 SPRT auto-stop | XV.2 memory promotion |
| 11 | XVI.1 React UI skeleton | XVII.1 NPP hosted node |
| 12 | XVI.2 voice transcribe | XVII.2 marketplace registry |
| 13 | XVI.3 PWA polish | XVII.3 OpenAI gateway in serve.py |
| 14 | XVIII.1 workspace isolation | release 0.5.0-rc1 |
| 15 | XVIII.2 per-tenant quotas | security review |
| 16 | XIX.1 MCP-native agent loop | docs polish |
| 17 | XIX.2 tool composition | release 0.5.0 |
| ... | (буфер: bug fixes, eval regressions, dependency updates) | |

**Cap:** 1 ведущая фаза + 1 параллельная фаза + 1 doc/release task per sprint.

---

## 17. Exit criteria для всего плана

После выполнения Phases X–XIX:

| Метрика | Текущее | Цель | Источник |
|---|:---:|:---:|---|
| Module count | 489 | ≥ 550 | `find docstoolkit -maxdepth 1 -type d` |
| Test files | 546 | ≥ 700 | `find docs-toolkit/tests -name 'test_*.py'` |
| Coverage (lines) | ~? | ≥ 80 % | `pytest --cov` (нужно добавить в CI) |
| Recall@5 (golden) | baseline | +10 % | `bench/QUALITY_HISTORY.md` |
| `ask_baseline` p50 | 40 μs | ≤ 50 μs (не деградируем) | `bench/BENCHMARKS.md` |
| HEALTH score | 99/100 | ≥ 99/100 | `docs/HEALTH.md` |
| Maturity layers ≥ 80 % | 6/14 | ≥ 12/14 | `ROADMAP/00-CURRENT-STATE.md §2` |
| Deferred items | 3 | 0 | `DEVELOPMENT_STATUS.md` |
| MVP milestones | 7/11 | 11/11 | `docs/PROGRESS.md` |

---

## 18. Команды для старта

```bash
# 1. Sanity check: всё ли зелёно перед стартом
python -m pytest docs-toolkit/tests/ -q --tb=line
python scripts/improve_run_all.py --group reports
python scripts/improve_health.py

# 2. Создать ветку для Phase X
git checkout -b feature/phase-x-distributed

# 3. Первый коммит: X.1 distributed worker pool
mkdir -p docs-toolkit/docstoolkit/jobs
touch docs-toolkit/docstoolkit/jobs/distributed.py
touch docs-toolkit/tests/test_jobs_distributed.py
# … (см. exit criteria X.1)

# 4. После Phase X — обновить документацию
python scripts/improve_progress.py
python scripts/improve_knowledge_snapshot.py
```

---

## 19. Связанные документы

- [`README.md`](../README.md) — обзор репозитория (обновлён 2026-05-15)
- [`CLAUDE.md`](../CLAUDE.md) — контекст для Claude Code
- [`docs-toolkit/README.md`](../docs-toolkit/README.md) — overview пакета
- [`docs-toolkit/DEVELOPMENT_STATUS.md`](../docs-toolkit/DEVELOPMENT_STATUS.md) — детальный статус Phases I–IX (база этого плана)
- [`docs-toolkit/ARCHITECTURE.md`](../docs-toolkit/ARCHITECTURE.md) — 5 ADRs архитектуры
- [`docs-toolkit/PROFILES.md`](../docs-toolkit/PROFILES.md) — composition matrix 17 kwargs
- [`docs/ROADMAP/00-CURRENT-STATE.md`](ROADMAP/00-CURRENT-STATE.md) — зрелость по слоям
- [`docs/ROADMAP/05-PRIORITIES.md`](ROADMAP/05-PRIORITIES.md) — 3 стратегических пути (исторический контекст)
- [`docs/DEVELOPMENT_PLAN.md`](DEVELOPMENT_PLAN.md) — план Phases 1–15 (исторический)
- [`docs/PROGRESS.md`](PROGRESS.md) — MVP milestones, 64 % → 100 % в треке 13.1
- [`docs/RISK_REGISTER.md`](RISK_REGISTER.md) — общий реестр рисков
- [`docs/CI_COST_INCIDENT_2026-05-14.md`](CI_COST_INCIDENT_2026-05-14.md) — постмортем + правила написания CI

---

_Документ — стартовая точка. Перед каждой фазой создаётся sprint-issue с
конкретными exit-критериями и DoD. После завершения фазы — раздел в
`docs-toolkit/CHANGELOG.md` и апдейт `DEVELOPMENT_STATUS.md`._
