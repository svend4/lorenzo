# 7. PortalEntry Structure

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
- [19-7-portalentry-structure](docs/02-anthropic-vacancies/19-7-portalentry-structure.md) (сходство 0.25)
- [81-6-adapter-interface](docs/02-anthropic-vacancies/81-6-adapter-interface.md) (сходство 0.12)
- [08-3-registry-nautilus-json](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md) (сходство 0.12)

