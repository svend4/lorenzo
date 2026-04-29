# Q&A: 01-svyazi

<!-- summary -->
> > 🎯 **Проблема:** Q&A: 01-svyazi Contents - Как реализован forensic RAG^rag с доказуемостью?(как-реализован-forensic-ragrag-с-доказуемостью) - Что такое Evidence Envelope и зачем он нужен?(что-такое
**Проекты:** Svyazi, LiteParse, Legal RAG, Hybrid RAG, Graph RAG, SENTINEL, LiteLLM, Auto AI Router

---
<!-- tags: rag, security, knowledge, ingestion, architecture, roadmap, anthropic, self-improvement, collaboration -->




<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Q&A: 01-svyazi Contents - Как реализован forensic RAG^rag с доказуемостью?(как-реализован-forensic-ragrag-с-доказуемостью) - Что такое Evidence Envelope и зачем он нужен?(что-такое
> 🔧 **Подход:** Упоминаются: Evidence Envelope, sourceid, page, span Какие RAG-подходы сравниваются в документах?
> 🏷️ **Ключевые слова:** `какие`, `упоминаются`, `evidence`, `envelope`, `между`, `входит`, `прототипа`, `реализован`
>


<!-- toc-auto -->
## Contents

- [Как реализован forensic RAG[^rag] с доказуемостью?](#как-реализован-forensic-ragrag-с-доказуемостью)
- [Что такое Evidence Envelope и зачем он нужен?](#что-такое-evidence-envelope-и-зачем-он-нужен)
- [Какие RAG-подходы сравниваются в документах?](#какие-rag-подходы-сравниваются-в-документах)
- [Какие инструменты обеспечивают безопасность агентов?](#какие-инструменты-обеспечивают-безопасность-агентов)
- [Какова политика доступа по умолчанию (tool classes)?](#какова-политика-доступа-по-умолчанию-tool-classes)
- [Как организован бюджетный роутинг между моделями?](#как-организован-бюджетный-роутинг-между-моделями)
- [Какие 5 архитектурных зазоров выделены в исследовании?](#какие-5-архитектурных-зазоров-выделены-в-исследовании)
- [Что входит в интеграционный контракт между слоями?](#что-входит-в-интеграционный-контракт-между-слоями)
- [Каковы этапы MVP и их оценка по времени?](#каковы-этапы-mvp-и-их-оценка-по-времени)
- [Что входит в первую итерацию прототипа?](#что-входит-в-первую-итерацию-прототипа)
- [Кто ключевые авторы проектов для контакта?](#кто-ключевые-авторы-проектов-для-контакта)
- [Какие вопросы лучше задавать авторам при первом контакте?](#какие-вопросы-лучше-задавать-авторам-при-первом-контакте)


> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

_Автоматически сгенерировано по 14 файлам раздела._

## Как реализован forensic RAG[^rag] с доказуемостью?

→ _См. также:_ [QA](docs/04-ai-collaborations/QA.md)

Упоминаются: **liteparse**, **bounding box**, **page-level**, **evidence**

## Что такое Evidence Envelope и зачем он нужен?

→ _См. также:_ [QA](docs/03-technology-combinations/QA.md)

Упоминаются: **Evidence Envelope**, **source_id**, **page**, **span**

## Какие RAG-подходы сравниваются в документах?

→ _См. также:_ [QA](docs/03-technology-combinations/QA.md)

Упоминаются: **Legal RAG**, **Hybrid RAG**, **Graph RAG**, **[LiteParse](../docs/01-svyazi/01-executive-summary.md)**

## Какие инструменты обеспечивают безопасность агентов?

→ _См. также:_ [QA](docs/04-ai-collaborations/QA.md)

Упоминаются: **SENTINEL**, **LiteLLM**, **Tool Search**, **Auto AI Router**

## Какова политика доступа по умолчанию (tool classes)?

→ _См. также:_ [QA](docs/04-ai-collaborations/QA.md)

Упоминаются: **read-only**, **allowlist**, **path guard**, **quarantine**

## Как организован бюджетный роутинг между моделями?

→ _См. также:_ [QA](docs/04-ai-collaborations/QA.md)

Упоминаются: **routing**, **budget**, **litellm**

## Какие 5 архитектурных зазоров выделены в исследовании?

→ _См. также:_ [QA](docs/02-anthropic-vacancies/QA.md)

Упоминаются: **зазор**, **карточка**, **evidence**, **memory governance**, **agent contract**

## Что входит в интеграционный контракт между слоями?

→ _См. также:_ [QA](docs/05-habr-projects/QA.md)

Упоминаются: **card envelope**, **Evidence Envelope**, **memory write**, **skill policy**, **review record**

## Каковы этапы MVP и их оценка по времени?

→ _См. также:_ [QA](docs/05-habr-projects/QA.md)

Упоминаются: **mvp**, **итерац**, **фаза**, **неделя**

## Что входит в первую итерацию прототипа?

→ _См. также:_ [QA](docs/05-habr-projects/QA.md)

Упоминаются: **evidence-first**, **unified card**, **page/span**, **manual review**

## Кто ключевые авторы проектов для контакта?

→ _См. также:_ [QA](docs/05-habr-projects/QA.md)

Упоминаются: **Андрей Чуян**, **Виталий Оборин**, **kksudo**, **spbmolot**

## Какие вопросы лучше задавать авторам при первом контакте?

Упоминаются: **первый вопрос**, **архитектурный**, **шаблон**, **контакт**

<!-- similar-docs -->

---

**Похожие документы:**
- [QA](docs/04-ai-collaborations/QA.md) (сходство 0.82)
- [QA](docs/02-anthropic-vacancies/QA.md) (сходство 0.52)
- [QA](docs/QA.md) (сходство 0.51)



<!-- footnotes-added -->

---

[^rag]: Retrieval-Augmented Generation — генерация с поиском
