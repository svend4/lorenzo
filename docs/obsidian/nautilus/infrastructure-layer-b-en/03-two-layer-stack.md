---
title: "The Two-Layer Stack As It Exists"
tags:
  - architecture
  - anthropic
  - nautilus
date: 2026-04-29
---

# The Two-Layer Stack As It Exists

> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Infrastructure for AI-Collaborative Intellectual Work (EN)».

---
<!-- tags: architecture, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Infrastructure for AI-Collaborative Intellectual Work (EN)».

## The Two-Layer Stack As It Exists

Currently, AI-collaborative work tends to occur in one of two 
layers:

**Layer A — Chat.** The Anthropic chat interface (and similar 
products from other providers). Excellent for creative dialogue, 
exploration, generating content. The natural creative space. 
Linear by structure.

**Layer C — Code repositories.** GitHub, GitLab, Codeberg. 
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

<!-- see-also -->

---

**Смотрите также:**
- [[276-the-two-layer-stack-as-it-exists]]
- [[06-existing-approximations]]
- [[01-missing-middle-layer]]
- [[02-why-document-exists]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[276-the-two-layer-stack-as-it-exists]] (сходство 0.82)
- [[276-the-two-layer-stack-as-it-exists]] (сходство 0.75)
- [[06-existing-approximations]] (сходство 0.25)

