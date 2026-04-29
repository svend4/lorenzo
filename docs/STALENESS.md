# Отчёт об устаревших документах

_Порог: 30 дней. Обновлено: 2026-04-29_

Найдено проблем: **113** файлов

## Без метаданных (нет summary или тегов) — 88 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/01-svyazi/00-intro-part2.md` | 5 | нет summary, нет тегов, короткий (5 слов) |
| `docs/01-svyazi/QA.md` | 277 | нет summary, нет тегов |
| `docs/01-svyazi/README.md` | 90 | нет тегов, короткий (90 слов) |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 14 | нет summary, нет тегов, короткий (14 слов) |
| `docs/02-anthropic-vacancies/QA.md` | 360 | нет summary, нет тегов |
| `docs/03-technology-combinations/QA.md` | 124 | нет summary, нет тегов |
| `docs/03-technology-combinations/README.md` | 39 | нет тегов, короткий (39 слов) |
| `docs/04-ai-collaborations/QA.md` | 282 | нет summary, нет тегов |
| `docs/04-ai-collaborations/README.md` | 84 | нет summary, нет тегов, короткий (84 слов) |
| `docs/05-habr-projects/QA.md` | 111 | нет summary, нет тегов |
| `docs/05-habr-projects/README.md` | 38 | нет summary, нет тегов, короткий (38 слов) |
| `docs/05-habr-projects/knowledge/README.md` | 10 | нет summary, нет тегов, короткий (10 слов) |
| `docs/05-habr-projects/memory/README.md` | 17 | нет summary, нет тегов, короткий (17 слов) |
| `docs/ABBREVIATIONS.md` | 1018 | нет summary, нет тегов |
| `docs/ACTION_ITEMS.md` | 7160 | нет summary, нет тегов |
| `docs/ALERTS.md` | 50 | нет summary, нет тегов, короткий (50 слов) |
| `docs/AUTHORS.md` | 66 | нет summary, нет тегов, короткий (66 слов) |
| `docs/CHANGELOG.md` | 914 | нет summary, нет тегов |
| `docs/CODE_BLOCKS.md` | 4580 | нет summary, нет тегов |
| `docs/COMPARE.md` | 321 | нет summary, нет тегов |

## Короткие (< 100 слов, заготовки) — 25 файлов

| Файл | Слов |
|------|------|
| `docs/obsidian/01-svyazi/00-intro-part2.md` | 27 |
| `docs/obsidian/02-anthropic-vacancies/102-доступ-к-данным.md` | 61 |
| `docs/obsidian/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | 77 |
| `docs/obsidian/02-anthropic-vacancies/16-history.md` | 97 |
| `docs/obsidian/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 38 |
| `docs/obsidian/ALERTS.md` | 80 |
| `docs/obsidian/KPI_HISTORY.md` | 89 |
| `docs/obsidian/autofilled/components/.md` | 78 |
| `docs/obsidian/autofilled/components/cowork.md` | 80 |
| `docs/obsidian/autofilled/components/ingit.md` | 80 |
| `docs/obsidian/autofilled/components/kksudo.md` | 68 |
| `docs/obsidian/autofilled/components/lorenzo.md` | 80 |
| `docs/obsidian/autofilled/components/nautilus.md` | 80 |
| `docs/obsidian/autofilled/components/sgb.md` | 80 |
| `docs/obsidian/autofilled/components/spbmolot.md` | 68 |
| `docs/obsidian/autofilled/components/svend4.md` | 80 |
| `docs/obsidian/autofilled/components/svyazi.md` | 80 |
| `docs/obsidian/templates/decision-record.md` | 82 |
| `docs/obsidian/templates/project-component.md` | 99 |
| `docs/obsidian/templates/research-note.md` | 77 |

## Рекомендуемые действия

```bash
# Добавить summary и теги к файлам без метаданных
python scripts/improve_summaries.py
python scripts/improve_tags.py

# Обогатить короткие файлы через LLM
python scripts/improve_llm_enrich.py --section 05-habr-projects
```
