# HW-NL2Workflow — Supervisor/Orchestrator/Filler с 3600+ examples

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
<!-- tags: rag, anthropic, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — расширенные примеры с Хабра по варианту D (поиск ещё уникальных проектов).

Что делает: Multi-agent framework для перевода natural language инструкций в business processes. Три агента: Supervisor, Orchestrator, Filler. Свой dataset HW-NL2Workflow с 3600+ примерами.

Уникальное:

Decomposition подход: каждый агент решает узкую подзадачу

Использует SentenceBERT для component matching

Открытый dataset для обучения

Состояние: Research project с paper.

Несколько других интересных направлений

Беглый просмотр Хабра показывает ещё несколько паттернов:

Telegram-бот ассистенты с RAG over personal documents — много вариантов, разные авторы

n8n + LLM workflow automation для personal use cases

Локальные кодовые агенты (BVM team подход)

Self-hosted второй мозг через Claude Code + Obsidian

Возможные синтезы — какие проекты вместе создают что-то уникальное

Теперь к самому интересному. Вижу несколько продуктивных синтезов, где совмещение нескольких проектов creates что-то greater than parts.

Синтез A: «Профессиональное community matching с глубокими профилями»

Совмещение: Свяжи (deep profiles + collaboration matcher) + Научный нетворкинг ВШЭ (микро-коллаборации) + ваш OKWF concept (Document 4).

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "HW NL2Workflow Supervisor Orchestrator"
```

## Смотрите также
- [08-personal-multi-agent-hub](08-personal-multi-agent-hub.md)
- [06-platform-for-professional-communities](06-platform-for-professional-communities.md)
- [03-brainbox-multi-ai-hub](03-brainbox-multi-ai-hub.md)
- [10-profession-specific-workflows](10-profession-specific-workflows.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ доступен для семантического поиска и навигации._ _Доступен поиск._

<!-- backlinks -->

---

**Кто ссылается на этот документ (9):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [00-question-habr-examples](00-question-habr-examples.md)
- [03-brainbox-multi-ai-hub](03-brainbox-multi-ai-hub.md)
- [06-platform-for-professional-communities](06-platform-for-professional-communities.md)
- _...ещё 1_


<!-- similar-docs -->

---

**Похожие документы:**
- [05-hw-nl2workflow](../../obsidian/habr-unique-projects/extra-examples/05-hw-nl2workflow.md) (сходство 0.98)
- [08-personal-multi-agent-hub](../../obsidian/habr-unique-projects/extra-examples/08-personal-multi-agent-hub.md) (сходство 0.32)
- [08-personal-multi-agent-hub](08-personal-multi-agent-hub.md) (сходство 0.32)

