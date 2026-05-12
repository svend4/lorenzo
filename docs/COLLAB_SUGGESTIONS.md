# Рекомендации по коллаборации (Collaboration Finder)

<!-- summary -->
> Автоматический поиск партнёрских проектов для: «temporal fusion transformer прогнозирования спроса ритейле»
> **Дата:** 2026-05-12 18:31  **Кандидатов:** 1

---

<!-- tags: collaboration, projects, recommendations, svyazi -->

**Источник:** `docs/06-discovery/round-36/projects/x5tech-tft-retail-demand-forecasting.md`

**Запрос:** temporal fusion transformer прогнозирования спроса ритейле

---

## 1. agent-memory-mcp + Memory OS

**Релевантность:** `0.442`  **Тип:** `project`  **Состояние:** `raw`  **Связей:** 7

**Документ:** [`docs/svyazi-2-0/components/agent-memory-mcp.md`](svyazi-2-0/components/agent-memory-mcp.md)

**Теги:** memory, ingestion, architecture, roadmap, collaboration
**Упомянутые проекты:** Svyazi, Rufler, Yodoca, MemNet

> Typed memory MCP плюс более тяжёлая концепция Memory OS с онтологией, gardener‑loop и bi‑temporal facts.

**Связан с:**
  - [docs/svyazi-2-0/components/memnet.md](svyazi-2-0/components/memnet.md) _references_
  - [docs/svyazi-2-0/components/yodoca.md](svyazi-2-0/components/yodoca.md) _references_
  - [docs/svyazi-2-0/components/rufler.md](svyazi-2-0/components/rufler.md) _references_
  - [docs/svyazi-2-0/components/ngt-memory.md](svyazi-2-0/components/ngt-memory.md) _references_

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
   python scripts/improve_collab_finder.py --query "temporal fusion transformer прогнозирования спроса"
   ```

_Сгенерировано: 2026-05-12 18:31  |  Алгоритм: TF-IDF + BM25 + граф_
