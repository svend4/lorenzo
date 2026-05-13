---
state: approved
---

# Результаты последнего поиска — что нашлось и что не нашлось

<!-- toc-auto -->
## Contents

- [Использование](#использование)
- [Смотрите также](#смотрите-также)


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — выбор имени Lorenzo как codename для Catalyst Agent (Lorenzo Medici, DHLab umbrella).

---
<!-- tags: anthropic, collaboration -->

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.





> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — выбор имени Lorenzo как codename для Catalyst Agent (Lorenzo Medici, DHLab umbrella).

Результаты последнего поиска — что нашлось и что не нашлось

Что НЕ нашлось

Точного аналога Catalyst Agent / Lorenzo нет. Я искал в нескольких направлениях:

AI scout талантов разработчиков → нашлись только negative use cases (scammers использующие AI агентов для targeting разработчиков на Хабр Карьере)

AI matchmaking разработчиков → не нашлось

AI curator + synthesis + outreach combination → нет

Это confirms the hypothesis: Lorenzo Catalyst Agent — genuinely emerging category, не established product.

Что нашлось как partial analogues

1. marmelab/curator-ai (GitHub, MIT)

Reads list articles, selects best, summarizes по interests

Powered by OpenAI API

Limitation: только news curation, не code synthesis, не outreach

Что взять: pattern для monitoring + selection

2. NocoBase «AI employees»

AI as roles в business operations

Read data models, interface configurations, business context

Execute tasks при triggers

Limitation: enterprise focus, internal systems, не cross-creator synthesis

Что взять: «AI as role/persona» pattern

3. Eigent (eigent-ai) — open source Cowork alternative

Built on CAMEL-AI

Multi-Agent Workforce

Apache 2.0

Developer Agent + Browser Agent + Document Agent + Multi-Modal Agent

Limitation: workforce automation, не identifying/synthesizing community work

Что взять: multi-agent coordination patterns

4. OpenHands (MIT)

Universal agent controller

Multi-agent collaboration

Multi-session management

Limitation: developer task automation, не community synthesis

Что взять: agent controller architecture

<!-- see-also -->

---

## Использование
```bash
# Поиск по теме документа
python scripts/improve_semantic_search.py --query "Результаты последнего поиска что"
```

## Смотрите также
- [06-level-5-full-network](../phased-deployment/06-level-5-full-network.md)
- 00-question-[lorenzo-codename](00-question-lorenzo-codename.md)
- [08-personal-multi-agent-hub](../../habr-unique-projects/extra-examples/08-personal-multi-agent-hub.md)
- [03-section-3-solution-architecture](../../anthropic-vacancies/beneficial-deployments-concept/03-section-3-solution-architecture.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (6):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)
- [README](README.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [01-search-results-not-found](../../obsidian/lorenzo-agent/naming/01-search-results-not-found.md) (сходство 0.92)
- [00-question-lorenzo-codename](00-question-lorenzo-codename.md) (сходство 0.23)
- [00-question-lorenzo-codename](../../obsidian/lorenzo-agent/naming/00-question-lorenzo-codename.md) (сходство 0.23)

