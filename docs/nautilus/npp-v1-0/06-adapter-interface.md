# 6. Adapter Interface

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

<!-- similar-docs -->

---

**Похожие документы:**
- [18-6-adapter-interface](docs/obsidian/02-anthropic-vacancies/18-6-adapter-interface.md) (сходство 0.67)
- [18-6-adapter-interface](docs/02-anthropic-vacancies/18-6-adapter-interface.md) (сходство 0.61)
- [06-adapter-interface](docs/nautilus/npp-v1-1/06-adapter-interface.md) (сходство 0.57)

