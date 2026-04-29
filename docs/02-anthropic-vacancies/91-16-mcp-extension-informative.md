# 16. MCP Extension (Informative)

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
- [128-доступные-инструменты](128-доступные-инструменты.md) (сходство 0.18)
- [129-примеры-запросов-в-claude](129-примеры-запросов-в-claude.md) (сходство 0.14)
- [103-appendix-b-change-log](103-appendix-b-change-log.md) (сходство 0.13)


<!-- see-also -->

---

**Смотрите также:**
- [128-доступные-инструменты](128-доступные-инструменты.md)
- [129-примеры-запросов-в-claude](129-примеры-запросов-в-claude.md)
- [103-appendix-b-change-log](103-appendix-b-change-log.md)
- [22-10-queryresult-structure](22-10-queryresult-structure.md)

<!-- backlinks-auto -->
## Упоминается в

- [Вакансии Anthropic — Анализ по кластерам](../README.md)

<!-- related-auto -->
## Связанные документы

- [Доступные инструменты](128-доступные-инструменты.md) _42%_
- [Примеры запросов (в Claude)](129-примеры-запросов-в-claude.md) _42%_
- [Ограничения текущей версии (0.1.0-draft)](131-ограничения-текущей-версии-0-1-0-draft.md) _29%_
- [Appendix B: Change Log](103-appendix-b-change-log.md) _25%_
- [2. Terminology](07-2-terminology.md) _21%_
- [Appendix B: Change Log](34-appendix-b-change-log.md) _21%_
- [2. Terminology](77-2-terminology.md) _21%_
- [Appendix C: References](104-appendix-c-references.md) _17%_
