# 10. QueryResult Structure

<!-- toc-auto -->
## Contents

- [10. QueryResult Structure](#10-queryresult-structure)
  - [10.1. Serialization](#101-serialization)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

- 10. [QueryResult Structure](#10-queryresult-structure)
  - [10.1. Serialization](#101-serialization)


<!-- summary -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

---
<!-- tags: anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.0.0-draft RFC (более ранняя версия v1.1).

## 10. QueryResult Structure

```python
class QueryResult:
query: str
results_by_repo: dict[str, list[PortalEntry]]
consensus: Consensus
total_entries: int
repos_queried: list[str]
errors: dict[str, str] # repo_name → error message
timing: dict[str, float] # repo_name → seconds elapsed
```

### 10.1. Serialization

QueryResult MUST поддерживать сериализацию в JSON, Markdown, HTML.

- `to_json()` — для MCP / API
- `to_markdown()` — для CLI и LLM consumption
- `to_html()` — для web interface

Формат Markdown SHOULD группировать результаты по consensus 
category (сначала full, затем partial, затем singular).

---

<!-- see-also -->

---

## Смотрите также
- [17-appendix-b-change-log](17-appendix-b-change-log.md)
- [13-reference-implementation](13-reference-implementation.md)
- [22-10-queryresult-structure](../../02-anthropic-vacancies/22-10-queryresult-structure.md)
- [15-glossary](15-glossary.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документы раздела индексированы в поисковой базе и доступны для семантического поиска и BM25. Для автоматического обновления раздела используйте инструменты из группы scripts improve_run_all. Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo.

<!-- backlinks -->

---

**Кто ссылается на этот документ (13):**
- [CONCEPT_GRAPH](../../CONCEPT_GRAPH.md)
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [02-terminology](02-terminology.md)
- [08-consensus-algorithm](08-consensus-algorithm.md)
- [11-security-considerations](11-security-considerations.md)
- _...ещё 5_


<!-- similar-docs -->

---

**Похожие документы:**
- [10-query-result](../../obsidian/nautilus/npp-v1-0/10-query-result.md) (сходство 0.98)
- [13-reference-implementation](../../obsidian/nautilus/npp-v1-0/13-reference-implementation.md) (сходство 0.66)
- [17-appendix-b-change-log](../../obsidian/nautilus/npp-v1-0/17-appendix-b-change-log.md) (сходство 0.66)

