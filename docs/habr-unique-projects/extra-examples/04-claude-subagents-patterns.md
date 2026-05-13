# Claude subagents patterns

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
<!-- tags: anthropic, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — расширенные примеры с Хабра по варианту D (поиск ещё уникальных проектов).

Что есть: Practical patterns для использования AI sub-agents в разработке:

.ai/agents/ папка с промптами для разных ролей (epic-writer, dev-plan-writer, php-developer, и т.д.)

Cursor sub-agents через cursor-agent CLI

Orchestrator pattern в .ai/agents/01_orchestrator.md

Уникальное:

Файлы как промпты-конфигурации — agents живут в репозитории

Шаблоны документов в YAML для context engineering

Орchestrator выбирает sub-agents под задачу

Состояние: Live patterns, используются в production.

Проект 6: WorkTeam (исследовательский)

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Claude subagents patterns"
```

## Смотрите также
- [08-personal-multi-agent-hub](08-personal-multi-agent-hub.md)
- [02-vshe-scientific-networking](02-vshe-scientific-networking.md)
- [00-question-habr-link](../../nautilus/community-discussions/habr-article-1-reaction/00-question-habr-link.md)
- [07-specialized-knowledge-workspace](07-specialized-knowledge-workspace.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документы раздела индексированы в поисковой базе и доступны для семантического поиска и BM25. Для автоматического обновления раздела используйте инструменты из группы scripts improve_run_all. Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов.

<!-- backlinks -->

---

**Кто ссылается на этот документ (10):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [01-svyazi-andrey-chuyan](01-svyazi-andrey-chuyan.md)
- [02-vshe-scientific-networking](02-vshe-scientific-networking.md)
- [03-brainbox-multi-ai-hub](03-brainbox-multi-ai-hub.md)
- _...ещё 2_


<!-- similar-docs -->

---

**Похожие документы:**
- [04-claude-subagents-patterns](../../obsidian/habr-unique-projects/extra-examples/04-claude-subagents-patterns.md) (сходство 0.94)
- [00-question-habr-link](../../obsidian/nautilus/community-discussions/habr-article-1-reaction/00-question-habr-link.md) (сходство 0.52)
- [00-question-habr-link](../../nautilus/community-discussions/habr-article-1-reaction/00-question-habr-link.md) (сходство 0.50)

