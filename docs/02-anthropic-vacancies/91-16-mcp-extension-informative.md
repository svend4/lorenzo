# 16. MCP Extension (Informative)

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
