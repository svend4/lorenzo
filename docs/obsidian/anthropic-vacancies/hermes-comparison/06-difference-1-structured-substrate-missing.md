---
title: "Различие 1: Структурированная подложка отсутствует"
tags:
  - architecture
  - anthropic
  - anthropic-vacancies
date: 2026-04-29
---

# Различие 1: Структурированная подложка отсутствует

<!-- summary -->
> > Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Resear

---
<!-- tags: architecture, anthropic -->




> Источник: MHTML‑снимок `Вакансии в Anthropic по кластерам - Claude` (корень репозитория). Раздел диалога — сравнение собственной архитектуры (InGit + Cowork + Nautilus) с Hermes Agent от Nous Research.

Различие 1: Структурированная подложка отсутствует

Hermes не imposes структуру на ваши файлы и проекты. Каждый пользователь хранит данные как ему удобно. Hermes adapts to whatever структура есть.

InGit specifically provides структуру (00_inbox через 90_exports, YAML metadata schemas). Это:

Делает кросс-проектное сравнение возможным

Стандартизирует team collaboration (когда станет доступным)

Обеспечивает predictable patterns для Hermes (или Cowork) к работе с

Делает migration между systems easier

То есть InGit + Hermes могло бы быть лучшей комбинацией, чем Hermes alone. Hermes как агентский слой, InGit как структурный слой. Точно так же, как InGit + Cowork.

<!-- see-also -->

---

**Смотрите также:**
- [[08-difference-3-federation-missing]]
- [[03-similarity-3-mcp-support]]
- [[05-similarity-5-self-hosting-privacy]]
- [[04-similarity-4-multi-platform]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[03-similarity-3-mcp-support]] (сходство 0.33)
- [[04-similarity-4-multi-platform]] (сходство 0.32)
- [[08-difference-3-federation-missing]] (сходство 0.31)

