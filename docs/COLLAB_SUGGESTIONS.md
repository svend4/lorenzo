# Рекомендации по коллаборации (Collaboration Finder)

<!-- summary -->
> Автоматический поиск партнёрских проектов для: «opensearch анализ логов безопасности через codegen»
> **Дата:** 2026-05-12 19:34  **Кандидатов:** 1

---

<!-- tags: collaboration, projects, recommendations, svyazi -->

**Источник:** `docs/06-discovery/round-40/projects/kaspersky-llm-mcp-opensearch-log-analysis.md`

**Запрос:** opensearch анализ логов безопасности через codegen

---

## 1. Wikontic: семантический граф

**Релевантность:** `0.400`  **Тип:** `project`  **Состояние:** `raw`  **Связей:** 6

**Документ:** [`docs/05-habr-projects/knowledge/wikontic.md`](05-habr-projects/knowledge/wikontic.md)

**Теги:** ingestion, collaboration
**Упомянутые проекты:** Yodoca, Wikontic

> Wikontic — Алла Чепурова (AIRI, лаборатория Cognitive AI Systems) https://habr.com/ru/companies/airi/articles/1000720/ И её более ранняя статья: https://habr.com/ru/companies/airi/articles/855128/ Пай

**Связан с:**
  - [docs/README.md](README.md) _references_
  - [docs/05-habr-projects/memory/ngt-memory.md](05-habr-projects/memory/ngt-memory.md) _references_
  - [docs/05-habr-projects/memory/yodoca.md](05-habr-projects/memory/yodoca.md) _references_
  - [docs/05-habr-projects/02-collaboration-partners.md](05-habr-projects/02-collaboration-partners.md) _references_

**Автор:** VitalyOborin @VitalyOborin  |  GitHub  |  ⬜ `not_started`
**Контакт:** [`docs/contacts/vitalyoborin.md`](contacts/vitalyoborin.md)

<details>
<summary>📧 Шаблон первого сообщения → VitalyOborin</summary>

```
**Кому:** VitalyOborin (@VitalyOborin)
**Тема:** Коллаборация по теме «opensearch анализ логов безопасности через codegen»

Привет, VitalyOborin!

Изучила ваш проект **Svyazi, Yodoca, Wikontic** и вижу сильную синергию с задачами, над которыми работаю.

Особенно ценна идея: _Wikontic — Алла Чепурова (AIRI, лаборатория Cognitive AI Systems) https://habr.com/ru/companies/airi/articles/1000720/ И её более ранняя статья: https_

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
   python scripts/improve_collab_finder.py --query "opensearch анализ логов безопасности через codegen"
   ```

_Сгенерировано: 2026-05-12 19:34  |  Алгоритм: TF-IDF + BM25 + граф_
