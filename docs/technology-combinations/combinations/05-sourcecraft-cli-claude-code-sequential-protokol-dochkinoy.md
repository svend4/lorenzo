# Комбинация 5: SourceCraft CLI × Claude Code × Sequential протокол Дочкиной

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---
<!-- tags: orchestration, collaboration -->




> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

SourceCraft CLI (habr.com/ru/news/1026498/) — Яндекс, консольное приложение с ИИ-агентом, skills (сценарии), накопление знаний команды

Claude Code — CLI с bash, MCP, subagents

Sequential протокол (habr.com/ru/articles/1017200/) — 8-16 малых агентов, каждый видит результаты предшественников, 44% качества выше координатора

Дети:

5.1 Distributed code review без координатора

Вместо одного агента-ревьюера — Sequential цепочка:

Agent-style — проверяет стиль и форматирование

Agent-logic — ищет логические баги

Agent-security — ищет уязвимости

Agent-performance — ищет узкие места

Каждый видит комментарии предыдущих, не дублирует. Все дешёвые модели (Haiku/DeepSeek), но вместе дают качество Opus.

5.2 Team knowledge graph через skills

SourceCraft-skills + MCP-серверы + durable state:

Каждый skill фиксирует паттерн решения

Skills сохраняются в корпоративный граф знаний через MCP

Новый разработчик получает автоматически релевантные skills для своей задачи

Для Max'а: legal skills (german-legal-deadline-calculator + court-document-analyzer) становятся частью командного графа, доступны всем через SourceCraft CLI.

<!-- see-also -->

---

**Смотрите также:**
- [02-knowledge-graphs](docs/03-technology-combinations/02-knowledge-graphs.md)
- [09-agent-orchestration-stack](docs/technology-combinations/combinations/09-agent-orchestration-stack.md)
- [02-multiagentnyy-khaos-reshenie-auto-ai-router](docs/technology-combinations/combinations/02-multiagentnyy-khaos-reshenie-auto-ai-router.md)
- [16-adversarial-multi-agent-code-review](docs/technology-combinations/combinations/16-adversarial-multi-agent-code-review.md)

