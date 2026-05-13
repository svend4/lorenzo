# Пять быстрых связок (fast-tracks)

<!-- toc-auto -->

<!-- summary -->
> Пять приоритетных комбинаций OSS-проектов: Collaboration Knowledge OS, Forensic Legal RAG, Agent Team Kernel, Secure Agent Runtime, Habr Scout — и их «внуковая» суперкомбинация.

<!-- tags: collaboration, architecture, ai-teams, rag, security -->

> Источник: MHTML‑снимок `Поиск коллабораций AI проектов` (корень репозитория).

> [!TIP]
> Лучшая точка входа для понимания, как совмещать проекты с Хабра в единую систему.

1. Svyazi + AgentFS + knowledge-space + Memory OS = Collaboration Knowledge OS.

Это самый прямой наследник исходной статьи. Svyazi даёт людей/профили/поиск коллабораций, AgentFS даёт операционку для агентов, knowledge-space — карточную переработку ресёрча, Memory OS — provenance и многослойную память. Это может стать системой, где не случайно находятся два человека, а постоянно рождаются проектные пары, тройки и команды.

2. LiteParse/research-docs + Hybrid RAG + Legal RAG Challenge + Graph RAG = Forensic Legal RAG.

Это уже почти готовый путь к серьёзной юридической/документной системе: визуальные цитаты, page grounding, answer-type scoring, graph reasoning, подсветка источника. Для документов, судов, регуляторики и научных статей это намного сильнее обычного RAG.

3. Rufler + agent-pool + locks/handoffs + Skate + AI Factory = Agent Team Kernel.

Это превращает хаотичные Claude/Cursor-сессии в управляемую команду: план, зависимости, статусы, handoffs, память, эволюция скиллов, Telegram/PR-выход.

4. SENTINEL/Shield + Prompt Worms lessons + Claude permissions + MCP Tool Search = Secure Agent Runtime.

Без этого все красивые агентные системы опасны. С этим появляется шанс допустить агентов к документам, GitHub, почте, браузеру, календарю, базам и локальным файлам.

5. Firecrawl/Playwright + Svyazi extraction + knowledge-space = Habr Scout / Project Scout.

Это как раз продолжение твоего текущего поиска: агент сам регулярно обходит Хабр, вытаскивает одиночные проекты, авторов, технологии, открытые вопросы и предлагает новые «родительские пары» для будущих проектов.

Самая интересная «внуковая» комбинация из всего найденного:

Habr Scout → Svyazi-like карточки авторов/проектов → Collaboration Knowledge OS → Agent Team Kernel → Forensic RAG → Secure Agent Runtime

То есть система, которая сама ищет на Хабре одиночные проекты, превращает их в карточки, находит связки 2–5 проектов, предлагает новые уникальные комбинации, проверяет источники, создаёт backlog и запускает агентную команду на прототип. Это уже не просто подбор статей — это машина технологической селекции и сборки проектов.

Источники

Вы сказали:

Продолжение 

ChatGPT сказал:

Вы сказали:

<!-- see-also -->

---

## Использование

```bash
python scripts/improve_semantic_search.py --query "Пять быстрых связок fast tracks"
```

## Смотрите также
- [00-overview-grandchild-combination](../../lorenzo-agent/operationalized/00-overview-grandchild-combination.md)
- [3-forensic-rag](../ensembles/3-forensic-rag.md)
- [04-memory-firewall-vs-prompt-worms](../continuation/04-memory-firewall-vs-prompt-worms.md)
- [executive-summary](../../svyazi-2-0/overview/executive-summary.md)


<!-- backlinks -->

---

**Кто ссылается на этот документ (5):**
- [OUTLINE](../../OUTLINE.md)
- [READABILITY](../../READABILITY.md)
- [READING_TIME](../../READING_TIME.md)
- [SEARCH](../../SEARCH.md)
- [TABLES](../../TABLES.md)


<!-- similar-docs -->

---

**Похожие документы:**
- [README](../../obsidian/ai-collaborations/fast-tracks/README.md) (сходство 0.97)
- [00-overview-grandchild-combination](../../lorenzo-agent/operationalized/00-overview-grandchild-combination.md) (сходство 0.22)
- [00-overview-grandchild-combination](../../obsidian/lorenzo-agent/operationalized/00-overview-grandchild-combination.md) (сходство 0.21)

