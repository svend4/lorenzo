# Round 15 — Лог поисковой сессии

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** AI Code Review (локальный CI/CD), Text-to-SQL агенты, Fine-tuning LLM 2026, LLM Immune System

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| AI Review (локальная LLM в CI/CD) | Nikita Filonov | quality / cicd / code-review | `projects/ai-review-local-llm.md` |
| Text2SQL X5Tech | X5 Retail Group | analytics / orchestration / SQL | `projects/text2sql-x5tech.md` |
| Fine-tuning LLM 2026 | OTUS (руководство) | knowledge / optimization / local | `projects/llm-finetuning-2026.md` |
| LLM Immune System | независимый разработчик | security / quality / middleware | `projects/llm-immune-system.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| Fine-tuning + 60 проектов Lorenzo | docs corpus | Дообучение Qwen 2.5 7B на базе Svyazi = локальный советник по проектам | ⭐⭐⭐⭐⭐ |
| Text2SQL + audit.db Lorenzo | BI Pattern (R12) | Агент отвечает на вопросы об аудите MCP-серверов через SQL | ⭐⭐⭐⭐⭐ |
| AI Review + DevClaw (R06) | GitHub automation | DevClaw создаёт PR → AI Review автоматически ревьюирует → полный CI-цикл | ⭐⭐⭐⭐ |
| Immune System + Security Audit (R14) | 5-фазный фреймворк | Audit находит уязвимости → Immune System закрывает в runtime (3ms) | ⭐⭐⭐⭐ |
| Fine-tuning + DSPy (R14) | prompt optimization | DSPy автогенерирует обучающие примеры для fine-tuning | ⭐⭐⭐ |

## Главные находки раунда

**Fine-tuning LLM 2026** (1026700) — переломный момент: дообучение 7–8B на 16 ГБ VRAM стало задачей одного разработчика. Qwen 2.5 7B + QLoRA + Unsloth = локальный агент знающий Lorenzo corpus. Первая статья за 15 раундов фиксирующая этот переход.

**AI Review** (github.com/Nikita-Filonov/ai-review) — единственный найденный за 15 раундов open-source CI/CD инструмент с локальным LLM-ревью: GitHub Actions + Ollama, ноль кода не уходит в облако. Прямое применение к репозиторию Lorenzo.

**Text2SQL X5Tech** (981494, февраль 2026) — корпоративный опыт применения CoT + Schema-aware + RAG для SQL-генерации на русских данных (MERA бенчмарк). Техники применимы к `audit.db` Lorenzo: вопросы об MCP-событиях на естественном языке.

**LLM Immune System** (996896) — токен-бай-токен фильтрация с задержкой 3 мс. Middleware-паттерн: работает с любым streaming LLM без изменения логики. Закрывает runtime-уязвимости, которые статический Security Audit (R14) не может поймать.

## Сводная карта R01–R15

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

**Итого: 64 проекта, 34+ авторов**

## Что осталось на R16

- **Workflow-оркестрация без LangChain** — чистый Python / граф / Temporal для агентов (статьи типа R15 "без LangChain: почему абстракции ломаются")
- **AI для работы с Kubernetes/инфраструктурой** — операционный AI, GitOps + LLM
- **Evaluation фреймворки** — как оценивать качество работы агентов (RAGAS, DeepEval, TruLens)
- **Аудио AI продвинутый** — многоканальная аудио обработка, speaker diarization, русскоязычные ASR
