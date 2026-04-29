# PDA-бот — «LLM как периферия»

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

---
<!-- tags: orchestration, architecture, collaboration -->




> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

AI-бот для самопознания
https://habr.com/ru/articles/1027210/
Автор строит систему, где LLM не ядро, а узел. Архитектура — Possibility-Driven Architecture (PDA): каждый ответ пользователя — неизменяемое событие (event sourcing), профиль — read model поверх event log, есть Stability Engine, Dialog Engine, Aeon Engine. Stability Engine отвечает за класс решений, которые LLM принимать не должен никогда. Это та же интуиция, что у Чуяна («гибрид LLM + детерминированный код, потому что LLM творец, а алгоритмами жёстко приводим в рамки»), но доведённая до предела: код целиком отвечает за стабильность, LLM — только генератор гипотез. Серия из четырёх статей у автора, видно, что это его главный проект.

Параллель к MoME-роутингу

Долой иерархию и роли — диссертация Виктории Дочкиной (Сбер, МФТИ)
https://habr.com/ru/articles/1017200/
Эксперимент: 8–16 LLM-агентов решают задачи по четырём протоколам коммуникации. Sequential-протокол (распределённая сеть, агенты видят только реальные завершённые результаты предшественников) выигрывает у Coordinator (центральный хаб) на 44% (Cohen's d = 1.86). Дочкина пишет диссертацию по автономным AI-системам, активно публикует. Это твой человек по теме «распределённое лучше центрального» — тот же тезис, что у тебя в Q6/MoME.

Источник данных и инфраструктурные кусочки

<!-- see-also -->

---

**Смотрите также:**
- [8-self-aware-mcp-specs](docs/habr-unique-projects/deep-pairs/8-self-aware-mcp-specs.md)
- [02-memnet](docs/habr-unique-projects/key-findings/02-memnet.md)
- [3-zinc-hybrid-arch](docs/habr-unique-projects/hardware-pairs/3-zinc-hybrid-arch.md)
- [05-supplementary-infrastructure](docs/habr-unique-projects/key-findings/05-supplementary-infrastructure.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [8-self-aware-mcp-specs](docs/habr-unique-projects/deep-pairs/8-self-aware-mcp-specs.md) (сходство 0.21)
- [02-memnet](docs/habr-unique-projects/key-findings/02-memnet.md) (сходство 0.17)
- [05-supplementary-infrastructure](docs/habr-unique-projects/key-findings/05-supplementary-infrastructure.md) (сходство 0.15)

