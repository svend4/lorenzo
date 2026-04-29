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

1. [`lorenzo-agent/README.md`](lorenzo-agent/README.md) — общий обзор.
2. [`lorenzo-agent/01-kto-ty.md`](lorenzo-agent/01-kto-ty.md) и [`lorenzo-agent/03-tvoya-missiya.md`](lorenzo-agent/03-tvoya-missiya.md) — суть.
3. [`lorenzo-agent/04-komu-ty-sluzhish.md`](lorenzo-agent/04-komu-ty-sluzhish.md) — слоистая модель «уязвимые группы ← создатели ← AI community ← DHLab».
4. [`lorenzo-agent/specification/README.md`](lorenzo-agent/specification/README.md) — 10 фундаментальных вопросов, приведших к промпту.
5. [`lorenzo-agent/phased-deployment/README.md`](lorenzo-agent/phased-deployment/README.md) — 6 уровней поэтапной деплоймента.
6. [`lorenzo-agent/operationalized/README.md`](lorenzo-agent/operationalized/README.md) — конкретная 6-узловая pipeline.

## 2. «Я хочу собрать прототип Svyazi 2.0»

1. [`svyazi-2-0/README.md`](svyazi-2-0/README.md) — обзор разделов.
2. [`svyazi-2-0/overview/executive-summary.md`](svyazi-2-0/overview/executive-summary.md) — главный вывод за 1 страницу.
3. [`svyazi-2-0/overview/projects-map.md`](svyazi-2-0/overview/projects-map.md) — карта найденных проектов.
4. [`svyazi-2-0/components/README.md`](svyazi-2-0/components/README.md) — детали по каждому проекту-кирпичику.
5. [`svyazi-2-0/architecture/integration-spec.md`](svyazi-2-0/architecture/integration-spec.md) — пять интеграционных контрактов.
6. [`svyazi-2-0/prototype/mvp-plan.md`](svyazi-2-0/prototype/mvp-plan.md) — план MVP на 12–18 дней.
7. [`svyazi-2-0/prototype/risks.md`](svyazi-2-0/prototype/risks.md), [`svyazi-2-0/prototype/roadmap.md`](svyazi-2-0/prototype/roadmap.md) — риски и дальнейшие итерации.
8. [`svyazi-2-0/security/`](svyazi-2-0/security/) — default policy, privacy, бюджетный роутинг.
9. [`svyazi-2-0/outreach/`](svyazi-2-0/outreach/) — кому писать и какие вопросы задавать.

## 3. «Я хочу понять Nautilus Portal Protocol»

1. [`nautilus/README.md`](nautilus/README.md) — обзор всех DHLab papers.
2. [`nautilus/npp-v1-1/00-abstract-status.md`](nautilus/npp-v1-1/00-abstract-status.md) и [`nautilus/npp-v1-1/01-introduction.md`](nautilus/npp-v1-1/01-introduction.md).
3. [`nautilus/npp-v1-1/02-terminology.md`](nautilus/npp-v1-1/02-terminology.md) — основные термины.
4. [`nautilus/npp-v1-1/19-adr-001-federation-over-merging.md`](nautilus/npp-v1-1/19-adr-001-federation-over-merging.md) — ключевое архитектурное обоснование.
5. [`nautilus/npp-v1-1/03-registry.md`](nautilus/npp-v1-1/03-registry.md), [`nautilus/npp-v1-1/04-passport.md`](nautilus/npp-v1-1/04-passport.md) — контракты.
6. [`nautilus/npp-v1-1/06-adapter-interface.md`](nautilus/npp-v1-1/06-adapter-interface.md) — Adapter API.
7. [`nautilus/npp-v1-1/12-onboarding-paths.md`](nautilus/npp-v1-1/12-onboarding-paths.md) — как подключиться.

## 4. «Я хочу комбинировать технологии для новых свойств»

1. [`technology-combinations/README.md`](technology-combinations/README.md).
2. [`technology-combinations/synthesis-tables/01-08-summary.md`](technology-combinations/synthesis-tables/01-08-summary.md) — главный паттерн «скромные родители → мощные дети».
3. [`technology-combinations/combinations/`](technology-combinations/combinations/) — 35 индивидуальных карточек комбинаций.
4. [`technology-combinations/mega-stacks/01-legal-ai-stack.md`](technology-combinations/mega-stacks/01-legal-ai-stack.md) → [`02-ultimate-legal-ai.md`](technology-combinations/mega-stacks/02-ultimate-legal-ai.md) → [`03-dsl-ast.md`](technology-combinations/mega-stacks/03-dsl-ast.md) → [`04-event-sourcing-consensus.md`](technology-combinations/mega-stacks/04-event-sourcing-consensus.md).

## 5. «Я ищу коллабораторов на Хабре»

