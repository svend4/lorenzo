---
title: "Пара 5 — Browser agents × headless web extraction"
tags:
  - habr-unique-projects
date: 2026-04-29
---

# Пара 5 — Browser agents × headless web extraction

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).
**Проекты:** Firecrawl, Yjs, Automerge, Whisper

---
<!-- tags: knowledge, ingestion, local-first, architecture, collaboration -->




> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Пара 5. Browser agents × headless web extraction

Родители: Claude in Chrome / Claude Cowork (агент с глазами и руками в браузере, https://habr.com/ru/articles/1009958/) и программные веб-движки — Firecrawl (https://habr.com/ru/articles/1020598/, чистый markdown из любой страницы через MCP), Browser Use, Playwright. Поодиночке: интерактивная автоматизация vs программная. Вместе — гибридный пайплайн.

Дети:

Hybrid web pipeline — Firecrawl MCP для массового регулярного сбора (sites.de, justiz.de, KSV-портал по schedule) + Cowork включается только тогда, когда сайт требует 2FA или интерактивного клика. Дешевле всего: Firecrawl ест 99% трафика, Cowork решает редкие сложные случаи.

AI-driven inbox-zero для legal — Cowork забирает входящие документы из e-mail/портала, Firecrawl чистит до markdown, твой german-legal-template-generator skill классифицирует, всё попадает в Obsidian через MCP. Полный конвейер от пришедшего письма до структурированной заметки в vault'е без ручного копи-пасты.

Self-aware agent с пониманием контекста — self-aware MCP-сервер (https://habr.com/ru/articles/1007122/, github.com/vuguzum/self-aware-mcp-server) добавляет агенту знание про текущую OS / локейшн / время. Для legal-стека это снимает класс ошибок: агент сам понимает, что Sitzung завтра 10:00 в Дрездене, что текущая ОС Linux, и что cron должен быть в Europe/Berlin. Не путает PowerShell с bash, не теряет часовые пояса.

Главная рационализация: пять кубиков заменяют стек подписок

Это уже не «новый проект», а резкое сжатие существующих расходов и зависимостей. Типичный стек для одного человека сейчас выглядит так: Make.com (~$30/mo) + Notion AI (~$20) + Notion Sync (включено) + Otter.ai (~$17) + Granola (~$18) + Wispr Flow (~$15) + Obsidian Sync (~$5) + ChatGPT Plus / Claude Pro (~$20). Итого около $120/мес при том, что данные размазаны по семи юрисдикциям.

Замена из open-source кубиков:

слой 1 — Activepieces self-hosted (вместо Make.com)

слой 2 — Obsidian + LLM Wiki плагин + Skills (вместо Notion AI)

слой 3 — Yjs/Automerge + IndexedDB + кастомный relay (вместо Notion Sync и Obsidian Sync)

слой 4 — Whisper.cpp + Handy + diarization-pipeline (вместо Otter.ai + Granola + Wispr Flow)

слой 5 — локальная LLM на собственном железе (вместо подписки на frontier-модель — для рутины; топовая модель остаётся только для трудных задач)

Стоимость: $0/мес + однократно VPS €4-10/мес для relay. Все данные на твоих машинах, ничего не уходит во внешние юрисдикции — что для GDPR-чувствительной legal работы и для приватного research-vault'а критично. Самое интересное: каждый из пяти кубиков по отдельности — посредственная замена соответствующего SaaS, но связка из всех пяти даёт качество, которого ни один SaaS-стек не предлагает, потому что данные лежат в одной плоскости и видны всем слоям сразу.

<!-- see-also -->

---

**Смотрите также:**
- [[8-self-aware-mcp-specs]]
- [[1-workflow-llm-mcp]]
- [[3-crdt-self-hosted]]
- [[2-pkm-mcp-skills]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[8-self-aware-mcp-specs]] (сходство 0.17)
- [[1-workflow-llm-mcp]] (сходство 0.17)
- [[3-crdt-self-hosted]] (сходство 0.15)

