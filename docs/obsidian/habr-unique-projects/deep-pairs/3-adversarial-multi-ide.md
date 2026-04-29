---
title: "Пара 3 — Adversarial agents × Multi-IDE стек"
tags:
  - collaboration
  - habr-unique-projects
date: 2026-04-29
---

# Пара 3 — Adversarial agents × Multi-IDE стек

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

---
<!-- tags: collaboration -->




> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Пара 3. Adversarial agents × Multi-IDE стэк

adversarial-review Дмитрия Дементьева (https://habr.com/ru/articles/1019588/, github.com/dementev-dev/adversarial-review) — скилл, в котором Claude Opus пишет план/код, Codex CLI его ревьюит, разные «мышления» ловят разные баги. Цикл план → ревью → код → ревью → APPROVED/REVISE до 5 раундов. Сравнение 12 агентских IDE (https://habr.com/ru/articles/975414/) — Cursor/Kiro/Claude Code/Roo Code/Kilo Code/Antigravity/Cline/WindSurf/Continue/TRAE/Qode/Warp ADE/Zed. Continue + Ollama офлайн за 15 минут (https://habr.com/ru/articles/1027658/) — qwen3-coder:30b + nomic-embed-text для индексации проекта. Серена MCP + Xcode MCP + Figma MCP + Vision-сравнение в iOS-сетапе (https://habr.com/ru/articles/1027382/).

Дети:

Adversarial review в legal flow — две модели Max'a: Claude Opus генерирует Stellungnahme, Codex/GPT-5.4 ревьюит на полноту аргументов, ссылки на Aktenzeichen, согласованность с § ссылками. Цикл повторяется до APPROVED. Это не про код, это про юридический текст — но паттерн один в один. Снимает класс ошибок «модель что-то забыла» без ручного перепроверять.

Specs-first iOS-style для legal — паттерн из iOS-разработки (CLAUDE.md + AGENTS.md + .cursorrules + skills.sh + Serena MCP): для legal это значит markdown-спека на каждое дело в .agents/case-protocol.md, ссылки на skills, обязательные правила («ни один Stellungnahme без проверки deadline и без Aktenzeichen»), Vision-сравнение для сверки PDF-форм по существующему шаблону. Дело переживает сессию: вернулся через две недели — контекст за минуту. Это Spisak-паттерн «второй мозг», но не в Obsidian, а прямо в репо проекта.

Continue полностью офлайн — для legal с GDPR-чувствительностью это особенно важно: Cursor/Claude Code отправляют код на серверы, Continue + Ollama работает на ноутбуке. qwen3-coder:30b, nomic-embed-text, 80k context, 8k max tokens, температура 0.2. Конфигурация на 50 строк yaml. Полная независимость от внешних API.

<!-- see-also -->

---

**Смотрите также:**
- [[4-skill-catalogs-subagents]]
- [[8-self-aware-mcp-specs]]
- [[1-workflow-llm-mcp]]
- [[6-tmux-village-openclaw]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[4-skill-catalogs-subagents]] (сходство 0.19)
- [[1-workflow-llm-mcp]] (сходство 0.19)
- [[8-self-aware-mcp-specs]] (сходство 0.18)

