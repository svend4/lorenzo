---
title: "Часто задаваемые вопросы (FAQ)"
tags:
  - general
date: 2026-05-12
---

# Часто задаваемые вопросы (FAQ)

> [!NOTE]
> Раздел `FAQ` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary -->
> _Извлечено: 251 вопросов и ответов_
**Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, Yodoca, agent-memory-mcp

---

<!-- toc -->
## Содержание

- [Архитектура](#архитектура)
  - [Что такое MCP?](#что-такое-mcp)
  - [Каков статус готовности MVP?](#каков-статус-готовности-mvp)
  - [Какой вариант резонирует?](#какой-вариант-резонирует)
  - [Что это такое?](#что-это-такое)
  - [Q&A: 02-anthropic-vacancies > > !NOTE - Какие 5 архитектурных зазоров выделены в исследовании?](#qa-02-anthropic-vacancies-note---какие-5-архитектурных-зазоров-выделены-в-исследовании)
  - [Q&A: 04-ai-collaborations > > !NOTE - Как реализован forensic RAG с доказуемостью?](#qa-04-ai-collaborations-note---как-реализован-forensic-rag-с-доказуемостью)
  - [Q&A: meta-scripting > > !NOTE - Какие инструменты обеспечивают безопасность агентов?](#qa-meta-scripting-note---какие-инструменты-обеспечивают-безопасность-агентов)
  - [Принимаем эту architecture как Lorenzo vision (с моими caveats)?](#принимаем-эту-architecture-как-lorenzo-vision-с-моими-caveats)
- [MVP/Запуск](#mvpзапуск)
  - [С чего начать?](#с-чего-начать)
  - [Q&A: anthropic-vacancies > > !NOTE - Какие кластеры найма выделены у Anthropic?](#qa-anthropic-vacancies-note---какие-кластеры-найма-выделены-у-anthropic)
  - [Q&A: contacts > > !NOTE - Какие системы памяти описаны в этом разделе?](#qa-contacts-note---какие-системы-памяти-описаны-в-этом-разделе)
  - [[[QA|Q&A: anthropic-vacancies]] > > !NOTE - Какие кластеры найма выделены у Anthropic?](#qaqa-anthropic-vacancies-note---какие-кластеры-найма-выделены-у-anthropic)
  - [[[QA|Q&A: contacts]] > > !NOTE - Какие системы памяти описаны в этом разделе?](#qaqa-contacts-note---какие-системы-памяти-описаны-в-этом-разделе)
- [Компоненты](#компоненты)
  - [Какова лицензия проекта?](#какова-лицензия-проекта)
  - [Как связаться с авторами компонентов?](#как-связаться-с-авторами-компонентов)
  - [Открытые вопросы 1. Есть ли публичная документация по Memory OS (bi-temporal facts, gardener-loop)?](#открытые-вопросы-1-есть-ли-публичная-документация-по-memory-os-bi-temporal-facts-gardener-loop)
  - [Q&A: lorenzo-agent > > !NOTE - Какие кластеры найма выделены у Anthropic?](#qa-lorenzo-agent-note---какие-кластеры-найма-выделены-у-anthropic)
  - [[[QA|Q&A: lorenzo-agent]] > > !NOTE - Какие кластеры найма выделены у Anthropic?](#qaqa-lorenzo-agent-note---какие-кластеры-найма-выделены-у-anthropic)
- [Интеграция](#интеграция)
  - [Это реализуется существующими tools?](#это-реализуется-существующими-tools)
  - [Является ли наш Nautilus Portal Protocol still valuable? Или HMP makes it redundant?](#является-ли-наш-nautilus-portal-protocol-still-valuable-или-hmp-makes-it-redundant)
  - [Question Set 4: Your resources 4a) Budget для setup (€500-1500 одноразовый)?](#question-set-4-your-resources-4a-budget-для-setup-500-1500-одноразовый)
  - [Набор вопросов 4: Ваши ресурсы 4a) Бюджет для setup (€500-1500 одноразово)?](#набор-вопросов-4-ваши-ресурсы-4a-бюджет-для-setup-500-1500-одноразово)
  - [Why "Nautilus"?](#why-nautilus)
  - [Did creator approve final attribution?](#did-creator-approve-final-attribution)
- [Лицензия](#лицензия)
  - [Question 5: Каковы limits Lorenzo's authority?](#question-5-каковы-limits-lorenzos-authority)
  - [Какой подход resonates? Integration в OKWF document, или separate short paper?](#какой-подход-resonates-integration-в-okwf-document-или-separate-short-paper)
- [Общее](#общее)
  - [Что такое Svyazi 2.0?](#что-такое-svyazi-20)
  - [9.1. Перед началом (Pre-Phase A) - [ ] Документ действительно критически важен (см. §4.1)?](#91-перед-началом-pre-phase-a---документ-действительно-критически-важен-см-41)
  - [10.3. Legal Questions What's the legal status of agent communications?](#103-legal-questions-whats-the-legal-status-of-agent-communications)
  - [10.4. Social Questions Will representative agents reduce or increase inequality?](#104-social-questions-will-representative-agents-reduce-or-increase-inequality)
  - [How do we ensure access for those who cannot pay?](#how-do-we-ensure-access-for-those-who-cannot-pay)
  - [What's the legal status of agent communications?](#whats-the-legal-status-of-agent-communications)
  - [10.3. Правовые Вопросы Каков правовой статус коммуникаций агента? Они обязательны для принципала?](#103-правовые-вопросы-каков-правовой-статус-коммуникаций-агента-они-обязательны-для-принципала)
  - [10.4. Социальные Вопросы Снизят ли представительские агенты или увеличат неравенство?](#104-социальные-вопросы-снизят-ли-представительские-агенты-или-увеличат-неравенство)

---

<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, anthropic, collaboration -->




_Извлечено: 251 вопросов и ответов_


## Архитектура

### Что такое MCP?

Model Context Protocol — открытый протокол Anthropic для взаимодействия LLM с внешними инструментами и данными. Ключевой элемент архитектуры Svyazi.

### Каков статус готовности MVP?

Согласно SCORING.md: 96% (159/164 баллов) — документация и архитектура готовы. Остаётся: связаться с авторами и реализовать прототип Knowledge OS.

### Какой вариант резонирует?

Если выберете первый или второй вариант, я могу написать в следующем сообщении. Если третий — то этот ответ остаётся как ваша заметка к шестому документу, и работа сессии завершена с шестью полноценными артефактами плюс этим архитектурным расширением.

_→ [[248-приложение-c-архитектура-быстрого-старта-для-sgb-а]]_

### Что это такое?

**Svyazi 2.0** — экосистема из 20+ взаимосвязанных OSS-проектов для построения AI-систем с долгосрочной памятью, оркестрацией агентов и безопасной обработкой данных. Статус готовности: **100% 🟢 GO** (документация и архитектура).

_→ [[ONBOARDING]]_

### Q&A: 02-anthropic-vacancies > > !NOTE - Какие 5 архитектурных зазоров выделены в исследовании?

- Что входит в интеграционный контракт между слоями? - Какие кластеры найма выделены у Anthropic? - Какие роли наиболее релевантны для профиля svend4? - Кто ключевые авторы проектов для контакта? - Какие вопросы лучше задавать авторам при первом контакте? - Каковы этапы MVP и их оценка по времени? - Что входит в первую итерацию прототипа? _... ещё 17 разделов_ _Слов: 422_

_→ [[OUTLINE]]_

### Q&A: 04-ai-collaborations > > !NOTE - Как реализован forensic RAG с доказуемостью?

- Что такое Evidence Envelope и зачем он нужен? - Какие RAG-подходы сравниваются в документах? - Какие 5 архитектурных зазоров выделены в исследовании? - Что входит в интеграционный контракт между слоями? - Каковы этапы MVP и их оценка по времени? - Что входит в первую итерацию прототипа? - Кто ключевые авторы проектов для контакта? _... ещё 9 разделов_ _Слов: 362_

_→ [[OUTLINE]]_

### Q&A: meta-scripting > > !NOTE - Какие инструменты обеспечивают безопасность агентов?

- Какова политика доступа по умолчанию (tool classes)? - Как организован бюджетный роутинг между моделями? - Какие 5 архитектурных зазоров выделены в исследовании? - Что входит в интеграционный контракт между слоями? - Использование - Запуск _Слов: 148_

_→ [[OUTLINE]]_

### Принимаем эту architecture как Lorenzo vision (с моими caveats)?

Если да — должен ли я update Lorenzo системный промпт с этой архитектурой?

_→ [[06-conclusion-deserves-attention]]_


## MVP/Запуск

### С чего начать?

Начните с Executive Summary (docs/01-svyazi/01-executive-summary.md), затем MVP Planning (07-mvp-planning.md) и Roadmap (12-roadmap.md).

### Q&A: anthropic-vacancies > > !NOTE - Какие кластеры найма выделены у Anthropic?

- Какие роли наиболее релевантны для профиля svend4? - Использование - Запуск _Слов: 131_

_→ [[OUTLINE]]_

### Q&A: contacts > > !NOTE - Какие системы памяти описаны в этом разделе?

- Как происходит консолидация и забывание в памяти агентов? - Какова разница между эпизодической и семантической памятью? - Использование - Запуск _Слов: 146_

_→ [[OUTLINE]]_

### [[QA|Q&A: anthropic-vacancies]] > > !NOTE - Какие кластеры найма выделены у Anthropic?

- Какие роли наиболее релевантны для профиля svend4? - Использование - Запуск _Слов: 131_

_→ [[OUTLINE]]_

### [[QA|Q&A: contacts]] > > !NOTE - Какие системы памяти описаны в этом разделе?

- Как происходит консолидация и забывание в памяти агентов? - Какова разница между эпизодической и семантической памятью? - Использование - Запуск _Слов: 146_

_→ [[OUTLINE]]_


## Компоненты

### Какова лицензия проекта?

Компоненты используют разные лицензии: MIT (AgentFS, knowledge-space), Apache 2.0 (Yodoca), BSL 1.1 (NGT-memory). Проект Lorenzo — MIT.

### Как связаться с авторами компонентов?

Контакты в docs/CONTACTS.md. Авторы: kksudo (Андрей) — AgentFS, spbmolot (Виталий) — ряд Habr-проектов. Используйте шаблон docs/templates/contact-outreach.md.

### Открытые вопросы 1. Есть ли публичная документация по Memory OS (bi-temporal facts, gardener-loop)?

2. Планируется ли поддержка внешних источников (CardIndex / doc-ingestion)? 3. Как memory write API взаимодействует с внешними источниками? 4. Планируется ли поддержка batch-ingestion из документов?

_→ [[agent-memory-mcp]]_

### Q&A: lorenzo-agent > > !NOTE - Какие кластеры найма выделены у Anthropic?

- Какие роли наиболее релевантны для профиля svend4? - Каковы этапы MVP и их оценка по времени? - Что входит в первую итерацию прототипа? - Кто ключевые авторы проектов для контакта? - Какие вопросы лучше задавать авторам при первом контакте? - Как работает AgentFS и что такое .agentos? - Что такое knowledge-space и для кого он предназначен? _... ещё 11 разделов_ _Слов: 305_

_→ [[OUTLINE]]_

### [[QA|Q&A: lorenzo-agent]] > > !NOTE - Какие кластеры найма выделены у Anthropic?

- Какие роли наиболее релевантны для профиля svend4? - Каковы этапы MVP и их оценка по времени? - Что входит в первую итерацию прототипа? - Кто ключевые авторы проектов для контакта? - Какие вопросы лучше задавать авторам при первом контакте? - Как работает AgentFS и что такое .agentos? - Что такое knowledge-space и для кого он предназначен? _... ещё 11 разделов_ _Слов: 305_

_→ [[OUTLINE]]_


## Интеграция

### Это реализуется существующими tools?

Частично да. - Нижний треугольник — уже работает через MCP (каждый человек конфигурирует свои MCP servers для своих assistant'ов). - Верхний треугольник — частично через GitHub Issues/Linear/Asana с AI-assisted triage. - Протокол 3 — не реализован нигде . Это именно то, чем стоит заняться.

_→ [[133-обратная-связь]]_

### Является ли наш Nautilus Portal Protocol still valuable? Или HMP makes it redundant?

My honest answer: Document 1 still has unique value , но не как «we're going to build this». Скорее как:

_→ [[341-приложение-c-образец-спецификаций-инструментов-ing]]_

### Question Set 4: Your resources 4a) Budget для setup (€500-1500 одноразовый)?

4b) Budget для monthly operations (€100-500/month)? 4c) Можете maintain Claude API access для Lorenzo's «brain»?

_→ [[342-что-такое-вариант-c-concept-document-для-anthropic]]_

### Набор вопросов 4: Ваши ресурсы 4a) Бюджет для setup (€500-1500 одноразово)?

4b) Бюджет для месячных операций (€100-500/месяц)? 4c) Можете поддерживать Claude API доступ для «мозга» Lorenzo?

_→ [[343-lorenzo-catalyst-agent-глубокая-проработка-специфи]]_

### Why "Nautilus"?

A nautilus shell is a **spiral of nested chambers**, each larger than the last but built on the same geometry. This is *fractal scaling with preserved proportion*. Nautilus Protocol embodies the same pattern: repos nested inside an ecosystem, each self-contained yet connected by the same protocol, the same geometry of bridges.

_→ [[68-about]]_

### Did creator approve final attribution?

Это много steps. И violations damage Lorenzo's reputation rapidly.

_→ [[11-difficulties-and-recommendations]]_


## Лицензия

### Question 5: Каковы limits Lorenzo's authority?

Critical question для ethical design.

_→ [[05-q5-authority-limits]]_

### Какой подход resonates? Integration в OKWF document, или separate short paper?

И еще один thoughtful вопрос для consideration: в вашем личном случае, как retired engineer / disabled expert / researcher with limited public presence — personal AI agent уже существенно меняет вашу daily реальность? Или это в основном concept о других people? Если первое, конкретные примеры из ваш

_→ [[01-response]]_


## Общее

### Что такое Svyazi 2.0?

Svyazi 2.0 — это экосистема из 20+ взаимосвязанных OSS-проектов для построения AI-систем с памятью, оркестрацией агентов и безопасной обработкой данных.

### 9.1. Перед началом (Pre-Phase A) - [ ] Документ действительно критически важен (см. §4.1)?

- [ ] Есть время на Фазу C в течение 2 недель? - [ ] Две ветки будут работать на **полностью независимых** prompts (не «продолжи вариант A»)?

_→ [[116-9-checklist-применения-методологии]]_

### 10.3. Legal Questions What's the legal status of agent communications?

Are they binding on the principal? How does liability work when agent makes consequential errors? What jurisdictional rules apply when agent represents person in country A communicating with party in country B? How do existing regulations (GDPR, HIPAA, AI Act) apply specifically to representative agents?

_→ [[179-10-open-questions]]_

### 10.4. Social Questions Will representative agents reduce or increase inequality?

What happens to professions currently providing representational services (lawyers, agents, intermediaries) when AI agents become widespread? What new social dynamics emerge when most interactions involve mediation by agents? How do we preserve direct human connection in a world of mediated communication?

_→ [[179-10-open-questions]]_

### How do we ensure access for those who cannot pay?

What economic effects do widespread representative

_→ [[179-10-open-questions]]_

### What's the legal status of agent communications?

Are they binding on the principal?

_→ [[179-10-open-questions]]_

### 10.3. Правовые Вопросы Каков правовой статус коммуникаций агента? Они обязательны для принципала?

Как работает ответственность, когда агент совершает существенные ошибки? Какие юрисдикционные правила применяются, когда агент представляет человека в стране A, общающегося со стороной в стране B? Как существующие регуляции (GDPR, HIPAA, AI Act) применяются конкретно к представительским агентам?

_→ [[200-10-открытые-вопросы]]_

### 10.4. Социальные Вопросы Снизят ли представительские агенты или увеличат неравенство?

Что происходит с профессиями, в настоящее время предоставляющими представительские услуги (юристы, агенты, посредники), когда AI-агенты становятся распространёнными? Какие новые социальные динамики возникают, когда большинство взаимодействий включают опосредование агентами? Как мы сохраняем прямую человеческую связь в мире опосредованной коммуникации?

_→ [[200-10-открытые-вопросы]]_


<!-- backlinks -->

---

**Кто ссылается на этот документ (18):**
- [[116-9-checklist-применения-методологии]]
- [[200-10-открытые-вопросы]]
- [[memnet]]
- [[CONCEPTS]]
- [[INDEX]]
- [[ONBOARDING]]
- [[OUTLINE]]
- [[QUESTIONS]]
- _...ещё 10_



## Использование
```bash
# Запуск
python scripts/improve_faq.py
```

<!-- see-also -->

---

**Смотрите также:**
- [[QUESTIONS]]
- [[10-otkrytye-voprosy]]
- [[10-open-questions]]
- [[CLUSTERS]]

