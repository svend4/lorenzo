---
title: "The Two-Layer Stack As It Exists"
tags:
  - architecture
  - anthropic
  - anthropic-vacancies
date: 2026-04-29
---

# The Two-Layer Stack As It Exists

<!-- toc -->
## Содержание

- [The Two-Layer Stack As It Exists](#the-two-layer-stack-as-it-exists)
- [Упоминается в](#упоминается-в)
- [Упоминается в](#упоминается-в)
- [Связанные документы](#связанные-документы)
- [Связанные документы](#связанные-документы)

---


<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** The problem is what happens between them.
> ✅ **Результат:** The Anthropic chat interface (and similar products from other providers).
> 🏷️ **Ключевые слова:** `anthropic`, `document`, `specific`, `vacancies`, `layer`, `exists`, `artifacts`, `human`
>


> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> Currently, AI-collaborative work tends to occur in one of two

---
<!-- tags: architecture, anthropic -->




## The Two-Layer Stack As It Exists

Currently, AI-collaborative work tends to occur in one of two 
layers:

**Layer A — Chat.** The Anthropic chat interface (and similar 
products from other providers). Excellent for creative dialogue, 
exploration, generating content. The natural creative space. 
Linear by structure.

**Layer C — Code repositories.** [[03-component-catalog|GitHub]], GitLab, Codeberg. 
Excellent for storing structured artifacts, version control, 
collaboration around technical artifacts. Branching, merging, 
issues, discussions. Code-oriented by design.

These two layers serve different functions and serve them well. 
The problem is what happens between them.

Currently, the transition from chat-derived content to repository-
stored artifacts is **manual copy-paste**. The chat produces a 
document; the human copies it; the human pastes it into a 
repository file; the human commits it. Any further development 
of the document goes back through chat (or sometimes through 
direct editing in the repository).

This works for simple cases. It breaks down when:

- The chat content is too large to copy effectively
- Multiple related artifacts emerge across multiple chats
- Cross-references between artifacts need to be maintained
- Comments on specific sections need preservation
- Branching exploration needs to maintain links to original
- The human wants to return to a specific point in chat to 
  develop a particular thread further
- Multiple parallel developments need to be tracked

This is what just happened in this seven-document session. 
The session contains the documents (in chat form), but extracting 
them, organizing them, maintaining their relationships, enabling 
further work on specific parts — all of this requires 
infrastructure that does not exist as a unified product.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[279-existing-approximations]] (сходство 0.19)
- [[275-why-this-document-exists]] (сходство 0.18)
- [[280-the-specific-case-in-front-of-us]] (сходство 0.18)


<!-- see-also -->

---

**Смотрите также:**
- [[279-existing-approximations]]
- [[280-the-specific-case-in-front-of-us]]
- [[275-why-this-document-exists]]
- [[277-what-s-missing-layer-b]]

<!-- backlinks-auto -->
## Упоминается в

- [[218-7-application-domains|7. Application Domains]]
- [[315-7-practical-first-steps-this-month|7. Practical First Steps This Month]]
- [[279-existing-approximations|Existing Approximations]]
- [[284-practical-recommendations-for-the-current-project|Practical Recommendations for the Current Project]]
- [[280-the-specific-case-in-front-of-us|The Specific Case in Front of Us]]
- [[282-what-industry-will-likely-build|What Industry Will Likely Build]]
- [[283-what-this-document-doesn-t-solve|What This Document Doesn't Solve]]
- [[277-what-s-missing-layer-b|What's Missing — Layer B]]
- [[275-why-this-document-exists|Why This Document Exists]]
- [[278-why-this-hasn-t-been-built|Why This Hasn't Been Built]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[277-what-s-missing-layer-b|What's Missing — Layer B]] _37%_
- [[280-the-specific-case-in-front-of-us|The Specific Case in Front of Us]] _37%_
- [[284-practical-recommendations-for-the-current-project|Practical Recommendations for the Current Project]] _37%_
- [[275-why-this-document-exists|Why This Document Exists]] _29%_
- [[279-existing-approximations|Existing Approximations]] _29%_
- [[278-why-this-hasn-t-been-built|Why This Hasn't Been Built]] _25%_
- [[282-what-industry-will-likely-build|What Industry Will Likely Build]] _25%_
- [[286-acknowledgments|Acknowledgments]] _25%_
## Связанные документы

- [[280-the-specific-case-in-front-of-us|The Specific Case in Front of Us]] _42%_
- [[284-practical-recommendations-for-the-current-project|Practical Recommendations for the Current Project]] _42%_
- [[277-what-s-missing-layer-b|What's Missing — Layer B]] _37%_
- [[275-why-this-document-exists|Why This Document Exists]] _29%_
- [[278-why-this-hasn-t-been-built|Why This Hasn't Been Built]] _29%_
- [[279-existing-approximations|Existing Approximations]] _29%_
- [[283-what-this-document-doesn-t-solve|What This Document Doesn't Solve]] _29%_
- [[286-acknowledgments|Acknowledgments]] _29%_
