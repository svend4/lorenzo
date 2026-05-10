# 7. Реализация в проекте Nautilus

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

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

- Вариант A: ветка `claude/review-[nautilus](../05-habr-projects/memory/memnet.md)-changes-tdywx`
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


<!-- backlinks -->

---

**Кто ссылается на этот документ (9):**
- [05-0-status-of-this-document](05-0-status-of-this-document.md)
- [122-глоссарий](122-глоссарий.md)
- [129-примеры-запросов-в-claude](129-примеры-запросов-в-claude.md)
- [24-12-versioning-policy](24-12-versioning-policy.md)
- [42-author-contact](42-author-contact.md)
- [53-history](53-history.md)
- [62-author-contact](62-author-contact.md)
- [75-0-status-of-this-document](75-0-status-of-this-document.md)
- _...ещё 1_

