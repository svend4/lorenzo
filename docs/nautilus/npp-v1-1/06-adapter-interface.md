# 6. Adapter Interface

> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: ingestion, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

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
"repo": str, # owner/repo-name
"format": str, # format identifier
"native_unit": str, # human description
"total_items": int | str, # сколько записей (int или "N+")
"compatibility": int, # 0..3
"q6_key": str | None, # rule for Q6 mapping, optional
"bridges": dict[str, str], # копия из nautilus.json
"last_updated": str | None # ISO 8601, optional
}
```

### 6.4. Type Safety

Reference implementation требует mypy-clean код. Альтернативные 
implementations SHOULD, но не MUST, придерживаться strict typing.

---

<!-- see-also -->

---

**Смотрите также:**
- [81-6-adapter-interface](docs/02-anthropic-vacancies/81-6-adapter-interface.md)
- [18-6-adapter-interface](docs/02-anthropic-vacancies/18-6-adapter-interface.md)
- [07-portal-entry](docs/nautilus/npp-v1-1/07-portal-entry.md)
- [16-mcp-extension](docs/nautilus/npp-v1-1/16-mcp-extension.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [81-6-adapter-interface](docs/obsidian/02-anthropic-vacancies/81-6-adapter-interface.md) (сходство 0.71)
- [81-6-adapter-interface](docs/02-anthropic-vacancies/81-6-adapter-interface.md) (сходство 0.71)
- [06-adapter-interface](docs/nautilus/npp-v1-0/06-adapter-interface.md) (сходство 0.57)

