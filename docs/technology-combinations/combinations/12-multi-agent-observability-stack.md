# Комбинация 12: Multi-Agent Observability Stack

> Источник: MHTML‑снимок `Комбинирование технологий для новых свойств - Claude` (корень репозитория).

Родители:

OpenTelemetry (unified standard, habr.com/ru/companies/wildberries/articles/995330/)

Prometheus + Grafana + Jaeger (metrics, logs, traces)

Agent orchestration (Conductor/Agent-Bridge/Sequential)

Дети:

Distributed agent observability dashboard

Each Claude Code / Qwen agent emits OpenTelemetry traces

Prometheus tracks agent resource usage (tokens, CPU, memory)

Jaeger visualizes agent→agent handoffs in Sequential chains

Grafana dashboard: "Agent A stuck 10 min on refactoring, Agent B idle"

Agent performance SLO tracking

SLI: p95 task completion time per agent type

SLO: "Code review agent must complete 95% tasks <5 min"

Alerting when agent degrades (e.g., model API latency spike)

ROI: Detect agent bottlenecks 60 sec vs manual review

Уникальность: OpenTelemetry for agent-to-agent tracing. Никто не делает observability specifically for multi-agent developer workflows.
