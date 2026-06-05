---
title: "7. PortalEntry Structure"
tags:
  - ingestion
  - architecture
  - collaboration
  - anthropic-vacancies
date: 2026-06-05
---

# 7. PortalEntry Structure

<!-- toc-auto -->
## Contents

- [7. PortalEntry Structure](#7-portalentry-structure)
  - [7.1. Field Semantics](#71-field-semantics)
  - [7.2. Q6 Metadata](#72-q6-metadata)
- [Похожие документы](#похожие-документы)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (7)](#кто-ссылается-на-этот-документ-7)


<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** PortalEntry Structure(7-portalentry-structure) - 7.1.
> 🔧 **Подход:** Q6 Metadata(72-q6-metadata) !IMPORTANT Ключевой документ для понимания архитектуры.
> ✅ **Результат:** Implementation MAY расширять список - content — полный текст/представление, MAY быть большим - metadata — MUST содержать q6 для Level 2+ адаптеров - links — список id из других Rep
> 🏷️ **Ключевые слова:** `portalentry`, `structure`, `anthropic`, `vacancies`, `metadata`, `format`, `adapter`, `interface`
>


  - [7.1. Field Semantics](#71-field-semantics)
  - [7.2. Q6 Metadata](#72-q6-metadata)
- 7. [PortalEntry Structure](#7-portalentry-structure)
  - [7.1. Field Semantics](#71-field-semantics)
  - [7.2. Q6 Metadata](#72-q6-metadata)
- 7. [PortalEntry Structure](#7-portalentry-structure)
  - [7.1. Field Semantics](#71-field-semantics)
  - [7.2. Q6 Metadata](#72-q6-metadata)
- 7. [PortalEntry Structure](#7-portalentry-structure)
  - [7.1. Field Semantics](#71-field-semantics)
  - [7.2. Q6 Metadata](#72-q6-metadata)
> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> * PortalEntry Structure - 7.1. * Q6 Metadata !IMPORTANT Ключевой документ для понимания архитектуры 🎯 Проблема: PortalEntry Structure - 7.1. 🔧 Подход: Q6 Metadata !IMPORTANT Ключевой документ для понимания архитектуры.
 — полный текст/представление, MAY быть большим
 — MUST содержать   для Level 2+ адаптеров
 — список id из других Repos, формат   
  или   (например,  , 
   )
 — Boolean, MUST быть   для fallback-entries, 
    (def

---
<!-- tags: ingestion, architecture, collaboration -->


## 7. PortalEntry Structure

Унифицированная структура данных, возвращаемая адаптерами.

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass
class PortalEntry:
    id: str                              # REQUIRED: "format:slug"
    title: str                           # REQUIRED: human-readable
    source: str                          # REQUIRED: owner/repo-name
    format_type: str                     # REQUIRED: concept type
    content: str                         # REQUIRED: full text
    metadata: dict[str, Any] = field(default_factory=dict)
    links: list[str] = field(default_factory=list)
    is_fallback: bool = False
```

### 7.1. Field Semantics

- `id` MUST быть уникален в пределах экосистемы. Формат: 
  `"<format>:<slug>"` (например, `"[[01-интегральный-анализ-профиля-svend4|info1]]:alpha-3-doc-1"`)
- `title` SHOULD быть до 120 символов
- `source` — [[03-component-catalog|GitHub]] slug `owner/repo-name`
- `format_type` — one of: `document`, `concept`, `rule`, `theory`, 
  `schema`, `archetype`. Implementation MAY расширять список
- `content` — полный текст/представление, MAY быть большим
- `metadata` — MUST содержать `q6` для Level 2+ адаптеров
- `links` — список id из других Repos, формат `"<format>:<type>:<id>"` 
  или `"<format>:<id>"` (например, `"[[01-интегральный-анализ-профиля-svend4|pro2]]:q6:010011"`, 
  `"meta:hexagram:50"`)
- `is_fallback` — Boolean, MUST быть `True` для fallback-entries, 
  `False` (default) для real fetch results

### 7.2. Q6 Metadata

Для адаптеров Level 2+, каждый [[01-интегральный-анализ-профиля-svend4|PortalEntry]] MUST содержать 
`metadata["q6"]` — 6-битную строку длиной 6, только символы `"0"` 
и `"1"`.

Пример:
```python
PortalEntry(
    id="info1:synthesis",
    title="Синтез",
    source="svend4/info1",
    format_type="concept",
    content="...",
    metadata={"q6": "010100", "alpha": 0},
    links=["pro2:q6:010100", "meta:hexagram:20"],
    is_fallback=False
)
```

---

<!-- similar-docs -->

---

## Похожие документы
- [[19-7-portalentry-structure]] (сходство 0.25)
- [[81-6-adapter-interface]] (сходство 0.12)
- [[memnet|08-3-registry-[nautilus]]-json](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md) (сходство 0.12)


<!-- see-also -->

---

## Смотрите также
- [[19-7-portalentry-structure]]
- [[81-6-adapter-interface]]
- [[memnet|08-3-registry-[nautilus]]-json](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md)
- 123-portal-[[123-portal-mcp-py|mcp-py]]


<!-- backlinks -->

---

## Кто ссылается на этот документ (7)
- [[103-appendix-b-change-log]]
- [[109-3-принципы-консолидации-фаза-c]]
- 123-portal-[[123-portal-mcp-py|mcp-py]]
- [[18-6-adapter-interface]]
- [[21-9-query-flow]]
- [[22-10-queryresult-structure]]
- [[README]]

