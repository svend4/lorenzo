---
template: project-component
version: "1.0"
author: "nlaik"
author_handle: "@nlaik"
component: LiteParse
projects: [research-docs, LiteParse]
layer: ingestion
license: Apache-2.0
maturity: beta
priority: 2
tags: [liteparse, pdf, forensic-qa, bounding-boxes, visual-grounding, spatial-parsing, html-report, evidence]
---
<!-- autofill-status -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

## Статус

| Параметр | Значение |
|----------|---------|
| Теги | — |
| Упоминаний в репо | 594 |
| Слой | ingestion/evidence |
| Контакт | [@nlaik](../../contacts/nlaik.md) |
| Статус связи | не писали |

_Обновлено: 2026-05-10_

# research-docs + LiteParse

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> projects: ["research-docs", "LiteParse"]
**Проекты:** Svyazi[^svyazi], AgentFS[^agentfs], knowledge-space[^knowledge-space], LiteParse, Yodoca[^yodoca], agent-memory-mcp

---

<!-- toc -->
## Содержание

- [Статус](#статус)
- [Профиль проекта](#профиль-проекта)
- [Описание](#описание)
- [Ключевые компоненты](#ключевые-компоненты)
- [Синергия со Svyazi 2.0](#синергия-со-svyazi-20)
- [Применение в архитектуре](#применение-в-архитектуре)
- [Сравнение с подходами](#сравнение-с-подходами)
- [Контакт](#контакт)
- [Смотрите также](#смотрите-также)

---




<!-- summary: Forensic document QA с HTML-отчётом и bounding boxes на PDF-страницах — visual grounding для RAG[^rag]-систем -->
<!-- tags: liteparse, pdf, forensic, bounding-boxes, visual-citations, spatial-text, html-report, evidence, document-qa -->

## Профиль проекта

| Параметр | Значение |
|----------|---------|
| Автор | nlaik / Jerry Liu / LlamaIndex |
| GitHub | @nlaik |
| Источник | Хабр + GitHub |
| Лицензия | **Apache 2.0** (LiteParse) |
| Maturity | Активный OSS |
| Слой в Svyazi | ingestion / evidence |

## Что это

research-docs + LiteParse — система Forensic Document QA: вместо стандартного "ответить на вопрос по PDF" она создаёт HTML-отчёт с визуальными цитатами и `bounding boxes` на страницах исходного документа. Каждый факт в ответе привязан к конкретной области конкретной страницы — это visual grounding.

LiteParse — локальный парсер документов с `spatial text parsing`: он не просто извлекает текст, но сохраняет координаты каждого слова на странице. Это позволяет строить visually-anchored ответы, которых обычным RAG-системам не хватает.

## Ключевые особенности

- **Spatial text parsing** — разбор PDF с сохранением координат (x, y, w, h) каждого слова
- **Bounding boxes** — визуальная привязка цитат к областям на страницах документа
- **Visual citations** — в HTML-отчёте каждая цитата показывает выделенный фрагмент страницы
- **Multi-format docs** — PDF, DOCX, изображения, таблицы
- **HTML evidence report** — финальный отчёт как интерактивный HTML с встроенными страницами
- **Локальный парсер** — всё работает офлайн, без внешних API
- **LlamaIndex интеграция** — совместим с экосистемой Jerry Liu

## Синергия со Svyazi 2.0

- **Evidence Envelope** из PROTOTYPE_SPEC — LiteParse как источник `evidence_chunks` с spatial_ref: `{page, bbox}`
- **Visual grounding** решает проблему «откуда это взялось» в RAG-ответах — каждый факт имеет точную привязку
- **Bounding boxes** → поле `source_span` в Evidence Envelope: `{file, page, bbox, score}`
- **HTML отчёт** — human-readable артефакт для ревью перед ApprovalMode("review") в SkillPolicy
- **Apache 2.0** — прямая коммерческая интеграция
- **Офлайн** — соответствует принципу local-first в Svyazi (GDPR-safe)

## Применение в архитектуре

LiteParse закрывает слой "structured ingestion with evidence" — то, чего нет у CardStore (просто markdown) и у BM25-поиска (нет координат). Для юридических, медицинских и академических документов, где важно не только найти ответ, но и показать откуда он взят — это критический компонент.

## Сравнение с подходами

| Подход | Visual grounding | Coordinate-level | Local |
|--------|-----------------|------------------|-------|
| **LiteParse** | **✓ bounding boxes** | **✓ слово-уровень** | **✓** |
| pdfplumber | ✗ (только текст) | ✓ координаты | ✓ |
| PyMuPDF | частично | ✓ | ✓ |
| PDF.js | ✗ | ✗ | ✗ |

## Контакт

- Контактный файл: [docs/contacts/nlaik.md](../../contacts/nlaik.md)

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "research docs LiteParse"
```

## Смотрите также

- [AgentFS](agentfs.md) — файловое ядро для хранения extracted documents
- [knowledge-space](knowledge-space.md) — база знаний, пополняемая через LiteParse ingestion pipeline
- [agent-memory-mcp](../memory/agent-memory-mcp.md) — memory layer для parsed document facts
- [Yodoca: консолидация и забывание](../memory/yodoca.md) — nightly consolidation extracted content

---
_Создано: 2026-05-10_

<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [README](README.md)
- [knowledge-space](knowledge-space.md)
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)



<!-- footnotes-added -->

---

[^rag]: Retrieval-Augmented Generation — генерация с поиском

[^agentfs]: OSS-проект: файловая система для AI-агентов (MIT)

[^yodoca]: OSS-проект: система памяти с консолидацией (Apache 2.0)

[^svyazi]: Главный проект: экосистема AI-компонентов

[^knowledge-space]: OSS-проект: база знаний 785+ карточек (MIT)

<!-- similar-docs -->

---

**Похожие документы:**
- [research-docs-liteparse](../../obsidian/05-habr-projects/knowledge/research-docs-liteparse.md) (сходство 0.95)
- [mclaude](mclaude.md) (сходство 0.28)
- [rufler](rufler.md) (сходство 0.26)

