---
title: "Прогресс MVP"
tags:
  - progress
  - docs
  - general
date: 2026-05-11
---

# Прогресс MVP

<!-- toc-auto -->

> [!NOTE]
> Раздел `PROGRESS` формируется автоматически из данных репозитория.

<!-- alert-added -->
<!-- tags: progress, docs -->


<!-- summary -->
> `PROGRESS` — раздел документации проекта Lorenzo.


_Обновлено: 2026-05-11 (improve_progress_sync.py)_

## Ключевые этапы (Milestones)

`████████████░░░░░░░░ 63%` 7/11

✅ Определена архитектура Svyazi 2.0
✅ Составлен каталог 20+ компонентов
✅ Выявлены 5 ансамблей
✅ Описаны интеграционные контракты
✅ Составлены контакты авторов
⬜ Написаны авторам ключевых компонентов
⬜ Получены ответы от авторов
⬜ LLM-обогащение проектных файлов
✅ Создан рабочий прототип Knowledge OS
✅ Пройдено тестирование компонентов
⬜ Опубликован MVP на GitHub

## Состояние компонентов

| Компонент | Статус | Детали |
|-----------|--------|--------|
| Контакты авторов | ⚠️ 16 файлов, не отправлено | 16 файлов в docs/contacts/ |
| LLM-обогащение | ⬜ не запущено | pip install anthropic && python scripts/improve_llm_enrich.py |
| Скрипты обработки | ✅ 165 скриптов | 5 LLM-скриптов, MCP=✅ |
| DIGEST.md | ✅ 7 секций | python scripts/improve_llm_summary.py |
| Claude Skills | ✅ 28 скиллов | analyze-project, write-contact, review-docs, improve, и др. |
| Lorenzo Gateway | ✅ Итерация 4 | scripts/gateway.py — OpenAI-compatible FastAPI, 5 инструментов |
| hnswlib ANN-граф | ✅ Итерация 1 | scripts/improve_ann_index.py — 37× speedup, Hit Rate@10=0.75 |
| Review Queue UI | ✅ Итерация 1 | scripts/review_queue.py — Streamlit, approve/reject/defer |
| Тесты компонентов | ✅ 43 теста | tests/test_gateway.py (25) + tests/test_ann_index.py (18) |
| Precision eval | ✅ PASS | scripts/improve_precision_eval.py — Hit Rate@10 = 0.75 ≥ 0.70 |

## Метрики качества

| Метрика | Балл | Статус |
|---------|------|--------|
| Здоровье репо (HEALTH) | 100.0/100 | 🟢 |
| Качество доков (METRICS) | 100.0/100 | 🟢 |
| Go/No-Go (SCORING) | 100.0/100 | 🟢 |

## Следующий шаг

➡️ **Написаны авторам ключевых компонентов**

_Написали: 0/16_

Контактные файлы готовы. Откройте и отправьте:

```bash
# Приоритет 1: kksudo (AgentFS, 13 упоминаний)
cat docs/contacts/kksudo.md

# Приоритет 2: spbmolot (NGT Memory, 12 упоминаний)
cat docs/contacts/spbmolot.md

# Приоритет 3: AnastasiyaW (knowledge-space, 11 упоминаний)
cat docs/contacts/anastasiyaw.md
```

## Связанные документы

- [[CONTACTS|Контакты авторов]]
- [[SCORING|Go/No-Go Scoring]]
- [[HEALTH|Health Dashboard]]
- [[07-mvp-planning|MVP Planning]]

<!-- auto-end -->



## Открытые письма авторам

Черновики писем подготовлены для 8 авторов — [[README|docs/letters/]]:

| Письмо | Автор | Статус |
|--------|-------|--------|
| [[kksudo|kksudo.md]] | AgentFS | ✅ Изучен, письмо готово |
| [[spbmolot|spbmolot.md]] | NGT Memory | ✅ Изучен, письмо готово |
| [[vitalyoborin|vitalyoborin.md]] | Yodoca + Wikontic | ✅ Изучен, письмо готово |
| [[anastasiyaw|anastasiyaw.md]] | knowledge-space + mclaude | ✅ Изучен, письмо готово |
| [[nlaik|nlaik.md]] | LiteParse | ✅ Изучен, письмо готово |
| [[zodigancode|zodigancode.md]] | Rufler | ✅ Изучен, письмо готово |
| [[antipozitive|antipozitive.md]] | MemNet | ✅ Изучен, письмо готово |
| [[vitalysemenov|vitalysemenov.md]] | agent-memory-mcp | ✅ Изучен, письмо готово |