1. [`ai-collaborations/candidates/01-three-key-candidates.md`](ai-collaborations/candidates/01-three-key-candidates.md) — K2-18, Wikontic, NGT Memory.
2. [`ai-collaborations/candidates/03-synthesis-hebbian-collaboration-graph.md`](ai-collaborations/candidates/03-synthesis-hebbian-collaboration-graph.md) — синтез.
3. [`habr-unique-projects/key-findings/`](habr-unique-projects/key-findings/) — ключевые находки (Yodoca, MemNet, PDA, Дочкина).
4. [`habr-unique-projects/final-ensembles/4-summary-authors.md`](habr-unique-projects/final-ensembles/4-summary-authors.md) — список имён.
5. [`anthropic-vacancies/extra-collaborator-findings/06-final-tier-ranking.md`](anthropic-vacancies/extra-collaborator-findings/06-final-tier-ranking.md) — финальный tier ranking 12 collaborators.
6. [`ai-collaborations/source-projects.md`](ai-collaborations/source-projects.md) — все 39 Хабр-источников.
7. [`svyazi-2-0/outreach/message-template.md`](svyazi-2-0/outreach/message-template.md) — шаблон первого сообщения.

## 6. «Я разбираю карьерные опции в Anthropic»

1. [`anthropic-vacancies/overview.md`](anthropic-vacancies/overview.md) — 16 кластеров найма (436 ролей).
2. [`anthropic-vacancies/signals.md`](anthropic-vacancies/signals.md) — что говорит структура.
3. [`anthropic-vacancies/profile-mapping/03-integral-final/02-final-ranking.md`](anthropic-vacancies/profile-mapping/03-integral-final/02-final-ranking.md) — финальное ранжирование под профиль svend4.
4. [`anthropic-vacancies/profile-mapping/03-integral-final/04-stronger-paths-outside-anthropic.md`](anthropic-vacancies/profile-mapping/03-integral-final/04-stronger-paths-outside-anthropic.md) — альтернативы (fellowships, accelerators, гранты).
5. [`anthropic-vacancies/beneficial-deployments-concept/README.md`](anthropic-vacancies/beneficial-deployments-concept/README.md) — outline concept document для outreach.
6. [`anthropic-vacancies/ai-managed-virtual-company/README.md`](anthropic-vacancies/ai-managed-virtual-company/README.md) — альтернатива «один человек / $500K» как AI-управляемая команда фрилансеров (Variant C).
7. [`anthropic-vacancies/mmorpg-for-programmers/README.md`](anthropic-vacancies/mmorpg-for-programmers/README.md) — гипотеза gamified work для технарей.
8. [`anthropic-vacancies/hermes-comparison/README.md`](anthropic-vacancies/hermes-comparison/README.md) — сравнение с Hermes Agent (Nous Research) и переоценка приоритетов.

## 7. «Я ищу конкретный компонент по имени»

→ [`glossary/components-by-name.md`](glossary/components-by-name.md) — алфавитный список с обратными ссылками.

→ [`glossary/authors-by-name.md`](glossary/authors-by-name.md) — список авторов.

→ [`glossary/concepts.md`](glossary/concepts.md) — ключевые понятия (CardIndex, Hot/Slow path, STDP, Sequential vs Coordinator, etc.).

## 8. «Я хочу понять архитектуру вашего DHLab серии»

Читайте в этом порядке:

1. [`nautilus/okwf-concept/README.md`](nautilus/okwf-concept/README.md) — фундаментальный концепт.
2. [`nautilus/representative-agent-layer-en/README.md`](nautilus/representative-agent-layer-en/README.md) — Cinderella Syndrome, общая идея.
3. [`nautilus/professional-colleague-agents-en/README.md`](nautilus/professional-colleague-agents-en/README.md) — типология агентов.
4. [`nautilus/composite-skills-agents/README.md`](nautilus/composite-skills-agents/README.md) — ансамбли агентов.
5. [`nautilus/double-triangle-architecture/README.md`](nautilus/double-triangle-architecture/README.md) — топология.
6. [`nautilus/infrastructure-layer-b-en/README.md`](nautilus/infrastructure-layer-b-en/README.md) — missing middle Layer B.
7. [`nautilus/npp-v1-1/README.md`](nautilus/npp-v1-1/README.md) — формальная спецификация.
8. [`nautilus/review-methodology/README.md`](nautilus/review-methodology/README.md) — методология review.
9. [`nautilus/ingit-cowork-en/README.md`](nautilus/ingit-cowork-en/README.md) — практическая интеграция.

## Полный листинг

См. [`README.md`](README.md) этой папки для алфавитного списка всех тем.

<!-- see-also -->

---

**Смотрите также:**
- [PRIORITIES](docs/PRIORITIES.md)
- [SEARCH](docs/SEARCH.md)
- [SITEMAP](docs/SITEMAP.md)
- [READING_ORDER](docs/READING_ORDER.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [PRIORITIES](docs/PRIORITIES.md) (сходство 0.17)
- [PRIORITIES](docs/obsidian/PRIORITIES.md) (сходство 0.17)
- [SEE_ALSO](docs/obsidian/SEE_ALSO.md) (сходство 0.16)

