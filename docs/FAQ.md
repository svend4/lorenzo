# Часто задаваемые вопросы (FAQ)

<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** - Верхний треугольник — частично через GitHub Issues/Linear/Asana с AI-assisted triage.
> 🔧 **Подход:** → 68-about(docs/02-anthropic-vacancies/68-about.md) Лицензия Какой подход resonates?
> 🏷️ **Ключевые слова:** `anthropic`, `vacancies`, `questions`, `agent`, `nautilus`, `какой`, `legal`, `такое`
>


<!-- toc-auto -->
## Contents

- [Архитектура](#архитектура)
  - [Что такое MCP?](#что-такое-mcp)
  - [Каков статус готовности MVP?](#каков-статус-готовности-mvp)
  - [Какой вариант резонирует?](#какой-вариант-резонирует)
- [MVP/Запуск](#mvpзапуск)
  - [С чего начать?](#с-чего-начать)
  - [Сейчас, для этой конкретной сессии с семью документами, что вы хотите сделать?](#сейчас-для-этой-конкретной-сессии-с-семью-документами-что-вы-хотите-сделать)
- [Компоненты](#компоненты)
  - [Какова лицензия проекта?](#какова-лицензия-проекта)
  - [Как связаться с авторами компонентов?](#как-связаться-с-авторами-компонентов)
- [Интеграция](#интеграция)
  - [Какой направление приоритетно?](#какой-направление-приоритетно)
  - [Это реализуется существующими tools?](#это-реализуется-существующими-tools)
  - [Является ли наш Nautilus Portal Protocol still valuable? Или HMP makes it redundant?](#является-ли-наш-nautilus-portal-protocol-still-valuable-или-hmp-makes-it-redundant)
  - [Question Set 4: Your resources 4a) Budget для setup (€500-1500 одноразовый)?](#question-set-4-your-resources-4a-budget-для-setup-500-1500-одноразовый)
  - [Набор вопросов 4: Ваши ресурсы 4a) Бюджет для setup (€500-1500 одноразово)?](#набор-вопросов-4-ваши-ресурсы-4a-бюджет-для-setup-500-1500-одноразово)
  - [Why "Nautilus"?](#why-nautilus)
- [Лицензия](#лицензия)
  - [Какой подход resonates? Integration в OKWF document, или separate short paper?](#какой-подход-resonates-integration-в-okwf-document-или-separate-short-paper)
- [Общее](#общее)
  - [Что такое Svyazi 2.0?](#что-такое-svyazi-20)
  - [9.1. Перед началом (Pre-Phase A) - [ ] Документ действительно критически важен (см. §4.1)?](#91-перед-началом-pre-phase-a---документ-действительно-критически-важен-см-41)
  - [Что из этого feels aligned с вашими current capabilities и interest?](#что-из-этого-feels-aligned-с-вашими-current-capabilities-и-interest)
  - [10.3. Legal Questions What's the legal status of agent communications?](#103-legal-questions-whats-the-legal-status-of-agent-communications)
  - [10.4. Social Questions Will representative agents reduce or increase inequality?](#104-social-questions-will-representative-agents-reduce-or-increase-inequality)
  - [How do we ensure access for those who cannot pay?](#how-do-we-ensure-access-for-those-who-cannot-pay)
  - [What's the legal status of agent communications?](#whats-the-legal-status-of-agent-communications)
  - [10.3. Правовые Вопросы Каков правовой статус коммуникаций агента? Они обязательны для принципала?](#103-правовые-вопросы-каков-правовой-статус-коммуникаций-агента-они-обязательны-для-принципала)


_Извлечено: 54 вопросов и ответов_


## Архитектура

### Что такое MCP?

Model Context Protocol — открытый протокол Anthropic для взаимодействия LLM с внешними инструментами и данными. Ключевой элемент архитектуры Svyazi.

### Каков статус готовности MVP?

Согласно SCORING.md: 96% (159/164 баллов) — документация и архитектура готовы. Остаётся: связаться с авторами и реализовать прототип Knowledge OS.

### Какой вариант резонирует?

Если выберете первый или второй вариант, я могу написать в следующем сообщении. Если третий — то этот ответ остаётся как ваша заметка к шестому документу, и работа сессии завершена с шестью полноценными артефактами плюс этим архитектурным расширением.

_→ [248-приложение-c-архитектура-быстрого-старта-для-sgb-а](docs/02-anthropic-vacancies/248-приложение-c-архитектура-быстрого-старта-для-sgb-а.md)_


## MVP/Запуск

### С чего начать?

Начните с Executive Summary (docs/01-svyazi/01-executive-summary.md), затем MVP Planning (07-mvp-planning.md) и Roadmap (12-roadmap.md).

### Сейчас, для этой конкретной сессии с семью документами, что вы хотите сделать?

Вариант 1. Закрыть сессию, commitнуть все семь документов в Nautilus repository, начать использовать GitHub Discussions для дальнейших observations и refinements. Pragmatic compromise.

_→ [272-appendix-d-connection-diagram](docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md)_


## Компоненты

### Какова лицензия проекта?

Компоненты используют разные лицензии: MIT (AgentFS, knowledge-space), Apache 2.0 (Yodoca), BSL 1.1 (NGT-memory). Проект Lorenzo — MIT.

### Как связаться с авторами компонентов?

Контакты в docs/CONTACTS.md. Авторы: kksudo (Андрей) — AgentFS, spbmolot (Виталий) — ряд Habr-проектов. Используйте шаблон docs/templates/contact-outreach.md.


## Интеграция

### Какой направление приоритетно?

Хорошо. Пишу portal-mcp.py — MCP wrapper над Nautilus Portal. Это обёртка, которая экспонирует движок портала как tools для LLM через Model Context Protocol.

_→ [122-глоссарий](docs/02-anthropic-vacancies/122-глоссарий.md)_

### Это реализуется существующими tools?

Частично да. - Нижний треугольник — уже работает через MCP (каждый человек конфигурирует свои MCP servers для своих assistant'ов). - Верхний треугольник — частично через GitHub Issues/Linear/Asana с AI-assisted triage. - Протокол 3 — не реализован нигде . Это именно то, чем стоит заняться.

_→ [133-обратная-связь](docs/02-anthropic-vacancies/133-обратная-связь.md)_

### Является ли наш Nautilus Portal Protocol still valuable? Или HMP makes it redundant?

My honest answer: Document 1 still has unique value , но не как «we're going to build this». Скорее как:

_→ [341-приложение-c-образец-спецификаций-инструментов-ing](docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md)_

### Question Set 4: Your resources 4a) Budget для setup (€500-1500 одноразовый)?

4b) Budget для monthly operations (€100-500/month)? 4c) Можете maintain Claude API access для Lorenzo's «brain»?

_→ [342-что-такое-вариант-c-concept-document-для-anthropic](docs/02-anthropic-vacancies/342-что-такое-вариант-c-concept-document-для-anthropic.md)_

### Набор вопросов 4: Ваши ресурсы 4a) Бюджет для setup (€500-1500 одноразово)?

4b) Бюджет для месячных операций (€100-500/месяц)? 4c) Можете поддерживать Claude API доступ для «мозга» Lorenzo?

_→ [343-lorenzo-catalyst-agent-глубокая-проработка-специфи](docs/02-anthropic-vacancies/343-lorenzo-catalyst-agent-глубокая-проработка-специфи.md)_

### Why "Nautilus"?

A nautilus shell is a **spiral of nested chambers**, each larger than the last but built on the same geometry. This is *fractal scaling with preserved proportion*. Nautilus Protocol embodies the same pattern: repos nested inside an ecosystem, each self-contained yet connected by the same protocol, the same geometry of bridges.

_→ [68-about](docs/02-anthropic-vacancies/68-about.md)_


## Лицензия

### Какой подход resonates? Integration в OKWF document, или separate short paper?

И еще один thoughtful вопрос для consideration: в вашем личном случае , как retired engineer / disabled expert / researcher with limited public presence — personal AI agent уже существенно меняет вашу daily реальность? Или это в основном concept о других people? Если первое, конкретные примеры из ва

_→ [165-closing](docs/02-anthropic-vacancies/165-closing.md)_


## Общее

### Что такое Svyazi 2.0?

Svyazi 2.0 — это экосистема из 20+ взаимосвязанных OSS-проектов для построения AI-систем с памятью, оркестрацией агентов и безопасной обработкой данных.

### 9.1. Перед началом (Pre-Phase A) - [ ] Документ действительно критически важен (см. §4.1)?

- [ ] Есть время на Фазу C в течение 2 недель? - [ ] Две ветки будут работать на **полностью независимых** prompts (не «продолжи вариант A»)?

_→ [116-9-checklist-применения-методологии](docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md)_

### Что из этого feels aligned с вашими current capabilities и interest?

И один дополнительный вопрос, который поможет calibrate: когда вы говорите о «гнезде для больших птиц», вы видите себя в роли:

_→ [150-appendix-c-version-history](docs/02-anthropic-vacancies/150-appendix-c-version-history.md)_

### 10.3. Legal Questions What's the legal status of agent communications?

Are they binding on the principal? How does liability work when agent makes consequential errors? What jurisdictional rules apply when agent represents person in country A communicating with party in country B? How do existing regulations (GDPR, HIPAA, AI Act) apply specifically to representative agents?

_→ [179-10-open-questions](docs/02-anthropic-vacancies/179-10-open-questions.md)_

### 10.4. Social Questions Will representative agents reduce or increase inequality?

What happens to professions currently providing representational services (lawyers, agents, intermediaries) when AI agents become widespread? What new social dynamics emerge when most interactions involve mediation by agents? How do we preserve direct human connection in a world of mediated communication?

_→ [179-10-open-questions](docs/02-anthropic-vacancies/179-10-open-questions.md)_

### How do we ensure access for those who cannot pay?

What economic effects do widespread representative

_→ [179-10-open-questions](docs/02-anthropic-vacancies/179-10-open-questions.md)_

### What's the legal status of agent communications?

Are they binding on the principal?

_→ [179-10-open-questions](docs/02-anthropic-vacancies/179-10-open-questions.md)_

### 10.3. Правовые Вопросы Каков правовой статус коммуникаций агента? Они обязательны для принципала?

Как работает ответственность, когда агент совершает существенные ошибки? Какие юрисдикционные правила применяются, когда агент представляет человека в стране A, общающегося со стороной в стране B? Как существующие регуляции (GDPR, HIPAA, AI Act) применяются конкретно к представительским агентам?

_→ [200-10-открытые-вопросы](docs/02-anthropic-vacancies/200-10-открытые-вопросы.md)_

