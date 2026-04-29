# Ключевые понятия и паттерны

<!-- summary -->
> Не проекты, а концепции, которые повторяются в нескольких разделах.
**Проекты:** Svyazi, CardIndex, Legal RAG, Yodoca, NGT Memory, MemNet, Tool Search, AutoResearch

---
<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, architecture, roadmap, anthropic, self-improvement, collaboration -->




Не проекты, а концепции, которые повторяются в нескольких разделах.

| Понятие | Краткое определение | Где раскрыто |
|---|---|---|
| **CardIndex** | Source of truth: неизменяемая карточка как единица знания | [Card Envelope](../svyazi-2-0/architecture/card-envelope.md) · [Svyazi](../svyazi-2-0/components/svyazi.md) |
| **Card Envelope** | Стандарт схемы карточки: `card_id`, `card_type`, `state`, `sources`, `edges`, `updated_at`, `payload_hash` | [Card Envelope](../svyazi-2-0/architecture/card-envelope.md) · [Integration spec](../svyazi-2-0/architecture/integration-spec.md) |
| **Evidence Envelope** | Стандарт привязки вывода к источнику: `source_id`, `page_or_span`, `bbox_or_offset`, `method`, `confidence`, `supporting_nodes` | [Evidence Envelope](../svyazi-2-0/architecture/evidence-envelope.md) |
| **Memory Write Policy** | Различение `episode` / `fact` / `proposal` / `decay_event` при записи в память | [Memory Write Policy](../svyazi-2-0/architecture/memory-write-policy.md) |
| **Skill and Tool Policy** | Класс tool: `read` / `annotate` / `plan` / `mutate` / `publish` / `external_send` | [Skill and Tool Policy](../svyazi-2-0/architecture/skill-tool-policy.md) |
| **Review Record** | Артефакт человеческого решения: `reviewer_role`, `decision`, `reason`, `evidence_refs`, `follow_up` | [Review Record](../svyazi-2-0/architecture/review-record.md) |
| **Trace Envelope** | Расширение для AgentOps: trace_id, model_route, tools_used, token_cost, anomaly_flags | [AgentOps + Trace Envelope](../ai-collaborations/continuation/02-agentops-trace-envelope.md) |
| **Hot path / Slow path** | Yodoca‑паттерн: эпизоды в SQLite за <50 мс vs асинхронные эмбеддинги ночью | [Yodoca карточка](../svyazi-2-0/components/yodoca.md) · [Habr key‑findings — Yodoca](../habr-unique-projects/key-findings/01-yodoca.md) |
| **Ebbinghaus decay** | Контролируемое забывание редко используемых фактов | [Yodoca](../svyazi-2-0/components/yodoca.md) · [Memory Write Policy](../svyazi-2-0/architecture/memory-write-policy.md) |
| **Hebbian / STDP plasticity** | Усиление связи между концептами при ко‑активации | [NGT Memory](../svyazi-2-0/components/ngt-memory.md) · [MemNet](../svyazi-2-0/components/memnet.md) · [Hardware pair 1](../habr-unique-projects/hardware-pairs/1-neuromorphic-ssm.md) |
| **Spreading activation / dream phase** | Самопроизвольная активация памяти без внешнего входа для поиска скрытых связей | [MemNet](../svyazi-2-0/components/memnet.md) · [Habr key‑findings — MemNet](../habr-unique-projects/key-findings/02-memnet.md) |
| **Discovery file** | Накопление неизвестного — то, что система не смогла классифицировать | [Svyazi](../svyazi-2-0/components/svyazi.md) · [Sensor-driven life log](../habr-unique-projects/hardware-pairs/5-tinyml-mcp-skills.md) |
| **«LLM как периферия»** | Архитектура, где LLM — не ядро, а узел; код отвечает за стабильность | [PDA — LLM как периферия](../habr-unique-projects/key-findings/03-pda-llm-as-periphery.md) |
| **Sequential vs Coordinator** | Распределённая цепочка агентов, видящих результаты предшественников, выигрывает у центрального координатора на 44% | [AutoResearch + Sequential](../svyazi-2-0/components/autoresearch-sequential.md) · [Habr key‑findings — Dochkina](../habr-unique-projects/key-findings/04-dochkina-sequential.md) |
| **Adversarial review** | Один агент пишет, другие критикуют; multi‑model | [Комбинация 8](../technology-combinations/combinations/08-conductor-adversarial-review-auto-ai-router.md) · [Adversarial × Multi-IDE](../habr-unique-projects/deep-pairs/3-adversarial-multi-ide.md) |
| **Local‑first / privacy‑by‑design** | Данные принадлежат устройству пользователя, в облако только избранное | [Privacy](../svyazi-2-0/security/privacy.md) · [Hardware pair 4](../habr-unique-projects/hardware-pairs/4-riscv-privacy.md) · [Federated Local Graph](../svyazi-2-0/ensembles/G-federated-local-graph.md) |
| **Privacy by design** | Контакты — в отдельный raw‑слой; в карточки уходит только очищенный профиль | [Default policy](../svyazi-2-0/security/default-policy.md) |
| **Page-level grounding** | Единица доказательства — страница, не чанк | [Legal RAG](../svyazi-2-0/components/legal-rag.md) · [Forensic RAG (ai‑collab)](../ai-collaborations/ensembles/3-forensic-rag.md) |
| **Lazy MCP loading (Tool Search)** | Не грузить все MCP‑инструменты в контекст; падение overhead с 82k до 5.7k токенов | [Security + routing plane](../svyazi-2-0/components/security-routing-plane.md) |
| **Two parents → many children** | Метафора: hardware/software пара рождает несколько по‑разному ориентированных потомков | [Hardware metaphor](../habr-unique-projects/hardware-pairs/7-metaphor.md) · [Software metaphor](../habr-unique-projects/software-pairs/6-metaphor.md) |
| **Скромные родители → мощные дети** | Та же мысль с другой стороны: ни один проект сам по себе не революционен | [Synthesis 1‑8](../technology-combinations/synthesis-tables/01-08-summary.md) |
| **One‑man AI company** | Один человек ведёт 30–50 дел Sozialrecht параллельно с качеством офиса из 5 юристов | [One person = one company](../habr-unique-projects/final-ensembles/1-one-person-one-company.md) |
| **Q6‑гиперкуб / MoME** | 64 гексаграммы как вершины Q6, MoME‑роутинг по геометрии | [Hardware pair 2 — TSU × MoME](../habr-unique-projects/hardware-pairs/2-tsu-mome.md) · [Hardware pair 3](../habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md) · [Profile five layers](../anthropic-vacancies/profile-mapping/01-initial-analysis/01-profile-five-layers.md) |
| **LCI (Lyapunov Coherence Index)** | Метрика энергетической когерентности системы | [Hardware pair 2](../habr-unique-projects/hardware-pairs/2-tsu-mome.md) · [Svyazi 2.0 block map](../habr-unique-projects/key-findings/06-svyazi-2-0-block-map.md) |
| **Forward Deployed Engineer (FDE)** | Инженер, приходящий к клиенту с проблемой, строящий прототип на Claude в production | [FDE primary match](../anthropic-vacancies/profile-mapping/01-initial-analysis/02-primary-fde.md) · [FDE downgraded](../anthropic-vacancies/profile-mapping/02-reanalysis/01-fde-downgraded.md) |
| **Beneficial Deployments** | Anthropic‑программа: применение Claude к общественно‑полезным задачам | [Secondary match](../anthropic-vacancies/profile-mapping/01-initial-analysis/03-secondary-beneficial-deployments.md) · [Sales](../anthropic-vacancies/clusters/02-sales.md) |

<!-- see-also -->

---

**Смотрите также:**
- [components-by-name](docs/glossary/components-by-name.md)
- [11-integration-contracts](docs/01-svyazi/11-integration-contracts.md)
- [11-интеграционный-контракт-который-стоит-зафиксироват](docs/04-ai-collaborations/11-интеграционный-контракт-который-стоит-зафиксироват.md)
- [QA](docs/QA.md)

