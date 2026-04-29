# 8. Implications for Nautilus and OKWF

<!-- toc -->
## Содержание

- [Contents](#contents)
- [8. Implications for Nautilus and OKWF](#8-implications-for-nautilus-and-okwf)
  - [8.1. Nautilus as Federated Knowledge Substrate](#81-nautilus-as-federated-knowledge-substrate)
  - [8.2. OKWF Pilot Implications](#82-okwf-pilot-implications)
  - [8.3. Composite Skills Agent in This Architecture](#83-composite-skills-agent-in-this-architecture)
  - [8.4. Document 2.3's Recursive Insight Realized](#84-document-23s-recursive-insight-realized)
- [Упоминается в](#упоминается-в)
- [Связанные документы](#связанные-документы)

---


<!-- toc-auto -->
## Contents

- [8. Implications for Nautilus and OKWF](#8-implications-for-nautilus-and-okwf)
  - [8.1. Nautilus as Federated Knowledge Substrate](#81-nautilus-as-federated-knowledge-substrate)
  - [8.2. OKWF Pilot Implications](#82-okwf-pilot-implications)
  - [8.3. Composite Skills Agent in This Architecture](#83-composite-skills-agent-in-this-architecture)
  - [8.4. Document 2.3's Recursive Insight Realized](#84-document-23s-recursive-insight-realized)


> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> Beyond InGit specifically, this positioning has implications

---

<!-- toc -->
## Содержание

- [8. Implications for Nautilus and OKWF](#8-implications-for-nautilus-and-okwf)
  - [8.1. Nautilus as Federated Knowledge Substrate](#81-nautilus-as-federated-knowledge-substrate)
  - [8.2. OKWF Pilot Implications](#82-okwf-pilot-implications)
  - [8.3. Composite Skills Agent in This Architecture](#83-composite-skills-agent-in-this-architecture)
  - [8.4. Document 2.3's Recursive Insight Realized](#84-document-23s-recursive-insight-realized)

---

<!-- tags: rag, architecture -->




## 8. Implications for Nautilus and OKWF

Beyond InGit specifically, this positioning has implications 
for the broader Nautilus / OKWF project.

### 8.1. Nautilus as Federated Knowledge Substrate

Nautilus was designed for federated knowledge across multiple 
repositories with semantic organization (Q6 hypercube, Pattern 
Library). With InGit as Cowork substrate, Nautilus's role 
clarifies:

**Nautilus operates one level above InGit**. While InGit 
structures individual projects, Nautilus federates across 
many projects. Multiple InGit projects can be Nautilus nodes; 
Nautilus Portal Protocol enables querying across them.

Cowork users with InGit Projects could optionally federate 
through Nautilus, gaining cross-project search, pattern 
sharing, and contribution paths.

This is consistent with Document 1 (Portal Protocol) but now 
with concrete substrate underneath.

### 8.2. OKWF Pilot Implications

Document 4 (OKWF Concept) and Document 6 (Professional 
Colleague Agents) proposed SGB Advocate Colleague pilot. With 
the InGit/Cowork combination available:

**Pilot architecture refined**:
- Each advocate has InGit Project for their case work
- Cowork operates within these Projects
- MCP server for SGB-specific knowledge (statutes, precedents)
- Pattern Library integration via Nautilus
- Cross-advocate sharing via federated Nautilus

This is dramatically more achievable than building everything 
custom. Substantial infrastructure (Cowork) is leveraged. 
Specialized layers (SGB MCP server, pattern library) are 
focused additions, not full system.

**Revised Year 1 budget**: Original Document 6 estimate was 
€430K, then Document 7 increased to €1.5M for composite 
architecture. With Cowork as agentic layer:

- Cowork: included in user subscriptions (€20/month per 
  practitioner)
- InGit substrate: ~€100K to mature
- SGB-specific MCP server: ~€200K to build
- Pattern library integration: ~€100K
- Operations and support: ~€100K
- **Revised Year 1: €500K**, plus practitioner Cowork 
  subscriptions

Closer to original estimate, more achievable, leverages 
existing infrastructure.

### 8.3. Composite Skills Agent in This Architecture

Document 7 introduced Composite Skills Agent — Type 1.5 
between Professional Colleague (Type 1) and Representative 
Agent (Type 4). With Cowork:

**Cowork is the coordinator of composite agents**. The 
configuration of sub-agents (specialized MCP servers for 
narrow specializations) is the principal's composite identity. 
Cowork orchestrates them, surfaces disagreements, integrates 
outputs.

Sub-agents become specialized MCP servers:
- `mcp-sgb-ix-section-78`
- `mcp-german-procedural-law`
- `mcp-saxony-court-procedures`
- `mcp-ksv-sachsen-patterns`
- `mcp-medical-assessment-interpretation`

Each is independently maintainable. Each can be added to 
practitioner's Cowork Project as needed. Configuration is 
literally the set of MCP servers active for that Project.

This is more concrete than Document 7's abstract description. 
The architecture maps onto actual Cowork capabilities.

### 8.4. Document 2.3's Recursive Insight Realized

Document 2.3 noted recursive symmetry: Nautilus extending 
itself to provide infrastructure for its own development. With 
InGit/Cowork:

**This now has concrete shape**. The Nautilus / OKWF intellectual 
project can:
- Live in InGit Project (substrate)
- Be developed in Cowork (agent layer)
- Federate via Nautilus (across-project layer)
- Inform its own architecture through usage

The recursive insight is no longer aspirational. It is 
implementable starting next week.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [318-10-strategic-positioning](318-10-strategic-positioning.md) (сходство 0.16)
- [262-9-integration-with-okwf-infrastructure](262-9-integration-with-okwf-infrastructure.md) (сходство 0.16)
- [310-2-what-cowork-provides-that-ingit-doesn-t-need-to-](310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md) (сходство 0.14)


<!-- see-also -->

---

**Смотрите также:**
- [262-9-integration-with-okwf-infrastructure](262-9-integration-with-okwf-infrastructure.md)
- [318-10-strategic-positioning](318-10-strategic-positioning.md)
- [310-2-what-cowork-provides-that-ingit-doesn-t-need-to-](310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md)
- [317-9-risks-and-open-questions](317-9-risks-and-open-questions.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [10. Strategic Positioning](318-10-strategic-positioning.md) _33%_
- [4. The Sub-Agent Registry](257-4-the-sub-agent-registry.md) _29%_
- [9. Integration with OKWF Infrastructure](262-9-integration-with-okwf-infrastructure.md) _29%_
- [INGIT AS COWORK-NATIVE WORKSPACE SUBSTRATE.md](304-ingit-as-cowork-native-workspace-substrate-md.md) _29%_
- [Abstract](307-abstract.md) _29%_
- [7. Practical First Steps This Month](315-7-practical-first-steps-this-month.md) _29%_
- [Appendix C: Sample InGit MCP Server Tool Specifications](323-appendix-c-sample-ingit-mcp-server-tool-specificat.md) _29%_
- [Карта происхождения текстов](../SOURCE_MAP.md) _29%_
