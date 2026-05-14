---
state: approved
---

# Сходство 3: MCP support

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

Сходство 3: MCP support

Hermes полностью поддерживает MCP. Это значит, что:

InGit MCP server, который мы планировали, работал бы и с Hermes

Любые специализированные sub-agent MCP servers работали бы с обоими

Архитектура переносима между Cowork и Hermes

Это хорошая новость для нашего общего подхода. Не нужно выбирать между ними — структура совместима.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Сходство 3 MCP support"
```

## Смотрите также
- [04-similarity-4-multi-platform](04-similarity-4-multi-platform.md)
- [02-similarity-2-persistent-memory](02-similarity-2-persistent-memory.md)
- [05-similarity-5-self-hosting-privacy](05-similarity-5-self-hosting-privacy.md)
- [09-difference-4-institutional-vision](09-difference-4-institutional-vision.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документы раздела индексированы в поисковой базе и доступны для семантического поиска и BM25. Для автоматического обновления раздела используйте инструменты из группы scripts improve_run_all. Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов.

<!-- backlinks -->

---

**Кто ссылается на этот документ (13):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [02-similarity-2-persistent-memory](02-similarity-2-persistent-memory.md)
- [04-similarity-4-multi-platform](04-similarity-4-multi-platform.md)
- [05-similarity-5-self-hosting-privacy](05-similarity-5-self-hosting-privacy.md)
- _...ещё 5_


<!-- similar-docs -->

---

**Похожие документы:**
- [03-similarity-3-mcp-support](../../obsidian/anthropic-vacancies/hermes-comparison/03-similarity-3-mcp-support.md) (сходство 0.98)
- [02-similarity-2-persistent-memory](02-similarity-2-persistent-memory.md) (сходство 0.62)
- [04-similarity-4-multi-platform](../../obsidian/anthropic-vacancies/hermes-comparison/04-similarity-4-multi-platform.md) (сходство 0.61)

