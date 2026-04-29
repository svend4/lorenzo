# Отчёт о дублировании

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

Порог сходства: **0.5**  
Точных дублей: **0**  
Похожих пар: **175**

## Похожие файлы (Jaccard ≥ 0.5)

### 100% — `docs/02-anthropic-vacancies/16-history.md` vs `docs/nautilus/npp-v1-0/04-passport.md`

**Общих абзацев:** 1  
**Примеры совпадений:**

> Passports MAY быть на любом языке. Для международной видимости  RECOMMENDED иметь минимум две секции: primary language автора +  English. Рекомендуется формат с параллельными разделами, а не  отдельны…

---

### 88% — `docs/02-anthropic-vacancies/192-2-исторические-прецеденты-агенты-как-цивилизационн.md` vs `docs/nautilus/representative-agent-layer-ru/02-istoricheskie-pretsedenty.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Механика**: Смешанная — некоторые финансируются государством (юридическая помощь, омбудсмены), некоторые коммерческие (иммиграционные консультанты, налоговые подготовители), некоторые добровольчески…

> 1. **Экономическая жизнеспособность требует достаточной ценности клиента** — агентам нужна комиссия, чтобы выжить 2. **Крупные агентства обслуживают крупных клиентов** — начинающие создатели исключены…

> **Ограничения**: Экономически жизнеспособно только для клиентов с достаточно высоким заработком, чтобы 10-20% комиссии стоили того для агента. Авторы литературной фантастики, например, часто не могут …

---

### 82% — `docs/02-anthropic-vacancies/173-4-ten-domains-of-application.md` vs `docs/nautilus/representative-agent-layer-en/04-ten-domains.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **What's different**: Proactive advocacy. Agent surfaces  opportunities for clients without requiring worker's manual  search. Reduces caseload-fatigue. Helps social workers serve  more clients more e…

> **Agent function**: Track condition. Alert to upcoming  appointments, refills, lab results. Translate medical  communications. Monitor for new treatments, clinical trials.  Coordinate among providers …

> **What's different**: Owner can focus on craft (their  restaurant, their consulting, their small workshop) while  agent handles business-development overhead. Particularly  valuable for micro-entrepre…

---

### 82% — `docs/02-anthropic-vacancies/261-8-seven-domains-of-application.md` vs `docs/nautilus/composite-skills-agents/08-seven-domains.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Typical configurations**: A primary care physician working  in a rural clinic with elderly patients faces different  challenges from a specialist working in tertiary care. Even  within specialties, …

> **Sub-agent specializations might include**: Programming languages,  architecture patterns, deployment platforms, security  disciplines, performance engineering, testing approaches,  specific applicat…

> **Typical configurations**: A jazz pianist who teaches has  different needs from a classical violinist, who has different  needs from an electronic music producer. Each builds their  own configuration…

---

### 81% — `docs/02-anthropic-vacancies/194-4-десять-областей-применения.md` vs `docs/nautilus/representative-agent-layer-ru/04-desyat-oblastey.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Функция агента**: Централизовать информацию по нескольким контекстам ухода. Мониторить изменения услуг. Планировать и напоминать. Составлять коммуникации. Выявлять ресурсы поддержки для самого опеку…

> **Функция агента**: Отслеживать статус каждого клиента в нескольких системах услуг. Предупреждать работника о сроках, возможностях, осложнениях. Составлять рутинные коммуникации. Готовить клиент-специ…

> **Что отличается**: Проактивная адвокация. Агент выводит возможности для клиентов без необходимости ручного поиска работником. Снижает усталость от нагрузки. Помогает социальным работникам обслуживать…

---

### 79% — `docs/02-anthropic-vacancies/256-3-what-makes-a-composite-skills-agent.md` vs `docs/nautilus/composite-skills-agents/03-what-makes-csa.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Property 4 — Coordinated Single-Surface Interaction.** The  principal interacts with the composite agent as a coherent  whole, not with each sub-agent separately. The composite agent's  job is to ro…

> **Function 1 — Routing.** When the principal poses a question  or task, the composite agent determines which sub-agents are  relevant. Some questions need only one sub-agent. Others need  several in c…

> **Function 3 — Disagreement Management.** When sub-agents  provide conflicting recommendations, the composite agent  presents the disagreement clearly to the principal: "Sub-agent  A recommends X for …

---

### 79% — `docs/02-anthropic-vacancies/263-10-risks-specific-to-composite-architectures.md` vs `docs/nautilus/composite-skills-agents/10-risks.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Mitigations**: - Version pinning (configurations specify exact sub-agent    versions, opt into updates) - Compatibility testing when sub-agents update - Notification of significant behavioral change…

