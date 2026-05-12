# Рекомендации по коллаборации (Collaboration Finder)

<!-- summary -->
> Автоматический поиск партнёрских проектов для: «agentic graph skeleton indexing vectorcypher pymangle datalog»
> **Дата:** 2026-05-12 19:13  **Кандидатов:** 1

---

<!-- tags: collaboration, projects, recommendations, svyazi -->

**Источник:** `docs/06-discovery/round-38/projects/agentic-graph-rag-skeleton-indexing-pymangle.md`

**Запрос:** agentic graph skeleton indexing vectorcypher pymangle datalog

---

## 1. research-docs + LiteParse

**Релевантность:** `0.424`  **Тип:** `project`  **Состояние:** `raw`  **Связей:** 7

**Документ:** [`docs/svyazi-2-0/components/research-docs-liteparse.md`](svyazi-2-0/components/research-docs-liteparse.md)

**Теги:** rag, ingestion, collaboration
**Упомянутые проекты:** Svyazi, mclaude, LiteParse, Yodoca

> Forensic document QA с HTML‑отчётом и bounding boxes на страницах PDF.

**Связан с:**
  - [docs/svyazi-2-0/components/yodoca.md](svyazi-2-0/components/yodoca.md) _references_
  - [docs/svyazi-2-0/components/mclaude.md](svyazi-2-0/components/mclaude.md) _references_
  - [docs/svyazi-2-0/components/graph-rag.md](svyazi-2-0/components/graph-rag.md) _references_
  - [docs/svyazi-2-0/components/memnet.md](svyazi-2-0/components/memnet.md) _references_

**Автор:** контакт не найден в docs/contacts/

---

## Следующие шаги

1. Изучить топ-3 кандидата и выбрать приоритет
2. Обновить статус контакта:
   ```
   python scripts/improve_contact_status.py --author <имя> --studied
   ```
3. Отправить сообщение по шаблону выше
4. Обновить после ответа:
   ```
   python scripts/improve_contact_status.py --author <имя> --messaged
   ```
5. Повторить поиск с уточнённым запросом:
   ```
   python scripts/improve_collab_finder.py --query "agentic graph skeleton indexing vectorcypher pyman"
   ```

_Сгенерировано: 2026-05-12 19:13  |  Алгоритм: TF-IDF + BM25 + граф_
