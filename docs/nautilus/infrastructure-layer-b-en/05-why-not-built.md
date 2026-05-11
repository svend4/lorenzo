# Why This Hasn't Been Built

<!-- toc-auto -->
## Contents

- [Why This Hasn't Been Built](#why-this-hasnt-been-built)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Infrastructure for AI-Collaborative Intellectual Work (EN)».

---
<!-- tags: architecture, anthropic -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — paper «Infrastructure for AI-Collaborative Intellectual Work (EN)».

## Why This Hasn't Been Built

Several explanations for the gap.

**Explanation 1 — It's harder than it looks.** Building a 
threading-and-branching system is not technically difficult. 
Building one that integrates AI collaboration smoothly, that 
handles documents at scale, that preserves cross-references 
across modifications, that maintains both fluidity and 
structure — this is substantial product engineering. It 
requires sustained investment.

**Explanation 2 — The market is unclear.** Who pays for this? 
Individual researchers cannot afford enterprise-grade tools. 
Enterprises have different needs (formal review, compliance). 
The middle market — individuals and small groups doing 
serious intellectual work — is hard to monetize.

**Explanation 3 — Cultural lag.** Software has been built 
around files and folders for decades. Threading was solved 
in forums twenty years ago but did not migrate into 
intellectual workspaces. Wikis showed cross-references can 
work but did not integrate AI collaboration. Each tool 
solved part of the problem; integration lagged.

**Explanation 4 — AI collaboration is recent.** Until 2022-2023, 
collaborative AI work at this depth was not feasible. 
Infrastructure built before then could not anticipate the 
workflow that emerged. Infrastructure built in the last three 
years is mostly focused on the chat layer, where the 
immediate need was visible.

**Explanation 5 — Concentration of effort on extremes.** 
Both Anthropic and OpenAI focus their product investment on 
the chat layer (most accessible) and on agent infrastructure 
(most futuristic). The middle layer — workspace for sustained 
intellectual collaboration — is less glamorous and gets less 
investment.

This last point matters. Layer B is not a research challenge. 
It is a product challenge. The components needed exist. The 
integration does not.

---

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Why This Hasn t Been Built"
```

## Смотрите также
- [278-why-this-hasn-t-been-built](../../02-anthropic-vacancies/278-why-this-hasn-t-been-built.md)
- [06-existing-approximations](06-existing-approximations.md)
- [01-missing-middle-layer](01-missing-middle-layer.md)
- [02-why-document-exists](02-why-document-exists.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (7):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [12-closing](12-closing.md)
- [README](README.md)

