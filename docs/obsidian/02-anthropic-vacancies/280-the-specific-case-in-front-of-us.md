---
title: "The Specific Case in Front of Us"
tags:
  - rag
  - anthropic
  - anthropic-vacancies
date: 2026-04-29
---

# The Specific Case in Front of Us

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Future Claude sessions about specific aspects of this work need specific context — not the whole 50,000 words.
> 🔧 **Подход:** The author may want to try two different approaches to Composite Skills Agent rollout, develop both, compare them, and choose.
> ✅ **Результат:** When the author shows the documents to potential collaborators, those collaborators will want to comment on specific sections.
> 🏷️ **Ключевые слова:** `specific`, `documents`, `anthropic`, `github`, `layer`, `context`, `vacancies`, `option`
>


<!-- summary -->
> The seven documents produced in this session have specific

---

<!-- toc -->
## Содержание

- [The Specific Case in Front of Us](#the-specific-case-in-front-of-us)
  - [What we have](#what-we-have)
  - [What we need but lack](#what-we-need-but-lack)
  - [What we can do pragmatically](#what-we-can-do-pragmatically)

---

<!-- tags: rag, anthropic -->




## The Specific Case in Front of Us

The seven documents produced in this session have specific 
infrastructure needs that current tools partially address.

### What we have

The chat session contains the documents and the dialogue that 
produced them. Through Claude's conversation_search and 
recent_chats tools, future sessions can retrieve context from 
this one. This is partial persistence.

### What we need but lack

**Threading from specific messages.** The author may want to 
return to the discussion of Composite Skills Agent risks 
(section 10 of Document 7) and develop one specific risk 
further. Current chat has no mechanism for this. The thread 
would need to start a new chat with quoted context.

**Annotation on documents.** When the author shows the 
documents to potential collaborators, those collaborators 
will want to comment on specific sections. Currently this 
requires them to either send messages with quoted text or 
edit the documents directly. No middle ground.

**Cross-reference maintenance.** When Document 7 says "see 
Document 6 Section 7.5 for the original SGB pilot proposal," 
this is text. If Document 6 is restructured (sections 
renumbered), the reference breaks silently. No mechanism 
detects this.

**Branching exploration.** The author may want to try two 
different approaches to Composite Skills Agent rollout, 
develop both, compare them, and choose. Currently this would 
require manual maintenance of two versions.

**Promotion to repository.** The seven documents should be 
committed to [[03-component-catalog|GitHub]]. This is straightforward — copy, commit, 
push. But the discussion that produced them, the alternatives 
considered, the reasoning chains — all of that lives only in 
chat. The repository will have artifacts without provenance.

**Selective context for further work.** Future Claude sessions 
about specific aspects of this work need specific context — 
not the whole 50,000 words. Currently, providing context means 
either uploading documents (loses chat context) or relying on 
conversation_search (limited).

### What we can do pragmatically

Given the gap, what can we realistically do now?

**Option 1 — Commit and walk away.** Save documents to [[03-component-catalog|GitHub]]. 
Treat them as static reference artifacts. Future development 
happens in fresh sessions with documents as context. 
Limitations: cross-references break, no annotation, no 
threading, but no maintenance overhead.

**Option 2 — Commit plus [[03-component-catalog|GitHub]] Discussions.** Save documents 
to [[03-component-catalog|GitHub]]. Open GitHub Discussions for the repository. Use 
Discussions for threaded conversations about specific aspects. 
Limitations: cultural mismatch, AI collaboration is external 
to Discussions, but threading works.

**Option 3 — Hybrid with Projects.** Save documents to [[03-component-catalog|GitHub]]. 
Create Anthropic Project for Nautilus / OKWF work. Use 
Project for AI-assisted development of new aspects. Use 
[[03-component-catalog|GitHub]] for stable artifacts. Use Discussions for community 
input. Limitations: fragmentation, but each tool used for 
its strengths.

**Option 4 — Custom lightweight setup.** For technical users 
willing to self-host, deploy Discourse or similar threaded 
forum. Connect to [[03-component-catalog|GitHub]] via integrations. Use Anthropic API 
for AI collaboration via custom interface. Limitations: 
maintenance burden, but more aligned to actual workflow.

For most cases, Option 3 (hybrid) is most realistic. Option 
4 is achievable for the specific case at hand because the 
author has technical capability and an existing repository 
infrastructure.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[276-the-two-layer-stack-as-it-exists]] (сходство 0.18)
- [[277-what-s-missing-layer-b]] (сходство 0.16)
- [[279-existing-approximations]] (сходство 0.16)


<!-- see-also -->

---

**Смотрите также:**
- [[277-what-s-missing-layer-b]]
- [[276-the-two-layer-stack-as-it-exists]]
- [[284-practical-recommendations-for-the-current-project]]
- [[279-existing-approximations]]

<!-- backlinks-auto -->
## Упоминается в

- [[218-7-application-domains|7. Application Domains]]
- [[315-7-practical-first-steps-this-month|7. Practical First Steps This Month]]
- [[279-existing-approximations|Existing Approximations]]
- [[284-practical-recommendations-for-the-current-project|Practical Recommendations for the Current Project]]
- [[276-the-two-layer-stack-as-it-exists|The Two-Layer Stack As It Exists]]
- [[282-what-industry-will-likely-build|What Industry Will Likely Build]]
- [[277-what-s-missing-layer-b|What's Missing — Layer B]]
- [[275-why-this-document-exists|Why This Document Exists]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[277-what-s-missing-layer-b|What's Missing — Layer B]] _53%_
- [[284-practical-recommendations-for-the-current-project|Practical Recommendations for the Current Project]] _42%_
- [[276-the-two-layer-stack-as-it-exists|The Two-Layer Stack As It Exists]] _37%_
- [[275-why-this-document-exists|Why This Document Exists]] _33%_
- [[279-existing-approximations|Existing Approximations]] _33%_
- [[282-what-industry-will-likely-build|What Industry Will Likely Build]] _25%_
- [[283-what-this-document-doesn-t-solve|What This Document Doesn't Solve]] _25%_
- [[309-1-the-cowork-discovery-and-why-it-changes-everythi|1. The Cowork Discovery and Why It Changes Everything]] _25%_
## Связанные документы

- [[276-the-two-layer-stack-as-it-exists|The Two-Layer Stack As It Exists]] _42%_
- [[277-what-s-missing-layer-b|What's Missing — Layer B]] _37%_
- [[284-practical-recommendations-for-the-current-project|Practical Recommendations for the Current Project]] _37%_
- [[275-why-this-document-exists|Why This Document Exists]] _29%_
- [[279-existing-approximations|Existing Approximations]] _29%_
- [[309-1-the-cowork-discovery-and-why-it-changes-everythi|1. The Cowork Discovery and Why It Changes Everything]] _25%_
- [[282-what-industry-will-likely-build|What Industry Will Likely Build]] _21%_
- [[283-what-this-document-doesn-t-solve|What This Document Doesn't Solve]] _21%_
