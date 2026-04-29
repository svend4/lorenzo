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
