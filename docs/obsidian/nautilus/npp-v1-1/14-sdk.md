---
title: "14. SDK Contract (Informative)"
tags:
  - anthropic
  - nautilus
date: 2026-04-29
---

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
- [[89-14-sdk-contract-informative]]
- [[18-reference-implementation]]
- [[11-relevance-ranking]]
- [[17-appendix-b-change-log]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[89-14-sdk-contract-informative]] (сходство 0.57)
- [[89-14-sdk-contract-informative]] (сходство 0.55)
- [[11-relevance-ranking]] (сходство 0.33)

