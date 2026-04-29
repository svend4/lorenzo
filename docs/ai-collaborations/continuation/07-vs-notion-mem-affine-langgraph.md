# Чем Svyazi 2.0 отличается от Notion AI / Mem / AFFiNE / LangGraph

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).
**Проекты:** Svyazi, CardIndex

---
<!-- tags: rag, knowledge, ingestion, local-first, architecture, collaboration -->




> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

7. Чем Svyazi‑2.0 отличается от Notion AI, Mem, AFFiNE и LangGraph‑стеков

Против Notion AI

Notion AI Enterprise Search уже умеет искать по Notion и подключённым приложениям вроде Slack, Google Drive, GitHub, Jira, Teams, SharePoint и OneDrive; он даёт ответы с citations, research reports, permission‑aware search, no training on customer data и enterprise compliance controls. Notion

Но Notion AI — это прежде всего workspace search + productivity AI. Svyazi‑2.0 в предлагаемой конфигурации — это collaboration discovery system: она не только отвечает на вопросы по базе, а строит карточки людей/проектов/эпизодов, отслеживает weak signals, ведёт review queue, различает raw/inferred/approved, объясняет match через evidence и память. Notion сильнее как готовый enterprise workspace; Svyazi‑2.0 сильнее как специализированная машина поиска коллабораций и структурированных связей.

Против Mem

Mem позиционируется как “AI Thought Partner”: Voice Mode, Mem Chat, Heads Up, Deep Search, автоматическое связывание заметок, capture через extension/email/share и offline/sync across Mac/Windows/iOS/Web. Mem Помощь

Но Mem в первую очередь строит личную или индивидуально‑командную knowledge memory. Svyazi‑2.0 должна строить социально‑проектный граф: кто может с кем работать, почему, на основании каких источников, с каким риском, кто подтвердил, какие гипотезы устарели. Mem хорош как “вспомнить мои мысли”; Svyazi‑2.0 — как “найти людей, проекты и скрытые комбинации”.

Против AFFiNE

AFFiNE силён как privacy‑first, local‑first, open-source workspace, объединяющий docs, whiteboards и databases; в свежем материале AFFiNE подчёркивает open source, отсутствие vendor lock‑in, local-first владение данными и связку документов/whiteboard/database в одной среде. AFFiNE

AFFiNE может быть отличным UI/vault substrate для Svyazi‑2.0, но сам по себе не даёт Svyazi‑логики: verified/claimed/inferred, CardIndex, collaboration cards, Evidence Envelope, memory governance, moderation protocol. Иначе говоря, AFFiNE — кандидат на “тело” интерфейса; Svyazi‑2.0 — кандидат на “нервную систему” discovery.

Против LangGraph‑based RAG систем

LangGraph официально позиционируется как низкоуровневый orchestration framework/runtime для long‑running stateful agents с durable execution, streaming, HITL и persistence. Его persistence layer сохраняет graph state как checkpoints, поддерживает threads, memory, time travel и fault tolerance. Документация LangChain+1

Но LangGraph — это runtime, а не доменная система. Он помогает построить workflow, но не решает сам по себе: какую карточку считать истиной, как отделить proposal от fact, как объяснять коллаборацию, как модерировать inferred‑значения, как нормализовать навыки и проекты. Svyazi‑2.0 может использовать LangGraph‑паттерны для HITL и stateful workflows, но её ценность выше уровня orchestration.

<!-- see-also -->

---

**Смотрите также:**
- [14-ограничения-лицензии-и-что-пока-лучше-не-склеивать](docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md)
- [03-a2a-vs-mcp-protocols](docs/ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md)
- [05-roadmap-6-12-months](docs/ai-collaborations/continuation/05-roadmap-6-12-months.md)
- [02-agentops-trace-envelope](docs/ai-collaborations/continuation/02-agentops-trace-envelope.md)

