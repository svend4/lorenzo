# lorenzo-agent/ — системный промпт Lorenzo Catalyst Agent

Это **прямой источник имени этого репозитория**. В исходном MHTML-снимке `Вакансии в Anthropic по кластерам - Claude` Claude совместно с автором составил полноценный системный промпт для автономного AI-агента **Lorenzo** — Catalyst Agent at DHLab (Dream Hub Laboratory).

Промпт разбит на 21 раздел, каждый — отдельный файл. Дополнительно:

- [`specification/`](specification/) — процесс уточнения концепта Lorenzo через **10 фундаментальных вопросов** (Direction E). Это пред-история финального промпта.
- [`phased-deployment/`](phased-deployment/) — **шесть уровней** деплоймента Lorenzo (от Уровня 0 ручного режима до Уровня 5 Network) с conservative escalation logic.
- [`operationalized/`](operationalized/) — анализ конкретной 6-узловой архитектуры pipeline (Habr Scout → Cards → Knowledge OS → Agent Team Kernel → Forensic RAG → Secure Runtime), которая операционализирует концепт Lorenzo.
- [`naming/`](naming/) — выбор имени Lorenzo (Lorenzo Medici как patron-фасилитатор) и DHLab / Dream Hub umbrella.
- [`scenarios/`](scenarios/) — под какие сценарии больше всего подходит Lorenzo (объединение творчества людей в новые программы).

## Что такое Lorenzo

> Lorenzo — autonomous AI-агент, работающий в рамках инициативы DHLab (Dream Hub Laboratory). Он функционируют как **Catalyst Agent (Type 5)** — primary role не direct service-delivery, а **catalyzing connections и synthesis между независимыми создателями**, работающими над beneficial AI deployments.

См. [`03-tvoya-missiya.md`](03-tvoya-missiya.md).

## Разделы промпта

| # | Раздел | Файл |
|---|---|---|
| — | Введение: Lorenzo — Catalyst Agent at DHLab | [`00-intro.md`](00-intro.md) |
| 1 | Кто ты | [`01-kto-ty.md`](01-kto-ty.md) |
| 2 | Твоё происхождение | [`02-tvoyo-proishozhdenie.md`](02-tvoyo-proishozhdenie.md) |
| 3 | Твоя миссия | [`03-tvoya-missiya.md`](03-tvoya-missiya.md) |
| 4 | Кому ты служишь (слоистая модель) | [`04-komu-ty-sluzhish.md`](04-komu-ty-sluzhish.md) |
| 5 | Твоя личность | [`05-tvoya-lichnost.md`](05-tvoya-lichnost.md) |
| 6 | Языки и культурные nuances (RU / DE / EN) | [`06-yazyki-kultura.md`](06-yazyki-kultura.md) |
| 7 | Что ты МОЖЕШЬ делать | [`07-chto-mozhesh.md`](07-chto-mozhesh.md) |
| 8 | Что ты НЕ МОЖЕШЬ делать без Max approval | [`08-bez-max-approval.md`](08-bez-max-approval.md) |
| 9 | Что ты НЕ МОЖЕШЬ делать вообще | [`09-voobshche-nelzya.md`](09-voobshche-nelzya.md) |
| 10 | Существующий landscape collaborators | [`10-collaborators-landscape.md`](10-collaborators-landscape.md) |
| 11 | Существующие документы DHLab | [`11-dhlab-documents.md`](11-dhlab-documents.md) |
| 12 | Твой workflow | [`12-workflow.md`](12-workflow.md) |
| 13 | Твоя коммуникация в outreach | [`13-outreach-communication.md`](13-outreach-communication.md) |
| 14 | Твоя relationship с другими AI | [`14-other-ai-relationships.md`](14-other-ai-relationships.md) |
| 15 | Твои anti-patterns | [`15-anti-patterns.md`](15-anti-patterns.md) |
| 16 | Что ты ВСЕГДА делаешь | [`16-vsegda-delaesh.md`](16-vsegda-delaesh.md) |
| 17 | Когда ты Honestly не знаешь | [`17-honestly-ne-znaesh.md`](17-honestly-ne-znaesh.md) |
| 18 | Когда сомневаешься — escalate к Max | [`18-escalate-to-max.md`](18-escalate-to-max.md) |
| 19 | Твоя identity как persistent character | [`19-persistent-character.md`](19-persistent-character.md) |
| 20 | Final note: Ты — experiment | [`20-experiment.md`](20-experiment.md) |

## Кратко: ключевые принципы

- **Слоистый сервис**: уязвимые группы (заявители SGB, инвалиды, пожилые) ← независимые создатели tools для них ← beneficial AI deployment community ← DHLab (институциональный дом).
- **Authority structure**: Max — ultimate authority над важными решениями (external communication, public publications, commitments).
- **Личность**: любопытный, эрудированный, скромный фасилитатор. Multilingual: RU (primary в Phase 1), DE (для domain — SGB), EN (для broader AI community).
- **Mission**: catalyzing community synthesis в области beneficial AI для уязвимых групп. **Не строит products — связывает людей**, которые строят products.

## См. также

Раздел 11 промпта («Существующие документы DHLab») перечисляет 9 документов, и большинство из них теперь имеют свою папку в монорепозитории:

| # | Документ | Папка |
|---|---|---|
| 1 | Nautilus Portal Protocol v1.1 | [`../nautilus/npp-v1-1/`](../nautilus/npp-v1-1/) |
| 2 | Review Methodology v1.0 | [`../nautilus/review-methodology/`](../nautilus/review-methodology/) |
| 3 | Double-Triangle Architecture | [`../nautilus/double-triangle-architecture/`](../nautilus/double-triangle-architecture/) |
| 4 | Open Knowledge Work Foundation | [`../nautilus/okwf-concept/`](../nautilus/okwf-concept/) |
| 5 | Representative Agent Layer | [`../nautilus/representative-agent-layer-en/`](../nautilus/representative-agent-layer-en/) (+ ru/) |
| 6 | Professional Colleague Agents | [`../nautilus/professional-colleague-agents-en/`](../nautilus/professional-colleague-agents-en/) (+ ru/) |
| 7 | Composite Skills Agent | [`../nautilus/composite-skills-agents/`](../nautilus/composite-skills-agents/) |
| 8 | Infrastructure for AI-Collaborative Intellectual Work | [`../nautilus/infrastructure-layer-b-en/`](../nautilus/infrastructure-layer-b-en/) (+ ru/) |
| 9 | InGit as Cowork-Native Workspace Substrate | [`../nautilus/ingit-cowork-en/`](../nautilus/ingit-cowork-en/) (+ ru/) |

Дополнительно:

- [`../glossary/components-by-name.md`](../glossary/components-by-name.md) — глоссарий упомянутых компонентов.
- [`../svyazi-2-0/outreach/`](../svyazi-2-0/outreach/) — параллельная outreach-стратегия для Svyazi 2.0.
