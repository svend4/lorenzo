---
title: "14. SDK Contract (Informative)"
tags:
  - anthropic
  - anthropic-vacancies
date: 2026-04-29
---

# 14. SDK Contract (Informative)
<!-- tags: anthropic -->


<!-- toc-auto -->
## Contents

- [14. SDK Contract (Informative)](#14-sdk-contract-informative)
  - [14.1. Required SDK Methods](#141-required-sdk-methods)
  - [14.2. Optional SDK Methods](#142-optional-sdk-methods)
  - [14.3. Return Types](#143-return-types)


<!-- summary -->
> Reference implementation предоставляет Python SDK (`nautilus_sdk.py`).

---
<!-- tags: anthropic -->




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

<!-- similar-docs -->

---

**Похожие документы:**
- [[93-18-reference-implementation]] (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [[93-18-reference-implementation]]
- [[22-10-queryresult-structure]]
- [[25-13-reference-implementation]]
- [[28-appendix-a-minimal-working-example]]

<!-- backlinks-auto -->
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[22-10-queryresult-structure|10. QueryResult Structure]] _33%_
- [[103-appendix-b-change-log|Appendix B: Change Log]] _25%_
- [[104-appendix-c-references|Appendix C: References]] _25%_
- [[93-18-reference-implementation|18. Reference Implementation]] _25%_
- [[04-abstract|Abstract]] _21%_
- [[08-3-registry-nautilus-json|3. Registry (`nautilus.json`)]] _21%_
- [[09-4-passport-passport-md|4. Passport (`passport.md`)]] _21%_
- [[28-appendix-a-minimal-working-example|Appendix A: Minimal Working Example]] _21%_
