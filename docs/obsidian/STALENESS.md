---
title: "Отчёт об устаревших документах"
tags:
  - ingestion
  - anthropic
  - collaboration
  - general
date: 2026-05-10
---

# Отчёт об устаревших документах

<!-- toc -->
## Содержание

- [Contents](#contents)
- [Без метаданных (нет summary или тегов) — 239 файлов](#без-метаданных-нет-summary-или-тегов-239-файлов)
- [Короткие (< 100 слов, заготовки) — 34 файлов](#короткие-100-слов-заготовки-34-файлов)
- [Рекомендуемые действия](#рекомендуемые-действия)
- [Смотрите также](#смотрите-также)

---


<!-- toc-auto -->
## Contents

- [Без метаданных (нет summary или тегов) — 239 файлов](#без-метаданных-нет-summary-или-тегов-239-файлов)
- [Короткие (< 100 слов, заготовки) — 34 файлов](#короткие-100-слов-заготовки-34-файлов)
- [Рекомендуемые действия](#рекомендуемые-действия)
- [Смотрите также](#смотрите-также)


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> _Порог: 30 дней. Обновлено: 2026-05-10_
**Проекты:** Svyazi

---
<!-- tags: ingestion, anthropic, collaboration -->




_Порог: 30 дней. Обновлено: 2026-05-10_

Найдено проблем: **273** файлов

## Без метаданных (нет summary или тегов) — 239 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/01-svyazi/00-intro-part2.md` | 5 | нет summary, нет тегов, короткий (5 слов) |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 14 | нет summary, нет тегов, короткий (14 слов) |
| `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` | 178 | нет тегов |
| `docs/MCP_DASHBOARD.md` | 177 | нет summary, нет тегов |
| `docs/ai-collaborations/README.md` | 40 | нет тегов, короткий (40 слов) |
| `docs/ai-collaborations/candidates/README.md` | 17 | нет тегов, короткий (17 слов) |
| `docs/ai-collaborations/channels/README.md` | 24 | нет summary, нет тегов, короткий (24 слов) |
| `docs/ai-collaborations/continuation/README.md` | 49 | нет тегов, короткий (49 слов) |
| `docs/ai-collaborations/ensembles/README.md` | 42 | нет тегов, короткий (42 слов) |
| `docs/ai-collaborations/fast-tracks/README.md` | 309 | нет summary, нет тегов |
| `docs/ai-collaborations/strategy/README.md` | 31 | нет summary, нет тегов, короткий (31 слов) |
| `docs/anthropic-vacancies/README.md` | 73 | нет тегов, короткий (73 слов) |
| `docs/anthropic-vacancies/ai-managed-virtual-company/README.md` | 51 | нет тегов, короткий (51 слов) |
| `docs/anthropic-vacancies/beneficial-deployments-concept/README.md` | 53 | нет тегов, короткий (53 слов) |
| `docs/anthropic-vacancies/clusters/README.md` | 69 | нет тегов, короткий (69 слов) |
| `docs/anthropic-vacancies/extra-collaborator-findings/README.md` | 34 | нет тегов, короткий (34 слов) |
| `docs/anthropic-vacancies/hermes-comparison/README.md` | 62 | нет тегов, короткий (62 слов) |
| `docs/anthropic-vacancies/mmorpg-for-programmers/README.md` | 29 | нет тегов, короткий (29 слов) |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/README.md` | 20 | нет тегов, короткий (20 слов) |
| `docs/anthropic-vacancies/nautilus-vs-camel/README.md` | 30 | нет тегов, короткий (30 слов) |

## Короткие (< 100 слов, заготовки) — 34 файлов

| Файл | Слов |
|------|------|
| `docs/SKILL_DASHBOARD.md` | 26 |
| `docs/anthropic-vacancies/clusters/04-security.md` | 86 |
| `docs/anthropic-vacancies/clusters/05-marketing-brand.md` | 97 |
| `docs/anthropic-vacancies/clusters/06-engineering-design-product.md` | 99 |
| `docs/anthropic-vacancies/clusters/07-software-engineering-infrastructure.md` | 97 |
| `docs/anthropic-vacancies/clusters/09-product-management-support-ops.md` | 86 |
| `docs/anthropic-vacancies/clusters/10-compute.md` | 90 |
| `docs/anthropic-vacancies/clusters/11-legal.md` | 90 |
| `docs/anthropic-vacancies/clusters/12-technical-program-management.md` | 78 |
| `docs/anthropic-vacancies/clusters/13-communications.md` | 71 |
| `docs/anthropic-vacancies/clusters/14-public-policy.md` | 78 |
| `docs/anthropic-vacancies/clusters/15-public-benefit.md` | 78 |
| `docs/anthropic-vacancies/clusters/16-people.md` | 69 |
| `docs/lorenzo-agent/00-intro.md` | 66 |
| `docs/nautilus/community-discussions/habr-article-1-reaction/00-question-habr-link.md` | 61 |
| `docs/nautilus/npp-v1-0/17-appendix-b-change-log.md` | 84 |
| `docs/nautilus/review-methodology/15-appendix-c-history.md` | 89 |
| `docs/obsidian/01-svyazi/00-intro-part2.md` | 27 |
| `docs/obsidian/02-anthropic-vacancies/120-главные-технические-риски.md` | 80 |
| `docs/obsidian/KPI_HISTORY.md` | 74 |

## Рекомендуемые действия

```bash
# Добавить summary и теги к файлам без метаданных
python scripts/improve_summaries.py
python scripts/improve_tags.py

# Обогатить короткие файлы через LLM
python scripts/improve_llm_enrich.py --section 05-habr-projects
```

<!-- see-also -->

---

## Смотрите также
- [[14-main-technical-risks]]
- [[COVERAGE]]
- [[12-appendix-a-header-warning]]
- [[SPELLCHECK]]


<!-- backlinks -->

---

**Кто ссылается на этот документ (3):**
- [READABILITY](../READABILITY.md)
- [READING_TIME](../READING_TIME.md)
- [SEARCH](../SEARCH.md)

