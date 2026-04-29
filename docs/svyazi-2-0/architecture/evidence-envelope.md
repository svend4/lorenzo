# Evidence Envelope

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
