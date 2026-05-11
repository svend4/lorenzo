---
title: "Changelog (авто)"
tags:
  - general
date: 2026-05-11
---

# Changelog (авто)

<!-- toc-auto -->

> [!NOTE]
> Раздел `CHANGELOG_AUTO` формируется автоматически из данных репозитория.

<!-- alert-added -->
<!-- tags: changelog-auto, docs -->


<!-- summary -->
> `CHANGELOG_AUTO` — раздел документации проекта Lorenzo.


_Сгенерировано из 200 коммитов git-истории._

## Статистика коммитов

| Тип | Название | Кол-во |
|-----|---------|--------|
| `feat` | ✨ Новые возможности | 63 |
| `fix` | 🐛 Исправления | 33 |
| `docs` | 📝 Документация | 21 |
| `chore` | 🔧 Технические задачи | 64 |
| `test` | ✅ Тесты | 10 |
| `other` | 📌 Прочее | 9 |

## История изменений


### 2026-05

**✨ Новые возможности**

- POST /api/search — лёгкий поиск без LLM-синтеза + тесты `63e1280e`
- PROGRESS.md 7/11 → 8/11 — MVP опубликован (git tag v1.0.0) `657ca79e`
- /api/status — core_cards фильтрация noise-секций `0bf15429`
- Hit Rate@10 0.750 → 1.000 — улучшение качества поиска `b5efba6c`
- POST /api/collabs endpoint + tests/test_search.py (16 тестов) `39796fb2`
- GET /api/benchmark endpoint + ускорение тестов `20c60b4c`
- автодетектирование milestone прототипа и тестирования в PROGRESS.md `82c7db84`
- автоматизация всех критериев benchmark в prototype_demo.py `e77ffcb8`
- улучшение качества поиска + CI fix для gateway/ANN тестов `b9d3e3b8`
- тесты gateway/ANN + Precision Eval (Hit Rate@10=0.75) + PROGRESS 63% `f3d00e22`
- hnswlib ANN-граф — ускоренный векторный поиск 37× (Итерация 1 завершена) `bd974316`
- Review Queue UI + gateway write-back fix + Iteration 4 `e31c908a`
- Lorenzo Gateway — OpenAI-compatible HTTP API для обогащения корпуса `f754e78b`
- working prototype Knowledge OS — prototype_demo.py `645d38b5`
- protect PROGRESS.md manual sections + update search/deeptext `deef911d`
- SENTINEL security check + contact statuses + progress 55% `62b5e192`
- add open letter drafts for 8 project authors `c601257d`
- add improve_quality_patch.py to prevent score regression after pipeline runs `81af4bf5`
- raise doc quality score from 96.3 → 100.0/100 with 0 broken links `cf9ebcce`
- improve doc quality score from 84.6 → 86.5/100 `82d3705e`
- quality metrics 83.5→84.6/100, fix duplicate TOCs, add 680 callouts `88511476`
- quality metrics 82.3→83.5/100, callout coverage 35%→95% `043b81e0`
- quality metrics 76.7→82.3/100, add callouts/TOCs/H1s/summaries `bd8d60bd`
- improve quality metrics 73.2→76.7, fix has_toc detection `858494ca`
- health 94→99/100, exclude mirror dirs from quality checks `09ae9873`
- add cross-links between project files to build knowledge graph edges `6b86d7ae`
- complete project coverage — Rufler, LiteParse; fix semantic search dedup `5412f874`
- add mclaude project file, update README indexes, rebuild passages.json `7f4b06b2`
- add rich project files for agent-memory-mcp, AgentFS, knowledge-space `69eecd21`
- enrich card payload with body field for better BM25 and TF-IDF coverage `fe2c28e1`
- unified semantic search, better card types, collab_finder quality `27640884`
- improve collab_finder quality and TF-IDF index `9e1f8eed`
- Collaboration Finder + TF-IDF semantic index + GitHub Actions schedule `e4e61656`
- incremental CardStore, better type detection, recipe --since, fix OSError `96e0eab4`
- card envelope library, card index CLI, fix recipe dry-run + history `95929faf`
- implement E-K roadmap items — recipe system, BM25 MCP, prototype spec, code generator `9b4e71ac`
- implement improve_self.py --batch and add REPL search script `f069f299`
- (scripts) complete run_all coverage + --dry-run for all red scripts `cdb6ccce`
- document all 156 scripts, fix risk algorithm, update methodology `a5de89d7`
- (scripts) add --dry-run to all 4 content-modifying scripts `fe718881`
- метаскрипт improve_self.py + документация docs/meta-scripting/ `1a1f0520`

