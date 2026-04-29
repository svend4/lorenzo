# 10. QueryResult Structure

<!-- summary -->
> results_by_repo: dict[str, list[PortalEntry]]

---



## 10. QueryResult Structure

```python
class QueryResult:
    query: str
    results_by_repo: dict[str, list[PortalEntry]]
    consensus: Consensus
    total_entries: int
    repos_queried: list[str]
    errors: dict[str, str]        # repo_name → error message
    timing: dict[str, float]      # repo_name → seconds elapsed
```

### 10.1. Serialization

QueryResult MUST поддерживать сериализацию в JSON, Markdown, HTML.

- `to_json()` — для MCP / API
- `to_markdown()` — для CLI и LLM consumption
- `to_html()` — для web interface

Формат Markdown SHOULD группировать результаты по consensus 
category (сначала full, затем partial, затем singular).

---

<!-- similar-docs -->

---

**Похожие документы:**
- [21-9-query-flow](docs/02-anthropic-vacancies/21-9-query-flow.md) (сходство 0.11)
- [25-13-reference-implementation](docs/02-anthropic-vacancies/25-13-reference-implementation.md) (сходство 0.11)
- [81-6-adapter-interface](docs/02-anthropic-vacancies/81-6-adapter-interface.md) (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [25-13-reference-implementation](docs/02-anthropic-vacancies/25-13-reference-implementation.md)
- [21-9-query-flow](docs/02-anthropic-vacancies/21-9-query-flow.md)
- [28-appendix-a-minimal-working-example](docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md)
- [86-11-relevance-ranking](docs/02-anthropic-vacancies/86-11-relevance-ranking.md)