> **Mitigations**: - Recommendation system explicitly suggests "growth-edge"    sub-agents outside principal's current configuration - Regular configuration reviews with prompts to consider    unfamilia…

> **Scenario**: A configuration appears to work well, but its  output depends on subtle interactions between specific sub-agents.  When one sub-agent updates, the configuration's output changes  in ways…

---

### 78% — `docs/02-anthropic-vacancies/237-6-риски-специфичные-для-этой-категории.md` vs `docs/nautilus/professional-colleague-agents-ru/06-riski.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - [6. Риски, специфичные для этой категории](#6-риски-специфичные-для-этой-категории)   - [6.1. Риск: Коллапс Опосредования](#61-риск-коллапс-опосредования)   - [6.2. Риск: Атрофия Навыков у Новых Пра…

> **Конкретный пример**: Младший юрист использует параюридический AI для всех рутинных составлений. Никогда лично не развивает навыки составления. Не может составлять, когда AI недоступен. Не может крит…

> **Конкретный пример**: Один AI-провайдер обслуживает 90% учителей. Дизайнерские решения провайдера эффективно определяют педагогику национально. Ценообразование и условия провайдера определяют рабочие…

---

### 78% — `docs/02-anthropic-vacancies/255-2-the-twenty-one-teachers-pattern.md` vs `docs/nautilus/composite-skills-agents/02-twenty-one-teachers-pattern.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Teaching.** A teacher whose effectiveness comes from combining  subject expertise (mathematics), pedagogical approach  (constructivist), specialty (working with neurodivergent  students), and cultur…

