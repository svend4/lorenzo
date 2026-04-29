# Отчёт об устаревших документах

_Порог: 30 дней. Обновлено: 2026-04-29_

Найдено проблем: **131** файлов

## Без метаданных (нет summary или тегов) — 93 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/01-svyazi/00-intro-part2.md` | 5 | нет summary, нет тегов, короткий (5 слов) |
| `docs/01-svyazi/QA.md` | 255 | нет summary, нет тегов |
| `docs/01-svyazi/README.md` | 90 | нет тегов, короткий (90 слов) |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 14 | нет summary, нет тегов, короткий (14 слов) |
| `docs/02-anthropic-vacancies/QA.md` | 360 | нет summary, нет тегов |
| `docs/03-technology-combinations/QA.md` | 100 | нет summary, нет тегов |
| `docs/03-technology-combinations/README.md` | 39 | нет тегов, короткий (39 слов) |
| `docs/04-ai-collaborations/QA.md` | 258 | нет summary, нет тегов |
| `docs/04-ai-collaborations/README.md` | 84 | нет summary, нет тегов, короткий (84 слов) |
| `docs/05-habr-projects/QA.md` | 111 | нет summary, нет тегов |
| `docs/05-habr-projects/README.md` | 38 | нет summary, нет тегов, короткий (38 слов) |
| `docs/05-habr-projects/knowledge/README.md` | 10 | нет summary, нет тегов, короткий (10 слов) |
| `docs/05-habr-projects/memory/README.md` | 17 | нет summary, нет тегов, короткий (17 слов) |
| `docs/ABBREVIATIONS.md` | 1019 | нет summary, нет тегов |
| `docs/ACTION_ITEMS.md` | 7179 | нет summary, нет тегов |
| `docs/ALERTS.md` | 50 | нет summary, нет тегов, короткий (50 слов) |
| `docs/AUTHORS.md` | 66 | нет summary, нет тегов, короткий (66 слов) |
| `docs/BACKLINKS.md` | 373 | нет summary, нет тегов |
| `docs/BROKEN_LINKS.md` | 443 | нет summary, нет тегов |
| `docs/CHANGELOG.md` | 884 | нет summary, нет тегов |

## Короткие (< 100 слов, заготовки) — 38 файлов

| Файл | Слов |
|------|------|
| `docs/02-anthropic-vacancies/102-доступ-к-данным.md` | 52 |
| `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | 66 |
| `docs/02-anthropic-vacancies/16-history.md` | 90 |
| `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` | 96 |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | 94 |
| `docs/autofilled/components/.md` | 77 |
| `docs/autofilled/components/cowork.md` | 77 |
| `docs/autofilled/components/ingit.md` | 77 |
| `docs/autofilled/components/kksudo.md` | 62 |
| `docs/autofilled/components/lorenzo.md` | 77 |
| `docs/autofilled/components/nautilus.md` | 77 |
| `docs/autofilled/components/sgb.md` | 77 |
| `docs/autofilled/components/spbmolot.md` | 62 |
| `docs/autofilled/components/svend4.md` | 77 |
| `docs/autofilled/components/svyazi.md` | 77 |
| `docs/obsidian/02-anthropic-vacancies/102-доступ-к-данным.md` | 61 |
| `docs/obsidian/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | 77 |
| `docs/obsidian/02-anthropic-vacancies/16-history.md` | 97 |
| `docs/obsidian/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 38 |
| `docs/obsidian/ALERTS.md` | 80 |

## Рекомендуемые действия

```bash
# Добавить summary и теги к файлам без метаданных
python scripts/improve_summaries.py
python scripts/improve_tags.py

# Обогатить короткие файлы через LLM
python scripts/improve_llm_enrich.py --section 05-habr-projects
```
