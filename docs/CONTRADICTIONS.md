# Противоречия в базе знаний

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

<!-- summary -->
> Утверждений: **71214** | Противоречий: **5915**
**Проекты:** Svyazi, LiteParse, MemNet, AutoResearch

---

<!-- toc -->
## Содержание

- [Найденные противоречия](#найденные-противоречия)
  - [1. 🔢 Числовое — 9.0 vs 4.0 (уверенность: 0.8)](#1-числовое-90-vs-40-уверенность-08)
  - [2. 🔢 Числовое — 4.0 vs 9.0 (уверенность: 0.8)](#2-числовое-40-vs-90-уверенность-08)
  - [3. 🔢 Числовое — 6.0 vs 58.0 (уверенность: 0.8)](#3-числовое-60-vs-580-уверенность-08)
  - [4. 🔢 Числовое — 1027724.0 vs 26.0 (уверенность: 0.8)](#4-числовое-10277240-vs-260-уверенность-08)
  - [5. 🔢 Числовое — 50.0 vs 27.0 (уверенность: 0.8)](#5-числовое-500-vs-270-уверенность-08)
  - [6. 🔢 Числовое — 53.0 vs 30.0 (уверенность: 0.8)](#6-числовое-530-vs-300-уверенность-08)
  - [7. 🔢 Числовое — 70.0 vs 4.0 (уверенность: 0.8)](#7-числовое-700-vs-40-уверенность-08)
  - [8. 🔢 Числовое — 3.0 vs 8.0 (уверенность: 0.8)](#8-числовое-30-vs-80-уверенность-08)
  - [9. 🔢 Числовое — 68.0 vs 8.0 (уверенность: 0.8)](#9-числовое-680-vs-80-уверенность-08)
  - [10. 🔢 Числовое — 68.0 vs 4.0 (уверенность: 0.8)](#10-числовое-680-vs-40-уверенность-08)
  - [11. 🔢 Числовое — 8.0 vs 4.0 (уверенность: 0.8)](#11-числовое-80-vs-40-уверенность-08)
  - [12. 🔢 Числовое — 8.0 vs 4.0 (уверенность: 0.8)](#12-числовое-80-vs-40-уверенность-08)
  - [13. 🔢 Числовое — 8.0 vs 58.0 (уверенность: 0.8)](#13-числовое-80-vs-580-уверенность-08)
  - [14. 🔢 Числовое — 24.0 vs 7.0 (уверенность: 0.8)](#14-числовое-240-vs-70-уверенность-08)
  - [15. 🔢 Числовое — 22.0 vs 6.0 (уверенность: 0.8)](#15-числовое-220-vs-60-уверенность-08)
  - [16. 🔢 Числовое — 22.0 vs 11.0 (уверенность: 0.8)](#16-числовое-220-vs-110-уверенность-08)
  - [17. 🔢 Числовое — 22.0 vs 3.0 (уверенность: 0.8)](#17-числовое-220-vs-30-уверенность-08)
  - [18. 🔢 Числовое — 22.0 vs 11.0 (уверенность: 0.8)](#18-числовое-220-vs-110-уверенность-08)
  - [19. 🔢 Числовое — 6.0 vs 11.0 (уверенность: 0.8)](#19-числовое-60-vs-110-уверенность-08)
  - [20. 🔢 Числовое — 6.0 vs 785.0 (уверенность: 0.8)](#20-числовое-60-vs-7850-уверенность-08)
  - [21. 🔢 Числовое — 6.0 vs 3.0 (уверенность: 0.8)](#21-числовое-60-vs-30-уверенность-08)
  - [22. 🔢 Числовое — 6.0 vs 16.0 (уверенность: 0.8)](#22-числовое-60-vs-160-уверенность-08)
  - [23. 🔢 Числовое — 6.0 vs 11.0 (уверенность: 0.8)](#23-числовое-60-vs-110-уверенность-08)
  - [24. 🔢 Числовое — 11.0 vs 3.0 (уверенность: 0.8)](#24-числовое-110-vs-30-уверенность-08)
  - [25. 🔢 Числовое — 11.0 vs 16.0 (уверенность: 0.8)](#25-числовое-110-vs-160-уверенность-08)
  - [26. 🔢 Числовое — 5.0 vs 30.0 (уверенность: 0.8)](#26-числовое-50-vs-300-уверенность-08)
  - [27. 🔢 Числовое — 1017200.0 vs 44.0 (уверенность: 0.8)](#27-числовое-10172000-vs-440-уверенность-08)
  - [28. 🔢 Числовое — 1017200.0 vs 44.0 (уверенность: 0.8)](#28-числовое-10172000-vs-440-уверенность-08)
  - [29. 🔢 Числовое — 3.0 vs 16.0 (уверенность: 0.8)](#29-числовое-30-vs-160-уверенность-08)
  - [30. 🔢 Числовое — 3.0 vs 11.0 (уверенность: 0.8)](#30-числовое-30-vs-110-уверенность-08)

---

<!-- tags: memory, rag, orchestration, security, ingestion, architecture, roadmap, anthropic, self-improve, collaboration -->




_Обновлено: 2026-05-10_

Утверждений: **71214** | Противоречий: **5915**

> Автоматический поиск без LLM — возможны ложные срабатывания.

## Найденные противоречия

### 1. 🔢 Числовое — 9.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `first`, `software`, `можно`, `собирать`

**A:** `docs/01-svyazi/README.md`
> 0 уже можно собирать из существующих software‑first кирпичей, не придумывая пол… - 09-architectural-gaps

**B:** `docs/SIMILAR_PASSAGES.md`
> 0 уже можно собирать из существующих software‑first кирпичей , не придумывая половину архитек ✅ Результат: Самый д B: docs/04-ai-collaborations/07-выв

---

### 2. 🔢 Числовое — 4.0 vs 9.0 (уверенность: 0.8)

**Общие ключевые слова:** `first`, `software`, `можно`, `собирать`

**A:** `docs/SIMILAR_PASSAGES.md`
> 0 уже можно собирать из существующих software‑first кирпичей , не придумывая половину архитек ✅ Результат: Самый д B: docs/04-ai-collaborations/07-выв

**B:** `docs/SUMMARIES.md`
> 0 уже можно собирать из существующих software‑first кирпичей , не придумывая пол… - 09-architectural-gaps

---

### 3. 🔢 Числовое — 6.0 vs 58.0 (уверенность: 0.8)

**Общие ключевые слова:** `автор`, `вовлечён`, `контекст`, `непосредственно`

**A:** `docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md`
> Контекст Автор этой статьи непосредственно вовлечён в немецкое социальное право через текущие разбирательства в Sozialgericht (дела S 6 SO 58/26 ER и 

**B:** `docs/nautilus/professional-colleague-agents-ru/08-pilot-sgb-kolega.md`
> Контекст Автор этой статьи непосредственно вовлечён в немецкое социальное право через текущие разбирательства в Sozialgericht (дела S 6 SO 58/26 ER и 

---

### 4. 🔢 Числовое — 1027724.0 vs 26.0 (уверенность: 0.8)

**Общие ключевые слова:** `articles`, `com`, `было`, `конце`

**A:** `docs/04-ai-collaborations/00-intro.md`
> com/ru/articles/1027724/ в конце статьи было написано как с помощью этой программы и ИИ нашлись два человека которые вместе организовали потом проект 

**B:** `docs/habr-unique-projects/extra-examples/00-question-habr-examples.md`
> com/ru/articles/1027724/ в конце статьи было написано как с помощью этой программы и ИИ нашлись два человека которые вместе организовали потом проект 

---

### 5. 🔢 Числовое — 50.0 vs 27.0 (уверенность: 0.8)

**Общие ключевые слова:** `docs`, `liteparse`, `research`

**A:** `docs/EMPTY_SECTIONS.md`
> md 1 2 50% research-docs-liteparse

**B:** `docs/LANGUAGE_STATS.md`
> md 27% 73% research-docs-liteparse

---

### 6. 🔢 Числовое — 53.0 vs 30.0 (уверенность: 0.8)

**Общие ключевые слова:** `components`, `docs`, `liteparse`, `research`

**A:** `docs/PRIORITIES.md`
> 53 docs/svyazi-2-0/components/research-docs-liteparse

**B:** `docs/VERSION_DIFF.md`
> md +30 — — docs/svyazi-2-0/components/research-docs-liteparse

---

### 7. 🔢 Числовое — 70.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `второе`, `месячная`, `одна`, `отрезвляющее`

**A:** `docs/02-anthropic-vacancies/00-intro.md`
> Второе — отрезвляющее: эти 70 репо — это одна 4-месячная брейн-волна , а не плоды многолетней разработки

**B:** `docs/CONCEPTS.md`
> md) Второе — отрезвляющее: эти 70 репо : одна 4-месячная брейн-волна , а не плоды многолетней разработки → 00-intro(docs/02-anthropic-vacancies/00-int

---

### 8. 🔢 Числовое — 3.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `годы`, `деятельность`, `добавить`, `областей`

**A:** `docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md`
> Фаза 2 — Расширение Областей (Годы 3-4) Деятельность: - Добавить области 2 (профессионалы на пенсии) и 8 (студенты) — обе относительно низкорисковые р

**B:** `docs/nautilus/representative-agent-layer-ru/09-strategiya-razvyortyvaniya.md`
> Фаза 2 — Расширение Областей (Годы 3-4) Деятельность: - Добавить области 2 (профессионалы на пенсии) и 8 (студенты) — обе относительно низкорисковые р

---

### 9. 🔢 Числовое — 68.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 68) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/01-svyazi/08-conclusions.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 10. 🔢 Числовое — 68.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 68) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/VALIDATION.md`
> md: docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 11. 🔢 Числовое — 8.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/08-conclusions.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/04-ai-collaborations/07-выводы.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 12. 🔢 Числовое — 8.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/08-conclusions.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/VALIDATION.md`
> md: docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 13. 🔢 Числовое — 8.0 vs 58.0 (уверенность: 0.8)

**Общие ключевые слова:** `добавляет`, `продолжение`

**A:** `docs/04-ai-collaborations/README.md`
> md(08-что-это-продолжение-добавляет

**B:** `docs/LANGUAGE_STATS.md`
> md 58% 42% 08-что-это-продолжение-добавляет

---

### 14. 🔢 Числовое — 24.0 vs 7.0 (уверенность: 0.8)

**Общие ключевые слова:** `habr`, `moltbot`, `openclaw`, `автономного`

**A:** `docs/04-ai-collaborations/00-intro.md`
> Habr Moltbot/OpenClaw добавляет автономного агента 24/7 с инструментами, браузером, почтой, API, фоном и 700+ skills; автор подчёркивает отличие от Ch

**B:** `docs/ai-collaborations/ensembles/7-domain-agent-app-factory.md`
> Habr Moltbot/OpenClaw добавляет автономного агента 24/7 с инструментами, браузером, почтой, API, фоном и 700+ skills; автор подчёркивает отличие от Ch

---

### 15. 🔢 Числовое — 22.0 vs 6.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 22) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/01-svyazi/03-component-catalog.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

---

### 16. 🔢 Числовое — 22.0 vs 11.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 22) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/01-svyazi/README.md`
> 11) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^svyazi: Главный проект: экосистема AI-компонентов

---

### 17. 🔢 Числовое — 22.0 vs 3.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 22) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^llm: Large Language Model — большая языковая модель ^pii: Personally Identifiable

---

### 18. 🔢 Числовое — 22.0 vs 11.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 22) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/SUMMARIES.md`
> 11 --- ^mcp : Model Context Protocol — протокол для AI-инструментов ^svyazi : Главный проект: экосистема AI-компонентов docs/02-anthropic-vacancies/00

---

### 19. 🔢 Числовое — 6.0 vs 11.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/03-component-catalog.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/01-svyazi/README.md`
> 11) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^svyazi: Главный проект: экосистема AI-компонентов

---

### 20. 🔢 Числовое — 6.0 vs 785.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/03-component-catalog.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

---

### 21. 🔢 Числовое — 6.0 vs 3.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/03-component-catalog.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^llm: Large Language Model — большая языковая модель ^pii: Personally Identifiable

---

### 22. 🔢 Числовое — 6.0 vs 16.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/03-component-catalog.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/04-ai-collaborations/README.md`
> 16) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^svyazi: Главный проект: экосистема AI-компонентов

---

### 23. 🔢 Числовое — 6.0 vs 11.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/03-component-catalog.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/SUMMARIES.md`
> 11 --- ^mcp : Model Context Protocol — протокол для AI-инструментов ^svyazi : Главный проект: экосистема AI-компонентов docs/02-anthropic-vacancies/00

---

### 24. 🔢 Числовое — 11.0 vs 3.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/README.md`
> 11) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^svyazi: Главный проект: экосистема AI-компонентов

**B:** `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^llm: Large Language Model — большая языковая модель ^pii: Personally Identifiable

---

### 25. 🔢 Числовое — 11.0 vs 16.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/README.md`
> 11) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^svyazi: Главный проект: экосистема AI-компонентов

**B:** `docs/04-ai-collaborations/README.md`
> 16) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^svyazi: Главный проект: экосистема AI-компонентов

---

### 26. 🔢 Числовое — 5.0 vs 30.0 (уверенность: 0.8)

**Общие ключевые слова:** `edge`, `mcp`, `skills`, `tinyml`

**A:** `docs/04-ai-collaborations/00-intro.md`
> TinyML/Edge AI × MCP-протокол + skills-система Родители: edge-устройства уровня Jetson Orin / Raspberry Pi 5 / Coral с TinyChat от MIT HAN Lab (LLaMA-

**B:** `docs/05-habr-projects/memory/memnet.md`
> TinyML/Edge AI × MCP-протокол + skills-система Родители: edge-устройства уровня Jetson Orin / Raspberry Pi 5 / Coral с TinyChat от MIT HAN Lab (LLaMA-

---

### 27. 🔢 Числовое — 1017200.0 vs 44.0 (уверенность: 0.8)

**Общие ключевые слова:** `articles`, `com`, `sequential`, `координатора`

**A:** `docs/04-ai-collaborations/00-intro.md`
> com/ru/articles/1017200/) — Sequential протокол лучше координатора на 44%

**B:** `docs/05-habr-projects/memory/memnet.md`
> com/ru/articles/1017200/ ) — Sequential протокол лучше координатора на 44%

---

### 28. 🔢 Числовое — 1017200.0 vs 44.0 (уверенность: 0.8)

**Общие ключевые слова:** `articles`, `com`, `sequential`, `координатора`

**A:** `docs/04-ai-collaborations/00-intro.md`
> com/ru/articles/1017200/) — Sequential протокол лучше координатора на 44%

**B:** `docs/habr-unique-projects/deep-pairs/7-autoresearch-distributed.md`
> com/ru/articles/1017200/) — Sequential протокол лучше координатора на 44%

---

### 29. 🔢 Числовое — 3.0 vs 16.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^llm: Large Language Model — большая языковая модель ^pii: Personally Identifiable

**B:** `docs/04-ai-collaborations/README.md`
> 16) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^svyazi: Главный проект: экосистема AI-компонентов

---

### 30. 🔢 Числовое — 3.0 vs 11.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^llm: Large Language Model — большая языковая модель ^pii: Personally Identifiable

**B:** `docs/SUMMARIES.md`
> 11 --- ^mcp : Model Context Protocol — протокол для AI-инструментов ^svyazi : Главный проект: экосистема AI-компонентов docs/02-anthropic-vacancies/00

---


<!-- see-also -->

---


## Использование

```bash
python scripts/improve_contradiction_check.py
```

```bash
# Дополнительный поиск по теме
python scripts/improve_semantic_search.py --query "Противоречия в базе знаний" --mode bm25
```

## Смотрите также
- [07-выводы](04-ai-collaborations/07-выводы.md)
- [08-conclusions](01-svyazi/08-conclusions.md)
- [FOOTNOTES](FOOTNOTES.md)
- [08-что-это-продолжение-добавляет](04-ai-collaborations/08-что-это-продолжение-добавляет.md)

