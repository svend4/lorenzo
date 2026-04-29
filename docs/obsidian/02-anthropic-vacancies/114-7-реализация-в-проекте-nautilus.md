---
title: "7. Реализация в проекте Nautilus"
tags:
  - orchestration
  - architecture
  - roadmap
  - anthropic-vacancies
date: 2026-04-29
---

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
- [[108-2-формальный-workflow]] (сходство 0.18)
- [[117-10-конкретный-план-применения-к-текущим-документам]] (сходство 0.14)
- [[05-0-status-of-this-document]] (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [[108-2-формальный-workflow]]
- [[117-10-конкретный-план-применения-к-текущим-документам]]
- [[05-0-status-of-this-document]]
- [[24-12-versioning-policy]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[108-2-формальный-workflow|2. Формальный workflow]] _48%_
- [[117-10-конкретный-план-применения-к-текущим-документам|10. Конкретный план применения к текущим документам]] _48%_
- [[42-author-contact|Author & Contact]] _25%_
- [[05-0-status-of-this-document|0. Status of This Document]] _21%_
- [[122-глоссарий|Глоссарий]] _21%_
- [[129-примеры-запросов-в-claude|Примеры запросов (в Claude)]] _21%_
- [[62-author-contact|Author & Contact]] _21%_
- [[75-0-status-of-this-document|0. Status of This Document]] _21%_
