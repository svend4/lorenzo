# 06-discovery — Раунды поиска проектов

Пронумерованные итерации поиска уникальных OSS-проектов с Хабра
и ценных комбинаций для Svyazi 2.0.

## Что ищем

1. **Уникальные проекты** — то, что сложно найти стандартным поиском:
   нестандартные авторы, нишевые темы, эксперименты без звёзд на GitHub
2. **Ценные комбинации** — два простых проекта, которые вместе дают новое свойство
3. **Новых авторов** — разработчики, готовые к коллаборации

## Раунды

| Раунд | Статус | Проектов | Ключевая тема | Папка |
|-------|--------|----------|---------------|-------|
| Round 01 | ✅ Завершён | 9 | Memory + Knowledge | `docs/05-habr-projects/` |
| Round 02 | ✅ Завершён | 6 | Voice, parsing, YAML | `round-02/` |
| Round 03 | ✅ Завершён | 3 | Code review, fine-tuned LLM | `round-03/` |
| Round 04 | ✅ Завершён | 3 | Agent platform, MCP protocol | `round-04/` |
| Round 05 | ✅ Завершён | 3 | Autonomous pipeline, Russian NLP | `round-05/` |
| Round 06 | ✅ Завершён | 4 | Video AI, CLI agents, GitHub automation | `round-06/` |
| Round 07 | ✅ Завершён | 4 | Multi-agent arch, agent safety, MCP pipeline | `round-07/` |
| Round 08 | ✅ Завершён | 4 | Codebase MCP, scientific ingestion, edu AI | `round-08/` |
| Round 09 | ✅ Завершён | 4 | GraphRAG, decentralized AI, coding agent | `round-09/` |
| Round 10 | ✅ Завершён | 4 | Viral simulation, self-hosted stacks, Rust | `round-10/` |
| Round 11 | ✅ Завершён | 4 | Desktop agents, edge AI, voice embedded | `round-11/` |
| Round 12 | ✅ Завершён | 4 | Data analytics AI, audio gen, vector DBs | `round-12/` |
| Round 13 | ✅ Завершён | 4 | Observability, ADD, self-healing tests, OCR | `round-13/` |
| Round 14 | ✅ Завершён | 4 | Context Engineering, DSPy, AI security, MarkItDown | `round-14/` |
| Round 15 | ✅ Завершён | 4 | Code review AI, Text2SQL, fine-tuning, LLM security | `round-15/` |
| Round 16 | ✅ Завершён | 4 | No-LangChain, monitoring LLM, GigaAM-v3 ASR, RAG eval | `round-16/` |
| Round 17 | ✅ Завершён | 4 | CoT research, LLM-Wiki, Knowledge Graph, LLM DBA | `round-17/` |
| Round 18 | ✅ Завершён | 4 | Agentic RAG, synthetic data, incident AI, RU embeddings | `round-18/` |
| Round 19 | ✅ Завершён | 4 | Multimodal RAG (Docling), doc review AI, vector DB, LLM inference | `round-19/` |
| Round 20 | ✅ Завершён | 4 | LLM unit tests, DeepSeek V3.2, Reasoning models, LLM economics | `round-20/` |
| Round 21 | ✅ Завершён | 4 | Multi-agent case, A2A protocol, LLM privacy, RU classification | `round-21/` |
| Round 22 | ✅ Завершён | 4 | Legal NLP, LLM AppSec, self-hosted AI, Graph RAG prod | `round-22/` |
| Round 23 | ✅ Завершён | 4 | HR AI, Durable State агентов, RPA+AI Enterprise, Prompt Injection | `round-23/` |
| Round 24 | ✅ Завершён | 4 | DevOps LLM fine-tuning, AIOps Sberbank, EdTech AI, Private LLM стек | `round-24/` |
| Round 25 | ✅ Завершён | 4 | Юридический RAG, нормоконтроль LLM, AI-наука, визуальное тестирование | `round-25/` |
| Round 26 | 🔜 Следующий | — | LLM финансы/BI, кастомные embeddings, Supply Chain AI, LLM как B2B SaaS | — |

**Итого: 104 проекта, 54+ авторов**

## Шаблон раунда

Каждый `round-XX/` содержит:
- `session-log.md` — что искали, запросы, ссылки на статьи Хабра
- `projects/` — один файл на проект (шаблон: см. ниже)
- `combinations/` — найденные пары и ансамбли

## Шаблон файла проекта

```markdown
# Название проекта

**Автор:** @habr_username  
**Хабр:** https://habr.com/...  
**GitHub:** https://github.com/...  
**Слой:** memory / knowledge / orchestration / ingestion / ui  
**Уникальность:** (1-2 предложения — чем отличается от аналогов)

## Что делает

## Почему интересно для Svyazi

## Возможные комбинации

## Контакт
```
