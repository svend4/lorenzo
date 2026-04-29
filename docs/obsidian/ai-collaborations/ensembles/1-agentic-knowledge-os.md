---
title: "Ансамбль 1 — Agentic Knowledge OS"
tags:
  - memory
  - rag
  - knowledge
  - ingestion
  - architecture
  - collaboration
  - ai-collaborations
date: 2026-04-29
---

# Ансамбль 1 — Agentic Knowledge OS

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).
**Проекты:** Svyazi, AgentFS, knowledge-space

---
<!-- tags: memory, rag, knowledge, ingestion, architecture, collaboration -->




> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

1. Agentic Knowledge OS: «память для агентов, не для людей»

Родители: Svyazi + AgentFS + knowledge-space + Memory OS + Context Engineering.

На Хабре есть сильная линия проектов, где знания начинают храниться не как обычные заметки для человека, а как операционная среда для AI-агентов. В статье про AgentFS автор описывает CLI, который разворачивает Obsidian vault как «операционную систему» для агентов: есть User Space для человека, Native Runtimes для конфигов Claude/Cursor/OpenClaw и Kernel Space .agentos/ как единый source of truth. Habr

Второй кубик — проект knowledge-space: автор собирает результаты deep research из разных чатов Claude в общий research/inbox/, затем отдельная сессия перерабатывает сырой ресёрч в карточки, убирает дубли, добавляет wiki-links, гоняет build и пушит изменения; один проход даёт 20–40 новых или обогащённых карточек. Habr

Третий кубик — Context Engineering: там CLAUDE.md трактуется не как «простыня инструкций», а как карта проекта, MEMORY.md — как индекс памяти, а Skills — как «книга на полке», которая грузится только по необходимости; AutoDream делает фоновую консолидацию памяти между сессиями. Habr

Четвёртый кубик — Memory OS: авторы уходят от flat RAG к многослойной памяти с Semantic Mapper, Knowledge Graph, Reflective Memory Layer и обязательным source provenance; каждое утверждение синтезирующего агента должно иметь ссылку на Concept ID или Source UUID, иначе ответ считается невалидным. Habr

Что рождается при склейке:

Получается агентная база знаний нового типа: не Obsidian, не RAG, не CRM, не wiki, а гибрид.

Схема:

сырой текст / чат / ресёрч / профиль человека → Svyazi-like extraction → карточка → knowledge-space → AgentFS → Memory OS → MCP-доступ для агентов

Дети этой связки:

Research Refinery — все результаты ресёрча из Claude/GPT/Gemini автоматически превращаются в карточки с источниками, связями и статусами.

Community Brain — Svyazi для сообщества, где карточки не только про людей, но и про проекты, идеи, навыки, боли, инструменты, открытые задачи.

Legal/Research Case OS — каждое дело, научная гипотеза или технический проект живёт как набор проверяемых карточек, а агент работает не с «памятью чата», а с устойчивой операционной системой знаний.

Главное новое свойство: агент больше не начинает каждый раз с нуля. Он входит в уже структурированную среду, где есть память, источники, связи, границы и история изменений.

<!-- see-also -->

---

**Смотрите также:**
- [[7-domain-agent-app-factory]]
- [[9-ambient-team-agent]]
- [[4-web-to-knowledge-pipeline]]
- [[2-distributed-agent-workshop]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[9-ambient-team-agent]] (сходство 0.18)
- [[2-distributed-agent-workshop]] (сходство 0.18)
- [[7-domain-agent-app-factory]] (сходство 0.17)

