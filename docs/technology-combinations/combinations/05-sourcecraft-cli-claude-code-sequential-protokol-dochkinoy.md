# Комбинация 5: SourceCraft CLI × Claude Code × Sequential протокол Дочкиной

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---
<!-- tags: orchestration, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





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

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Комбинация 5 SourceCraft CLI Claude"
```

## Смотрите также
- [02-knowledge-graphs](../../03-technology-combinations/02-knowledge-graphs.md)
- [09-agent-orchestration-stack](09-agent-orchestration-stack.md)
- [02-multiagentnyy-khaos-reshenie-auto-ai-router](02-multiagentnyy-khaos-reshenie-auto-ai-router.md)
- [16-adversarial-multi-agent-code-review](16-adversarial-multi-agent-code-review.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [components-by-name](../../glossary/components-by-name.md)
- [README](README.md)
- [01-08-summary](../synthesis-tables/01-08-summary.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в базе репозитория Lorenzo и доступен для семантического поиска._ _Доступен семантический поиск._ _Индексировано._

<!-- similar-docs -->

---

**Похожие документы:**
- [05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy](../../obsidian/technology-combinations/combinations/05-sourcecraft-cli-claude-code-sequential-protokol-dochkinoy.md) (сходство 0.97)
- [02-knowledge-graphs](../../obsidian/03-technology-combinations/02-knowledge-graphs.md) (сходство 0.32)
- [02-knowledge-graphs](../../03-technology-combinations/02-knowledge-graphs.md) (сходство 0.31)

