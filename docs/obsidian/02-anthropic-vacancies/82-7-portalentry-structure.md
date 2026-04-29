---
title: "7. PortalEntry Structure"
tags:
  - ingestion
  - architecture
  - collaboration
  - anthropic-vacancies
date: 2026-04-29
---

# 7. PortalEntry Structure

<!-- toc-auto -->
## Contents

- [7. PortalEntry Structure](#7-portalentry-structure)
  - [7.1. Field Semantics](#71-field-semantics)
  - [7.2. Q6 Metadata](#72-q6-metadata)


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> Унифицированная структура данных, возвращаемая адаптерами.

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
  `"<format>:<slug>"` (например, `"info1:alpha-3-doc-1"`)
- `title` SHOULD быть до 120 символов
- `source` — GitHub slug `owner/repo-name`
- `format_type` — one of: `document`, `concept`, `rule`, `theory`, 
  `schema`, `archetype`. Implementation MAY расширять список
- `content` — полный текст/представление, MAY быть большим
- `metadata` — MUST содержать `q6` для Level 2+ адаптеров
- `links` — список id из других Repos, формат `"<format>:<type>:<id>"` 
  или `"<format>:<id>"` (например, `"pro2:q6:010011"`, 
  `"meta:hexagram:50"`)
- `is_fallback` — Boolean, MUST быть `True` для fallback-entries, 
  `False` (default) для real fetch results

### 7.2. Q6 Metadata

Для адаптеров Level 2+, каждый PortalEntry MUST содержать 
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

**Похожие документы:**
- [[19-7-portalentry-structure]] (сходство 0.25)
- [[81-6-adapter-interface]] (сходство 0.12)
- [[08-3-registry-nautilus-json]] (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [[19-7-portalentry-structure]]
- [[81-6-adapter-interface]]
- [[08-3-registry-nautilus-json]]
- [[123-portal-mcp-py]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[19-7-portalentry-structure|7. PortalEntry Structure]] _42%_
- [[08-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] _33%_
- [[18-6-adapter-interface|6. Adapter Interface]] _29%_
- [[77-2-terminology|2. Terminology]] _29%_
- [[81-6-adapter-interface|6. Adapter Interface]] _29%_
- [[07-2-terminology|2. Terminology]] _25%_
- [[22-10-queryresult-structure|10. QueryResult Structure]] _25%_
- [[79-4-passport-passport-md|4. Passport (`passport.md`)]] _25%_
