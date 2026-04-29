# 9. Risks and Open Questions

<!-- toc -->
## Содержание

- [Contents](#contents)
- [9. Risks and Open Questions](#9-risks-and-open-questions)
  - [9.1. Cowork's Future Direction](#91-coworks-future-direction)
  - [9.2. MCP Standard Evolution](#92-mcp-standard-evolution)
  - [9.3. Cowork's Resource Consumption](#93-coworks-resource-consumption)
  - [9.4. Privacy and Sensitive Work](#94-privacy-and-sensitive-work)
  - [9.5. Author Capacity](#95-author-capacity)
  - [9.6. Open Questions](#96-open-questions)
- [Упоминается в](#упоминается-в)
- [Связанные документы](#связанные-документы)

---


<!-- toc-auto -->
## Contents

- [9. Risks and Open Questions](#9-risks-and-open-questions)
  - [9.1. Cowork's Future Direction](#91-coworks-future-direction)
  - [9.2. MCP Standard Evolution](#92-mcp-standard-evolution)
  - [9.3. Cowork's Resource Consumption](#93-coworks-resource-consumption)
  - [9.4. Privacy and Sensitive Work](#94-privacy-and-sensitive-work)
  - [9.5. Author Capacity](#95-author-capacity)
  - [9.6. Open Questions](#96-open-questions)


> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> Several uncertainties merit explicit attention.

---
<!-- tags: rag, orchestration, local-first, architecture, roadmap, anthropic -->




## 9. Risks and Open Questions

Several uncertainties merit explicit attention.

### 9.1. Cowork's Future Direction

Cowork is research preview. Anthropic's product roadmap not 
publicly committed. Possible scenarios:

**Scenario 1 — Cowork matures as expected**: Adds team 
sharing, mature MCP integration, Project templates. InGit 
positioning solid.

**Scenario 2 — Cowork pivots**: Anthropic redirects toward 
different model. Some current capabilities deprecated. InGit 
substrate still useful (offline-first), but Cowork integration 
weaker.

**Scenario 3 — Cowork captured by competition**: OpenAI, 
Google launch competing products. Cowork remains capable but 
loses market share. InGit needs broader compatibility.

Mitigation: InGit's value beyond Cowork (offline-first, 
portable, structured) ensures viability even in adverse 
scenarios. Don't over-commit to Cowork-specific features 
that lose value if Cowork changes.

### 9.2. MCP Standard Evolution

MCP is recent (late 2024). Standards still evolving. Risk 
that significant changes break existing servers.

Mitigation: MCP is open standard with multiple implementers. 
Even if Anthropic specifically changes direction, MCP 
continues. Build for MCP, not for Cowork-specific protocol.

### 9.3. Cowork's Resource Consumption

Per published reports, Cowork sessions consume significantly 
more usage allocation than chat (one Cowork Project session = 
20+ regular chats). For Pro users, limits may be hit quickly.

Mitigation: InGit Projects with Cowork should be designed 
for **efficient agent use**, not chatty interaction. 
Structured outputs, batch operations, scheduled tasks rather 
than real-time chat.

### 9.4. Privacy and Sensitive Work

Cowork's data flows through Anthropic infrastructure. For 
highly sensitive work (legal, medical, financial), this may 
be unacceptable.

Mitigation: InGit's offline mode remains valuable. For 
sensitive work, use InGit alone with manual workflows or 
local models. Cowork integration for non-sensitive components.

### 9.5. Author Capacity

The author of this paper has multiple active commitments: 
SGB legal cases, physical health considerations (GdB 70, 
Pflegegrad), Nautilus development, the eight existing 
documents in this series.

Adding active InGit/Cowork integration work may exceed 
realistic capacity.

Mitigation: Sequential progress. Start with Path 1 (no 
development). Expand only as bandwidth permits. Don't commit 
to ambitious timelines.

### 9.6. Open Questions

**Q1**: Will Anthropic open Project templates to third parties 
soon? Unknown.

**Q2**: Will MCP server distribution improve (registry, 
package management)? Currently fragmented.

**Q3**: How does pricing evolve? Cowork is currently 
expensive in usage; if costs drop, adoption accelerates.

**Q4**: Will Cowork add threading/branching/annotation features? 
If yes, fills more of Layer B gap; if no, leaves space for 
others.

**Q5**: Will competitors emerge? OpenAI, Google likely build 
similar capabilities. Standardization unclear.

These uncertainties shape but do not block progress. Path 1 
works regardless of any of them.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [318-10-strategic-positioning](318-10-strategic-positioning.md) (сходство 0.15)
- [311-3-what-ingit-provides-that-cowork-lacks](311-3-what-ingit-provides-that-cowork-lacks.md) (сходство 0.13)
- [323-appendix-c-sample-ingit-mcp-server-tool-specificat](323-appendix-c-sample-ingit-mcp-server-tool-specificat.md) (сходство 0.13)


<!-- see-also -->

---

**Смотрите также:**
- [318-10-strategic-positioning](318-10-strategic-positioning.md)
- [316-8-implications-for-nautilus-and-okwf](316-8-implications-for-nautilus-and-okwf.md)
- [313-5-four-integration-paths-in-order-of-accessibility](313-5-four-integration-paths-in-order-of-accessibility.md)
- [311-3-what-ingit-provides-that-cowork-lacks](311-3-what-ingit-provides-that-cowork-lacks.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [10. Strategic Positioning](318-10-strategic-positioning.md) _33%_
- [3. What InGit Provides That Cowork Lacks](311-3-what-ingit-provides-that-cowork-lacks.md) _25%_
- [5. Four Integration Paths in Order of Accessibility](313-5-four-integration-paths-in-order-of-accessibility.md) _21%_
- [6. Refined InGit Scope with Cowork in Mind](314-6-refined-ingit-scope-with-cowork-in-mind.md) _21%_
- [8. Implications for Nautilus and OKWF](316-8-implications-for-nautilus-and-okwf.md) _21%_
- [Acknowledgments](319-acknowledgments.md) _21%_
- [Appendix C: Sample InGit MCP Server Tool Specifications](323-appendix-c-sample-ingit-mcp-server-tool-specificat.md) _21%_
- [8. Call to Action](145-8-call-to-action.md) _17%_
