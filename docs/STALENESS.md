# Отчёт об устаревших документах
<!-- tags: ingestion, local-first, anthropic, collaboration -->


_Порог: 30 дней. Обновлено: 2026-05-13_

Найдено проблем: **81** файлов

## Без метаданных (нет summary или тегов) — 59 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/autofilled/README.md` | 66 | нет summary, нет тегов, короткий (66 слов) |
| `docs/autofilled/components/README.md` | 96 | нет summary, нет тегов, короткий (96 слов) |
| `docs/ALERTS.md` | 105 | нет тегов |
| `docs/BACKLINKS.md` | 413 | нет тегов |
| `docs/CLUSTERS.md` | 1671 | нет тегов |
| `docs/COMPARE.md` | 342 | нет тегов |
| `docs/CONCEPT_GRAPH.md` | 611 | нет тегов |
| `docs/CONSISTENCY.md` | 520 | нет тегов |
| `docs/CONTENT_GAPS.md` | 683 | нет тегов |
| `docs/CONTRADICTIONS.md` | 1450 | нет тегов |
| `docs/CROSS_SECTION.md` | 4035 | нет тегов |
| `docs/DEPENDABOT.md` | 116 | нет тегов |
| `docs/DIGEST_AUTO.md` | 371 | нет тегов |
| `docs/INFO_PROCESSING_METHODS.md` | 3075 | нет тегов |
| `docs/KEYWORD_INDEX.md` | 489 | нет тегов |
| `docs/KPI.md` | 2222 | нет тегов |
| `docs/KPI_HISTORY.md` | 131 | нет тегов |
| `docs/LANGUAGE_STATS.md` | 3471 | нет тегов |
| `docs/LLM_GAPS.md` | 72 | нет тегов, короткий (72 слов) |
| `docs/NARRATIVE.md` | 1036 | нет тегов |

## Короткие (< 100 слов, заготовки) — 22 файлов

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
