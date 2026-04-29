---
title: "Что стоит зафиксировать как default policy"
tags:
  - memory
  - orchestration
  - security
  - knowledge
  - ingestion
  - architecture
  - collaboration
  - svyazi-2-0
date: 2026-04-29
---

# Что стоит зафиксировать как default policy

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> > Источник: `deep-research-report (1).md`, раздел «Безопасность, приватность и бюджетный роутинг».
**Проекты:** Svyazi, AI Factory, agent-memory-mcp, SENTINEL

---
<!-- tags: memory, orchestration, security, knowledge, ingestion, architecture, collaboration -->




> Источник: `deep-research-report (1).md`, раздел «Безопасность, приватность и бюджетный роутинг».

Для Svyazi‑2.0 безопасная архитектура — не «добавить сканер в конце», а **с самого начала считать skills, MCP servers, импорты документов и memory writes потенциально недоверенными**. Это не паранойя, а прямой вывод из материалов про Prompt Worms, катастрофы автономных агентов и практик защиты AI Factory/SENTINEL. Дополнительный важный сигнал: сами reference MCP servers указываются как образовательные примеры, а не production‑готовые решения — значит, прод‑политики доступа и аудит нужно строить отдельно. citeturn34view4turn34view5turn29search6turn20view10turn15search10

| Контроль | Практический дефолт | Основание |
|---|---|---|
| Разделение tool‑классов | По умолчанию разрешать read‑only tools; любые send/write/delete/execute — только через явный approval | Автономный агент отличается от чатбота именно доступом к реальным действиям; это и создаёт катастрофы. citeturn34view5 |
| Quarantine для external skills/MCP | Любой внешний skill/MCP сначала в sandbox, потом статический/репутационный скан, потом allowlist | AI Factory прямо предупреждает о prompt injection в SKILL.md и запускает двухуровневый security scan. citeturn29search6 |
| Path allowlist | Жёстко ограничить, что агент вообще может читать и писать на диске | `agent-memory-mcp` демонстрирует хороший паттерн Path Guard/allowlist против traversal и выхода за пределы проекта. citeturn20view16 |
| PII separation | Любые контакты, email, Telegram, ссылки — в отдельном raw‑слое; в карточки уходит только очищенный профиль | Так делает Svyazi; это правильный privacy‑baseline для людей и сообществ. citeturn41search0 |
| Truth vs Proposal | `inferred` и weak signals не писать сразу в «истину», а ставить в pending review | И Svyazi, и более тяжёлые memory‑системы сходятся на нужде в review‑контуре. citeturn41search0turn36search0 |
| Runtime firewall | Между агентом и mutating tools держать специализированный защитный слой | Именно для этого и нужен SENTINEL‑подобный слой, а не только «умный промпт». citeturn20view10 |

<!-- see-also -->

---

**Смотрите также:**
- [[06-security-privacy]]
- [[06-безопасность-приватность-и-бюджетный-роутинг]]
- [[risks]]
- [[first-contacts]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[06-security-privacy]] (сходство 0.45)
- [[06-безопасность-приватность-и-бюджетный-роутинг]] (сходство 0.44)
- [[06-security-privacy]] (сходство 0.43)

