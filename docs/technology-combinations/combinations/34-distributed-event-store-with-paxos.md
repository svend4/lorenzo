# Комбинация 34: Distributed Event Store with Paxos

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---



> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

Paxos consensus (Google Chubby, Spanner)

Event Sourcing (append-only log)

Multi-datacenter replication

Legal document versioning

Дети:

Geo-replicated legal document store

Datacenters:
- Dresden (primary)
- Berlin (replica)
- München (replica)

Paxos consensus:
- Write "WiderspruchFiled" event
- Paxos ensures all DCs agree on order
- Majority (2/3) must acknowledge

Benefits:
- Availability: Dresden fails → Berlin takes over
- Consistency: all DCs see same event order
- Latency: read from nearest DC

Byzantine-fault-tolerant legal archive

Paxos handles failures, network partitions

Scenario: network split Dresden ↔ Berlin

Majority (Berlin + München) continues

Dresden rejoins → syncs missing events

ROI: Legal documents never lost, even with datacenter failure

Уникальность: Paxos-replicated legal event store. Guarantees global consistency across datacenters. First application of consensus algorithms to German Sozialrecht document management.

<!-- see-also -->

---

**Смотрите также:**
- [32-consensus-based-multi-agent-coordination](docs/technology-combinations/combinations/32-consensus-based-multi-agent-coordination.md)
- [31-35-final](docs/technology-combinations/synthesis-tables/31-35-final.md)
- [31-event-sourced-legal-document-history](docs/technology-combinations/combinations/31-event-sourced-legal-document-history.md)
- [33-event-sourcing-cqrs-clickhouse-analytics](docs/technology-combinations/combinations/33-event-sourcing-cqrs-clickhouse-analytics.md)

