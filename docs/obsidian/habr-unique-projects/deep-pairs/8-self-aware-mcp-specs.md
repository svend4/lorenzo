---
title: "Пара 8 — Self-aware MCP × Specs-first архитектура"
tags:
  - knowledge
  - architecture
  - collaboration
  - habr-unique-projects
date: 2026-04-29
---

# Пара 8 — Self-aware MCP × Specs-first архитектура

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

---
<!-- tags: knowledge, architecture, collaboration -->




> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Пара 8. Self-aware MCP × Specs-first архитектура

Self-aware MCP server vuguzum (https://habr.com/ru/articles/1007122/, github.com/vuguzum/self-aware-mcp-server) — даёт агенту знание про OS / локацию / время. Реализован одновременно на Python, TypeScript и C#. AI-бот для самопознания PDA-архитектуры из прошлых ответов (https://habr.com/ru/articles/1027210/) — event sourcing, LLM как периферия, Stability Engine. Specs-first паттерн из iOS-материала: CLAUDE.md + AGENTS.md + .cursorrules + markdown-спека на каждую фичу.

Дети:

Possibility-Driven legal architecture — каждое заседание Sozialgericht — неизменяемое событие, статус дела — read model поверх event log, Stability Engine отвечает за класс решений, которые LLM не должен принимать никогда (например, «никогда не отправлять Klage без человеческого подтверждения» или «никогда не пропускать Frist»). Агент может предлагать, но финальные действия — через Stability Engine с явным human-in-the-loop. Чисто архитектурно — то, что нужно для legal-чувствительной системы.

Spec на каждое дело как первоисточник — у тебя сейчас 41 тематический файл в S 7 SO 99/25 case. Если каждый файл — это spec в формате как .cursor/plans/, агент читает их как контракт, и любая работа над делом начинается с уточнения spec, а не с кода. Это превращает legal documentation в исполняемую структуру: агент сверяет каждый шаг с spec и не может «забыть» про важный пункт.

Self-aware legal MCP — агент знает «сейчас 26 апреля 2026, я в Дрездене, активные дедлайны: S 6 SO 58/26 ER (🔴 3 дня), S 7 SO 99/25 (🟡 14 дней), часовой пояс Europe/Berlin». Не путает регионы (Saxon vs Bavaria), не считает выходные как рабочие дни, автоматически выбирает приоритет для top-of-day-greeting.

Ансамбль 1: «Один человек = одна компания»

Возьми пары 1 + 4 + 5 + 6, поставь поверх vault'а из пары 2:

<!-- see-also -->

---

**Смотрите также:**
- [[03-pda-llm-as-periphery]]
- [[5-browser-agents-headless]]
- [[4-skill-catalogs-subagents]]
- [[3-adversarial-multi-ide]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[03-pda-llm-as-periphery]] (сходство 0.21)
- [[3-adversarial-multi-ide]] (сходство 0.18)
- [[1-workflow-llm-mcp]] (сходство 0.18)

