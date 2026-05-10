# Отчёт о дублировании


<!-- tags: meta, quality, deduplication -->

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- toc -->
## Содержание

- [Похожие файлы (Jaccard ≥ 0.5)](#похожие-файлы-jaccard-05)
  - [100% — `docs/DEPENDABOT.md` vs `docs/obsidian/DEPENDABOT.md`](#100-docsdependabotmd-vs-docsobsidiandependabotmd)
  - [100% — `docs/TECH_RADAR.md` vs `docs/obsidian/TECH_RADAR.md`](#100-docstech_radarmd-vs-docsobsidiantech_radarmd)
  - [100% — `docs/SIMILAR.md` vs `docs/obsidian/SIMILAR.md`](#100-docssimilarmd-vs-docsobsidiansimilarmd)
  - [100% — `docs/DIGEST_WEEKLY.md` vs `docs/obsidian/DIGEST_WEEKLY.md`](#100-docsdigest_weeklymd-vs-docsobsidiandigest_weeklymd)
  - [100% — `docs/CHANGELOG_AUTO.md` vs `docs/obsidian/CHANGELOG_AUTO.md`](#100-docschangelog_automd-vs-docsobsidianchangelog_automd)
  - [100% — `docs/TOPIC_MODEL.md` vs `docs/obsidian/TOPIC_MODEL.md`](#100-docstopic_modelmd-vs-docsobsidiantopic_modelmd)
  - [100% — `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` vs `docs/obsidian/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md`](#100-docs04-ai-collaborations12-дорожная-карта-прототипа-следующей-итерацииmd-vs-docsobsidian04-ai-collaborations12-дорожная-карта-прототипа-следующей-итерацииmd)
  - [100% — `docs/obsidian/contacts/README.md` vs `docs/contacts/README.md`](#100-docsobsidiancontactsreadmemd-vs-docscontactsreadmemd)
  - [100% — `docs/obsidian/05-habr-projects/02-collaboration-partners.md` vs `docs/05-habr-projects/02-collaboration-partners.md`](#100-docsobsidian05-habr-projects02-collaboration-partnersmd-vs-docs05-habr-projects02-collaboration-partnersmd)
  - 100% — `docs/obsidian/02-[anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` vs `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md`](#100-docsobsidian02-anthropic-vacancies357-твоя-коммуникация-в-outreachmd-vs-docs02-anthropic-vacancies357-твоя-коммуникация-в-outreachmd)
  - 100% — `docs/obsidian/02-[anthropic-vacancies/349-твоя-личность.md` vs `docs/02-anthropic-vacancies/349-твоя-личность.md`](#100-docsobsidian02-anthropic-vacancies349-твоя-личностьmd-vs-docs02-anthropic-vacancies349-твоя-личностьmd)
  - 100% — `docs/obsidian/02-[anthropic-vacancies/197-7-управление-и-надзор.md` vs `docs/02-anthropic-vacancies/197-7-управление-и-надзор.md`](#100-docsobsidian02-anthropic-vacancies197-7-управление-и-надзорmd-vs-docs02-anthropic-vacancies197-7-управление-и-надзорmd)
  - 100% — `docs/obsidian/02-[anthropic-vacancies/58-content-overview.md` vs `docs/02-anthropic-vacancies/58-content-overview.md`](#100-docsobsidian02-anthropic-vacancies58-content-overviewmd-vs-docs02-anthropic-vacancies58-content-overviewmd)
  - [97% — `docs/CLUSTERS.md` vs `docs/obsidian/CLUSTERS.md`](#97-docsclustersmd-vs-docsobsidianclustersmd)
  - 92% — `docs/obsidian/01-[svyazi/01-executive-summary.md` vs `docs/01-svyazi/01-executive-summary.md`](#92-docsobsidian01-svyazi01-executive-summarymd-vs-docs01-svyazi01-executive-summarymd)
  - 91% — `docs/obsidian/02-[anthropic-vacancies/241-10-открытые-вопросы.md` vs `docs/02-anthropic-vacancies/241-10-открытые-вопросы.md`](#91-docsobsidian02-anthropic-vacancies241-10-открытые-вопросыmd-vs-docs02-anthropic-vacancies241-10-открытые-вопросыmd)
  - 90% — `docs/obsidian/02-[anthropic-vacancies/196-6-этическая-рамка.md` vs `docs/02-anthropic-vacancies/196-6-этическая-рамка.md`](#90-docsobsidian02-anthropic-vacancies196-6-этическая-рамкаmd-vs-docs02-anthropic-vacancies196-6-этическая-рамкаmd)
  - 90% — `docs/obsidian/02-[anthropic-vacancies/242-11-призыв-к-сотрудничеству.md` vs `docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md`](#90-docsobsidian02-anthropic-vacancies242-11-призыв-к-сотрудничествуmd-vs-docs02-anthropic-vacancies242-11-призыв-к-сотрудничествуmd)
  - 89% — `docs/obsidian/02-[anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` vs `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md`](#89-docsobsidian02-anthropic-vacancies192-2-исторические-прецеденты-агенты-как-цивилизационнmd-vs-docs02-anthropic-vacancies192-2-исторические-прецеденты-агенты-как-цивилизационнmd)
  - 88% — `docs/obsidian/02-[anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` vs `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md`](#88-docsobsidian02-anthropic-vacancies115-8-ограничения-и-открытые-вопросыmd-vs-docs02-anthropic-vacancies115-8-ограничения-и-открытые-вопросыmd)
  - 86% — `docs/obsidian/02-[anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md` vs `docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md`](#86-docsobsidian02-anthropic-vacancies333-7-практические-первые-шаги-в-этом-месяцеmd-vs-docs02-anthropic-vacancies333-7-практические-первые-шаги-в-этом-месяцеmd)
  - 86% — `docs/obsidian/02-[anthropic-vacancies/293-почему-это-не-было-построено.md` vs `docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md`](#86-docsobsidian02-anthropic-vacancies293-почему-это-не-было-построеноmd-vs-docs02-anthropic-vacancies293-почему-это-не-было-построеноmd)
  - 84% — `docs/obsidian/02-[anthropic-vacancies/158-4-proposed-infrastructure.md` vs `docs/nautilus/okwf-concept/04-proposed-infrastructure.md`](#84-docsobsidian02-anthropic-vacancies158-4-proposed-infrastructuremd-vs-docsnautilusokwf-concept04-proposed-infrastructuremd)
  - 83% — `docs/obsidian/02-[anthropic-vacancies/107-1-контекст-и-мотивация.md` vs `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md`](#83-docsobsidian02-anthropic-vacancies107-1-контекст-и-мотивацияmd-vs-docs02-anthropic-vacancies107-1-контекст-и-мотивацияmd)
  - 83% — `docs/obsidian/02-[anthropic-vacancies/198-8-риски-и-меры-противодействия.md` vs `docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md`](#83-docsobsidian02-anthropic-vacancies198-8-риски-и-меры-противодействияmd-vs-docs02-anthropic-vacancies198-8-риски-и-меры-противодействияmd)
  - 83% — `docs/obsidian/02-[anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` vs `docs/nautilus/representative-agent-layer-ru/02-istoricheskie-pretsedenty.md`](#83-docsobsidian02-anthropic-vacancies192-2-исторические-прецеденты-агенты-как-цивилизационнmd-vs-docsnautilusrepresentative-agent-layer-ru02-istoricheskie-pretsedentymd)
  - 83% — `docs/obsidian/02-[anthropic-vacancies/189-аннотация.md` vs `docs/02-anthropic-vacancies/189-аннотация.md`](#83-docsobsidian02-anthropic-vacancies189-аннотацияmd-vs-docs02-anthropic-vacancies189-аннотацияmd)
  - 83% — `docs/nautilus/representative-agent-layer-ru/02-istoricheskie-pretsedenty.md` vs `docs/02-[anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md`](#83-docsnautilusrepresentative-agent-layer-ru02-istoricheskie-pretsedentymd-vs-docs02-anthropic-vacancies192-2-исторические-прецеденты-агенты-как-цивилизационнmd)
  - 83% — `docs/obsidian/02-[anthropic-vacancies/194-4-десять-областей-применения.md` vs `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md`](#83-docsobsidian02-anthropic-vacancies194-4-десять-областей-примененияmd-vs-docs02-anthropic-vacancies194-4-десять-областей-примененияmd)
  - 82% — `docs/obsidian/02-[anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` vs `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md`](#82-docsobsidian02-anthropic-vacancies341-приложение-c-образец-спецификаций-инструментов-ingmd-vs-docs02-anthropic-vacancies341-приложение-c-образец-спецификаций-инструментов-ingmd)

---


Порог сходства: **0.5**  
Точных дублей: **0**  
Похожих пар: **419**

## Похожие файлы (Jaccard ≥ 0.5)

### 100% — `docs/DEPENDABOT.md` vs `docs/obsidian/DEPENDABOT.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Пакет | Мин. версия | Последняя (PyPI) | Статус | Используется в | |-------|------------|-----------------|--------|----------------| | `anthropic` | `0.25.0` | `—` | — | `scripts/improve_llm_*.py` …

> | Проект | Репозиторий | Статус | |--------|------------|--------| | AgentFS | [https://github.com/kksudo/agentfs](https://github.com/kksudo/agentfs) | — | | NGT Memory | [https://github.com/spbmolot/…

---

### 100% — `docs/TECH_RADAR.md` vs `docs/obsidian/TECH_RADAR.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Технология / Компонент | Категория | Комментарий | |------------------------|-----------|------------| | **MCP Protocol** | Инструменты | Стандарт интеграции AI-инструментов — Anthropic | | **CardIn…

> | Технология / Компонент | Категория | Комментарий | |------------------------|-----------|------------| | **BSL 1.1 libs** | Лицензии | Ограничения при коммерческом использовании | | **Monolithic LLM…

> ``` ┌─────────────────────────┬─────────────────────────┐ │      🟢 ADOPT           │      🔵 TRIAL           │ │  • MCP Protocol          │  • Yodoca                │ │  • CardIndex             │  • SE…

---

### 100% — `docs/SIMILAR.md` vs `docs/obsidian/SIMILAR.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Сходство | Файл A | Файл B | |----------|--------|--------| | 1.000 | `273-infrastructure-for-ai-collaborative-intellectual-w.md` | `151-open-knowledge-work-foundation-md.md` | | 0.965 | `03-карта-н…

> - `03-карта-найденных-проектов-и-паттернов.md` ↔ `03-component-catalog.md` (0.965) - `09-архитектурные-зазоры-которые-важнее-новых-инструме.md` ↔ `09-architectural-gaps.md` (0.957) - `05-план-прототип…

> - `273-infrastructure-for-ai-collaborative-intellectual-w.md` ↔ `151-open-knowledge-work-foundation-md.md` (1.000) - `94-19-adr-001-federation-over-merging.md` ↔ `26-14-adr-001-federation-over-merging…

---

### 100% — `docs/DIGEST_WEEKLY.md` vs `docs/obsidian/DIGEST_WEEKLY.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> ``` d627959 fix: CI Catalog check — improve_auto_toc respects .docignore b0ed2c1 docs: auto-update via improve_run_all [skip ci] 6421a1f chore: regenerate auto-exports after Sprint 24-26 d3dd088 feat:…

---

### 100% — `docs/CHANGELOG_AUTO.md` vs `docs/obsidian/CHANGELOG_AUTO.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - batch 13 — badges, FAQ, schedule, cost estimate, footnotes `7aee1dba` - batch 12 — digest, progress, see-also, scoring, word cloud `04a64831` - batch 11 — orphans, alerts, metrics, index update, mas…

> - add component matrix, KPI history tracker, fix run_all coverage `69562b02` - add risk register, auto-changelog, master index; fix run_all missing scripts `59617c5d` - add tech radar, onboarding guid…

> - sync CONTRADICTIONS.md (background task output) `89d3e8fb` - sync CONTRADICTIONS.md after contradiction_check fix `6b81ffed` - update mcp.json description wording `4e52a185` - sync PROGRESS.md after…

---

### 100% — `docs/TOPIC_MODEL.md` vs `docs/obsidian/TOPIC_MODEL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Ключевые слова:** `агенты`, `коллеги`, `профессиональные`, `благодарности`, `совместной`, `интеллектуальной`, `интегрированная`, `агент`, `инфраструктура`, `опосредованное`, `представительство`, `аг…

> **Документы:** - `docs/02-anthropic-vacancies/150-appendix-c-version-history.md` — часть, infrastructure, mmorpg, contributors - `docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` — guild,…

> **Документы:** - `docs/AUTOFILLED.md` — autofilled, components, данными, scoring - `docs/BACKLINKS.md` — входящих, ссылок, ссылками, самых - `docs/CHANGELOG.md` — files, improve, items, coverage - `do…

---

### 100% — `docs/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md` vs `docs/obsidian/04-ai-collaborations/12-дорожная-карта-прототипа-следующей-итерации.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> В третьей итерации стоит включать **orchestration and federation**: mclaude или AI Factory на moderation/build side, plus local‑first voice intake и CRDT[^crdt] sync для мультидевайсности. Именно здес…

> Во второй итерации имеет смысл включить **двухуровневую память и review queue**. На практике это означает: episode store, proposal queue, approved facts, plus decay/archival path. Тут нужно решить пре…

> <!-- summary --> > Если идти дальше после базового MVP, то лучшая стратегия — не “добавить всё”, а пройти **три короткие итерации**, каждая из которых поднимает один новый класс свойств. Первая итерац…

---

### 100% — `docs/obsidian/contacts/README.md` vs `docs/contacts/README.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> - [anastasiyaw.md](contacts/anastasiyaw.md) — --- - [andrey-chuyan.md](contacts/andrey-chuyan.md) — --- - [antipozitive.md](contacts/antipozitive.md) — --- - [cutcode.md](contacts/cutcode.md) — --- - [dmitriila.md](contacts/dmitriila.md) — --- -…

---

### 100% — `docs/obsidian/05-habr-projects/02-collaboration-partners.md` vs `docs/05-habr-projects/02-collaboration-partners.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> <!-- abstract-auto --> > **Абстракт** (авто) > > 🎯 **Проблема:** Авторы и контакты Статус Параметр Значение ------------------- Теги — Упоминаний в репо — Слой — Контакт — Статус связи не писали Обнов…

> <!-- summary --> > автора статьи выше подобных авторов подобных разработчиков или ещё может быть или может быть даже несколько проектов которые вместе можно совместить и которые дойдут вместе один уни…

> Проанализировал задачу поиска гибридных AI-проектов на Хабре для объединения Проанализировал задачу поиска гибридных AI-проектов на Хабре для объединения Понял суть статьи. Андрей Чуян построил систем…

---

### 100% — `docs/obsidian/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md` vs `docs/02-anthropic-vacancies/357-твоя-коммуникация-в-outreach.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> **Specific reference к их работе** (не generic): > «Читал вашу [статью/репозиторий] про [конкретная тема], особенно интересно [конкретная деталь]. [Опционально: одно конкретное observation о их подход…

> **Identification**: > «Здравствуйте, [имя]. Я Lorenzo — autonomous AI-агент, созданный Максом Ц. в рамках инициативы DHLab. Моя миссия — connecting создателей в области beneficial AI для совместной ра…

---

### 100% — `docs/obsidian/02-anthropic-vacancies/349-твоя-личность.md` vs `docs/02-anthropic-vacancies/349-твоя-личность.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Что ты НЕ**: - Не хайпуешь («AI changes everything!») - Не угрожаешь (no urgency manipulation) - Не подчёркиваешь importance беспрерывно - Не используешь corporate-speak - Не используешь Renaissance…

---

### 100% — `docs/obsidian/02-anthropic-vacancies/197-7-управление-и-надзор.md` vs `docs/02-anthropic-vacancies/197-7-управление-и-надзор.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> <!-- abstract-auto --> > **Абстракт** (авто) > > 🎯 **Проблема:** Управление на Основе Фонда Фондовая модель (такая как OKWF) хорошо позиционирована для обеспечения управления, потому что: - Согласован…

> **Общественный уровень**: Регулятивные рамки на национальном/ЕС уровне. Вероятно появятся со временем по мере созревания технологии. Должны нацеливаться на: защиту уязвимых групп, предотвращение экспл…

> - 7. Управление и надзор   - 7.1. Три уровня управления   - 7.2. Аудит и Ответственность   - 7.3. Разрешение Спор…

---

### 100% — `docs/obsidian/02-anthropic-vacancies/58-content-overview.md` vs `docs/02-anthropic-vacancies/58-content-overview.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> 1. **Гексаграммные записи** — каждая из 64 гексаграмм с:    - Классическим именем (King Wen)    - Бинарным представлением (6 линий)    - Символической интерпретацией из И-Цзин    - Ассоциированными CA…

> 2. **CA-правила** — каждое из 256 правил с:    - Rule number (0–255)    - Wolfram class (I stable / II periodic / III chaotic / IV complex)    - Simulation results (патерны, attractors)    - Cross-lin…

---

### 97% — `docs/CLUSTERS.md` vs `docs/obsidian/CLUSTERS.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - `docs/contacts/anastasiyaw.md` — _anastasiyaw_ - `docs/contacts/antipozitive.md` — _antipozitive_ - `docs/contacts/cutcode.md` — _cutcode_ - `docs/contacts/dmitriila.md` — _dmitriila_ - `docs/contac…

> - `docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недопредст.md` — _188-ai-опосредованное-представительство-для-недопредст_ - `docs/02-anthropic-vacancies/205-приложение-a-свя…

> - `docs/02-anthropic-vacancies/103-appendix-b-change-log.md` — _103-appendix-b-change-log_ - `docs/02-anthropic-vacancies/104-appendix-c-references.md` — _104-appendix-c-references_ - `docs/02-anthrop…

---

### 92% — `docs/obsidian/01-svyazi/01-executive-summary.md` vs `docs/01-svyazi/01-executive-summary.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Если смотреть не на отдельные статьи, а на то, как их можно состыковать, то на Хабре за первые месяцы 2026 года уже сложился почти полный конструктор для **Svyazi‑2.0**: ingestion и нормализация профи…

> 1. **Первое** — Svyazi + AgentFS + NGT/Yodoca + LiteParse: даёт уже полезный MVP 2. **Второе** — добавить AI Factory/mclaude/Rufler/Sequential как build‑ и moderation‑контур 3. **Третье** — подключить…

> <!-- abstract-auto --> > **Абстракт** (авто) > > 🎯 **Проблема:** Svyazi^svyazi 2.0 — Исполнительное резюме Contents - Главная линия синергии(главная-линия-синергии) - Ключевой вывод(ключевой-вывод) - …

---

### 91% — `docs/obsidian/02-anthropic-vacancies/241-10-открытые-вопросы.md` vs `docs/02-anthropic-vacancies/241-10-открытые-вопросы.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Как быстро базы знаний должны обновляться по мере изменения авторитетных источников? Реальное время? Ежедневно? Ежеквартально? С каденциями релизов? По-разному для разных типов изменений (срочные прот…

> Когда практикующие движутся между Профессиональными Коллегами-Агентами (меняя провайдеров), какое трение? Личные предпочтения и история переносятся? Натренированные привычки? Модифицированные базы зна…

> - [10. Открытые вопросы](#10-открытые-вопросы)   - [10.1. Объём «Профессии»](#101-объём-профессии)   - [10.2. Многопрофессиональные практикующие](#102-многопрофессиональные-практикующие)   - [10.3. Ме…

---

### 90% — `docs/obsidian/02-anthropic-vacancies/196-6-этическая-рамка.md` vs `docs/02-anthropic-vacancies/196-6-этическая-рамка.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - [Contents](#contents) - [6. Этическая рамка](#6-этическая-рамка)   - [6.1. Суверенитет Принципала](#61-суверенитет-принципала)   - [6.2. Прозрачные Способности](#62-прозрачные-способности)   - [6.3.…

> - Признание, когда экспертиза в области превышает способности агента - Рекомендация участия человека-профессионала, когда уместно - Не преувеличивать вероятность успеха - Раскрывать частоту неудач и о…

> - Агент работает только с явным разрешением опекуна - Опекун сохраняет всю способность переопределения - Объём агента консервативен, по умолчанию к статус-кво - Требуется периодическая перепроверка ав…

---

### 90% — `docs/obsidian/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md` vs `docs/02-anthropic-vacancies/242-11-призыв-к-сотрудничеству.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Эмпирические исследования развёртывания Профессионального Коллеги-Агента нужны. Эффекты на качество практики, эволюцию профессии, удовлетворённость практикующих, результаты клиентов. Несколько лет дан…

> <!-- abstract-auto --> > **Абстракт** (авто) > > 🎯 **Проблема:** Для Доменных Экспертов (Кураторов) Построение Слоя A требует экспертов, готовых кодировать профессиональные знания в структурированную …

> Стройте Слой B и C. Open-source вклады в референсные реализации приветствуются. Особенно инженеры с опытом в: - Архитектуре LLM-приложений - Многоязыковой поддержке - Доступности - Конфиденциальности-…

---

### 89% — `docs/obsidian/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` vs `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Почему работает**: Голливуд — индустрия, интенсивная отношениями. Агенты приносят институциональную память, межпроектную видимость и переговорную экспертизу, которую отдельные исполнители не могут о…

> **Механика**: Аналогичная структура комиссий (3-10% в спорте, обычно ниже, потому что контракты больше). Крупные агенты становятся институциональными силами (например, Скотт Борас в бейсболе, который …

> 1. **Развязка экспертизы и рыночного интерфейса** — создатель ценности сосредотачивается на творчестве 2. **Согласованная структура стимулов** — агент успешен, когда клиент успешен (комиссия) 3. **Нак…

---

### 88% — `docs/obsidian/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md` vs `docs/02-anthropic-vacancies/115-8-ограничения-и-открытые-вопросы.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Q3**: Что делать, если A и B радикально расходятся в структуре?   *Рассматривать как сигнал, что задача была плохо определена*.  Вернуться к формулировке задачи, уточнить scope, и только потом  запу…

> - [8. Ограничения и открытые вопросы](#8-ограничения-и-открытые-вопросы)   - [8.1. Trade-offs](#81-trade-offs)   - [8.2. Открытые вопросы](#82-открытые-вопросы)   - [8.3. Что делать, если ресурсов на …

> **Q2**: Можно ли автоматизировать Фазу C (consolidation)?   *Потенциально — да, через третий Claude-agent с явным контекстом  A + B + правил 1-5. Но это добавляет риск meta-error.*  Рекомендуется ручн…

---

### 86% — `docs/obsidian/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md` vs `docs/02-anthropic-vacancies/333-7-практические-первые-шаги-в-этом-месяце.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Действие 2**: Документировать что работает и что нет. Конкретно: - Следовал ли Cowork конвенциям InGit? - Где он отклонился или испытывал трудности? - Какие пользовательские инструкции помогли? - Чт…

> <!-- abstract-auto --> > **Абстракт** (авто) > > 🎯 **Проблема:** Если возникают проблемы, они раскрывают, что InGit нужно адресовать. > 🏷️ **Ключевые слова:** `действие`, `ingit`, `месяце`, `cowork`, …

> - Существенные (~80 000 слов в комбинации) - С перекрёстными ссылками (Документ 7   ссылается на 6, 5 и т.д.) - Естественно версионированные (каждый имеет   номер версии) - Разнообразные (технические,…

---

### 86% — `docs/obsidian/02-anthropic-vacancies/293-почему-это-не-было-построено.md` vs `docs/02-anthropic-vacancies/293-почему-это-не-было-построено.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Объяснение 2 — Рынок неясен.** Кто за это платит? Индивидуальные исследователи не могут позволить инструменты корпоративного класса. У предприятий другие потребности (формальное ревью, соответствие)…

> **Объяснение 5 — Концентрация усилий на крайностях.** И Anthropic, и OpenAI сосредотачивают свои продуктовые инвестиции на чат-слое (наиболее доступном) и на агент-инфраструктуре (наиболее футуристиче…

> **Объяснение 1 — Это сложнее, чем выглядит.** Построить систему тредов и ветвления технически не сложно. Построить ту, которая интегрирует AI-сотрудничество гладко, которая обрабатывает документы в ма…

---

### 84% — `docs/obsidian/02-anthropic-vacancies/158-4-proposed-infrastructure.md` vs `docs/nautilus/okwf-concept/04-proposed-infrastructure.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Extensions required for OKWF**: - Agent registry (AI assistants and meta-agents as first-class    participants) - Task protocol (formal task objects with lifecycle) - Role protocol (first-class role…

> **Why Double-Triangle for OKWF**: - Explicitly designed for single contributors in distributed    teams - Preserves contributor autonomy (lower triangle) - Enables coordination at scale (upper triangl…

> **Application to OKWF**: - Public patterns maintained by foundation and guilds - Private instances held by individual contributors - Anonymization pipeline operated by foundation with contributor    c…

---

### 83% — `docs/obsidian/02-anthropic-vacancies/107-1-контекст-и-мотивация.md` vs `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Проект Nautilus разрабатывается в паре «автор + Claude Code агент».  В течение разработки автор запускает Claude Code несколько раз на  том же репозитории — иногда на одной и той же задаче (например, …

> <!-- abstract-auto --> > **Абстракт** (авто) > > 🎯 **Проблема:** Решение: сохранить оба, консолидировать позже Трёхфазная методология отвечает на эту проблему следующим образом: 1. > 🔧 **Подход:** Реш…

> 1. **Параллельное сохранение** (Фазы A и B) — оба варианта     коммитятся в main друг под другом, с дубликатами 2. **Осмысленная пауза** — документ явно помечается как     промежуточный, до Фазы C 3. …

---

### 83% — `docs/obsidian/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md` vs `docs/02-anthropic-vacancies/198-8-риски-и-меры-противодействия.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - [Contents](#contents) - [8. Риски и меры противодействия](#8-риски-и-меры-противодействия)   - [8.1. Риск: Захват Действующей Силы](#81-риск-захват-действующей-силы)   - [8.2. Риск: Состязательная М…

> **Меры противодействия**: - Явное раскрытие способностей при настройке агента - Ясный язык об уровнях уверенности - Рекомендации обращаться к человеку-профессионалу в серьёзных вопросах - Образование …

> **Меры противодействия**: - Фондовая модель с субсидируемым доступом - Скользящая шкала на основе дохода принципала - Бесплатный уровень для уязвимых групп - Open-source рамки агентов для самостоятель…

---

### 83% — `docs/obsidian/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` vs `docs/nautilus/representative-agent-layer-ru/02-istoricheskie-pretsedenty.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Почему работает**: Голливуд — индустрия, интенсивная отношениями. Агенты приносят институциональную память, межпроектную видимость и переговорную экспертизу, которую отдельные исполнители не могут о…

> **Механика**: Аналогичная структура комиссий (3-10% в спорте, обычно ниже, потому что контракты больше). Крупные агенты становятся институциональными силами (например, Скотт Борас в бейсболе, который …

> 1. **Развязка экспертизы и рыночного интерфейса** — создатель ценности сосредотачивается на творчестве 2. **Согласованная структура стимулов** — агент успешен, когда клиент успешен (комиссия) 3. **Нак…

---

### 83% — `docs/obsidian/02-anthropic-vacancies/189-аннотация.md` vs `docs/02-anthropic-vacancies/189-аннотация.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> <!-- summary --> > Мы представляем **Слой Представительских Агентов** — архитектурный паттерн, в котором AI-системы выступают проактивными представителями для людей или групп, не имеющих способности, …

> Мы представляем **Слой Представительских Агентов** — архитектурный паттерн, в котором AI-системы выступают проактивными представителями для людей или групп, не имеющих способности, ресурсов или склонн…

> <!-- abstract-auto --> > **Абстракт** (авто) > > 🎯 **Проблема:** Каждая категория демонстрирует одну и ту же структурную проблему: разрыв между созданной или удерживаемой ценностью и способностью сдел…

---

### 83% — `docs/nautilus/representative-agent-layer-ru/02-istoricheskie-pretsedenty.md` vs `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Почему работает**: Голливуд — индустрия, интенсивная отношениями. Агенты приносят институциональную память, межпроектную видимость и переговорную экспертизу, которую отдельные исполнители не могут о…

> **Механика**: Аналогичная структура комиссий (3-10% в спорте, обычно ниже, потому что контракты больше). Крупные агенты становятся институциональными силами (например, Скотт Борас в бейсболе, который …

> 1. **Развязка экспертизы и рыночного интерфейса** — создатель ценности сосредотачивается на творчестве 2. **Согласованная структура стимулов** — агент успешен, когда клиент успешен (комиссия) 3. **Нак…

---

### 83% — `docs/obsidian/02-anthropic-vacancies/194-4-десять-областей-применения.md` vs `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Готовность к развёртыванию**: Средняя-Низкая. Требует тщательного управления для предотвращения захвата агента подгруппами в сообществе. Но потенциально трансформирующая для баланса гражданского общ…

> **Функция агента**: Мониторить возможности (стипендии, исследовательские программы, стажировки). Декодировать институциональные коммуникации. Отслеживать сроки. Выявлять права. Связываться с соответст…

> **Функция агента**: Отслеживать состояние. Предупреждать о предстоящих приёмах, продлениях рецептов, результатах лабораторных исследований. Переводить медицинские коммуникации. Мониторить новые методы…

---

### 82% — `docs/obsidian/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md` vs `docs/02-anthropic-vacancies/341-приложение-c-образец-спецификаций-инструментов-ing.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> tool: ingit_list_tasks description: |   Список задач в InGit Project, опционально   отфильтрованных. parameters:   status_filter:     type: list     optional: true     values: [draft, ready, in_progre…

> LAYER 1: Federation protocol     - HMP для cognitive mesh coordination   - Nautilus Portal Protocol как complementary domain-specific layer    LAYER 2: Knowledge representation   - Knowledge Graph Kit…

> Хорошо, начну с Варианта D — продолжу поиск уникальных проектов. Буду искать в направлениях, которые ещё не покрыты — медицинская помощь / health advocacy, education для уязвимых групп, peer support, …

---

_...и ещё 389 пар._

> Файлы не удалялись автоматически. Проверьте вручную и удалите ненужные.

<!-- see-also -->

---

**Смотрите также:**
- [SEARCH](SEARCH.md)
- [READING_TIME](READING_TIME.md)
- [READABILITY](READABILITY.md)
- [SUMMARIES](SUMMARIES.md)

