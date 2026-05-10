# 7. PortalEntry Structure

<!-- toc-auto -->
## Contents

- [7. PortalEntry Structure](#7-portalentry-structure)
  - [7.1. Field Semantics](#71-field-semantics)


- 7. [PortalEntry Structure](#7-portalentry-structure)
  - [7.1. Field Semantics](#71-field-semantics)


> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

---
<!-- tags: anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

## 7. PortalEntry Structure

Унифицированная структура данных, возвращаемая адаптерами.

```python
class PortalEntry:
repo_name: str # REQUIRED: откуда пришло
native_id: str # REQUIRED: id в native формате
title: str # REQUIRED: человекочитаемое имя
summary: str # REQUIRED: до 280 символов
content: str # REQUIRED: полный текст
tags: list[str] # OPTIONAL: ключевые слова
confidence: float # OPTIONAL: 0.0–1.0, default 1.0
native_metadata: dict # OPTIONAL: любые native-специфичные поля
url: str | None # OPTIONAL: прямая ссылка на источник
```

### 7.1. Field Semantics

- `repo_name` MUST совпадать с `name` в registry
- `native_id` MUST быть уникален в пределах Repo
- `title` SHOULD быть до 120 символов
- `summary` MUST быть до 280 символов (для предпросмотров)
- `content` MAY быть большим, но implementation MAY trimming при 
transport
- `confidence` — субъективная оценка адаптера о релевантности entry 
к query
- `native_metadata` — escape hatch для данных, не ложащихся в 
стандартные поля

---

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ доступен для семантического поиска и навигации._ _Доступен поиск._

<!-- backlinks -->

---

**Кто ссылается на этот документ (5):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [README](README.md)

