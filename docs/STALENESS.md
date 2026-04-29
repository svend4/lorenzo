# Отчёт об устаревших документах

_Порог: 30 дней. Обновлено: 2026-04-29_

Найдено проблем: **252** файлов

## Без метаданных (нет summary или тегов) — 199 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/01-svyazi/00-intro-part2.md` | 5 | нет summary, нет тегов, короткий (5 слов) |
| `docs/01-svyazi/QA.md` | 206 | нет summary, нет тегов |
| `docs/01-svyazi/README.md` | 69 | нет тегов, короткий (69 слов) |
| `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` | 148 | нет тегов |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 14 | нет summary, нет тегов, короткий (14 слов) |
| `docs/02-anthropic-vacancies/347-твоя-миссия.md` | 110 | нет тегов |
| `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` | 178 | нет тегов |
| `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` | 77 | нет тегов, короткий (77 слов) |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | 75 | нет тегов, короткий (75 слов) |
| `docs/02-anthropic-vacancies/QA.md` | 362 | нет summary, нет тегов |
| `docs/03-technology-combinations/QA.md` | 100 | нет summary, нет тегов |
| `docs/03-technology-combinations/README.md` | 32 | нет тегов, короткий (32 слов) |
| `docs/04-ai-collaborations/QA.md` | 258 | нет summary, нет тегов |
| `docs/04-ai-collaborations/README.md` | 69 | нет тегов, короткий (69 слов) |
| `docs/05-habr-projects/QA.md` | 111 | нет summary, нет тегов |
| `docs/05-habr-projects/README.md` | 32 | нет тегов, короткий (32 слов) |
| `docs/05-habr-projects/knowledge/README.md` | 10 | нет summary, нет тегов, короткий (10 слов) |
| `docs/05-habr-projects/memory/README.md` | 18 | нет summary, нет тегов, короткий (18 слов) |
| `docs/ABBREVIATIONS.md` | 1111 | нет summary, нет тегов |
| `docs/ACTION_ITEMS.md` | 5511 | нет summary |

## Короткие (< 100 слов, заготовки) — 53 файлов

| Файл | Слов |
|------|------|
| `docs/02-anthropic-vacancies/120-главные-технические-риски.md` | 68 |
| `docs/02-anthropic-vacancies/348-кому-ты-служишь-слоистая-модель.md` | 90 |
| `docs/02-anthropic-vacancies/360-что-ты-всегда-делаешь.md` | 89 |
| `docs/SEARCH_RESULTS.md` | 47 |
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

## Рекомендуемые действия

```bash
# Добавить summary и теги к файлам без метаданных
python scripts/improve_summaries.py
python scripts/improve_tags.py

# Обогатить короткие файлы через LLM
python scripts/improve_llm_enrich.py --section 05-habr-projects
```
