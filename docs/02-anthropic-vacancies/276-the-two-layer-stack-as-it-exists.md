# The Two-Layer Stack As It Exists

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

<!-- similar-docs -->

---

**Похожие документы:**
- [279-existing-approximations](279-existing-approximations.md) (сходство 0.19)
- [275-why-this-document-exists](275-why-this-document-exists.md) (сходство 0.18)
- [280-the-specific-case-in-front-of-us](280-the-specific-case-in-front-of-us.md) (сходство 0.18)


<!-- see-also -->

---

**Смотрите также:**
- [279-existing-approximations](279-existing-approximations.md)
- [280-the-specific-case-in-front-of-us](280-the-specific-case-in-front-of-us.md)
- [275-why-this-document-exists](275-why-this-document-exists.md)
- [277-what-s-missing-layer-b](277-what-s-missing-layer-b.md)

<!-- backlinks-auto -->
## Упоминается в

- [7. Application Domains](218-7-application-domains.md)
- [7. Practical First Steps This Month](315-7-practical-first-steps-this-month.md)
- [Existing Approximations](279-existing-approximations.md)
- [Practical Recommendations for the Current Project](284-practical-recommendations-for-the-current-project.md)
- [The Specific Case in Front of Us](280-the-specific-case-in-front-of-us.md)
- [What Industry Will Likely Build](282-what-industry-will-likely-build.md)
- [What This Document Doesn't Solve](283-what-this-document-doesn-t-solve.md)
- [What's Missing — Layer B](277-what-s-missing-layer-b.md)
- [Why This Document Exists](275-why-this-document-exists.md)
- [Why This Hasn't Been Built](278-why-this-hasn-t-been-built.md)
- [Вакансии Anthropic — Анализ по кластерам](README.md)
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [What's Missing — Layer B](277-what-s-missing-layer-b.md) _37%_
- [The Specific Case in Front of Us](280-the-specific-case-in-front-of-us.md) _37%_
- [Practical Recommendations for the Current Project](284-practical-recommendations-for-the-current-project.md) _37%_
- [Why This Document Exists](275-why-this-document-exists.md) _29%_
- [Existing Approximations](279-existing-approximations.md) _29%_
- [Why This Hasn't Been Built](278-why-this-hasn-t-been-built.md) _25%_
- [What Industry Will Likely Build](282-what-industry-will-likely-build.md) _25%_
- [Acknowledgments](286-acknowledgments.md) _25%_
## Связанные документы

- [The Specific Case in Front of Us](280-the-specific-case-in-front-of-us.md) _42%_
- [Practical Recommendations for the Current Project](284-practical-recommendations-for-the-current-project.md) _42%_
- [What's Missing — Layer B](277-what-s-missing-layer-b.md) _37%_
- [Why This Document Exists](275-why-this-document-exists.md) _29%_
- [Why This Hasn't Been Built](278-why-this-hasn-t-been-built.md) _29%_
- [Existing Approximations](279-existing-approximations.md) _29%_
- [What This Document Doesn't Solve](283-what-this-document-doesn-t-solve.md) _29%_
- [Acknowledgments](286-acknowledgments.md) _29%_
