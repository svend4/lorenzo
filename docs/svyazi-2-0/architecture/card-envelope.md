# Card Envelope

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
