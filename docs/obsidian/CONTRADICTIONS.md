---
title: "Противоречия в базе знаний"
tags:
  - general
date: 2026-04-29
---

# Противоречия в базе знаний

<!-- summary -->
> title: "Противоречия в базе знаний"
**Проекты:** Svyazi, LiteParse, MemNet

---

<!-- toc -->
## Содержание

- [Найденные противоречия](#найденные-противоречия)
  - [1. 🔢 Числовое — 42.0 vs 66.0 (уверенность: 0.8)](#1-числовое-420-vs-660-уверенность-08)
  - [2. 🔢 Числовое — 1017200.0 vs 44.0 (уверенность: 0.8)](#2-числовое-10172000-vs-440-уверенность-08)
  - [3. 🔢 Числовое — 8.0 vs 44.0 (уверенность: 0.8)](#3-числовое-80-vs-440-уверенность-08)
  - [4. 🔢 Числовое — 70.0 vs 4.0 (уверенность: 0.8)](#4-числовое-700-vs-40-уверенность-08)
  - [5. 🔢 Числовое — 68.0 vs 8.0 (уверенность: 0.8)](#5-числовое-680-vs-80-уверенность-08)
  - [6. 🔢 Числовое — 68.0 vs 4.0 (уверенность: 0.8)](#6-числовое-680-vs-40-уверенность-08)
  - [7. 🔢 Числовое — 68.0 vs 37.0 (уверенность: 0.8)](#7-числовое-680-vs-370-уверенность-08)
  - [8. 🔢 Числовое — 68.0 vs 4.0 (уверенность: 0.8)](#8-числовое-680-vs-40-уверенность-08)
  - [9. 🔢 Числовое — 8.0 vs 37.0 (уверенность: 0.8)](#9-числовое-80-vs-370-уверенность-08)
  - [10. 🔢 Числовое — 8.0 vs 4.0 (уверенность: 0.8)](#10-числовое-80-vs-40-уверенность-08)
  - [11. 🔢 Числовое — 8.0 vs 53.0 (уверенность: 0.8)](#11-числовое-80-vs-530-уверенность-08)
  - [12. 🔢 Числовое — 8.0 vs 4.0 (уверенность: 0.8)](#12-числовое-80-vs-40-уверенность-08)
  - [13. 🔢 Числовое — 53.0 vs 37.0 (уверенность: 0.8)](#13-числовое-530-vs-370-уверенность-08)
  - [14. 🔢 Числовое — 53.0 vs 4.0 (уверенность: 0.8)](#14-числовое-530-vs-40-уверенность-08)
  - [15. 🔢 Числовое — 53.0 vs 4.0 (уверенность: 0.8)](#15-числовое-530-vs-40-уверенность-08)
  - [16. 🔢 Числовое — 37.0 vs 4.0 (уверенность: 0.8)](#16-числовое-370-vs-40-уверенность-08)
  - [17. 🔢 Числовое — 22.0 vs 785.0 (уверенность: 0.8)](#17-числовое-220-vs-7850-уверенность-08)
  - [18. 🔢 Числовое — 22.0 vs 4.0 (уверенность: 0.8)](#18-числовое-220-vs-40-уверенность-08)
  - [19. 🔢 Числовое — 5.0 vs 30.0 (уверенность: 0.8)](#19-числовое-50-vs-300-уверенность-08)
  - [20. 🔢 Числовое — 785.0 vs 4.0 (уверенность: 0.8)](#20-числовое-7850-vs-40-уверенность-08)
  - [21. 🔢 Числовое — 33.0 vs 8.0 (уверенность: 0.8)](#21-числовое-330-vs-80-уверенность-08)
  - [22. 🔢 Числовое — 33.0 vs 8.0 (уверенность: 0.8)](#22-числовое-330-vs-80-уверенность-08)
  - [23. 🔢 Числовое — 33.0 vs 8.0 (уверенность: 0.8)](#23-числовое-330-vs-80-уверенность-08)
  - [24. 🔢 Числовое — 33.0 vs 8.0 (уверенность: 0.8)](#24-числовое-330-vs-80-уверенность-08)
  - [25. 🔢 Числовое — 33.0 vs 8.0 (уверенность: 0.8)](#25-числовое-330-vs-80-уверенность-08)
  - [26. 🔢 Числовое — 33.0 vs 8.0 (уверенность: 0.8)](#26-числовое-330-vs-80-уверенность-08)
  - [27. 🔢 Числовое — 8.0 vs 25.0 (уверенность: 0.8)](#27-числовое-80-vs-250-уверенность-08)
  - [28. 🔢 Числовое — 25.0 vs 8.0 (уверенность: 0.8)](#28-числовое-250-vs-80-уверенность-08)
  - [29. 🔢 Числовое — 25.0 vs 8.0 (уверенность: 0.8)](#29-числовое-250-vs-80-уверенность-08)
  - [30. 🔢 Числовое — 25.0 vs 8.0 (уверенность: 0.8)](#30-числовое-250-vs-80-уверенность-08)

---

<!-- tags: memory, rag, orchestration, security, ingestion, roadmap, anthropic, self-improvement, collaboration -->




_Обновлено: 2026-04-29_

Утверждений: **32902** | Противоречий: **4516**

> Автоматический поиск без LLM — возможны ложные срабатывания.

## Найденные противоречия

### 1. 🔢 Числовое — 42.0 vs 66.0 (уверенность: 0.8)

**Общие ключевые слова:** `docs`, `liteparse`, `nlaik`, `research`

**A:** `docs/contacts/antipozitive.md`
> md) 42% - Контакт: nlaik / LiteParse / research-docs(docs/contacts/nlaik

**B:** `docs/contacts/sonia-black.md`
> md) 66% - Контакт: nlaik / LiteParse / research-docs(docs/contacts/nlaik

---

### 2. 🔢 Числовое — 1017200.0 vs 44.0 (уверенность: 0.8)

**Общие ключевые слова:** `articles`, `com`, `sequential`, `координатора`

**A:** `docs/04-ai-collaborations/00-intro.md`
> com/ru/articles/1017200/) — Sequential протокол лучше координатора на 44%

**B:** `docs/05-habr-projects/memory/memnet.md`
> com/ru/articles/1017200/ ) — Sequential протокол лучше координатора на 44%

---

### 3. 🔢 Числовое — 8.0 vs 44.0 (уверенность: 0.8)

**Общие ключевые слова:** `sequential`, `вместо`, `если`, `одного`

**A:** `docs/04-ai-collaborations/00-intro.md`
> Если поставить вместо одного человека Sequential-протокол из 8 малых агентов на дешёвых моделях, каждый видит результаты предшественников, — получаешь

**B:** `docs/05-habr-projects/memory/memnet.md`
> Если поставить вместо одного человека Sequential-протокол из 8 малых агентов на дешёвых моделях, каждый видит результаты предшественников, — получаешь

---

### 4. 🔢 Числовое — 70.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `второе`, `месячная`, `одна`, `отрезвляющее`

**A:** `docs/02-anthropic-vacancies/00-intro.md`
> Второе — отрезвляющее: эти 70 репо — это одна 4-месячная брейн-волна , а не плоды многолетней разработки

**B:** `docs/CONCEPTS.md`
> md) Второе — отрезвляющее: эти 70 репо : одна 4-месячная брейн-волна , а не плоды многолетней разработки → 00-intro(docs/02-anthropic-vacancies/00-int

---

### 5. 🔢 Числовое — 68.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 68) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/01-svyazi/08-conclusions.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 6. 🔢 Числовое — 68.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 68) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/01-svyazi/08-conclusions.md`
> md) 53% - Что это продолжение добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 7. 🔢 Числовое — 68.0 vs 37.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 68) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md`
> md) 37% - Что это продолжение добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 8. 🔢 Числовое — 68.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 68) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/VALIDATION.md`
> md: docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 9. 🔢 Числовое — 8.0 vs 37.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/08-conclusions.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md`
> md) 37% - Что это продолжение добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 10. 🔢 Числовое — 8.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/08-conclusions.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/04-ai-collaborations/07-выводы.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 11. 🔢 Числовое — 8.0 vs 53.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/08-conclusions.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/04-ai-collaborations/07-выводы.md`
> md) 53% - Что это продолжение добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 12. 🔢 Числовое — 8.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/08-conclusions.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/VALIDATION.md`
> md: docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 13. 🔢 Числовое — 53.0 vs 37.0 (уверенность: 0.8)

**Общие ключевые слова:** `edge`, `mcp`, `skills`, `tinyml`

**A:** `docs/01-svyazi/08-conclusions.md`
> md) 53% - Что это продолжение добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md`
> md) 37% - Что это продолжение добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 14. 🔢 Числовое — 53.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `dhlab`, `docs`, `документы`

**A:** `docs/01-svyazi/08-conclusions.md`
> md) 53% - Что это продолжение добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/04-ai-collaborations/07-выводы.md`
> md) 53% - Что это продолжение добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 15. 🔢 Числовое — 53.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `coder`, `context`, `embed`, `nomic`

**A:** `docs/01-svyazi/08-conclusions.md`
> md) 53% - Что это продолжение добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/VALIDATION.md`
> md: docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 16. 🔢 Числовое — 37.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `docs`, `ing`, `инструментов`, `образец`

**A:** `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md`
> md) 37% - Что это продолжение добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/VALIDATION.md`
> md: docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 17. 🔢 Числовое — 22.0 vs 785.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 22) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

---

### 18. 🔢 Числовое — 22.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 22) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^llm: Large Language Model — большая языковая модель ^pii: Personally Identifiable

---

### 19. 🔢 Числовое — 5.0 vs 30.0 (уверенность: 0.8)

**Общие ключевые слова:** `edge`, `mcp`, `skills`, `tinyml`

**A:** `docs/04-ai-collaborations/00-intro.md`
> TinyML/Edge AI × MCP-протокол + skills-система Родители: edge-устройства уровня Jetson Orin / Raspberry Pi 5 / Coral с TinyChat от MIT HAN Lab (LLaMA-

**B:** `docs/05-habr-projects/memory/memnet.md`
> TinyML/Edge AI × MCP-протокол + skills-система Родители: edge-устройства уровня Jetson Orin / Raspberry Pi 5 / Coral с TinyChat от MIT HAN Lab (LLaMA-

---

### 20. 🔢 Числовое — 785.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/04-ai-collaborations/06-безопасность-приватность-и-бюджетный-роутинг.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^llm: Large Language Model — большая языковая модель ^pii: Personally Identifiable

---

### 21. 🔢 Числовое — 33.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `conclusions`, `docs`, `svyazi`

**A:** `docs/01-svyazi/01-executive-summary.md`
> md) 33% - 08 Conclusions(docs/01-svyazi/08-conclusions

**B:** `docs/01-svyazi/04-ensembles-overview.md`
> md) 33% - 08 Conclusions(docs/01-svyazi/08-conclusions

---

### 22. 🔢 Числовое — 33.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `conclusions`, `docs`, `svyazi`

**A:** `docs/01-svyazi/01-executive-summary.md`
> md) 33% - 08 Conclusions(docs/01-svyazi/08-conclusions

**B:** `docs/01-svyazi/12-roadmap.md`
> md) - 08-conclusions(docs/01-svyazi/08-conclusions

---

### 23. 🔢 Числовое — 33.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `conclusions`, `docs`, `svyazi`

**A:** `docs/01-svyazi/01-executive-summary.md`
> md) 33% - 08 Conclusions(docs/01-svyazi/08-conclusions

**B:** `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md`
> md) 25% - 08 Conclusions(docs/01-svyazi/08-conclusions

---

### 24. 🔢 Числовое — 33.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `conclusions`, `docs`, `svyazi`

**A:** `docs/01-svyazi/01-executive-summary.md`
> md) 33% - 08 Conclusions(docs/01-svyazi/08-conclusions

**B:** `docs/BROKEN_LINKS.md`
> md 08 Conclusions docs/01-svyazi/08-conclusions

---

### 25. 🔢 Числовое — 33.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `conclusions`, `docs`, `svyazi`

**A:** `docs/01-svyazi/01-executive-summary.md`
> md) 33% - 08 Conclusions(docs/01-svyazi/08-conclusions

**B:** `docs/CONTENT_GAPS.md`
> md - docs/01-svyazi/08-conclusions

---

### 26. 🔢 Числовое — 33.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `conclusions`, `docs`, `svyazi`

**A:** `docs/01-svyazi/01-executive-summary.md`
> md) 33% - 08 Conclusions(docs/01-svyazi/08-conclusions

**B:** `docs/VALIDATION.md`
> md: docs/01-svyazi/08-conclusions

---

### 27. 🔢 Числовое — 8.0 vs 25.0 (уверенность: 0.8)

**Общие ключевые слова:** `conclusions`, `docs`, `svyazi`

**A:** `docs/01-svyazi/12-roadmap.md`
> md) - 08-conclusions(docs/01-svyazi/08-conclusions

**B:** `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md`
> md) 25% - 08 Conclusions(docs/01-svyazi/08-conclusions

---

### 28. 🔢 Числовое — 25.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `conclusions`, `docs`, `svyazi`

**A:** `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md`
> md) 25% - 08 Conclusions(docs/01-svyazi/08-conclusions

**B:** `docs/BROKEN_LINKS.md`
> md 08 Conclusions docs/01-svyazi/08-conclusions

---

### 29. 🔢 Числовое — 25.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `conclusions`, `docs`, `svyazi`

**A:** `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md`
> md) 25% - 08 Conclusions(docs/01-svyazi/08-conclusions

**B:** `docs/CONTENT_GAPS.md`
> md - docs/01-svyazi/08-conclusions

---

### 30. 🔢 Числовое — 25.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `conclusions`, `docs`, `svyazi`

**A:** `docs/04-ai-collaborations/02-методика-и-рамка-отбора.md`
> md) 25% - 08 Conclusions(docs/01-svyazi/08-conclusions

**B:** `docs/VALIDATION.md`
> md: docs/01-svyazi/08-conclusions

---


<!-- see-also -->

---

**Смотрите также:**
- [[PRIORITIES]]
- [[07-выводы]]
- [[08-что-это-продолжение-добавляет]]
- [[01-executive-summary]]

