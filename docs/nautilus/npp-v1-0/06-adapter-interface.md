# 6. Adapter Interface

<!-- toc-auto -->
## Contents

- [6. Adapter Interface](#6-adapter-interface)
  - [6.1. BaseAdapter Contract](#61-baseadapter-contract)
  - [6.2. describe() — Required for Level 1+](#62-describe-required-for-level-1)
  - [6.3. fetch(query) — Required for Level 2+](#63-fetchquery-required-for-level-2)
  - [6.4. translate_to(entry, target_repo) — Required for Level 3](#64-translate_toentry-target_repo-required-for-level-3)


  - 6.1. [BaseAdapter Contract](#61-baseadapter-contract)
  - [6.2. describe() — Required for Level 1+](#62-describe-required-for-level-1)
  - [6.3. fetch(query) — Required for Level 2+](#63-fetchquery-required-for-level-2)
  - [6.4. translate_to(entry, target_repo) — Required for Level 3](#64-translate_toentry-target_repo-required-for-level-3)
  - 6.1. [BaseAdapter Contract](#61-baseadapter-contract)
  - [6.2. describe() — Required for Level 1+](#62-describe-required-for-level-1)
  - [6.3. fetch(query) — Required for Level 2+](#63-fetchquery-required-for-level-2)
  - [6.4. translate_to(entry, target_repo) — Required for Level 3](#64-translate_toentry-target_repo-required-for-level-3)
  - 6.1. [BaseAdapter Contract](#61-baseadapter-contract)
  - [6.2. describe() — Required for Level 1+](#62-describe-required-for-level-1)
  - [6.3. fetch(query) — Required for Level 2+](#63-fetchquery-required-for-level-2)
  - [6.4. translate_to(entry, target_repo) — Required for Level 3](#64-translate_toentry-target_repo-required-for-level-3)


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

---
<!-- tags: anthropic -->


> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

## 6. Adapter Interface

### 6.1. BaseAdapter Contract

Каждый адаптер MUST наследоваться (или иметь эквивалентный интерфейс) 
от `BaseAdapter`:

```python
class BaseAdapter:
name: str
repo_path: str # local path или git URL

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
"name": str, # совпадает с self.name
"format": str, # native format identifier
"total_entries": int | None, # сколько записей всего
"last_updated": str | None, # ISO 8601 timestamp
"topics": list[str], # ключевые темы
"bridges": dict[str, str] # копия из nautilus.json bridges
}
```

### 6.3. `fetch(query)` — Required for Level 2+

Accepts string query, returns list of `PortalEntry`.

Implementation MUST:

- Возвращать пустой список, если ничего не найдено (не `None`, не exception)
- Ограничить результат разумным числом (SHOULD ≤ 100)
- Не выполнять сетевые запросы к другим Repos (только локальный Repo)

Implementation SHOULD:

- Поддерживать case-insensitive matching для текстовых запросов
- Возвращать результаты в порядке убывания релевантности
- Кешировать результаты для одинаковых query

### 6.4. `translate_to(entry, target_repo)` — Required for Level 3

Accepts `PortalEntry` и имя target repo из `bridges`. Returns 
string description концепта entry в терминах target_repo, или 
`None` если перевод невозможен.

Это **свободная текстовая интерпретация**, не formal mapping. 
Цель — дать пользователю возможность увидеть концепт «глазами» 
другого Repo.

---

<!-- backlinks -->

---

**Кто ссылается на этот документ (5):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [06-adapter-interface](../../obsidian/nautilus/npp-v1-0/06-adapter-interface.md) (сходство 0.98)
- [18-6-adapter-interface](../../02-anthropic-vacancies/18-6-adapter-interface.md) (сходство 0.67)
- [18-6-adapter-interface](../../obsidian/02-anthropic-vacancies/18-6-adapter-interface.md) (сходство 0.66)

