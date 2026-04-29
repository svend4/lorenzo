---
title: "6. Refined InGit Scope with Cowork in Mind"
tags:
  - architecture
  - roadmap
  - anthropic
  - nautilus
date: 2026-04-29
---

# 6. Refined InGit Scope with Cowork in Mind

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «InGit + Cowork (EN)».

---
<!-- tags: architecture, roadmap, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «InGit + Cowork (EN)».

## 6. Refined InGit Scope with Cowork in Mind

The original InGit roadmap (10-16 months to v1.0) reflected 
ambition for full standalone product. With Cowork as 
complement, scope can dramatically reduce.

### 6.1. New Phase 1 (Months 1-3): Substrate MVP

**Goal**: InGit becomes usable as Cowork substrate.

**Deliverables**:
- Folder structure conventions (already in repository)
- YAML metadata schemas for tasks, documents, wiki pages
- Pre-commit hooks for validation
- Basic encryption for sensitive folders (using age)
- Documentation of conventions
- Examples and templates

**Removed from original Phase 1**:
- Desktop GUI (deferred to "maybe never" given Cowork)
- Database layer (SQLite still useful but secondary)
- Web UI (Cowork is the UI)

**Effort**: Achievable in 3 months by individual developer 
working part-time.

### 6.2. New Phase 2 (Months 3-6): MCP Server

**Goal**: InGit operations available to Cowork via MCP.

**Deliverables**:
- `ingit-mcp-server` Python package
- 15-20 tools covering core operations
- Open source release
- Integration documentation
- Examples for Cowork Projects

**Effort**: 2-3 months for solo developer.

### 6.3. New Phase 3 (Months 6-12): Adoption and Refinement

**Goal**: Real-world usage drives improvements.

**Deliverables**:
- Migration tools (Notion, Obsidian, GitHub)
- Refinements based on user feedback
- Documentation expansion
- Community building

**Effort**: Depends on adoption velocity.

### 6.4. Total Reduced Scope

Original plan: 10-16 months to v1.0 with substantial features.
Revised plan: 12 months to mature substrate + MCP integration.

**Removed scope**:
- Desktop GUI: -3 months effort
- Web UI: -2 months effort
- Mobile app: -2 months effort (was implicit)
- Agent infrastructure: -3 months effort (Cowork provides)
- Independent connector ecosystem: -2 months effort

**Net effort reduction**: ~12 months work removed.
**Net timeline**: From 10-16 months to roughly 12 months, with 
much higher quality result.

This is the value of strategic positioning: less work for 
better outcomes.

---

<!-- see-also -->

---

**Смотрите также:**
- [[314-6-refined-ingit-scope-with-cowork-in-mind]]
- [[02-cowork-provides]]
- [[03-ingit-provides]]
- [[310-2-what-cowork-provides-that-ingit-doesn-t-need-to-]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[314-6-refined-ingit-scope-with-cowork-in-mind]] (сходство 0.76)
- [[314-6-refined-ingit-scope-with-cowork-in-mind]] (сходство 0.73)
- [[02-cowork-provides]] (сходство 0.23)

