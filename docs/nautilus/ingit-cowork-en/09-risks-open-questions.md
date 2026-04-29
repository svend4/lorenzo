# 9. Risks and Open Questions

> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «InGit + Cowork (EN)».

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
