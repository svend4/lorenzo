# Changelog (авто)

<!-- summary -->
> - [Статистика коммитов](#статистика-коммитов)

---

<!-- toc -->
## Содержание

- [Contents](#contents)
- [Статистика коммитов](#статистика-коммитов)
- [История изменений](#история-изменений)
  - [2026-04](#2026-04)

---

<!-- tags: rag, ingestion, roadmap, anthropic -->




<!-- toc-auto -->
## Contents

- [Статистика коммитов](#статистика-коммитов)
- [История изменений](#история-изменений)
  - [2026-04](#2026-04)


_Сгенерировано из 48 коммитов git-истории._

## Статистика коммитов

| Тип | Название | Кол-во |
|-----|---------|--------|
| `feat` | ✨ Новые возможности | 17 |
| `fix` | 🐛 Исправления | 3 |
| `docs` | 📝 Документация | 2 |
| `chore` | 🔧 Технические задачи | 10 |
| `other` | 📌 Прочее | 16 |

## История изменений


### 2026-04

**✨ Новые возможности**

- add component matrix, KPI history tracker, fix run_all coverage `69562b02`
- add risk register, auto-changelog, master index; fix run_all missing scripts `59617c5d`
- add tech radar, onboarding guide, dependency map, meta group in run_all `4ddee95e`
- add autonomous watcher (Ступень 6), CI workflow, LLM section summaries `1f3fe74a`
- add CLAUDE.md, weekly digest script, enrich group in run_all `469dbced`
- add LLM integration (Ступень 3), skills (Ступень 4), MCP server (Ступень 5) `00a25f78`
- добавить 12 скриптов глубокой обработки текста (группа deeptext) `6cbd49c7`
- add 9 text-processing scripts (textwork group) for large-scale knowledge management `bfe2bdda`
- add 16 new improve_* scripts across quality/export/cicd/analytics groups `f8464fe2`
- 13 улучшений — search fix, parallel/report/only, watch, priority, bulk, coverage, staleness, autofix, qa history, llm co `3d29c06c`
- 4 улучшения — кэш QA, --save, dedup с текстом дублей, --only, MCP contact status `77613be2`
- 4 улучшения — contact_status CLI, --changed флаг, нормализация поискового индекса, post-commit хук `58003258`
- add improve skill — universal improvement workflow for Lorenzo `6e576a81`
- implement 3 improvements + fix question truncation `a32f556b`
- implement stages 0-5 of the script→skill→plugin hierarchy `612e585b`
- add improve_autofill.py — fills templates from existing script outputs `d946c3b3`
- organize docs into monorepo structure with topic-based subfolders `d49a1f0f`

**🐛 Исправления**

- fix update-docs CI job failures `42f561dd`
- исправить ошибки в deeptext скриптах, добавить выходные файлы `4755dd94`
- search engine bug — 356/460 docs had empty 'content' field `f873e5fc`

**📝 Документация**

- sync PROGRESS.md `4e217f2b`
- sync PROGRESS.md after adding 16 new scripts `4d237951`

**🔧 Технические задачи**

- sync CONTRADICTIONS.md (background task output) `89d3e8fb`
- sync CONTRADICTIONS.md after contradiction_check fix `6b81ffed`
- update mcp.json description wording `4e52a185`
- sync PROGRESS.md after deeptext scripts commit `1d552d4e`
- sync PROGRESS.md after session `53bfdbd8`
- sync generated docs (CONTACTS, HEALTH, METRICS) `5571b369`
- add CLAUDE.md, requirements.txt, .claude/settings.json `cfdcd4e8`
- commit README.md with SVG badges from batch 13 `be9de469`
- add .gitignore for Python cache files `7658df5b`
- add extract_mhtml.py and ignore pycache `ff8a8161`

**📌 Прочее**

- batch 13 — badges, FAQ, schedule, cost estimate, footnotes `7aee1dba`
- batch 12 — digest, progress, see-also, scoring, word cloud `04a64831`
- batch 11 — orphans, alerts, metrics, index update, master runner `a48150bf`
- batch 10 — backlinks, heatmap, templates, validation, executive report `a25efe45`
- batch 9 — abbreviations, sentiment, narrative, JSON export, network `873b8c58`
- batch 8 — stats, similar docs, questions, KPI, sitemap `ff8fe0fa`
- batch 7 — compare, density, complexity, entities, concepts `1c9ceeaa`
- batch 6 — autocorrect, TOC, tables/code extraction, word freq, health dashboard, reading order, decisions `0952c336`
- consistency check, broken links, changelog, CSV export `14f735a7`
- action items, gap analysis, clustering, mindmap, HTML export `4e7137c4`
- add Q&A sheets, priority ranking, and contacts extraction `e787c21f`
- add tags, search index, and project relationship graph `b3d7d0bf`
- add summaries, cross-refs, dedup report, timeline `75f1b3e4`
- verify coverage, merge short files, add READMEs and glossary `91dd9685`
- Add files via upload `183c4e9f`
- Initial commit `6c49dba6`

---

_Changelog генерируется автоматически из conventional commits._

_Ручной changelog: `docs/CHANGELOG.md` (если существует)._


<!-- see-also -->

---

**Смотрите также:**
- [CHANGELOG](docs/CHANGELOG.md)
- [DEPENDENCY_MAP](docs/DEPENDENCY_MAP.md)
- [DIGEST](docs/DIGEST.md)
- [SITEMAP](docs/SITEMAP.md)

