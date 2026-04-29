# A2A vs MCP, ансамбль H — MCP/A2A Review Fabric

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).
**Проекты:** Svyazi, mclaude, AI Factory

---
<!-- tags: memory, rag, orchestration, ingestion, architecture, collaboration -->




> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

3. Третий новый слой: A2A как протокол для агентов, MCP как протокол для инструментов

До сих пор мы рассматривали MCP как главный внешний интерфейс. Но для Svyazi‑2.0, где могут работать extractor‑агент, reviewer‑агент, security‑агент, evidence‑агент, moderator‑агент и publisher‑агент, одного MCP мало. MCP отвечает за “агент использует инструмент”. A2A отвечает за “агент договаривается с другим агентом”. Linux Foundation в апреле 2026 года объявила, что A2A стал production‑ready open standard с более чем 150 организациями поддержки и интеграциями в крупные cloud‑платформы; спецификация A2A описывает discovery capabilities, modalities, collaborative tasks и обмен информацией между независимыми агентами без доступа к их внутреннему состоянию. Linux Foundation+1

В Хабр‑обзорах A2A также прямо противопоставляется MCP: MCP — инструменты и данные, A2A — коммуникация агентов, Agent Cards, Tasks, long‑running operations и push‑уведомления. Habr+1

Ансамбль H — MCP/A2A Review Fabric

Родители: MCP tools + A2A agents + LangGraph HITL + mclaude mailbox + AI Factory/Handoff.

Что рождается: не “рой агентов”, а проверяемая сеть ролей, где каждый агент публикует capability card, принимает задачи, отдаёт промежуточные артефакты и ждёт human approval там, где нужно.

Mermaid

LangGraph здесь полезен не как конкурент, а как reference‑runtime для stateful workflows: его документация описывает persistence через checkpoints, threads, human‑in‑the‑loop, memory, time travel и fault‑tolerant execution. HITL‑middleware умеет останавливать agent tool call перед рискованным действием, сохранять состояние и ждать решения человека: approve, edit или reject. Документация LangChain+1

Для Svyazi‑2.0 это означает: review protocol лучше проектировать сразу как state machine, а не как комментарии в чате.

YAML

review_state:
proposal_id: "match_2026_04_29_001"
state: "pending_review"
required_roles:
- "evidence_reviewer"
- "privacy_reviewer"
allowed_decisions:
- "approve"
- "edit"
- "reject"
- "defer"
interrupt_policy:
external_send: "human_required"
card_publish: "human_required"
memory_episode: "auto_allowed"
memory_fact: "review_required"

<!-- see-also -->

---

**Смотрите также:**
- [07-vs-notion-mem-affine-langgraph](docs/ai-collaborations/continuation/07-vs-notion-mem-affine-langgraph.md)
- [14-ограничения-лицензии-и-что-пока-лучше-не-склеивать](docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md)
- [04-memory-firewall-vs-prompt-worms](docs/ai-collaborations/continuation/04-memory-firewall-vs-prompt-worms.md)
- [10-architecture-rfc](docs/ai-collaborations/continuation/10-architecture-rfc.md)

