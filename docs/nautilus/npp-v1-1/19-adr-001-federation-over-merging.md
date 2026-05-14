---
state: approved
---

# 19. ADR-001: Federation over Merging

<!-- toc-auto -->
## Contents

- [19. ADR-001: Federation over Merging](#19-adr-001-federation-over-merging)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: architecture, anthropic, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

## 19. ADR-001: Federation over Merging

**Status**: Accepted (since v1.0, reaffirmed in v1.1)

**Context**: При построении системы knowledge management встаёт 
выбор: заставить все данные мигрировать в единую схему (merge), 
либо сохранить разные native-форматы и переводить по необходимости 
(federation).

**Decision**: Выбрана federation.

**Consequences**:

**Positive**:
- Low barrier to entry: существующие Repos подключаются без 
рефакторинга
- Authorship preserved: каждый автор работает в своей модели
- Multi-angle views: один концепт может существовать в трёх Repos 
с тремя разными углами одновременно
- Five onboarding paths: гибкость от manual до fully automated

**Negative**:
- Cross-repo queries дороже: требуется вызов всех адаптеров
- Consensus нетривиален: string matching — аппроксимация, не 
formal mapping
- Bridges — текстовые описания, не machine-executable (открытый 
вопрос для v2.0)

**Alternatives rejected**:
- Unified RDF/OWL ontology: слишком высокий barrier
- Centralized database: нарушает local autonomy
- Schema-less dump: теряется семантика angles

---

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "19 ADR 001 Federation over Merging"
```

## Смотрите также
- [14-adr-001-federation-over-merging](../npp-v1-0/14-adr-001-federation-over-merging.md)
- [94-19-adr-001-federation-over-merging](../../02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md)
- [26-14-adr-001-federation-over-merging](../../02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md)
- [21-adr-003-five-onboarding-paths](21-adr-003-five-onboarding-paths.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [README](../README.md)
- [README](README.md)
- [reading-paths](../../reading-paths.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [19-adr-001-federation-over-merging](../../obsidian/nautilus/npp-v1-1/19-adr-001-federation-over-merging.md) (сходство 0.98)
- [94-19-adr-001-federation-over-merging](../../02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md) (сходство 0.82)
- [94-19-adr-001-federation-over-merging](../../obsidian/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md) (сходство 0.82)

