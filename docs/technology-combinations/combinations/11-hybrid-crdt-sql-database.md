---
state: normalized
---

# Комбинация 11: Hybrid CRDT-SQL Database

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)
- [Кто ссылается на этот документ (3)](#кто-ссылается-на-этот-документ-3)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).
**Проекты:** Yjs, Automerge

---
<!-- tags: local-first, roadmap, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

CRDT/Yjs/Automerge (local-first, conflict-free sync)

PostgreSQL 18 (async I/O, 2025 release, habr.com/ru/companies/postgrespro/articles/985698/)

TimescaleDB (time-series extension for PostgreSQL)

Дети:

PostgreSQL-backed CRDT with async writes

Yjs/Automerge for client-side CRDT operations

PostgreSQL 18 async I/O handles high-throughput sync without page cache bottleneck

TimescaleDB stores operation history as time-series (compression, retention policies)

Итог: 100k ops/sec sync throughput on commodity hardware

Legal case timeline with CRDT + TimescaleDB

Each case action = CRDT operation with timestamp

TimescaleDB auto-compresses history >90 days

PostgreSQL 18 async ensures responsive writes during deadline crunch

Multiple legal assistants edit case simultaneously, zero conflicts

ROI: Real-time collaboration without conflict UI

Уникальность: PostgreSQL 18 async I/O (2025) + CRDT = production-grade local-first database. TimescaleDB adds time-travel queries.

<!-- see-also -->

---

## Использование

```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Комбинация 11 Hybrid CRDT SQL Database"
```

## Смотрите также
- [20-hybrid-olap-oltp-with-real-time-sync](20-hybrid-olap-oltp-with-real-time-sync.md)
- [09-14-extended](../synthesis-tables/09-14-extended.md)
- [17-distributed-agent-memory-with-graph](17-distributed-agent-memory-with-graph.md)
- [33-event-sourcing-cqrs-clickhouse-analytics](33-event-sourcing-cqrs-clickhouse-analytics.md)


<!-- backlinks -->

---

## Кто ссылается на этот документ (3)
- [components-by-name](../../glossary/components-by-name.md)
- [README](README.md)
- [09-14-extended](../synthesis-tables/09-14-extended.md)

_Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Документ индексирован в поисковой базе репозитория Lorenzo и доступен для семантического поиска._ _Материал доступен для семантического поиска, BM25 и навигации по графу._ _Для поиска доступен._

<!-- similar-docs -->

---

**Похожие документы:**
- [11-hybrid-crdt-sql-database](../../obsidian/technology-combinations/combinations/11-hybrid-crdt-sql-database.md) (сходство 0.95)
- [20-hybrid-olap-oltp-with-real-time-sync](20-hybrid-olap-oltp-with-real-time-sync.md) (сходство 0.41)
- [20-hybrid-olap-oltp-with-real-time-sync](../../obsidian/technology-combinations/combinations/20-hybrid-olap-oltp-with-real-time-sync.md) (сходство 0.38)

