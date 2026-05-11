# 7. Реализация в проекте Nautilus

<!-- toc-auto -->
## Contents

- [7. Реализация в проекте Nautilus](#7-реализация-в-проекте-nautilus)
  - [7.1. Хронология применения](#71-хронология-применения)
  - [7.2. Артефакты](#72-артефакты)
  - [7.3. Интеграция с Nautilus Portal Protocol](#73-интеграция-с-nautilus-portal-protocol)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Трёхфазная методология Review в Nautilus».

---
<!-- tags: orchestration, architecture, roadmap, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Трёхфазная методология Review в Nautilus».

## 7. Реализация в проекте Nautilus

### 7.1. Хронология применения

**Первое применение — IMPLEMENTATION_STAGE_PART_[1-4].md** 
(апрель 2026):

- Вариант A: ветка `claude/review-nautilus-changes-tdywx`
- Вариант B: ветка `claude/project-implementation-stage-CzylE`
- Текущий статус: Merged-to-main with parallel blocks, Фаза C не 
пройдена

**Повторное применение — STATUS.md** (апрель 2026):

- Пройдена Фаза A единожды (single-pass)
- Статус: канонично, трёхфазная методология не применялась
- Осмысленность: документ достаточно простой для single-pass

Пример, что **методология применяется селективно**, только там, 
где польза оправдывает overhead.

### 7.2. Артефакты

Для каждого документа, прошедшего через методологию, в репо 
сохраняются:

1. **Исходные draft ветки** (`claude/*`) — как audit trail
2. **Merged-to-main с header warning** — текущее состояние
3. **Финальная консолидированная** — после Фазы C

Удалять исходные ветки **не следует** до завершения Фазы C — они 
могут содержать контекст, нужный для разрешения неочевидных 
расхождений.

### 7.3. Интеграция с Nautilus Portal Protocol

NPP v1.1 §17.3 «Breaking Changes Process» упоминает RFC-процесс 
для major version bump. Трёхфазная методология — **неофициальный 
аналог** RFC для документов, не затрагивающих протокол formally, 
но имеющих высокую ценность (STATUS, IMPLEMENTATION_STAGE, 
итд).

В будущем методология может быть формализована в NPP v2.0 как 
рекомендованный workflow для community-contributed documentation.

---

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "7 Реализация в проекте Nautilus"
```

## Смотрите также
- [114-7-реализация-в-проекте-nautilus](../../02-anthropic-vacancies/114-7-реализация-в-проекте-nautilus.md)
- [02-formal-workflow](02-formal-workflow.md)
- [11-application-plan-current-docs](11-application-plan-current-docs.md)
- [108-2-формальный-workflow](../../02-anthropic-vacancies/108-2-формальный-workflow.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (7):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [02-formal-workflow](02-formal-workflow.md)
- [11-application-plan-current-docs](11-application-plan-current-docs.md)
- [README](README.md)

