# Рекомендации по коллаборации (Collaboration Finder)

<!-- summary -->
> Автоматический поиск партнёрских проектов для: «self hosted водяным охлаждением реплицированный tensor parallelism»
> **Дата:** 2026-05-13 16:33  **Кандидатов:** 1

---

<!-- tags: collaboration, projects, recommendations, svyazi -->

**Источник:** `docs/06-discovery/round-49/projects/dmitrii-chashchin-self-hosted-4x4090-vllm-parallelism.md`

**Запрос:** self hosted водяным охлаждением реплицированный tensor parallelism

---

## 1. Yodoca

**Релевантность:** `0.417`  **Тип:** `project`  **Состояние:** `raw`  **Связей:** 8

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
**Тема:** Коллаборация по теме «self hosted водяным охлаждением реплицированный tensor paral»

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
   python scripts/improve_collab_finder.py --query "self hosted водяным охлаждением реплицированный te"
   ```

_Сгенерировано: 2026-05-13 16:33  |  Алгоритм: TF-IDF + BM25 + граф_
