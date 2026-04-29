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
- [93-18-reference-implementation](docs/02-anthropic-vacancies/93-18-reference-implementation.md) (сходство 0.12)


<!-- see-also -->

---

**Смотрите также:**
- [93-18-reference-implementation](docs/02-anthropic-vacancies/93-18-reference-implementation.md)
- [22-10-queryresult-structure](docs/02-anthropic-vacancies/22-10-queryresult-structure.md)
- [25-13-reference-implementation](docs/02-anthropic-vacancies/25-13-reference-implementation.md)
- [28-appendix-a-minimal-working-example](docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](docs/02-anthropic-vacancies/README.md)

<!-- related-auto -->
## Связанные документы

- [10. QueryResult Structure](docs/02-anthropic-vacancies/22-10-queryresult-structure.md) _33%_
- [Appendix B: Change Log](docs/02-anthropic-vacancies/103-appendix-b-change-log.md) _25%_
- [Appendix C: References](docs/02-anthropic-vacancies/104-appendix-c-references.md) _25%_
- [18. Reference Implementation](docs/02-anthropic-vacancies/93-18-reference-implementation.md) _25%_
- [Abstract](docs/02-anthropic-vacancies/04-abstract.md) _21%_
- [3. Registry (`nautilus.json`)](docs/02-anthropic-vacancies/08-3-registry-nautilus-json.md) _21%_
- [4. Passport (`passport.md`)](docs/02-anthropic-vacancies/09-4-passport-passport-md.md) _21%_
- [Appendix A: Minimal Working Example](docs/02-anthropic-vacancies/28-appendix-a-minimal-working-example.md) _21%_
