# Различие 3: Federated knowledge architecture отсутствует

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Resear

---
<!-- tags: architecture, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Research.

Различие 3: Federated knowledge architecture отсутствует

Hermes — single-agent system per installation. Каждый пользователь имеет свой Hermes instance. Между instances нет federation.

Nautilus Portal Protocol specifically addresses federated queries across multiple repositories. Это совершенно другой architectural concern.

То есть для personal use Hermes сам по себе достаточен. Для federated knowledge work (multiple practitioners sharing patterns, OKWF guild structure), нужен Nautilus-like layer поверх Hermes.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Различие 3 Federated knowledge"
```

## Смотрите также
- [06-difference-1-structured-substrate-missing](06-difference-1-structured-substrate-missing.md)
- [09-difference-4-institutional-vision](09-difference-4-institutional-vision.md)
- 03-similarity-3-[mcp-support](03-similarity-3-mcp-support.md)
- [02-similarity-2-persistent-memory](02-similarity-2-persistent-memory.md)

Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов. Используйте скрипты группы reports для получения актуальной статистики по разделу. Рекомендуется начинать с основных документов раздела и переходить к деталям через внутренние ссылки. Все связанные документы доступны через граф концептов и поисковый индекс репозитория Lorenzo. Документы раздела индексированы в поисковой базе и доступны для семантического поиска и BM25. Для автоматического обновления раздела используйте инструменты из группы scripts improve_run_all. Документ индексирован в базе знаний репозитория. Навигация возможна через семантический поиск и граф концептов репозитория Lorenzo. Материал доступен для семантического поиска, BM25-поиска и навигации через граф концептов.

<!-- backlinks -->

---

**Кто ссылается на этот документ (9):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [06-difference-1-structured-substrate-missing](06-difference-1-structured-substrate-missing.md)
- [09-difference-4-institutional-vision](09-difference-4-institutional-vision.md)
- [README](README.md)
- [01-passive-vs-active-roles](../nautilus-vs-camel/01-passive-vs-active-roles.md)
- _...ещё 1_

