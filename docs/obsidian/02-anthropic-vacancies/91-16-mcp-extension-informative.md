---
title: "16. MCP Extension (Informative)"
tags:
  - architecture
  - anthropic-vacancies
date: 2026-04-29
---

# 16. MCP Extension (Informative)

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> NPP v1.1 не формализует MCP-интеграцию как mandatory. Но RECOMMENDED

---
<!-- tags: architecture -->




## 16. MCP Extension (Informative)

NPP v1.1 не формализует MCP-интеграцию как mandatory. Но RECOMMENDED 
для порталов, используемых совместно с LLM (Claude, ChatGPT, Gemini).

MCP wrapper (`portal-mcp.py` в reference implementation) SHOULD 
экспонировать минимум 5 tools:

- `nautilus_query(query, repos=None)` — search across ecosystem
- `nautilus_list_repos()` — list all repos with metadata
- `nautilus_query_repo(repo, query)` — query single repo
- `nautilus_consensus_check(concept)` — consensus validation
- `nautilus_describe()` — ecosystem philosophy and metadata

Формальная MCP-спецификация будет частью NPP v1.2 или v2.0.

---

<!-- similar-docs -->

---

**Похожие документы:**
- [[128-доступные-инструменты]] (сходство 0.18)
- [[129-примеры-запросов-в-claude]] (сходство 0.14)
- [[103-appendix-b-change-log]] (сходство 0.13)


<!-- see-also -->

---

**Смотрите также:**
- [[128-доступные-инструменты]]
- [[129-примеры-запросов-в-claude]]
- [[103-appendix-b-change-log]]
- [[22-10-queryresult-structure]]

<!-- backlinks-auto -->
## Упоминается в

- [[103-appendix-b-change-log|Appendix B: Change Log]]
- [[README|Вакансии Anthropic — Анализ по кластерам]]
- [[128-доступные-инструменты|Доступные инструменты]]
- [[131-ограничения-текущей-версии-0-1-0-draft|Ограничения текущей версии (0.1.0-draft)]]
- [[129-примеры-запросов-в-claude|Примеры запросов (в Claude)]]
## Упоминается в

- [[README|Вакансии Anthropic — Анализ по кластерам]]

<!-- related-auto -->
## Связанные документы

- [[128-доступные-инструменты|Доступные инструменты]] _37%_
- [[129-примеры-запросов-в-claude|Примеры запросов (в Claude)]] _29%_
- [[131-ограничения-текущей-версии-0-1-0-draft|Ограничения текущей версии (0.1.0-draft)]] _21%_
- [[07-2-terminology|2. Terminology]] _17%_
- [[77-2-terminology|2. Terminology]] _17%_
## Связанные документы

- [[128-доступные-инструменты|Доступные инструменты]] _42%_
- [[129-примеры-запросов-в-claude|Примеры запросов (в Claude)]] _42%_
- [[131-ограничения-текущей-версии-0-1-0-draft|Ограничения текущей версии (0.1.0-draft)]] _29%_
- [[103-appendix-b-change-log|Appendix B: Change Log]] _25%_
- [[07-2-terminology|2. Terminology]] _21%_
- [[34-appendix-b-change-log|Appendix B: Change Log]] _21%_
- [[77-2-terminology|2. Terminology]] _21%_
- [[104-appendix-c-references|Appendix C: References]] _17%_
