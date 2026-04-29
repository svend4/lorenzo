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
- [93-18-reference-implementation](93-18-reference-implementation.md) (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [93-18-reference-implementation](93-18-reference-implementation.md)
- [22-10-queryresult-structure](22-10-queryresult-structure.md)
- [25-13-reference-implementation](25-13-reference-implementation.md)
- [28-appendix-a-minimal-working-example](28-appendix-a-minimal-working-example.md)

<!-- backlinks-auto -->
## Упоминается в

- [10. QueryResult Structure](22-10-queryresult-structure.md)
- [11. Relevance Ranking](86-11-relevance-ranking.md)
- [18. Reference Implementation](93-18-reference-implementation.md)
- [6. Adapter Interface](81-6-adapter-interface.md)
- [Appendix B: Change Log](103-appendix-b-change-log.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
- [Доступные инструменты](128-доступные-инструменты.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [10. QueryResult Structure](22-10-queryresult-structure.md) _33%_
- [Appendix B: Change Log](103-appendix-b-change-log.md) _29%_
- [4. Passport (`passport.md`)](09-4-passport-passport-md.md) _25%_
- [Appendix A: Minimal Working Example](28-appendix-a-minimal-working-example.md) _25%_
- [Compatibility Level](41-compatibility-level.md) _21%_
- [11. Relevance Ranking](86-11-relevance-ranking.md) _21%_
- [18. Reference Implementation](93-18-reference-implementation.md) _21%_
- [Appendix A: Minimal Working Example](98-appendix-a-minimal-working-example.md) _21%_
## Связанные документы

- [10. QueryResult Structure](22-10-queryresult-structure.md) _33%_
- [Appendix B: Change Log](103-appendix-b-change-log.md) _25%_
- [Appendix C: References](104-appendix-c-references.md) _25%_
- [18. Reference Implementation](93-18-reference-implementation.md) _25%_
- [Abstract](04-abstract.md) _21%_
- [3. Registry (`nautilus.json`)](08-3-registry-nautilus-json.md) _21%_
- [4. Passport (`passport.md`)](09-4-passport-passport-md.md) _21%_
- [Appendix A: Minimal Working Example](28-appendix-a-minimal-working-example.md) _21%_
