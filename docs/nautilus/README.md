# nautilus/ — Nautilus Portal Protocol и связанные working papers

Часть исходного MHTML‑снимка `Вакансии в Anthropic по кластерам - Claude` посвящена не вакансиям, а собственным архитектурным работам пользователя — формальной спецификации **Nautilus Portal Protocol** и нескольким companion papers. Содержимое разбито здесь на тематические подпапки.

## Подпапки

| Подпапка | Что содержит |
|---|---|
| [`npp-v1-1/`](npp-v1-1/) | Nautilus Portal Protocol v1.1 RFC — полная формальная спецификация, 23 раздела (Abstract, Introduction, Terminology, Registry, Passport, Compatibility Levels, Adapter Interface, PortalEntry, Q6 Space, Consensus Algorithm, Query Flow, Relevance Ranking, Onboarding Paths, REST API, SDK, Security, MCP Extension, Versioning, Reference Implementation, ADRs, Glossary) |
| [`professional-colleague-agents-en/`](professional-colleague-agents-en/) | Working paper «Professional Colleague Agents» — типология AI-агентов на стороне принципала (12 разделов, EN) |
| [`professional-colleague-agents-ru/`](professional-colleague-agents-ru/) | Тот же документ на русском (12 разделов) |
| [`composite-skills-agents/`](composite-skills-agents/) | Working paper «Composite Skills Agents» — Twenty-One Teachers Pattern, sub-agent registry, ensembles (13 разделов) |
| [`ingit-cowork-en/`](ingit-cowork-en/) | Working paper «InGit + Cowork — Symbiotic Architecture» (10 разделов, EN) |
| [`ingit-cowork-ru/`](ingit-cowork-ru/) | Тот же документ на русском (10 разделов) |

## Как читать

1. **Начните с [`npp-v1-1/`](npp-v1-1/)** — это формальный протокол, на который ссылаются остальные документы.
2. **Затем [`professional-colleague-agents-en/`](professional-colleague-agents-en/)** (или RU) — типология агентов и кейс «Обучай».
3. **Composite Skills Agents** — следующий шаг от одного агента к ансамблю агентов.
4. **InGit + Cowork** — практическая интеграция с продуктом Anthropic Cowork.

## Ключевой принцип Nautilus

> **Федерация, а не слияние.** Native-форматы репозиториев сохраняются; унификация происходит только в момент обращения, через адаптер.

См. [`npp-v1-1/19-adr-001-federation-over-merging.md`](npp-v1-1/19-adr-001-federation-over-merging.md) для архитектурного обоснования.

## Связь с остальным монорепозиторием

- **Q6-гиперкуб / MoME** упоминается во многих местах: [`../glossary/concepts.md`](../glossary/concepts.md), [`../habr-unique-projects/hardware-pairs/2-tsu-mome.md`](../habr-unique-projects/hardware-pairs/2-tsu-mome.md), [`../habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md`](../habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md).
- **Architecture Spec** и **Card Envelope** в Svyazi 2.0 связаны с PortalEntry/Card паттернами здесь: [`../svyazi-2-0/architecture/`](../svyazi-2-0/architecture/).
- **Профиль svend4** (автор) — см. [`../anthropic-vacancies/profile-mapping/`](../anthropic-vacancies/profile-mapping/).
