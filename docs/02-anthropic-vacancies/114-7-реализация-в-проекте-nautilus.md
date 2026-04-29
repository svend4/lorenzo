# 7. Реализация в проекте Nautilus

<!-- toc-auto -->
## Contents

- [7. Реализация в проекте Nautilus](#7-реализация-в-проекте-nautilus)
  - [7.1. Хронология применения](#71-хронология-применения)
  - [7.2. Артефакты](#72-артефакты)
  - [7.3. Интеграция с Nautilus Portal Protocol](#73-интеграция-с-nautilus-portal-protocol)


<!-- summary -->
> **Первое применение — IMPLEMENTATION_STAGE_PART_[1-4].md**

---
<!-- tags: orchestration, architecture, roadmap -->




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

<!-- similar-docs -->

---

**Похожие документы:**
- [108-2-формальный-workflow](108-2-формальный-workflow.md) (сходство 0.18)
- [117-10-конкретный-план-применения-к-текущим-документам](117-10-конкретный-план-применения-к-текущим-документам.md) (сходство 0.14)
- [05-0-status-of-this-document](05-0-status-of-this-document.md) (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [108-2-формальный-workflow](108-2-формальный-workflow.md)
- [117-10-конкретный-план-применения-к-текущим-документам](117-10-конкретный-план-применения-к-текущим-документам.md)
- [05-0-status-of-this-document](05-0-status-of-this-document.md)
- [24-12-versioning-policy](24-12-versioning-policy.md)

<!-- backlinks-auto -->
## Упоминается в

- [10. Конкретный план применения к текущим документам](117-10-конкретный-план-применения-к-текущим-документам.md)
- [2. Формальный workflow](108-2-формальный-workflow.md)
- [4. Условия применимости](111-4-условия-применимости.md)
- [8. Ограничения и открытые вопросы](115-8-ограничения-и-открытые-вопросы.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
- [Примеры запросов (в Claude)](129-примеры-запросов-в-claude.md)
- [⬡](69-section.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [2. Формальный workflow](108-2-формальный-workflow.md) _37%_
- [10. Конкретный план применения к текущим документам](117-10-конкретный-план-применения-к-текущим-документам.md) _37%_
- [0. Status of This Document](05-0-status-of-this-document.md) _25%_
- [13. Reference Implementation](25-13-reference-implementation.md) _25%_
- [Author & Contact](42-author-contact.md) _25%_
- [0. Status of This Document](75-0-status-of-this-document.md) _25%_
- [18. Reference Implementation](93-18-reference-implementation.md) _25%_
- [4. Условия применимости](111-4-условия-применимости.md) _21%_
## Связанные документы

- [2. Формальный workflow](108-2-формальный-workflow.md) _48%_
- [10. Конкретный план применения к текущим документам](117-10-конкретный-план-применения-к-текущим-документам.md) _48%_
- [Author & Contact](42-author-contact.md) _25%_
- [0. Status of This Document](05-0-status-of-this-document.md) _21%_
- [Глоссарий](122-глоссарий.md) _21%_
- [Примеры запросов (в Claude)](129-примеры-запросов-в-claude.md) _21%_
- [Author & Contact](62-author-contact.md) _21%_
- [0. Status of This Document](75-0-status-of-this-document.md) _21%_
