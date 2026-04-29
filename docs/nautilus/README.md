# nautilus/ — Nautilus Portal Protocol и связанные working papers

Часть исходного MHTML‑снимка `Вакансии в Anthropic по кластерам - Claude` посвящена не вакансиям, а собственным архитектурным работам пользователя — формальной спецификации **Nautilus Portal Protocol** и нескольким companion papers. Содержимое разбито здесь на тематические подпапки.

## Подпапки

| Подпапка | Что содержит |
|---|---|
| [`npp-v1-1/`](npp-v1-1/) | Nautilus Portal Protocol v1.1 RFC — полная формальная спецификация, 23 раздела |
| [`okwf-concept/`](okwf-concept/) | Open Knowledge Work Foundation — Concept Document (11 разделов): шестислойная инфраструктура, target populations, governance, phased rollout |
| [`representative-agent-layer-en/`](representative-agent-layer-en/) | Representative Agent Layer (EN) — Cinderella Syndrome, исторические прецеденты, архитектурная спецификация (13 разделов) |
| [`representative-agent-layer-ru/`](representative-agent-layer-ru/) | Слой Представительских Агентов (RU, 13 разделов) |
| [`professional-colleague-agents-en/`](professional-colleague-agents-en/) | Professional Colleague Agents — типология AI-агентов на стороне принципала (13 разделов, EN) |
| [`professional-colleague-agents-ru/`](professional-colleague-agents-ru/) | Тот же документ на русском (13 разделов) |
| [`composite-skills-agents/`](composite-skills-agents/) | Composite Skills Agents — Twenty-One Teachers Pattern, sub-agent registry, ensembles (13 разделов) |
| [`double-triangle-architecture/`](double-triangle-architecture/) | Double-Triangle Architecture for Human-AI Collaboration — звезда Давида (12 разделов) |
| [`infrastructure-layer-b-en/`](infrastructure-layer-b-en/) | Infrastructure for AI-Collaborative Intellectual Work (EN) — «missing middle Layer B» между Chat и Code (14 разделов) |
| [`infrastructure-layer-b-ru/`](infrastructure-layer-b-ru/) | Инфраструктура для AI-совместной интеллектуальной работы (RU, 13 разделов) |
| [`ingit-cowork-en/`](ingit-cowork-en/) | InGit + Cowork — Symbiotic Architecture (10 разделов, EN) |
| [`ingit-cowork-ru/`](ingit-cowork-ru/) | Тот же документ на русском (10 разделов) |

## Как читать

1. **Начните с [`okwf-concept/`](okwf-concept/)** — это foundational concept document, фон для всех остальных.
2. **Затем [`npp-v1-1/`](npp-v1-1/)** — формальный протокол, на который ссылаются остальные.
3. **[`representative-agent-layer-en/`](representative-agent-layer-en/)** (или RU) — Cinderella Syndrome и общая идея агентов на стороне принципала.
4. **[`professional-colleague-agents-en/`](professional-colleague-agents-en/)** (или RU) — типология агентов и кейс «Обучай».
5. **Composite Skills Agents** — следующий шаг от одного агента к ансамблю агентов.
6. **[`double-triangle-architecture/`](double-triangle-architecture/)** — топология взаимодействия людей и AI.
7. **[`infrastructure-layer-b-en/`](infrastructure-layer-b-en/)** (или RU) — «missing middle Layer B».
8. **InGit + Cowork** — практическая интеграция с продуктом Anthropic Cowork.

## Ключевой принцип Nautilus

> **Федерация, а не слияние.** Native-форматы репозиториев сохраняются; унификация происходит только в момент обращения, через адаптер.

См. [`npp-v1-1/19-adr-001-federation-over-merging.md`](npp-v1-1/19-adr-001-federation-over-merging.md) для архитектурного обоснования.

## Связь с остальным монорепозиторием

- **Q6-гиперкуб / MoME** упоминается во многих местах: [`../glossary/concepts.md`](../glossary/concepts.md), [`../habr-unique-projects/hardware-pairs/2-tsu-mome.md`](../habr-unique-projects/hardware-pairs/2-tsu-mome.md), [`../habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md`](../habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md).
- **Architecture Spec** и **Card Envelope** в Svyazi 2.0 связаны с PortalEntry/Card паттернами здесь: [`../svyazi-2-0/architecture/`](../svyazi-2-0/architecture/).
- **Профиль svend4** (автор) — см. [`../anthropic-vacancies/profile-mapping/`](../anthropic-vacancies/profile-mapping/).
