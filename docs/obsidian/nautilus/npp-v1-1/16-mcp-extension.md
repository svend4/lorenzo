---
title: "16. MCP Extension (Informative)"
tags:
  - architecture
  - anthropic
  - nautilus
date: 2026-04-29
---

# 16. MCP Extension (Informative)

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

---
<!-- tags: architecture, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — Nautilus Portal Protocol v1.1 RFC, написанный совместно с Claude.

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

<!-- see-also -->

---

**Смотрите также:**
- [[91-16-mcp-extension-informative]]
- [[17-appendix-b-change-log]]
- [[13-reference-implementation]]
- [[11-relevance-ranking]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[91-16-mcp-extension-informative]] (сходство 0.60)
- [[91-16-mcp-extension-informative]] (сходство 0.60)
- [[11-relevance-ranking]] (сходство 0.33)

