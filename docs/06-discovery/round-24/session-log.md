# Round 24 — Лог поисковой сессии

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** DevOps LLM дистилляция, Sberbank AIOps, EdTech AI-first, Private LLM стек

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| Обучил свой DevOps-агент: fine-tuning + дистилляция qwen3 (3 части) | независимый разработчик | DevOps / orchestration / fine-tuning | `projects/devops-llm-finetuning-distillation.md` |
| Sberbank AIOps: ML в мониторинге — предотвращение инцидентов (-73% MTTR) | Сбербанк (Павел Стёпуро) | DevOps / analytics / orchestration | `projects/sberbank-aiops-incident-prevention.md` |
| EdTech-платформа за неделю: AI-first workflow (адаптивные тесты, оценка эссе) | независимый разработчик | knowledge / orchestration / analytics | `projects/edtech-platform-ai-week.md` |
| 7 pet-проектов с LLM: приватный on-device RAG, firewall, privacy gateway | независимый разработчик | security / memory / orchestration | `projects/private-llm-stack-7-projects.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| DevOps LLM + Self-hosted (R22) | infrastructure | Ollama + fine-tuned qwen = полностью локальный DevOps-агент без облачной зависимости | ⭐⭐⭐⭐⭐ |
| AIOps + RAG Incident (R18) | ops knowledge | Sberbank KB + Agentic RAG: агент сам выбирает стратегию поиска по похожим инцидентам | ⭐⭐⭐⭐⭐ |
| 7 Projects + Jay Guard (R21) | privacy stack | Privacy Gateway (Проект 4) = улучшенный Jay Guard + двусторонняя анонимизация | ⭐⭐⭐⭐ |
| EdTech + Graph RAG (R22) | knowledge graph | Граф концептов курса → Neo4j → студент видит связи между темами (R22 96.7%) | ⭐⭐⭐⭐ |
| DevOps LLM + LLM Router (R20) | cost/quality | Маршрутизация: простые DevOps-задачи → fine-tuned local ($0), сложные → Claude | ⭐⭐⭐⭐ |

## Главные находки раунда

**DevOps LLM дистилляция** (1033128/1033426/1033434, май 2026) — 3-частная серия: разработчик провёл 2 недели вместо отпуска, обучая свой DevOps-агент, потому что ни одна существующая локальная модель не справлялась с реальными задачами (SSH, nginx, docker, systemd). Подход: Teacher (Claude/GPT-4o) → 2107 traces → LoRA fine-tune qwen3:14b → 10/10 реальных задач vs 7/10 у базовой. Ключ: acceptance rate 76%, борьба с catastrophic forgetting через смешанный датасет. Для Lorenzo: кастомная модель для Lorenzo-специфичных tool calls.

**Sberbank AIOps** (1015336, март 2026) — Три слоя ML в production мониторинге при ~50M пользователей: Anomaly Detection (Prophet/LSTM), Incident Predictor (XGBoost), Alert Correlator (Louvain community detection). LLM добавляет объяснение + auto-remediation. Метрики: MTTR -73% (45→12 мин), alert noise -85%, 35% инцидентов предотвращено. Для Lorenzo: AIOps паттерн над audit.db (мониторинг выполнения 159+ скриптов).

**EdTech платформа** (1010294, март 2026) — Полная образовательная платформа за 1 неделю соло: AI-генерация тестов по таксономии Блума, адаптация сложности, LLM-оценка эссе с рубрикой, чат-помощник через RAG. Демонстрирует скорость AI-first разработки 2026: схема БД 2ч, CRUD 4ч, UI 1 день. Педагогический дизайн и качество контента — по-прежнему требуют человека. Для Lorenzo: Knowledge Testing паттерн.

**7 LLM Pet-Projects** (988774, январь 2026) — Практическая карта privacy-first AI стека: (1) Private RAG on-device, (2) Tool Retrieval через VectorDB, (3) Agent Firewall, (4) Privacy Gateway (локальная NER + облачный LLM), (5) Inference Optimizer (prompt cache, batching), (6) Multimodal pipeline, (7) Cost Tracker. Все 7 → единая система. Для Lorenzo: каждый компонент применим к существующей архитектуре.

## Сводная карта R01–R24

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
| R22 | 4 | Legal NLP, LLM AppSec, self-hosted AI, Graph RAG prod | Graph RAG 96.7%, n8n+Ollama self-hosted |
| R23 | 4 | HR AI, Durable State агентов, RPA+AI Enterprise, Prompt Injection | Durable State архитектура, Phantom framework |
| R24 | 4 | DevOps LLM fine-tuning, AIOps Sberbank, EdTech AI, Private LLM стек | DevOps дистилляция 10/10, Sberbank -73% MTTR |

**Итого: 100 проектов, 52+ авторов**

## Что осталось на R25

- **LLM для юридической автоматизации** — генерация договоров, нормоконтроль, анализ судебной практики
- **AI-ассистенты для науки** — автоматизация литературного обзора, генерация гипотез, анализ данных экспериментов
- **Streaming и real-time AI** — streaming inference, WebSocket агенты, live data processing с LLM
- **AI для тестирования UI** — vision-based UI testing, AI QA-инженер, screenshot-to-test
