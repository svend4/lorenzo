# Evidence Envelope

<!-- toc-auto -->
## Contents

- [Минимальные поля](#минимальные-поля)
- [Особые случаи](#особые-случаи)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: `deep-research-report (3).md`, раздел «Интеграционный контракт».
**Проекты:** LiteParse, Legal RAG, Hybrid RAG, Graph RAG, NGT Memory

---
<!-- tags: memory, rag, local-first, architecture, self-improvement -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: `deep-research-report (3).md`, раздел «Интеграционный контракт».

Любой retrieval‑ответ, match suggestion, profile enrichment или auto‑summary должен возвращать не только текст, но и `source_id`, `page`, `span`, `box`, `retrieval_method`, `confidence`, `supporting_nodes`. Для документов это page+box; для чатов и заметок — message/thread/time span; для голосовых эпизодов — timestamp window; для ассоциативных выводов — список triggered nodes и path explanation. Это прямой синтез из LiteParse/research-docs, Legal RAG, Hybrid RAG и Graph RAG. Без такого формата нельзя построить ни нормальную ручную модерацию, ни «объяснение рекомендации». citeturn20view5turn20view6turn34view2turn34view3

## Минимальные поля

- `source_id` — идентификатор источника
- `page_or_span` — для документов: страница; для текста: диапазон
- `bbox_or_offset` — координаты bounding box или offset
- `method` — какой retrieval‑метод использовался
- `confidence` — уверенность
- `supporting_nodes` — для ассоциативных выводов: список triggered nodes и path explanation

## Особые случаи

- **Документ** — `page` + `box` (LiteParse / Legal RAG / Hybrid RAG).
- **Чат / заметка** — `message_id` / `thread_id` + `time span`.
- **Голосовой эпизод** — `timestamp window`.
- **Ассоциативный вывод** — список triggered nodes и path explanation (NGT Memory, Graph RAG).

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Evidence Envelope"
```

## Смотрите также
- [11-integration-contracts](../../01-svyazi/11-integration-contracts.md)
- [11-интеграционный-контракт-который-стоит-зафиксироват](../../04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md)
- [integration-spec](integration-spec.md)
- [review-record](review-record.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [concepts](../../glossary/concepts.md)
- [README](README.md)
- [integration-spec](integration-spec.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [evidence-envelope](../../obsidian/svyazi-2-0/architecture/evidence-envelope.md) (сходство 0.97)
- [READING_LIST](../../READING_LIST.md) (сходство 0.27)
- [READING_LIST](../../obsidian/READING_LIST.md) (сходство 0.27)

