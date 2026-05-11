# Отчёт об устаревших документах

<!-- toc-auto -->

> [!NOTE]
> Документ `STALENESS` создаётся автоматически.

<!-- alert-added -->
<!-- tags: staleness, docs, analysis -->


<!-- summary -->
> Автоматически сформированный документ: `STALENESS`.


_Порог: 30 дней. Обновлено: 2026-05-11_

Найдено проблем: **181** файлов

## Без метаданных (нет summary или тегов) — 175 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/01-svyazi/QA.md` | 257 | нет summary, нет тегов |
| `docs/02-anthropic-vacancies/QA.md` | 362 | нет summary, нет тегов |
| `docs/03-technology-combinations/QA.md` | 100 | нет summary, нет тегов |
| `docs/04-ai-collaborations/QA.md` | 258 | нет summary, нет тегов |
| `docs/05-habr-projects/QA.md` | 206 | нет summary, нет тегов |
| `docs/CHANGELOG.md` | 3014 | нет тегов |
| `docs/COMPARE.md` | 321 | нет summary, нет тегов |
| `docs/CONTACTS.md` | 316 | нет summary, нет тегов |
| `docs/COST.md` | 344 | нет summary, нет тегов |
| `docs/FAQ.md` | 867 | нет summary, нет тегов |
| `docs/PROGRESS.md` | 219 | нет summary, нет тегов |
| `docs/QA.md` | 2107 | нет summary, нет тегов |
| `docs/READING_ORDER.md` | 4042 | нет summary, нет тегов |
| `docs/SCHEDULE.md` | 212 | нет summary, нет тегов |
| `docs/SCORING.md` | 198 | нет summary, нет тегов |
| `docs/SEE_ALSO.md` | 365 | нет summary, нет тегов |
| `docs/SITEMAP.md` | 6630 | нет summary, нет тегов |
| `docs/STATS.md` | 355 | нет summary, нет тегов |
| `docs/ai-collaborations/README.md` | 70 | нет summary, нет тегов, короткий (70 слов) |
| `docs/ai-collaborations/candidates/README.md` | 47 | нет summary, нет тегов, короткий (47 слов) |

## Короткие (< 100 слов, заготовки) — 6 файлов

| Файл | Слов |
|------|------|
| `docs/ALERTS.md` | 83 |
| `docs/templates/contact-outreach.md` | 81 |
| `docs/templates/decision-record.md` | 53 |
| `docs/templates/ensemble.md` | 81 |
| `docs/templates/project-component.md` | 69 |
| `docs/templates/research-note.md` | 51 |

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
- [Дашборд](HEALTH.md)
- [Глоссарий](GLOSSARY.md)
- [Сущности](ENTITIES.md)
