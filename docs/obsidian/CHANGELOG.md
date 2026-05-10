---
title: "CHANGELOG"
tags:
  - general
date: 2026-05-10
---

# CHANGELOG

<!-- toc-auto -->
## Contents

- [semantic (1 коммитов)](#semantic-1-коммитов)
  - [🔧 Обслуживание](#обслуживание)
- [md (1 коммитов)](#md-1-коммитов)
  - [🔧 Обслуживание](#обслуживание-1)
- [2026-05-10 (11 коммитов)](#2026-05-10-11-коммитов)
  - [🔧 Обслуживание](#обслуживание-2)
  - [✨ Новые функции](#новые-функции)
- [2026-04-29 (141 коммитов)](#2026-04-29-141-коммитов)
  - [🔧 Обслуживание](#обслуживание-3)
  - [📝 Документация](#документация)
  - [✨ Новые функции](#новые-функции-1)
  - [🐛 Исправления](#исправления)
  - [⚡ Улучшения](#улучшения)
- [skip  (1 коммитов)](#skip-1-коммитов)
  - [🔧 Обслуживание](#обслуживание-4)
- [22 скила  (1 коммитов)](#22-скила-1-коммитов)
  - [🔧 Обслуживание](#обслуживание-5)
- [$.STEP.ou (1 коммитов)](#stepou-1-коммитов)
  - [🔧 Обслуживание](#обслуживание-6)
- [(1 коммитов)](#1-коммитов)
  - [🔧 Обслуживание](#обслуживание-7)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> Статистика: 🔧 chore: 66 | ✨ feat: 47 | 📝 docs: 21 | ⚡ improve: 14 | 🐛 fix: 10
**Проекты:** Svyazi

---
<!-- tags: rag, orchestration, ingestion, architecture, roadmap, anthropic, self-improve, collaboration -->




Всего коммитов: **158**  
Статистика: 🔧 chore: 66 | ✨ feat: 47 | 📝 docs: 21 | ⚡ improve: 14 | 🐛 fix: 10


## semantic (1 коммитов)

### 🔧 Обслуживание

- hybrid _  E4. cm_

## md (1 коммитов)

### 🔧 Обслуживание

- csv: bulk export _  --expo_

## 2026-05-10 (11 коммитов)

### 🔧 Обслуживание

- update generated docs — auto-enrichment, TOC, summaries, meta-scripting _696550ff_
  > Scripts ran during session added summaries, TOC, abstract blocks, and
- update generated indexes and dashboards _3ac7b575_
  > Re-run improve_health.py (84/100), improve_metrics.py (69.6/100),
- restore: восстановить контент обеднённый ботом — preview-строки, похожие документы, footnotes _daf0d7f2_
  > Бот заменял живые превью содержимого (первые предложения файлов) на HTML-заглушки
- отключить автоматические коммиты бота, добавить METHODOLOGY.md _40e69e77_
### ✨ Новые функции

- card envelope library, card index CLI, fix recipe dry-run + history _95929faf_
  > utils_card_envelope.py — 5 data contracts from PROTOTYPE_SPEC.md:
- implement E-K roadmap items — recipe system, BM25 MCP, prototype spec, code generator _9b4e71ac_
  > F: improve_recipe.py — 20 built-in recipes (quality-check, morning-run, full-index,
- implement improve_self.py --batch and add REPL search script _f069f299_
  > - improve_self.py: add --batch flag for bulk script enrichment (docstring + main block)
- complete run_all coverage + --dry-run for all red scripts _cdb6ccce_
  > A) improve_run_all.py:
- document all 156 scripts, fix risk algorithm, update methodology _a5de89d7_
  > Priority 2: Added all 85 previously undocumented scripts to CLAUDE.md
- add --dry-run to all 4 content-modifying scripts _fe718881_
  > improve_alerts.py, improve_footnotes.py, improve_reading_list.py,
- метаскрипт improve_self.py + документация docs/meta-scripting/ _1a1f0520_
  > improve_self.py — скрипт четвёртого порядка: читает другие скрипты через AST,

## 2026-04-29 (141 коммитов)

### 🔧 Обслуживание

- Merge remote-tracking branch 'origin/main' into claude/organize-monorepo-docs-VmctA _741edf95_
- regenerate auto-feeds after Sprint 51-53 _ba2fcac1_
  > https://claude.ai/code/session_01Dz4rhQWcqu2afRsJ5LqHpz
- regenerate auto-feeds after Sprint 48-50 _dedfe11d_
  > https://claude.ai/code/session_01Dz4rhQWcqu2afRsJ5LqHpz
- regenerate auto-feeds after Sprint 45-47 _74b242b5_
  > https://claude.ai/code/session_01Dz4rhQWcqu2afRsJ5LqHpz
- regenerate auto-feeds after Sprint 42-44 _7d1a69d2_
  > https://claude.ai/code/session_01Dz4rhQWcqu2afRsJ5LqHpz
- sync auto-generated docs after status report run _2ed1bf01_
  > Reports, metrics, indexes and contact files updated by benchmark
- regenerate auto-feeds after Sprint 39-41 _d445ffb3_
- regenerate auto-feeds after Sprint 36-38 _6efb6b90_
- regenerate auto-feeds after Sprint 33-35 _65941440_
- regenerate confluence/obsidian REPORT exports _2b1e57d2_
- regenerate auto-exports after Sprint 30-32 _e0233b26_
- regenerate auto-exports after Sprint 27-29 _40f1222e_
- regenerate SPELLCHECK.md _471565f1_
- regenerate READABILITY.md after merge _4bdf6b83_
- regenerate exports/indexes after merge with main _b9521c3d_
- regenerate auto-exports after Sprint 24-26 _6421a1fc_
- regenerate auto-exports after Sprint 21-23 _6ac59707_
- regenerate auto-exports after Sprint 18-20 _f053125f_
- extend gitignore + regenerate badges/exports after Sprint 15-17 _3ca737f2_
- regenerate badges + auto-exports after Sprint 12-14 _25de4e63_
- regenerate export artifacts (REPORT, CSV, RSS, Atom, HTML) _b471bbad_
- ignore auto-generated exports and runtime caches _41a9c8aa_
- regenerate VALIDATION.md after rebase _093bb8c8_
- sync PROGRESS.md _78e6481d_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
- sync PROGRESS.md _d4d34b4a_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
- sync PROGRESS.md _2a9e9403_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
- sync PROGRESS.md _fc65bef5_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
- Audit-driven extraction of major missing substantive content _fedc045a_
  > After audit of source dialogs against extracted content, 12 major
- refresh executive report _12dea45c_
  > https://claude.ai/code/session_0179jSZDgmKgh9eLH72HRLuv
- синхронизировать сгенерированные отчёты и docs _64358a84_
  > Обновление всех авто-генерируемых файлов после запуска
- Extract Nautilus Portal Protocol v1.0.0-draft (earlier version) _c6592525_
  > docs/nautilus/npp-v1-0/ (NEW, 20 files):
- Extract Nautilus-vs-CAMEL analysis and Habr extra-examples _ee71737e_
  > docs/anthropic-vacancies/nautilus-vs-camel/ (NEW, 7 files):
- Extract Hermes Agent comparison and re-prioritization _7822b130_
  > docs/anthropic-vacancies/hermes-comparison/ (NEW, 15 files):
- sync PROGRESS.md after content scripts commit _afe64e18_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
- Extract AI-managed virtual company and MMORPG-for-programmers analyses _e965e1cd_
  > docs/anthropic-vacancies/ai-managed-virtual-company/ (NEW, 12 files):
- Extract Anthropic outreach concept, collaborator findings, reading paths _088f3f16_
  > docs/anthropic-vacancies/beneficial-deployments-concept/ (NEW, 13 files):
- Extract Lorenzo specification questions and phased deployment _9d9d2fee_
  > The same anthropic-vacancies dialog contained more substantive
- Extract Three-Phase Review Methodology and operationalized Lorenzo _047d6c06_
  > docs/nautilus/review-methodology/ (NEW):
- Extract Lorenzo agent prompt and 4 more DHLab papers _5a34f469_
  > The same MHTML dialog (anthropic-vacancies) contained even more
- sync PROGRESS.md after nlpplus scripts commit _78f4f118_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
- Extract Nautilus Portal Protocol RFC and companion papers _cbe83e6e_
  > The anthropic-vacancies dialog drifted into substantial Nautilus
- Add profile-mapping, glossary, source-projects index _b552bcfc_
  > docs/anthropic-vacancies/profile-mapping/:
- sync CONTRADICTIONS.md (background task output) _89d3e8fb_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
- sync CONTRADICTIONS.md after contradiction_check fix _6b81ffed_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
- update mcp.json description wording _4e52a185_
  > https://claude.ai/code/session_0179jSZDgmKgh9eLH72HRLuv
- sync PROGRESS.md after deeptext scripts commit _1d552d4e_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
- Extract MHTML content into topic docs _4b567b23_
  > Continuation of the monorepo split: parsed each MHTML snapshot and
- sync PROGRESS.md after session _53bfdbd8_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
- sync generated docs (CONTACTS, HEALTH, METRICS) _5571b369_
  > Auto-updated by improve_* scripts during session.
- add CLAUDE.md, requirements.txt, .claude/settings.json _cfdcd4e8_
  > CLAUDE.md: project context loaded automatically by Claude Code each session
- commit README.md with SVG badges from batch 13 _be9de469_
  > https://claude.ai/code/session_0179jSZDgmKgh9eLH72HRLuv
- add .gitignore for Python cache files _7658df5b_
  > https://claude.ai/code/session_0179jSZDgmKgh9eLH72HRLuv
- add extract_mhtml.py and ignore pycache _ff8a8161_
  > https://claude.ai/code/session_0179jSZDgmKgh9eLH72HRLuv
- Organize repo as monorepo with topic-split docs _d5ddac56_
  > - Make repo a monorepo (package.json workspaces, pnpm-workspace.yaml,
- Add files via upload _183c4e9f_
- Initial commit _6c49dba6_
### 📝 Документация

- auto-update metrics [skip ci] _d4da2426_
- add 10-part processing guide with combined master document _c4b470af_
  > Complete guide to processing large document collections, covering:
- auto-update metrics [skip ci] _bf2aa845_
- auto-update via improve_run_all [skip ci] _c3a31450_
- auto-update via improve_run_all [skip ci] _b0ed2c15_
- auto-update via improve_run_all [skip ci] _0f740af3_
- auto-update via improve_run_all [skip ci] _88a8480c_
- auto-update via improve_run_all [skip ci] _6f3be4a7_
- auto-update via improve_run_all [skip ci] _0c696915_
- auto-update via improve_run_all [skip ci] _519d41b5_
- auto-update via improve_run_all [skip ci] _fdd84b5b_
- auto-update metrics [skip ci] _d8c1da19_
- auto-update metrics [skip ci] _94be1ad1_
- auto-update via improve_run_all [skip ci] _ba78ff20_
- auto-update via improve_run_all [skip ci] _f63f1a9f_
- auto-update via improve_run_all [skip ci] _039a4a2a_
- auto-update via improve_run_all [skip ci] _dfc530a0_
- auto-update via improve_run_all [skip ci] _f73c58f7_
- auto-update via improve_run_all [skip ci] _8e689b3d_
- sync PROGRESS.md _4e217f2b_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
- sync PROGRESS.md after adding 16 new scripts _4d237951_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
### ✨ Новые функции

- Sprint 51-53 — prompt library, webhooks, adaptive retrieval _4d415860_
  > Sprint 51: Prompt library (`docstoolkit/prompts/`)
- Sprint 48-50 — eval framework, conversation memory, plan-and-execute _707d1d26_
  > Sprint 48: Eval / golden dataset (`docstoolkit/eval/`)
- Sprint 45-47 — budget guards, model router, workflow DAG _5b15d5f6_
  > Sprint 45: Budget tracker (`docstoolkit/budget/`)
- Sprint 42-44 — streaming RAG, feedback loop, A/B experiments _2a7a98b3_
  > Sprint 42: Streaming RAG (`docstoolkit/rag/streaming.py`)
- Sprint 39-41 — auth/RBAC, vector DB plugins, OpenTelemetry _dccdd498_
  > Sprint 39 — Authentication + RBAC
- Sprint 36-38 — federation, event bus, multi-modal ingest _6313b6a7_
  > Sprint 36 — Federation (NPP Nautilus Portal Protocol)
- Sprint 33-35 — agent loop, cloud ingest, time-travel queries _be1b6b9b_
  > Sprint 33 — Autonomous Agent loop
- Sprint 30-32 — interactive web UI, SSE streaming, benchmark suite _965bc0d7_
  > Sprint 30 — Interactive web UI
- Sprint 27-29 — Multi-LLM, concept clustering, docs portal _00ff4e11_
  > Sprint 27 — Multi-LLM providers
- Sprint 24-26 — RAG pipeline, jobs queue, knowledge graph _d3dd0884_
  > Sprint 24 — RAG end-to-end
- Sprint 21-23 — embeddings cache, skill testing, release engineering _11d7bad1_
  > Sprint 21 — Persistent embeddings cache
- Sprint 18-20 — MCP-изация новых слоёв, plugin system, web ingest _89f9dc93_
  > Sprint 18 — MCP-изация
- Sprint 15-17 — workflow v2, observability, embeddings, i18n _2265a4db_
  > Sprint 15 — workflow & observability
- Sprint 12-14 — bot-aware exclusions, distribution, web dashboard _1bf14810_
  > Sprint 12 — bot-aware system
- Sprint 9-11 — skills MCP server, ingestion plugins, CI/CD _22c4cf8d_
  > Sprint 9 — agentic skills layer
- Sprint 6-8 — миграции, мета-скилы, workflow-runner, registry, docs-toolkit vendoring _589fe47e_
  > Sprint 6 — операционализация
- 5-sprint roadmap — templates, skills, plugins + manifest engine _81644487_
  > Sprint 1 (T1+S1+P1): универсальный слой
- 3 новых скрипта — cross_section, digest_auto, export_report _cd90a751_
  > improve_cross_section.py (группа analytics):
- применить auto-linker + gap-filler ко всей базе знаний _ef99f46a_
  > Практические улучшения контента:
- improve_reading_list.py — BM25-список чтения по теме _19398486_
  > Новый скрипт для создания персонализированных списков чтения:
- ещё 3 скрипта + применить TOC/абстракты ко всей базе знаний _a8455926_
  > Новые скрипты (группа content + nlpplus):
- run all script groups, apply TOC/abstracts/crosslinks, rebuild search index _898c42a0_
  > - All 7 script groups pass clean (quality, analytics, deeptext, meta, textwork, reports, generate)
- add component matrix, KPI history tracker, fix run_all coverage _69562b02_
  > - improve_component_matrix.py: 14×10 compatibility matrix (memory/search/
- добавить 8 скриптов группы nlpplus — расширенный NLP-анализ _4bcc9739_
  > Новые скрипты:
- add risk register, auto-changelog, master index; fix run_all missing scripts _59617c5d_
  > - improve_risk_register.py: 10 curated risks + 15 extracted from docs,
- add tech radar, onboarding guide, dependency map, meta group in run_all _4ddee95e_
  > - improve_tech_radar.py: 22 tech positions across ADOPT/TRIAL/ASSESS/HOLD
- add autonomous watcher (Ступень 6), CI workflow, LLM section summaries _1f3fe74a_
  > Ступень 6 — improve_watcher.py:
- add CLAUDE.md, weekly digest script, enrich group in run_all _469dbced_
  > - CLAUDE.md: project guide for Claude — structure, key docs, all 5 tiers,
- add LLM integration (Ступень 3), skills (Ступень 4), MCP server (Ступень 5) _00a25f78_
  > Ступень 3 — Claude API scripts:
- добавить 12 скриптов глубокой обработки текста (группа deeptext) _6cbd49c7_
  > Batch 1 — структура и навигация:
- add 9 text-processing scripts (textwork group) for large-scale knowledge management _bfe2bdda_
  > New scripts in group textwork (92 total, 12 groups):
- add 16 new improve_* scripts across quality/export/cicd/analytics groups _f8464fe2_
  > Quality/validation:
- 13 улучшений — search fix, parallel/report/only, watch, priority, bulk, coverage, staleness, autofix, qa history, llm contact, benchmark _3d29c06c_
  > Инфраструктура:
- 4 улучшения — кэш QA, --save, dedup с текстом дублей, --only, MCP contact status _77613be2_
  > improve_llm_qa.py:
- 4 улучшения — contact_status CLI, --changed флаг, нормализация поискового индекса, post-commit хук _58003258_
  > - improve_contact_status.py: CLI для обновления статуса контактов без редактирования файла
- add improve skill — universal improvement workflow for Lorenzo _6e576a81_
  > .claude/skills/improve.md — 370 lines, 6 decision branches:
- implement 3 improvements + fix question truncation _a32f556b_
  > 1. improve_llm_enrich.py — add --file and --force flags
- implement stages 0-5 of the script→skill→plugin hierarchy _612e585b_
  > Stage 0 — utils_chunker.py: chunking utilities for large texts
- add improve_autofill.py — fills templates from existing script outputs _d946c3b3_
  > - Creates docs/contacts/ with 14 contact-outreach.md files (one per author)
- organize docs into monorepo structure with topic-based subfolders _d49a1f0f_
  > - Split 4 deep-research-report .md files into 14 focused docs in docs/01-svyazi/
### 🐛 Исправления

- docs-check workflow — добавить deps + continue-on-error _c11825ce_
  > Job 'check' падал на каждом push потому что:
- regenerate catalogs (Catalog up-to-date check) _8ac2cdaa_
- CI Catalog check — improve_auto_toc respects .docignore _d6279595_
  > CI workflow .github/workflows/test.yml job 'Catalog up-to-date check'
- восстановить 24 файла повреждённых GitHub Actions ботом _643d52de_
  > Бот (improve_run_all --fast --group reports) на чистом CI-сервере
- остановить деструктивные авто-обновления от GitHub Actions бота _ee0b767e_
  > Проблема: бот запускал improve_run_all.py --fast --group reports на чистом
- fix crosslink root cause (relative paths), map all 125 scripts in dependency map _ed3fa81f_
  > - Fixed improve_crosslink_all.py: links now use os.path.relpath() instead of
- fix 8607 broken internal links, improve health score formula _52179ba5_
  > - Fixed 8607 broken links (absolute → relative paths via improve_broken_links --fix)
- fix update-docs CI job failures _42f561dd_
  > Three issues fixed:
- исправить ошибки в deeptext скриптах, добавить выходные файлы _4755dd94_
  > Исправления в improve_contradiction_check.py:
- search engine bug — 356/460 docs had empty 'content' field _f873e5fc_
  > search_index.json uses two field names depending on improve_search_index.py
### ⚡ Улучшения

- batch 13 — badges, FAQ, schedule, cost estimate, footnotes _7aee1dba_
  > - improve_badges.py: docs/badges/ — 7 SVG badges inserted into README.md
- batch 12 — digest, progress, see-also, scoring, word cloud _04a64831_
  > - improve_digest.py: DIGEST.md — 15 commits history, 17 new files in last 3 commits
- batch 11 — orphans, alerts, metrics, index update, master runner _a48150bf_
  > - improve_orphans.py: ORPHANS.md — 0 isolated files (all 400 docs linked)
- batch 10 — backlinks, heatmap, templates, validation, executive report _a25efe45_
  > - improve_backlinks.py: BACKLINKS.md — 405 files mapped, reverse link index
- batch 9 — abbreviations, sentiment, narrative, JSON export, network _873b8c58_
  > - improve_abbreviations.py: ABBREVIATIONS.md — 83 abbreviations (21 known + 62 auto)
- batch 8 — stats, similar docs, questions, KPI, sitemap _ff8fe0fa_
  > - improve_stats.py: STATS.md — 436 files, 356,902 words across 6 sections
- batch 7 — compare, density, complexity, entities, concepts _1c9ceeaa_
  > - improve_compare.py: COMPARE.md — diff vs prev commit (151 new, 83 changed)
- batch 6 — autocorrect, TOC, tables/code extraction, word freq, health dashboard, reading order, decisions _0952c336_
  > - improve_autocorrect.py: 125 term replacements across 52 files
- consistency check, broken links, changelog, CSV export _14f735a7_
  > - improve_consistency.py: 66 inconsistent term spellings → CONSISTENCY.md
- action items, gap analysis, clustering, mindmap, HTML export _4e7137c4_
  > - improve_action_items.py: 490 items (risks, decisions, next steps) → ACTION_ITEMS.md
- add Q&A sheets, priority ranking, and contacts extraction _e787c21f_
  > - improve_qa.py: 5 section Q&A files + global QA.md (12 topic templates)
- add tags, search index, and project relationship graph _b3d7d0bf_
  > - improve_tags.py: tagged 316 files with 12 topics, 1021 tag entries → TAGS.md
- add summaries, cross-refs, dedup report, timeline _75f1b3e4_
  > - improve_summaries.py: added auto-annotations to 376 files
- verify coverage, merge short files, add READMEs and glossary _91dd9685_
  > - verify_coverage.py: checks 97.6%→100.5% text coverage, all 26 terms found

##  skip  (1 коммитов)

### 🔧 Обслуживание

- retry (with max_retries) _  - on_e_

##  22 скила  (1 коммитов)

### 🔧 Обслуживание

- 9 MCP-серверов (+8) _Итого: 2_
  > 5 манифестов

##  $.STEP.ou (1 коммитов)

### 🔧 Обслуживание

- constants _  - Inpu_

##  (1 коммитов)

### 🔧 Обслуживание

- preview _- _doc_t_

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "CHANGELOG"
```

```bash
# Альтернативный поиск (BM25)
python scripts/improve_semantic_search.py --query "CHANGELOG" --mode bm25
```

## Смотрите также
- [[CHANGELOG_AUTO]]
- [[DEPENDENCY_MAP]]
- [[VERSION_DIFF]]
- [[LANGUAGE_STATS]]


<!-- backlinks -->

---

**Кто ссылается на этот документ (4):**
- [READABILITY](../READABILITY.md)
- [READING_TIME](../READING_TIME.md)
- [SEARCH](../SEARCH.md)
- [TABLES](../TABLES.md)

