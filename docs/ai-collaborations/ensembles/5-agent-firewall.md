# Ансамбль 5 — Agent Firewall

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).
**Проекты:** Svyazi, SENTINEL, Tool Search

---
<!-- tags: rag, security, ingestion, architecture, self-improvement, collaboration -->




> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

5. Agent Firewall: «иммунная система для автономных агентов»

Родители: SENTINEL + Shield/Guards + Prompt Worms + OpenClaw risk cases + Claude permissions/Tool Search.

Здесь очень важный слой, потому что все предыдущие связки опасны без предохранителей.

SENTINEL описан как open-source платформа безопасности для LLM и AI-агентов: 116 тысяч строк кода, Apache 2.0, режимы Defense/Offense/Framework, ядро из 49 Rust Super-Engines через PyO3, включая движки для injection, jailbreak, PII, exfiltration, memory integrity, tool shadowing, RAG, agentic и других классов атак. Habr

Shield-подход делит безопасность не на один классификатор, а на специализированные guards: LLM Guard, RAG Guard, Agent Guard, Tool Guard, MCP Guard и API Guard; RAG Guard проверяет poisoning/provenance/context integrity, Agent Guard — бесконечные циклы, privilege escalation и misuse инструментов, MCP Guard — схемы и capability. Habr

Prompt Worms показывает, почему это не теория: OpenClaw назван «идеальным носителем» из-за доступа к файловой системе, .env, SSH-ключам, email/Slack/Discord/веб-страницам, внешним командам и persistent memory. Habr

Отдельная статья формулирует главную разницу: агент — это не чатбот, а LLM + инструменты + автономия + состояние; он может выполнять действия по расписанию, триггеру или heartbeat’у, и именно на стыке автономии и доступа к реальным ресурсам происходят катастрофы. Habr

Claude Code настройки дают практический минимальный слой защиты: permissions с deny для .env, lazy loading MCP-инструментов и проектные настройки, которые можно коммитить. Habr

Что рождается при склейке:

Получается Agent Firewall / Agent Immune System.

Схема:

входные данные → prompt-injection scan → RAG provenance check → tool scope validation → MCP capability check → memory integrity → trace/eval

Дети этой связки:

Secure Svyazi — люди, профили, контакты, персональные данные и inferred-факты проходят через privacy/security guard до индексации.

Legal Agent Sandbox — агент может читать документы и готовить черновики, но не может сам отправить письмо, удалить файл, прочитать .env, изменить дедлайн или подать документ без human-in-the-loop.

MCP Firewall — единая прослойка между агентом и всеми MCP-серверами: браузер, GitHub, Postgres, почта, календарь, Obsidian, shell.

Главное новое свойство: агентная система становится допускаемой к реальным задачам. Без этого она остаётся игрушкой или риском.

<!-- see-also -->

---

**Смотрите также:**
- [04-memory-firewall-vs-prompt-worms](docs/ai-collaborations/continuation/04-memory-firewall-vs-prompt-worms.md)
- [8-budget-aware-intelligence-stack](docs/ai-collaborations/ensembles/8-budget-aware-intelligence-stack.md)
- [7-domain-agent-app-factory](docs/ai-collaborations/ensembles/7-domain-agent-app-factory.md)
- [default-policy](docs/svyazi-2-0/security/default-policy.md)

