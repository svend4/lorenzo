# Round 21 — Лог поисковой сессии

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** Multi-agent orchestration case (3 агента → 5 человек), A2A протокол v1.0, Jay Guard (LLM privacy), Альфа-Банк LLM классификация

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| Оркестрация 2026: 3 агента вместо отдела | независимый (анонимный кейс) | orchestration / analytics | `projects/multiagent-orchestration-case.md` |
| A2A протокол v1.0 — стандарт агент↔агент | Cloud.ru / Google | orchestration / knowledge | `projects/a2a-protocol-agent-interoperability.md` |
| Jay Guard — анонимизация ПД для LLM API | Just AI | orchestration / ingestion | `projects/jay-guard-llm-privacy.md` |
| LLM для нестандартной классификации | Альфа-Банк ML | knowledge / ingestion | `projects/llm-finetuning-classification-alfabank.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| A2A + MCP (Lorenzo) | весь стек | MCP для инструментов + A2A для координации = полный агентный стек Lorenzo | ⭐⭐⭐⭐⭐ |
| 3-агент паттерн → Lorenzo ops | Discovery+Enricher+Monitor | автономный knowledge maintenance: поиск → обогащение → мониторинг | ⭐⭐⭐⭐⭐ |
| Jay Guard + improve_llm_*.py | privacy layer | анонимизация ПД перед Claude API = compliance для корпоративных клиентов | ⭐⭐⭐⭐ |
| Alfa Classification + Synthetic Data (R18) | fine-tuning | Distilabel генерирует 2000+ примеров → Qwen2.5 classify Lorenzo docs | ⭐⭐⭐⭐ |
| A2A + No-LangChain (R16) | agent coord | стандарт координации без LangGraph: agent=function, A2A=протокол | ⭐⭐⭐⭐ |

## Главные находки раунда

**3-агент кейс** (1008598, март 2026) — конкретные метрики замены реального отдела: 42→6 минут, -80% нагрузки. Ключевой инсайт: «инструменты важнее параметров» — агент с 1С+email > GPT-5 без интеграций. «Human in Loop — это не провал, а intended behavior». Process Map → роли → инструменты → модели (именно такой порядок!). Lorenzo: Discovery/Enricher/Monitor агенты = тот же паттерн.

**A2A v1.0** (1011868, апрель 2026) — первый production-ready стандарт агент↔агент (Google, март 2026). Agent Card как JSON-манифест, Tasks для долгоживущих операций, Push notifications, Multi-tenancy. Дополняет MCP: MCP = агент↔инструмент, A2A = агент↔агент. Cloud.ru = первая российская компания с публичным кейсом A2A. Lorenzo как A2A-агент в Svyazi 2.0 экосистеме.

**Jay Guard** (946392, 2025) — intelligent proxy Just AI: перехватывает запросы → NER-анонимизация ПД (ФИО, ИНН, ОГРН, паспорт) → LLM → деанонимизация ответа. F1 93.5% на русских корпусах. Benchmark на HuggingFace. Российское законодательство: ФЗ-152 = нельзя передавать ПД за рубеж. Smежный open-source: ChamelOn (95% точность, Apache 2.0).

**Alfa Classification** (968176, 2025) — «лабораторная работа» ML-команды банка: когда LLM > BERT (мало данных, меняющиеся категории, объяснения нужны), когда BERT > LLM (много данных, стабильные классы, скорость). Qwen2.5-7B fine-tuned = лучший баланс для Russian NLP. 500-1000 примеров дают 80-90% от полного датасета.

## Сводная карта R01–R21

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
| R20 | 4 | LLM unit tests, DeepSeek V3.2, Reasoning models, LLM economics | LLM Router pattern, mutation test pipeline |
| R21 | 4 | Multi-agent case, A2A protocol, LLM privacy, RU classification | A2A+MCP stack, 3-agent autonomous ops |

**Итого: 88 проектов, 46+ авторов**

## Что осталось на R22

- **LLM для юридических и compliance задач** — анализ договоров, извлечение обязательств, проверка на соответствие (legal NLP, не только финансы)
- **Embeddings и semantic search 2026** — новые архитектуры: ColBERT v2, late interaction, bi-encoder vs cross-encoder на русском
- **AI для DevSecOps** — SAST через LLM, авто-нахождение уязвимостей в коде, приоритизация
- **Self-hosted AI стек 2026** — Coolify + Ollama + n8n + open-WebUI: полный production стек без облака
