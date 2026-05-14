---
state: approved
---

# Card Envelope

<!-- toc-auto -->
## Contents

- [Минимальные поля](#минимальные-поля)
- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (4)](#кто-ссылается-на-этот-документ-4)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> Эта структура логически следует из CardIndex‑мышления Svyazi, immutable/event‑style практик AgentFS и Memory OS, а также из необходимости разводить truth и proposal в memory‑системах.
**Проекты:** Svyazi, CardIndex, AgentFS

---
<!-- tags: memory, knowledge, ingestion, architecture -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: `deep-research-report (3).md`, раздел «Интеграционный контракт».

У каждой карточки должен быть неизменяемый `card_id`, `card_type`, статус `raw | normalized | inferred | approved | rejected | decayed`, список source links, список relation edges, временные метки и хэш полезной нагрузки. Эта структура логически следует из CardIndex‑мышления Svyazi, immutable/event‑style практик AgentFS и Memory OS, а также из необходимости разводить truth и proposal в memory‑системах. Это не «идеальная онтология», а минимальный договор, который позволяет системам вообще разговаривать между собой. citeturn41search0turn27view0turn39view3turn20view16

## Минимальные поля

- `card_id` — неизменяемый идентификатор
- `card_type` — `person` | `project` | `episode` | `document` | `hypothesis` | …
- `state` — `raw` | `normalized` | `inferred` | `approved` | `rejected` | `decayed`
- `sources` — список ссылок на источники
- `edges` — список связей (relations)
- `updated_at` — временная метка последнего изменения
- `payload_hash` — хэш полезной нагрузки для dedup/version trace

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Card Envelope"
```

## Смотрите также
- [11-integration-contracts](../../01-svyazi/11-integration-contracts.md)
- [11-интеграционный-контракт-который-стоит-зафиксироват](../../04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md)
- [integration-spec](integration-spec.md)
- [review-record](review-record.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (4)
- [components-by-name](../../glossary/components-by-name.md)
- [concepts](../../glossary/concepts.md)
- [README](README.md)
- [integration-spec](integration-spec.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в базе репозитория Lorenzo и доступен для семантического поиска._ _Доступен семантический поиск._ _Индексировано._

<!-- similar-docs -->

---

**Похожие документы:**
- [card-envelope](../../obsidian/svyazi-2-0/architecture/card-envelope.md) (сходство 0.97)
- [memory-write-policy](memory-write-policy.md) (сходство 0.34)
- [memory-write-policy](../../obsidian/svyazi-2-0/architecture/memory-write-policy.md) (сходство 0.33)

