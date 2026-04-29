# 19. ADR-001: Federation over Merging

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: architecture, anthropic, collaboration -->




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

**Смотрите также:**
- [14-adr-001-federation-over-merging](docs/nautilus/npp-v1-0/14-adr-001-federation-over-merging.md)
- [94-19-adr-001-federation-over-merging](docs/02-anthropic-vacancies/94-19-adr-001-federation-over-merging.md)
- [26-14-adr-001-federation-over-merging](docs/02-anthropic-vacancies/26-14-adr-001-federation-over-merging.md)
- [21-adr-003-five-onboarding-paths](docs/nautilus/npp-v1-1/21-adr-003-five-onboarding-paths.md)

