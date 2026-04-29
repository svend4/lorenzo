# 20. ADR-002: Q6 as First-Class Protocol Concept

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

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

<!-- see-also -->

---

**Смотрите также:**
- [95-20-adr-002-q6-as-first-class-protocol-concept](docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md)
- [21-adr-003-five-onboarding-paths](docs/nautilus/npp-v1-1/21-adr-003-five-onboarding-paths.md)
- [11-relevance-ranking](docs/nautilus/npp-v1-1/11-relevance-ranking.md)
- [14-sdk](docs/nautilus/npp-v1-1/14-sdk.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [95-20-adr-002-q6-as-first-class-protocol-concept](docs/obsidian/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md) (сходство 0.70)
- [95-20-adr-002-q6-as-first-class-protocol-concept](docs/02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md) (сходство 0.69)
- [21-adr-003-five-onboarding-paths](docs/nautilus/npp-v1-1/21-adr-003-five-onboarding-paths.md) (сходство 0.27)

