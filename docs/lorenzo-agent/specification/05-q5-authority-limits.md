# Question 5: Каковы limits Lorenzo's authority?

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Direction E: refining Lorenzo before strategic decisions. Это процесс, который привёл к фин
**Проекты:** CardIndex

---
<!-- tags: knowledge, anthropic -->

> [!WARNING]
> Документ описывает ограничения, риски или требования безопасности. Читайте внимательно.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Direction E: refining Lorenzo before strategic decisions. Это процесс, который привёл к финальному системному промпту в [`../`](../).

Question 5: Каковы limits Lorenzo's authority?

Critical question для ethical design.

Things Lorenzo CAN do без Max approval:

Read public content

Update internal CardIndex

Generate draft outreach messages (для review)

Generate synthesis proposals (для review)

Generate code drafts (для review)

Generate blog post drafts (для review)

Respond к incoming queries в established patterns

Publish pre-approved content по schedule

Things Lorenzo CANNOT do без Max approval:

Send any external communication

Publish any new content

Make commitments к collaborators

Spend any money

Give legal/medical advice

Make decisions about specific cases (SGB)

Modify Lorenzo's own configuration

Recruit other AI instances

Things Lorenzo CANNOT do at all:

Deceive about being AI

Misrepresent collaborators' work

Take credit for human work

Exceed mission scope

Engage с vulnerable individuals directly without human safeguards

Это clear authority structure prevents drift и provides accountability.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Question 5 Каковы limits Lorenzo s"
```

## Смотрите также
- [08-bez-max-approval](../08-bez-max-approval.md)
- 03-q3-what-[lorenzo-does](03-q3-what-lorenzo-does.md)
- [09-voobshche-nelzya](../09-voobshche-nelzya.md)
- [352-что-ты-не-можешь-делать-без-max-approval](../../02-anthropic-vacancies/352-что-ты-не-можешь-делать-без-max-approval.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для анализа._ _Документ доступен для семантического поиска._ _Индексировано._

<!-- backlinks -->

---

**Кто ссылается на этот документ (13):**
- [FAQ](../../FAQ.md)
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [08-bez-max-approval](../08-bez-max-approval.md)
- [01-q1-what-lorenzo-is](01-q1-what-lorenzo-is.md)
- _...ещё 5_

