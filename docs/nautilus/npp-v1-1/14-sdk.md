# 14. SDK Contract (Informative)

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

## 14. SDK Contract (Informative)

Reference implementation предоставляет Python SDK (`nautilus_sdk.py`). 
SDK-ы на других языках MAY быть написаны — они считаются 
NPP-compatible, если предоставляют эквиваленты следующих методов.

### 14.1. Required SDK Methods

```python
class NautilusClient:
def __init__(self, base_url: str = "http://localhost:8080"): ...

def query(self, q: str, ranked: bool = True) -> QueryResult: ...
def describe(self) -> dict: ...
def health(self) -> HealthReport: ...
```

### 14.2. Optional SDK Methods

```python
def links(self) -> LinksReport: ...
def neighbors(self, q6: str, dist: int = 1) -> list[QueryResult]: ...
```

### 14.3. Return Types

SDK MUST деsериализовать JSON responses в typed structures (dataclasses 
для Python, interfaces для TypeScript и т.д.). Raw dict return 
acceptable только для debugging/experimental версий.

---

<!-- see-also -->

---

**Смотрите также:**
- [89-14-sdk-contract-informative](docs/02-anthropic-vacancies/89-14-sdk-contract-informative.md)
- [18-reference-implementation](docs/nautilus/npp-v1-1/18-reference-implementation.md)
- [11-relevance-ranking](docs/nautilus/npp-v1-1/11-relevance-ranking.md)
- [17-appendix-b-change-log](docs/nautilus/npp-v1-0/17-appendix-b-change-log.md)

