---
title: "Отчёт об устаревших документах"
tags:
  - ingestion
  - anthropic
  - collaboration
  - general
date: 2026-05-11
---

# Отчёт об устаревших документах

<!-- summary -->
> _Порог: 30 дней. Обновлено: 2026-05-11_
**Проекты:** Svyazi

---
<!-- tags: ingestion, anthropic, collaboration -->




_Порог: 30 дней. Обновлено: 2026-05-11_

Найдено проблем: **111** файлов

## Без метаданных (нет summary или тегов) — 35 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/autofilled/README.md` | 48 | нет summary, нет тегов, короткий (48 слов) |
| `docs/01-svyazi/QA.md` | 208 | нет summary, нет тегов |
| `docs/02-anthropic-vacancies/QA.md` | 362 | нет summary, нет тегов |
| `docs/03-technology-combinations/QA.md` | 100 | нет summary, нет тегов |
| `docs/04-ai-collaborations/QA.md` | 258 | нет summary, нет тегов |
| `docs/05-habr-projects/QA.md` | 168 | нет summary, нет тегов |
| `docs/CHANGELOG.md` | 3358 | нет тегов |
| `docs/COMPARE.md` | 269 | нет summary, нет тегов |
| `docs/CONTACTS.md` | 314 | нет summary, нет тегов |
| `docs/COST.md` | 332 | нет summary, нет тегов |
| `docs/DIGEST.md` | 219 | нет summary, нет тегов |
| `docs/PROGRESS.md` | 219 | нет summary, нет тегов |
| `docs/QA.md` | 2132 | нет summary, нет тегов |
| `docs/READING_ORDER.md` | 4042 | нет summary, нет тегов |
| `docs/REPORT.md` | 640 | нет summary, нет тегов |
| `docs/SCHEDULE.md` | 212 | нет summary, нет тегов |
| `docs/SCORING.md` | 198 | нет summary, нет тегов |
| `docs/SITEMAP.md` | 6763 | нет summary, нет тегов |
| `docs/STATS.md` | 363 | нет summary, нет тегов |
| `docs/VALIDATION.md` | 558 | нет summary, нет тегов |

## Короткие (< 100 слов, заготовки) — 76 файлов

| Файл | Слов |
|------|------|
| `docs/ALERTS.md` | 98 |
| `docs/MCP_DASHBOARD.md` | 86 |
| `docs/SKILL_DASHBOARD.md` | 86 |
| `docs/ai-collaborations/README.md` | 98 |
| `docs/ai-collaborations/candidates/README.md` | 80 |
| `docs/anthropic-vacancies/extra-collaborator-findings/README.md` | 99 |
| `docs/anthropic-vacancies/mmorpg-for-programmers/README.md` | 95 |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/README.md` | 84 |
| `docs/anthropic-vacancies/nautilus-vs-camel/README.md` | 95 |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/README.md` | 91 |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/README.md` | 91 |
| `docs/glossary/README.md` | 98 |
| `docs/habr-unique-projects/analogues/README.md` | 87 |
| `docs/habr-unique-projects/final-ensembles/README.md` | 81 |
| `docs/habr-unique-projects/hardware-pairs/README.md` | 99 |
| `docs/habr-unique-projects/key-findings/README.md` | 95 |
| `docs/habr-unique-projects/software-pairs/README.md` | 86 |
| `docs/lorenzo-agent/naming/README.md` | 87 |
| `docs/lorenzo-agent/operationalized/README.md` | 96 |
| `docs/lorenzo-agent/scenarios/README.md` | 84 |

## Рекомендуемые действия

```bash
# Добавить summary и теги к файлам без метаданных
python scripts/improve_summaries.py
python scripts/improve_tags.py

# Обогатить короткие файлы через LLM
python scripts/improve_llm_enrich.py --section 05-habr-projects
```

<!-- backlinks -->

---

**Кто ссылается на этот документ (4):**
- [READABILITY](../READABILITY.md)
- [READING_TIME](../READING_TIME.md)
- [SEARCH](../SEARCH.md)
- [TABLES](../TABLES.md)

