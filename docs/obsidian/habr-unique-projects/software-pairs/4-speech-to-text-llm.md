---
title: "Пара 4 — Speech-to-text локально × LLM с памятью"
tags:
  - habr-unique-projects
date: 2026-04-29
---

# Пара 4 — Speech-to-text локально × LLM с памятью

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).
**Проекты:** Yodoca, NGT Memory, MemNet, Whisper

---
<!-- tags: memory, local-first, collaboration -->




> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Пара 4. Speech-to-text локально × LLM с памятью

Родители: Whisper.cpp Георги Герганова (тот же автор llama.cpp, работает от десктопа до телефона), Handy и OpenWhispr (push-to-talk обёртки локально, habr.com/ru/articles/1024634/), GigaAM v3 (русская модель), WhisperX (диаризация), Whisper Notes (Mac/iOS). Параллельно — память Yodoca, NGT Memory, MemNet из прошлых ответов. Поодиночке: транскрипция — это просто текст, без структуры; память — без входного канала. Вместе появляется voice-first second brain.

Дети:

Voice-first second brain — Handy (push-to-talk, Pause-key) + Whisper.cpp + NGT Memory + Obsidian: зажал, надиктовал мысль о деле или о Nautilus, отпустил — текст разобран как у Чуяна (entities извлечены), сохранён в граф памяти, появились wikilinks. На ходу, без печати, без интернета. Для legal — захват пометок после заседания. Для AI/ML research — мгновенная фиксация идеи о Q6 при выходе из метро.

Court hearing analyser с диаризацией — Whisper + voice-эмбеддинги через wespeaker-voxceleb-resnet34-LM (https://habr.com/ru/companies/yoomoney/articles/1012870/) + кастомный MCP-сервер. Запись с заседания Sozialgericht автоматически делится на спикеров (судья / KSV-вертретер / клиент / ты), каждый блок передаётся в соответствующий skill. Полная запись + структурированный протокол + extracted facts — за один проход, без отправки наружу.

Discovery-loop через voice journal — каждый вечер пять минут устного рассказа о дне. Whisper транскрибирует → LLM извлекает события и сущности → Yodoca-консолидатор ночью кристаллизует факты → утром в Obsidian вышли wikilinks к новым связям. Это life-log + research-log в одном пайплайне, без необходимости печатать.

<!-- see-also -->

---

**Смотрите также:**
- [[5-voice-local-memory]]
- [[5-tinyml-mcp-skills]]
- [[3-discovery-research]]
- [[6-metaphor]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[5-voice-local-memory]] (сходство 0.42)
- [[3-discovery-research]] (сходство 0.20)
- [[5-tinyml-mcp-skills]] (сходство 0.18)

