---
title: "Пара 5 — TinyML/Edge AI × MCP + skills"
tags:
  - memory
  - orchestration
  - anthropic
  - collaboration
  - habr-unique-projects
date: 2026-04-29
---

# Пара 5 — TinyML/Edge AI × MCP + skills

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).
**Проекты:** Yodoca, NGT Memory

---
<!-- tags: memory, orchestration, anthropic, collaboration -->




> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Пара 5. TinyML/Edge AI × MCP-протокол + skills-система

Родители: edge-устройства уровня Jetson Orin / Raspberry Pi 5 / Coral с TinyChat от MIT HAN Lab (LLaMA-2 на 30 tok/s) и MCP/skills-стек (Anthropic Skills, Knowledge Graph Kit). Биология: на edge всё локально, приватно, без интернета. Физика: MCP даёт стандартный интерфейс, skills — переносимый рецепт.

Дети:

Pocket Yodoca — телефон или Pi с локальной малой моделью, NGT Memory (хеббовский граф) и MCP-сервером. Память владельца, которую он буквально носит в кармане и которая физически не покидает устройство. На каждый контакт можно поднять уже знакомый персональный граф.

Sensor-driven life log — Edge-устройство со связкой TinyML + tg-chat-analyser-style парсер активности, которое собирает паттерны (как Чуян хочет — «постоянно по мере поступления») и автоматически консолидирует их в персональный граф ночью. Discovery-файл живёт прямо на устройстве; пользователь по утрам разгребает только то, что система не смогла классифицировать.

Edge multi-agent mesh — рой Pi/Jetson-агентов, каждый — узкий эксперт (legal, technical, networking, медицинский). Общаются по MCP в Sequential-режиме Дочкиной. Это материализация твоего же multi-chat-orchestrator skill'а в железе: вместо параллельных чатов в одном Claude — параллельные малые агенты на физически разных устройствах.

<!-- see-also -->

---

**Смотрите также:**
- [[4-riscv-privacy]]
- [[4-speech-to-text-llm]]
- [[05-supplementary-infrastructure]]
- [[3-zinc-hybrid-arch]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[4-riscv-privacy]] (сходство 0.18)
- [[4-speech-to-text-llm]] (сходство 0.18)
- [[2-tsu-mome]] (сходство 0.17)

