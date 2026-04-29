# 6. Adapter Interface

<!-- toc -->
## Содержание

- [Contents](#contents)
- [Contents](#contents)
- [6. Adapter Interface](#6-adapter-interface)
  - [6.1. BaseAdapter Contract](#61-baseadapter-contract)
  - [6.2. `describe()` — Required for Level 1+](#62-describe-required-for-level-1)
  - [6.3. `fetch(query)` — Required for Level 2+](#63-fetchquery-required-for-level-2)
  - [6.4. `translate_to(entry, target_repo)` — Required for Level 3](#64-translate_toentry-target_repo-required-for-level-3)
- [Упоминается в](#упоминается-в)
- [Упоминается в](#упоминается-в)
- [Связанные документы](#связанные-документы)
- [Связанные документы](#связанные-документы)

---

<!-- tags: ingestion, architecture, anthropic, collaboration -->

<!-- toc -->
## Содержание

- [Contents](#contents)
- [6. Adapter Interface](#6-adapter-interface)
  - [6.1. BaseAdapter Contract](#61-baseadapter-contract)
  - [6.2. `describe()` — Required for Level 1+](#62-describe-required-for-level-1)
  - [6.3. `fetch(query)` — Required for Level 2+](#63-fetchquery-required-for-level-2)
  - [6.4. `translate_to(entry, target_repo)` — Required for Level 3](#64-translate_toentry-target_repo-required-for-level-3)
- [Упоминается в](#упоминается-в)
- [Упоминается в](#упоминается-в)
- [Связанные документы](#связанные-документы)
- [Связанные документы](#связанные-документы)

---

<!-- tags: ingestion, architecture, anthropic -->


<!-- toc-auto -->
## Contents

- [6. Adapter Interface](#6-adapter-interface)
  - [6.1. BaseAdapter Contract](#61-baseadapter-contract)
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
- [81-6-adapter-interface](81-6-adapter-interface.md) (сходство 0.51)
- [21-9-query-flow](21-9-query-flow.md) (сходство 0.11)
- [85-10-query-flow](85-10-query-flow.md) (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [81-6-adapter-interface](81-6-adapter-interface.md)
- [19-7-portalentry-structure](19-7-portalentry-structure.md)
- [82-7-portalentry-structure](82-7-portalentry-structure.md)
- [23-11-security-considerations](23-11-security-considerations.md)

<!-- backlinks-auto -->
## Упоминается в

- [10. Query Flow](85-10-query-flow.md)
- [10. QueryResult Structure](22-10-queryresult-structure.md)
- [13. REST API Contract (Normative for Portals)](88-13-rest-api-contract-normative-for-portals.md)
- [15. Security Considerations](90-15-security-considerations.md)
- [3. Registry (`nautilus.json`)](08-3-registry-nautilus-json.md)
- [5. Compatibility Levels](17-5-compatibility-levels.md)
- [5. Compatibility Levels](80-5-compatibility-levels.md)
- [6. Adapter Interface](81-6-adapter-interface.md)
- [7. PortalEntry Structure](19-7-portalentry-structure.md)
- [7. PortalEntry Structure](82-7-portalentry-structure.md)
- [8. Q6 Space (Normative)](83-8-q6-space-normative.md)
- [9. Query Flow](21-9-query-flow.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [6. Adapter Interface](81-6-adapter-interface.md) _48%_
- [9. Query Flow](21-9-query-flow.md) _33%_
- [10. Query Flow](85-10-query-flow.md) _25%_
- [3. Registry (`nautilus.json`)](08-3-registry-nautilus-json.md) _21%_
- [7. PortalEntry Structure](19-7-portalentry-structure.md) _21%_
- [10. QueryResult Structure](22-10-queryresult-structure.md) _21%_
- [7. PortalEntry Structure](82-7-portalentry-structure.md) _21%_
- [5. Compatibility Levels](17-5-compatibility-levels.md) _17%_
## Связанные документы

- [6. Adapter Interface](81-6-adapter-interface.md) _53%_
- [9. Query Flow](21-9-query-flow.md) _33%_
- [10. QueryResult Structure](22-10-queryresult-structure.md) _29%_
- [7. PortalEntry Structure](82-7-portalentry-structure.md) _29%_
- [10. Query Flow](85-10-query-flow.md) _29%_
- [3. Registry (`nautilus.json`)](08-3-registry-nautilus-json.md) _25%_
- [5. Compatibility Levels](17-5-compatibility-levels.md) _21%_
- [7. PortalEntry Structure](19-7-portalentry-structure.md) _21%_
