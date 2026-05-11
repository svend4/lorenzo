# Memory Write Policy

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
> > Источник: `deep-research-report (3).md`, раздел «Интеграционный контракт».
**Проекты:** Yodoca, NGT Memory, agent-memory-mcp

---
<!-- tags: memory, architecture -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: `deep-research-report (3).md`, раздел «Интеграционный контракт».

Система должна различать хотя бы четыре режима записи:

- `episode` — для сырых наблюдений
- `fact` — для подтверждённого знания
- `proposal` — для гипотез
- `decay_event` — для понижения значимости

Yodoca уже мыслит память через consolidation + forgetting, NGT Memory — через ассоциативные связи и иерархическую консолидацию, agent-memory-mcp — через typed memory primitives, а Memory OS — через bi‑temporal и provenance‑heavy представление знаний. Из этих линий следует, что «записать что‑то в память» никогда не должно быть одной неразличимой операцией. citeturn21view0turn22view4turn20view16turn39view3

## Минимальные поля

- `write_type` — `episode` | `fact` | `proposal` | `decay_event`
- `promotion_rule` — правило перехода из proposal в fact
- `review_required` — нужен ли явный review перед промоцией
- `decay_policy` — параметры забывания (Ebbinghaus‑decay в стиле Yodoca)

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Memory Write Policy"
```

## Смотрите также
- [11-integration-contracts](../../01-svyazi/11-integration-contracts.md)
- [11-интеграционный-контракт-который-стоит-зафиксироват](../../04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md)
- [card-envelope](card-envelope.md)
- [review-record](review-record.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (4)
- [components-by-name](../../glossary/components-by-name.md)
- [concepts](../../glossary/concepts.md)
- [README](README.md)
- [integration-spec](integration-spec.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Материал доступен для семантического поиска, BM25 и навигации через граф концептов._ _Материал доступен для поиска._ _Индексировано._
