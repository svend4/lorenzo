# Changelog

Все важные изменения в `docs-toolkit` записываются в этот файл.

Формат: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
версионирование: [Semantic Versioning 2.0.0](https://semver.org/).

## [Unreleased]

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
