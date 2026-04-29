# 10. QueryResult Structure

<!-- summary -->
> results_by_repo: dict[str, list[PortalEntry]]

---
<!-- tags: anthropic -->




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
- [21-9-query-flow](21-9-query-flow.md) (сходство 0.11)
- [25-13-reference-implementation](25-13-reference-implementation.md) (сходство 0.11)
- [81-6-adapter-interface](81-6-adapter-interface.md) (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [25-13-reference-implementation](25-13-reference-implementation.md)
- [21-9-query-flow](21-9-query-flow.md)
- [28-appendix-a-minimal-working-example](28-appendix-a-minimal-working-example.md)
- [86-11-relevance-ranking](86-11-relevance-ranking.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [Appendix A: Minimal Working Example](98-appendix-a-minimal-working-example.md) _37%_
- [9. Query Flow](21-9-query-flow.md) _33%_
- [Appendix A: Minimal Working Example](28-appendix-a-minimal-working-example.md) _33%_
- [14. SDK Contract (Informative)](89-14-sdk-contract-informative.md) _33%_
- [6. Adapter Interface](18-6-adapter-interface.md) _29%_
- [6. Adapter Interface](81-6-adapter-interface.md) _29%_
- [4. Passport (`passport.md`)](09-4-passport-passport-md.md) _25%_
- [Appendix B: Change Log](103-appendix-b-change-log.md) _25%_
