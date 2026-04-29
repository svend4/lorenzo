---
title: "Отчёт о дублировании"
tags:
  - general
date: 2026-04-29
---

# Отчёт о дублировании

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

Порог сходства: **0.5**  
Точных дублей: **0**  
Похожих пар: **307**

## Похожие файлы (Jaccard ≥ 0.5)

### 100% — `docs/SCHEDULE.md` vs `docs/obsidian/SCHEDULE.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> ``` Фаза                    | Q4'24 | Q1'25 | Q2'25 | Q3'25 | Q4'25 | Q1'26 | Q2'26 | Q3'26 ------------------------|-------|-------|-------|-------|-------|-------|-------|------- Исследование       …

> | Срок | Веха | Статус | |------|------|--------| | **2024-Q4** | ✅ Исследование компонентов завершено | ✅ Выполнено | | **2024-Q4** | ✅ Архитектура Svyazi 2.0 задокументирована | ✅ Выполнено | | **20…

---

### 100% — `docs/ORPHANS.md` vs `docs/obsidian/ORPHANS.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> 1. Добавить ссылки на изолированные файлы из README.md соответствующего раздела 2. Проверить, не являются ли они дублями других файлов 3. Крупные изолированные файлы (>100 слов) — добавить в READING_O…

---

### 100% — `docs/DEPENDABOT.md` vs `docs/obsidian/DEPENDABOT.md`

**Общих абзацев:** 2  
**Примеры совпадений:**

