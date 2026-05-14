---
state: approved
---

# The Specific Case in Front of Us

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Infrastructure for AI-Collaborative Intellectual Work (EN)».

---

<!-- toc -->

> [!IMPORTANT]
> Нормативный документ. Описывает контракты и архитектурные решения.

## Содержание

- [The Specific Case in Front of Us](#the-specific-case-in-front-of-us)
  - [What we have](#what-we-have)
  - [What we need but lack](#what-we-need-but-lack)
  - [What we can do pragmatically](#what-we-can-do-pragmatically)

---

<!-- tags: rag, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Infrastructure for AI-Collaborative Intellectual Work (EN)».

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
committed to GitHub. This is straightforward — copy, commit, 
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

**Option 1 — Commit and walk away.** Save documents to GitHub. 
Treat them as static reference artifacts. Future development 
happens in fresh sessions with documents as context. 
Limitations: cross-references break, no annotation, no 
threading, but no maintenance overhead.

**Option 2 — Commit plus GitHub Discussions.** Save documents 
to GitHub. Open GitHub Discussions for the repository. Use 
Discussions for threaded conversations about specific aspects. 
Limitations: cultural mismatch, AI collaboration is external 
to Discussions, but threading works.

**Option 3 — Hybrid with Projects.** Save documents to GitHub. 
Create Anthropic Project for Nautilus / OKWF work. Use 
Project for AI-assisted development of new aspects. Use 
GitHub for stable artifacts. Use Discussions for community 
input. Limitations: fragmentation, but each tool used for 
its strengths.

**Option 4 — Custom lightweight setup.** For technical users 
willing to self-host, deploy Discourse or similar threaded 
forum. Connect to GitHub via integrations. Use Anthropic API 
for AI collaboration via custom interface. Limitations: 
maintenance burden, but more aligned to actual workflow.

For most cases, Option 3 (hybrid) is most realistic. Option 
4 is achievable for the specific case at hand because the 
author has technical capability and an existing repository 
infrastructure.

---

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "The Specific Case in Front of Us"
```

## Смотрите также
- [280-the-specific-case-in-front-of-us](../../02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md)
- [03-two-layer-stack](03-two-layer-stack.md)
- [04-whats-missing-layer-b](04-whats-missing-layer-b.md)
- [06-existing-approximations](06-existing-approximations.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (9):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [04-whats-missing-layer-b](04-whats-missing-layer-b.md)
- [06-existing-approximations](06-existing-approximations.md)
- [11-practical-recommendations](11-practical-recommendations.md)
- _...ещё 1_


<!-- similar-docs -->

---

**Похожие документы:**
- [07-specific-case](../../obsidian/nautilus/infrastructure-layer-b-en/07-specific-case.md) (сходство 0.99)
- [280-the-specific-case-in-front-of-us](../../02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md) (сходство 0.81)
- [280-the-specific-case-in-front-of-us](../../obsidian/02-anthropic-vacancies/280-the-specific-case-in-front-of-us.md) (сходство 0.81)

