# Пара 1 — Workflow-автоматизация × LLM-агенты с MCP

> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Пара 1. Workflow-автоматизация × LLM-агенты с MCP

Родители: open-source автоматизаторы — Activepieces (no-code, AI-native, простой self-host), Windmill (script-first для Python/TS/Go/Bash, h-class developer-friendly), Huginn (event-driven scraping и веб-агенты), Node-RED (4000+ нод, IoT-родом). Каждый из них поодиночке слабее Make.com или n8n по экосистеме, но открыт и self-hostable. И — Claude Code + MCP с subagents и skills (https://habr.com/ru/articles/938626/, habr.com/ru/articles/987094/). У MCP богатая агентность, но нет визуального оркестратора и нет надёжного детерминированного fallback.

Дети:

Visual orchestrator над Claude subagents — Activepieces как drag-and-drop визуализация над всеми 87 твоими skills (multi-chat-orchestrator, legal-domain-manager). Бизнес-процесс рисуется юристом-непрограммистом, но каждый шаг — это вызов MCP с конкретным skill'ом. Получается: «детерминированный flow + LLM-узлы там, где нужна интерпретация». Для немецкого Sozialrecht это снимает требование, чтобы все пользователи понимали Claude Code.

Headless ночной DevOps-юрист — Windmill (Python/TS) + Claude Code в headless mode (флаг -p, https://habr.com/ru/companies/surfstudio/articles/943108/) на одной немецкой VPS: cron каждое утро обходит сайты Sozialgericht/BSG/KSV, генерирует Stellungnahme-черновики, обновляет статусы Aktenzeichen. UI не нужен — всё через slack-/telegram-уведомления.

Event-driven legal watcher — Huginn собирает RSS/обновления сайтов + кастомный MCP-сервер (паттерн self-aware-mcp-server, habr.com/ru/articles/1007122/) + LLM-классификатор. «Заседание перенесли — пришёл alert; новый Urteil BSG, релевантный нашему делу — пришёл alert». Делает то, что обычно делает чиновник руками.
