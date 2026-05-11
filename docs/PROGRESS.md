# Прогресс MVP

<!-- toc-auto -->
## Contents

- [Ключевые этапы (Milestones)](#ключевые-этапы-milestones)
- [Состояние компонентов](#состояние-компонентов)
- [Метрики качества](#метрики-качества)
- [Следующий шаг](#следующий-шаг)
- [Связанные документы](#связанные-документы)
- [Открытые письма авторам](#открытые-письма-авторам)
- [Что было сделано (журнал сессий)](#что-было-сделано-журнал-сессий)
  - [Сессия 2026-05-11 — Стабилизация + Письма](#сессия-2026-05-11-стабилизация-письма)
  - [Сессия 2026-05-11 — SENTINEL + Контакты + Защита PROGRESS.md](#сессия-2026-05-11-sentinel-контакты-защита-progressmd)
- [Текущая стадия — Итерация 2 Consolidation (55%)](#текущая-стадия-итерация-2-consolidation-55)
- [Связанные документы](#связанные-документы-1)



> [!NOTE]
> Раздел `PROGRESS` формируется автоматически из данных репозитория.

<!-- alert-added -->
<!-- tags: progress, docs -->


<!-- summary -->
> `PROGRESS` — раздел документации проекта Lorenzo.


_Обновлено: 2026-05-11 (improve_progress_sync.py)_

## Ключевые этапы (Milestones)

`█████████░░░░░░░░░░░ 45%` 5/11

✅ Определена архитектура Svyazi 2.0
✅ Составлен каталог 20+ компонентов
✅ Выявлены 5 ансамблей
✅ Описаны интеграционные контракты
✅ Составлены контакты авторов
⬜ Написаны авторам ключевых компонентов
⬜ Получены ответы от авторов
⬜ LLM-обогащение проектных файлов
⬜ Создан рабочий прототип Knowledge OS
⬜ Пройдено тестирование ансамбля
⬜ Опубликован MVP на GitHub

## Состояние компонентов

| Компонент | Статус | Детали |
|-----------|--------|--------|
| Контакты авторов | ⚠️ 16 файлов, не отправлено | 16 файлов в docs/contacts/ |
| LLM-обогащение | ⬜ не запущено | pip install anthropic && python scripts/improve_llm_enrich.py |
| Скрипты обработки | ✅ 164 скриптов | 5 LLM-скриптов, MCP=✅ |
| DIGEST.md | ✅ 7 секций | python scripts/improve_llm_summary.py |
| Claude Skills | ✅ 28 скиллов | track-decisions, new-research, review-docs, search, dispatch, status, evaluate-tech, compare, synthesize, find-gaps, summarize, outreach-day, propose-mega-stack, evaluate-skill, find-cinderella, skill-router, weekly-review, plan-mvp, write-contact, improve, propose-collaboration, find-contradictions, audit-corpus, review-architecture, generate-rfc, design-ensemble, analyze-project, daily-routine |

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

- [Контакты авторов](CONTACTS.md)
- [Go/No-Go Scoring](SCORING.md)
- [Health Dashboard](HEALTH.md)
- [MVP Planning](01-svyazi/07-mvp-planning.md)

<!-- auto-end -->


## Открытые письма авторам

Черновики писем подготовлены для 8 авторов — [docs/letters/](letters/README.md):

| Письмо | Автор | Статус |
|--------|-------|--------|
| [kksudo.md](letters/kksudo.md) | AgentFS | ✅ Изучен, письмо готово |
| [spbmolot.md](letters/spbmolot.md) | NGT Memory | ✅ Изучен, письмо готово |
| [vitalyoborin.md](letters/vitalyoborin.md) | Yodoca + Wikontic | ✅ Изучен, письмо готово |
| [anastasiyaw.md](letters/anastasiyaw.md) | knowledge-space + mclaude | ✅ Изучен, письмо готово |
| [nlaik.md](letters/nlaik.md) | LiteParse | ✅ Изучен, письмо готово |
| [zodigancode.md](letters/zodigancode.md) | Rufler | ✅ Изучен, письмо готово |
| [antipozitive.md](letters/antipozitive.md) | MemNet | ✅ Изучен, письмо готово |
| [vitalysemenov.md](letters/vitalysemenov.md) | agent-memory-mcp | ✅ Изучен, письмо готово |

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

## Текущая стадия — Итерация 2 Consolidation (55%)

| Подзадача | Статус |
|-----------|--------|
| CI daily pipeline | ✅ Настроен |
| Инкрементальная сборка CardStore | ✅ < 3 сек |
| Orphan rate < 15% | ✅ 0/2162 |
| Качество документации 100/100 | ✅ Стабильно |
| Открытые письма 8 авторам | ✅ Готовы к отправке |
| SENTINEL security check | ✅ Реализован (`improve_sentinel_check.py`) |
| Yodoca decay_event API | ⬜ Ожидает ответа автора |

**Следующий приоритет:**
1. Отправить письма → kksudo → spbmolot → AnastasiyaW → VitalyOborin → nlaik
2. LLM-обогащение проектных файлов (`ANTHROPIC_API_KEY`)
3. Рабочий прототип Knowledge OS (Итерация → Итерация 3)

## Связанные документы

- [Открытые письма](letters/README.md)
- [Контакты авторов](CONTACTS.md)
- [Go/No-Go Scoring](SCORING.md)
- [Health Dashboard](HEALTH.md)
- [MVP Planning](01-svyazi/07-mvp-planning.md)
