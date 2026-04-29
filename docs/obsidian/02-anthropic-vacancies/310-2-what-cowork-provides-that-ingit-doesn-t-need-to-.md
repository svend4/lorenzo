---
title: "2. What Cowork Provides That InGit Doesn't Need to Build"
tags:
  - architecture
  - roadmap
  - anthropic-vacancies
date: 2026-04-29
---

# 2. What Cowork Provides That InGit Doesn't Need to Build

> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** What Cowork Provides That InGit Doesn't Need to Build(2-what-cowork-provides-that-ingit-doesnt-need-to-build) - 2.1.
> 🔧 **Подход:** Claude in Cowork can: - Read multiple files, synthesize information - Make decisions about approach - Execute shell commands in isolated VM - Iterate based on results - Coordinate 
> ✅ **Результат:** What Cowork Provides That InGit Doesn't Need to Build(2-what-cowork-provides-that-ingit-doesnt-need-to-build) - 2.1.
> 🏷️ **Ключевые слова:** `cowork`, `ingit`, `provides`, `roadmap`, `build`, `anthropic`, `vacancies`, `memory`
>


<!-- summary -->
> If InGit positions to complement Cowork rather than replace

---

<!-- toc -->
## Содержание

- [2. What Cowork Provides That InGit Doesn't Need to Build](#2-what-cowork-provides-that-[ingit](../docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md)-doesnt-need-to-build)
  - [2.1. Agentic Task Execution](#21-agentic-task-execution)
  - [2.2. Persistent Memory Across Sessions](#22-persistent-memory-across-sessions)
  - [2.3. UI for Knowledge Work](#23-ui-for-knowledge-work)
  - [2.4. Connector Ecosystem](#24-connector-ecosystem)
  - [2.5. Computer Use Capability](#25-computer-use-capability)
  - [2.6. Scheduled Recurring Tasks](#26-scheduled-recurring-tasks)
  - [2.7. Cross-Platform Availability](#27-cross-platform-availability)
  - [2.8. What This Removes from InGit Roadmap](#28-what-this-removes-from-[ingit](../docs/02-anthropic-vacancies/306-with-anthropic-s-cowork-platform.md)-roadmap)

---

<!-- tags: architecture, roadmap -->




## 2. What Cowork Provides That InGit Doesn't Need to Build

If InGit positions to complement Cowork rather than replace 
it, several substantial features can be removed from InGit's 
roadmap. These are now **provided by Cowork**, and InGit 
should not duplicate them.

### 2.1. Agentic Task Execution

Cowork's core capability: agentic multi-step task execution. 
Claude in Cowork can:
- Read multiple files, synthesize information
- Make decisions about approach
- Execute shell commands in isolated VM
- Iterate based on results
- Coordinate sub-agents for parallel work
- Self-verify outputs before reporting

InGit was not planning to build this anyway, but Cowork 
provides the agentic layer that makes structured workspace 
much more valuable.

### 2.2. Persistent Memory Across Sessions

Cowork Projects have scoped memory. Claude remembers within a 
Project across sessions. Sensitive data is excluded. User can 
view, edit, delete remembered content.

This is something InGit might have eventually wanted. Not 
needed now.

### 2.3. UI for Knowledge Work

Cowork provides the user interface for interacting with the 
Project. Files visible. Tasks visible. Memory visible. 
Permission prompts for sensitive operations.

InGit's roadmap originally included Desktop GUI with 
Electron + React. With Cowork as primary interface, **this 
becomes unnecessary**. Saves substantial development effort.

### 2.4. Connector Ecosystem

Cowork integrates with Gmail, Drive, Slack, [[03-component-catalog|GitHub]], Notion, 
many others. Through MCP, custom connectors can be added.

InGit was not planning to build connectors itself, but 
Cowork's existing ecosystem means an InGit Project can use 
external services freely.

### 2.5. Computer Use Capability

When connectors are unavailable, Cowork can navigate the 
desktop and browser through computer use. This is research 
preview but functional.

For InGit Project workflows, this means even systems without 
APIs can be accessed. This was beyond InGit's planning.

### 2.6. Scheduled Recurring Tasks

Cowork can run scheduled tasks: weekly reports, daily email 
checks, monthly archives. Defined once, executed automatically.

This addresses what InGit's roadmap referred to as "auto-
generated reports."

### 2.7. Cross-Platform Availability

Cowork runs on macOS and Windows (Linux likely eventually). 
Mobile app for task assignment via Dispatch.

InGit's plan to build Desktop GUI for cross-platform support 
becomes unnecessary if Cowork is the primary interface.

### 2.8. What This Removes from InGit Roadmap

If Cowork provides the above, InGit's original roadmap can 
be substantially reduced:

**Remove or defer**:
- Desktop GUI (Electron + React)
- Web UI for project management
- Mobile app
- Persistent memory layer
- Agent execution infrastructure
- Connector framework
- Auto-report generation system

**Keep and focus on**:
- File structure conventions
- YAML metadata as code
- Git-native versioning
- Validation hooks
- Encryption for sensitive data
- Migration tools (from other systems)
- MCP server for InGit operations

This reduces InGit from a full application to a **specialized 
substrate**. Substrate is a much more achievable scope for an 
individual developer or small team.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[306-with-anthropic-s-cowork-platform|311-3-what-[ingit]]-provides-that-cowork-lacks](docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md) (сходство 0.20)
- [[309-1-the-cowork-discovery-and-why-it-changes-everythi]] (сходство 0.18)
- [[306-with-anthropic-s-cowork-platform|314-6-refined-[ingit]]-scope-with-cowork-in-mind](docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md) (сходство 0.17)


<!-- see-also -->

---

**Смотрите также:**
- [[306-with-anthropic-s-cowork-platform|311-3-what-[ingit]]-provides-that-cowork-lacks](docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md)
- [[306-with-anthropic-s-cowork-platform|314-6-refined-[ingit]]-scope-with-cowork-in-mind](docs/02-anthropic-vacancies/314-6-refined-ingit-scope-with-cowork-in-mind.md)
- [[309-1-the-cowork-discovery-and-why-it-changes-everythi]]
- [[307-abstract]]

