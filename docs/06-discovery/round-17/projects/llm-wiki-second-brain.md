---
date: 2026-05-15
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# LLM-Wiki — второй мозг как инфраструктура для AI-агента

<!-- toc-auto -->
<!-- tags: llm-wiki-second-brain, docs -->


<!-- summary -->
> Автор: независимый разработчик (Хабр, май 2026) Хабр: https://habr.com/ru/articles/1031970/
Хабр: https://habr.com/ru/articles/1031970/  
GitHub: vault с AGENTS.md (Obsidian + Claude Code / Codex CLI)  
Слой: knowledge / orchestration / memory  
Дата: май 2026  
Уникальность: Смена парадигмы


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** независимый разработчик (Хабр, май 2026)  
**Хабр:** https://habr.com/ru/articles/1031970/  
**GitHub:** vault с AGENTS.md (Obsidian + Claude Code / Codex CLI)  
**Слой:** knowledge / orchestration / memory  
**Дата:** май 2026  
**Уникальность:** Смена парадигмы: «второй мозг» строят теперь **не для себя, а для агента**. Метафора: Obsidian = IDE, LLM = программист, wiki = кодовая база. Три операции: Ingest, Query, Lint. AGENTS.md работает без изменений в Claude Code, Codex CLI и Cursor.

## Парадигма

### Раньше (PKM)
> Второй мозг = инструмент мышления для человека.  
> Человек читает, связывает, вспоминает.

### Теперь (LLM-Wiki)
> Второй мозг = инфраструктура для AI-агента.  
> Агент ingests, queries, lints. Человек выбирает направление.

## Три операции

```
Ingest:  новый источник → агент читает → обновляет wiki
         (автоматически: summary, теги, связи с существующим)
         ↓
Query:   вопрос → не к набору файлов, а к готовой карте знаний
         (агент знает структуру, может рассуждать над ней)
         ↓
Lint:    аудит базы → сломанные ссылки, устаревшие утверждения,
         противоречия, страницы без связей
```

## AGENTS.md как universal interface

```markdown
# AGENTS.md (в корне vault)

## Структура wiki
- /inbox/     — новые необработанные материалы
- /projects/  — активные проекты
- /reference/ — справочный материал (постоянный)
- /archive/   — завершённые

## Операции
- ingest <url/file>  — добавить источник
- query <вопрос>     — спросить базу знаний
- lint               — аудит целостности
```

`AGENTS.md` не меняется при смене инструмента (Claude Code → Codex → Cursor).

## Вдохновение: Karpathy-wiki паттерн

Andrej Karpathy строит живую wiki поверх Obsidian, где агент поддерживает структуру.  
LLM-Wiki = русскоязычная реализация этого подхода с open-source vault.

## Lorenzo = LLM-Wiki в production

Lorenzo **уже реализует** этот паттерн:
- `docs/` = wiki (база знаний)
- `CLAUDE.md` = AGENTS.md
- `improve_*.py` = операции Ingest/Query/Lint
- `improve_watch.py` = continuous Lint

Статья даёт **теоретическое обоснование** архитектуры Lorenzo и язык для её описания.  
**Lorenzo is a LLM-Wiki for Svyazi community intelligence.**

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **LLM-Wiki + Context Engineering (R14)** | AGENTS.md = применение Context Engineering к wiki |
| **LLM-Wiki + MarkItDown (R14)** | Ingest: любой формат → MarkItDown → wiki автоматически |
| **LLM-Wiki + RAG Eval (R16)** | Lint операция = RAGAS-аудит качества базы знаний |
| **LLM-Wiki + ADD (R13)** | Wiki становится memory для ADD feedback loop |

## Контакт

- Статья: https://habr.com/ru/articles/1031970/ (май 2026)
- Смежная (Obsidian + Claude Code): https://habr.com/ru/companies/bothub/articles/985736/
- Смежная (локально без подписок): https://habr.com/ru/articles/1022080/
- Смежная (второй мозг для агента): https://habr.com/ru/articles/1031112/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
