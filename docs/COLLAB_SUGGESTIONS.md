# Рекомендации по коллаборации (Collaboration Finder)

<!-- summary -->
> Автоматический поиск партнёрских проектов для: «multi agent customer support автоматизации эскалации живых операторов»
> **Дата:** 2026-05-13 17:32  **Кандидатов:** 3

---

<!-- tags: collaboration, projects, recommendations, svyazi -->

**Источник:** `docs/06-discovery/round-52/projects/ivan-zhirnov-multiagent-customer-support-92pct-automation.md`

**Запрос:** multi agent customer support автоматизации эскалации живых операторов

---

## 1. agent-memory-mcp + Memory OS

**Релевантность:** `0.412`  **Тип:** `project`  **Состояние:** `raw`  **Связей:** 7

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

## 2. NGT[^ngt] Memory: ассоциативный граф

**Релевантность:** `0.286`  **Тип:** `project`  **Состояние:** `raw`  **Связей:** 8

**Документ:** [`docs/05-habr-projects/memory/ngt-memory.md`](05-habr-projects/memory/ngt-memory.md)

**Теги:** memory, ingestion, collaboration
**Упомянутые проекты:** Svyazi, Yodoca, NGT Memory, MemNet

> ассоциативные связи в персистентной памяти LLM

**Связан с:**
  - [docs/contacts/spbmolot.md](contacts/spbmolot.md) _references_
  - [docs/05-habr-projects/knowledge/wikontic.md](05-habr-projects/knowledge/wikontic.md) _references_
  - [docs/05-habr-projects/memory/yodoca.md](05-habr-projects/memory/yodoca.md) _references_
  - [docs/05-habr-projects/memory/agent-memory-mcp.md](05-habr-projects/memory/agent-memory-mcp.md) _references_

**Автор:** spbmolot @spbmolot  |  GitHub  |  📖 `studied`
**Контакт:** [`docs/contacts/spbmolot.md`](contacts/spbmolot.md)

<details>
<summary>📧 Шаблон первого сообщения → spbmolot</summary>

```
**Кому:** spbmolot (@spbmolot)
**Тема:** Коллаборация по теме «multi agent customer support автоматизации эскалации живых о»

Привет, spbmolot!

Изучил ваш проект **Svyazi, NGT Memory** и вижу сильную синергию с задачами, над которыми работаю.

Особенно ценна идея: _ассоциативные связи в персистентной памяти LLM_

Работаю над Knowledge OS для локальных коллаборационных сетей (Svyazi 2.0 — CardIndex + Retrieval + Memory).
Хотел бы обсудить возможность интеграции или обмена опытом.

**Конкретные вопросы:**
- Как Svyazi, NGT Memory решает [_конкретный аспект из запроса_]?
- Есть ли API / адаптер для внешних систем?
- Открыты к совместным PR или техническому обмену?

Репо: github.com/svend4/lorenzo | Документация: docs/PROTOTYPE_SPEC.md

С уважением,
Lorenzo / svend4
```

</details>

---

## 3. knowledge-space

**Релевантность:** `0.235`  **Тип:** `project`  **Состояние:** `raw`  **Связей:** 7

**Документ:** [`docs/svyazi-2-0/components/knowledge-space.md`](svyazi-2-0/components/knowledge-space.md)

**Теги:** knowledge, ingestion, architecture, collaboration
**Упомянутые проекты:** Svyazi, knowledge-space, mclaude, Rufler

> Agent‑first референсная база: 785+ карточек по 26 доменам, растущая из реальных research‑сессий.

**Связан с:**
  - [docs/svyazi-2-0/components/mclaude.md](svyazi-2-0/components/mclaude.md) _references_
  - [docs/svyazi-2-0/components/rufler.md](svyazi-2-0/components/rufler.md) _references_
  - [docs/svyazi-2-0/components/memnet.md](svyazi-2-0/components/memnet.md) _references_
  - [docs/svyazi-2-0/components/yodoca.md](svyazi-2-0/components/yodoca.md) _references_

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
   python scripts/improve_collab_finder.py --query "multi agent customer support автоматизации эскалац"
   ```

_Сгенерировано: 2026-05-13 17:32  |  Алгоритм: TF-IDF + BM25 + граф_
