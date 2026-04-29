# Противоречия в базе знаний

<!-- summary -->
> Утверждений: **32363** | Противоречий: **2966**
**Проекты:** Svyazi, knowledge-space, mclaude, AI Factory, Rufler, MemNet, LiteLLM, Auto AI Router

---

<!-- toc -->
## Содержание

- [Найденные противоречия](#найденные-противоречия)
  - [1. 🔢 Числовое — 9.0 vs 4.0 (уверенность: 0.8)](#1-числовое-90-vs-40-уверенность-08)
  - [2. 🔢 Числовое — 20.0 vs 8.0 (уверенность: 0.8)](#2-числовое-200-vs-80-уверенность-08)
  - [3. 🔢 Числовое — 4.0 vs 9.0 (уверенность: 0.8)](#3-числовое-40-vs-90-уверенность-08)
  - [4. 🔢 Числовое — 1027724.0 vs 4.0 (уверенность: 0.8)](#4-числовое-10277240-vs-40-уверенность-08)
  - [5. 🔢 Числовое — 1017200.0 vs 44.0 (уверенность: 0.8)](#5-числовое-10172000-vs-440-уверенность-08)
  - [6. 🔢 Числовое — 8.0 vs 44.0 (уверенность: 0.8)](#6-числовое-80-vs-440-уверенность-08)
  - [7. 🔢 Числовое — 6.0 vs 366.0 (уверенность: 0.8)](#7-числовое-60-vs-3660-уверенность-08)
  - [8. 🔢 Числовое — 70.0 vs 4.0 (уверенность: 0.8)](#8-числовое-700-vs-40-уверенность-08)
  - [9. 🔢 Числовое — 7.0 vs 50.0 (уверенность: 0.8)](#9-числовое-70-vs-500-уверенность-08)
  - [10. 🔢 Числовое — 68.0 vs 8.0 (уверенность: 0.8)](#10-числовое-680-vs-80-уверенность-08)
  - [11. 🔢 Числовое — 68.0 vs 4.0 (уверенность: 0.8)](#11-числовое-680-vs-40-уверенность-08)
  - [12. 🔢 Числовое — 8.0 vs 4.0 (уверенность: 0.8)](#12-числовое-80-vs-40-уверенность-08)
  - [13. 🔢 Числовое — 8.0 vs 4.0 (уверенность: 0.8)](#13-числовое-80-vs-40-уверенность-08)
  - [14. 🔢 Числовое — 3.0 vs 330.0 (уверенность: 0.8)](#14-числовое-30-vs-3300-уверенность-08)
  - [15. 🔢 Числовое — 8.0 vs 41.0 (уверенность: 0.8)](#15-числовое-80-vs-410-уверенность-08)
  - [16. 🔢 Числовое — 8.0 vs 41.0 (уверенность: 0.8)](#16-числовое-80-vs-410-уверенность-08)
  - [17. 🔢 Числовое — 22.0 vs 11.0 (уверенность: 0.8)](#17-числовое-220-vs-110-уверенность-08)
  - [18. 🔢 Числовое — 22.0 vs 785.0 (уверенность: 0.8)](#18-числовое-220-vs-7850-уверенность-08)
  - [19. 🔢 Числовое — 22.0 vs 11.0 (уверенность: 0.8)](#19-числовое-220-vs-110-уверенность-08)
  - [20. 🔢 Числовое — 11.0 vs 785.0 (уверенность: 0.8)](#20-числовое-110-vs-7850-уверенность-08)
  - [21. 🔢 Числовое — 11.0 vs 16.0 (уверенность: 0.8)](#21-числовое-110-vs-160-уверенность-08)
  - [22. 🔢 Числовое — 5.0 vs 30.0 (уверенность: 0.8)](#22-числовое-50-vs-300-уверенность-08)
  - [23. 🔢 Числовое — 785.0 vs 16.0 (уверенность: 0.8)](#23-числовое-7850-vs-160-уверенность-08)
  - [24. 🔢 Числовое — 785.0 vs 11.0 (уверенность: 0.8)](#24-числовое-7850-vs-110-уверенность-08)
  - [25. 🔢 Числовое — 16.0 vs 11.0 (уверенность: 0.8)](#25-числовое-160-vs-110-уверенность-08)
  - [26. 🔢 Числовое — 15.0 vs 355.0 (уверенность: 0.8)](#26-числовое-150-vs-3550-уверенность-08)
  - [27. 🔢 Числовое — 80.0 vs 8.0 (уверенность: 0.8)](#27-числовое-800-vs-80-уверенность-08)
  - [28. 🔢 Числовое — 30.0 vs 739.0 (уверенность: 0.8)](#28-числовое-300-vs-7390-уверенность-08)
  - [29. 🔢 Числовое — 5.0 vs 36.0 (уверенность: 0.8)](#29-числовое-50-vs-360-уверенность-08)
  - [30. 🔢 Числовое — 785.0 vs 26.0 (уверенность: 0.8)](#30-числовое-7850-vs-260-уверенность-08)

---

<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, architecture, roadmap, anthropic, self-improvement, collaboration -->




_Обновлено: 2026-04-29_

Утверждений: **32363** | Противоречий: **2966**

> Автоматический поиск без LLM — возможны ложные срабатывания.

## Найденные противоречия

### 1. 🔢 Числовое — 9.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `first`, `software`, `можно`, `собирать`

**A:** `docs/01-svyazi/README.md`
> 0 уже можно собирать из существующих software‑first кирпичей, не придумывая пол… - 09-architectural-gaps

**B:** `docs/SIMILAR_PASSAGES.md`
> 0 уже можно собирать из существующих software‑first кирпичей , не придумывая половину архитек ✅ Результат: Самый д B: docs/04-ai-collaborations/07-выв

---

### 2. 🔢 Числовое — 20.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `ещё`, `запрос`, `можно`, `нормально`

**A:** `docs/02-anthropic-vacancies/272-appendix-d-connection-diagram.md`
> Запрос Да это нормально хорошо сделано ну можно ещё поговорить пообсуждать про технические инфраструктурные вопросы например это большая сессия много 

**B:** `docs/QUESTIONS.md`
> md (8) - Запрос Да это нормально хорошо сделано ну можно ещё поговорить пообсуждать про технические инфраструктурные вопросы например это большая сесс

---

### 3. 🔢 Числовое — 4.0 vs 9.0 (уверенность: 0.8)

**Общие ключевые слова:** `first`, `software`, `можно`, `собирать`

**A:** `docs/SIMILAR_PASSAGES.md`
> 0 уже можно собирать из существующих software‑first кирпичей , не придумывая половину архитек ✅ Результат: Самый д B: docs/04-ai-collaborations/07-выв

**B:** `docs/SUMMARIES.md`
> 0 уже можно собирать из существующих software‑first кирпичей , не придумывая пол… - 09-architectural-gaps

---

### 4. 🔢 Числовое — 1027724.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `articles`, `com`, `было`, `конце`

**A:** `docs/04-ai-collaborations/00-intro.md`
> com/ru/articles/1027724/ в конце статьи было написано как с помощью этой программы и ИИ нашлись два человека которые вместе организовали потом проект 

**B:** `docs/NARRATIVE.md`
> com/ru/articles/1027724/ в конце статьи было написано как с помощью этой программы и ИИ нашлись два человека которые вместе организовали потом проект 

---

### 5. 🔢 Числовое — 1017200.0 vs 44.0 (уверенность: 0.8)

**Общие ключевые слова:** `articles`, `com`, `sequential`, `координатора`

**A:** `docs/04-ai-collaborations/00-intro.md`
> com/ru/articles/1017200/) — Sequential протокол лучше координатора на 44%

**B:** `docs/05-habr-projects/memory/memnet.md`
> com/ru/articles/1017200/ ) — Sequential протокол лучше координатора на 44%

---

### 6. 🔢 Числовое — 8.0 vs 44.0 (уверенность: 0.8)

**Общие ключевые слова:** `sequential`, `вместо`, `если`, `одного`

**A:** `docs/04-ai-collaborations/00-intro.md`
> Если поставить вместо одного человека Sequential-протокол из 8 малых агентов на дешёвых моделях, каждый видит результаты предшественников, — получаешь

**B:** `docs/05-habr-projects/memory/memnet.md`
> Если поставить вместо одного человека Sequential-протокол из 8 малых агентов на дешёвых моделях, каждый видит результаты предшественников, — получаешь

---

### 7. 🔢 Числовое — 6.0 vs 366.0 (уверенность: 0.8)

**Общие ключевые слова:** `all`, `factory`, `layer`, `mclaude`

**A:** `docs/02-anthropic-vacancies/366-технический-stack-svyazi-2-0-foundation.md`
> 0) Layer 6 — Orchestration: mclaude + AI Factory + Rufler (all MIT) Layer 7 — Execution: LiteLLM + Auto AI Router + Tool Search Layer 8 — Security: SE

**B:** `docs/CONCEPTS.md`
> md) Layer 6 — Orchestration : mclaude + AI Factory + Rufler (all MIT) → 366-технический-stack-svyazi-2-0-foundation(docs/02-anthropic-vacancies/366-те

---

### 8. 🔢 Числовое — 70.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `второе`, `месячная`, `одна`, `отрезвляющее`

**A:** `docs/02-anthropic-vacancies/00-intro.md`
> Второе — отрезвляющее: эти 70 репо — это одна 4-месячная брейн-волна , а не плоды многолетней разработки

**B:** `docs/CONCEPTS.md`
> md) Второе — отрезвляющее: эти 70 репо : одна 4-месячная брейн-волна , а не плоды многолетней разработки → 00-intro(docs/02-anthropic-vacancies/00-int

---

### 9. 🔢 Числовое — 7.0 vs 50.0 (уверенность: 0.8)

**Общие ключевые слова:** `архитектура`, `безопасная`, `добавить`, `конце`

**A:** `docs/01-svyazi/README.md`
> 0 безопасная архитектура — не “добавить сканер в конце”, а с самого начала считать skills, MCP^mcp servers, и… - 07-mvp-planning

**B:** `docs/DUPLICATES.md`
> 0 безопасная архитектура — не “добавить сканер в конце”, а с самого начала считать skills, MCP^mcp servers, импорты документов и memory writes потенци

---

### 10. 🔢 Числовое — 68.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 68) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/01-svyazi/08-conclusions.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 11. 🔢 Числовое — 68.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 68) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/VALIDATION.md`
> md: docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 12. 🔢 Числовое — 8.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/08-conclusions.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/04-ai-collaborations/07-выводы.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 13. 🔢 Числовое — 8.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/08-conclusions.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/VALIDATION.md`
> md: docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 14. 🔢 Числовое — 3.0 vs 330.0 (уверенность: 0.8)

**Общие ключевые слова:** `ingit`, `важно`, `где`, `добавляет`

**A:** `docs/02-anthropic-vacancies/329-3-что-ingit-обеспечивает-чего-cowork-не-хватает.md`
> Не менее важно: где InGit добавляет ценность, --- Содержание - 3

**B:** `docs/02-anthropic-vacancies/README.md`
> md) — Не менее важно: где InGit добавляет ценность, - 330-4-симбиотическая-архитектура

---

### 15. 🔢 Числовое — 8.0 vs 41.0 (уверенность: 0.8)

**Общие ключевые слова:** `добавляет`, `продолжение`

**A:** `docs/04-ai-collaborations/README.md`
> md(08-что-это-продолжение-добавляет

**B:** `docs/LANGUAGE_STATS.md`
> md 41% 59% 08-что-это-продолжение-добавляет

---

### 16. 🔢 Числовое — 8.0 vs 41.0 (уверенность: 0.8)

**Общие ключевые слова:** `добавляет`, `продолжение`

**A:** `docs/CLUSTERS.md`
> md — 08-что-это-продолжение-добавляет -

**B:** `docs/LANGUAGE_STATS.md`
> md 41% 59% 08-что-это-продолжение-добавляет

---

### 17. 🔢 Числовое — 22.0 vs 11.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 22) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/01-svyazi/README.md`
> 11) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^svyazi: Главный проект: экосистема AI-компонентов

---

### 18. 🔢 Числовое — 22.0 vs 785.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 22) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

---

### 19. 🔢 Числовое — 22.0 vs 11.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 22) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/SUMMARIES.md`
> 11 --- ^mcp : Model Context Protocol — протокол для AI-инструментов ^svyazi : Главный проект: экосистема AI-компонентов docs/02-anthropic-vacancies/00

---

### 20. 🔢 Числовое — 11.0 vs 785.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/README.md`
> 11) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^svyazi: Главный проект: экосистема AI-компонентов

**B:** `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

---

### 21. 🔢 Числовое — 11.0 vs 16.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/README.md`
> 11) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^svyazi: Главный проект: экосистема AI-компонентов

**B:** `docs/04-ai-collaborations/README.md`
> 16) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^svyazi: Главный проект: экосистема AI-компонентов

---

### 22. 🔢 Числовое — 5.0 vs 30.0 (уверенность: 0.8)

**Общие ключевые слова:** `edge`, `mcp`, `skills`, `tinyml`

**A:** `docs/04-ai-collaborations/00-intro.md`
> TinyML/Edge AI × MCP-протокол + skills-система Родители: edge-устройства уровня Jetson Orin / Raspberry Pi 5 / Coral с TinyChat от MIT HAN Lab (LLaMA-

**B:** `docs/05-habr-projects/memory/memnet.md`
> TinyML/Edge AI × MCP-протокол + skills-система Родители: edge-устройства уровня Jetson Orin / Raspberry Pi 5 / Coral с TinyChat от MIT HAN Lab (LLaMA-

---

### 23. 🔢 Числовое — 785.0 vs 16.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/04-ai-collaborations/README.md`
> 16) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^svyazi: Главный проект: экосистема AI-компонентов

---

### 24. 🔢 Числовое — 785.0 vs 11.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/SUMMARIES.md`
> 11 --- ^mcp : Model Context Protocol — протокол для AI-инструментов ^svyazi : Главный проект: экосистема AI-компонентов docs/02-anthropic-vacancies/00

---

### 25. 🔢 Числовое — 16.0 vs 11.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/04-ai-collaborations/README.md`
> 16) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^svyazi: Главный проект: экосистема AI-компонентов

**B:** `docs/SUMMARIES.md`
> 11 --- ^mcp : Model Context Protocol — протокол для AI-инструментов ^svyazi : Главный проект: экосистема AI-компонентов docs/02-anthropic-vacancies/00

---

### 26. 🔢 Числовое — 15.0 vs 355.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `dhlab`, `docs`, `документы`

**A:** `docs/02-anthropic-vacancies/149-appendix-b-summary-of-contributions.md`
> 15) - 355-существующие-документы-dhlab-твой-context(docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context

**B:** `docs/02-anthropic-vacancies/319-acknowledgments.md`
> md) - 355-существующие-документы-dhlab-твой-context(docs/02-anthropic-vacancies/355-существующие-документы-dhlab-твой-context

---

### 27. 🔢 Числовое — 80.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `coder`, `context`, `embed`, `nomic`

**A:** `docs/04-ai-collaborations/00-intro.md`
> qwen3-coder:30b, nomic-embed-text, 80k context, 8k max tokens, температура 0

**B:** `docs/05-habr-projects/memory/memnet.md`
> qwen3-coder:30b, nomic-embed-text, 80k context, 8k max tokens, температура 0

---

### 28. 🔢 Числовое — 30.0 vs 739.0 (уверенность: 0.8)

**Общие ключевые слова:** `методика`, `отбора`, `рамка`

**A:** `docs/LANGUAGE_STATS.md`
> md 30% 70% 02-методика-и-рамка-отбора

**B:** `docs/SIMILAR.md`
> 739 02-методика-и-рамка-отбора

---

### 29. 🔢 Числовое — 5.0 vs 36.0 (уверенность: 0.8)

**Общие ключевые слова:** `attention`, `full`, `moe`, `ssm`

**A:** `docs/04-ai-collaborations/00-intro.md`
> 5: 4 слоя full attention + 36 слоёв SSM + MoE-роутер с 8+1 экспертами на слой

**B:** `docs/05-habr-projects/memory/memnet.md`
> 5: 4 слоя full attention + 36 слоёв SSM + MoE-роутер с 8+1 экспертами на слой

---

### 30. 🔢 Числовое — 785.0 vs 26.0 (уверенность: 0.8)

**Общие ключевые слова:** `anastasiyaw`, `github`, `knowledge`, `soniablack`

**A:** `docs/01-svyazi/03-component-catalog.md`
> knowledge-space SoniaBlack / AnastasiyaW Хабр + GitHub citeturn33view0turn33view2turn37search1 Agent‑first референсная база: 785+ карточек по 26 

**B:** `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md`
> knowledge-space SoniaBlack / AnastasiyaW Хабр + GitHub citeturn33view0turn33view2turn37search1 Agent‑first референсная база: 785+ карточек по 26 

---


<!-- similar-docs -->

---

**Похожие документы:**
- [07-выводы](docs/04-ai-collaborations/07-выводы.md) (сходство 0.20)
- [08-conclusions](docs/01-svyazi/08-conclusions.md) (сходство 0.19)
- [KEYWORD_INDEX](docs/KEYWORD_INDEX.md) (сходство 0.17)

