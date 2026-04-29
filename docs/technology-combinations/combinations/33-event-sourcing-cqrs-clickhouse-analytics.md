# Комбинация 33: Event Sourcing + CQRS + ClickHouse Analytics

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---



> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

Event Sourcing (immutable log)

CQRS (separate read/write)

ClickHouse (columnar analytics)

Kafka (event stream)

Дети:

Real-time legal analytics pipeline

Write Model (Commands):
Lawyer action → Kafka topic → Event Store

Event Stream:
Kafka → ClickHouse table (MergeTree engine)

Read Models (Queries):
- PostgreSQL: current case status (OLTP)
- ClickHouse: analytics on 50k+ cases (OLAP)

Pipeline:
1. Lawyer files Widerspruch → Command
2. WiderspruchFiled event → Kafka
3. Kafka → ClickHouse (async ingestion)
4. Materialized view: "success rate by §§ cited"

Multi-projection legal knowledge base

Same event stream → multiple read models

Projection 1: PostgreSQL (current state, for UI)

Projection 2: ClickHouse (analytics, for strategy)

Projection 3: Elasticsearch (full-text search)

Projection 4: Graph database (precedent links)

ROI: Write once (event), read many ways (projections)

Уникальность: CQRS with ClickHouse as analytics read model. Event Sourcing provides audit trail, Kafka streams events, ClickHouse analyzes at scale. First legal system with real-time analytics on event stream.

<!-- see-also -->

---

**Смотрите также:**
- [31-event-sourced-legal-document-history](docs/technology-combinations/combinations/31-event-sourced-legal-document-history.md)
- [35-mega-stack-4-0-with-event-sourcing-consensus](docs/technology-combinations/combinations/35-mega-stack-4-0-with-event-sourcing-consensus.md)
- [31-35-final](docs/technology-combinations/synthesis-tables/31-35-final.md)
- [20-hybrid-olap-oltp-with-real-time-sync](docs/technology-combinations/combinations/20-hybrid-olap-oltp-with-real-time-sync.md)

