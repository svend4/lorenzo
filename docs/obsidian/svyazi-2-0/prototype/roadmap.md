---
title: "Дорожная карта прототипа"
tags:
  - svyazi-2-0
date: 2026-04-29
---

# Дорожная карта прототипа

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> > Источник: `deep-research-report (3).md`, раздел «Дорожная карта прототипа следующей итерации».
**Проекты:** Svyazi, mclaude, AI Factory, Yodoca, NGT Memory

---

<!-- toc -->
## Содержание

- [Итерация 1 — Evidence-first card graph](#итерация-1-evidence-first-card-graph)
- [Итерация 2 — Memory governance](#итерация-2-memory-governance)
- [Итерация 3 — Orchestration + federation](#итерация-3-orchestration-federation)
- [Сводная таблица](#сводная-таблица)
- [Главный инженерный вывод](#главный-инженерный-вывод)

---

<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, self-improvement -->




> Источник: `deep-research-report (3).md`, раздел «Дорожная карта прототипа следующей итерации».

Если идти дальше после базового MVP, то лучшая стратегия — не «добавить всё», а пройти **три короткие итерации**, каждая из которых поднимает один новый класс свойств. Первая итерация должна закрепить контракт и доказуемость. Вторая — добавить controlled memory и human review. Третья — подключить orchestration и local‑first ingestion. Такой порядок лучше соответствует зрелости уже найденных компонентов и снижает риск, что вы сначала построите красивую агентную фабрику, а потом обнаружите, что утверждения в ней невозможно надёжно проверить. citeturn20view5turn20view6turn21view0turn22view4turn20view2turn20view3

## Итерация 1 — Evidence-first card graph

В первой итерации разумно сосредоточиться на привести Card Envelope к одному формату, внедрить Evidence Envelope и сделать два типа карточек — `person` и `project`, плюс `episode` как сырой контейнер. В этой фазе память можно держать даже в упрощённом режиме, но без явного evidence‑слоя дальше лучше не идти. Эта фаза даёт уже очень ценный эффект: объяснимые suggestions вместо «магического мэтчинга». citeturn41search0turn20view5turn34view2turn20view6

## Итерация 2 — Memory governance

Включить **двухуровневую память и review queue**. На практике это означает: episode store, proposal queue, approved facts, plus decay/archival path. Тут нужно решить прежде всего не «какая память умнее», а «какая licence/policy лучше подходит». Если нужен максимально permissive и понятный старт, Yodoca‑style паттерн и typed memory выглядят безопаснее; если важнее предельно быстрый ассоциативный matching, NGT Memory выглядит сильнее, но его BSL‑режим уже требует аккуратной проверки коммерческих планов. Это не недостаток одного проекта, а просто лицензионная развилка, которую лучше признать заранее. citeturn21view0turn22view5turn20view16

## Итерация 3 — Orchestration + federation

Включать orchestration: mclaude или AI Factory на moderation/build side, plus local‑first voice intake и CRDT sync для мультидевайсности. Именно здесь Svyazi‑2.0 перестаёт быть одиночным инструментом исследователя и становится системой для маленькой команды или сообщества. Но делать это раньше, чем специфицированы card/evidence/memory policies, невыгодно: рой агентов лишь ускорит накопление неструктурированного долга. citeturn20view2turn20view3turn21view10turn11search11

## Сводная таблица

| Итерация | Главная цель | Минимум, который должен заработать | Оценка усилий | Главный риск |
|---|---|---|---|---|
| Evidence-first core | Из любого suggestions можно перейти к основанию | Unified cards + page/span evidence + manual reviewer UI | 1–2 недели | Переусложнение схемы слишком рано |
| Memory governance | Ассоциации перестают путаться с фактами | Episode store + proposal queue + approval/decay states | 1–2 недели | Ложная уверенность в «умной памяти» без жёсткого review |
| Agented moderation | Рой помогает, а не создаёт шум | extractor/reviewer/publisher roles + handoff/journal | 1–2 недели | Многоагентный хаос без хороших критериев качества |
| Local-first ingestion | Система начинает жить в ежедневном потоке | voice→episode, local vault, selective sync | 1–2 недели | Sync-конфликты и таскание лишних данных наружу |
| Self-improvement loop | Ошибки превращаются в benchmark и patch | benchmark set + nightly eval + rollback policy | 1 неделя на каркас, дальше непрерывно | Большой соблазн автоматизировать раньше, чем появилась метрика |

## Главный инженерный вывод

Самая большая инженерная работа здесь — **не реализация низкоуровневых библиотек, а проектирование статусов, границ и ручных переходов**. Это хорошая новость: такую архитектуру можно собрать без огромной команды, если с самого начала дисциплинировать стыки. citeturn41search0turn27view0turn21view0turn20view5turn20view2turn39view1

<!-- see-also -->

---

**Смотрите также:**
- [[12-roadmap]]
- [[12-дорожная-карта-прототипа-следующей-итерации]]
- [[05-roadmap-6-12-months]]
- [[conclusions]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[12-roadmap]] (сходство 0.80)
- [[12-дорожная-карта-прототипа-следующей-итерации]] (сходство 0.79)
- [[12-roadmap]] (сходство 0.77)

