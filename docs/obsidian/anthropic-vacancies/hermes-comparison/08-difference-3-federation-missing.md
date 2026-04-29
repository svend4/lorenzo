---
title: "Различие 3: Federated knowledge architecture отсутствует"
tags:
  - architecture
  - anthropic
  - anthropic-vacancies
date: 2026-04-29
---

# Различие 3: Federated knowledge architecture отсутствует

> [!TIP]
> Документ содержит практические рекомендации и лучшие практики.

<!-- alert-added -->

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Resear

---
<!-- tags: architecture, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Research.

Различие 3: Federated knowledge architecture отсутствует

Hermes — single-agent system per installation. Каждый пользователь имеет свой Hermes instance. Между instances нет federation.

Nautilus Portal Protocol specifically addresses federated queries across multiple repositories. Это совершенно другой architectural concern.

То есть для personal use Hermes сам по себе достаточен. Для federated knowledge work (multiple practitioners sharing patterns, OKWF guild structure), нужен Nautilus-like layer поверх Hermes.

<!-- see-also -->

---

**Смотрите также:**
- [[06-difference-1-structured-substrate-missing]]
- [[09-difference-4-institutional-vision]]
- [[03-similarity-3-mcp-support]]
- [[02-similarity-2-persistent-memory]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[09-difference-4-institutional-vision]] (сходство 0.33)
- [[02-similarity-2-persistent-memory]] (сходство 0.32)
- [[03-similarity-3-mcp-support]] (сходство 0.32)

