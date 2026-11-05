# Отчёт об устаревших документах

<!-- toc-auto -->

> [!NOTE]
> Раздел `STALENESS` формируется автоматически из данных репозитория.

<!-- alert-added -->
<!-- tags: staleness, docs -->


<!-- summary -->
> `STALENESS` — раздел документации проекта Lorenzo.


_Порог: 30 дней. Обновлено: 2026-06-05_

Найдено проблем: **472** файлов

## Без метаданных (нет summary или тегов) — 470 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/01-svyazi/QA.md` | 208 | нет summary, нет тегов |
| `docs/02-anthropic-vacancies/QA.md` | 362 | нет summary, нет тегов |
| `docs/03-technology-combinations/QA.md` | 100 | нет summary, нет тегов |
| `docs/04-ai-collaborations/QA.md` | 258 | нет summary, нет тегов |
| `docs/05-habr-projects/QA.md` | 168 | нет summary, нет тегов |
| `docs/06-discovery/README.md` | 915 | нет summary, нет тегов |
| `docs/CHANGELOG.md` | 14531 | нет тегов |
| `docs/CONTACTS.md` | 440 | нет summary, нет тегов |
| `docs/COST.md` | 344 | нет summary, нет тегов |
| `docs/FEEDBACK_LOOP.md` | 16 | нет summary, нет тегов, короткий (16 слов) |
| `docs/QA.md` | 2214 | нет summary, нет тегов |
| `docs/QUERY_ANALYTICS.md` | 16 | нет summary, нет тегов, короткий (16 слов) |
| `docs/ROADMAP/README.md` | 881 | нет тегов |
| `docs/SCHEDULE.md` | 212 | нет summary, нет тегов |
| `docs/SCORING.md` | 198 | нет summary, нет тегов |
| `docs/anthropic-vacancies/QA.md` | 70 | нет summary, нет тегов, короткий (70 слов) |
| `docs/autofilled/README.md` | 116 | нет тегов |
| `docs/autofilled/components/README.md` | 105 | нет summary, нет тегов |
| `docs/badges/README.md` | 69 | нет summary, нет тегов, короткий (69 слов) |
| `docs/letters/QA.md` | 118 | нет summary, нет тегов |

## Короткие (< 100 слов, заготовки) — 2 файлов

| Файл | Слов |
|------|------|
| `docs/MCP_DASHBOARD.md` | 78 |
| `docs/SKILL_DASHBOARD.md` | 96 |

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
