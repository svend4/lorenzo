---
title: "Отчёт об устаревших документах"
tags:
  - general
date: 2026-05-12
---

# Отчёт об устаревших документах

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> _Порог: 30 дней. Обновлено: 2026-05-12_
**Проекты:** Svyazi

---
<!-- tags: ingestion, local-first, collaboration -->




_Порог: 30 дней. Обновлено: 2026-05-12_

Найдено проблем: **132** файлов

## Без метаданных (нет summary или тегов) — 97 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/ALERTS.md` | 81 | нет summary, нет тегов, короткий (81 слов) |
| `docs/AUTHORS.md` | 100 | нет summary, нет тегов |
| `docs/BACKLINKS.md` | 401 | нет summary, нет тегов |
| `docs/CHANGELOG.md` | 5351 | нет тегов |
| `docs/COMPARE.md` | 321 | нет summary, нет тегов |
| `docs/CONCEPT_GRAPH.md` | 641 | нет тегов |
| `docs/CONSISTENCY.md` | 533 | нет summary, нет тегов |
| `docs/CONTACTS.md` | 350 | нет summary, нет тегов |
| `docs/CONTENT_GAPS.md` | 687 | нет summary, нет тегов |
| `docs/CONTRADICTIONS.md` | 1624 | нет summary, нет тегов |
| `docs/COST.md` | 344 | нет summary, нет тегов |
| `docs/CROSSREFS.md` | 522 | нет тегов |
| `docs/CROSS_SECTION.md` | 3800 | нет summary, нет тегов |
| `docs/DEPENDABOT.md` | 124 | нет summary, нет тегов |
| `docs/DIGEST.md` | 229 | нет summary, нет тегов |
| `docs/DIGEST_AUTO.md` | 418 | нет summary, нет тегов |
| `docs/GLOSSARY.md` | 125 | нет summary, нет тегов |
| `docs/KEYWORD_INDEX.md` | 498 | нет summary, нет тегов |
| `docs/KPI.md` | 2096 | нет summary, нет тегов |
| `docs/KPI_HISTORY.md` | 116 | нет summary, нет тегов |

## Короткие (< 100 слов, заготовки) — 35 файлов

| Файл | Слов |
|------|------|
| `docs/ai-collaborations/candidates/README.md` | 98 |
| `docs/glossary/README.md` | 88 |
| `docs/habr-unique-projects/analogues/README.md` | 91 |
| `docs/habr-unique-projects/final-ensembles/README.md` | 99 |
| `docs/lorenzo-agent/scenarios/README.md` | 88 |
| `docs/nautilus/community-discussions/agent-changes-reality/README.md` | 98 |
| `docs/nautilus/community-discussions/habr-article-1-reaction/README.md` | 88 |
| `docs/nautilus/community-discussions/habr-article-2-reaction/README.md` | 91 |
| `docs/nautilus/community-discussions/practical-observations/README.md` | 91 |
| `docs/nautilus/community-discussions/voiceless-contributors/README.md` | 88 |
| `docs/nautilus/composite-skills-agents-companion-mentors/README.md` | 99 |
| `docs/nautilus/innovation-transitions/README.md` | 95 |
| `docs/nautilus/multi-tier-architecture/README.md` | 91 |
| `docs/nautilus/supply-demand/README.md` | 91 |
| `docs/nautilus/transmission-box/README.md` | 91 |
| `docs/svyazi-2-0/limitations/README.md` | 95 |
| `docs/svyazi-2-0/outreach/README.md` | 98 |
| `docs/svyazi-2-0/prototype/README.md` | 88 |
| `docs/svyazi-2-0/security/README.md` | 98 |
| `docs/technology-combinations/research-reports/README.md` | 91 |

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

**Смотрите также:**
- [[TAGS]]
- [[SPELLCHECK]]
- [[HEALTH]]
- [[LLM_SUMMARIES]]


<!-- backlinks -->

---

**Кто ссылается на этот документ (7):**
- [[READABILITY]]
- [[READING_TIME]]
- [[README]]
- [[SEARCH]]
- [[TABLES]]
- [[TAGS]]
- [[VERSION_DIFF]]

