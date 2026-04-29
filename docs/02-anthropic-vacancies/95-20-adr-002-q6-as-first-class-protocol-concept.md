# 20. ADR-002: Q6 as First-Class Protocol Concept

<!-- summary -->
> **Status**: Accepted (new in v1.1)

---



## 20. ADR-002: Q6 as First-Class Protocol Concept

**Status**: Accepted (new in v1.1)

**Context**: В v1.0 Q6-пространство существовало как implementation 
detail reference portal (pro2 → hexagrams). При росте экосистемы 
стало ясно, что Q6 работает как универсальная система координат 
для всех Repos, не только pro2.

**Decision**: В v1.1 Q6 повышается до нормативного концепта 
протокола. Level 2+ адаптеры MUST обеспечивать Q6-координаты. 
Каждый format MUST документировать свой Q6 mapping rule.

**Consequences**:

**Positive**:
- Унифицированная система координат для всей экосистемы
- Возможность cross-format similarity queries через Hamming distance
- Визуализации (Q6 map, heatmaps) работают universally
- CA-class mapping даёт rich symbolic interpretation

**Negative**:
- Adapters Level 2+ вынуждены определять Q6 mapping
- 64 вершин может быть мало для некоторых форматов (но достаточно 
  для большинства)
- v2.0 может понадобиться Q8 или Q12 для больших экосистем

---

<!-- similar-docs -->

---

**Похожие документы:**
- [83-8-q6-space-normative](docs/02-anthropic-vacancies/83-8-q6-space-normative.md) (сходство 0.11)
- [26-14-adr-001-federation-over-merging](docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md) (сходство 0.10)

