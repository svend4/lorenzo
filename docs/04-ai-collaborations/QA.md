# Q&A: 04-ai-collaborations

> [!NOTE]
> Раздел `QA` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary -->
> _Автоматически сгенерировано по 15 файлам раздела._
**Проекты:** CardIndex[^cardindex], AgentFS[^agentfs], knowledge-space[^knowledge-space], LiteParse, Legal RAG[^rag], Hybrid RAG, Graph RAG, SENTINEL[^sentinel]

---
<!-- tags: rag, security, knowledge, ingestion, architecture, roadmap, collaboration -->




_Автоматически сгенерировано по 15 файлам раздела._

## Как реализован forensic RAG с доказуемостью?

Упоминаются: **liteparse**, **bounding box**, **page-level**, **evidence**

## Что такое Evidence Envelope и зачем он нужен?

Упоминаются: **Evidence Envelope**, **source_id**, **page**, **span**

## Какие RAG-подходы сравниваются в документах?

Упоминаются: **Legal RAG**, **Hybrid RAG**, **Graph RAG**, **LiteParse**

## Какие 5 архитектурных зазоров выделены в исследовании?

Упоминаются: **зазор**, **карточка**, **evidence**, **memory governance**, **agent contract**

## Что входит в интеграционный контракт между слоями?

Упоминаются: **card envelope**, **Evidence Envelope**, **memory write**, **skill policy**, **review record**

## Каковы этапы MVP и их оценка по времени?

Упоминаются: **mvp**, **итерац**, **фаза**, **неделя**

## Что входит в первую итерацию прототипа?

Упоминаются: **evidence-first**, **unified card**, **page/span**, **manual review**

## Кто ключевые авторы проектов для контакта?

Упоминаются: **Андрей Чуян**, **Виталий Оборин**, **kksudo**, **spbmolot**

## Какие вопросы лучше задавать авторам при первом контакте?

Упоминаются: **первый вопрос**, **архитектурный**, **шаблон**, **контакт**

## Какие инструменты обеспечивают безопасность агентов?

Упоминаются: **SENTINEL**, **LiteLLM**, **Tool Search**, **Auto AI Router**

## Какова политика доступа по умолчанию (tool classes)?

Упоминаются: **read-only**, **allowlist**, **path guard**, **quarantine**

## Как организован бюджетный роутинг между моделями?

Упоминаются: **routing**, **budget**, **litellm**, **local model**

## Как работает AgentFS и что такое .agentos?

Упоминаются: **agentos**, **vault**, **compile**, **persistent state**

## Что такое knowledge-space и для кого он предназначен?

Упоминаются: **reference card**, **agent-readable**, **785**, **gotcha**

## Как CardIndex хранит и версионирует карточки?

Упоминаются: **cardindex**, **card_id**, **state**, **hash**, **dedup**

<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [README](README.md)
- [OUTLINE](../OUTLINE.md)
- [READABILITY](../READABILITY.md)
- [READING_TIME](../READING_TIME.md)
- [SEARCH](../SEARCH.md)
- [TABLES](../TABLES.md)



## Использование
```bash
# Запуск
python scripts/improve_qa.py
```

<!-- similar-docs -->

---

**Похожие документы:**
- [QA](../obsidian/04-ai-collaborations/QA.md) (сходство 0.99)
- [QA](../01-svyazi/QA.md) (сходство 0.85)
- [QA](../obsidian/01-svyazi/QA.md) (сходство 0.84)



<!-- footnotes-added -->

---

[^rag]: Retrieval-Augmented Generation — генерация с поиском

[^cardindex]: OSS-проект: индекс знаний на карточках (MIT)

[^agentfs]: OSS-проект: файловая система для AI-агентов (MIT)

[^sentinel]: OSS-проект: безопасность и allowlist для MCP

[^knowledge-space]: OSS-проект: база знаний 785+ карточек (MIT)
