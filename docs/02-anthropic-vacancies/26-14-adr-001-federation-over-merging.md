# 14. ADR-001: Federation over Merging

<!-- summary -->
> **Context:** При построении системы knowledge management встаёт

---
<!-- tags: architecture, collaboration -->




## 14. ADR-001: Federation over Merging

**Status:** Accepted

**Context:** При построении системы knowledge management встаёт 
выбор: заставить все данные мигрировать в единую схему (merge), 
либо сохранить разные native-форматы и переводить по необходимости 
(federation).

**Decision:** Выбрана federation.

**Consequences:**

**Positive:**
- Low barrier to entry: существующие Repos подключаются без 
  рефакторинга
- Authorship preserved: каждый автор работает в своей модели
- Multi-angle views: один концепт может существовать в трёх Repos 
  с тремя разными углами одновременно

**Negative:**
- Cross-repo queries дороже: требуется вызов всех адаптеров
- Consensus нетривиален: string matching — аппроксимация, не 
  formal mapping
- Bridges — текстовые описания, не machine-executable

**Alternatives rejected:**
- Unified RDF/OWL ontology: слишком высокий barrier to entry
- Centralized database: нарушает принцип local autonomy
- Schema-less dump: теряется семантика angles

---
