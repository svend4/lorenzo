# 6. Adapter Interface

<!-- toc-auto -->
## Contents

- [6. Adapter Interface](#6-adapter-interface)
  - [6.1. BaseAdapter Contract](#61-baseadapter-contract)
  - [6.2. fetch(query) — Required](#62-fetchquery-required)
  - [6.3. describe() — Required](#63-describe-required)
  - [6.4. Type Safety](#64-type-safety)


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> Каждый адаптер MUST наследоваться (или иметь эквивалентный интерфейс)

---
<!-- tags: ingestion -->




## 6. Adapter Interface

### 6.1. BaseAdapter Contract

Каждый адаптер MUST наследоваться (или иметь эквивалентный интерфейс) 
от `BaseAdapter`:

```python
from abc import ABC, abstractmethod
from typing import Any

class BaseAdapter(ABC):
    name: str = "unnamed"
    
    @abstractmethod
    def fetch(self, query: str) -> list["PortalEntry"]:
        """Search the repo, return unified entries. MUST NOT raise."""
        ...
    
    @abstractmethod
    def describe(self) -> dict[str, Any]:
        """Return metadata about the repo."""
        ...
```

### 6.2. `fetch(query)` — Required

Accepts string query, returns list of `PortalEntry`.

Implementation MUST:

- Возвращать пустой список или fallback-entries, если ничего не 
  найдено (NOT `None`, NOT raise exception)
- Ограничить результат разумным числом (SHOULD ≤ 100)
- Не выполнять сетевые запросы к другим Repos (только свой Repo 
  или external API)
- При ошибке возвращать fallback с `is_fallback=True`

Implementation SHOULD:

- Поддерживать case-insensitive matching
- Возвращать результаты в порядке убывания релевантности
- Кешировать результаты для одинаковых query (TTL по дизайну 
  implementation, RECOMMENDED 24 часа)

### 6.3. `describe()` — Required

Returns dict со следующей рекомендованной структурой:

```python
{
    "repo": str,                    # owner/repo-name
    "format": str,                  # format identifier
    "native_unit": str,             # human description
    "total_items": int | str,       # сколько записей (int или "N+")
    "compatibility": int,           # 0..3
    "q6_key": str | None,           # rule for Q6 mapping, optional
    "bridges": dict[str, str],      # копия из nautilus.json
    "last_updated": str | None      # ISO 8601, optional
}
```

### 6.4. Type Safety

Reference implementation требует mypy-clean код. Альтернативные 
implementations SHOULD, но не MUST, придерживаться strict typing.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [18-6-adapter-interface](18-6-adapter-interface.md) (сходство 0.51)
- [85-10-query-flow](85-10-query-flow.md) (сходство 0.12)
- [82-7-portalentry-structure](82-7-portalentry-structure.md) (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [18-6-adapter-interface](18-6-adapter-interface.md)
- [82-7-portalentry-structure](82-7-portalentry-structure.md)
- [19-7-portalentry-structure](19-7-portalentry-structure.md)
- [22-10-queryresult-structure](22-10-queryresult-structure.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [6. Adapter Interface](18-6-adapter-interface.md) _53%_
- [10. QueryResult Structure](22-10-queryresult-structure.md) _29%_
- [7. PortalEntry Structure](82-7-portalentry-structure.md) _29%_
- [3. Registry (`nautilus.json`)](08-3-registry-nautilus-json.md) _25%_
- [9. Query Flow](21-9-query-flow.md) _25%_
- [Appendix B: Change Log](103-appendix-b-change-log.md) _21%_
- [11. Relevance Ranking](86-11-relevance-ranking.md) _21%_
- [14. SDK Contract (Informative)](89-14-sdk-contract-informative.md) _21%_
