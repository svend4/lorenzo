---
title: "6. Adapter Interface"
tags:
  - ingestion
  - architecture
  - anthropic
  - collaboration
  - anthropic-vacancies
date: 2026-04-29
---

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
  - [[01-интегральный-анализ-профиля-svend4|6.1. [BaseAdapter]] Contract](#61-baseadapter-contract)
  - [6.2. describe() — Required for Level 1+](#62-describe-required-for-level-1)
  - [6.3. fetch(query) — Required for Level 2+](#63-fetchquery-required-for-level-2)
  - [6.4. translateto(entry, targetrepo) — Required for Level 3](#64-translatetoentry-targetrepo-required-for-level-3)


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
от `[[01-интегральный-анализ-профиля-svend4|BaseAdapter]]`:

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

Accepts string query, returns list of `[[01-интегральный-анализ-профиля-svend4|PortalEntry]]`.

Implementation MUST:

- Возвращать пустой список, если ничего не найдено (не `None`, не exception)
- Ограничить результат разумным числом (SHOULD ≤ 100)
- Не выполнять сетевые запросы к другим Repos (только локальный Repo)

Implementation SHOULD:

- Поддерживать case-insensitive matching для текстовых запросов
- Возвращать результаты в порядке убывания релевантности
- Кешировать результаты для одинаковых query

### 6.4. `translate_to(entry, target_repo)` — Required for Level 3

Accepts `[[01-интегральный-анализ-профиля-svend4|PortalEntry]]` и имя target repo из `bridges`. Returns 
string description концепта entry в терминах target_repo, или 
`None` если перевод невозможен.

Это **свободная текстовая интерпретация**, не formal mapping. 
Цель — дать пользователю возможность увидеть концепт «глазами» 
другого Repo.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[81-6-adapter-interface]] (сходство 0.51)
- [[21-9-query-flow]] (сходство 0.11)
- [[85-10-query-flow]] (сходство 0.10)


<!-- see-also -->

---

**Смотрите также:**
- [[81-6-adapter-interface]]
- [[19-7-portalentry-structure]]
- [[82-7-portalentry-structure]]
- [[23-11-security-considerations]]

<!-- backlinks-auto -->
## Упоминается в

- [[85-10-query-flow|10. Query Flow]]
- [[22-10-queryresult-structure|10. QueryResult Structure]]
- [[88-13-rest-api-contract-normative-for-portals|13. REST API Contract (Normative for Portals)]]
- [[90-15-security-considerations|15. Security Considerations]]
- [[08-3-registry-nautilus-json|3. Registry (`nautilus.json`)]]
- [[17-5-compatibility-levels|5. Compatibility Levels]]
- [[80-5-compatibility-levels|5. Compatibility Levels]]
- [[81-6-adapter-interface|6. Adapter Interface]]
- [[19-7-portalentry-structure|7. PortalEntry Structure]]
- [[82-7-portalentry-structure|7. PortalEntry Structure]]
- [[83-8-q6-space-normative|8. Q6 Space (Normative)]]
- [[21-9-query-flow|9. Query Flow]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[81-6-adapter-interface|6. Adapter Interface]] _48%_
- [[21-9-query-flow|9. Query Flow]] _33%_
- [[85-10-query-flow|10. Query Flow]] _25%_
- [[08-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] _21%_
- [[19-7-portalentry-structure|7. PortalEntry Structure]] _21%_
- [[22-10-queryresult-structure|10. QueryResult Structure]] _21%_
- [[82-7-portalentry-structure|7. PortalEntry Structure]] _21%_
- [[17-5-compatibility-levels|5. Compatibility Levels]] _17%_
## Связанные документы

- [[81-6-adapter-interface|6. Adapter Interface]] _53%_
- [[21-9-query-flow|9. Query Flow]] _33%_
- [[22-10-queryresult-structure|10. QueryResult Structure]] _29%_
- [[82-7-portalentry-structure|7. PortalEntry Structure]] _29%_
- [[85-10-query-flow|10. Query Flow]] _29%_
- [[08-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] _25%_
- [[17-5-compatibility-levels|5. Compatibility Levels]] _21%_
- [[19-7-portalentry-structure|7. PortalEntry Structure]] _21%_
