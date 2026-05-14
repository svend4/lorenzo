---
title: "7. PortalEntry Structure"
tags:
  - memory
  - ingestion
  - architecture
  - anthropic
  - collaboration
  - anthropic-vacancies
date: 2026-05-14
---

# 7. PortalEntry Structure

<!-- toc-auto -->
## Contents

- [7. PortalEntry Structure](#7-portalentry-structure)
  - [7.1. Field Semantics](#71-field-semantics)
- [Похожие документы](#похожие-документы)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (6)](#кто-ссылается-на-этот-документ-6)


- 7. [PortalEntry Structure](#7-portalentry-structure)
  - [7.1. Field Semantics](#71-field-semantics)

<!-- tags: memory, ingestion, architecture, anthropic, collaboration -->


<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** PortalEntry Structure !IMPORTANT Ключевой документ для понимания архитектуры.
> 🔧 **Подход:** PortalEntry Structure !IMPORTANT Ключевой документ для понимания архитектуры.
> 🏷️ **Ключевые слова:** `portalentry`, `structure`, `anthropic`, `vacancies`, `данных`, `registry`, `summary`, `унифицированная`
>


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> * PortalEntry Structure !IMPORTANT Ключевой документ для понимания архитектуры. * PortalEntry Structure !IMPORTANT Ключевой документ для понимания архитектуры
 
 
> Абстракт (авто)
>
> 🎯 Проблема: PortalEntry Structure !IMPORTANT Ключевой документ для понимания архитектуры.

---



## 7. PortalEntry Structure

Унифицированная структура данных, возвращаемая адаптерами.

```python
class PortalEntry:
    repo_name: str           # REQUIRED: откуда пришло
    native_id: str           # REQUIRED: id в native формате
    title: str               # REQUIRED: человекочитаемое имя
    summary: str             # REQUIRED: до 280 символов
    content: str             # REQUIRED: полный текст
    tags: list[str]          # OPTIONAL: ключевые слова
    confidence: float        # OPTIONAL: 0.0–1.0, default 1.0
    native_metadata: dict    # OPTIONAL: любые native-специфичные поля
    url: str | None          # OPTIONAL: прямая ссылка на источник
```

### 7.1. Field Semantics

- `repo_name` MUST совпадать с `name` в registry
- `native_id` MUST быть уникален в пределах Repo
- `title` SHOULD быть до 120 символов
- `summary` MUST быть до 280 символов (для предпросмотров)
- `content` MAY быть большим, но implementation MAY trimming при 
  transport
- `confidence` — субъективная оценка адаптера о релевантности entry 
  к query
- `native_metadata` — escape hatch для данных, не ложащихся в 
  стандартные поля

---

<!-- similar-docs -->

---

## Похожие документы
- [[82-7-portalentry-structure]] (сходство 0.25)


<!-- see-also -->

---

## Смотрите также
- [[82-7-portalentry-structure]]
- 123-portal-[[123-portal-mcp-py|mcp-py]]
- [[memnet|08-3-registry-[nautilus]]-json](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md)
- [[81-6-adapter-interface]]


<!-- backlinks -->

---

## Кто ссылается на этот документ (6)
- [[109-3-принципы-консолидации-фаза-c]]
- 123-portal-[[123-portal-mcp-py|mcp-py]]
- [[18-6-adapter-interface]]
- [[23-11-security-considerations]]
- [[74-abstract]]
- [[README]]

