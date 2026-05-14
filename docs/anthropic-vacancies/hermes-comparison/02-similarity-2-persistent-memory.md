---
state: approved
---

# Сходство 2: Persistent memory — Layer B функциональность

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Resear

---
<!-- tags: architecture, anthropic -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Research.

Сходство 2: Persistent memory — Layer B функциональность

Hermes имеет three-layer memory: FTS5 search, LLM summarization, Honcho user modeling. Это substantially решает многие из тех проблем, которые Document 2.3 идентифицировал как Layer B gap.

Cowork также имеет persistent memory, но Hermes идёт дальше — autonomous skill creation означает, что агент сам определяет, что worth remembering, без явного указания пользователя.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Сходство 2 Persistent memory Layer B"
```

## Смотрите также
- 03-similarity-3-[mcp-support](03-similarity-3-mcp-support.md)
- [04-similarity-4-multi-platform](04-similarity-4-multi-platform.md)
- [09-difference-4-institutional-vision](09-difference-4-institutional-vision.md)
- [07-difference-2-domain-specialization](07-difference-2-domain-specialization.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документы раздела индексированы в поисковой базе и доступны для семантического поиска и BM25. Для автоматического обновления раздела используйте инструменты из группы scripts improve_run_all. Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo.

<!-- backlinks -->

---

**Кто ссылается на этот документ (14):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [00-question-what-is-hermes](00-question-what-is-hermes.md)
- [01-similarity-1-composite-skills](01-similarity-1-composite-skills.md)
- [03-similarity-3-mcp-support](03-similarity-3-mcp-support.md)
- _...ещё 6_


<!-- similar-docs -->

---

**Похожие документы:**
- [02-similarity-2-persistent-memory](../../obsidian/anthropic-vacancies/hermes-comparison/02-similarity-2-persistent-memory.md) (сходство 0.98)
- [03-similarity-3-mcp-support](03-similarity-3-mcp-support.md) (сходство 0.62)
- [03-similarity-3-mcp-support](../../obsidian/anthropic-vacancies/hermes-comparison/03-similarity-3-mcp-support.md) (сходство 0.61)

