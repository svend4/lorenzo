---
title: "Комбинация 11: Hybrid CRDT-SQL Database"
tags:
  - technology-combinations
date: 2026-04-29
---

# Комбинация 11: Hybrid CRDT-SQL Database

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).
**Проекты:** Yjs, Automerge

---
<!-- tags: local-first, roadmap, collaboration -->




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

**Смотрите также:**
- [[20-hybrid-olap-oltp-with-real-time-sync]]
- [[09-14-extended]]
- [[17-distributed-agent-memory-with-graph]]
- [[33-event-sourcing-cqrs-clickhouse-analytics]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[20-hybrid-olap-oltp-with-real-time-sync]] (сходство 0.36)
- [[17-distributed-agent-memory-with-graph]] (сходство 0.28)
- [[33-event-sourcing-cqrs-clickhouse-analytics]] (сходство 0.27)

