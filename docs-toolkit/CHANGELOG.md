# Changelog

Все важные изменения в `docs-toolkit` записываются в этот файл.

Формат: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
версионирование: [Semantic Versioning 2.0.0](https://semver.org/).

## [Unreleased]

### Added

**Phase II.1+II.2 — pipeline fix:** `_self_rag_run` now forwards every
RAGPipeline kwarg via a `pipeline_kwargs` dict, so `self_rag=True`
composes with `with_got`/`with_debate`/`with_negotiation`/`memory`/
`personality`. Presets `ask_with_reasoning` and `ask_full_stack` had
self-RAG restored. 7 contract tests in `tests/test_self_rag_composition.py`.

**Phase III — observability:** `TraceEvent(stage, t_ms, payload)` and
`AnswerResult.trace` (Phase III.1); `AnswerResult.to_trace_markdown()`
(Phase III.2); HTTP `/api/ask?trace=1` opt-in (Phase III.3). Every
pipeline stage emits an event with non-negative `t_ms`. 8 tests in
`tests/test_answer_result_trace.py`.

**Phase IV.1+IV.3 — performance:**
- negotiation agents: hoisted Bid import, pre-compiled regex,
  tokenise-query-once. `ask_with_negotiation` 141 → 118 μs (-16%).
- provenance claims: pre-compiled regex, pre-tokenised passages, removed
  O(M·N) re-tokenisation in `link_sources`.

**Phase V — Knowledge Graph deepening:**
- `docstoolkit.knowledge_graph.store.TripleStore` — SQLite-backed
  persistent triple store with indexed lookup by subject/predicate/
  object/doc_id, upsert with MAX(score), neighbours traversal. 13 tests
  in `tests/test_kg_store.py`.
- `docstoolkit.knowledge_graph.query` — mini DSL (`"py" uses ?topic`)
  with `parse_query()` / `run_query()`. Multi-pattern hash-join. 10 tests
  in `tests/test_kg_query.py`.
- New `kg` bench suite (4 benches: lookup, neighbors, 1-pattern,
  2-pattern). Measurements in `bench/BENCHMARKS.md`.

**Phase IX — docs:**
- `COOKBOOK.md` — 10 recipes by task
- `ARCHITECTURE.md` — layers, contracts, 5 ADRs
- `MIGRATING.md` — 1-to-1 mapping for LangChain/LlamaIndex users

### Fixed

- `bench/history.jsonl` baseline record committed so PR regression
  checks have something to diff against (Phase I.3).
- `docs/REGISTRY.md`, `docs/SCRIPTS_CATALOG.md`, `docs/TASKS_INDEX.md`
  re-generated to unblock PR #27 "Catalog up-to-date" CI gate.

## [0.3.0] - 2026-05-15

### Added — full roadmap coverage (Sprints 54-92)

**Path A** — production foundation:
- S6 per-user preferences: `apply_profile()` middleware,
  `ask(user_id=...)` integration
- S4 PageRank citation boost: `PageRankBoostedRetriever`
- S2 faceted search: `aggregate_facets()` + `apply_filters()`,
  `ask(filters=..., with_facets=...)`
- S7 read-receipts: auto-mark `read_docs` per `user_id` in `ask()`
- S3 doc classification: `classify_docs()` over `TfidfClassifier`
- S1 saved searches: `save_query()` + `run_due_alerts()` on `AlertStore`
- S5 bulk diff: `diff_corpus_dirs()` / `diff_commits()` / `diff_since_days()`
- M5 online eval: `OnlineEvalRunner` hook + HTML `render_dashboard()`
- M2 cross-encoder rerank: `ask(reranker=...)` over-fetches top_k*3
- M3 hierarchical: `ask(hierarchical=True)`
- M4 auto-intent routing: `ask(auto_intent=True)`
- M6 active learning: `ask(learning_queue=...)` auto-enqueue
- M7 incremental indexing: `incremental_index_docs()`
- M8 cross-modal assets: `search_assets()`

**Path B** — differentiation:
- I1 self-RAG: `ask(self_rag=True)` reflect loop
- I2 multi-agent debate: `ask(with_debate=True)`
- I3 provenance + CI: `ask(with_provenance=True)`
- I4 counterfactual probing: `probe_counterfactual()`
- I5 MemGPT memory: `ask(memory=TieredMemory(...))`
- I6 learned fusion: `FusedRetrieverAdapter`
- I7 bandit A/B: `ask_with_bandit(exp, variants)`
- I8 time-travel: `ask(at_commit="abc")`
- I9 prompt GA: `evolve_prompt()`
- I10 map-reduce: `ask(with_mapreduce=True)`

**Path C** — research bets:
- N1 metabolism: `propose_rewrite()` + `rank_stale_documents()`
- N2 negotiation: `ask(with_negotiation=True)` auction broker
- N3 graph-of-thoughts: `ask(with_got=True)`
- N4 epistemic voice: `measure_voice()`
- N5 federated eval: `federated_aggregate()` with Laplace noise
- N6 knowledge diffusion: `diffuse_knowledge()`
- N7 self-organising taxonomy: `build_taxonomy_ask()`
- N9 personality retrieval: `ask(personality=CognitiveProfile(...))`
- N10 adversarial co-evolution: `co_evolve_round()`

**HTTP server** (`docstoolkit serve`):
- `/api/ask` — RAG with all 17 ask() kwargs as query strings
- `/api/eval/dashboard` — HTML drift dashboard
- `/api/saved`, `/api/voice`, `/api/assets`, `/api/taxonomy`,
  `/api/diff`, `/api/kg`, `/api/profile` — per-feature JSON endpoints

**Tests:** 250+ new sprint-level tests; ~4800 related tests pass in ~26s
with no regressions. Roadmap coverage: 35 / 35 items (100%).

**Docs:** `PROFILES.md` (composition guide), `ROADMAP_EXECUTION.md`
(step-by-step plan for every roadmap item).

**Examples:** `examples/composition/01-08*.py` — eight self-contained runnable
demos covering baseline, personalization, quality, reasoning, advanced,
Path C, standalone helpers, and full-stack (all 17 features in one `ask()`).

**Benchmarks:** new `ask_features` and `helpers` suites in `bench.runner`
(10 + 3 benches over stubbed Retriever/Answerer to isolate per-feature
overhead). Results tracked in `bench/BENCHMARKS.md`; CI regression check
in `.github/workflows/benchmark.yml` now covers all suites.

**Presets:** `docstoolkit.rag.presets` — six named bundles of `ask()` kwargs
(`ask_personalized`, `ask_high_quality`, `ask_with_reasoning`, `ask_advanced`,
`ask_research`, `ask_full_stack`) so callers don't need to remember which
flags compose well. Each preset forwards extra kwargs, so any caller-supplied
flag still wins over the preset default.

## [0.2.0] - 2026-05-13

### Added
- Persistent SQLite кэш embeddings (`docstoolkit/embeddings/cache.py`)
  с TF-IDF IDF и vectors, content-hash cache invalidation
- CLI команды: `docstoolkit index build/update/clear/stats`
- Skill testing framework (`docstoolkit/skills/testing.py`)
  с golden tests формата `*.test.yaml`
- CLI команды: `docstoolkit skills list/test`
- Skills registry: discovery от `.claude/skills/` + entry_points плагинов

### Changed
- TFIDFProvider принимает опциональный `cache=` для persistent IDF
- `TestResult` dataclass получил `__test__ = False` для совместимости с pytest

### Performance
- TF-IDF.fit() с кэшем: 25x speedup на повторных вызовах
- Index build для 1194 документов: 1.4s (853 doc/sec)

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

[Unreleased]: https://github.com/svend4/lorenzo/compare/toolkit-v0.2.0...HEAD
[0.2.0]: https://github.com/svend4/lorenzo/compare/toolkit-v0.1.0...toolkit-v0.2.0
[0.1.0]: https://github.com/svend4/lorenzo/releases/tag/toolkit-v0.1.0
