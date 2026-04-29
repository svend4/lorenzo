---
title: "Пара 2 — Local-first PKM (Obsidian/Logseq) × MCP/Skills"
tags:
  - habr-unique-projects
date: 2026-04-29
---

# Пара 2 — Local-first PKM (Obsidian/Logseq) × MCP/Skills

<!-- summary -->
> > Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).
**Проекты:** Yodoca

---
<!-- tags: memory, knowledge, local-first, anthropic, collaboration -->




> Источник: MHTML‑снимок `Поиск уникальных проектов на Хабре для совместной разработки - Claude` (корень репозитория).

Пара 2. Local-first PKM (Obsidian/Logseq) × MCP/Skills

Родители: Obsidian с 1000+ плагинами и graph view, Logseq (open-source, block-first), Foam (просто markdown в VS Code) — отличные хранилища, но без LLM это статичный архив. MCP + Anthropic Skills даёт активного агента поверх vault'а. Появилось ключевое: плагин LLM Wiki для Obsidian (https://forum.obsidian.md/t/new-plugin-llm-wiki-turn-your-vault-into-a-queryable-knowledge-base-privately/113223), реализующий Karpathy-паттерн локально на Ollama. И second-brain skill-pack Николаса Списака (github.com/NicholasSpisak/second-brain) — четыре skill'а, которые учат Claude/Codex/Gemini-CLI работать с Obsidian нативно.

Дети:

Obsidian-as-MCP-database — vault превращается в MCP-сервер, любой агент видит твою юридическую базу как структурированный источник правды. Для тебя это значит: один vault с делами, прецедентами, шаблонами — все 87 skills и все Claude-инстансы (Code, Chrome, Cowork) ходят туда через стандартный протокол. Privacy by design — данные физически не покидают машину.

InfraNodus-style structural gap finder (infranodus.com/use-case/visualize-knowledge-graphs-pkm) — анализ графа vault'а ищет структурные пробелы: тематически близкие заметки, между которыми нет связи. Это discovery-механизм Чуяна, применённый не к людям, а к юридическим делам и прецедентам. Может найти неожиданную релевантность между делом по § 78 Abs. 6 SGB IX и закрытым делом BSG двухлетней давности.

Local LLM Wiki поверх раздельной личной/агентной зоны — раздел raw/ (clipped material из браузера, голосовые транскрипты, сканы) + wiki/ (consolidated). Соавтор Obsidian Steph Ango рекомендует именно эту изоляцию: LLM работает в wiki/, ты живёшь в personal/, переход между ними — твой контролируемый ритуал. На уровне идеи — то же, что Yodoca с консолидацией, но реализовано через файлы и git вместо SQLite.

<!-- see-also -->

---

**Смотрите также:**
- [[07-crawl4ai-docling-yodoca-consolidator]]
- [[02-related-projects]]
- [[4-speech-to-text-llm]]
- [[2-document-rag]]


<!-- similar-docs -->

---

**Похожие документы:**
- [[2-document-rag]] (сходство 0.17)
- [[5-voice-local-memory]] (сходство 0.17)
- [[07-crawl4ai-docling-yodoca-consolidator]] (сходство 0.17)

