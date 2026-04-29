---
title: "Profession-specific workflows"
tags:
  - roadmap
  - anthropic
  - collaboration
  - habr-unique-projects
date: 2026-04-29
---

# Profession-specific workflows

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — расширенные примеры с Хабра по варианту D (поиск ещё уникальных проектов).

---
<!-- tags: roadmap, anthropic, collaboration -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — расширенные примеры с Хабра по варианту D (поиск ещё уникальных проектов).

Что получается: Tool для конкретных profession-specific workflows:

Practitioner describes task в natural language

WorkTeam-style decomposition → конкретные steps

n8n-style automation execution

Свяжи-style structured data flow между steps

Obsidian-style knowledge accumulation

Применение: «Process this Bescheid → check Frist → cross-reference with similar past cases → draft Widerspruch с relevant arguments → schedule reminder for response deadline» — все automated через NL command.

Оценка для практической реализации

Из этих синтезов, какие наиболее реалистичны для implementation?

Самый реалистичный (не требует много новой разработки): Синтез B (Personal Knowledge Workspace).

Это потому что все компоненты уже existed and work:

Obsidian + plugins работают

Local LLM через Ollama работает

Свяжи's parsing patterns documented (даже если код закрыт)

Cowork integration possible сейчас

Time to MVP: 1-2 месяца part-time work.

Самый ambitious но ценный: Синтез D (Federated knowledge marketplace).

Это closest к нашей OKWF vision (Document 4). Но требует много working pieces.

Time to MVP: 12+ месяцев с small team.

Самый relevant к вашей текущей ситуации: Синтез A (Professional community matching).

Связи (Свяжи) demonstrated, что matching работает empirically (Wi-Fi инженер example). Apply pattern к SGB advocates community.

Time to MVP: 3-6 месяцев focused work.

<!-- see-also -->

---

**Смотрите также:**
- [[07-specialized-knowledge-workspace]]
- [[09-federated-platform]]
- [[08-personal-multi-agent-hub]]
- [[06-platform-for-professional-communities]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[07-specialized-knowledge-workspace]] (сходство 0.27)
- [[09-federated-platform]] (сходство 0.27)
- [[08-personal-multi-agent-hub]] (сходство 0.25)