> - [2. The Twenty-One Teachers Pattern](#2-the-twenty-one-teachers-pattern)   - [2.1. The Story](#21-the-story)   - [2.2. What This Pattern Reveals](#22-what-this-pattern-reveals)   - [2.3. Why This Pa…

> - One taught a particular asana lineage - Another, specific pranayama techniques - Another, the philosophical foundations - Another, therapeutic applications for back pain - Another, work with mental …

---

### 77% — `docs/02-anthropic-vacancies/158-4-proposed-infrastructure.md` vs `docs/nautilus/okwf-concept/04-proposed-infrastructure.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Why pattern library is critical**: - Compounds knowledge across contributors - Enables specialized work without reinvention - Preserves contributor intellectual property through    anonymization - C…

> - Contributors log in (community identity), pick up tasks    (guild structure, pattern library), execute work (Nautilus    substrate + Double-Triangle with assistants), receive    compensation (econom…

> **Principles**: - **Dignified baseline**: all active contributors receive    stipend meeting minimum threshold - **Contribution bonuses**: measurable high-impact work    generates additional compensat…

---

### 76% — `docs/02-anthropic-vacancies/156-2-target-populations.md` vs `docs/nautilus/okwf-concept/02-target-populations.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Example use cases**: - Senior engineer in Belarus contributing to AI safety research - ML researcher in Argentina working on multilingual models - Medical AI specialist in Kenya contributing to glob…

> **Characteristics**: - Technical expertise often comparable to non-disabled peers - Variable daily capacity (good days and bad days) - Need flexibility impossible in most full-time roles - Often exper…

> - [2. Target Populations](#2-target-populations)   - [2.1. Retired Experts with Remaining Intellectual Capacity](#21-retired-experts-with-remaining-intellectual-capacity)   - [2.2. Disabled Specialist…

---

### 76% — `docs/02-anthropic-vacancies/235-4-архитектура-профессиональных-коллег-агентов.md` vs `docs/nautilus/professional-colleague-agents-ru/04-arkhitektura.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Рабочими инструментами**, которые использует профессия. Юристы используют конкретные системы управления делами. Учителя используют конкретные системы электронных журналов. Врачи используют конкретны…

> Эта работа по интеграции значительна. Это также то, где многие проекты «AI для X профессии» проваливаются — построив прекрасного агента, которого ни один практикующий не может вписать в свой существую…

> **Принцип Осведомлённости об Обновлениях.** Существенные обновления базы знаний выводятся на поверхность практикующему. «Соответствующий статут был изменён на прошлой неделе. Ваше текущее обращение мо…

---

### 75% — `docs/02-anthropic-vacancies/161-7-phased-rollout-plan.md` vs `docs/nautilus/okwf-concept/07-phased-rollout.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Success criteria**: - 50 active contributors engaged - 5-10 completed pilot projects with measurable quality    outcomes - Working pattern library with 100+ public patterns - Contributor satisfactio…

> OKWF evolves into trusted infrastructure for distributed  expert work globally. Multiple foundations and corporate  partners sustain operations. Contributors span every continent.  Specialization exte…

> **Risk mitigations**: - If anchor commitment fails: pivot to foundation-only funding    with delayed, smaller pilot - If core team assembly slow: partner with established entity    (e.g., Mozilla Foun…

---

### 75% — `docs/02-anthropic-vacancies/234-3-эмпирический-кейс-обучай.md` vs `docs/nautilus/professional-colleague-agents-ru/03-keys-obuchay.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Предпосылкой стало собственное наблюдение Чукавина во время преподавания: учителя тратят приблизительно 20 неоплачиваемых часов в неделю на рутинные задачи — подготовку материалов к урокам, генерацию …

> «Обучай» также иллюстрирует риски категории. Несколько комментаторов публично заметили: «Ученики "делают" дз с ИИ, учителя с ним же генерируют задания и проверяют. Школы скоро можно будет закрыть за н…

> - [3. Эмпирический кейс: «Обучай»](#3-эмпирический-кейс-обучай)   - [3.1. Предыстория](#31-предыстория)   - [3.2. Функциональное описание](#32-функциональное-описание)   - [3.3. Траектория развёртыван…

---

### 73% — `docs/02-anthropic-vacancies/162-8-risk-analysis.md` vs `docs/nautilus/okwf-concept/08-risk-analysis.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Mitigations**: - Rigorous selection in Phase 1 - Explicit quality gates at each guild level - Peer review processes - AI-assisted consistency checking - External quality auditing - Willingness to re…

> **Mitigations**: - Explicit regulatory counsel from early stages - Proactive engagement with regulators - Conservative approach (pay more in taxes, compliance    overhead rather than risk) - Legal inf…

> **Mitigations**: - Aggressive outreach during Phase 1 recruitment - Partnership with existing advocacy organizations - Focused pilot in high-density population area - Built-in pivot capacity (can cons…

---

### 73% — `docs/02-anthropic-vacancies/144-7-open-questions.md` vs `docs/nautilus/double-triangle-architecture/07-open-questions.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Participants may game the system: - Nodes may present inflated deliverables to meta-agent - Meta-agents may favor some Nodes over others - Assistants may develop unauthorized private goals - Bad actor…

> **Who decides who meta-agent coordinates?** Node's participation  in a team means meta-agent has authority over Node's task  assignment. But what if Node disagrees with an assignment? What  is the "ex…

> Empirical observation from the reference implementation  deployment (one person, 4 months): **accelerated output, but  also increased coordination overhead**. 70 repositories created,  but several in …

---

### 73% — `docs/02-anthropic-vacancies/171-2-historical-precedents-agents-as-civilizational-i.md` vs `docs/nautilus/representative-agent-layer-en/02-historical-precedents.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Limitations**: Severely underfunded for the scale of need.  In disability rights, social welfare, immigration — most  people who need representation cannot access it. This is  the largest domain whe…

> 1. **Decoupling expertise from market interface** — value     creator focuses on creation 2. **Aligned incentive structure** — agent succeeds when     client succeeds (commission) 3. **Accumulated rel…

> - [2. Historical Precedents: Agents as Civilizational Innovation](#2-historical-precedents-agents-as-civilizational-innovation)   - [2.1. Literary and Performance Agents](#21-literary-and-performance-…

---

### 73% — `docs/02-anthropic-vacancies/195-5-архитектурная-спецификация.md` vs `docs/nautilus/representative-agent-layer-ru/05-arkhitekturnaya-spetsifikatsiya.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Компонент 1 — Профиль Принципала**: Всестороннее представление экспертизы, способностей, предпочтений, истории, целей, ограничений принципала. Создаётся через интервью на стадии онбординга, уточняет…

> **Компонент 2 — Движок Обнаружения**: Постоянно мониторит соответствующие области в поисках возможностей. Источники включают: публичные доски вакансий, RSS-каналы, партнёрские системы, коллегиальные с…

> **Пользовательский Интерфейс**: Мульти-модальный доступ (веб, мобильный, голос), соответствующий потребностям доступности принципала. Особенно важно для пожилых, инвалидов или незнакомых с технологиям…

---

### 72% — `docs/02-anthropic-vacancies/145-8-call-to-action.md` vs `docs/nautilus/double-triangle-architecture/08-call-to-action.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Empirical studies.** Document existing deployments (including  the Nautilus reference implementation) with formal measurements:  coordination overhead, task completion rates, conflict frequency,  pa…

> **Comparative analysis.** Compare Double-Triangle deployments  against single-triangle baselines (centralized AI assistants vs.  centralized multi-agent systems). Quantify productivity,  coordination …

> **Product opportunities.** Existing AI tools implement single  triangles. Double-Triangle implementations represent differentiated  product opportunities across many domains. First-movers will  define…

---

### 72% — `docs/02-anthropic-vacancies/215-4-architecture-of-professional-colleague-agents.md` vs `docs/nautilus/professional-colleague-agents-en/04-architecture.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Strategy 3 — Authority Integration.** Direct integration with authoritative sources (legal databases, medical guidelines, educational standards). Auto-update as sources update. Most rigorous, requir…

> **QA Mechanism 1 — Confidence Indicators.** The agent reports its confidence in each output element. High confidence: "Standard format applied per current regulation." Low confidence: "Approach uncert…

> This is the most expensive layer to build and the most valuable competitive moat. A high-quality professional knowledge base for German social law, for example, represents thousands of hours of expert…

---

### 71% — `docs/02-anthropic-vacancies/262-9-integration-with-okwf-infrastructure.md` vs `docs/nautilus/composite-skills-agents/09-okwf-integration.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Phase 0** (Months 1-12): Foundation establishment, initial  sub-agent set for one profession (perhaps SGB social law). Build  20-30 narrow sub-agents plus coordinator. Pilot with 5-10  practitioners…

> Cost increases (€1.5M vs €430K for Year 1), but produces a  genuinely useful infrastructure that scales to multiple  adjacent legal domains and supports practitioners' actual  diverse practices rather…

> Composite Skills Agents and Representative Agents work together  naturally: - The composite agent supports the practitioner's work - The representative agent supports the practitioner's external    po…

---

### 71% — `docs/02-anthropic-vacancies/233-2-что-делает-агента-профессиональным-коллегой.md` vs `docs/nautilus/professional-colleague-agents-ru/02-chto-delaet-pka.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Функция 5 — Поиск знаний.** Обеспечивать быстрый доступ к профессиональным базам знаний — прецеденты, клиническая литература, методологические ссылки, обновления регуляций. Сокращает время исследова…

> **Свойство 5 — Массовое тиражирование.** Один и тот же дизайн агента обслуживает всех практикующих профессии. Кастомизация под конкретного пользователя ограничена пользовательскими предпочтениями и ра…

> **Функция 3 — Автоматизация рутинных задач.** Заниматься повторяющимися компонентами профессиональной работы, которые потребляют непропорционально много времени относительно ценности. Ввод оценок. Зап…

---

### 71% — `docs/02-anthropic-vacancies/191-1-синдром-золушки-почему-качество-остаётся-невидим.md` vs `docs/nautilus/representative-agent-layer-ru/01-sindrom-zolushki.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Существует повторяющаяся асимметрия на современных рынках — рынках труда, внимания, возможностей, услуг. Качество и видимость **слабо коррелируют**, а иногда и **отрицательно коррелируют**. Те, кто пр…

> Мы рассмотрим эти прецеденты в Разделе 2. Предложение этой статьи прямолинейно: **AI теперь делает этот представительский класс доступным и доступным в масштабах, ранее невозможных**. Это и есть Слой …

> Это не наивная экономика — это верное представление динамики внимания. Качество само по себе **недостаточно** для рыночного успеха. Качество плюс видимость побеждает. Только видимость с посредственным…

---

### 69% — `docs/02-anthropic-vacancies/258-5-configuration-how-principals-build-their-ensembl.md` vs `docs/nautilus/composite-skills-agents/05-configuration-ensembles.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> 1. **Initial AI recommendation** based on principal's stated     profile generates a starting configuration 2. **Self-directed exploration** lets principal browse, adjust,     add specializations they…

> A principal's configuration is not static. Specializations  change over time: - New specializations enter their work as careers evolve - Old specializations become less relevant as priorities shift - …

> **Approach 2 — AI-assisted recommendation.** The composite  agent (or a separate recommendation system) analyzes the  principal's stated goals, work history, and preferences, then  suggests an initial…

---

### 69% — `docs/02-anthropic-vacancies/143-6-four-deployment-domains.md` vs `docs/nautilus/double-triangle-architecture/06-four-deployment-domains.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Concrete deployment.** An individual (the first author,  svend4) currently engages with Sozialgericht Dresden on cases  S 6 SO 58/26 ER and S 7 SO 99/25. Personal workflow already  exhibits lower tr…

> **Novel opportunity.** Open-source projects traditionally lack  scalable coordination. A Double-Triangle deployment could enable  small maintainer teams to manage much larger contributor  communities …

> - [6. Four Deployment Domains](#6-four-deployment-domains)   - [6.1. Humanities Domain (Legal, Medical, Social)](#61-humanities-domain-legal-medical-social)   - [6.2. Project Management Domain](#62-pr…

---

### 69% — `docs/02-anthropic-vacancies/254-1-why-the-binary-view-is-incomplete.md` vs `docs/nautilus/composite-skills-agents/01-why-binary-incomplete.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> Importantly, the differentiation usually comes not from  inventing entirely novel skills but from **specific combinations  of generally available skills**. A jazz pianist who also studied  classical c…

> This second characteristic is not exceptional but typical. It  is **how professions actually contain their members**. The  profession provides the genus; specialization provides the  species; combinat…

> **They are differentiated within the profession.** No two  musicians are identical. No two lawyers practice exactly the  same way. Each combines particular specializations, particular  influences, par…

---

### 69% — `docs/02-anthropic-vacancies/142-5-pattern-library-as-bridge-between-triangles.md` vs `docs/nautilus/double-triangle-architecture/05-pattern-library-bridge.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> - **Start** of work: instance inherits from patterns (use existing    knowledge) - **During** work: instance cites authorities (ground work in    source material) - **After** work: instance contribute…

> Double-Triangle systems face a fundamental question: how do  assistants in different Nodes' lower triangles share knowledge  about best practices, conventions, and reusable patterns, without  each Nod…

> - [5. Pattern Library as Bridge Between Triangles](#5-pattern-library-as-bridge-between-triangles)   - [5.1. The Problem of Shared Knowledge](#51-the-problem-of-shared-knowledge)   - [5.2. Pattern Lib…

---

### 69% — `docs/02-anthropic-vacancies/213-2-what-makes-a-professional-colleague-agent.md` vs `docs/nautilus/professional-colleague-agents-en/02-what-makes-pca.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Property 2 — Single-Profession Specialization.** The agent serves one defined profession (or one defined sub-specialty). Not "multiple professions". Not "general professional work." This focus enabl…

> **Property 5 — Mass Replication.** The same agent design serves all practitioners of the profession. Per-user customization is limited to user preferences and work-in-progress. The professional contex…

> **Function 1 — Generation in Professional Format.** Produce drafts, materials, plans, analyses in formats specific to the profession. A teaching agent generates lesson plans in educational formats. A …

---

### 67% — `docs/02-anthropic-vacancies/292-что-отсутствует-слой-b.md` vs `docs/nautilus/infrastructure-layer-b-ru/03-otsutstvuet-sloy-b.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **AI-сотрудничество как первичная операция.** Каждый тред, каждый документ, каждая аннотация могли бы развиваться в сотрудничестве с AI. AI имел бы доступ к полному контексту проекта — не только к тек…

> **Перекрёстные ссылки.** Документы и треды обсуждений могли бы ссылаться друг на друга явно. Ссылка из Документа 7 на Документ 6 была бы реальной ссылкой, не просто текстом. Переход по ссылке показыва…

> **Версионирование без кодо-ориентации.** Документы могли бы версионироваться, с показанными диффами, но без культурных накладных расходов на pull requests и процессы ревью кода. Правки могли бы быть с…

---

### 67% — `docs/02-anthropic-vacancies/277-what-s-missing-layer-b.md` vs `docs/nautilus/infrastructure-layer-b-en/04-whats-missing-layer-b.md`

**Общих абзацев:** 3  
**Примеры совпадений:**

> **Annotation on documents.** Specific sections of documents  could be annotated with comments. Comments could be threaded.  Other AI agents (or human collaborators) could respond to  comments. Annotat…

> **Promotion workflow.** Content developed in Layer B could be  promoted to Layer C (committed to repository) when stable  enough. Content from Layer A (chat) could be promoted to Layer  B when worth p…

> **Cross-references.** Documents and discussion threads could  link to each other explicitly. A reference from Document 7 to  Document 6 would be a real link, not just text. Following the  link would s…

---

_...и ещё 145 пар._

> Файлы не удалялись автоматически. Проверьте вручную и удалите ненужные.

<!-- see-also -->

---

**Смотрите также:**
- [01-response-en](docs/nautilus/community-discussions/agent-changes-reality/01-response-en.md)
- [SOURCE_MAP](docs/SOURCE_MAP.md)
- [READING_TIME](docs/READING_TIME.md)
- [01-completing-loop](docs/nautilus/transmission-box/01-completing-loop.md)