> | Проект | Репозиторий | Статус | |--------|------------|--------| | AgentFS | [https://github.com/kksudo/agentfs](https://github.com/kksudo/agentfs) | — | | NGT Memory | [https://github.com/spbmolot/…

> | Пакет | Мин. версия | Последняя (PyPI) | Статус | Используется в | |-------|------------|-----------------|--------|----------------| | `anthropic` | `0.25.0` | `—` | — | `scripts/improve_llm_*.py` …

---

### 100% — `docs/SCORING.md` vs `docs/obsidian/SCORING.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> | Критерий | Статус | Вес | |----------|--------|-----| | Прогресс MVP отслеживается | ✅ | 8 | | Action items задокументированы | ✅ | 8 | | Порядок чтения задан | ✅ | 5 | | Executive report создан | ✅…

> | Критерий | Статус | Вес | |----------|--------|-----| | Риски выявлены и задокументированы | ✅ | 8 | | Лицензии проверены | ✅ | 8 | | Сломанных ссылок < 30 | ❌ | 5 | |  ↳ _Слишком много сломанных сс…

> | Критерий | Статус | Вес | |----------|--------|-----| | Компоненты каталогизированы (20+) | ✅ | 10 | | Ансамбли определены (5+) | ✅ | 10 | | Архитектурные пробелы выявлены | ✅ | 8 | | Безопасность и…

---

### 100% — `docs/MINDMAP.md` vs `docs/obsidian/MINDMAP.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> ```mermaid flowchart LR   subgraph INGEST     Svyazi[Svyazi]     CardIndex[CardIndex]     Firecrawl[Firecrawl]   end   subgraph KNOWLEDGE     AgentFS[AgentFS]     knowledge-space[knowledge-space]   en…

> ```mermaid mindmap   root((Lorenzo Repository))     🧠 **Svyazi 2.0**       CardIndex       Evidence Envelope       Memory Write Policy       Ансамбли       MVP 12-18 дней       Безопасность     💼 **An…

> | Слой | Проекты | |------|---------| | Ingestion | Svyazi, CardIndex, Firecrawl | | Knowledge | AgentFS, knowledge-space | | Memory | Yodoca, NGT Memory, MemNet | | RAG | LiteParse, Legal RAG, Hybrid…

---

### 100% — `docs/CHANGELOG_AUTO.md` vs `docs/obsidian/CHANGELOG_AUTO.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - batch 13 — badges, FAQ, schedule, cost estimate, footnotes `7aee1dba` - batch 12 — digest, progress, see-also, scoring, word cloud `04a64831` - batch 11 — orphans, alerts, metrics, index update, mas…

> - add component matrix, KPI history tracker, fix run_all coverage `69562b02` - add risk register, auto-changelog, master index; fix run_all missing scripts `59617c5d` - add tech radar, onboarding guid…

> | Тип | Название | Кол-во | |-----|---------|--------| | `feat` | ✨ Новые возможности | 17 | | `fix` | 🐛 Исправления | 3 | | `docs` | 📝 Документация | 2 | | `chore` | 🔧 Технические задачи | 10 | | `ot…

---

### 100% — `docs/obsidian/autofilled/components/.md` vs `docs/obsidian/autofilled/components/ingit.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Похожие документы:** - [[svyazi]] (сходство 1.00) - [[sgb]] (сходство 1.00) - [nautilus](docs/obsidian/autofill…

---

### 100% — `docs/obsidian/autofilled/components/.md` vs `docs/obsidian/autofilled/components/cowork.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Похожие документы:** - [svyazi](docs/obsidian/autofilled/components/svyazi.md) (сходство 1.00) - [[sgb]] (сходство 1.00) - [nautilus](docs/obsidian/autofill…

---

### 100% — `docs/obsidian/autofilled/components/.md` vs `docs/obsidian/autofilled/components/lorenzo.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Похожие документы:** - [svyazi](docs/obsidian/autofilled/components/svyazi.md) (сходство 1.00) - [[sgb]] (сходство 1.00) - [nautilus](docs/obsidian/autofill…

---

### 100% — `docs/obsidian/autofilled/components/ingit.md` vs `docs/obsidian/autofilled/components/cowork.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Похожие документы:** - [svyazi](docs/obsidian/autofilled/components/svyazi.md) (сходство 1.00) - [[sgb]] (сходство 1.00) - [nautilus](docs/obsidian/autofill…

---

### 100% — `docs/obsidian/autofilled/components/ingit.md` vs `docs/obsidian/autofilled/components/lorenzo.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Похожие документы:** - [svyazi](docs/obsidian/autofilled/components/svyazi.md) (сходство 1.00) - [[sgb]] (сходство 1.00) - [nautilus](docs/obsidian/autofill…

---

### 100% — `docs/obsidian/autofilled/components/cowork.md` vs `docs/obsidian/autofilled/components/lorenzo.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> **Похожие документы:** - [svyazi](docs/obsidian/autofilled/components/svyazi.md) (сходство 1.00) - [[sgb]] (сходство 1.00) - [nautilus](docs/obsidian/autofill…

---

### 90% — `docs/TOPIC_MODEL.md` vs `docs/obsidian/TOPIC_MODEL.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Документы:** - `docs/02-anthropic-vacancies/107-1-контекст-и-мотивация.md` — ограничения, разрабатывается, паре, агент - `docs/02-anthropic-vacancies/188-ai-опосредованное-представительство-для-недо…

> **Документы:** - `docs/01-svyazi/01-executive-summary.md` — svyazi, подобный, agentfs, проект - `docs/01-svyazi/02-methodology.md` — отбора, методика, рамка, первичный - `docs/01-svyazi/03-component-c…

> - [Тема 1: turn, view, cite (325 документов)](#тема-1-turn-view-cite-325-документов) - [Тема 4: cowork, ingit, composite (79 документов)](#тема-4-cowork-ingit-composite-79-документов) - [Тема 2: middl…

---

### 88% — `docs/obsidian/02-anthropic-vacancies/158-4-proposed-infrastructure.md` vs `docs/nautilus/okwf-concept/04-proposed-infrastructure.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Application to OKWF**: - Each contributor = Node with personal AI assistants (lower    triangle) - Guild-level coordination via meta-agent (upper triangle) - Cross-guild coordination via higher-leve…

> **Funding sources**: - Corporate sponsorships (core unrestricted funds) - Grant funding (project-specific) - Client payments (commercial projects) - Foundation endowment (eventual self-sustaining core…

> **Mechanism**: - OKWF foundation provides EoR-equivalent services - AI-assisted compliance automation reduces costs 10x vs.    existing platforms - Modular legal templates for different engagement typ…

---

### 86% — `docs/obsidian/02-anthropic-vacancies/261-8-seven-domains-of-application.md` vs `docs/nautilus/composite-skills-agents/08-seven-domains.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Typical configurations**: A computational biologist working  on epidemiology with humanities co-authors faces unique  configuration needs combining biology, computer science,  epidemiological method…

> **Bridge to existing infrastructure**: Many artists already  combine multiple educational sources (online courses, traditional  training, peer learning). Composite agents formalize and  augment this p…

> **Sub-agent specializations might include**: Classical  composition, jazz improvisation, electronic music production,  specific instruments (piano, violin, voice, etc.), genres  (folk traditions, cont…

---

### 85% — `docs/obsidian/02-anthropic-vacancies/162-8-risk-analysis.md` vs `docs/nautilus/okwf-concept/08-risk-analysis.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Mitigations**: - Anchor partner committed before launch - Multiple partnership types explored in parallel - Hybrid funding model (corporate + foundation + grants) - Strong pipeline of grants submiss…

> **Mitigations**: - Realistic hiring of core team (5-8 people, not 3) - Co-leadership model (Executive Director supported by    technical, community leads) - Clear succession planning from launch - Exp…

> **Evidence that quality achievable**: - Existing open-source communities produce high-quality work - AI-assistance dramatically reduces variance - Guild-based mentorship structures proven elsewhere - …

---

### 83% — `docs/CODE_BLOCKS.md` vs `docs/obsidian/CODE_BLOCKS.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> ```markdown > ⚠️ **Статус документа**: сравнительный промежуточный вариант. >  > Этот файл содержит **параллельно сохранённые версии** из двух  > независимых анализов: Вариант A (ветка ``) и Вариант B…

> ```python class QueryResult:     query: str     results_by_repo: dict[str, list[PortalEntry]]     consensus: Consensus     total_entries: int     repos_queried: list[str]     errors: dict[str, str]   …

> ```json {   "query": "string",   "entries": [     {       "id": "string",       "title": "string",       "source": "owner/repo",       "format_type": "string",       "content": "string",       "metada…

---

### 83% — `docs/obsidian/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` vs `docs/nautilus/representative-agent-layer-ru/02-istoricheskie-pretsedenty.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> 1. **Развязка экспертизы и рыночного интерфейса** — создатель ценности сосредотачивается на творчестве 2. **Согласованная структура стимулов** — агент успешен, когда клиент успешен (комиссия) 3. **Нак…

> **Механика**: На основе комиссии (10% стандарт). Агентства (CAA, WME, UTA) имеют сотни агентов, структурированных как сложные организации со специализированными отделами (кино, ТВ, музыка, издательско…

> **Ограничения**: Крупные агентства обслуживают только верхний эшелон. Новые или малозарабатывающие исполнители с трудом получают представительство. Это создаёт ту же проблему Золушки на уровне начинаю…

---

### 83% — `docs/obsidian/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` vs `docs/nautilus/composite-skills-agents/03-what-makes-csa.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Property 2 — Sub-Agents Are Individually General.** Each  sub-agent in the configuration is a Type 1-style Professional  Colleague Agent for a narrow specialization, shared across  all principals wh…

> **Property 6 — Disagreement Surfacing.** When sub-agents  disagree (which is normal and informative), the composite agent  surfaces the disagreement to the principal rather than masking  it through av…

> We suggest twenty as a reasonable working constraint:  configurations under five are probably better served by Type 1;  configurations over forty are probably indicating a need for  narrower focus or …

---

### 83% — `docs/obsidian/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` vs `docs/nautilus/composite-skills-agents/10-risks.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Mitigations**: - Strong starting templates for common professional patterns - AI-assisted recommendation as default (with override) - Limit on initial configuration size (start with 5-10, grow    ov…

> **Scenario**: Principal selects sub-agents that confirm their  existing approach, missing specializations that would challenge  or expand their practice. Composite becomes a sophisticated  form of con…

> **Scenario**: Faced with hundreds of available sub-agents, the  principal cannot decide which to include. Configuration becomes  overwhelming task. Principal gives up and uses generic  Professional Co…

---

### 82% — `docs/obsidian/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` vs `docs/nautilus/composite-skills-agents/02-twenty-one-teachers-pattern.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Medicine.** Physicians who developed specific specialties  combining multiple clinical areas — for example, oncology with  focus on immunology and palliative care. Each component  specialization is …

> A journalist interviewing an Indian yoga master asked how he  became a teacher. The master replied that before he became a  teacher in his own right, he had studied with twenty different  teachers. Ea…

> The master, asked to characterize his own teaching, said:  **none of his twenty teachers taught what he teaches**. Each  contributed a specialization. The combination — that twenty-first  teacher — wa…

---

### 82% — `docs/obsidian/02-anthropic-vacancies/194-4-десять-областей-применения.md` vs `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Функция агента**: Мониторить запросы клиентов по разным каналам. Составлять ответы. Отслеживать регулятивные сроки. Выявлять возможности (гранты для малого бизнеса, новые рыночные тренды). Управлять…

> <!-- summary --> > Паттерн Представительских Агентов широко применим. Мы выделяем десять разных областей, упорядоченных по готовности к развёртыванию (наиболее простые сначала, наиболее сложные в конц…

> **Функция агента**: Отслеживать статус каждого клиента в нескольких системах услуг. Предупреждать работника о сроках, возможностях, осложнениях. Составлять рутинные коммуникации. Готовить клиент-специ…

---

### 82% — `docs/obsidian/02-anthropic-vacancies/173-4-ten-domains-of-application.md` vs `docs/nautilus/representative-agent-layer-en/04-ten-domains.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Critical clarification**: The agent represents the **social  worker**, not the clients directly. It serves the worker's  ability to advocate for clients. Direct client representation  is more sensit…

> **Agent function**: Monitor customer inquiries across channels.  Draft responses. Track regulatory deadlines. Identify  opportunities (grants for small business, new market trends).  Manage routine co…

> The Representative Agent pattern applies broadly. We identify  ten distinct domains, ordered by readiness for deployment  (easiest first, most challenging last). Each section briefly  outlines: who is…

---

### 81% — `docs/obsidian/02-anthropic-vacancies/194-4-десять-областей-применения.md` vs `docs/nautilus/representative-agent-layer-ru/04-desyat-oblastey.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Функция агента**: Мониторить запросы клиентов по разным каналам. Составлять ответы. Отслеживать регулятивные сроки. Выявлять возможности (гранты для малого бизнеса, новые рыночные тренды). Управлять…

> **Функция агента**: Отслеживать статус каждого клиента в нескольких системах услуг. Предупреждать работника о сроках, возможностях, осложнениях. Составлять рутинные коммуникации. Готовить клиент-специ…

> - [4. Десять областей применения](#4-десять-областей-применения)   - [4.1. Область 1 — Работники знаний на распределённых рынках](#41-область-1-работники-знаний-на-распределённых-рынках)   - [4.2. Обл…

---

### 81% — `docs/obsidian/02-anthropic-vacancies/140-3-three-inter-layer-protocols.md` vs `docs/nautilus/double-triangle-architecture/03-three-inter-layer-protocols.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Routing semantics.** Messages are routed by the meta-agent  based on: - Ownership: which Node owns the relevant artifact - Expertise: which Node has the required domain knowledge - Availability: whi…

> **Failure modes:** Routing loops, context fragmentation (details  lost in translation), escalation spirals where every conflict  reaches human review. These are genuinely unsolved and require  empiric…

> **Why this protocol matters.** Without Protocol 3, humans become  routing bottlenecks. Every cross-Node coordination requires  humans to manually translate from their assistants' findings to  team con…

---

### 81% — `docs/obsidian/02-anthropic-vacancies/170-1-the-cinderella-syndrome-why-quality-stays-invisi.md` vs `docs/nautilus/representative-agent-layer-en/01-cinderella-syndrome.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - [1. The Cinderella Syndrome: Why Quality Stays Invisible](#1-the-cinderella-syndrome-why-quality-stays-invisible)   - [1.1. The Pattern](#11-the-pattern)   - [1.2. Anecdotal Illustration](#12-anecdo…

> A simple economic simulation game from the early 2000s,  described by an early reader of this concept, illustrated this  pattern starkly. In the game, a player could invest in  competing computer comp…

> Throughout history, civilizations have developed institutional  solutions to this asymmetry. The pattern is consistent: **a  representative class** emerges between value creators and  value seekers, t…

---

### 81% — `docs/obsidian/02-anthropic-vacancies/156-2-target-populations.md` vs `docs/nautilus/okwf-concept/02-target-populations.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Example use cases**: - Blind contributor working on screen reader AI improvements - Chronic fatigue patient contributing health AI research    during good hours - Person with Sozialgericht experienc…

> - [2. Target Populations](#2-target-populations)   - [2.1. Retired Experts with Remaining Intellectual Capacity](#21-retired-experts-with-remaining-intellectual-capacity)   - [2.2. Disabled Specialist…

> **Unique value proposition from OKWF**: - Foundation-handled compliance (single legal interface for    contributors globally) - Persistent professional identity across engagements - Reputation portabl…

---

### 81% — `docs/obsidian/02-anthropic-vacancies/145-8-call-to-action.md` vs `docs/nautilus/double-triangle-architecture/08-call-to-action.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Public infrastructure.** Pattern libraries in domains like  legal knowledge, medical protocols, educational curricula have  public good properties. Government funding for public pattern  libraries (…

> I am a single author with personal constraints (GdB 70, Pflegegrad  2–3, ongoing Sozialgericht proceedings). I am not a full research  team. Collaboration, critique, and contribution from others are  …

> - [8. Call to Action](#8-call-to-action)   - [8.1. For Researchers](#81-for-researchers)   - [8.2. For Practitioners](#82-for-practitioners)   - [8.3. For Founders and Organizations](#83-for-founders-…

---

### 81% — `docs/obsidian/02-anthropic-vacancies/123-portal-mcp-py.md` vs `docs/02-anthropic-vacancies/123-portal-mcp-py.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> def _q6_bfs(start: str, max_distance: int) -> list[str]:     """BFS over 6-bit hypercube, return all vertices within max_distance."""     visited: dict[str, int] = {start: 0}     queue: list[str] = [s…

> # ============================================================ # MCP SDK imports # ============================================================ # # We use the official MCP Python SDK. If not installed…

> def portal_query_one(repo: str, query: str, limit: int = 20) -> dict[str, Any]:     """Query a single adapter by name."""     portal = get_portal()     adapter = portal.adapters.get(repo)     if adapt…

---

### 80% — `docs/obsidian/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` vs `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> «Обучай» — российский AI-сервис для школьных учителей, запущенный осенью 2025 года Константином Чукавиным (тогда 25 лет, учителем и образовательным предпринимателем в Петербурге) вместе с разработчико…

> Предпосылкой стало собственное наблюдение Чукавина во время преподавания: учителя тратят приблизительно 20 неоплачиваемых часов в неделю на рутинные задачи — подготовку материалов к урокам, генерацию …

> 1. **Встроенный профессиональный контекст**: Да    (ФГОС, методологии) 2. **Специализация на единственной профессии**:    Да (только учителя) 3. **Дополнение, не замена**: Да (учитель остаётся    отве…

---

_...и ещё 277 пар._

> Файлы не удалялись автоматически. Проверьте вручную и удалите ненужные.
