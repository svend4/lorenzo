# Сходство 5: Self-hosting и privacy

<!-- toc-auto -->
## Contents

- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Resear

---
<!-- tags: local-first, architecture, anthropic -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Research.

Сходство 5: Self-hosting и privacy

Hermes полностью self-hosted, MIT license, all data stays on your machine. Это точно соответствует offline-first философии InGit. На самом деле, Hermes реализует то, что InGit стремится быть — minus файловые конвенции и Git-нативную структуру.

Чем Hermes отличается — где наши документы добавляют value

Несмотря на впечатляющий functionality Hermes, есть несколько важных различий, где наша архитектура остаётся релевантной.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Сходство 5 Self hosting и privacy"
```

## Смотрите также
- 03-similarity-3-[mcp-support](03-similarity-3-mcp-support.md)
- [04-similarity-4-multi-platform](04-similarity-4-multi-platform.md)
- [10-difference-5-tool-vs-mission-drift](10-difference-5-tool-vs-mission-drift.md)
- [02-similarity-2-persistent-memory](02-similarity-2-persistent-memory.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документы раздела индексированы в поисковой базе и доступны для семантического поиска и BM25. Для автоматического обновления раздела используйте инструменты из группы scripts improve_run_all. Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo.
