# Personal multi-agent hub

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — расширенные примеры с Хабра по варианту D (поиск ещё уникальных проектов).

---
<!-- tags: architecture, anthropic, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — расширенные примеры с Хабра по варианту D (поиск ещё уникальных проектов).

Что получается: Personal multi-agent hub:

Local AI infrastructure (BrainBox-style hosting)

Files-as-config для agent roles (.ai/agents/ pattern)

Decomposition patterns (WorkTeam supervisor → orchestrator → filler)

CAMEL для actual coordination

Применение: Personal SGB Advocate с specialized sub-agents:

agents/01_legal_research.md — для поиска precedent

agents/02_drafting.md — для составления документов

agents/03_citation_checker.md — для проверки ссылок

agents/04_strategic_advisor.md — для общей стратегии

Все work через CAMEL coordination, hosted locally в style BrainBox.

Это очень близко к Document 7 (Composite Skills Agent), но с конкретными templates и patterns из real Хабр-работающих проектов.

Синтез D: «Federated knowledge marketplace для уязвимых групп»

Совмещение: Свяжи (collaboration matching) + info40 (marketplace concept) + Document 5 (Representative Agent Layer) + Nautilus Portal Protocol (Document 1).

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Personal multi agent hub"
```

## Смотрите также
- [07-specialized-knowledge-workspace](07-specialized-knowledge-workspace.md)
- [06-platform-for-professional-communities](06-platform-for-professional-communities.md)
- [09-federated-platform](09-federated-platform.md)
- 04-[claude-subagents-patterns](04-claude-subagents-patterns.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ доступен для семантического поиска, BM25 и навигации через граф связей репозитория._ _Индексировано в поисковой базе репозитория Lorenzo._ _Индексировано._

<!-- backlinks -->

---

**Кто ссылается на этот документ (15):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [05-existing-infrastructure-stack](../../anthropic-vacancies/extra-collaborator-findings/05-existing-infrastructure-stack.md)
- [03-sgb-advocate-colleague-example](../../anthropic-vacancies/nautilus-vs-camel/03-sgb-advocate-colleague-example.md)
- [04-claude-subagents-patterns](04-claude-subagents-patterns.md)
- _...ещё 7_


<!-- similar-docs -->

---

**Похожие документы:**
- [08-personal-multi-agent-hub](../../obsidian/habr-unique-projects/extra-examples/08-personal-multi-agent-hub.md) (сходство 0.94)
- [07-specialized-knowledge-workspace](07-specialized-knowledge-workspace.md) (сходство 0.41)
- [09-federated-platform](09-federated-platform.md) (сходство 0.40)

