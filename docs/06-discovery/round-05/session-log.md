# Round 05 — Лог поисковой сессии

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** образование, русский NLP, бизнес-аналитика, автономные системы, тестирование

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| AI Web Tester | неизвестен | AI testing / 57× token efficiency | `projects/ai-web-tester.md` |
| Autonomous News System | неизвестен | 5-agent pipeline / ingestion | `projects/autonomous-news-system.md` |
| Natasha | @natasha org | Russian NLP / production-grade | `projects/natasha-nlp.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| News System паттерн | Lorenzo corpus | 5-агентный ingestion pipeline | ⭐⭐⭐⭐⭐ |
| Natasha | improve_named_entity_index | ML-NER вместо regex для русского | ⭐⭐⭐⭐ |
| Natasha navec | improve_embedding_index | Русские эмбеддинги вместо TF-IDF | ⭐⭐⭐⭐ |
| AI Web Tester | AI Review (R03) | Полный QA-цикл | ⭐⭐⭐ |

## Главная находка раунда

**Autonomous News System** — единственный найденный за все 5 раундов проект,
который реализует **весь стек Svyazi** в production: ingestion + multi-agent +
local LLM + Telegram + автономная работа. Это не набор инструментов, а готовая
архитектура. Паттерн «5 агентов в пайплайне» прямо применим к Lorenzo.

**Natasha** — немедленно применима: заменить regex-NER в
`improve_named_entity_index.py` на Natasha → точность именованных сущностей
вырастет, леммы улучшат поиск.

## Сводная карта R01–R05

| Раунд | Проектов | Ключевая тема | Лучшая находка |
|-------|----------|---------------|----------------|
| R01 | 9 | Memory + Knowledge | AgentFS, Yodoca, knowledge-space |
| R02 | 6 | Voice, parsing, YAML | Coreness Flow, Ирина, Dedoc |
| R03 | 3 | Code review, fine-tuned LLM | DevOps LLM паттерн |
| R04 | 3 | Agent platform, MCP protocol | TRAIL spec, OpenClaw |
| R05 | 3 | Autonomous pipeline, Russian NLP | News System паттерн, Natasha |

**Итого: 24 проекта, 17+ авторов**

## Что осталось на R06

- Проекты для работы с изображениями/видео + AI
- AI-инструменты для научных публикаций (arXiv, цитирование)
- Decentralized / federated AI (без единого сервера)
- Специализированные MCP-серверы (базы данных, файловые системы)
