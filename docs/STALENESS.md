# Отчёт об устаревших документах

<!-- toc-auto -->
## Содержание

- Основной раздел


<!-- summary -->
> Отчёт об устаревших документах — документ базы знаний репозитория Lorenzo.

<!-- tags: docs, reference, lorenzo -->

> [!NOTE]
> Документ содержит структурированную информацию из базы знаний репозитория Lorenzo.

<!-- alert-added -->


_Порог: 30 дней. Обновлено: 2026-05-10_

Найдено проблем: **215** файлов

## Без метаданных (нет summary или тегов) — 210 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/01-svyazi/QA.md` | 257 | нет summary, нет тегов |
| `docs/02-anthropic-vacancies/QA.md` | 362 | нет summary, нет тегов |
| `docs/03-technology-combinations/QA.md` | 124 | нет summary, нет тегов |
| `docs/04-ai-collaborations/QA.md` | 282 | нет summary, нет тегов |
| `docs/05-habr-projects/QA.md` | 206 | нет summary, нет тегов |
| `docs/ABBREVIATIONS.md` | 1273 | нет summary, нет тегов |
| `docs/ACTION_ITEMS.md` | 2957 | нет summary, нет тегов |
| `docs/ALERTS.md` | 50 | нет summary, нет тегов, короткий (50 слов) |
| `docs/AUTHORS.md` | 120 | нет summary, нет тегов |
| `docs/BACKLINKS.md` | 412 | нет summary, нет тегов |
| `docs/CHANGELOG.md` | 2990 | нет тегов |
| `docs/CODE_BLOCKS.md` | 5086 | нет summary, нет тегов |
| `docs/COMPARE.md` | 321 | нет summary, нет тегов |
| `docs/COMPLEXITY.md` | 343 | нет summary, нет тегов |
| `docs/CONCEPTS.md` | 15918 | нет summary, нет тегов |
| `docs/CONSISTENCY.md` | 527 | нет summary, нет тегов |
| `docs/CONTACTS.md` | 316 | нет summary, нет тегов |
| `docs/CONTENT_GAPS.md` | 674 | нет summary, нет тегов |
| `docs/COST.md` | 344 | нет summary, нет тегов |
| `docs/CROSSREFS.md` | 502 | нет summary, нет тегов |

## Короткие (< 100 слов, заготовки) — 5 файлов

| Файл | Слов |
|------|------|
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


_Смотрите также: [README](README.md) · [Глоссарий](GLOSSARY.md) · [Контакты](CONTACTS.md)_
