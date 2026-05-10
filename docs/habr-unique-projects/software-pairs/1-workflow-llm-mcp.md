# Пара 1 — Workflow-автоматизация × LLM-агенты с MCP

<!-- toc-auto -->
## Contents

- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

---
<!-- tags: rag, orchestration, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Пара 1. Workflow-автоматизация × LLM-агенты с MCP

Родители: open-source автоматизаторы — Activepieces (no-code, AI-native, простой self-host), Windmill (script-first для Python/TS/Go/Bash, h-class developer-friendly), Huginn (event-driven scraping и веб-агенты), Node-RED (4000+ нод, IoT-родом). Каждый из них поодиночке слабее Make.com или n8n по экосистеме, но открыт и self-hostable. И — Claude Code + MCP с subagents и skills (https://habr.com/ru/articles/938626/, habr.com/ru/articles/987094/). У MCP богатая агентность, но нет визуального оркестратора и нет надёжного детерминированного fallback.

Дети:

Visual orchestrator над Claude subagents — Activepieces как drag-and-drop визуализация над всеми 87 твоими skills (multi-chat-orchestrator, legal-domain-manager). Бизнес-процесс рисуется юристом-непрограммистом, но каждый шаг — это вызов MCP с конкретным skill'ом. Получается: «детерминированный flow + LLM-узлы там, где нужна интерпретация». Для немецкого Sozialrecht это снимает требование, чтобы все пользователи понимали Claude Code.

Headless ночной DevOps-юрист — Windmill (Python/TS) + Claude Code в headless mode (флаг -p, https://habr.com/ru/companies/surfstudio/articles/943108/) на одной немецкой VPS: cron каждое утро обходит сайты Sozialgericht/BSG/KSV, генерирует Stellungnahme-черновики, обновляет статусы Aktenzeichen. UI не нужен — всё через slack-/telegram-уведомления.

Event-driven legal watcher — Huginn собирает RSS/обновления сайтов + кастомный MCP-сервер (паттерн self-aware-mcp-server, habr.com/ru/articles/1007122/) + LLM-классификатор. «Заседание перенесли — пришёл alert; новый Urteil BSG, релевантный нашему делу — пришёл alert». Делает то, что обычно делает чиновник руками.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Пара 1 Workflow автоматизация LLM"
```

## Смотрите также
- [4-skill-catalogs-subagents](../deep-pairs/4-skill-catalogs-subagents.md)
- [5-browser-agents-headless](5-browser-agents-headless.md)
- [6-tmux-village-openclaw](../deep-pairs/6-tmux-village-openclaw.md)
- 8-self-aware-[mcp-specs](../deep-pairs/8-self-aware-mcp-specs.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (11):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [components-by-name](../../glossary/components-by-name.md)
- [3-adversarial-multi-ide](../deep-pairs/3-adversarial-multi-ide.md)
- [4-skill-catalogs-subagents](../deep-pairs/4-skill-catalogs-subagents.md)
- _...ещё 3_

