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
| Round 09 | 🔜 Следующий | — | Federated AI, knowledge graphs, domain agents | — |

**Итого: 36 проектов, 20+ авторов**

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
