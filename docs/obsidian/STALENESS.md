---
title: "Отчёт об устаревших документах"
tags:
  - general
date: 2026-04-29
---

# Отчёт об устаревших документах

_Порог: 30 дней. Обновлено: 2026-04-29_

Найдено проблем: **258** файлов

## Без метаданных (нет summary или тегов) — 169 файлов

| Файл | Слов | Проблемы |
|------|------|---------|
| `docs/01-svyazi/00-intro-part2.md` | 5 | нет summary, нет тегов, короткий (5 слов) |
| `docs/01-svyazi/QA.md` | 255 | нет summary, нет тегов |
| `docs/01-svyazi/README.md` | 83 | нет тегов, короткий (83 слов) |
| `docs/02-anthropic-vacancies/102-доступ-к-данным.md` | 20 | нет summary, нет тегов, короткий (20 слов) |
| `docs/02-anthropic-vacancies/113-6-почему-это-валидный-паттерн-для-ai-assisted-work.md` | 148 | нет тегов |
| `docs/02-anthropic-vacancies/121-appendix-c-история-изменений-методологии.md` | 41 | нет тегов, короткий (41 слов) |
| `docs/02-anthropic-vacancies/185-appendix-b-domain-comparison-matrix.md` | 91 | нет summary, нет тегов, короткий (91 слов) |
| `docs/02-anthropic-vacancies/202-12-заключение.md` | 179 | нет тегов |
| `docs/02-anthropic-vacancies/206-приложение-b-матрица-сравнения-областей.md` | 93 | нет summary, нет тегов, короткий (93 слов) |
| `docs/02-anthropic-vacancies/250-bridging-the-gap-between-profession-wide-and-indiv.md` | 14 | нет summary, нет тегов, короткий (14 слов) |
| `docs/02-anthropic-vacancies/339-приложение-a-дерево-решений-для-принимающих-ingit.md` | 140 | нет тегов |
| `docs/02-anthropic-vacancies/347-твоя-миссия.md` | 110 | нет тегов |
| `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` | 178 | нет тегов |
| `docs/02-anthropic-vacancies/361-когда-ты-honestly-не-знаешь.md` | 77 | нет тегов, короткий (77 слов) |
| `docs/02-anthropic-vacancies/362-когда-сомневаешься-escalate-к-max.md` | 75 | нет тегов, короткий (75 слов) |
| `docs/02-anthropic-vacancies/QA.md` | 362 | нет summary, нет тегов |
| `docs/03-technology-combinations/QA.md` | 146 | нет summary, нет тегов |
| `docs/03-technology-combinations/README.md` | 38 | нет тегов, короткий (38 слов) |
| `docs/04-ai-collaborations/QA.md` | 258 | нет summary, нет тегов |
| `docs/04-ai-collaborations/README.md` | 78 | нет summary, нет тегов, короткий (78 слов) |

## Короткие (< 100 слов, заготовки) — 89 файлов

| Файл | Слов |
|------|------|
| `docs/02-anthropic-vacancies/03-portal-protocol-md.md` | 65 |
| `docs/02-anthropic-vacancies/05-0-status-of-this-document.md` | 92 |
| `docs/02-anthropic-vacancies/105-review-methodology-md.md` | 64 |
| `docs/02-anthropic-vacancies/12-content-overview.md` | 29 |
| `docs/02-anthropic-vacancies/120-главные-технические-риски.md` | 68 |
| `docs/02-anthropic-vacancies/125-readme-mcp-md-инструкция-по-установке.md` | 88 |
| `docs/02-anthropic-vacancies/13-angle-perspective.md` | 58 |
| `docs/02-anthropic-vacancies/131-ограничения-текущей-версии-0-1-0-draft.md` | 88 |
| `docs/02-anthropic-vacancies/132-planned-v0-2-0.md` | 62 |
| `docs/02-anthropic-vacancies/134-the-double-triangle-architecture-md.md` | 35 |
| `docs/02-anthropic-vacancies/135-a-formal-model-for-human-ai-collaboration-in-distr.md` | 82 |
| `docs/02-anthropic-vacancies/137-table-of-contents.md` | 85 |
| `docs/02-anthropic-vacancies/151-open-knowledge-work-foundation-md.md` | 38 |
| `docs/02-anthropic-vacancies/152-ai-coordinated-infrastructure-for-distributed-expe.md` | 77 |
| `docs/02-anthropic-vacancies/154-table-of-contents.md` | 70 |
| `docs/02-anthropic-vacancies/16-history.md` | 71 |
| `docs/02-anthropic-vacancies/166-representative-agent-layer-md.md` | 36 |
| `docs/02-anthropic-vacancies/167-ai-mediated-representation-for-underrepresented-ex.md` | 99 |
| `docs/02-anthropic-vacancies/187-слой-представительских-агентов-md.md` | 35 |
| `docs/02-anthropic-vacancies/190-содержание.md` | 88 |

## Рекомендуемые действия

```bash
# Добавить summary и теги к файлам без метаданных
python scripts/improve_summaries.py
python scripts/improve_tags.py

# Обогатить короткие файлы через LLM
python scripts/improve_llm_enrich.py --section 05-habr-projects
```
