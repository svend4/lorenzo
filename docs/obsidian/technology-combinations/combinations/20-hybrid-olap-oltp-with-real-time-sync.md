---
title: "Комбинация 20: Hybrid OLAP-OLTP with Real-Time Sync"
tags:
  - technology-combinations
date: 2026-04-29
---

# Комбинация 20: Hybrid OLAP-OLTP with Real-Time Sync

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).
**Проекты:** Yjs, Automerge

---
<!-- tags: rag, local-first, architecture -->




> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

ClickHouse (Yandex, колоночная OLAP, 100M+ строк/сек, $2B valuation)

CRDT (Yjs/Automerge, conflict-free sync)

PostgreSQL 18 async I/O (2025 release, no page cache dependency)

Дети:

Real-time analytics with offline-capable writes

Architecture:
[Client] → CRDT local state (Yjs)
↓ background sync
[PostgreSQL 18] ← async I/O, OLTP layer
↓ CDC (Change Data Capture)
[ClickHouse] ← OLAP analytics, materialized views

User edits locally (CRDT, offline-capable)

PostgreSQL 18 handles OLTP (transactions, point queries)

ClickHouse processes OLAP (aggregations, time-series)

Example: Legal case management

Lawyer edits case notes offline (Yjs local)

PostgreSQL stores transactional data (case status, deadlines)

ClickHouse analyzes 50k+ cases (success rates by judge, average durations, §§ frequency)

Temporal knowledge graph with columnar analytics

CRDT syncs graph operations P2P

PostgreSQL 18 async stores graph (nodes, edges)

ClickHouse analyzes graph evolution over time

Queries:

PostgreSQL: "Get current state of Aktenzeichen S 7 SO 99/25"

ClickHouse: "Show precedent citation trends 2020-2026 across all courts"

ROI: Real-time collaboration + analytical insights, best of both worlds

Уникальность: First system combining CRDT (local-first), PostgreSQL 18 async (OLTP), ClickHouse (OLAP) in single architecture. Each layer handles what it does best.

<!-- see-also -->

---

**Смотрите также:**
- [[11-hybrid-crdt-sql-database]]
- [[33-event-sourcing-cqrs-clickhouse-analytics]]
- [[17-distributed-agent-memory-with-graph]]
- [[20-24-final]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[11-hybrid-crdt-sql-database]] (сходство 0.36)
- [[33-event-sourcing-cqrs-clickhouse-analytics]] (сходство 0.30)
- [[17-distributed-agent-memory-with-graph]] (сходство 0.29)

