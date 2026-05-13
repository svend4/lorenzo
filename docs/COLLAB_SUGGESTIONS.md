# Рекомендации по коллаборации (Collaboration Finder)

<!-- summary -->
> Автоматический поиск партнёрских проектов для: «video search assistant clip only видеонаблюдения декодера»
> **Дата:** 2026-05-13 17:13  **Кандидатов:** 3

---

<!-- tags: collaboration, projects, recommendations, svyazi -->

**Источник:** `docs/06-discovery/round-51/projects/ecaesar-mts-video-rag-clip-vlm-search.md`

**Запрос:** video search assistant clip only видеонаблюдения декодера

---

## 1. Yodoca

**Релевантность:** `0.436`  **Тип:** `project`  **Состояние:** `raw`  **Связей:** 8

**Документ:** [`docs/svyazi-2-0/components/yodoca.md`](svyazi-2-0/components/yodoca.md)

**Теги:** memory, ingestion, architecture, self-improvement, collaboration
**Упомянутые проекты:** Svyazi, mclaude, Yodoca, MemNet

> Локальный self‑evolving AI assistant с долговременной памятью и ночной консолидацией.

**Связан с:**
  - [docs/svyazi-2-0/components/ngt-memory.md](svyazi-2-0/components/ngt-memory.md) _references_
  - [docs/svyazi-2-0/components/memnet.md](svyazi-2-0/components/memnet.md) _references_
  - [docs/svyazi-2-0/components/mclaude.md](svyazi-2-0/components/mclaude.md) _references_
  - [docs/svyazi-2-0/components/ai-factory.md](svyazi-2-0/components/ai-factory.md) _references_

**Автор:** VitalyOborin @VitalyOborin  |  GitHub  |  ⬜ `not_started`
**Контакт:** [`docs/contacts/vitalyoborin.md`](contacts/vitalyoborin.md)

<details>
<summary>📧 Шаблон первого сообщения → VitalyOborin</summary>

```
**Кому:** VitalyOborin (@VitalyOborin)
**Тема:** Коллаборация по теме «video search assistant clip only видеонаблюдения декодера»

Привет, VitalyOborin!

Изучила ваш проект **Svyazi, Yodoca, Wikontic** и вижу сильную синергию с задачами, над которыми работаю.

Особенно ценна идея: _Локальный self‑evolving AI assistant с долговременной памятью и ночной консолидацией._

Работаю над Knowledge OS для локальных коллаборационных сетей (Svyazi 2.0 — CardIndex + Retrieval + Memory).
Хотел бы обсудить возможность интеграции или обмена опытом.

**Конкретные вопросы:**
- Как Svyazi, Yodoca, Wikontic решает [_конкретный аспект из запроса_]?
- Есть ли API / адаптер для внешних систем?
- Открыты к совместным PR или техническому обмену?

Репо: github.com/svend4/lorenzo | Документация: docs/PROTOTYPE_SPEC.md

С уважением,
Lorenzo / svend4
```

</details>

---

## 2. MemNet / memory-is-all-you-need

**Релевантность:** `0.293`  **Тип:** `project`  **Состояние:** `raw`  **Связей:** 8

**Документ:** [`docs/svyazi-2-0/components/memnet.md`](svyazi-2-0/components/memnet.md)

**Теги:** memory, ingestion, architecture, roadmap, collaboration
**Упомянутые проекты:** Svyazi, knowledge-space, Rufler, Yodoca

> Исследовательская активная память для трансформеров.

**Связан с:**
  - [docs/svyazi-2-0/components/ngt-memory.md](svyazi-2-0/components/ngt-memory.md) _references_
  - [docs/svyazi-2-0/components/yodoca.md](svyazi-2-0/components/yodoca.md) _references_
  - [docs/svyazi-2-0/components/rufler.md](svyazi-2-0/components/rufler.md) _references_
  - [docs/svyazi-2-0/components/knowledge-space.md](svyazi-2-0/components/knowledge-space.md) _references_

**Автор:** контакт не найден в docs/contacts/

---

## 3. mclaude

**Релевантность:** `0.217`  **Тип:** `project`  **Состояние:** `raw`  **Связей:** 7

**Документ:** [`docs/svyazi-2-0/components/mclaude.md`](svyazi-2-0/components/mclaude.md)

**Теги:** orchestration, ingestion, collaboration
**Упомянутые проекты:** Svyazi, knowledge-space, mclaude, Rufler

> Координация нескольких сессий Claude Code и других coding‑агентов над одним проектом.

**Связан с:**
  - [docs/svyazi-2-0/components/rufler.md](svyazi-2-0/components/rufler.md) _references_
  - [docs/svyazi-2-0/components/knowledge-space.md](svyazi-2-0/components/knowledge-space.md) _references_
  - [docs/svyazi-2-0/components/yodoca.md](svyazi-2-0/components/yodoca.md) _references_
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
   python scripts/improve_collab_finder.py --query "video search assistant clip only видеонаблюдения д"
   ```

_Сгенерировано: 2026-05-13 17:13  |  Алгоритм: TF-IDF + BM25 + граф_