## Что было сделано (журнал сессий)

### Сессия 2026-05-11 — Стабилизация + Письма

**Инфраструктура:**
- `improve_quality_patch.py` — идемпотентный патч качества, предотвращает регрессии
- Исправлен баг U+2011 (не-разрывный дефис) в anchor-генераторах
- Исправлена формула TOC-баллов для файлов < 300 слов
- Устранено загрязнение ссылками в 5 генераторах

**Контент:**
- `docs/letters/` — 8 персонализированных открытых писем авторам проектов
- PROGRESS.md обновлён с журналом изменений и текущей стадией

**Результат:** 100.0/100 по 1221 файлу, 0 сломанных ссылок, 0 orphans.

### Сессия 2026-05-11 — Gateway + ANN + Тесты + Precision Eval

**Новые компоненты:**
- `scripts/gateway.py` — Lorenzo Gateway: OpenAI-compatible FastAPI, 5 инструментов,
  write-back (POST /api/cards), гибридный поиск + опциональный ANN, LLM-синтез
- `docs/GATEWAY.md` — полная документация gateway с примерами, таблицей vs DAF
- `scripts/improve_ann_index.py` — hnswlib HNSW ANN-индекс, 37× speedup vs TF-IDF,
  random projection (6000→256 dim), двухстадийный поиск (ANN + exact re-rank)
- `scripts/review_queue.py` — Streamlit Review Queue UI (approve/reject/defer)

**Тесты:**
- `tests/test_gateway.py` — 25 тестов FastAPI (health, status, ask, cards, completions)
- `tests/test_ann_index.py` — 18 тестов ANN (vocab, files, search, speed)

**Оценка качества:**
- `scripts/improve_precision_eval.py` — автоматическая оценка Hit Rate@K
  - Hit Rate@10 = 0.75 ≥ 0.70 ✅ PASS
  - Mean MRR = 0.419, шум фильтруется (obsidian/, autofilled/, TABLES.md и др.)
  - Метрика исправлена: Hit Rate@K вместо P@K (P@K с 1 релевантным doc ≤ 1/K)

### Сессия 2026-05-11 — SENTINEL + Контакты + Защита PROGRESS.md

**Инфраструктура:**
- `improve_sentinel_check.py` — SENTINEL security audit: PII, unsafe code, credentials,
  HTTP-ссылки, лицензионные риски. Итог: 0 критических проблем. Добавлен в группу `quality`.
- `improve_progress_sync.py` — добавлена защита ручных секций через маркер `<!-- auto-end -->`.
  Теперь скрипт сохраняет журнал и текущую стадию при каждом запуске.
- `improve_recipe.py` — исправлен `__import__('datetime')` → корректный import.

**Контакты:**
- 8 авторов отмечены как `studied` (письмо готово).
- PROTOTYPE_SPEC: SENTINEL-check ✅ (Итерация 2: 4/5 задач).

## Текущая стадия — Итерация 4 Gateway & Enrichment (63%)

| Подзадача | Статус |
|-----------|--------|
| CI daily pipeline | ✅ Настроен |
| Инкрементальная сборка CardStore | ✅ < 3 сек |
| Orphan rate < 15% | ✅ 0/2162 |
| Качество документации 100/100 | ✅ Стабильно |
| Открытые письма 8 авторам | ✅ Готовы к отправке |
| SENTINEL security check | ✅ (`improve_sentinel_check.py`) |
| Lorenzo Gateway (Итерация 4) | ✅ `scripts/gateway.py` + `docs/GATEWAY.md` |
| hnswlib ANN-граф (Итерация 1) | ✅ `scripts/improve_ann_index.py`, speedup 37× |
| Review Queue UI (Итерация 1) | ✅ `scripts/review_queue.py` |
| Тесты gateway + ANN | ✅ 43 теста в `tests/` |
| Hit Rate@10 ≥ 0.70 (Итерация 4) | ✅ 0.75 (`improve_precision_eval.py`) |
| Yodoca decay_event API | ⬜ Ожидает ответа автора |

**Следующий приоритет:**
1. Отправить письма → kksudo → spbmolot → AnastasiyaW → VitalyOborin → nlaik
2. LLM-обогащение проектных файлов (`ANTHROPIC_API_KEY`)
3. Опубликовать MVP на GitHub (README + docs)

## Связанные документы

- [[README|Открытые письма]]
- [[CONTACTS|Контакты авторов]]
- [[SCORING|Go/No-Go Scoring]]
- [[HEALTH|Health Dashboard]]
- [[07-mvp-planning|MVP Planning]]
