# 14. SDK Contract (Informative)
<!-- tags: memory, anthropic, collaboration -->


<!-- toc-auto -->
## Contents

- [Contents](#contents)
- [14. SDK Contract (Informative)](#14-sdk-contract-informative)
  - [14.1. Required SDK Methods](#141-required-sdk-methods)
  - [14.2. Optional SDK Methods](#142-optional-sdk-methods)
  - [14.3. Return Types](#143-return-types)
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
для Python, interfaces для [TypeScript](../05-habr-projects/memory/memnet.md) и т.д.). Raw dict return 
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


<!-- backlinks -->

---

**Кто ссылается на этот документ (9):**
- [04-abstract](04-abstract.md)
- [09-4-passport-passport-md](09-4-passport-passport-md.md)
- [103-appendix-b-change-log](103-appendix-b-change-log.md)
- [104-appendix-c-references](104-appendix-c-references.md)
- [128-доступные-инструменты](128-доступные-инструменты.md)
- [22-10-queryresult-structure](22-10-queryresult-structure.md)
- [25-13-reference-implementation](25-13-reference-implementation.md)
- [93-18-reference-implementation](93-18-reference-implementation.md)
- _...ещё 1_

