# Комбинация 31: Event-Sourced Legal Document History

<!-- summary -->
> > Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

---
<!-- tags: rag -->




> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

Event Sourcing (immutable event log, time-travel queries)

CQRS (Command Query Responsibility Segregation)

ClickHouse (OLAP analytics on event stream)

German legal workflows (Antrag → Bescheid → Widerspruch → Klage)

Дети:

Audit-complete legal case management

Event Store (append-only):
- AntragSubmitted(id, date, content)
- BescheidReceived(id, decision, deadline)
- WiderspruchFiled(id, arguments, evidence)
- KlageInitiated(id, grounds)

Commands (write model):
- SubmitAntrag → AntragSubmitted event
- FileWiderspruch → WiderspruchFiled event

Queries (read model):
- "Show current status S 7 SO 99/25" → projection
- "Replay case history from beginning" → event replay
- "Calculate average processing time" → ClickHouse analytics

Time-travel case analysis

Replay case to any point in time

"What was status on 2024-06-15?" → replay events until that date

Use cases:

Audit: prove when Frist was calculated

Analysis: identify decision points

Legal strategy: "what if we filed Widerspruch earlier?"

ROI: Complete audit trail for court, instant historical queries

Уникальность: First event-sourced legal system. Every action (Antrag, Bescheid, Widerspruch) is immutable event. Time-travel queries show exact state at any deadline. CQRS separates writing (lawyer actions) from reading (reports, analytics).

<!-- see-also -->

---

**Смотрите также:**
- [33-event-sourcing-cqrs-clickhouse-analytics](docs/technology-combinations/combinations/33-event-sourcing-cqrs-clickhouse-analytics.md)
- [35-mega-stack-4-0-with-event-sourcing-consensus](docs/technology-combinations/combinations/35-mega-stack-4-0-with-event-sourcing-consensus.md)
- [31-35-final](docs/technology-combinations/synthesis-tables/31-35-final.md)
- [20-hybrid-olap-oltp-with-real-time-sync](docs/technology-combinations/combinations/20-hybrid-olap-oltp-with-real-time-sync.md)

