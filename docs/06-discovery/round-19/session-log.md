# Round 19 — Лог поисковой сессии

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** Multimodal RAG (Docling), Desmond doc review agent (Альфа-Банк), Vector DB обзор 2025, LLM-инференс фреймворки

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| RAG Challenge победитель — Docling + multimodal PDF | независимый разработчик | ingestion / knowledge | `projects/rag-challenge-docling-multimodal.md` |
| Desmond — AI-агент проверки документации | Альфа-Банк | orchestration / quality | `projects/desmond-doc-review-agent.md` |
| Векторные БД для AI-агентов и RAG — большой обзор | независимый исследователь | knowledge / memory | `projects/vector-db-big-overview.md` |
| LLM-инференс: Ollama vs vLLM vs Triton vs llama.cpp vs SGLang | независимый исследователь | orchestration / memory | `projects/llm-inference-frameworks.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| Docling + MarkItDown (R14) | ingestion layer | MarkItDown = общий конвертер, Docling = PDF-таблицы специалист = полный ingest pipeline | ⭐⭐⭐⭐⭐ |
| Qdrant + FRIDA (R18) | vector search | FRIDA нейронные embeddings → Qdrant хранилище = production нейронный поиск по Lorenzo | ⭐⭐⭐⭐⭐ |
| SGLang + improve_llm_enrich | structured output | надёжный JSON без retry: SGLang гарантирует формат вывода | ⭐⭐⭐⭐ |
| Desmond-паттерн + improve_validate | quality layer | rule-based (Lorenzo) + LLM (Desmond) = двухуровневая проверка docs/ | ⭐⭐⭐⭐ |
| llama.cpp + Lorenzo offline | independence | полностью локальный Lorenzo без ANTHROPIC_API_KEY | ⭐⭐⭐⭐ |
| Docling + Agentic RAG (R18) | intelligent ingest | агент решает: нужен ли Docling для этого документа (PDF vs TXT) | ⭐⭐⭐ |

## Главные находки раунда

**Docling** (IBM, Apache 2.0, март 2025) — конкурсная победа: 100 annual reports (PDF 1000 стр) → Q&A за 2.5 часа. Ключевой инсайт: таблицы из PDF → Markdown сохраняя структуру → LLM читает без галлюцинаций. RRF-ансамбль BM25 + dense. Критический вывод: «магия RAG в деталях, не в сложности». Прямая связь с MarkItDown (R14) — образует полный ingestion layer.

**Desmond** (Альфа-Банк, 2025) — паттерн Cognitive Worker: агент без диалога, запускается по webhook из Jira, проверяет документ Confluence по 20+ критериям, возвращает structured report. −60% времени аналитиков. Применим к Lorenzo: post-commit hook → проверить изменённый docs/ файл → REVIEW_REPORT.md.

**Vector DB обзор** (961088, ноябрь 2025) — 12+ баз данных с рекомендациями по сценариям. Ключевые: Qdrant (production-ready, фильтрация, Rust), ChromaDB (PoC за 3 строки), pgvectorscale (если уже PG). Embedded LanceDB = замена search_index.json без сервера. Квантизация: binary vectors −97% памяти.

**LLM inference** (948934, 2025) — сравнение 6 фреймворков. Самый ценный инсайт: llama.cpp в 2.8–3.2× быстрее Ollama при тех же ресурсах. SGLang = structured output без retry (RadixAttention). Рекомендация для Lorenzo: разработка → Ollama, production → vLLM или llama.cpp, JSON-структуры → SGLang.

## Сводная карта R01–R19

| Раунд | Проектов | Ключевая тема | Лучшая находка |
|-------|----------|---------------|----------------|
| R01 | 9 | Memory + Knowledge | AgentFS, Yodoca, knowledge-space |
| R02 | 6 | Voice, parsing, YAML | Coreness Flow, Ирина, Dedoc |
| R03 | 3 | Code review, fine-tuned LLM | DevOps LLM паттерн |
| R04 | 3 | Agent platform, MCP protocol | TRAIL spec, OpenClaw |
| R05 | 3 | Autonomous pipeline, Russian NLP | News System паттерн, Natasha |
| R06 | 4 | Video AI, CLI agents, GitHub automation | Memory MCP v2, DevClaw паттерн |
| R07 | 4 | Multi-agent architecture, agent safety | openLight принцип, 9-агентный паттерн |
| R08 | 4 | Codebase MCP, scientific ingestion, edu AI | SocratiCode, Paper2Agent |
| R09 | 4 | GraphRAG, decentralized AI, coding agent | GraphRAG pipeline, HMP, OpenCode |
| R10 | 4 | Viral simulation, self-hosted stacks, Rust | MiroFish, n8n AI Stack |
| R11 | 4 | Desktop agents, edge AI, voice embedded | Союз (MCP desktop), RPi+Ирина voice pipeline |
| R12 | 4 | Data analytics AI, audio gen, vector DBs | Veai IDE agent, BI Agent Pattern |
| R13 | 4 | Observability, ADD, self-healing, OCR | Langfuse pattern, ADD feedback loop |
| R14 | 4 | Context Engineering, DSPy, security, ingestion | MarkItDown, Security Audit framework |
| R15 | 4 | Code review AI, Text2SQL, fine-tuning, LLM security | Fine-tuning 2026, AI Review CI/CD |
| R16 | 4 | No-LangChain, monitoring LLM, GigaAM-v3, RAG eval | GigaAM-v3 SOTA, Custom LLM distillation |
| R17 | 4 | CoT research, LLM-Wiki, Knowledge Graph, LLM DBA | LLM-Wiki paradigm, Sberbank KG production |
| R18 | 4 | Agentic RAG, synthetic data, incident AI, RU embeddings | FRIDA #1 ruMTEB, Agentic RAG taxonomy |
| R19 | 4 | Multimodal RAG, doc review AI, vector DB, LLM inference | Docling+RRF SoTA, Desmond Cognitive Worker |

**Итого: 80 проектов, 42+ авторов**

## Что осталось на R20

- **Prompt-free / instruction-following** — модели 2026, которые следуют инструкции без сложных промптов (Qwen3, Mistral Nemo, DeepSeek-V3)
- **AI для тестирования** — mutation testing, property-based testing через LLM, авто-генерация edge cases
- **Knowledge distillation 2026** — перегонка больших моделей в маленькие через synthetic traces (паттерн из R16 + свежие техники)
- **Streaming + real-time AI** — WebSocket-агенты, streaming RAG, событийные системы с LLM
