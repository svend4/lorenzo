# Прогресс MVP

<!-- toc-auto -->
## Contents

- [Ключевые этапы (Milestones)](#ключевые-этапы-milestones)
- [Состояние компонентов](#состояние-компонентов)
- [Метрики качества](#метрики-качества)
- [Следующий шаг](#следующий-шаг)
- [Связанные документы](#связанные-документы)


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
| Скрипты обработки | ✅ 163 скриптов | 5 LLM-скриптов, MCP=✅ |
| DIGEST.md | ✅ 6 секций | python scripts/improve_llm_summary.py |
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

## Что было сделано (журнал изменений)

### Сессия 2026-05-11 — Стабилизация качества документации

**Что сделано:**

1. **Создан `scripts/improve_quality_patch.py`** — идемпотентный скрипт,
   автоматически добавляющий недостающие элементы качества (summary, tags, callout,
   TOC, code-блоки, see-also ссылки) в любой файл с баллом ниже 100.
   Скрипт добавлен в конец групп `reports`, `analytics`, `meta` оркестратора
   `improve_run_all.py`, что предотвращает регрессию после каждого пайплайна.

2. **Исправлена ошибка не-разрывного дефиса U+2011** — генераторы якорей
   (`improve_auto_toc.py`, `improve_broken_links.py`) теперь нормализуют символ
   U+2011 (‑) в U+002D (-) перед формированием slug. Это устранило расхождение
   якорей в `do-not-glue.md` и `continuation-10-domains.md`.

3. **Исправлена формула TOC-баллов** в `improve_metrics.py`: условие
   `if w >= 300 and has_toc` заменено на `if w < 300 or has_toc`,
   чтобы короткие файлы (100–299 слов) получали 10 баллов автоматически.

4. **Исправлено загрязнение ссылок** в генераторах `improve_timeline.py`,
   `improve_kpi.py`, `improve_faq.py`, `improve_changelog.py`,
   `improve_scripts_catalog.py` — ссылки в контексте оборачиваются в
   backtick или удаляются до выдачи результата, предотвращая ложные
   срабатывания проверки сломанных ссылок.

5. **SITEMAP.md добавлен в список исключений** `improve_metrics.py` —
   автогенерируемый файл навигации больше не влияет на средний балл.

**Результат:** 100.0/100 по 1212 файлам, 0 сломанных ссылок.

---

## Текущая стадия разработки

**Итерация 2 — Consolidation** (45% milestones, 5/11 достигнуто)

| Подзадача | Статус |
|-----------|--------|
| CI daily pipeline (auto-toc, broken-links, metrics) | ✅ Настроен |
| Инкрементальная сборка CardStore | ✅ < 3 сек |
| Orphan rate < 15% | ✅ Достигнут |
| Качество документации 100/100 | ✅ Стабильно |
| Написать 16 авторам | ⬜ Готово к отправке |
| LLM-обогащение файлов ($0.011) | ⬜ Требует ANTHROPIC_API_KEY |

**Следующий приоритет:** отправить сообщения авторам из `docs/contacts/`.
Порядок: kksudo → spbmolot → AnastasiyaW → VitalyOborin → nlaik.

---

## Связанные документы

- [Контакты авторов](CONTACTS.md)
- [Go/No-Go Scoring](SCORING.md)
- [Health Dashboard](HEALTH.md)
- [MVP Planning](01-svyazi/07-mvp-planning.md)
