# CHANGELOG

Всего коммитов: **52**  
Статистика: ✨ feat: 18 | ⚡ improve: 14 | 🔧 chore: 13 | 🐛 fix: 4 | 📝 docs: 3


## 2026-04-29 (51 коммитов)

### 🔧 Обслуживание

- sync CONTRADICTIONS.md (background task output) _89d3e8fb_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
- sync CONTRADICTIONS.md after contradiction_check fix _6b81ffed_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
- update mcp.json description wording _4e52a185_
  > https://claude.ai/code/session_0179jSZDgmKgh9eLH72HRLuv
- sync PROGRESS.md after deeptext scripts commit _1d552d4e_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
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
- Add files via upload _183c4e9f_
- Initial commit _6c49dba6_
### 📝 Документация

- auto-update via improve_run_all [skip ci] _8e689b3d_
- sync PROGRESS.md _4e217f2b_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
- sync PROGRESS.md after adding 16 new scripts _4d237951_
  > https://claude.ai/code/session_01R8BfHH65xW6pXJw2RvvLiW
### ✨ Новые функции

- run all script groups, apply TOC/abstracts/crosslinks, rebuild search index _898c42a0_
  > - All 7 script groups pass clean (quality, analytics, deeptext, meta, textwork, reports, generate)
- add component matrix, KPI history tracker, fix run_all coverage _69562b02_
  > - improve_component_matrix.py: 14×10 compatibility matrix (memory/search/
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

##  (1 коммитов)

### 🔧 Обслуживание

- preview _- _doc_t_
