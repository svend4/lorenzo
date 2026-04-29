# Changelog

Все важные изменения в `docs-toolkit` записываются в этот файл.

Формат: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
версионирование: [Semantic Versioning 2.0.0](https://semver.org/).

## [Unreleased]

Накоплено **17 спринтов** (Sprint 36-53) за период after 0.1.0. Готовится релиз 0.2.0.

### Added — RAG / Retrieval

- **Adaptive multi-hop retrieval** (`docstoolkit/rag/adaptive.py`, Sprint 53):
  confidence-driven query reformulation, dedup across hops, pluggable reformulator/confidence_fn
- **Streaming RAG** (`docstoolkit/rag/streaming.py`, Sprint 42):
  generator yields `passages_retrieved → token* → done | error` events;
  echo emulates chunked output, anthropic + openai do real SDK streaming
- SSE endpoint `POST /api/stream/rag` в `serve.py`

### Added — Agent / Reasoning

- **Plan-and-execute mode** (`docstoolkit/agent/planner.py`, Sprint 50):
  heuristic_planner (numbered/«потом»/«и» splits), execute_plan
  с dependency-aware prefix injection, optional replanner на failure

### Added — Workflow / Orchestration

- **Workflow DAG runner** (`docstoolkit/workflow/`, Sprint 47):
  topological sort + level-параллелизм через ThreadPool, on_error fail/skip/retry,
  cycle detection, `$.var` / `$.STEP.output` reference синтаксис
- **Model router** (`docstoolkit/router/`, Sprint 46):
  ModelChain с failover hops, retry+backoff, optional budget_check;
  built-in chains: cheap / fast / balanced / high-quality / echo-only

### Added — Eval / A/B / Feedback

- **A/B experiments framework** (`docstoolkit/experiments/`, Sprint 44):
  Experiment / VariantResult / ExperimentResult, markdown отчёт с Verdict
- **Eval / golden datasets** (`docstoolkit/eval/`, Sprint 48):
  GoldenItem (expected_answer_contains + expected_doc_ids + forbidden_phrases),
  P/R/F1 для citations + keyword score для answers, weighted overall
- **Feedback loop** (`docstoolkit/feedback/`, Sprint 43):
  SQLite store, Wilson confidence interval lower bound для quality scoring

### Added — Memory / Sessions

- **Conversation memory** (`docstoolkit/conversation/`, Sprint 49):
  SQLite sessions+messages, history_for_llm с tail-fit к token budget,
  squash_old с pluggable summarizer

### Added — Governance

- **Budget tracker** (`docstoolkit/budget/`, Sprint 45):
  per-scope LLM budget guards (day/week/month/total),
  warning/blocked states, top spenders + per-model breakdown analytics
- **Auth / RBAC** (`docstoolkit/auth/`, Sprint 39):
  scopes с wildcards, User/Scope dataclasses, check_scope
- **Versioned prompts с A/B variants** (`docstoolkit/prompts/`, Sprint 51):
  auto-extracted placeholders, fingerprint hash, weighted random pick
  (deterministic с rng_seed), JSON save/load

### Added — Observability

- **OpenTelemetry traces + Prometheus metrics** (`docstoolkit/telemetry/`, Sprint 41):
  StubTracer fallback if OTel SDK absent, prometheus_format() exposition
- `/metrics` endpoint в serve.py

### Added — Integration

- **Federation (NPP)** (`docstoolkit/federation/`, Sprint 36):
  Nautilus Portal Protocol, multi-node distributed queries, RRF merging
- **Event bus** (`docstoolkit/events/`, Sprint 37):
  pub-sub с pattern subscription, async dispatch
- **Multi-modal ingest** (`docstoolkit/ingest/multimodal.py`, Sprint 38):
  image / audio / video metadata extraction
- **Webhook dispatcher** (`docstoolkit/webhooks/`, Sprint 52):
  SQLite registry, HMAC-SHA256 signing, lifecycle pending→sent/failed→dead,
  retry_failed loop, pluggable http_send
- **VectorDB plugins** (`docstoolkit/vectordb/`, Sprint 40):
  abstract VectorDB interface, in-memory + sqlite-vec implementations
- **Time-travel queries** (`docstoolkit/timetravel/`, Sprint 41):
  git-based historical queries, query_at_commit, bisect_corpus

### Added — Tests

- 17 новых test файлов (test_streaming, test_feedback, test_experiments,
  test_budget, test_router, test_workflow, test_eval, test_conversation,
  test_planner, test_prompts, test_webhooks, test_adaptive,
  test_federation, test_events, test_multimodal, test_auth, test_vectordb,
  test_telemetry, test_timetravel)
- **Total: 546 тестов passed** (vs 96 в 0.1.0)

### Performance

- Workflow async: 3×30ms steps в 51ms (parallel) vs 90ms (sync)
- Webhook delivery: <100ms p99 (mock HTTP)
- Adaptive search: ≤max_hops × retriever_latency

### Documentation

- ROADMAP series: `docs/ROADMAP/` с 35 идей развития (4 уровня сложности)
- README.md перегенерирован, отражает 30+ модулей
- CONTRIBUTING.md обновлён со структурой проекта

## [0.1.0] - 2026-04-29

### Added
- Базовое ядро: `Config`, `load_config`, `write_doc`, `extract_frontmatter`, `parse_yaml`
- CLI команды: `init`, `doc new/validate/list-templates`, `ingest`, `serve`, `doctor`,
  `search`, `plugins list/inspect`
- Embeddings провайдеры: `TFIDFProvider`, `SentenceTransformersProvider` (опц.)
- HybridSearcher с RRF и weighted-fusion
- 7 ingest плагинов: markdown, html, mhtml, jupyter (stdlib);
  pdf (pypdf), epub (ebooklib), docx (python-docx) — опциональные
- Web ingest: url, arxiv, hackernews, habr (всё на stdlib)
- Plugin system через PEP 621 entry_points (6 групп)
- Multi-language: detect, i18n (RU+EN, 10 ключей), readability (Flesch-Kincaid)
- Doctor: 8 типов проверок системы
- Встроенный HTTP dashboard (`serve`) на stdlib
- Dockerfile (multi-stage), GitHub Action template, PyPI publish workflow
- Example plugin pack с 4 типами расширений

[Unreleased]: https://github.com/svend4/lorenzo/compare/toolkit-v0.1.0...HEAD
[0.1.0]: https://github.com/svend4/lorenzo/releases/tag/toolkit-v0.1.0
