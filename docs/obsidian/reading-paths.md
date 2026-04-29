---
title: "Reading paths — рекомендуемые маршруты по монорепозиторию"
tags:
  - memory
  - orchestration
  - knowledge
  - ingestion
  - architecture
  - roadmap
  - anthropic
  - collaboration
  - general
date: 2026-04-29
---

# Reading paths — рекомендуемые маршруты по монорепозиторию

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> Документов в `docs/` много (около 470). Ниже — **тематические маршруты** для разных интересов: начните с верхнего пункта и двигайтесь вниз.
**Проекты:** Svyazi, CardIndex, Yodoca, NGT Memory, MemNet, Wikontic

---

<!-- toc -->
## Содержание

- [1. «Я хочу понять, что такое Lorenzo (имя репозитория)»](#1-я-хочу-понять-что-такое-lorenzo-имя-репозитория)
- [2. «Я хочу собрать прототип Svyazi 2.0»](#2-я-хочу-собрать-прототип-svyazi-20)
- [3. «Я хочу понять Nautilus Portal Protocol»](#3-я-хочу-понять-nautilus-portal-protocol)
- [4. «Я хочу комбинировать технологии для новых свойств»](#4-я-хочу-комбинировать-технологии-для-новых-свойств)
- [5. «Я ищу коллабораторов на Хабре»](#5-я-ищу-коллабораторов-на-хабре)
- [6. «Я разбираю карьерные опции в Anthropic»](#6-я-разбираю-карьерные-опции-в-anthropic)
- [7. «Я ищу конкретный компонент по имени»](#7-я-ищу-конкретный-компонент-по-имени)
- [8. «Я хочу понять архитектуру вашего DHLab серии»](#8-я-хочу-понять-архитектуру-вашего-dhlab-серии)
- [Полный листинг](#полный-листинг)

---

<!-- tags: memory, orchestration, knowledge, ingestion, architecture, roadmap, anthropic, collaboration -->




Документов в `docs/` много (около 470). Ниже — **тематические маршруты** для разных интересов: начните с верхнего пункта и двигайтесь вниз.

## 1. «Я хочу понять, что такое Lorenzo (имя репозитория)»

1. [[README|`lorenzo-agent/README.md`]] — общий обзор.
2. [[01-kto-ty|`lorenzo-agent/01-kto-ty.md`]] и [[03-tvoya-missiya|`lorenzo-agent/03-tvoya-missiya.md`]] — суть.
3. [[04-komu-ty-sluzhish|`lorenzo-agent/04-komu-ty-sluzhish.md`]] — слоистая модель «уязвимые группы ← создатели ← AI community ← DHLab».
4. [[README|`lorenzo-agent/specification/README.md`]] — 10 фундаментальных вопросов, приведших к промпту.
5. [[README|`lorenzo-agent/phased-deployment/README.md`]] — 6 уровней поэтапной деплоймента.
6. [[README|`lorenzo-agent/operationalized/README.md`]] — конкретная 6-узловая pipeline.

## 2. «Я хочу собрать прототип Svyazi 2.0»

1. [[README|`svyazi-2-0/README.md`]] — обзор разделов.
2. [[executive-summary|`svyazi-2-0/overview/executive-summary.md`]] — главный вывод за 1 страницу.
3. [[projects-map|`svyazi-2-0/overview/projects-map.md`]] — карта найденных проектов.
4. [[README|`svyazi-2-0/components/README.md`]] — детали по каждому проекту-кирпичику.
5. [[integration-spec|`svyazi-2-0/architecture/integration-spec.md`]] — пять интеграционных контрактов.
6. [[mvp-plan|`svyazi-2-0/prototype/mvp-plan.md`]] — план MVP на 12–18 дней.
7. [[risks|`svyazi-2-0/prototype/risks.md`]], [[roadmap|`svyazi-2-0/prototype/roadmap.md`]] — риски и дальнейшие итерации.
8. [`svyazi-2-0/security/`](svyazi-2-0/security/) — default policy, privacy, бюджетный роутинг.
9. [`svyazi-2-0/outreach/`](svyazi-2-0/outreach/) — кому писать и какие вопросы задавать.

## 3. «Я хочу понять Nautilus Portal Protocol»

1. [[README|`nautilus/README.md`]] — обзор всех DHLab papers.
2. [[00-abstract-status|`nautilus/npp-v1-1/00-abstract-status.md`]] и [[01-introduction|`nautilus/npp-v1-1/01-introduction.md`]].
3. [[02-terminology|`nautilus/npp-v1-1/02-terminology.md`]] — основные термины.
4. [[19-adr-001-federation-over-merging|`nautilus/npp-v1-1/19-adr-001-federation-over-merging.md`]] — ключевое архитектурное обоснование.
5. [[03-registry|`nautilus/npp-v1-1/03-registry.md`]], [[04-passport|`nautilus/npp-v1-1/04-passport.md`]] — контракты.
6. [[06-adapter-interface|`nautilus/npp-v1-1/06-adapter-interface.md`]] — Adapter API.
7. [[12-onboarding-paths|`nautilus/npp-v1-1/12-onboarding-paths.md`]] — как подключиться.

## 4. «Я хочу комбинировать технологии для новых свойств»

1. [[README|`technology-combinations/README.md`]].
2. [[01-08-summary|`technology-combinations/synthesis-tables/01-08-summary.md`]] — главный паттерн «скромные родители → мощные дети».
3. [`technology-combinations/combinations/`](technology-combinations/combinations/) — 35 индивидуальных карточек комбинаций.
4. [[01-legal-ai-stack|`technology-combinations/mega-stacks/01-legal-ai-stack.md`]] → [[02-ultimate-legal-ai|`02-ultimate-legal-ai.md`]] → [[03-dsl-ast|`03-dsl-ast.md`]] → [[04-event-sourcing-consensus|`04-event-sourcing-consensus.md`]].

## 5. «Я ищу коллабораторов на Хабре»

1. [[01-three-key-candidates|`ai-collaborations/candidates/01-three-key-candidates.md`]] — K2-18, Wikontic, NGT Memory.
2. [[03-synthesis-hebbian-collaboration-graph|`ai-collaborations/candidates/03-synthesis-hebbian-collaboration-graph.md`]] — синтез.
3. [`habr-unique-projects/key-findings/`](habr-unique-projects/key-findings/) — ключевые находки (Yodoca, MemNet, PDA, Дочкина).
4. [[4-summary-authors|`habr-unique-projects/final-ensembles/4-summary-authors.md`]] — список имён.
5. [[06-final-tier-ranking|`anthropic-vacancies/extra-collaborator-findings/06-final-tier-ranking.md`]] — финальный tier ranking 12 collaborators.
6. [[source-projects|`ai-collaborations/source-projects.md`]] — все 39 Хабр-источников.
7. [[message-template|`svyazi-2-0/outreach/message-template.md`]] — шаблон первого сообщения.

## 6. «Я разбираю карьерные опции в Anthropic»

1. [[overview|`anthropic-vacancies/overview.md`]] — 16 кластеров найма (436 ролей).
2. [[signals|`anthropic-vacancies/signals.md`]] — что говорит структура.
3. [[02-final-ranking|`anthropic-vacancies/profile-mapping/03-integral-final/02-final-ranking.md`]] — финальное ранжирование под профиль svend4.
4. [[04-stronger-paths-outside-anthropic|`anthropic-vacancies/profile-mapping/03-integral-final/04-stronger-paths-outside-anthropic.md`]] — альтернативы (fellowships, accelerators, гранты).
5. [[README|`anthropic-vacancies/beneficial-deployments-concept/README.md`]] — outline concept document для outreach.
6. [[README|`anthropic-vacancies/ai-managed-virtual-company/README.md`]] — альтернатива «один человек / $500K» как AI-управляемая команда фрилансеров (Variant C).
7. [[README|`anthropic-vacancies/mmorpg-for-programmers/README.md`]] — гипотеза gamified work для технарей.
8. [[README|`anthropic-vacancies/hermes-comparison/README.md`]] — сравнение с Hermes Agent (Nous Research) и переоценка приоритетов.

## 7. «Я ищу конкретный компонент по имени»

→ [[components-by-name|`glossary/components-by-name.md`]] — алфавитный список с обратными ссылками.

→ [[authors-by-name|`glossary/authors-by-name.md`]] — список авторов.

→ [[concepts|`glossary/concepts.md`]] — ключевые понятия (CardIndex, Hot/Slow path, STDP, Sequential vs Coordinator, etc.).

## 8. «Я хочу понять архитектуру вашего DHLab серии»

Читайте в этом порядке:

1. [[README|`nautilus/okwf-concept/README.md`]] — фундаментальный концепт.
2. [[README|`nautilus/representative-agent-layer-en/README.md`]] — Cinderella Syndrome, общая идея.
3. [[README|`nautilus/professional-colleague-agents-en/README.md`]] — типология агентов.
4. [[README|`nautilus/composite-skills-agents/README.md`]] — ансамбли агентов.
5. [[README|`nautilus/double-triangle-architecture/README.md`]] — топология.
6. [[README|`nautilus/infrastructure-layer-b-en/README.md`]] — missing middle Layer B.
7. [[README|`nautilus/npp-v1-1/README.md`]] — формальная спецификация.
8. [[README|`nautilus/review-methodology/README.md`]] — методология review.
9. [[README|`nautilus/ingit-cowork-en/README.md`]] — практическая интеграция.

## Полный листинг

См. [[README|`README.md`]] этой папки для алфавитного списка всех тем.

<!-- see-also -->

---

**Смотрите также:**
- [[PRIORITIES]]
- [[SEARCH]]
- [[SITEMAP]]
- [[READING_ORDER]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[PRIORITIES]] (сходство 0.17)
- [[PRIORITIES]] (сходство 0.17)
- [[SEE_ALSO]] (сходство 0.16)

