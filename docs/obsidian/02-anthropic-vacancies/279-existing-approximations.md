---
title: "Existing Approximations"
tags:
  - rag
  - architecture
  - anthropic
  - anthropic-vacancies
date: 2026-04-29
---

# Existing Approximations

> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- toc -->
## Содержание

- [Contents](#contents)
- [Existing Approximations](#existing-approximations)
  - [Anthropic Projects](#anthropic-projects)
  - [GitHub Discussions](#github-discussions)
  - [Notion / Obsidian / Roam](#notion-obsidian-roam)
  - [Discourse / phpBB-style forums](#discourse-phpbb-style-forums)
  - [Combination workflows](#combination-workflows)

---


<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** It solves part of the problem (persistent context) but not the threading and structural needs.
> 🔧 **Подход:** Limitations: - No AI collaboration - Not designed for documents as first-class artifacts - Not designed for project-style work tracking These tools are good for community discussio
> ✅ **Результат:** Anthropic Projects Provides persistent context across multiple chats grouped around a topic.
> 🏷️ **Ключевые слова:** `anthropic`, `layer`, `vacancies`, `existing`, `github`, `discussions`, `tools`, `projects`
>


<!-- toc-auto -->
## Contents

- [Existing Approximations](#existing-approximations)
  - [Anthropic Projects](#anthropic-projects)
  - [GitHub Discussions](#github-discussions)
  - [Notion / Obsidian / Roam](#notion-[obsidian](../docs/01-svyazi/03-component-catalog.md)-roam)
  - [Discourse / phpBB-style forums](#discourse-phpbb-style-forums)
  - [Combination workflows](#combination-workflows)


<!-- summary -->
> Several existing tools approximate parts of what Layer B

---
<!-- tags: rag, architecture, anthropic -->




## Existing Approximations

Several existing tools approximate parts of what Layer B 
should be. None covers the full need.

### Anthropic Projects

Provides persistent context across multiple chats grouped 
around a topic. The closest to Layer B from the chat side. 
Limitations:
- Each chat within a project is still linear
- No threading or branching from specific messages
- No annotation on documents
- Documents are stored as files in Project Knowledge but not 
  versioned in a way useful for intellectual work
- Cross-references between content items not first-class

Projects is **necessary but not sufficient**. It solves part 
of the problem (persistent context) but not the threading 
and structural needs.

### GitHub Discussions

Provides threaded forum within [[03-component-catalog|GitHub]] repositories. Threading 
works well. Limitations:
- Culturally code-oriented; intellectual discussions feel 
  out of place
- No AI collaboration as native operation
- Discussions are separate from documents in the repository; 
  links between them are external references, not first-class
- No annotation on document text

[[03-component-catalog|GitHub]] Discussions is **structurally close** but **culturally 
distant** for intellectual work.

### Notion / Obsidian / Roam

Personal knowledge management with linked notes. Cross-references 
work well. Limitations:
- Designed for individual use; collaboration is added as 
  feature, not core
- AI integration is added as feature, not core
- No native threading model — linking is bidirectional but 
  not threaded
- Document versioning works but is not the central organizing 
  principle

These tools are **good for personal knowledge** but **not 
designed for sustained AI collaboration on shared work**.

### Discourse / phpBB-style forums

Mature threaded discussion tools. Threading is the central 
organizing principle. Limitations:
- No AI collaboration
- Not designed for documents as first-class artifacts
- Not designed for project-style work tracking

These tools are **good for community discussion** but **not 
designed for intellectual project development**.

### Combination workflows

Most serious intellectual workers combine tools:
- Anthropic Projects for AI-assisted writing
- [[03-component-catalog|GitHub]] for storage and versioning
- Notion or Obsidian for personal knowledge
- Email or messaging for real-time
- Discord or Slack for community

This works. But the fragmentation has costs:
- Context is split across systems
- Cross-references are mostly mental, not technical
- Each system has different access controls
- Migration between systems requires effort
- Each system has its own UI to learn

The fragmentation is what the author was identifying as the 
problem.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[276-the-two-layer-stack-as-it-exists]] (сходство 0.19)
- [[309-1-the-cowork-discovery-and-why-it-changes-everythi]] (сходство 0.16)
- [[280-the-specific-case-in-front-of-us]] (сходство 0.16)


<!-- see-also -->

---

**Смотрите также:**
- [[276-the-two-layer-stack-as-it-exists]]
- [[277-what-s-missing-layer-b]]
- [[280-the-specific-case-in-front-of-us]]
- [[309-1-the-cowork-discovery-and-why-it-changes-everythi]]

