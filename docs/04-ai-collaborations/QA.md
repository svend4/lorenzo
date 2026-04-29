# Q&A: 04-ai-collaborations

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

_Автоматически сгенерировано по 15 файлам раздела._

## Как реализован forensic RAG[^rag] с доказуемостью?

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

## Как работает AgentFS[^agentfs] и что такое .agentos?

Упоминаются: **agentos**, **vault**, **compile**, **persistent state**

## Что такое knowledge-space[^knowledge_space] и для кого он предназначен?

Упоминаются: **reference card**, **agent-readable**, **785**, **gotcha**

## Как CardIndex[^cardindex] хранит и версионирует карточки?

Упоминаются: **cardindex**, **card_id**, **state**, **hash**, **dedup**

<!-- similar-docs -->

---

**Похожие документы:**
- [QA](docs/01-svyazi/QA.md) (сходство 0.82)
- [QA](docs/02-anthropic-vacancies/QA.md) (сходство 0.63)
- [QA](docs/QA.md) (сходство 0.62)



<!-- footnotes-added -->

---

[^rag]: Retrieval-Augmented Generation — генерация с поиском

[^cardindex]: OSS-проект: индекс знаний на карточках (MIT)

[^agentfs]: OSS-проект: файловая система для AI-агентов (MIT)

[^knowledge_space]: OSS-проект: база знаний 785+ карточек (MIT)
