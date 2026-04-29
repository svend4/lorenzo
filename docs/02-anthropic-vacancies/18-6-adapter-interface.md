# 6. Adapter Interface

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Adapter Interface(6-adapter-interface) - 6.1.
> 🔧 **Подход:** translateto(entry, targetrepo) — Required for Level 3(64-translatetoentry-targetrepo-required-for-level-3) !IMPORTANT Ключевой документ для понимания архитектуры.
> ✅ **Результат:** Implementation MUST: - Возвращать пустой список, если ничего не найдено (не None, не exception) - Ограничить результат разумным числом (SHOULD ≤ 100) - Не выполнять сетевые запросы
> 🏷️ **Ключевые слова:** `required`, `level`, `adapter`, `interface`, `query`, `anthropic`, `vacancies`, `portalentry`
>


<!-- toc-auto -->
## Contents

- [6. Adapter Interface](#6-adapter-interface)
  - [6.1. [BaseAdapter](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md) Contract](#61-baseadapter-contract)
  - [6.2. describe() — Required for Level 1+](#62-describe-required-for-level-1)
  - [6.3. fetch(query) — Required for Level 2+](#63-fetchquery-required-for-level-2)
  - [6.4. translateto(entry, targetrepo) — Required for Level 3](#64-translatetoentry-targetrepo-required-for-level-3)


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> Каждый адаптер MUST наследоваться (или иметь эквивалентный интерфейс)

---



## 6. Adapter Interface

### 6.1. BaseAdapter Contract

Каждый адаптер MUST наследоваться (или иметь эквивалентный интерфейс) 
от `[BaseAdapter](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)`:

```python
class BaseAdapter:
    name: str
    repo_path: str  # local path или git URL
    
    def describe(self) -> dict:
        """Level 1+: return metadata about the repo."""
        ...
    
    def fetch(self, query: str) -> list[PortalEntry]:
        """Level 2+: search the repo, return unified entries."""
        ...
    
    def translate_to(self, entry: "PortalEntry", 
                     target_repo: str) -> str | None:
        """Level 3: translate entry to another repo's native concept."""
        return None
```

### 6.2. `describe()` — Required for Level 1+

Returns dict со следующей обязательной структурой:

```python
{
    "name": str,                    # совпадает с self.name
    "format": str,                  # native format identifier
    "total_entries": int | None,    # сколько записей всего
    "last_updated": str | None,     # ISO 8601 timestamp
    "topics": list[str],            # ключевые темы
    "bridges": dict[str, str]       # копия из nautilus.json bridges
}
```

### 6.3. `fetch(query)` — Required for Level 2+

Accepts string query, returns list of `[PortalEntry](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)`.

Implementation MUST:

- Возвращать пустой список, если ничего не найдено (не `None`, не exception)
- Ограничить результат разумным числом (SHOULD ≤ 100)
- Не выполнять сетевые запросы к другим Repos (только локальный Repo)

Implementation SHOULD:

- Поддерживать case-insensitive matching для текстовых запросов
- Возвращать результаты в порядке убывания релевантности
- Кешировать результаты для одинаковых query

### 6.4. `translate_to(entry, target_repo)` — Required for Level 3

Accepts `[PortalEntry](../docs/02-anthropic-vacancies/01-интегральный-анализ-профиля-svend4.md)` и имя target repo из `bridges`. Returns 
string description концепта entry в терминах target_repo, или 
`None` если перевод невозможен.

Это **свободная текстовая интерпретация**, не formal mapping. 
Цель — дать пользователю возможность увидеть концепт «глазами» 
другого Repo.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [81-6-adapter-interface](docs/02-anthropic-vacancies/81-6-adapter-interface.md) (сходство 0.51)
- [21-9-query-flow](docs/02-anthropic-vacancies/21-9-query-flow.md) (сходство 0.11)
- [85-10-query-flow](docs/02-anthropic-vacancies/85-10-query-flow.md) (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [81-6-adapter-interface](docs/02-anthropic-vacancies/81-6-adapter-interface.md)
- [19-7-portalentry-structure](docs/02-anthropic-vacancies/19-7-portalentry-structure.md)
- [82-7-portalentry-structure](docs/02-anthropic-vacancies/82-7-portalentry-structure.md)
- [23-11-security-considerations](docs/02-anthropic-vacancies/23-11-security-considerations.md)

