# 21. ADR-003: Five Onboarding Paths as Equal-Rank

<!-- toc-auto -->
## Contents

- [21. ADR-003: Five Onboarding Paths as Equal-Rank](#21-adr-003-five-onboarding-paths-as-equal-rank)
- [Похожие документы](#похожие-документы)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (6)](#кто-ссылается-на-этот-документ-6)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> **Status**: Accepted (new in v1.1)

---
<!-- tags: anthropic -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





## 21. ADR-003: Five Onboarding Paths as Equal-Rank

**Status**: Accepted (new in v1.1)

**Context**: В v1.0 была одна "основная" стратегия подключения 
(manual adapter). В процессе развития reference implementation 
появились 4 дополнительных пути (B–E). Возникал вопрос: какой 
канонический?

**Decision**: Все 5 путей — равнорангованные. Выбор делается по 
контексту (раздел 12.6), не по иерархии.

**Consequences**:

**Positive**:
- Flexibility для разных use cases
- Self-declaring repos (Path C) enables federation без центральной 
  координации
- Automated paths (D, E) scale для fleet-federation

**Negative**:
- Больше документации
- Users могут путаться, какой путь выбрать (mitigated via раздел 
  12.6 guidance)

---

<!-- similar-docs -->

---

## Похожие документы
- [94-19-adr-001-federation-over-merging](94-19-adr-001-federation-over-merging.md) (сходство 0.11)


<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "21 ADR 003 Five Onboarding Paths as"
```

## Смотрите также
- [94-19-adr-001-federation-over-merging](94-19-adr-001-federation-over-merging.md)
- [95-20-adr-002-q6-as-first-class-protocol-concept](95-20-adr-002-q6-as-first-class-protocol-concept.md)
- [26-14-adr-001-federation-over-merging](26-14-adr-001-federation-over-merging.md)
- [321-appendix-a-decision-tree-for-[ingit](306-with-anthropic-s-cowork-platform.md)-adopters](docs/02-anthropic-vacancies/321-appendix-a-decision-tree-for-ingit-adopters.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (6)
- [104-appendix-c-references](104-appendix-c-references.md)
- [26-14-adr-001-federation-over-merging](26-14-adr-001-federation-over-merging.md)
- 321-appendix-a-decision-tree-for-[ingit-adopters](321-appendix-a-decision-tree-for-ingit-adopters.md)
- [94-19-adr-001-federation-over-merging](94-19-adr-001-federation-over-merging.md)
- [95-20-adr-002-q6-as-first-class-protocol-concept](95-20-adr-002-q6-as-first-class-protocol-concept.md)
- [README](README.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория и доступен для поиска._ _Доступен семантический поиск._ _Индексировано._
