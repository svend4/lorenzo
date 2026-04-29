# 1. The Cowork Discovery and Why It Changes Everything

<!-- summary -->
> When Document 2.3 was written earlier in this session, the

---

<!-- toc -->
## Содержание

- [1. The Cowork Discovery and Why It Changes Everything](#1-the-cowork-discovery-and-why-it-changes-everything)
  - [1.1. Document 2.3's Position Was Incomplete](#11-document-23s-position-was-incomplete)
  - [1.2. What Document 2.3 Got Right](#12-what-document-23-got-right)
  - [1.3. The Strategic Implication](#13-the-strategic-implication)

---

<!-- tags: rag, local-first, architecture, anthropic -->




## 1. The Cowork Discovery and Why It Changes Everything

### 1.1. Document 2.3's Position Was Incomplete

When Document 2.3 was written earlier in this session, the 
author and collaborator framed the Layer B gap as essentially 
unfilled. We surveyed Anthropic Projects, GitHub Discussions, 
Notion, Obsidian, and various combinations — and concluded 
that no existing tool adequately served sustained AI-
collaborative intellectual work.

This framing was incomplete. We were unaware (or only 
partially aware) of Anthropic's Cowork platform, launched 
January 12, 2026, and its substantial expansion since.

Cowork specifically addresses many of the Layer B requirements:
- Persistent memory across sessions (scoped to Project)
- Local file system access (within permitted folders)
- MCP connector support for external integrations
- Multi-step task execution (agentic, not just chat)
- Scheduled recurring tasks
- Computer use for UI navigation when needed
- Project workspaces with custom instructions

Reading the Cowork documentation in light of Document 2.3's 
requirements reveals that **substantial Layer B infrastructure 
already exists in production**. This is not speculative; it is 
deployed and being used by significant numbers of professional 
knowledge workers.

### 1.2. What Document 2.3 Got Right

Despite missing Cowork, Document 2.3 correctly identified 
several requirements that Cowork itself does not fully solve:

**Threading at message level.** Cowork has Project-scoped 
memory, but within a session, conversation is still linear. 
Branching from specific points to develop alternatives in 
parallel is not a first-class operation.

**Annotation on document sections.** Cowork can read and edit 
documents but has no native annotation layer where comments 
attach to specific text passages and persist across versions.

**Cross-references with link integrity.** Cowork can follow 
references in documents but does not maintain reference 
integrity automatically when documents restructure.

**Promotion workflow between layers.** Cowork lives within 
Claude Desktop; promoting content from chat sessions to 
durable Project artifacts to repository commits remains 
manual.

These remain genuine gaps. But the gaps are now in a different 
context: they are gaps **above** a substantial Layer B 
foundation, not the entire absence of Layer B.

### 1.3. The Strategic Implication

This changes strategy dramatically. Building Layer B from 
scratch was the implicit framing of Document 2.3's recursive 
insight (Nautilus extending into Layer B prototype). The 
implication was a multi-year, substantial product development 
effort.

With Cowork existing, the question changes. Now it is: how 
does InGit position itself relative to Cowork? Three 
possibilities:

**Option A — Compete.** Build InGit as alternative to Cowork. 
This requires matching Cowork's agentic capabilities, 
persistence, MCP support, computer use. Multi-year effort 
duplicating Anthropic's investment.

**Option B — Ignore.** Build InGit independently of Cowork. 
Useful for offline-first scenarios but misses the value 
multiplication.

**Option C — Complement.** Position InGit as the structure 
layer that Cowork needs. Leverage Cowork's agentic intelligence; 
provide structured workspace substrate that Cowork's general-
purpose Project storage doesn't.

Option C is dramatically better. It reduces InGit's required 
scope. It accelerates time to value. It creates symbiotic 
relationship rather than competitive one. It aligns with 
InGit's existing offline-first philosophy (Cowork can work 
with local InGit projects). And it makes InGit immediately 
useful, not after years of development.

The remainder of this document develops Option C.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [307-abstract](docs/02-anthropic-vacancies/307-abstract.md) (сходство 0.19)
- [310-2-what-cowork-provides-that-ingit-doesn-t-need-to-](docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md) (сходство 0.18)
- [311-3-what-ingit-provides-that-cowork-lacks](docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md) (сходство 0.17)


<!-- see-also -->

---

**Смотрите также:**
- [307-abstract](docs/02-anthropic-vacancies/307-abstract.md)
- [310-2-what-cowork-provides-that-ingit-doesn-t-need-to-](docs/02-anthropic-vacancies/310-2-what-cowork-provides-that-ingit-doesn-t-need-to-.md)
- [279-existing-approximations](docs/02-anthropic-vacancies/279-existing-approximations.md)
- [311-3-what-ingit-provides-that-cowork-lacks](docs/02-anthropic-vacancies/311-3-what-ingit-provides-that-cowork-lacks.md)

