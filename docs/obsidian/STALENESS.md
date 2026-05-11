---
title: "Отчёт об устаревших документах"
tags:
  - general
date: 2026-05-11
---

# Отчёт об устаревших документах

<!-- summary -->
> _Порог: 30 дней. Обновлено: 2026-05-11_

---
<!-- tags: orchestration, local-first, anthropic, collaboration -->




_Порог: 30 дней. Обновлено: 2026-05-11_

Найдено проблем: **126** файлов

## Без метаданных (нет summary или тегов) — 87 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/ABBREVIATIONS.md` | 1304 | нет summary, нет тегов |
| `docs/ACTION_ITEMS.md` | 9444 | нет summary, нет тегов |
| `docs/ALERTS.md` | 50 | нет summary, нет тегов, короткий (50 слов) |
| `docs/AUTHORS.md` | 144 | нет summary, нет тегов |
| `docs/BACKLINKS.md` | 432 | нет summary, нет тегов |
| `docs/CHANGELOG.md` | 3792 | нет тегов |
| `docs/CLUSTERS.md` | 1669 | нет summary, нет тегов |
| `docs/CODE_BLOCKS.md` | 5044 | нет summary, нет тегов |
| `docs/COMPARE.md` | 321 | нет summary, нет тегов |
| `docs/COMPLEXITY.md` | 343 | нет summary, нет тегов |
| `docs/CONCEPTS.md` | 16181 | нет summary, нет тегов |
| `docs/CONTACTS.md` | 316 | нет summary, нет тегов |
| `docs/CONTENT_GAPS.md` | 674 | нет summary, нет тегов |
| `docs/COST.md` | 344 | нет summary, нет тегов |
| `docs/CROSSREFS.md` | 502 | нет summary, нет тегов |
| `docs/DENSITY.md` | 336 | нет summary, нет тегов |
| `docs/DIGEST.md` | 200 | нет summary, нет тегов |
| `docs/ENTITIES.md` | 397 | нет summary, нет тегов |
| `docs/FAQ.md` | 1346 | нет summary, нет тегов |
| `docs/FOOTNOTES.md` | 204 | нет summary, нет тегов |

## Короткие (< 100 слов, заготовки) — 39 файлов

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
| `docs/obsidian/glossary/README.md` | 91 |
| `docs/obsidian/habr-unique-projects/analogues/README.md` | 94 |
| `docs/obsidian/lorenzo-agent/scenarios/README.md` | 92 |
| `docs/obsidian/nautilus/community-discussions/habr-article-1-reaction/README.md` | 92 |
| `docs/obsidian/nautilus/community-discussions/habr-article-2-reaction/README.md` | 94 |

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

**Кто ссылается на этот документ (9):**
- [[CONSISTENCY]]
- [[DEPENDENCY_MAP]]
- [[DIGEST_AUTO]]
- [[ORPHANS]]
- [[READABILITY]]
- [[READING_TIME]]
- [[README]]
- [[SEARCH]]
- _...ещё 1_

