# Отчёт об устаревших документах

<!-- toc-auto -->

> [!NOTE]
> Раздел `STALENESS` формируется автоматически из данных репозитория.

<!-- alert-added -->
<!-- tags: staleness, docs -->


<!-- summary -->
> `STALENESS` — раздел документации проекта Lorenzo.


_Порог: 30 дней. Обновлено: 2026-05-11_

Найдено проблем: **134** файлов

## Без метаданных (нет summary или тегов) — 90 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/autofilled/README.md` | 48 | нет summary, нет тегов, короткий (48 слов) |
| `docs/obsidian/SCORING.md` | 226 | нет summary |
| `docs/CHANGELOG.md` | 3063 | нет тегов |
| `docs/COMPARE.md` | 321 | нет summary, нет тегов |
| `docs/CONTACTS.md` | 316 | нет summary, нет тегов |
| `docs/COST.md` | 344 | нет summary, нет тегов |
| `docs/PROGRESS.md` | 219 | нет summary, нет тегов |
| `docs/QA.md` | 2107 | нет summary, нет тегов |
| `docs/READING_ORDER.md` | 4042 | нет summary, нет тегов |
| `docs/SCHEDULE.md` | 212 | нет summary, нет тегов |
| `docs/SCORING.md` | 198 | нет summary, нет тегов |
| `docs/SITEMAP.md` | 6630 | нет summary, нет тегов |
| `docs/STATS.md` | 355 | нет summary, нет тегов |
| `docs/autofilled/components/README.md` | 78 | нет summary, нет тегов, короткий (78 слов) |
| `docs/obsidian/QA.md` | 385 | нет summary, нет тегов |
| `docs/obsidian/ai-collaborations/README.md` | 57 | нет summary, нет тегов, короткий (57 слов) |
| `docs/obsidian/ai-collaborations/candidates/README.md` | 38 | нет summary, нет тегов, короткий (38 слов) |
| `docs/obsidian/ai-collaborations/continuation/README.md` | 88 | нет summary, нет тегов, короткий (88 слов) |
| `docs/obsidian/ai-collaborations/ensembles/README.md` | 84 | нет summary, нет тегов, короткий (84 слов) |
| `docs/obsidian/anthropic-vacancies/README.md` | 96 | нет summary, нет тегов, короткий (96 слов) |

## Короткие (< 100 слов, заготовки) — 44 файлов

| Файл | Слов |
|------|------|
| `docs/ai-collaborations/README.md` | 98 |
| `docs/ai-collaborations/candidates/README.md` | 80 |
| `docs/anthropic-vacancies/extra-collaborator-findings/README.md` | 99 |
| `docs/anthropic-vacancies/mmorpg-for-programmers/README.md` | 95 |
| `docs/anthropic-vacancies/nautilus-pro2-analysis/README.md` | 84 |
| `docs/anthropic-vacancies/nautilus-vs-camel/README.md` | 95 |
| `docs/anthropic-vacancies/profile-mapping/02-reanalysis/README.md` | 91 |
| `docs/anthropic-vacancies/profile-mapping/03-integral-final/README.md` | 91 |
| `docs/badges/README.md` | 98 |
| `docs/glossary/README.md` | 91 |
| `docs/habr-unique-projects/analogues/README.md` | 91 |
| `docs/habr-unique-projects/final-ensembles/README.md` | 81 |
| `docs/habr-unique-projects/hardware-pairs/README.md` | 99 |
| `docs/habr-unique-projects/key-findings/README.md` | 95 |
| `docs/habr-unique-projects/software-pairs/README.md` | 86 |
| `docs/lorenzo-agent/naming/README.md` | 87 |
| `docs/lorenzo-agent/operationalized/README.md` | 96 |
| `docs/lorenzo-agent/scenarios/README.md` | 88 |
| `docs/meta-scripting/README.md` | 87 |
| `docs/nautilus/community-discussions/agent-changes-reality/README.md` | 91 |

## Рекомендуемые действия

```bash
# Добавить summary и теги к файлам без метаданных
python scripts/improve_summaries.py
python scripts/improve_tags.py

# Обогатить короткие файлы через LLM
python scripts/improve_llm_enrich.py --section 05-habr-projects
```

## Смотрите также
- [Главная](README.md)
- [Метрики](METRICS.md)
- [Здоровье](HEALTH.md)
- [Глоссарий](GLOSSARY.md)
- [Сущности](ENTITIES.md)
