# Противоречия в базе знаний

<!-- summary -->
> Утверждений: **51294** | Противоречий: **5408**
**Проекты:** Svyazi, knowledge-space, NGT Memory, MemNet, AutoResearch

---

<!-- toc -->
## Содержание

- [Найденные противоречия](#найденные-противоречия)
  - [1. 🔢 Числовое — 6.0 vs 58.0 (уверенность: 0.8)](#1-числовое-60-vs-580-уверенность-08)
  - [2. 🔢 Числовое — 1027724.0 vs 26.0 (уверенность: 0.8)](#2-числовое-10277240-vs-260-уверенность-08)
  - [3. 🔢 Числовое — 4.0 vs 9.0 (уверенность: 0.8)](#3-числовое-40-vs-90-уверенность-08)
  - [4. 🔢 Числовое — 70.0 vs 4.0 (уверенность: 0.8)](#4-числовое-700-vs-40-уверенность-08)
  - [5. 🔢 Числовое — 3.0 vs 8.0 (уверенность: 0.8)](#5-числовое-30-vs-80-уверенность-08)
  - [6. 🔢 Числовое — 68.0 vs 8.0 (уверенность: 0.8)](#6-числовое-680-vs-80-уверенность-08)
  - [7. 🔢 Числовое — 68.0 vs 4.0 (уверенность: 0.8)](#7-числовое-680-vs-40-уверенность-08)
  - [8. 🔢 Числовое — 8.0 vs 4.0 (уверенность: 0.8)](#8-числовое-80-vs-40-уверенность-08)
  - [9. 🔢 Числовое — 8.0 vs 4.0 (уверенность: 0.8)](#9-числовое-80-vs-40-уверенность-08)
  - [10. 🔢 Числовое — 8.0 vs 41.0 (уверенность: 0.8)](#10-числовое-80-vs-410-уверенность-08)
  - [11. 🔢 Числовое — 8.0 vs 41.0 (уверенность: 0.8)](#11-числовое-80-vs-410-уверенность-08)
  - [12. 🔢 Числовое — 24.0 vs 7.0 (уверенность: 0.8)](#12-числовое-240-vs-70-уверенность-08)
  - [13. 🔢 Числовое — 22.0 vs 785.0 (уверенность: 0.8)](#13-числовое-220-vs-7850-уверенность-08)
  - [14. 🔢 Числовое — 22.0 vs 11.0 (уверенность: 0.8)](#14-числовое-220-vs-110-уверенность-08)
  - [15. 🔢 Числовое — 5.0 vs 30.0 (уверенность: 0.8)](#15-числовое-50-vs-300-уверенность-08)
  - [16. 🔢 Числовое — 1017200.0 vs 44.0 (уверенность: 0.8)](#16-числовое-10172000-vs-440-уверенность-08)
  - [17. 🔢 Числовое — 1017200.0 vs 44.0 (уверенность: 0.8)](#17-числовое-10172000-vs-440-уверенность-08)
  - [18. 🔢 Числовое — 785.0 vs 11.0 (уверенность: 0.8)](#18-числовое-7850-vs-110-уверенность-08)
  - [19. 🔢 Числовое — 4.0 vs 7.0 (уверенность: 0.8)](#19-числовое-40-vs-70-уверенность-08)
  - [20. 🔢 Числовое — 31.0 vs 3.0 (уверенность: 0.8)](#20-числовое-310-vs-30-уверенность-08)
  - [21. 🔢 Числовое — 5.0 vs 36.0 (уверенность: 0.8)](#21-числовое-50-vs-360-уверенность-08)
  - [22. 🔢 Числовое — 80.0 vs 8.0 (уверенность: 0.8)](#22-числовое-800-vs-80-уверенность-08)
  - [23. 🔢 Числовое — 785.0 vs 26.0 (уверенность: 0.8)](#23-числовое-7850-vs-260-уверенность-08)
  - [24. 🔢 Числовое — 785.0 vs 26.0 (уверенность: 0.8)](#24-числовое-7850-vs-260-уверенность-08)
  - [25. 🔢 Числовое — 6.0 vs 10.0 (уверенность: 0.8)](#25-числовое-60-vs-100-уверенность-08)
  - [26. 🔢 Числовое — 2026.0 vs 4.0 (уверенность: 0.8)](#26-числовое-20260-vs-40-уверенность-08)
  - [27. 🔢 Числовое — 4.0 vs 11.0 (уверенность: 0.8)](#27-числовое-40-vs-110-уверенность-08)
  - [28. 🔢 Числовое — 5.0 vs 3.0 (уверенность: 0.8)](#28-числовое-50-vs-30-уверенность-08)
  - [29. 🔢 Числовое — 3.0 vs 74.0 (уверенность: 0.8)](#29-числовое-30-vs-740-уверенность-08)
  - [30. 🔢 Числовое — 3.0 vs 5.0 (уверенность: 0.8)](#30-числовое-30-vs-50-уверенность-08)

---

<!-- tags: memory, rag, orchestration, knowledge, ingestion, architecture, roadmap, anthropic, self-improvement, collaboration -->




_Обновлено: 2026-04-29_

Утверждений: **51294** | Противоречий: **5408**

> Автоматический поиск без LLM — возможны ложные срабатывания.

## Найденные противоречия

### 1. 🔢 Числовое — 6.0 vs 58.0 (уверенность: 0.8)

**Общие ключевые слова:** `автор`, `вовлечён`, `контекст`, `непосредственно`

**A:** `docs/02-anthropic-vacancies/239-8-пилотное-предложение-sgb-колega-адвокат.md`
> Контекст Автор этой статьи непосредственно вовлечён в немецкое социальное право через текущие разбирательства в Sozialgericht (дела S 6 SO 58/26 ER и 

**B:** `docs/nautilus/professional-colleague-agents-ru/08-pilot-sgb-kolega.md`
> Контекст Автор этой статьи непосредственно вовлечён в немецкое социальное право через текущие разбирательства в Sozialgericht (дела S 6 SO 58/26 ER и 

---

### 2. 🔢 Числовое — 1027724.0 vs 26.0 (уверенность: 0.8)

**Общие ключевые слова:** `articles`, `com`, `было`, `конце`

**A:** `docs/04-ai-collaborations/00-intro.md`
> com/ru/articles/1027724/ в конце статьи было написано как с помощью этой программы и ИИ нашлись два человека которые вместе организовали потом проект 

**B:** `docs/habr-unique-projects/extra-examples/00-question-habr-examples.md`
> com/ru/articles/1027724/ в конце статьи было написано как с помощью этой программы и ИИ нашлись два человека которые вместе организовали потом проект 

---

### 3. 🔢 Числовое — 4.0 vs 9.0 (уверенность: 0.8)

**Общие ключевые слова:** `first`, `software`, `можно`, `собирать`

**A:** `docs/SIMILAR_PASSAGES.md`
> 0 уже можно собирать из существующих software‑first кирпичей , не придумывая половину архитек ✅ Результат: Самый д B: docs/04-ai-collaborations/07-выв

**B:** `docs/SUMMARIES.md`
> 0 уже можно собирать из существующих software‑first кирпичей , не придумывая пол… - 09-architectural-gaps

---

### 4. 🔢 Числовое — 70.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `второе`, `месячная`, `одна`, `отрезвляющее`

**A:** `docs/02-anthropic-vacancies/00-intro.md`
> Второе — отрезвляющее: эти 70 репо — это одна 4-месячная брейн-волна , а не плоды многолетней разработки

**B:** `docs/CONCEPTS.md`
> md) Второе — отрезвляющее: эти 70 репо : одна 4-месячная брейн-волна , а не плоды многолетней разработки → 00-intro(docs/02-anthropic-vacancies/00-int

---

### 5. 🔢 Числовое — 3.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `годы`, `деятельность`, `добавить`, `областей`

**A:** `docs/02-anthropic-vacancies/199-9-стратегия-поэтапного-развёртывания.md`
> Фаза 2 — Расширение Областей (Годы 3-4) Деятельность: - Добавить области 2 (профессионалы на пенсии) и 8 (студенты) — обе относительно низкорисковые р

**B:** `docs/nautilus/representative-agent-layer-ru/09-strategiya-razvyortyvaniya.md`
> Фаза 2 — Расширение Областей (Годы 3-4) Деятельность: - Добавить области 2 (профессионалы на пенсии) и 8 (студенты) — обе относительно низкорисковые р

---

### 6. 🔢 Числовое — 68.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 68) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/01-svyazi/08-conclusions.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 7. 🔢 Числовое — 68.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 68) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/VALIDATION.md`
> md: docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 8. 🔢 Числовое — 8.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/08-conclusions.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/04-ai-collaborations/07-выводы.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 9. 🔢 Числовое — 8.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `collaborations`, `docs`, `добавляет`, `продолжение`

**A:** `docs/01-svyazi/08-conclusions.md`
> md) - 08-что-это-продолжение-добавляет(docs/04-ai-collaborations/08-что-это-продолжение-добавляет

**B:** `docs/VALIDATION.md`
> md: docs/04-ai-collaborations/08-что-это-продолжение-добавляет

---

### 10. 🔢 Числовое — 8.0 vs 41.0 (уверенность: 0.8)

**Общие ключевые слова:** `добавляет`, `продолжение`

**A:** `docs/04-ai-collaborations/README.md`
> md) — - 08-что-это-продолжение-добавляет

**B:** `docs/LANGUAGE_STATS.md`
> md 41% 59% 08-что-это-продолжение-добавляет

---

### 11. 🔢 Числовое — 8.0 vs 41.0 (уверенность: 0.8)

**Общие ключевые слова:** `добавляет`, `продолжение`

**A:** `docs/04-ai-collaborations/README.md`
> md(08-что-это-продолжение-добавляет

**B:** `docs/LANGUAGE_STATS.md`
> md 41% 59% 08-что-это-продолжение-добавляет

---

### 12. 🔢 Числовое — 24.0 vs 7.0 (уверенность: 0.8)

**Общие ключевые слова:** `habr`, `moltbot`, `openclaw`, `автономного`

**A:** `docs/04-ai-collaborations/00-intro.md`
> Habr Moltbot/OpenClaw добавляет автономного агента 24/7 с инструментами, браузером, почтой, API, фоном и 700+ skills; автор подчёркивает отличие от Ch

**B:** `docs/ai-collaborations/ensembles/7-domain-agent-app-factory.md`
> Habr Moltbot/OpenClaw добавляет автономного агента 24/7 с инструментами, браузером, почтой, API, фоном и 700+ skills; автор подчёркивает отличие от Ch

---

### 13. 🔢 Числовое — 22.0 vs 785.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 22) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

---

### 14. 🔢 Числовое — 22.0 vs 11.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/01-svyazi/01-executive-summary.md`
> 22) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/SUMMARIES.md`
> 11 --- ^mcp : Model Context Protocol — протокол для AI-инструментов ^svyazi : Главный проект: экосистема AI-компонентов docs/02-anthropic-vacancies/00

---

### 15. 🔢 Числовое — 5.0 vs 30.0 (уверенность: 0.8)

**Общие ключевые слова:** `edge`, `mcp`, `skills`, `tinyml`

**A:** `docs/04-ai-collaborations/00-intro.md`
> TinyML/Edge AI × MCP-протокол + skills-система Родители: edge-устройства уровня Jetson Orin / Raspberry Pi 5 / Coral с TinyChat от MIT HAN Lab (LLaMA-

**B:** `docs/05-habr-projects/memory/memnet.md`
> TinyML/Edge AI × MCP-протокол + skills-система Родители: edge-устройства уровня Jetson Orin / Raspberry Pi 5 / Coral с TinyChat от MIT HAN Lab (LLaMA-

---

### 16. 🔢 Числовое — 1017200.0 vs 44.0 (уверенность: 0.8)

**Общие ключевые слова:** `articles`, `com`, `sequential`, `координатора`

**A:** `docs/04-ai-collaborations/00-intro.md`
> com/ru/articles/1017200/) — Sequential протокол лучше координатора на 44%

**B:** `docs/05-habr-projects/memory/memnet.md`
> com/ru/articles/1017200/ ) — Sequential протокол лучше координатора на 44%

---

### 17. 🔢 Числовое — 1017200.0 vs 44.0 (уверенность: 0.8)

**Общие ключевые слова:** `articles`, `com`, `sequential`, `координатора`

**A:** `docs/04-ai-collaborations/00-intro.md`
> com/ru/articles/1017200/) — Sequential протокол лучше координатора на 44%

**B:** `docs/habr-unique-projects/deep-pairs/7-autoresearch-distributed.md`
> com/ru/articles/1017200/) — Sequential протокол лучше координатора на 44%

---

### 18. 🔢 Числовое — 785.0 vs 11.0 (уверенность: 0.8)

**Общие ключевые слова:** `context`, `mcp`, `model`, `protocol`

**A:** `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md`
> md) --- ^mcp: Model Context Protocol — протокол для AI-инструментов ^rag: Retrieval-Augmented Generation — генерация с поиском ^llm: Large Language Mo

**B:** `docs/SUMMARIES.md`
> 11 --- ^mcp : Model Context Protocol — протокол для AI-инструментов ^svyazi : Главный проект: экосистема AI-компонентов docs/02-anthropic-vacancies/00

---

### 19. 🔢 Числовое — 4.0 vs 7.0 (уверенность: 0.8)

**Общие ключевые слова:** `match`, `pendingreview`, `proposalid`, `reviewstate`

**A:** `docs/04-ai-collaborations/14-ограничения-лицензии-и-что-пока-лучше-не-склеивать.md`
> YAML reviewstate: proposalid: "match20260429001" state: "pendingreview" requiredroles: - "evidencereviewer" - "privacyreviewer" alloweddecisions: - "a

**B:** `docs/ai-collaborations/continuation/03-a2a-vs-mcp-protocols.md`
> YAML reviewstate: proposalid: "match20260429001" state: "pendingreview" requiredroles: - "evidencereviewer" - "privacyreviewer" alloweddecisions: - "a

---

### 20. 🔢 Числовое — 31.0 vs 3.0 (уверенность: 0.8)

**Общие ключевые слова:** `различение`, `слоёв`, `трёх`

**A:** `docs/02-anthropic-vacancies/193-3-что-делает-агента-представительским.md`
> Различение трёх слоёв(31-различение-трёх-слоёв) - 3

**B:** `docs/nautilus/representative-agent-layer-ru/03-chto-delaet-predstavitelskim.md`
> Различение трёх слоёв(31-различение-трёх-слоёв) - 3

---

### 21. 🔢 Числовое — 5.0 vs 36.0 (уверенность: 0.8)

**Общие ключевые слова:** `attention`, `full`, `moe`, `ssm`

**A:** `docs/04-ai-collaborations/00-intro.md`
> 5: 4 слоя full attention + 36 слоёв SSM + MoE-роутер с 8+1 экспертами на слой

**B:** `docs/05-habr-projects/memory/memnet.md`
> 5: 4 слоя full attention + 36 слоёв SSM + MoE-роутер с 8+1 экспертами на слой

---

### 22. 🔢 Числовое — 80.0 vs 8.0 (уверенность: 0.8)

**Общие ключевые слова:** `coder`, `context`, `embed`, `nomic`

**A:** `docs/04-ai-collaborations/00-intro.md`
> qwen3-coder:30b, nomic-embed-text, 80k context, 8k max tokens, температура 0

**B:** `docs/05-habr-projects/memory/memnet.md`
> qwen3-coder:30b, nomic-embed-text, 80k context, 8k max tokens, температура 0

---

### 23. 🔢 Числовое — 785.0 vs 26.0 (уверенность: 0.8)

**Общие ключевые слова:** `anastasiyaw`, `github`, `knowledge`, `soniablack`

**A:** `docs/01-svyazi/03-component-catalog.md`
> knowledge-space SoniaBlack / AnastasiyaW Хабр + GitHub citeturn33view0turn33view2turn37search1 Agent‑first референсная база: 785+ карточек по 26 

**B:** `docs/04-ai-collaborations/03-карта-найденных-проектов-и-паттернов.md`
> knowledge-space SoniaBlack / AnastasiyaW Хабр + GitHub citeturn33view0turn33view2turn37search1 Agent‑first референсная база: 785+ карточек по 26 

---

### 24. 🔢 Числовое — 785.0 vs 26.0 (уверенность: 0.8)

**Общие ключевые слова:** `anastasiyaw`, `github`, `knowledge`, `soniablack`

**A:** `docs/01-svyazi/03-component-catalog.md`
> knowledge-space SoniaBlack / AnastasiyaW Хабр + GitHub citeturn33view0turn33view2turn37search1 Agent‑first референсная база: 785+ карточек по 26 

**B:** `docs/svyazi-2-0/overview/projects-map.md`
> knowledge-space SoniaBlack / AnastasiyaW Хабр + GitHub citeturn33view0turn33view2turn37search1 Agent‑first референсная база: 785+ карточек по 26 домен

---

### 25. 🔢 Числовое — 6.0 vs 10.0 (уверенность: 0.8)

**Общие ключевые слова:** `anastasiyaw`, `com`, `github`, `knowledge`

**A:** `docs/CITATION_INDEX.md`
> com/AnastasiyaW/knowledge-space 6 ⭐⭐⭐⭐⭐ github

**B:** `docs/CONTACTS.md`
> com/AnastasiyaW/knowledge-space 10 github

---

### 26. 🔢 Числовое — 2026.0 vs 4.0 (уверенность: 0.8)

**Общие ключевые слова:** `vladspace`, `автоматически`, `вопрос`, `документы`

**A:** `docs/contacts/kksudo.md`
> Вопрос 2 --- Создано автоматически: 2026-04-29 --- Похожие документы: - vladspace(docs/contacts/vladspace

**B:** `docs/contacts/sonia-black.md`
> Вопрос 2 --- Создано автоматически: 2026-04-29 --- Похожие документы: - vladspace(docs/contacts/vladspace

---

### 27. 🔢 Числовое — 4.0 vs 11.0 (уверенность: 0.8)

**Общие ключевые слова:** `engine`, `hebbian`, `memory`, `ngt`

**A:** `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md`
> NGT Memory автор — Hebbian engine Tier 4 — institutional reference 11

**B:** `docs/anthropic-vacancies/extra-collaborator-findings/06-final-tier-ranking.md`
> NGT Memory автор — Hebbian engine Tier 4 — institutional reference 11

---

### 28. 🔢 Числовое — 5.0 vs 3.0 (уверенность: 0.8)

**Общие ключевые слова:** `consolidation`, `outline`, `прочитаны`, `фаза`

**A:** `docs/02-anthropic-vacancies/116-9-checklist-применения-методологии.md`
> Фаза C — Consolidation - Прочитаны A и B целиком - Outline финальной версии создан - Применены правила 1-5 ко всем расхождениям - Числа верифицированы

**B:** `docs/nautilus/review-methodology/10-checklist.md`
> Фаза C — Consolidation - Прочитаны A и B целиком - Outline финальной версии создан - Применены правила 1-5 ко всем расхождениям - Числа верифицированы

---

### 29. 🔢 Числовое — 3.0 vs 74.0 (уверенность: 0.8)

**Общие ключевые слова:** `consolidation`, `operations`, `phase`, `self`

**A:** `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md`
> Phase 3: Consolidation and Self-Sustaining Operations(74-phase-3-consolidation-and-self-sustaining-operations) - 7

**B:** `docs/nautilus/okwf-concept/07-phased-rollout.md`
> Phase 3: Consolidation and Self-Sustaining Operations(74-phase-3-consolidation-and-self-sustaining-operations) - 7

---

### 30. 🔢 Числовое — 3.0 vs 5.0 (уверенность: 0.8)

**Общие ключевые слова:** `consolidation`, `operations`, `phase`, `self`

**A:** `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md`
> Phase 3: Consolidation and Self-Sustaining Operations (Years 3-5) Key activities: - Expand to 5000+ contributors - Develop endowment and reduce fundin

**B:** `docs/nautilus/okwf-concept/07-phased-rollout.md`
> Phase 3: Consolidation and Self-Sustaining Operations (Years 3-5) Key activities: - Expand to 5000+ contributors - Develop endowment and reduce fundin

---


<!-- similar-docs -->

---

**Похожие документы:**
- [CONTRADICTIONS](docs/obsidian/CONTRADICTIONS.md) (сходство 0.29)
- [07-выводы](docs/obsidian/04-ai-collaborations/07-выводы.md) (сходство 0.16)
- [08-conclusions](docs/01-svyazi/08-conclusions.md) (сходство 0.15)