**🐛 Исправления**

- валидация шаблонов — 12 файлов с frontmatter ошибками `785f998a`
- stabilize quality score 100/100 + 0 broken links `7741b0dd`
- restore 100.0/100 and 0 broken links after second pipeline run `728700c0`
- restore 100.0/100 quality score and 0 broken links after pipeline run `c02dda87`
- restore 100.0/100 quality score and 0 broken links after pipeline run `447e84d3`
- remove 61 broken internal links (dangling #contents anchors + SEARCH.md paths) `a469b340`
- eliminate last 5 broken links, add 300+ TOCs and quality enrichments `7eb5fa87`
- eliminate all broken links, health score 99→100/100 `d4c3c287`
- health 91→94, fix MISSING.md emoji counting in improve_health.py `be5892e3`
- reduce broken links 512→209, health 89→91 `38e7dec4`
- reduce broken links 779→512, health 87→89 `f720e48b`
- generate relative links in COLLAB_SUGGESTIONS.md `32d55e7b`
- fill missing status sections in 3 project files + autofill path fix `43c99b25`
- improve_autofill.py generates relative contact paths + rebuild indexes `c44e306c`
- autofill status sections placed after YAML frontmatter + sync PROGRESS `4d7b3b41`
- processing-guide contact path + MVP link, update BROKEN_LINKS `421206a7`
- further reduce broken links — nautilus nested brackets + TABLES.md paths `cb9acdb6`
- bulk resolve 9742 broken internal links across docs/ `6c550366`
- auto-generated link sections now use relative paths (not root-relative) `62d0d354`
- resolve all 66 broken internal links in docs/05-habr-projects/ `d8cc81a0`
- correct relative paths for contact links in 05-habr-projects `c3019d35`
- Russian инструментальный падеж в stemmer + rebuild indexes `9e8247a5`
- semantic search — stub dedup + Russian suffix stemming + type-aware hybrid `6c6f9f25`
- card type detection — templates, section dirs, numeric prefix in meta names `bf29e8f6`
- card type detection — analysis dirs, H1 prefix guard, Russian plural проектов `90a387e1`
- card summary extraction, deduplication, contact matching quality `e93b9b94`

**📝 Документация**

- обновление README.md и GATEWAY.md `f5ebc628`
- обновлён README.md для публикации MVP `049d3303`
- update CLAUDE.md to reflect current system state `80dba2ab`
- add SCRIPT_EVAL_REPORT.md — live test results, before/after, analysis `75e2e913`

**🔧 Технические задачи**

- regenerate auto-generated docs artifacts `02c362fe`
- regenerate auto-generated docs artifacts `7e4ee06b`
- regenerate auto-generated docs artifacts `0623cb16`
- regenerate all auto-generated docs artifacts after smart pipeline run `7ff328ed`
- update auto-generated docs artifacts `4a6e7a87`
- обновление COMPLEXITY.md и SENTIMENT.md `779808d5`
- обновление CONCEPTS.md и ENTITIES.md `a5b93b95`
- обновление QUESTIONS.md `56694311`
- обновление ACTION_ITEMS.md и DECISIONS.md `04a47cc0`
- обновление DENSITY.md и HEATMAP.md `619729e1`
- авто-обновление docs/ после improve_run_all --smart `4489b806`
- обновление зеркальных файлов obsidian/confluence `07739d9c`
- авто-перегенерация дашбордов после v1.0.0 + check_published `8e032586`
- авто-перегенерация дашбордов после Hit Rate@10 1.000 `9cb118ab`
- обновление каталогов после gateway.py + тестов `7ffc3e02`
- авто-перегенерация зеркал obsidian/ confluence/ и индексов `80bb9e42`
- авто-перегенерация дашбордов после fix template validation `b9d16368`
- авто-перегенерация дашбордов после обновления search_index.json `ba60a3ce`
- обновление каталогов скриптов и реестра артефактов `6d6ef3d7`
- авто-перегенерация derived-файлов после rebuild search_index.json `4b5b08cb`
- обновление авто-генерируемых дашбордов после новых файлов `48553442`
- update SCORING.md auto-generated dashboard `2655a8cb`
- linter adjustments to letters and DEMO.md `dc3c1dfc`
- update auto-generated dashboards `defa92c5`
- update auto-generated docs after reports pipeline run `f5d46f4c`
- update generated docs after reports pipeline run `089b157f`
- add docs/bad_links.json (broken link skip-list, 25 long paths) `c70da065`
- update SCORING.md and BROKEN_LINKS.md after link fixes `f149cf4b`
- update recipe_history.json after card-index dry-run `c6b29dac`
- update BROKEN_LINKS.md after broken_links fix `16d1f6b3`
- update reports group outputs after background run `bc4135dd`
- update generated docs and scripts after evaluation session `d5b430f6`
- update generated docs — auto-enrichment, TOC, summaries, meta-scripting `696550ff`
- update generated indexes and dashboards `3ac7b575`
- отключить автоматические коммиты бота, добавить METHODOLOGY.md `40e69e77`

**✅ Тесты**

- add 74 tests for improve_contact_status, improve_kpi_snapshot, improve_complexity `351a135d`
- add 95 tests for improve_export_csv, improve_scoring, improve_workflow_run `2b05200b`
- add 52 tests for improve_watcher, improve_self, improve_card_index `e734762d`
- add 95 tests for improve_llm_qa, improve_abstract, improve_benchmark `a345c19d`
- +54 теста — test_status_badges.py + test_autofill.py; итого 394 `cda0f08a`
- +54 теста — test_metrics.py + test_migrate_contacts.py; итого 340 `c34d758c`
- +51 тест — test_embedding_index.py + test_badges.py; итого 286 `3c00c354`
- +27 тестов — test_passage_retrieval.py; итого 235 тестов `a833ea0b`
- +25 тестов — test_index_update.py; обновление docs/ и README.md `0515207f`
- +44 теста — test_progress_sync.py + test_semantic_search.py `b3b6c5db`

**📌 Прочее**

- 05-habr-projects 65→72/100 — 100% summary+tags coverage `e8cc1b60`
- восстановить контент обеднённый ботом — preview-строки, похожие документы, footnotes `daf0d7f2`


### 2026-04

**✨ Новые возможности**

- Sprint 51-53 — prompt library, webhooks, adaptive retrieval `4d415860`
- Sprint 48-50 — eval framework, conversation memory, plan-and-execute `707d1d26`
- Sprint 45-47 — budget guards, model router, workflow DAG `5b15d5f6`
- Sprint 42-44 — streaming RAG, feedback loop, A/B experiments `2a7a98b3`
- Sprint 39-41 — auth/RBAC, vector DB plugins, OpenTelemetry `dccdd498`
- Sprint 36-38 — federation, event bus, multi-modal ingest `6313b6a7`
- Sprint 33-35 — agent loop, cloud ingest, time-travel queries `be1b6b9b`
- Sprint 30-32 — interactive web UI, SSE streaming, benchmark suite `965bc0d7`
- Sprint 27-29 — Multi-LLM, concept clustering, docs portal `00ff4e11`
- Sprint 24-26 — RAG pipeline, jobs queue, knowledge graph `d3dd0884`
- Sprint 21-23 — embeddings cache, skill testing, release engineering `11d7bad1`
- Sprint 18-20 — MCP-изация новых слоёв, plugin system, web ingest `89f9dc93`
- Sprint 15-17 — workflow v2, observability, embeddings, i18n `2265a4db`
- Sprint 12-14 — bot-aware exclusions, distribution, web dashboard `1bf14810`
- Sprint 9-11 — skills MCP server, ingestion plugins, CI/CD `22c4cf8d`
- Sprint 6-8 — миграции, мета-скилы, workflow-runner, registry, docs-toolkit vendoring `589fe47e`
- 5-sprint roadmap — templates, skills, plugins + manifest engine `81644487`
- 3 новых скрипта — cross_section, digest_auto, export_report `cd90a751`
- применить auto-linker + gap-filler ко всей базе знаний `ef99f46a`
- improve_reading_list.py — BM25-список чтения по теме `19398486`
- ещё 3 скрипта + применить TOC/абстракты ко всей базе знаний `a8455926`
- run all script groups, apply TOC/abstracts/crosslinks, rebuild search index `898c42a0`

**🐛 Исправления**

- docs-check workflow — добавить deps + continue-on-error `c11825ce`
- regenerate catalogs (Catalog up-to-date check) `8ac2cdaa`
- CI Catalog check — improve_auto_toc respects .docignore `d6279595`
- восстановить 24 файла повреждённых GitHub Actions ботом `643d52de`
- остановить деструктивные авто-обновления от GitHub Actions бота `ee0b767e`
- fix crosslink root cause (relative paths), map all 125 scripts in dependency map `ed3fa81f`
- fix 8607 broken internal links, improve health score formula `52179ba5`

**📝 Документация**

- auto-update metrics [skip ci] `d4da2426`
- add 10-part processing guide with combined master document `c4b470af`
- auto-update metrics [skip ci] `bf2aa845`
- auto-update via improve_run_all [skip ci] `c3a31450`
- auto-update via improve_run_all [skip ci] `b0ed2c15`
- auto-update via improve_run_all [skip ci] `0f740af3`
- auto-update via improve_run_all [skip ci] `88a8480c`
- auto-update via improve_run_all [skip ci] `6f3be4a7`
- auto-update via improve_run_all [skip ci] `0c696915`
- auto-update via improve_run_all [skip ci] `519d41b5`
- auto-update via improve_run_all [skip ci] `fdd84b5b`
- auto-update metrics [skip ci] `d8c1da19`
- auto-update metrics [skip ci] `94be1ad1`
- auto-update via improve_run_all [skip ci] `ba78ff20`
- auto-update via improve_run_all [skip ci] `f63f1a9f`
- auto-update via improve_run_all [skip ci] `039a4a2a`
- auto-update via improve_run_all [skip ci] `dfc530a0`

**🔧 Технические задачи**

- regenerate auto-feeds after Sprint 51-53 `ba2fcac1`
- regenerate auto-feeds after Sprint 48-50 `dedfe11d`
- regenerate auto-feeds after Sprint 45-47 `74b242b5`
- regenerate auto-feeds after Sprint 42-44 `7d1a69d2`
- sync auto-generated docs after status report run `2ed1bf01`
- regenerate auto-feeds after Sprint 39-41 `d445ffb3`
- regenerate auto-feeds after Sprint 36-38 `6efb6b90`
- regenerate auto-feeds after Sprint 33-35 `65941440`
- regenerate confluence/obsidian REPORT exports `2b1e57d2`
- regenerate auto-exports after Sprint 30-32 `e0233b26`
- regenerate auto-exports after Sprint 27-29 `40f1222e`
- regenerate SPELLCHECK.md `471565f1`
- regenerate READABILITY.md after merge `4bdf6b83`
- regenerate exports/indexes after merge with main `b9521c3d`
- regenerate auto-exports after Sprint 24-26 `6421a1fc`
- regenerate auto-exports after Sprint 21-23 `6ac59707`
- regenerate auto-exports after Sprint 18-20 `f053125f`
- extend gitignore + regenerate badges/exports after Sprint 15-17 `3ca737f2`
- regenerate badges + auto-exports after Sprint 12-14 `25de4e63`
- regenerate export artifacts (REPORT, CSV, RSS, Atom, HTML) `b471bbad`
- ignore auto-generated exports and runtime caches `41a9c8aa`
- regenerate VALIDATION.md after rebase `093bb8c8`
- sync PROGRESS.md `78e6481d`
- sync PROGRESS.md `d4d34b4a`
- sync PROGRESS.md `2a9e9403`
- sync PROGRESS.md `fc65bef5`
- refresh executive report `12dea45c`
- синхронизировать сгенерированные отчёты и docs `64358a84`
- sync PROGRESS.md after content scripts commit `afe64e18`

**📌 Прочее**

- Merge remote-tracking branch 'origin/main' into claude/organize-monorepo-docs-VmctA `741edf95`
- Audit-driven extraction of major missing substantive content `fedc045a`
- Extract Nautilus Portal Protocol v1.0.0-draft (earlier version) `c6592525`
- Extract Nautilus-vs-CAMEL analysis and Habr extra-examples `ee71737e`
- Extract Hermes Agent comparison and re-prioritization `7822b130`
- Extract AI-managed virtual company and MMORPG-for-programmers analyses `e965e1cd`
- Extract Anthropic outreach concept, collaborator findings, reading paths `088f3f16`

---

_Changelog генерируется автоматически из conventional commits._

_Ручной changelog: `docs/CHANGELOG.md` (если существует)._



## Использование
```bash
# Запуск
python scripts/improve_changelog_auto.py
```

## Смотрите также
- [[README|Главная]]
- [[METRICS|Метрики]]
- [[HEALTH|Здоровье]]
- [[GLOSSARY|Глоссарий]]
- [[ENTITIES|Сущности]]
- [[DECISIONS|Решения]]
