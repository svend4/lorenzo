# Round 18 — Лог поисковой сессии

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** Agentic RAG (10 подходов), Synthetic Data Toolkit, RAG Incident Management, FRIDA (RU embeddings)

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| 10 актуальных RAG-подходов | независимый исследователь | orchestration / knowledge | `projects/agentic-rag-10-approaches.md` |
| Synthetic Data Toolkit (DataDreamer + Distilabel + Bespoke Curator) | MWS / разные команды | ingestion / knowledge | `projects/synthetic-data-toolkit.md` |
| RAG-агент для инцидент-менеджмента | OTUS | orchestration / analytics | `projects/rag-incident-management.md` |
| FRIDA — русскоязычные embeddings | SberDevices | knowledge / memory | `projects/frida-russian-embeddings.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| FRIDA + Lorenzo search | improve_embedding_index | TF-IDF → нейронные embeddings: recall@10 +15-25% для RU | ⭐⭐⭐⭐⭐ |
| Agentic RAG + improve_llm_qa | весь стек | `improve_llm_qa.py` с retrieval-петлёй = мультишаговые ответы | ⭐⭐⭐⭐⭐ |
| Distilabel + Lorenzo corpus | 2483 карточки | Автогенерация Q&A из корпуса → fine-tuning (паттерн R15) | ⭐⭐⭐⭐ |
| Incident RAG + ADD (R13) | ADD feedback loop | RAG база решений + ADD chronicles = self-healing knowledge base | ⭐⭐⭐⭐ |
| FRIDA + Sberbank KG (R17) | hybrid search | Оба от SberDevices: FRIDA (вектор) + Apache Jena (граф) = полный hybrid | ⭐⭐⭐⭐ |
| Synthetic Data + RAG Eval (R16) | CI pipeline | Distilabel → синтетика → RAGAS бенчмарк перед деплоем | ⭐⭐⭐⭐ |

## Главные находки раунда

**FRIDA** (SberDevices, декабрь 2024 → #1 ruMTEB май 2025) — MIT-лицензия, 128M параметров, обходит OpenAI text-embedding-3-large на русских задачах (+3.7 avg ruMTEB). Asymmetric search: `query_prefix + document_prefix`. Прямая замена TF-IDF в `improve_embedding_index.py` — самое высокоприоритетное улучшение Lorenzo из всех 18 раундов.

**Agentic RAG** (1029616, май 2026) — систематизация: 10 подходов от Naive до Self-RAG / Corrective RAG / Adaptive RAG. Ключевой сдвиг: retrieval = инструмент агента (не фиксированный этап). Corrective RAG добавляет evaluator: нерелевантные docs → web search fallback. Self-RAG: 4 специальных токена управляют решением о retrieval.

**Synthetic Data Toolkit** (MWS, 932066) — три инструмента разного уровня: DataDreamer (академический, воспроизводимость), Distilabel (production, Argilla), Bespoke Curator (минималистичный, 2025). Lorenzo corpus (2483 карточки) → Distilabel Q&A → QLoRA fine-tuning (паттерн R15) = специализированная модель для `improve_llm_qa.py`.

**RAG Incident Management** (OTUS, 912228) — паттерн self-improving loop: каждый решённый инцидент автоматически записывается в базу → улучшает retrieval следующего. Применимо к Lorenzo как knowledge maintenance agent: "инцидент" = битая ссылка, противоречие, устаревший документ.

## Сводная карта R01–R18

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

**Итого: 76 проектов, 40+ авторов**

## Что осталось на R19

- **Multimodal RAG** — обработка PDF, таблиц, изображений в единой RAG-системе (Docling, Unstructured, ColPali)
- **Локальные LLM для enterprise** — Ollama в production: балансировка нагрузки, мониторинг, HA
- **AI-ассистент для code generation** — не Copilot-клоны, а нишевые: тестирование, рефакторинг, документация
- **Vector DB сравнение 2026** — Qdrant vs Weaviate vs Chroma vs Milvus: бенчмарки на русских корпусах
