# 6. Adapter Interface

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Type Safety Reference implementation требует mypy-clean код.
> 🔧 **Подход:** Type Safety(64-type-safety) !IMPORTANT Ключевой документ для понимания архитектуры.
> ✅ **Результат:** Implementation MUST: - Возвращать пустой список или fallback-entries, если ничего не найдено (NOT None, NOT raise exception) - Ограничить результат разумным числом (SHOULD ≤ 100) -
> 🏷️ **Ключевые слова:** `adapter`, `interface`, `structure`, `portalentry`, `anthropic`, `vacancies`, `query`, `required`
>


<!-- toc-auto -->
## Contents

- [6. Adapter Interface](#6-adapter-interface)
  - [6.1. [BaseAdapter](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md) Contract](#61-baseadapter-contract)
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
от `[BaseAdapter](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)`:

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

Accepts string query, returns list of `[PortalEntry](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)`.

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
- [18-6-adapter-interface](docs/02-anthropic-vacancies/18-6-adapter-interface.md) (сходство 0.51)
- [85-10-query-flow](docs/02-anthropic-vacancies/85-10-query-flow.md) (сходство 0.12)
- [82-7-portalentry-structure](docs/02-anthropic-vacancies/82-7-portalentry-structure.md) (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [18-6-adapter-interface](docs/02-anthropic-vacancies/18-6-adapter-interface.md)
- [82-7-portalentry-structure](docs/02-anthropic-vacancies/82-7-portalentry-structure.md)
- [19-7-portalentry-structure](docs/02-anthropic-vacancies/19-7-portalentry-structure.md)
- [22-10-queryresult-structure](docs/02-anthropic-vacancies/22-10-queryresult-structure.md)

