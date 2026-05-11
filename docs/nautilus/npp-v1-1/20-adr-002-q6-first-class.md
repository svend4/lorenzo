# 20. ADR-002: Q6 as First-Class Protocol Concept

<!-- toc-auto -->
## Contents

- [20. ADR-002: Q6 as First-Class Protocol Concept](#20-adr-002-q6-as-first-class-protocol-concept)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: anthropic -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





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

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "20 ADR 002 Q6 as First Class Protocol"
```

## Смотрите также
- [95-20-adr-002-q6-as-first-class-protocol-concept](../../02-anthropic-vacancies/95-20-adr-002-q6-as-first-class-protocol-concept.md)
- [21-adr-003-five-onboarding-paths](21-adr-003-five-onboarding-paths.md)
- [11-relevance-ranking](11-relevance-ranking.md)
- [14-sdk](14-sdk.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория и доступен для поиска._ _Доступен семантический поиск._ _Индексировано._

<!-- backlinks -->

---

**Кто ссылается на этот документ (8):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [14-adr-001-federation-over-merging](../npp-v1-0/14-adr-001-federation-over-merging.md)
- [08-q6-space](08-q6-space.md)
- [21-adr-003-five-onboarding-paths](21-adr-003-five-onboarding-paths.md)
- [README](README.md)

